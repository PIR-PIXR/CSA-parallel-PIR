#include <condition_variable>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <grpcpp/grpcpp.h>

#include "proto/pirmessage.grpc.pb.h"
#include "pir.hpp"
#include "pir_client.hpp"
#include "/home/nhat/Desktop/vcpkg/installed/x64-linux/include/rapidjson/document.h"
//#include "/home/dowload/vcpkg/installed/x64-linux/include/rapidjson/document.h"
#include "helper.hpp"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using pir_message::PIRService;
using pir_message::RequestData;
using pir_message::ResponseData;

using namespace std::chrono;
using namespace std;
using namespace seal;
using namespace rapidjson;

class ClientWorker {
 public:
  ClientWorker(std::shared_ptr<Channel> channel)
      : stub_(PIRService::NewStub(channel)) {}

  ClientWorker(std::shared_ptr<Channel> channel,std::string jsfile,uint64_t eIndex)
      : stub_(PIRService::NewStub(channel)),jsonDBFileName(jsfile),ele_index(eIndex) {

      }

  int GetDBInfor(pir_message::DBInfo &dbInfo) {
      ClientContext context;  
      pir_message::EmptyParam emptyParam;
      Status status =  stub_->GetDBInfo(&context,emptyParam,&dbInfo);
      if (status.ok()) {
        return 0;
      }else{
        return -1;
      }
  }
  // Assembles the client's payload, sends it and presents the response back
  // from the server.
  std::string GetPIRFromServer(PIRClient *pirClient,const RequestData& request) {        
    ClientContext context;
    ResponseData reply;

    Status status = stub_->GetPIR(&context,request,&reply);
    if (status.ok()) {      
      
       stringstream read_stream;
       read_stream.str(reply.data());
    /////////////////////////////////Client///////////////////////////////////////////
    // Read data from the binary file into the stringstream

      PirReply reply = pirClient->deserialize_reply(read_stream);

      //cout << "Decode response from server" << endl;
      // Measure response extraction
      auto time_decode_s = high_resolution_clock::now();
      vector<uint8_t> elems = pirClient-> decode_reply(reply, offset);
      auto time_decode_e = high_resolution_clock::now();
      auto time_decode_us = duration_cast<microseconds>(time_decode_e - time_decode_s).count();
      cout << "Client: answer decode time: " << time_decode_us << " us" << endl;

      string decodedVal = VectorToHexString(elems);
      cout <<"Server response: "<<decodedVal << endl;

      //validate with database
      //std::string result = ValidateResult(jsonDBFileName,elems,decodedVal);
      //return result;
      return "The strings are EQUAL.";
    } else {
      std::cout << status.error_code() << ": " << status.error_message()
                << std::endl;
      return "RPC failed";
    }
  
  }

