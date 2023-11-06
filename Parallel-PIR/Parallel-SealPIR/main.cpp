#include <boost/asio.hpp>
#include "pir.hpp"
#include "pir_client.hpp"
#include "pir_server.hpp"
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <memory>
#include <random>
#include <seal/seal.h>

#include <iostream>
#include <fstream>
#include <iomanip>

#include <string.h>
#include <thread>
#include "/home/nhat/Desktop/vcpkg/installed/x64-linux/include/rapidjson/document.h"
//#include "/home/dowload/vcpkg/installed/x64-linux/include/rapidjson/document.h"
#include "helper.hpp"

using namespace std;
using namespace boost::asio;
using namespace boost::asio::ip;
using std::thread;
using ip::tcp;
using std::string;
using std::cout;
using std::endl;
//g++ -o client client.cpp -lboost_system -lboost_thread -pthread

using namespace std::chrono;
using namespace std;
using namespace seal;
using namespace rapidjson;


#define LISTEN_PORT 12345

int main() {

  // Open the JSON file
  //ifstream file("/home/nhat/Desktop/DataPreprocessing/layer1.json");
  ifstream file("layer1.json");
  // Read the entire file into a string
  string json((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());

  // Close the file
  file.close();

  // Create a Document object to hold the JSON data
  Document doc;

  // Parse the JSON data
  doc.Parse(json.c_str());

  const Value& obj = doc[0];

  uint64_t number_of_items = obj.MemberCount();
  string str = obj.MemberBegin()->value.GetString();
  uint64_t size_per_item = str.length() / 2; // in bytes
  uint32_t N = 4096;

  //////////////////////////////////////////////SERVER////////////////
  cout << "Main: Loading the database (this may take some time) ..." << endl;

  // Create test database
  auto db(make_unique<uint8_t[]>(number_of_items * size_per_item));

  // Copy of the database. We use this at the end to make sure we retrieved
  // the correct element.
  auto db_copy(make_unique<uint8_t[]>(number_of_items * size_per_item));

  // Check if the JSON is an array
  if (doc.IsArray()) {
    uint64_t i = 0;
    string hexString; // Initialize an empty string

    // Loop through the object's members
    for (Value::ConstMemberIterator it = obj.MemberBegin(); it != obj.MemberEnd(); ++it) {
      //cout << "Key: " << it->name.GetString() << ", Value: " << it->value.GetString() << endl;
      hexString = it->value.GetString();
      //number_of_items++;
      for (uint64_t j = 0; j < size_per_item; j++) {
        string byteStr = hexString.substr(j * 2, 2); // Get two characters at a time
        uint8_t val = stoul(byteStr, nullptr, 16); // Convert hex string to uint8_t
        //cout << "byteStr = " << byteStr << " = " << static_cast<int>(val) << endl;
        db.get()[(i * size_per_item) + j] = val;
        db_copy.get()[(i * size_per_item) + j] = val;
      }
      i++;
    }
  }
  else {
    cerr << "JSON is not an array." << endl;
    return 1;
  }
  //////////////////////////////////////////////////////////////


  // Recommended values: (logt, d) = (20, 2).
  uint32_t logt = 20;
  uint32_t d = 2;
  bool use_symmetric = true; // use symmetric encryption instead of public key
  // (recommended for smaller query)
  bool use_batching = true;  // pack as many elements as possible into a BFV
  // plaintext (recommended)
  bool use_recursive_mod_switching = true;

  // Generates all parameters
  cout << "Main: Loading SEAL parameters" << endl;
  //gen_encryption_params(N, logt, enc_params_test);
  // Save the encryption parameters to a file
  //save_encryption_parameters(enc_params_test, "encryption_parameters.bin");
  // Load encryption parameters from a file
  EncryptionParameters enc_params = load_encryption_parameters("encryption_parameters.bin");
  cout << "Main: Verifying SEAL parameters" << endl;
  verify_encryption_params(enc_params);
  cout << "Main: SEAL parameters are good" << endl;

  PirParams pir_params;
  cout << "Main: Loading PIR parameters" << endl;
  gen_pir_params(number_of_items, size_per_item, d, enc_params, pir_params,
    use_symmetric, use_batching, use_recursive_mod_switching);
    // Load pir parameters from a file
    //pir_params = load_pir_parameters("pir_parameters.bin");

    print_seal_params(enc_params);
    print_pir_params(pir_params);

    // Initialize PIR client....
    PIRClient client(enc_params, pir_params);
    cout << "Main: Generating galois keys for client" << endl;

    GaloisKeys galois_keys = client.generate_galois_keys();


    //////////////////////////////////////////////SERVER////////////////
    // Initialize PIR Server
    cout << "Main: Initializing server" << endl;
    PIRServer server(enc_params, pir_params);

    // Server maps the galois key to client 0. We only have 1 client,
    // which is why we associate it with 0. If there are multiple PIR
    // clients, you should have each client generate a galois key,
    // and assign each client an index or id, then call the procedure below.
    server.set_galois_key(0, galois_keys);


    //////////////////////////////////////////////////////////////////////

    // Choose an index of an element in the DB
    uint64_t ele_index = 2;
    //rd() % number_of_items; // element in DB at random position
    uint64_t index = client.get_fv_index(ele_index);   // index of FV plaintext
    uint64_t offset = client.get_fv_offset(ele_index); // offset in FV plaintext
    cout << "Main: element index = " << ele_index << " from [0, "
    << number_of_items - 1 << "]" << endl;
    cout << "Main: FV index = " << index << ", FV offset = " << offset << endl;

    //////////////////////////////////////////////////////////////
    // Measure database setup
    auto time_pre_s = high_resolution_clock::now();
    server.set_database(move(db), number_of_items, size_per_item);
    server.preprocess_database();
    auto time_pre_e = high_resolution_clock::now();
    auto time_pre_us =
    duration_cast<microseconds>(time_pre_e - time_pre_s).count();
    cout << "Main: database pre processed " << endl;
    
    //////////////////////////////Client////////////////////////////////

    // Measure query generation
    auto time_query_s = high_resolution_clock::now();
    PirQuery query = client.generate_query(index);
    auto time_query_e = high_resolution_clock::now();
    auto time_query_us =
    duration_cast<microseconds>(time_query_e - time_query_s).count();
    cout << "Main: query generated" << endl;

    // Measure serialized query generation (useful for sending over the network)
    stringstream client_stream;
    auto time_s_query_s = high_resolution_clock::now();
    int query_size = client.generate_serialized_query(index, client_stream);
    auto time_s_query_e = high_resolution_clock::now();
    auto time_s_query_us =
    duration_cast<microseconds>(time_s_query_e - time_s_query_s).count();
    cout << "Main: serialized query generated" << endl;
    cout << "Main: Query size: " << query_size << " bytes" << endl;

    // Write data to a binary file
    Write("q1.bin", client_stream);

    /////////////////////////////////Server///////////////////////////////////////////

    // Measure query deserialization (useful for receiving over the network)
    auto time_deserial_s = high_resolution_clock::now();
    PirQuery query2 = server.deserialize_query(client_stream);
    auto time_deserial_e = high_resolution_clock::now();
    auto time_deserial_us =
    duration_cast<microseconds>(time_deserial_e - time_deserial_s).count();
    cout << "Main: query deserialized" << endl;
    // Measure query processing (including expansion)
    auto time_server_s = high_resolution_clock::now();
    // Answer PIR query from client 0. If there are multiple clients,
    // enter the id of the client (to use the associated galois key).
    PirReply reply = server.generate_reply(query2, 0);
    auto time_server_e = high_resolution_clock::now();
    auto time_server_us =
    duration_cast<microseconds>(time_server_e - time_server_s).count();
    cout << "Main: reply generated" << endl;

    // Serialize reply (useful for sending over the network)
    stringstream server_stream;
    int reply_size = server.serialize_reply(reply, server_stream);

    // Write data to a binary file
    Write("a1.bin", server_stream);

    /////////////////////////////////Client///////////////////////////////////////////
    // Read data from the binary file into the stringstream
    stringstream read_stream;
    Read("a1.bin", read_stream);
    // Measure reply deserialization (useful for receiving over the network)
    PirReply reply2 = client.deserialize_reply(read_stream);

    // Measure response extraction
    auto time_decode_s = high_resolution_clock::now();
    vector<uint8_t> elems = client.decode_reply(reply2, offset);
    auto time_decode_e = high_resolution_clock::now();
    auto time_decode_us =
    duration_cast<microseconds>(time_decode_e - time_decode_s).count();
    cout << "Main: reply decoded" << endl;

    assert(elems.size() == size_per_item);

    string decodedVal = VectorToHexString(elems);
    cout << decodedVal << endl;

    Value::ConstMemberIterator it = obj.MemberBegin();
    std::advance(it, ele_index); // Move the iterator to the i-th position
    //string key = it->name.GetString();
    string value = it->value.GetString();

    cout << value << endl;

    int result = decodedVal.compare(value);

    if (result == 0) {
      std::cout << "The strings are EQUAL." << std::endl;
    } else {
      std::cout << "The strings are NOT equal." << std::endl;
    }

    printf("Client end\r\n");

    return 0;
  }
