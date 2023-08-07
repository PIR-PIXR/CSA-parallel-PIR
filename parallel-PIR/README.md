<p align="center">
  <img width="250" height="250" src="https://github.com/cnquang/cnquang/assets/87842051/8c730560-bbc7-44d3-9a56-491a1034fefd">
</p>

# Parallel-PIR: Parallel SealPIR

---
## Experimental setup
We ran our experiments using the Amazone c6i.8xlarge instance (Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz, 32 CPUs, 64GiB System Memory, 12.5 Gbps network bandwidth, all running Ubuntu 22-04 LTS). The C++ code of the [SealPIR library](https://github.com/microsoft/SealPIR) was designed to execute only on one core. We created multiple threads to run on multiple cores to serve our purpose. We compiled our C++ code (main.cpp) with Cmake version 3.22.1 and [Microsoft SEAL version 4.0.0](https://github.com/cnquang/SEAL-4.0.0). In the *parallel* mode, each thread ran the SealPIR scheme server and client on a database on a separate core in our Amazone EC2 instance. The size of each database varied, depending on the solutions. For example, if $h = 10$, then we will need ten threads, each of which will run on a different database with a size ranging from $2^{1}$ to $2^{10}$ for the layer-based scheme. For the coloring-based scheme, all databases have roughly the same size $({2^{11} - 2})/10$. We ran 10 times of parallel SealPIR for each tree leaves size ranging from $2^{10}$ to $2^{20}$ and calculated the average.

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
To summarize, our coloring-based solution provides a novel partitioning of the Merkle tree such that the client can retrieve Meklre proof in parallel while guaranteeing privacy, minimizing the storage requirement, and reducing computational complexity. In CPIR, such as SealPIR, the significant computation costs are often on the server side. Figure \ref{fig:serverSealPIR} showed that our solution is always better than others and just under 0.2 seconds when $n = 2^{20}$. Hence, our solution is also far more efficient than others with larger tree sizes. The results shown in Figure 1 demonstrated that the Proof-as-Element approach is efficient for small trees (where $n < 2^{15}$). However, as the tree size increases, the database size also significantly increases, resulting in a considerably worse total running time.
In contrast, the probabilistic solution presented in \cite{angel2018}, known as PBC-SealPIR, consistently requires an additional $\lceil 1.5h \rceil$ cores compared to other methods. As a result, the communication costs associated with PBC-SealPIR are consistently the highest. At the same time, the Proof-as-Element approach only requires a single core, making it the most efficient communication cost. The total communication and computation costs in our solution are better than others and beat the trivial solution downloading the whole database from $n = 2^{17}$ and $n = 2^{19}$ when the bandwidths are 100Mbps and 1 Gbps, respectively. Note that for bandwidths larger than 100Mbps, the computation time will contribute to a higher percentage of the total running time. Also, a larger bandwidth will make the trivial algorithm faster, and as a consequence, the threshold of the leaves size $(n)$ where a Coloring-based scheme like ours can beat the trivial solution will be increased. 

<p align="center">
  <img width="400" height="300" src="https://github.com/cnquang/cnquang/assets/87842051/92dcbf05-1fbf-458d-b759-adfd68ebba36">
</p>
<strong> Fig. 1.</strong> A comparison of the server computation costs of five solutions from $n = 2^{10}$ to $n = 2^{20}$. Our coloring-based solution is always better than other solutions.

<p align="center">
  <img width="800" height="350" src="https://github.com/cnquang/cnquang/assets/87842051/1405b979-329f-4a79-b506-ddc7bf7d7bd8"> 
</p>
<strong> Fig. 2.</strong> A comparison of the total running times (communication and computation) of six solutions in the network bandwidth 100 Mbps and 1 Gbps. Our coloring-based solution beats the trivial solution from $n = 2^{17}$ and $n = 2^{19}$ respectively.

---
## ACKNOWLEDGMENTS
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.
