#include <openssl/evp.h>
#include <openssl/rand.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <cstring>

extern "C" {

// Function to generate key from password using SHA-256
void generate_key(const std::string &password, unsigned char *key) {
    EVP_Digest(password.c_str(), password.length(), key, nullptr, EVP_sha256(), nullptr);
}

// AES encryption function
int encrypt_file(const char *input_file, const char *output_file, const char *password) {
    const int key_length = 32;  // AES-256
    unsigned char key[key_length];
    generate_key(password, key);

    unsigned char iv[16];
    RAND_bytes(iv, sizeof(iv));

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) return -1;

    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key, iv) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }

    std::ifstream infile(input_file, std::ios::binary);
    std::ofstream outfile(output_file, std::ios::binary);

    outfile.write(reinterpret_cast<const char *>(iv), sizeof(iv));  // Save IV at start of file

    std::vector<unsigned char> buffer(4096);
    std::vector<unsigned char> ciphertext(4096 + EVP_CIPHER_block_size(EVP_aes_256_cbc()));

    int len;
    while (infile.read(reinterpret_cast<char *>(buffer.data()), buffer.size())) {
        if (EVP_EncryptUpdate(ctx, ciphertext.data(), &len, buffer.data(), infile.gcount()) != 1) {
            EVP_CIPHER_CTX_free(ctx);
            return -1;
        }
        outfile.write(reinterpret_cast<char *>(ciphertext.data()), len);
    }

    if (EVP_EncryptFinal_ex(ctx, ciphertext.data(), &len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    outfile.write(reinterpret_cast<char *>(ciphertext.data()), len);

    EVP_CIPHER_CTX_free(ctx);
    return 0;
}

// AES decryption function
int decrypt_file(const char *input_file, const char *output_file, const char *password) {
    const int key_length = 32;  // AES-256
    unsigned char key[key_length];
    generate_key(password, key);

    std::ifstream infile(input_file, std::ios::binary);
    std::ofstream outfile(output_file, std::ios::binary);

    unsigned char iv[16];
    infile.read(reinterpret_cast<char *>(iv), sizeof(iv));

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) return -1;

    if (EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key, iv) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }

    std::vector<unsigned char> buffer(4096);
    std::vector<unsigned char> plaintext(4096 + EVP_CIPHER_block_size(EVP_aes_256_cbc()));

    int len;
    while (infile.read(reinterpret_cast<char *>(buffer.data()), buffer.size())) {
        if (EVP_DecryptUpdate(ctx, plaintext.data(), &len, buffer.data(), infile.gcount()) != 1) {
            EVP_CIPHER_CTX_free(ctx);
            return -1;
        }
        outfile.write(reinterpret_cast<char *>(plaintext.data()), len);
    }

    if (EVP_DecryptFinal_ex(ctx, plaintext.data(), &len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    outfile.write(reinterpret_cast<char *>(plaintext.data()), len);

    EVP_CIPHER_CTX_free(ctx);
    return 0;
}

}