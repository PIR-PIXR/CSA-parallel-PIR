<p align="center">
  <img width="250" height="250" src="https://github.com/cnquang/cnquang/assets/87842051/8c730560-bbc7-44d3-9a56-491a1034fefd">
</p>

# Parallel SealPIR

---
## Experimental setup
We ran our experiments on Ubuntu 22.04.1 environment (Intel Core i5-1035G1 CPU @1.00GHz×8, 15GiB System memory) for the client side and until 30 PIR servers on Amazon t2.large instances (Intel(R) Xeon(R) CPU E5-2686 v4 @ 2.30GHz, 2 vCPUs, 8GiB System Memory). We utilize the HTTP/2 protocol in conjunction with [gRPC](https://github.com/grpc/grpc) version 35.0.0, which is developed by Google, for connecting numerous clients and servers over the network.

The main underlying PIR scheme is [SealPIR library](https://github.com/microsoft/SealPIR). We compiled our C++ code (main.cpp) with Cmake version 3.22.1 and [Microsoft SEAL version 4.0.0](https://github.com/cnquang/SEAL-4.0.0). The trees in our experiments have $n=2^{10},2^{12},\ldots,2^{20}$ leaves. The tree nodes contained the latest Bitcoin transactions datasets, and each node in the tree had a size of 256 bits, following the standard hash size (as in SHA-256). 

We compared the performance of our scheme (SealPIR+Coloring) with SealPIR as the underlying PIR and several related solutions including [SealPIR+PBC](https://eprint.iacr.org/2017/1142.pdf) and combinations of SealPIR with $h$-repetition, Proof-as-Elements, and layer-based. Note that [SealPIR+PBC](https://eprint.iacr.org/2017/1142.pdf) uses $m=1.5h$ databases of size $2N/h$ each, Proof-as-Elements uses a single proof-database containing all $n$ proofs ($h$ hashes), $h$-Repetition uses $h$ databases of size $N$ each, and layer-based uses $h$ databases of sizes $2,4,\ldots,2^h=n$. Our solution (SealPIR+Coloring) uses $h$ databases of size approximately $N/h$ each. Here, $N=2^{h+1}-2$ is the number of tree nodes (except the root) and $h$ is the height of the perfect binary trees.

<p align="center">
  <img width="1000" height="400" src="https://github.com/cnquang/CPIR/assets/87842051/1b47d79a-8977-4092-a188-2c26d2579da8"> 
</p>
<strong> Figure 1.</strong> A comparison of the server computation costs in parallel of five schemes from $n = 2^{10}$ to $n = 2^{20}$. Our coloring-based scheme outperforms others. Size of each node is 32 bytes (hash digest size).

---
## Compiling SealPIR
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
- #### JSON
      $ git clone https://github.com/microsoft/vcpkg
      $ ./vcpkg/bootstrap-vcpkg.sh
      $ ./vcpkg install rapidjson
- #### Google gRPC
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

### Executing Parallel SealPIR
      $ cd /path/to/Parallel-SealPIR
      $ cmake .
      $ make
      $ -> Generated: CXX executable pirmessage_server and CXX executable pirmessage_client
      
- #### On your local machine
  ##### Open the first terminal as Server side (You can create as many servers as you want in the separate terminals. Make sure each server opens different port numbers)
      $ cd /path/to/Parallel-SealPIR
      $ ./pirmessage_server -port 3000
  ##### Open the second terminal as Client side
      $ Change the servers_list.txt with local IP address 127.0.0.1:3000; database file name (change the database name in the Server side to data.json); and index i in the database
      $ cd /path/to/Parallel-SealPIR
      $ ./pirmessage_client
      
- #### On AWS
Create EC2 instances on AWS. Ensure all the instances have TCP allow ports in the 0 to 65535 range. Connect all instances via SSH.
  ##### On the Servers side
      $ Copy pirmessage_server and data.json from your local machine to the Server
      $ Edit inbound rules on Security groups with type ALL TCP and add your client ip address
      $ ./pirmessage_server -port 3000
  ##### Open the Client side
      $ Copy pirmessage_client, encryption_parameters.bin, and servers_list.txt from your local machine to the Client
      $ Change the servers_list.txt with each Server IP address (e.g., 54.253.187.61:3000); database file name; and index i in the database for each line in the file
      $ cd /path/to/Parallel-SealPIR
      $ ./pirmessage_client

---
## ACKNOWLEDGMENTS
This work was supported by the Australian Research Council through the Discovery Project under Grant DP200100731.
