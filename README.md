<p align="center">
  <img width="400" height="250" src="https://github.com/cnquang/testPIR/assets/87842051/a1977288-1e72-4cfb-b233-a8cf89e93fe8">
</p>

# Parallelizing Private Information Retrieval of Merkle Proofs via Tree Colorings
Abstract: We present a new partition binary tree algorithm derived from a novel tree coloring problem. In this problem, every node in a rooted tree with a height of $h$ is assigned one out of $h$ available colors satisfying any two nodes connected as ancestors and descendants must have distinct colors. Our major contribution is the characterization of $all$ possible input color sequences based on majorizations. We then develop an almost linear time divide-and-conquer algorithm to generate such a coloring for $every$ perfect binary tree of height $h\geq 2$. The algorithm presented efficiently produces a balanced ancestral coloring for large trees with around two billion nodes in less than five minutes, ensuring that the numbers of nodes in any two different color classes differ by at most one. The balanced ancestral coloring is crucial in enhancing the efficiency of $parallel$ private information retrieval (PIR) schemes, specifically when retrieving a Merkle proof in a Merkle tree. This research concentrates explicitly on the computational PIR implementation of SealPIR, a state-of-the-art PIR scheme. It demonstrates a remarkable reduction in running time by a factor of $\Theta(h/2)$. Additionally, balanced ancestral coloring provides insights into combinatorial batch codes. When the batch of nodes follows a specific pattern along a root-to-leaf path in a tree, the total storage capacity required can be reduced by a factor of $\Theta(h)$ compared to an $arbitrary$ batch while maintaining a balanced distribution of storage capacity across h servers. Furthermore, our findings reveal an infinite family of graphs where the equitable chromatic number can be explicitly determined. This family of graphs has not been previously discovered in existing literature, making it a novel contribution. You can find a copy of the paper [here](https://arxiv.org/abs/2205.05211)

## CSA: Color-Splitting Algorithm
We develop a divide-and-conquer CSA algorithm that generates a balanced and unbalanced ancestral coloring. For balanced ancestral coloring, the algorithm is running time almost linear in the number of tree nodes, the running time is in O(2^{h+1}*log h). The flexibility of our algorithm establishes the existence of optimal combinatorial patterned batch codes corresponding to the case of servers with heterogeneous storage capacities. At the high level, the algorithm colors two sibling nodes simultaneously proceeds recursively down to the two subtrees and repeats the process while maintaining the Ancestral Property. Using our algorithm, we can generate a balanced ancestral coloring for the tree $T(30)$ (around two billion nodes) remarkably fast in under five minutes (with 16GB allocated for Java's heap memory).

---
## ACKNOWLEDGMENTS 
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.

