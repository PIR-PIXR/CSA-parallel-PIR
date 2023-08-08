<p align="center">
  <img width="250" height="250" src="https://github.com/cnquang/cnquang/assets/87842051/8c730560-bbc7-44d3-9a56-491a1034fefd">
</p>

# Parallel-PIR: Parallel SealPIR

---
## Experimental setup
We ran our experiments using the Amazone c6i.8xlarge instance (Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz, 32 CPUs, 64GiB System Memory, 12.5 Gbps network bandwidth, all running Ubuntu 22-04 LTS). The main underlying PIR scheme is [SealPIR library](https://github.com/microsoft/SealPIR). Its C++ implementation, however, was designed to execute only on one core. We created multiple threads to run on multiple vCPUs to parallelize the retrieval. Each thread ran the SealPIR scheme server and client on a random database on a separate vCPU in our Amazon EC2 instance. We compiled our C++ code (main.cpp) with Cmake version 3.22.1 and [Microsoft SEAL version 4.0.0](https://github.com/cnquang/SEAL-4.0.0). The trees in our experiments have $n=2^{15},2^{16},\ldots,2^{20}$ leaves. The tree nodes contained randomly generated data and had size 256 bits, following the standard hash size (as in SHA3-256). 

We compared the performance of our scheme  (SealPIR + Coloring) with SealPIR as the underlying PIR and several related solutions including [SealPIR + PBC](https://eprint.iacr.org/2017/1142.pdf) and combinations of SealPIR with $h$-repetition, Proof-as-Elements, and layer-based. Note that [SealPIR + PBC](https://eprint.iacr.org/2017/1142.pdf) uses $m=1.5h$ databases of size $2N/h$ each, Proof-as-Elements uses a single proof-database containing all $n$ proofs ($h$ hashes), $h$-Repetition uses $h$ databases of size $N$ each, and layer-based uses $h$ databases of sizes $2,4,\ldots,2^h=n$. Our solution (SealPIR + Coloring) uses $h$ databases of size approximately $N/h$ each. Here, $N=2^{h+1}-2$ is the number of tree nodes (except the root) and $h$ is the height of the perfect binary trees.
For example, with $h = 20$, (SealPIR + PBC) ran 30 threads, each of which processed a PIR database of size approximately 200,000 while our scheme used 20 threads, each of which handled a PIR database of size roughly 100,000. We did not include [Vectorized BPIR](https://eprint.iacr.org/2022/1262) in the comparisons because their code hadn't been released at our time of submission and the parameters provided in their paper do not match our setting, which has batch size $h$ on a database of size $N=2^{h+1}-2$. However, as noted in [Vectorized BPIR](https://eprint.iacr.org/2022/1262), in their experiment, Vectorized BatchPIR had communication cost $20-96\times$ smaller than (SealPIR + PBC), but with a slightly higher computation cost ($1.1\times$ to $1.6\times$ higher).

To ensure that all threads execute concurrently and avoid potential data race issues, we utilized the std::mutex class. When a thread arrives, it attempts to acquire the lock by calling lock() on the mutex. If another thread holds the lock, the current thread goes to sleep, waiting for the lock to be released. Once the final thread completes its task, the first thread releases the lock using unlock(). Consequently, all threads can execute their respective tasks simultaneously, processing data independently within their corresponding databases.

We ran each scheme ten times and calculated the average server and (server+client) computation times. The results are presented in Figure 1 (server times only) and Figure 2 (total running time = server+client computation times plus the communication times). To calculate the communication times, we assume network bandwidths of 100Mbps and 1Gbps, the typical expected range for 5G mobile phones in Australia. 

<p align="center">
  <img width="1000" height="400" src="https://github.com/cnquang/cnquang/assets/87842051/ce2c3047-16cf-44c6-9882-e10f97a29de3"> 
</p>
<strong> Table 1.</strong> A comparison of our  scheme and related batch PIR schemes regarding the total storage overhead, the number $m$ of databases (or cores/servers/buckets), the server/client running times, and the failure probability. Here, $N$ and $h$ denote the number of tree nodes and the tree height, respectively, and $\ell\geq 2$ is the tuning parameter in the subcube code. The client's time is much lower than the server's time in practice as it only processes the indices. The big-O notation cannot capture this fact.

---
## Compiling CPIR
### Installing Libraries

- #### SEAL 4.0.0
      $ sudo apt install build-essential cmake clang git g++ libssl-dev libgmp3-dev
      $ sudo apt update
      $ sudo apt upgrade
      $ git clone https://github.com/cnquang/SEAL-4.0.0.git
      $ cd SEAL-4.0.0
      $ cmake -S . -B build
      $ cmake --build build
      $ sudo cmake --install build
- #### Testing original SealPIR (2022)
      $ git clone https://github.com/microsoft/SealPIR.git
      $ cd SealPIR
      $ cmake .
      $ make
      $ sudo ./bin/main
      $ ...

### Executing Parallel SealPIR
      $ git clone https://github.com/PIR-PIXR/CSA-parallel-PIR
      $ cd CSA-parallel-Pir/Parallel-PIR
      $ cmake .
      $ make
      $ sudo bin/main
### Plotting
      $ cd graphs
      $ python3 figurePIR.py
---
## Performance
To summarize, our coloring-based solution provides a novel partitioning of the Merkle tree such that the client can retrieve Meklre proof in parallel while guaranteeing privacy, minimizing the storage requirement, and reducing computational complexity. 
We present in Figure 1 the (parallel) server time of different retrieval schemes. Our solution always performed better than others and took less than 0.2 seconds when $n = 2^{20}$. The total running times (server+client computation and communication) of all schemes  are shown in Figure 2. As mentioned earlier, [SealPIR + PBC](https://eprint.iacr.org/2017/1142.pdf) requires $\lceil 1.5h \rceil$ cores while most others require $h$ cores. As a result, the communication costs associated with SealPIR were consistently the highest.
On the other hand, the Proof-as-Element approach only requires a single core, making it the method with the lowest communication cost. However, this scheme also required the longest computation time (no parallel computation). The total communication and computation costs of our proposed scheme were, as expected, lower than others most of the time, especially for larger $h$ (larger saving). The computation times of our scheme (SealPIR + Coloring) were roughly half of those of [SealPIR + PBC](https://eprint.iacr.org/2017/1142.pdf), consistent with the theoretical analysis in Table 1. 

<p align="center">
  <img width="500" height="350" src="https://github.com/cnquang/cnquang/assets/87842051/92dcbf05-1fbf-458d-b759-adfd68ebba36">
</p>
<strong> Fig. 1.</strong> A comparison of the server computation costs of five schemes from $n = 2^{10}$ to $n = 2^{20}$. Our coloring-based scheme outperforms others.

<p align="center">
  <img width="900" height="400" src="https://github.com/cnquang/cnquang/assets/87842051/1405b979-329f-4a79-b506-ddc7bf7d7bd8"> 
</p>
<strong> Fig. 2.</strong> A comparison of the total running times (communication and computation) of five PIR schemes in the network bandwidth 100 Mbps and 1 Gbps.

---
## ACKNOWLEDGMENTS
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.
