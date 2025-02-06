import socket
import os
import time
import threading

BUFFER_SIZE = 4096
TIMEOUT_SECONDS = 10

def send_file(ip: str, port: int, file_path: str):
    """Send a file to the specified IP and port with error handling."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[+] Connecting to {ip}:{port}...")
            s.connect((ip, port))
            file_size = os.path.getsize(file_path)
            
            # Send the file name and size
            s.send(f"{os.path.basename(file_path)}|{file_size}".encode())
            s.recv(BUFFER_SIZE)  # Wait for ACK before sending the file
            
            with open(file_path, 'rb') as f:
                while chunk := f.read(BUFFER_SIZE):
                    s.sendall(chunk)
            
            print(f"[+] File '{file_path}' sent successfully to {ip}:{port}")

    except ConnectionRefusedError:
        print(f"[!] Connection to {ip}:{port} was refused. Is the recipient listening?")
    
    except TimeoutError:
        print(f"[!] Connection to {ip}:{port} timed out. Please check your network settings.")
    
    except socket.gaierror:
        print(f"[!] Invalid IP address or hostname: {ip}")
    
    except Exception as e:
        print(f"[!] An unexpected error occurred while sending the file: {str(e)}")

def countdown_timer(stop_event):
    """Display a countdown timer while waiting for a connection."""
    for remaining in range(TIMEOUT_SECONDS, 0, -1):
        if stop_event.is_set():
            break
        print(f"[+] Waiting for connection... {remaining} seconds remaining", end='\r')
        time.sleep(1)
    print("\n", end='')  # Move to the next line after countdown

def receive_file(port: int) -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(TIMEOUT_SECONDS)
        s.bind(('', port))
        s.listen(1)
        print(f"[+] Listening for incoming files on port {port}...")

        stop_event = threading.Event()
        timer_thread = threading.Thread(target=countdown_timer, args=(stop_event,))
        timer_thread.start()

        try:
            conn, addr = s.accept()
            stop_event.set()  # Stop the countdown when a connection is made
            with conn:
                print(f"[+] Connection established with {addr}")
                
                metadata = conn.recv(BUFFER_SIZE).decode()
                file_name, file_size = metadata.split('|')
                file_size = int(file_size)
                conn.send(b"ACK")

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

        except socket.timeout:
            stop_event.set()
            print(f"[!] No connection received within {TIMEOUT_SECONDS} seconds. Stopping listener.")

        except Exception as e:
            stop_event.set()
            print(f"[!] An error occurred while receiving the file: {str(e)}")