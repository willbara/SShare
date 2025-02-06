import ctypes
import os
import sys

def load_library(lib_path):
    try:
        return ctypes.CDLL(lib_path)
    except OSError as e:
        print(f"Error loading DLL at {lib_path}: {e}", file=sys.stderr)
        return None

# Construct path relative to THIS file (encryption_wrapper.py)
lib_dir = os.path.join(os.path.dirname(__file__), '../cpp/build')
lib_path = os.path.join(lib_dir, 'libencrypt.dll')

encrypt_lib = load_library(lib_path)

if encrypt_lib is None:
    exit(1)  # Exit with an error code if DLL loading fails


def encrypt_file(input_file: str, password: str) -> str:
    output_file = f"{input_file}.enc"
    result = encrypt_lib.encrypt_file(  # Assuming these are the correct function names
        input_file.encode('utf-8'),
        output_file.encode('utf-8'),
        password.encode('utf-8')
    )
    if result != 0:
        raise Exception("[!] Encryption failed.")
    return output_file


def decrypt_file(encrypted_file: str, password: str) -> str:
    output_file = encrypted_file.replace('.enc', '.dec')
    result = encrypt_lib.decrypt_file(  # Assuming these are the correct function names
        encrypted_file.encode('utf-8'),
        output_file.encode('utf-8'),
        password.encode('utf-8')
    )
    if result != 0:
        raise Exception("[!] Decryption failed. Incorrect password?")
    return output_file