<p align="center">
  <img width="250" height="250" src="https://github.com/cnquang/testPIR/assets/87842051/9435d9e8-4df5-4a84-9939-3e67768689b8">
</p>

## CSA: Color-Splitting Algorithm
We develop a divide-and-conquer CSA algorithm that generates a **balanced and unbalanced** ancestral coloring. For balanced ancestral coloring, the algorithm is running time almost linear in the number of tree nodes, the running time is in O(2^{h+1}*log h). The flexibility of our algorithm establishes the existence of optimal combinatorial patterned batch codes corresponding to the case of servers with heterogeneous storage capacities. At the high level, the algorithm colors two sibling nodes simultaneously proceeds recursively down to the two subtrees and repeats the process while maintaining the Ancestral Property. Using our algorithm, we can generate a balanced ancestral coloring for the tree $T(30)$ (around two billion nodes) remarkably fast in under five minutes (with 16GB allocated for Java's heap memory).

### Experimental setup (CSA)

We ran our experiments on Linux server (Intel(R) Xeon(R) CPU E5-2690 v2 @ 3.00GHz) based on Red Hat Enterprise Linux Server version 7.9 (Maipo)  all running Linux 3.10.0-1160.59.1.el7.x86_64 x86_64. We compile our Java code with Java OpenJDK version 1.8.0_322. Time generates a balanced ancestral coloring for the tree T (h) as below:

    T(20) = 224 milliseconds
    T(25) = 7523 milliseconds   = 7.52 seconds
    T(30) = 241847 milliseconds = 4.03 minutes      (Recommended the maximum Java heap size: 16GB)
    T(31) = 490781 milliseconds = 8.18 minutes      (Recommended the maximum Java heap size: 32GB)
    T(32) = 978274 milliseconds = 16.30 minutes     (Recommended the maximum Java heap size: 64GB)
    T(33) = 1994432 milliseconds = 33.24 minutes    (Recommended the maximum Java heap size: 120GB)
    T(34) = 4378425 milliseconds = 1.22 hours       (Recommended the maximum Java heap size: 240GB)
    T(35) = 8691602 milliseconds = 2.41 hours       (Recommended the maximum Java heap size: 500GB)

Moreover, we ran our experiments using the Amazone c6i.8xlarge instance (Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz, 32 CPUs, 64GiB System Memory, 12.5 Gbps network bandwidth, all running Ubuntu 22-04 LTS). Our Java code (CSA.java) was compiled using Java OpenJDK version 11.0.19. We ran 100 times of CSA for each tree leaves size ranging from $2^{10}$ to $2^{20}$ and calculated the average. The results are presented in Figure 1.

<p align="center">
  <img width="400" height="350" src="https://github.com/cnquang/testPIR/assets/87842051/4017a802-45a4-4eb4-bf16-fbe754bed0fe">
</p>
<strong> Fig. 1.</strong> Color-Splitting Algorithm (CSA) generates balanced ancestral coloring for the perfect binary tree, which the number of leaves from $2^{10}$ to $2^{20}$. Every point is the average 100 times running CSA, corresponding with the number of leaves.

---
## Compiling CSA
### Installing Libraries

- #### Javac
      $ sudo apt update
      $ sudo apt upgrade
      $ sudo apt install default-jdk

### Executing CSA
- #### Once Java and Javac are installed, to build CSA simply run:

      $ javac CSA.java
      $ java CSA

- #### To build CSA with recommended max heap size simply run:

      $ javac CSA.java
      $ java -Xmx32g CSA

### Plotting
      $ python3 figureCSA.py
    
### User Interface Guideline (CSA)

Take a look at the pictures below, guidelines and in CSA.java comments for how to use CSA.  

<img width="415" alt="h5auto" src="https://user-images.githubusercontent.com/102839948/161372568-85df8aed-6424-4977-9853-722879624efe.png">

*Fig 1: An example of the CSA algorithm running option A (Automatic Balanced Ancestral Coloring) when h = 5.*


<img width="575" alt="h3manual" src="https://user-images.githubusercontent.com/102839948/161372572-773c693e-bd18-4a97-b979-00bbc393fce9.png">

*Fig 2: An example of the CSA algorithm running option B (Manual Feasible Color Sequences) with c = [3 3 8].*
