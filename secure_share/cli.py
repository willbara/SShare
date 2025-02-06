from secure_share.encryption import encrypt_file, decrypt_file
from secure_share.file_transfer import send_file, receive_file

def main():
    print("\n=== Secure Share CLI ===")
    
    while True:
        print("\nWhat do you want to do?")
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Send a file")
        print("4. Receive a file")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == '1':
            input_file = input("Enter the file to encrypt: ").strip()
            password = input("Enter a password: ").strip()
            encrypted_file = encrypt_file(input_file, password)
            print(f"[+] File encrypted as '{encrypted_file}'")

        elif choice == '2':
            encrypted_file = input("Enter the file to decrypt: ").strip()
            password = input("Enter the password: ").strip()
            decrypted_file = decrypt_file(encrypted_file, password)
            print(f"[+] File decrypted as '{decrypted_file}'")

        elif choice == '3':
            ip = input("Enter the recipient's IP address: ").strip()
            port = int(input("Enter the port (default 5000): ").strip() or "5000")
            file_path = input("Enter the file to send: ").strip()
            send_file(ip, port, file_path)

        elif choice == '4':
            port = int(input("Enter the port to listen on (default 5000): ").strip() or "5000")
            received_file = receive_file(port)
            print(f"[+] Received file: {received_file}")

        elif choice == '5':
            print("Exiting Secure Share. Goodbye!")
            break

        else:
            print("[!] Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()