  std::string ValidateResult(std::string jsonFile,const vector<uint8_t> &elems,const std::string &decodedVal){
      Document doc;
      uint64_t number_of_items;
      uint64_t size_per_item;

      get_seal_params(jsonFile,number_of_items,size_per_item,doc);

      cout <<"Validate result with database: ";
      assert(elems.size() == size_per_item);

      //validate
      const Value& obj = doc[0];
      Value::ConstMemberIterator it = obj.MemberBegin();
      std::advance(it, ele_index); // Move the iterator to the i-th position
      //string key = it->name.GetString();
      string value = it->value.GetString();

      cout << value << endl;

      int result = decodedVal.compare(value);     
      if (result == 0) {
        //std::cout << "The strings are EQUAL." << std::endl;
          return "The strings are EQUAL.";
      } else {
          //std::cout << "The strings are NOT equal." << std::endl;
          return "The strings are NOT equal.";
      }    
  }

  
  int PrepareData(uint64_t number_of_items,uint64_t size_per_item,PIRClient* &pirClient,RequestData &requestData){
    
    uint32_t logt = 20;
    uint32_t d = 2;
    bool use_symmetric = true; // use symmetric encryption instead of public key
    // (recommended for smaller query)
    bool use_batching = true;  // pack as many elements as possible into a BFV
    // plaintext (recommended)
    bool use_recursive_mod_switching = true;
   
    auto ecp = loadFileToString("encryption_parameters.bin");
    if (ecp.size() ==0) {
      return -1;
    }
   
    //enc_params = load_encryption_parameters("encryption_parameters.bin");
    EncryptionParameters enc_params = load_encryption_parameters_from_string(ecp);
    //cout << "Verifying SEAL parameters" << endl;
    verify_encryption_params(enc_params);
    //cout << "SEAL parameters are good" << endl;

    PirParams pir_params;
    gen_pir_params(number_of_items, size_per_item, d, enc_params, pir_params,
      use_symmetric, use_batching, use_recursive_mod_switching);
   
    print_seal_params(enc_params);
    print_pir_params(pir_params);
    pirClient = new PIRClient(enc_params, pir_params);
    //cout << "Generating galois keys for client" << endl;
    GaloisKeys galois_keys = pirClient->generate_galois_keys();

    string gkey = SEALSerialize(galois_keys);
    

    //Generate query
    // Choose an index of an element in the DB
   
    //rd() % number_of_items; // element in DB at random position
    uint64_t index = pirClient->get_fv_index(ele_index);   // index of FV plaintext
    offset = pirClient->get_fv_offset(ele_index); // offset in FV plaintext
    cout << "element index = " << ele_index << " from [0, "
    << number_of_items - 1 << "]" << endl;
    //cout << "FV index = " << index << ", FV offset = " << offset << endl;

    auto time_query_s = high_resolution_clock::now();
    PirQuery query = pirClient->generate_query(index);
    auto time_query_e = high_resolution_clock::now();
    auto time_query_us = duration_cast<microseconds>(time_query_e - time_query_s).count();
    cout << "Client: Query generated" << endl;
    cout << "Client: Query generation time: " << time_query_us << " us" << endl;

   // Measure serialized query generation (useful for sending over the network)
    stringstream client_stream;
    auto time_s_query_s = high_resolution_clock::now();
    int query_size = pirClient->generate_serialized_query(index, client_stream);
    auto time_s_query_e = high_resolution_clock::now();
    auto time_s_query_us =
    duration_cast<microseconds>(time_s_query_e - time_s_query_s).count();
    //cout << "Client: serialized query generated" << endl;
    cout << "Client: Query size: " << query_size << " bytes" << endl;
    
    requestData.set_clientid(1);
    requestData.set_requestid(1);       
    requestData.mutable_pirconfig()->set_use_symmetric(use_symmetric);
    requestData.mutable_pirconfig()->set_use_batching(use_batching);
    requestData.mutable_pirconfig()->set_use_recursive_mod_switching(use_recursive_mod_switching);
    requestData.mutable_pirconfig()->set_d(2);
    requestData.mutable_pirconfig()->set_num_of_items(number_of_items);
    requestData.mutable_pirconfig()->set_size_per_item(size_per_item);

    requestData.mutable_pirconfig()->mutable_epparams()->assign(ecp);
    requestData.set_gkey(gkey);
    requestData.set_query(client_stream.str());
    
    cout<<"End Query phase"<<endl;
    return 0;
}

 private:
  std::unique_ptr<PIRService::Stub> stub_;
  uint64_t ele_index;
  uint64_t offset;
  std::string jsonDBFileName;
 
};


int main(int argc, char** argv) { 
     
    cout<<"Get list server"<<endl;
    std::vector<ClientRequestInfo> listServers = getListServers("servers_list.txt");   
    vector<ClientRequestInfo>::iterator ptr; 
    for (ptr = listServers.begin(); ptr < listServers.end(); ptr++) {
        cout<<"================BEGIN============="<<endl;
        cout<<"Get PIR with info: ";
        ptr->print();
        ClientWorker client(grpc::CreateChannel(ptr->hostAddr, grpc::InsecureChannelCredentials()),ptr->jsDBFile,ptr->eIndex);
        pir_message::DBInfo dbInfo;
        if (client.GetDBInfor(dbInfo) >=0) {
            RequestData requestData;
            PIRClient *pirClient = NULL;
            if (client.PrepareData(dbInfo.num_of_items(),dbInfo.size_per_item(),pirClient,requestData) >=0) {

                std::string result = client.GetPIRFromServer(pirClient,requestData);
                cout<<"Result: "<<result<<endl;

            }else{
              cout<<"Prepare data error. Cannot get encription parameters."<<endl;
            }
            if (pirClient != NULL) {
              delete pirClient;
            }
            requestData.Clear();
        }else{
            cout<<"Cannot get database information"<<endl;
        }
        cout<<"================END==============="<<endl;
        ptr -> clear(); 
    }
    listServers.clear();
    cout<<"Finished all queries"<<endl;
    return 0;
}
