<p align="center">
  <img width="250" height="250" src="https://github.com/cnquang/testPIR/assets/87842051/fba201f1-3818-4e0b-b0a9-cca7ffd4b74c">
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

---
## ACKNOWLEDGMENTS
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.
