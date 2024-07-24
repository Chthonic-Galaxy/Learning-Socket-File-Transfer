import socket
import os

HOST = "0.0.0.0" # Listening to all available interfaces
PORT = 65432     # Any free port (Unregistred ports > 1023)
MAX_CONNECTIONS = 1
BUFFER_SIZE = 1024*1024
TIMEOUT = 20

def check_file(filename: str) -> int:
    filepath = os.path.join("FILES", filename)
    if os.path.exists(filepath):
        return os.path.getsize(filepath)
    return 0

server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_CONNECTIONS)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connected by {addr}")
    try:
        while True:
            filename = client_socket.recv(BUFFER_SIZE).decode()
            if not filename:
                break
            
            filesize = check_file(filename)
            client_socket.send(str(filesize).encode())

            print("Flag waiting...")
            client_socket.settimeout(TIMEOUT)
            try:
                flag = int(client_socket.recv(1).decode())
                print(f"Flag catched - {flag}")
                client_socket.settimeout(None)
            except socket.timeout:
                print(f"Timeout while waiting for flag from {addr}")
                break
            
            if filesize and flag:
                print(f"+ Start file transfering - (FILES/{filename}) to the ({addr})")
                filepath = os.path.join("FILES", filename) 
                with open(filepath, "rb") as file:
                    while True:
                        data = file.read(BUFFER_SIZE)
                        if not data:
                            break
                        client_socket.sendall(data)
                print(f"+ File tramnsfer is DONE - (FILES/{filename}) to the ({addr})")
    except ConnectionError:
        print(f"Connection closed by {addr}")
    finally:
        client_socket.close()

server_socket.close()