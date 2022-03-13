# EXAMPLE IMPLEMENTATION

from http import server
import socket
import sys
import pyDHE
from math import ceil

HOST = "192.168.0.105"
print(HOST)
PORT = 40001 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    client_key = pyDHE.new(14)
    client_pubkey = client_key.getPublicKey()
    s.sendall(client_pubkey.to_bytes(ceil(client_pubkey.bit_length()/8), sys.byteorder, signed=False))
    server_pubkey = int.from_bytes(s.recv(2048),sys.byteorder,signed=False)
    shared_key = client_key.update(server_pubkey)
    print(shared_key)


