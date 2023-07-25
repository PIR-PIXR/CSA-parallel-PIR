<p align="center">
  <img width="400" height="250" src="https://github.com/cnquang/testPIR/assets/87842051/a1977288-1e72-4cfb-b233-a8cf89e93fe8">
</p>

# Parallelizing Private Information Retrieval of Merkle Proofs via Tree Colorings
Abstract: Motivated by a practical scenario in blockchains in which a client, who possesses a transaction, wishes to privately verify that the transaction actually belongs to a block, we investigate the problem of private retrieval of Merkle proofs (i.e. proofs of inclusion/membership) in a Merkle tree.
In this setting, one or more servers store the nodes of a binary tree (a Merkle tree), while a client wants to retrieve the set of nodes along a root-to-leaf path (i.e. a Merkle proof, after appropriate node swapping operations), without letting the servers know which path is being retrieved. 
We propose a method that partitions the Merkle tree to enable parallel private retrieval of the Merkle proofs. The partitioning step is based on a novel tree coloring called \textit{ancestral coloring} in which nodes that have ancestor-descendant relationships must have distinct colors. To minimize the retrieval time, the coloring is required to be balanced, i.e. the sizes of the color classes differ by at most one. We develop a fast algorithm to find a balanced (in fact, any) ancestral coloring in almost linear time in the number of tree nodes, which can handle trees with billions of nodes in a few minutes. Our partitioning method can be applied on top of any private information retrieval scheme, leading to the minimum storage overhead and fastest running times compared to existing approaches. You can find a copy of the paper [here](https://arxiv.org/abs/2205.05211)

## CSA: Color-Splitting Algorithm
We develop a divide-and-conquer CSA algorithm that generates a balanced and unbalanced ancestral coloring. For balanced ancestral coloring, the algorithm's running time is almost linear in the number of tree nodes, the running time is in O(nloglogn). The flexibility of our algorithm establishes the existence of optimal combinatorial patterned batch codes corresponding to the case of servers with heterogeneous storage capacities. At the high level, the algorithm colors two sibling nodes simultaneously proceeds recursively down to the two subtrees and repeats the process while maintaining the Ancestral Property. Using our algorithm, we can generate a balanced ancestral coloring for the tree $T(30)$ (around two billion nodes) remarkably fast in under five minutes (with 16GB allocated for Java's heap memory).

---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.

