#include "pir.hpp"
#include "pir_client.hpp"
#include "pir_server.hpp"
#include <ctime>
#include <mutex>
#include <chrono>
#include <memory>
#include <random>
#include <string>
#include <thread>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <iostream>
#include <unistd.h>
#include <pthread.h>
#include <filesystem>
#include <seal/seal.h>
#include <condition_variable>

using namespace std::chrono;
using namespace std;
using namespace seal;
std::mutex m;
std::string filename;
std::ofstream outputFile;
std::condition_variable cv;

int countThread1 = 0;
int countThread2 = 0;
bool onetime1 = false;
bool onetime2 = false;
bool onetime3 = false;
int totalquerysize, totalanswersize;

auto start = chrono::high_resolution_clock::now();

//---------------------------------------------------SealPIR function----------------------------------------------------
void SealPIR(uint64_t number_of_items, uint64_t size_per_item, uint32_t N, uint32_t logt, uint32_t d, int h, int sol) {
  EncryptionParameters enc_params(scheme_type::bfv);
  PirParams pir_params;
  // Generates all parameters
  gen_encryption_params(N, logt, enc_params); // Main: Generating SEAL parameters

  verify_encryption_params(enc_params); // Main: Verifying SEAL parameters

  // Main: Generating PIR parameters
  gen_pir_params(number_of_items, size_per_item, d, enc_params, pir_params, true, true, true);

  // Initialize PIR client....
  // Main: Generating galois keys for client
  PIRClient client(enc_params, pir_params);
  GaloisKeys galois_keys = client.generate_galois_keys();

  // Initialize PIR Server
  PIRServer server(enc_params, pir_params); // Main: Initializing server

  // Server maps the galois key to client 0. We only have 1 client,
  // which is why we associate it with 0. If there are multiple PIR
  // clients, you should have each client generate a galois key,
  // and assign each client an index or id, then call the procedure below.
  server.set_galois_key(0, galois_keys);

  // Creating the database with random data (this may take some time) ...
  auto db(make_unique<uint8_t[]>(number_of_items * size_per_item)); // Create test database
  random_device rd;
  for (uint64_t i = 0; i < number_of_items; i++) {
    for (uint64_t j = 0; j < size_per_item; j++) {
      uint8_t val = rd() % 256;
      db.get()[(i * size_per_item) + j] = val;
    }
  }

  // Measure database setup
  server.set_database(move(db), number_of_items, size_per_item);
  server.preprocess_database();

  // Main: database pre processed
  // Choose an index of an element in the DB
  uint64_t ele_index = rd() % number_of_items; // element in DB at random position
  uint64_t index = client.get_fv_index(ele_index);   // index of FV plaintext
  uint64_t offset = client.get_fv_offset(ele_index); // offset in FV plaintext
  stringstream client_stream;
  stringstream server_stream;

  //Lock to wait other threads finish
  m.lock();
  if (!onetime1){
    onetime1 = true;
    if (sol == 4){
      sleep(5*h);
    }
    else {
      sleep(2*h);
    }
    start = chrono::high_resolution_clock::now();
  }
  m.unlock();

  // Measure query generation
  PirQuery query = client.generate_query(index); //Query generated
  int query_size = client.generate_serialized_query(index, client_stream); //Serialized query generation

  totalquerysize += query_size;
  countThread1++;
  if (countThread1 == h){
    auto end = chrono::high_resolution_clock::now();
    countThread1 = 0;
    onetime1 = false;
    auto total = duration_cast<microseconds>(end - start).count();
    cout << "SEALPIR query time: " << total / 1000 << " ms" << endl;
    cout << "Query size: " << totalquerysize << " bytes" << endl;
    outputFile << total / 1000 << std::endl;
    outputFile << totalquerysize << std::endl;
    totalquerysize = 0;
  }

  //Lock to wait other threads finish
  m.lock();
  if (!onetime2){
    onetime2 = true;
    sleep(6);
    start = chrono::high_resolution_clock::now();
  }
  m.unlock();

  // Measure answer processing
  PirQuery query2 = server.deserialize_query(client_stream); //Query deserialized
  // Answer PIR query from client 0. If there are multiple clients,
  // enter the id of the client (to use the associated galois key).
  PirReply reply = server.generate_reply(query2, 0); // Answer generated
  int reply_size = server.serialize_reply(reply, server_stream); //Serialized anwser generation

  totalanswersize += reply_size;
  countThread2++;
  if (countThread2 == h){
    auto end = chrono::high_resolution_clock::now();
    countThread2 = 0;
    onetime2 = false;
    auto total = duration_cast<microseconds>(end - start).count();
    cout << "SEALPIR answer time: " << total / 1000 << " ms" << endl;
    cout << "Answer size: " << totalanswersize << " bytes" << endl;
    outputFile << total / 1000 << std::endl;
    outputFile << totalanswersize << std::endl;
    totalanswersize = 0;
  }

  //Lock to wait other threads finish
  m.lock();
  if (!onetime3){
    onetime3 = true;
    sleep(6);
    start = chrono::high_resolution_clock::now();
  }
  m.unlock();

  // Measure response extraction
  vector<uint8_t> elems = client.decode_reply(reply, offset); //Anwser decoded
}

