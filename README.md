<p align="center">
  <img width="500" height="200" src="https://github-production-user-asset-6210df.s3.amazonaws.com/87842051/293288659-bba521cd-cf66-4a19-8246-f76475631963.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T232401Z&X-Amz-Expires=300&X-Amz-Signature=208fb51c88b00c05114996376306e29d75b4ae736590a1c25e5211987e80392c&X-Amz-SignedHeaders=host&actor_id=87842051&key_id=0&repo_id=474514659">
</p>

# Parallel Private Retrieval of Merkle Proofs via Tree Colorings

### Abstract
Motivated by a practical scenario in blockchains in which a client, who possesses a transaction, wishes to privately verify that the transaction actually belongs to a block, we investigate the problem of private retrieval of Merkle proofs (i.e. proofs of inclusion/membership) in a Merkle tree.
In this setting, one or more servers store the nodes of a binary tree (a Merkle tree), while a client wants to retrieve the set of nodes along a root-to-leaf path (i.e. a Merkle proof, after appropriate node swapping operations), without letting the servers know which path is being retrieved. 
We propose a method that partitions the Merkle tree to enable parallel private retrieval of the Merkle proofs. The partitioning step is based on a novel tree coloring called \textit{ancestral coloring} in which nodes that have ancestor-descendant relationship must have distinct colors. To minimize the retrieval time, the coloring is required to be balanced, i.e. the sizes of the color classes differ by at most one. We develop a fast algorithm to find a balanced (in fact, any) ancestral coloring in almost linear time in the number of tree nodes, which can handle trees with billions of nodes in a few minutes. Our partitioning method can be applied on top of any private information retrieval scheme, leading to the minimum storage overhead and fastest running times compared to existing approaches. You can find a copy of the paper [here](https://arxiv.org/abs/2205.05211)

---
## Main Contributions

- We propose an efficient approach to parallelize the private retrieval of the Merkle proofs based on the novel concept of balanced ancestral coloring of rooted trees. Our approach achieves the lowest possible storage overhead (no redundancy) and lowest computation complexity compared to existing approaches.

- We establish a necessary and sufficient condition for the existence of an ancestral coloring with arbitrary color sequences.

- We develop a \textit{divide-and-conquer} algorithm to generate an ancestral coloring for \textit{every} feasible color sequence with time complexity $\Theta(n\log\log(n))$ on the perfect binary tree of $n$ leaves. The algorithm can color a tree of two billion nodes in under five minutes.

- Finally, we implement and evaluate the empirical performance of our approach using [SealPIR](https://eprint.iacr.org/2017/1142.pdf) and [DP-PIR](https://www.usenix.org/system/files/sec22-albab.pdf) as the underlying PIR schemes.

---
## Problem Description

Given a (perfect) Merkle tree stored at one or more servers, we are interested in designing an _efficient_ private retrieval scheme in which a client can send queries to the server(s) and retrieve an arbitrary Merkle proof without letting the server(s) know which proof is being retrieved. This problem is equivalent to the problem of designing an efficient private retrieval scheme for every root-to-leaf path in a perfect binary tree (with depth $h$ and $n=2^h$ leaves).
An efficient retrieval scheme should have _low storage, computation, and communication overheads_.
The server(s) should not be able to learn which path is being retrieved based on the queries received from the client. We do not need to formally define privacy because it is nonessential to our contribution and also because the privacy of our solution is guaranteed by the privacy of the underlying PIR scheme straightforwardly.

We assume a setting in which the nodes of a Merkle/perfect binary tree are stored at one multi-core server or multiple (single-core) servers. Hence, the system is capable of parallel processing. This is a key assumption of our approach to work. For brevity, we will use the multi-server setting henceforth. To simplify the discussion, we assume that the servers have the same storage/computational capacities and will complete the same workload simultaneously.

<p align="center">
  <img width="600" height="300" src="https://github.com/cnquang/cnquang/assets/87842051/bd15563b-48f7-4422-be5b-02800e704cd6">
</p>
<strong> Fig. 1.</strong> An illustration of our coloring-based parallel private retrieval of Merkle proofs. First, the nodes of the Merkle tree of height $h$ are partitioned into $h$ parts/color classes/sub-databases, each of which is stored by a server. The client runs $h$ PIR schemes with these $h$ servers in parallel to privately retrieve $h$ nodes of the Merkle proof, one from each server. Here, PIR.Query and PIR. Answer refers to the query and answer generations in the corresponding PIR scheme.

---
## [Bitcoin Datasets in Real-time](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/BitcoinDataset)
We utilized our Java code to gather 200 Bitcoin Blocks in \textit{real-time} from the \textit{latest} Block 813562, containing 2390 transactions, mined on 2023-10-24 at 09:52:26 GMT +11, to Block 813363, which included 2769 transactions and was mined on 2023-10-23 at 04:13:24 GMT +11. On average, within the dataset we collected, there were 1839 transactions in each Block. The number of transactions in each Bitcoin Block typically ranges from 1000 to 4500, and the number of active addresses per day is more than 900K. To interface with the [Blockchain Data API](https://www.blockchain.com/explorer/api/blockchain_api) for collecting real-time Bitcoin Blocks in JSON format, we used HttpURLConnection and [Google GSON](https://github.com/google/gson) 2.10.1.
Our work focuses on the perfect Merkle tree, so we collected the latest Bitcoin transactions to make the Merkle tree perfect. As Bitcoin, our Java code generated the Block's Merkle tree using the SHA-256 hash function. Hence, each tree node had a size of 256 bits (hash digit size).

### Executing MainDatasets.java
The output will generate many datasets in the Datasets folder for experimental purposes.

      $ cd path/to/BitcoinDataset
      $ javac -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainDatasets.java
      $ java -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainDatasets

### Executing MainBitcoinAPI.java
This function collects Bitcoin Blocks in real-time, and we provided many functions to interact with [Bitcoin Data API](https://www.blockchain.com/explorer/api/blockchain_api).

      $ cd path/to/BitcoinDataset
      $ javac -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainBitcoinAPI.java
      $ java -cp /path/to/BitcoinDataset/gson-2.10.1.jar:/path/to/BitcoinDataset MainBitcoinAPI

---
## [CSA: Color-Splitting Algorithm](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/CSA)

We develop a divide-and-conquer CSA algorithm that generates a balanced and unbalanced ancestral coloring. For balanced ancestral coloring, the algorithm's running time is almost linear in the number of tree nodes, the running time is in O(N*loglog(N)). The flexibility of our algorithm establishes the existence of optimal combinatorial patterned batch codes corresponding to the case of servers with heterogeneous storage capacities. At the high level, the algorithm colors two sibling nodes simultaneously, proceeds recursively down to the two subtrees and repeats the process while maintaining the Ancestral Property. Using our algorithm, we can generate a balanced ancestral coloring for the tree $T(30)$ (around two billion nodes) remarkably fast in under five minutes (with 16GB allocated for Java's heap memory).

### Experimental setup
We ran our experiments using the Amazone c6i.8xlarge instance (Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz, 32 vCPUs, 64GiB System Memory, 12.5 Gbps network bandwidth, all running Ubuntu 22-04 LTS). Our Java code (CSA.java) was compiled using Java OpenJDK version 11.0.19. The running times are presented in Figure 1, confirming our algorithm's theoretical complexity (almost linear). Note that the algorithm only ran on a single vCPU of the virtual machine. Our current code can handle trees of heights up to $35$, for which the algorithm took 2.5 hours to complete. For a perfect binary tree of height $h=30$, it took less than 5 minutes to produce a balanced ancestral coloring.

<p align="center">
  <img width="500" height="300" src="https://github.com/cnquang/CPIR/assets/87842051/185c01a5-a643-437e-a637-f8b02f6cbdc4">
</p>
<strong> Fig. 2.</strong> The average running times of the Color-Splitting Algorithm (CSA) when generating balanced ancestral colorings for the perfect binary trees with $n = 2^{10},2^{11},...,2^{20}$ leaves. For each $n$, the algorithm was run a hundred times, and the average running time was recorded.

---
### Compiling CSA
#### Installing Libraries

- ##### Javac
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install default-jdk

#### Executing CSA
- ##### Once Java and Javac are installed, to build CSA simply run:

      $ cd path/to/CSA
      $ javac CSA.java
      $ java CSA

- ##### To build CSA with recommended max heap size simply run:

      $ cd path/to/CSA
      $ javac CSA.java
      $ java -Xmx32g CSA
    
#### User Interface Guideline (CSA)

Take a look at the pictures below, guidelines and CSA.java comments for how to use CSA.  

<img width="415" alt="h5auto" src="https://user-images.githubusercontent.com/102839948/161372568-85df8aed-6424-4977-9853-722879624efe.png">

*Fig. 3: An example of the CSA algorithm running option A (Automatic Balanced Ancestral Coloring) when h = 5.*


<img width="575" alt="h3manual" src="https://user-images.githubusercontent.com/102839948/161372572-773c693e-bd18-4a97-b979-00bbc393fce9.png">

*Fig. 4: An example of the CSA algorithm running option B (Manual Feasible Color Sequences) with c = [3 3 8].*

---
## [One Client parallel privately retrieves a Merkle proof](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/Parallel-PIR/Parallel-SealPIR)

Our Coloring method can be applied on top of any PIR schemes, allowing us to optimize with other Batched PIR solutions following baselines:

+ [Angle et al.'s batchPIR](https://eprint.iacr.org/2017/1142.pdf) (SealPIR+PBC) employs SealPIR as the foundational PIR. Note that (SealPIR+PBC) uses $m=1.5h$ databases of size $2N/h$ each.

+ $h$-Repetition, which is a trivial solution repeated $h$ times SealPIR on top of the whole tree.

+ Proof-as-Element is applied SealPIR once on a database where each element is a Merkle proof ($h$ hashes).

+ Layer-based, which is a trivial coloring solution repeated $h$ times SealPIR on each layer of the tree.

### Experimental setup
We ran our experiments on Ubuntu 22.04.1 environment (Intel Core i5-1035G1 CPU @1.00GHz×8, 15GiB System memory) for the client side and until 30 PIR servers on Amazon t2.large instances (Intel(R) Xeon(R) CPU E5-2686 v4 @ 2.30GHz, 2 vCPUs, 8GiB System Memory). We utilize the HTTP/2 protocol in conjunction with [gRPC](https://github.com/grpc/grpc) version 35.0.0, which is developed by Google, for connecting numerous clients and servers over the network.

The main underlying PIR scheme is [SealPIR library](https://github.com/microsoft/SealPIR). We compiled our C++ code (main.cpp) with Cmake version 3.22.1 and [Microsoft SEAL version 4.0.0](https://github.com/cnquang/SEAL-4.0.0). The trees in our experiments have $n=2^{10},2^{12},\ldots,2^{20}$ leaves. The tree nodes contained the latest Bitcoin transactions datasets, and each node in the tree had a size of 256 bits, following the standard hash size (as in SHA-256). 

We compared the performance of our scheme (SealPIR+Coloring) with SealPIR as the underlying PIR and several related solutions including [SealPIR+PBC](https://eprint.iacr.org/2017/1142.pdf) and combinations of SealPIR with $h$-repetition, Proof-as-Elements, and layer-based. Note that [SealPIR+PBC](https://eprint.iacr.org/2017/1142.pdf) uses $m=1.5h$ databases of size $2N/h$ each, Proof-as-Elements uses a single proof-database containing all $n$ proofs ($h$ hashes), $h$-Repetition uses $h$ databases of size $N$ each, and layer-based uses $h$ databases of sizes $2,4,\ldots,2^h=n$. Our solution (SealPIR+Coloring) uses $h$ databases of size approximately $N/h$ each. Here, $N=2^{h+1}-2$ is the number of tree nodes (except the root) and $h$ is the height of the perfect binary trees.

<p align="center">
  <img width="600" height="300" src="https://github.com/cnquang/CPIR/assets/87842051/1b47d79a-8977-4092-a188-2c26d2579da8"> 
</p>
<strong> Fig. 5.</strong> A comparison of the server computation costs in parallel of five schemes from $n = 2^{10}$ to $n = 2^{20}$. Our coloring-based scheme outperforms others. Size of each node is 32 bytes (hash digest size).

---
### Compiling SealPIR
#### Installing Libraries

- ##### SEAL 4.0.0
      $ sudo apt install build-essential cmake clang git g++ libssl-dev libgmp3-dev
      $ sudo apt update
      $ sudo apt upgrade
      $ git clone https://github.com/cnquang/SEAL-4.0.0.git
      $ cd SEAL-4.0.0
      $ cmake -S . -B build
      $ cmake --build build
      $ sudo cmake --install build
- ##### JSON
      $ git clone https://github.com/microsoft/vcpkg
      $ ./vcpkg/bootstrap-vcpkg.sh
      $ ./vcpkg install rapidjson
- ##### Google gRPC
      $ sudo apt install -y build-essential autoconf libtool pkg-config
      $ git clone --recurse-submodules -b v1.58.0 --depth 1 --shallow-submodules https://github.com/grpc/grpc
      $ cd grpc
      $ mkdir -p cmake/build
      $ pushd cmake/build
      $ cmake -DgRPC_INSTALL=ON \
        -DgRPC_BUILD_TESTS=OFF \
        ../..
      $ make -j 4
      $ sudo make install
      $ popd

#### Executing Parallel SealPIR
      $ cd /path/to/Parallel-SealPIR
      $ cmake .
      $ make
      $ -> Generated: CXX executable pirmessage_server and CXX executable pirmessage_client
      
- ##### On your local machine
  ###### Open the first terminal as Server side (You can create as many servers as you want in the separate terminals. Make sure each server opens different port numbers)
      $ cd /path/to/Parallel-SealPIR
      $ ./pirmessage_server -port 3000
  ###### Open the second terminal as Client side
      $ Change the servers_list.txt with local IP address 127.0.0.1:3000; database file name (change the database name in the Server side to data.json); and index i in the database
      $ cd /path/to/Parallel-SealPIR
      $ ./pirmessage_client
      
- ##### On AWS
  Create EC2 instances on AWS. Ensure all the instances have TCP allow ports in the 0 to 65535 range. Connect all instances via SSH.
  ###### On the Servers side
      $ Copy pirmessage_server and data.json from your local machine to the Server
      $ Edit inbound rules on Security groups with type ALL TCP and add your client ip address
      $ ./pirmessage_server -port 3000
  ###### Open the Client side
      $ Copy pirmessage_client, encryption_parameters.bin, and servers_list.txt from your local machine to the Client
      $ Change the servers_list.txt with each Server IP address (e.g., 54.253.187.61:3000); database file name; and index i in the database for each line in the file
      $ ./pirmessage_client

---
## [Multiple Clients parallel privately retrieve multiple Merkle proofs](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/Parallel-PIR/DPPIR-Coloring)
### Experimental setup
For simplicity, we ran our experiments on a local Ubuntu 22.04.1 environment (Intel Core i5-1035G1 CPU @1.00GHz×8, 15GiB System memory). We employed two servers and one client, which acted as multiple clients, following the same settings described in [DP-PIR](https://github.com/multiparty/DP-PIR/tree/usenix2022).

<p align="center">
  <img width="600" height="300" src="https://github.com/cnquang/CPIR/assets/87842051/c3729bb6-133c-49f5-9b29-00793ce776bc"> 
</p>
<strong> Fig. 6.</strong> The computation time for DP-PIR and DP-PIR+Coloring, both online and offline, was evaluated from $n = 2^{10}$ to $n = 2^{16}$ while retrieving 6000 Merkle proofs privately.

---
### Compiling DP-PIR + Coloring
#### Installing Libraries

- ##### g++-11
      $ sudo apt install g++-11
      $ sudo apt update
      $ sudo apt upgrade
- ##### Bazel 4.2.1
      $ curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
      $ sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
      $ echo "deb [arch=amd64 signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
      $ sudo apt update
      $ sudo apt install bazel-4.2.1
      $ sudo apt install bazel-bootstrap
- ##### Golang
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install golang-go  
- ##### npm
      $ sudo apt install npm
      $ npm install express

#### Executing DP-PIR and DP-PIR+Coloring
      $ sudo sysctl -w net.core.rmem_max=123289600
      $ sudo sysctl -w net.core.wmem_max=123289600
      $ cd /path/to/experiments/orchestrator
- ##### On your local machine
  ###### Open the first terminal
      $ cd /path/to/experiments/orchestrator
      $ node main.js
  ###### Open the second terminal
      $ ./experiments/local.sh 2 1
  ###### Return to the first terminal
      $ load dpPIR
  You can find a description for these experiments under experiments/orchestrator/stored/dpPIR.json.

---
## [Plotting](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/graphs)
    $ cd /path/to/graphs
    $ python3 figureCSA.py
    $ python3 figurePIR.py

---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.

