from encryption import encrypt_file, decrypt_file
from file_transfer import send_file, receive_file

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
            input_file = input("Enter the path to the file you want to encrypt: ").strip()
            password = input("Enter a password for encryption: ").strip()
            encrypted_file = encrypt_file(input_file, password)
            print(f"[+] File encrypted successfully as '{encrypted_file}'")

        elif choice == '2':
            encrypted_file = input("Enter the path to the encrypted file: ").strip()
            password = input("Enter the password for decryption: ").strip()
            decrypted_file = decrypt_file(encrypted_file, password)
            print(f"[+] File decrypted successfully as '{decrypted_file}'")

        elif choice == '3':
            file_to_send = input("Enter the path to the file you want to send: ").strip()
            ip = input("Enter the recipient's IP address: ").strip()
            port = int(input("Enter the port number (default is 5000): ").strip() or 5000)
            send_file(ip, port, file_to_send)

        elif choice == '4':
            port = int(input("Enter the port number to listen on (default is 5000): ").strip() or 5000)
            received_file = receive_file(port)
            print(f"[+] Received file saved as '{received_file}'")

        elif choice == '5':
            print("Exiting Secure Share. Goodbye!")
            break

        else:
            print("[!] Invalid choice. Please select a valid option (1-5).")

if __name__ == "__main__":
    main()