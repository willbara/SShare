#ifndef ENCRYPTION_H
#define ENCRYPTION_H

extern "C" {
    int encrypt_file(const char *input_file, const char *output_file, const char *password);
    int decrypt_file(const char *input_file, const char *output_file, const char *password);
}

#endif