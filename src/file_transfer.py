import socket
import os

BUFFER_SIZE = 4096

def send_file(ip: str, port: int, file_path: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        file_size = os.path.getsize(file_path)
        
        # Send the file name and size first
        s.send(f"{os.path.basename(file_path)}|{file_size}".encode())
        
        ack = s.recv(BUFFER_SIZE).decode()  # Wait for acknowledgment before sending file

        with open(file_path, 'rb') as f:
            while (chunk := f.read(BUFFER_SIZE)):
                s.sendall(chunk)
        
        print(f"[+] File '{file_path}' sent successfully to {ip}:{port}")

def receive_file(port: int) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen(1)
        print(f"[+] Listening for incoming files on port {port}...")

        conn, addr = s.accept()
        with conn:
            print(f"[+] Connection established with {addr}")
            
            # Receive file name and size
            metadata = conn.recv(BUFFER_SIZE).decode()
            file_name, file_size = metadata.split('|')
            file_size = int(file_size)

            conn.send("ACK".encode())  # Send acknowledgment to start file transfer
            
            received_file = f"received_{file_name}"
            with open(received_file, 'wb') as f:
                received = 0
                while received < file_size:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)
            
            print(f"[+] File '{received_file}' received successfully!")
            return received_file