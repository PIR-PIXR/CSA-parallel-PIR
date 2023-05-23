cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
project(SealPIR VERSION 2.2 LANGUAGES CXX)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)

find_package(SEAL 4.0 REQUIRED)

add_library(sealpir pir.hpp pir.cpp pir_client.hpp pir_client.cpp pir_server.hpp pir_server.cpp)
target_link_libraries(sealpir SEAL::seal)

add_executable(main main.cpp)
target_link_libraries(main sealpir)
