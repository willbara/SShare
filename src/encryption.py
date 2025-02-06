from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

# Derive a key from the password
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(
        salt=salt,
        length=32,  # AES-256
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt the file
def encrypt_file(input_file: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read and pad the file
    with open(input_file, 'rb') as f:
        data = f.read()
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    # Write the encrypted file
    encrypted_file = f"{input_file}.enc"
    with open(encrypted_file, 'wb') as f:
        f.write(salt + iv + encryptor.update(padded_data) + encryptor.finalize())

    return encrypted_file

# Decrypt the file
def decrypt_file(encrypted_file: str, password: str) -> str:
    with open(encrypted_file, 'rb') as f:
        salt = f.read(16)
        iv = f.read(16)
        ciphertext = f.read()
    
    key = derive_key(password, salt)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the data
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    # Write the decrypted file
    decrypted_file = encrypted_file.replace('.enc', '.dec')
    with open(decrypted_file, 'wb') as f:
        f.write(data)

    return decrypted_file
