# UDPListener developed by LU2FTI
# N1MM raw
# v4
# https://github.com/nicosistemas/UDPListener
#
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 12060

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Escuchando N1MM UDP en puerto {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(4096)
    print(f"\nPaquete desde {addr}, {len(data)} bytes\n")
    print(data.decode("utf-8", errors="ignore"))
    print("-" * 80)