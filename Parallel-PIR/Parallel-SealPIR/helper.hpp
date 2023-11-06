#ifndef __HELPER__
#define __HELPER__
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
#include "/home/nhat/Desktop/vcpkg/installed/x64-linux/include/rapidjson/document.h"
//#include "/home/dowload/vcpkg/installed/x64-linux/include/rapidjson/document.h"

using namespace seal;
using namespace rapidjson;

struct ClientRequestInfo {
    uint64_t eIndex;
    std::string hostAddr;
    std::string jsDBFile;
    void print(){
        cout<<"host: "<<hostAddr<<", db: "<<jsDBFile<<", element index: "<<eIndex<<endl;
    }
    void clear(){
        hostAddr.clear();
        jsDBFile.clear();
    }
};

void Write(const string& filename, stringstream& dataStream) ;
void Read(const string& filename, stringstream& dataStream);
string VectorToHexString(const vector<uint8_t>& elems) ;
EncryptionParameters load_encryption_parameters(const string &filename);
EncryptionParameters load_encryption_parameters_from_buffer(const std::vector<uint8_t>  &buffer);
std::vector<uint8_t>  loadFileToBuffer(const string &filename);
EncryptionParameters load_encryption_parameters_from_string(const string  &buffer);
std::string loadFileToString(const string &filename);
void save_pir_parameters(const PirParams &pir_params, const string &filename);
std::vector<uint8_t>  get_seal_params(string jsonFile,uint64_t &number_of_items,uint64_t &size_per_item,Document &doc);
std::unique_ptr<uint8_t[]>  readDatabase(string jsonFile,uint64_t &number_of_items,uint64_t &size_per_item);
PirParams load_pir_parameters(const string &filename);
PIRClient create_pir_params(string encryptionFile,PirParams &pir_params,uint64_t number_of_items,uint64_t size_per_item);
int parseRequestInfo(const std::string &str,ClientRequestInfo &clientRequestInfo);
std::vector<ClientRequestInfo> getListServers(const string &filename);

#endif