//---------------------------------------------------MAIN----------------------------------------------------
int main(int argc, char *argv[]) {
  int h; //height of the tree
  int solution;
  int option;
  uint64_t n; //number of leave nodes
  uint32_t N = 4096; //degree of polynomial
  uint64_t size_per_item = 32; //size of hash value in bytes
  uint64_t number_of_items; //total number of items in a database
  // Recommended values: (logt, d) = (20, 2)
  uint32_t logt = 20;
  uint32_t d = 2;

  while(1) {
    cout << "***** Menu - Parallel or One core *****"<< endl;
    cout << "1. One core"<< endl;
    cout << "2. Call SealPIR on the whole tree h times parallel (h cores)"<< endl;
    cout << "3. Each Merkle proof as one element (1 core)"<< endl;
    cout << "4. Call SealPIR on each layer and wait for the slowest (h cores)"<< endl;
    cout << "5. Probabilistic Batch Code SealPIR (1.5h cores)"<< endl;
    cout << "6. Balanced ancestral coloring (h cores)"<< endl;
    cout << "7. End"<< endl;
    cout << "Choose your option from 1 to 7:  ";
    cin >> option; // Get user input from the keyboard

    if(option == 7) {
      break;
    }

    std::string folderPath = "FULL-PATH/CSA-parallel-PIR/parallelPIR/graphs";
    std::filesystem::create_directory(folderPath);
    filename = folderPath + "/output" + std::to_string(option) + ".txt";
    outputFile.open(filename, std::ios::app); // Open the file in append mode

    cout << "Type a number of leaves: 2^"; // Type a number and press enter
    cin >> h; // Get user input from the keyboard
    n = 1 << h; //number of leave nodes
    outputFile << h << std::endl;

    //1. One core
    if(option == 1) {
      cout << "***** Menu - One core *****"<< endl;
      cout << "1.1 Call SealPIR on the whole tree"<< endl;
      cout << "1.2. Call SealPIR on the bottom layer"<< endl;
      cout << "1.3. Call SealPIR on the balanced partition"<< endl;
      cout << "1.4. Call SealPIR on the Probabilistic Batch Code"<< endl;
      cout << "1.5. End"<< endl;
      cout << "Choose your solutions from 1 to 5:  ";
      cin >> solution; // Get user input from the keyboard

      if(solution == 5) {
        break;
      }

      onetime1 = true;
      onetime2 = true;
      onetime3 = true;

      //1.1. Call SealPIR on the whole tree
      if(solution == 1){
        number_of_items = (2*n - 2);
        SealPIR(number_of_items, size_per_item, N, logt, d, 1, 0);
      }
      //1.2. Call SealPIR on the bottom layer
      else if(solution == 2){
        number_of_items = n;
        SealPIR(number_of_items, size_per_item, N, logt, d, 1, 0);
      }
      //1.3. Call SealPIR on a balanced partition
      else if(solution == 3){
        //partition size ((2*n-2)/log(n))
        number_of_items = ceil((2*n - 2)/h);
        SealPIR(number_of_items, size_per_item, N, logt, d, 1, 0);
      }
      //1.4. Call SealPIR on a Probabilistic Batch Code - O(3n/1.5logn)
      else {
        number_of_items = ceil(2*(2*n - 2)/h);
        SealPIR(number_of_items, size_per_item, N, logt, d, 1, 0);
      }

      onetime1 = false;
      onetime2 = false;
      onetime3 = false;
      countThread1 = 0;
      countThread2 = 0;
    }
    //2. Call SealPIR on the whole tree h times parallel
    else if(option == 2) {
      number_of_items = (2*n - 2);
      size_per_item = 32;
      std::thread threads[h];
      for (int i = 0; i < h; i++) {
        threads[i] = std::thread(SealPIR, number_of_items, size_per_item, N, logt, d, h, option);
      }
      // Wait for all threads to finish
      for (int j = 0; j < h; j++) {
        threads[j].join();
      }

    }
    //3. Each Merkle proof as one element
    else if(option == 3) {
      number_of_items = n;
      size_per_item = 32*h;
      SealPIR(number_of_items, size_per_item, N, logt, d, 1, option);
    }
    //4. Call SealPIR on each layer and wait for the slowest
    else if(option == 4) {
      size_per_item = 32;
      std::thread threads[h];
      for (int i = 1; i < h + 1; i++) {
        number_of_items = 1 << i;
        threads[i - 1] = std::thread(SealPIR, number_of_items, size_per_item, N, logt, d, h, option);
      }
      // Wait for all threads to finish
      for (int j = 0; j < h; j++) {
        threads[j].join();
      }
    }
    //5. Probabilistic Batch Code SealPIR
    else if(option == 5) {
      number_of_items = static_cast<int>(ceil(2*(2*n - 2)/h));
      size_per_item = 32;
      int q = static_cast<int>(ceil(1.5 * h));
      std::thread threads[q];
      for (int i = 0; i < q; i++) {
        threads[i] = std::thread(SealPIR, number_of_items, size_per_item, N, logt, d, q, option);
      }
      // Wait for all threads to finish
      for (int j = 0; j < q; j++) {
        threads[j].join();
      }
    }
    //6. Balanced ancestral coloring
    else if (option == 6){
      number_of_items = ceil((2*n - 2)/h);
      size_per_item = 32;
      std::thread threads[h];
      for (int i = 0; i < h; i++) {
        threads[i] = std::thread(SealPIR, number_of_items, size_per_item, N, logt, d, h, option);
      }
      // Wait for all threads to finish
      for (int j = 0; j < h; j++) {
        threads[j].join();
      }
    }
    
    auto end = chrono::high_resolution_clock::now();
    auto total = duration_cast<microseconds>(end - start).count();
    cout << "SEALPIR Decoded time: " << total / 1000 << " ms" << endl;
    outputFile << total / 1000 << std::endl;
    onetime1 = false;
    onetime2 = false;
    onetime3 = false;
    countThread1 = 0;
    countThread2 = 0;
    totalquerysize = 0;
    totalanswersize = 0;

    outputFile.close();
  }
  return 0;
}
