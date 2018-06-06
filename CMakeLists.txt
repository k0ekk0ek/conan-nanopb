cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

find_program(PROTOC_PATH NAMES protoc)
if(PROTOC_PATH)
    set(nanopb_PROTOC_PATH ${PROTOC_PATH})
endif()

add_subdirectory("source_subfolder")
