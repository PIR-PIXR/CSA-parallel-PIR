<p align="center">
  <img width="400" height="250" src="https://github.com/cnquang/cnquang/assets/87842051/1f4af073-6965-4e6e-876f-d835e42f7cf2">
</p>

# Parallelizing Private Information Retrieval of Merkle Proofs via Tree Colorings

### Abstract
Motivated by a practical scenario in blockchains in which a client, who possesses a transaction, wishes to privately verify that the transaction actually belongs to a block, we investigate the problem of private retrieval of Merkle proofs (i.e. proofs of inclusion/membership) in a Merkle tree.
In this setting, one or more servers store the nodes of a binary tree (a Merkle tree), while a client wants to retrieve the set of nodes along a root-to-leaf path (i.e. a Merkle proof, after appropriate node swapping operations), without letting the servers know which path is being retrieved. 
We propose a method that partitions the Merkle tree to enable parallel private retrieval of the Merkle proofs. The partitioning step is based on a novel tree coloring called \textit{ancestral coloring} in which nodes that have ancestor-descendant relationship must have distinct colors. To minimize the retrieval time, the coloring is required to be balanced, i.e. the sizes of the color classes differ by at most one. We develop a fast algorithm to find a balanced (in fact, any) ancestral coloring in almost linear time in the number of tree nodes, which can handle trees with billions of nodes in a few minutes. Our partitioning method can be applied on top of any private information retrieval scheme, leading to the minimum storage overhead and fastest running times compared to existing approaches. You can find a copy of the paper [here](https://arxiv.org/abs/2205.05211)

---
## Main Contributions

- We propose an efficient approach to parallelize the private retrieval of the Merkle proofs based on the novel concept of balanced ancestral coloring of rooted trees. Our approach achieves the lowest possible storage overhead (no redundancy) and lowest computation complexity compared to existing approaches.

- We establish a necessary and sufficient condition for the existence of an ancestral coloring with arbitrary color sequences.

- We develop a \textit{divide-and-conquer} algorithm to generate an ancestral coloring for \textit{every} feasible color sequence with time complexity $\Theta(n\log\log(n))$ on the perfect binary tree of $n$ leaves. The algorithm can color a tree of two billion nodes in under five minutes.

- Finally, we implement and evaluate the empirical performance of our approach using SealPIR and DP-PIR as the underlying PIR schemes.

---
## Problem Description

Given a (perfect) Merkle tree stored at one or more servers, we are interested in designing an _efficient_ private retrieval scheme in which a client can send queries to the server(s) and retrieve an arbitrary Merkle proof without letting the server(s) know which proof is being retrieved. This problem is equivalent to the problem of designing an efficient private retrieval scheme for every root-to-leaf path in a perfect binary tree (with depth $h$ and $n=2^h$ leaves).
An efficient retrieval scheme should have _low storage, computation, and communication overheads_.
The server(s) should not be able to learn which path is being retrieved based on the queries received from the client. We do not need to formally define privacy because it is nonessential to our contribution and also because the privacy of our solution is guaranteed by the privacy of the underlying PIR scheme straightforwardly.

We assume a setting in which the nodes of a Merkle/perfect binary tree are stored at one multi-core server or multiple (single-core) servers. Hence, the system is capable of parallel processing. This is a key assumption of our approach to work. For brevity, we will use the multi-server setting henceforth. To simplify the discussion, we assume that the servers have the same storage/computational capacities and will complete the same workload simultaneously.

---
## [Bitcoin Datasets in Real-time](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/BitcoinDataset)
We utilized our Java code to gather 200 Bitcoin Blocks in \textit{real-time} from the \textit{latest} Block 813562, containing 2390 transactions, mined on 2023-10-24 at 09:52:26 GMT +11, to Block 813363, which included 2769 transactions and was mined on 2023-10-23 at 04:13:24 GMT +11. On average, within the dataset we collected, there were 1839 transactions in each Block. The number of transactions in each Bitcoin Block typically ranges from 1000 to 4500, and the number of active addresses per day is more than 900K. To interface with the [Blockchain Data API](https://www.blockchain.com/explorer/api/blockchain_api) for collecting real-time Bitcoin Blocks in JSON format, we used HttpURLConnection and [Google GSON](https://github.com/google/gson) 2.10.1.

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

We ran our experiments using the Amazone c6i.8xlarge instance (Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz, 32 vCPUs, 64GiB System Memory, 12.5 Gbps network bandwidth, all running Ubuntu 22-04 LTS). Our Java code (CSA.java) was compiled using Java OpenJDK version 11.0.19. The running times are presented in Figure 1, confirming our algorithm's theoretical complexity (almost linear). Note that the algorithm only ran on a single vCPU of the virtual machine. Our current code can handle trees of heights up to $35$, for which the algorithm took 2.5 hours to complete. For a perfect binary tree of height $h=30$, it took less than 5 minutes to produce a balanced ancestral coloring.

<p align="center">
  <img width="500" height="300" src="https://github.com/cnquang/CPIR/assets/87842051/185c01a5-a643-437e-a637-f8b02f6cbdc4">
</p>
<strong> Fig. 1.</strong> The average running times of the Color-Splitting Algorithm (CSA) when generating balanced ancestral colorings for the perfect binary trees with $n = 2^{10},2^{11},...,2^{20}$ leaves. For each $n$, the algorithm was run a hundred times, and the average running time was recorded.

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

*Fig 2: An example of the CSA algorithm running option A (Automatic Balanced Ancestral Coloring) when h = 5.*


<img width="575" alt="h3manual" src="https://user-images.githubusercontent.com/102839948/161372572-773c693e-bd18-4a97-b979-00bbc393fce9.png">

*Fig 3: An example of the CSA algorithm running option B (Manual Feasible Color Sequences) with c = [3 3 8].*

---
## [Parallel PIR retrieving Merkle proof](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/parallel-PIR)

Suppose the client has an item $T_j$ and knows its index $j$ in the Merkle tree. Note that the index retrieval phase does not rule out the case where the item does not belong to the block. Now, the client wants to privately and efficiently download the Merkle proof of that item and verify if the item is really included in the block. Given the index, the client knows precisely which nodes to download from the Merkle tree. Our solution (h-time-WholeTree) is to run $h$ parallel PIR on the $h$ color classes/sub-databases as a result of CSA.

<p align="center">
  <img width="600" height="300" src="https://github.com/cnquang/cnquang/assets/87842051/bd15563b-48f7-4422-be5b-02800e704cd6">
</p>
<strong> Fig. 1.</strong> An illustration of our coloring-based parallel private retrieval of Merkle proofs. First, the nodes of the Merkle tree of height $h$ are partitioned into $h$ parts/color classes/sub-databases, each of which is stored by a server. The client runs $h$ PIR schemes with these $h$ servers in parallel to privately retrieve $h$ nodes of the Merkle proof, one from each server. Here, PIR.Query and PIR. Answer refers to the query and answer generations in the corresponding PIR scheme.

---
## Experimental setup
We ran our experiments using the Amazone c6i.8xlarge instance (Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz, 32 vCPUs, 64GiB System Memory, 12.5 Gbps network bandwidth). We performed these experiments on Ubuntu 22-04 LTS.

---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.

