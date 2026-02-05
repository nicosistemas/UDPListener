# UDPListener developed by LU2FTI
# JTDX raw
# v4
# https://github.com/nicosistemas/UDPListener
#
import socket
import binascii

UDP_IP = "0.0.0.0"
UDP_PORT = 2237

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Escuchando JTDX UDP en 2237...")

while True:
    data, addr = sock.recvfrom(4096)
    print("Desde:", addr)
    print("Bytes:", len(data))
    print(binascii.hexlify(data[:32]))
    print("-" * 40)
