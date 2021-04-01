import socket

HOST = '127.0.0.1'
PORT = 80

num = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes([num, num]))
    data = s.recv(1024)
