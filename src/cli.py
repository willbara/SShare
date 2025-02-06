import argparse
from encryption_wrapper import encrypt_file, decrypt_file
from file_transfer import send_file, receive_file

def main():
    parser = argparse.ArgumentParser(description="Secure File Sharing with AES Encryption (Python + C++)")
    
    # Encrypt file
    parser.add_argument('--encrypt', type=str, help='File to encrypt')
    parser.add_argument('--password', type=str, help='Password for encryption/decryption')
    
    # Send file
    parser.add_argument('--send', action='store_true', help='Send encrypted file to a user')
    parser.add_argument('--to', type=str, help='Recipient IP address')
    parser.add_argument('--port', type=int, default=5000, help='Port for file transfer')
    
    # Receive file
    parser.add_argument('--receive', action='store_true', help='Receive a file on specified port')

    args = parser.parse_args()

    if args.encrypt:
        if not args.password:
            print("[!] Password is required for encryption.")
            return
        encrypted_file = encrypt_file(args.encrypt, args.password)
        print(f"[+] File encrypted as '{encrypted_file}'")

        if args.send and args.to:
            send_file(args.to, args.port, encrypted_file)
    
    elif args.receive:
        received_file = receive_file(args.port)
        password = input("Enter password to decrypt the file: ")
        decrypted_file = decrypt_file(received_file, password)
        print(f"[+] File decrypted successfully as '{decrypted_file}'")

if __name__ == "__main__":
    main()
