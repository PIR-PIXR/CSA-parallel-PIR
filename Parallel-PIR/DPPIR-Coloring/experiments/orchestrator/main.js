// Dependencies.
const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const ipaddr = require('ipaddr.js');

const Cmd = require('./cmd.js');
const Orchestrator = require('./orchestrator.js');

// Configurations.
const PORT = 8000;

// Helpers.
function formatIP(ipString) {
  if (ipaddr.IPv4.isValid(ipString)) {
    return ipString;
  } else if (ipaddr.IPv6.isValid(ipString)) {
    var ip = ipaddr.IPv6.parse(ipString);
    if (ip.isIPv4MappedAddress()) {
      return ip.toIPv4Address().toString();
    } else {
      // ipString is IPv6
      throw 'Cannot handle ipv6 ' + ipString;
    }
  } else {
    throw 'Invalid IP! ' + ipString;
  }
}

// Create app.
const app = express();
app.use(bodyParser.text({ inflate: true, limit: '50mb', type: 'text/plain' }));

// Create an instance of the orchestrator.
const orchestrator = new Orchestrator();

/*** SERVER ROUTES ***/
// Registering IPs with orchestrator.
app.get('/giveip/server', (req, res) => {
  const ip = formatIP(req.connection.remoteAddress);
  const id = orchestrator.addServerWorker(ip);
  res.send(id.toString());
});
app.get('/giveip/client', (req, res) => {
  const ip = formatIP(req.connection.remoteAddress);
  const id = orchestrator.addClientWorker(ip);
  res.send(id.toString());
});

// (DPPIR) Experiment configuration and table files.
/*
app.get('/table/:id', (req, res) => {
  const id = parseInt(req.params.id);
  res.send(orchestrator.getWorkerById(id).experiment.table);
});
*/
app.get('/config/:id', async function (req, res) {
  const id = parseInt(req.params.id);
  const experiment = orchestrator.getWorkerById(id).experiment;
  if (experiment.serversNum != experiment.servers.length) {
    res.send("WAIT");
  } else if (experiment.config == null) {
    experiment.generateTableAndConfigurations();
    res.send(experiment.config);
  } else if (experiment.config == "PENDING") {
    res.send("WAIT");
  } else {
    res.send(experiment.config);
  }
});

// Returns 1 if the worker's job should be killed, 2 if we need its log, and 0
// otherwise.
app.get('/shouldkill/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const worker = orchestrator.getWorkerById(id);
  if (worker.shouldLog()) {
    res.send("2\n");
  } else if (worker.shouldKill()) {
    res.send("1\n");
  } else {
    res.send("0\n");
  }
});

// Shows the current log of the worker, returns nothing.
app.post('/showlog/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const log = req.body;
  orchestrator.getWorkerById(id).showLog(log);
  res.send("");
});

// Ping when ready to receive a job.
app.get('/ping/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const worker = orchestrator.getWorkerById(id);
  const experiment = orchestrator.assignExperiment(worker);
  if (experiment != null) {
    res.send(experiment.serialize(worker));
  } else {
    res.send("WAIT");
  }
});

// Report finishing.
app.post('/done/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const result = req.body;
  const worker = orchestrator.getWorkerById(id);
  const experiment = worker.experiment;
  const filePath = experiment.resultFile(worker);
  fs.writeFileSync(filePath, result);
  worker.finished();
  experiment.finished(worker);
  res.send("");
});

app.listen(PORT, () => {
  console.log(`Orchestrator listening at http://localhost:${PORT}`);
  const cmdInterface = new Cmd(orchestrator);
  cmdInterface.Listen();
});
