<p align="center">
  <img width="400" height="250" src="https://github.com/cnquang/cnquang/assets/87842051/1f4af073-6965-4e6e-876f-d835e42f7cf2">
</p>

# Parallelizing Private Information Retrieval of Merkle Proofs via Tree Colorings

### Abstract
Motivated by a practical scenario in blockchains in which a client, who possesses a transaction, wishes to privately verify that the transaction actually belongs to a block, we investigate the problem of private retrieval of Merkle proofs (i.e. proofs of inclusion/membership) in a Merkle tree.
In this setting, one or more servers store the nodes of a binary tree (a Merkle tree), while a client wants to retrieve the set of nodes along a root-to-leaf path (i.e. a Merkle proof, after appropriate node swapping operations), without letting the servers know which path is being retrieved. 
We propose a method that partitions the Merkle tree to enable parallel private retrieval of the Merkle proofs. The partitioning step is based on a novel tree coloring called \textit{ancestral coloring} in which nodes that have ancestor-descendant relationships must have distinct colors. To minimize the retrieval time, the coloring is required to be balanced, i.e. the sizes of the color classes differ by at most one. We develop a fast algorithm to find a balanced (in fact, any) ancestral coloring in almost linear time in the number of tree nodes, which can handle trees with billions of nodes in a few minutes. Our partitioning method can be applied on top of any private information retrieval scheme, leading to the minimum storage overhead and fastest running times compared to existing approaches. You can find a copy of the paper [here](https://arxiv.org/abs/2205.05211)

---
## Main Contributions

- We propose an efficient approach to parallelize the private retrieval of the Merkle proofs based on the novel concept of balanced ancestral coloring of rooted trees. Our approach achieves the lowest possible storage overhead (no redundancy) and lowest computation complexity compared to existing approaches.

- We establish a necessary and sufficient condition for the existence of an ancestral coloring with arbitrary color sequences, i.e. color class sizes. Our condition allows us to check if an ancestral coloring for the perfect binary tree $T(4)$ using three red, six green, eight blue, and thirteen purple nodes exists.

- We develop a \textit{divide-and-conquer} algorithm to generate an ancestral coloring for \textit{every} feasible color sequence with time complexity $\Theta(n\log\log(n))$ on the perfect binary tree of $n$ leaves. The algorithm can color a tree of two billion nodes in under five minutes.

- Finally, we implement and evaluate the empirical performance of our approach using SealPIR as the underlying PIR scheme.

---
## Problem Description

Given a (perfect) Merkle tree stored at one or more servers, we are interested in designing an \textit{efficient} private retrieval scheme in which a client can send queries to the server(s) and retrieve an arbitrary Merkle proof without letting the server(s) know which proof is being retrieved. This problem is equivalent to the problem of designing an efficient private retrieval scheme for every root-to-leaf path in a perfect binary tree (with depth $h$ and $n=2^h$ leaves).
An efficient retrieval scheme should have \textit{low} \textit{storage}, \textit{computation}, and \textit{communication overheads}.
The server(s) should not be able to learn which path is being retrieved based on the queries received from the client. We do not need to formally define privacy because it is nonessential to our contribution and also because the privacy of our solution is guaranteed by the privacy of the underlying PIR scheme straightforwardly.

We assume a setting in which the nodes of a Merkle/perfect binary tree are stored at one multi-core server or multiple (single-core) servers. Hence, the system is capable of parallel processing. This is a key assumption of our approach to work. For brevity, we will use the multi-server setting henceforth. To simplify the discussion, we assume that the servers have the same storage/computational capacities and will complete the same workload simultaneously.

---
## [CSA: Color-Splitting Algorithm](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/CSA)

We develop a divide-and-conquer CSA algorithm that generates a balanced and unbalanced ancestral coloring. For balanced ancestral coloring, the algorithm's running time is almost linear in the number of tree nodes, the running time is in O(N*loglog(N)). The flexibility of our algorithm establishes the existence of optimal combinatorial patterned batch codes corresponding to the case of servers with heterogeneous storage capacities. At the high level, the algorithm colors two sibling nodes simultaneously, proceeds recursively down to the two subtrees and repeats the process while maintaining the Ancestral Property. Using our algorithm, we can generate a balanced ancestral coloring for the tree $T(30)$ (around two billion nodes) remarkably fast in under five minutes (with 16GB allocated for Java's heap memory).

---
## [Parallel PIR retrieving Merkle proof](https://github.com/PIR-PIXR/CSA-parallel-PIR/tree/main/parallel-PIR)

Suppose the client has an item $T_j$ and knows its index $j$ in the Merkle tree. Note that the index retrieval phase does not rule out the case where the item does not belong to the block. Now, the client wants to privately and efficiently download the Merkle proof of that item and verify if the item is really included in the block. Given the index, the client knows precisely which nodes to download from the Merkle tree. Our solution (h-time-WholeTree) is to run $h$ parallel PIR on the $h$ color classes/sub-databases as a result of CSA.

<p align="center">
  <img width="600" height="300" src="https://github.com/cnquang/cnquang/assets/87842051/bd15563b-48f7-4422-be5b-02800e704cd6">
</p>
<strong> Fig. 1.</strong> An illustration of our coloring-based parallel private retrieval of Merkle proofs. First, the nodes of the Merkle tree of height $h$ are partitioned into $h$ parts/color classes/sub-databases, each of which is stored by a server. The client runs $h$ PIR schemes with these $h$ servers in parallel to privately retrieve $h$ nodes of the Merkle proof, one from each server. Here, PIR.Query and PIR. Answer refers to the query and answer generations in the corresponding PIR scheme.

---
## Experimental setup
We ran our experiments using the Amazone c6i.8xlarge instance (Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz, 32 CPUs, 64GiB System Memory, 12.5 Gbps network bandwidth). We performed these experiments on Ubuntu 22-04 LTS.

---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.

