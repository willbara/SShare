cmake_minimum_required(VERSION 3.10)
project(SecureShareEncryption)

set(CMAKE_CXX_STANDARD 11)

# Include OpenSSL headers
include_directories("C:/Program Files/OpenSSL-Win64/include")

# Link against DLLs directly
add_library(encrypt SHARED encryption.cpp)

# Link to the DLLs instead of static libs
target_link_libraries(encrypt "C:/Program Files/OpenSSL-Win64/libcrypto-3-x64.dll" "C:/Program Files/OpenSSL-Win64/libssl-3-x64.dll")
