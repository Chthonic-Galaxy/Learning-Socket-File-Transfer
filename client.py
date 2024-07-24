import socket
import os

import time

HOST = ""    # Server IP/HOST
PORT = 65432 # Server PORT
BUFFER_SIZE = 1024*1024

client_socket = socket.socket()

try:
    client_socket.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")
except Exception as e:
    print(f"Connecrion failed due to {e}")
    exit()

try:
    while True:
        filename = input("Enter file name >>> ")
        client_socket.send(filename.encode())
        filesize = int(client_socket.recv(BUFFER_SIZE).decode())
        
        if filesize:
            client_socket.send(str(1).encode()) # Flag
            
            print(f"File size: {filesize}")
            filepath = os.path.join("SAVED", filename)
            with open(filepath, "wb") as file:
                received = 0
                while received < filesize:
                    data = client_socket.recv(BUFFER_SIZE)
                    if not data: 
                        break  
                    file.write(data)
                    received += len(data)
                    print(f" Progress - {received / filesize * 100:.2f}%")
            if received == filesize:
                print("+ File was downloaded")
            else:
                print("- File downloading - FAILED")
        else:
            client_socket.send(str(0).encode()) # Flag
            print(f"File doesn't exists. Try again.")
except Exception as e:
    print(e)
finally:
    client_socket.close()