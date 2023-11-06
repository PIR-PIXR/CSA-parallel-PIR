# DP-PIR + Coloring

---
## Experimental setup
For simplicity, we ran our experiments on a local Ubuntu 22.04.1 environment (Intel Core i5-1035G1 CPU @1.00GHz×8, 15GiB System memory). We employed two servers and one client, which acted as multiple clients, following the same settings described in [DP-PIR](https://github.com/multiparty/DP-PIR/tree/usenix2022).

<p align="center">
  <img width="1000" height="400" src="https://github.com/cnquang/CPIR/assets/87842051/c3729bb6-133c-49f5-9b29-00793ce776bc"> 
</p>
<strong> Figure 1.</strong> The computation time for DP-PIR and DP-PIR+Coloring, both online and offline, was evaluated from $n = 2^{10}$ to $n = 2^{16}$ while retrieving 6000 Merkle proofs privately.

---
## Compiling DP-PIR + Coloring
### Installing Libraries

- #### g++-11
      $ sudo apt install g++-11
      $ sudo apt update
      $ sudo apt upgrade
- #### Bazel 4.2.1
      $ curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
      $ sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
      $ echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
      $ sudo apt update
      $ sudo apt install bazel-4.2.1
      $ sudo apt install bazel-bootstrap
- #### Golang
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install golang-go  
- #### npm
      $ sudo apt install npm
      $ npm install express

### Executing DP-PIR and DP-PIR+Coloring
      $ sudo sysctl -w net.core.rmem_max=123289600
      $ sudo sysctl -w net.core.wmem_max=123289600
      $ cd /path/to/experiments/orchestrator
- #### On your local machine
  ##### Open the first terminal
      $ cd /path/to/experiments/orchestrator
      $ node main.js
  ##### Open the second terminal
      $ ./experiments/local.sh 2 1
  ##### Return to the first terminal
      $ load dpPIR

---
## ACKNOWLEDGMENTS
This work was modifiered from [DP-PIR](https://github.com/multiparty/DP-PIR/tree/usenix2022) accompanying the Usenix Security 2022 paper "Batched Differentially Private Information Retrieval".
