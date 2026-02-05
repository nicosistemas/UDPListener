# UDPListener developed by LU2FTI
# N1MM console log
# v4
# https://github.com/nicosistemas/UDPListener
#
import socket
import xml.etree.ElementTree as ET
from datetime import datetime

UDP_IP = "0.0.0.0"
UDP_PORT = 12060

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Escuchando N1MM UDP en puerto {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(4096)
    try:
        xml_str = data.decode("utf-8", errors="ignore")
        root = ET.fromstring(xml_str)

        timestamp = root.findtext("timestamp", default="")
        mycall = root.findtext("mycall", default="")
        txfreq = root.findtext("txfreq", default="0")
        band = root.findtext("band", default="?")
        mode = root.findtext("mode", default="?")
        call = root.findtext("call", default="")

        # Convertir frecuencia a MHz correctamente
        try:
            freq_mhz = int(txfreq) / 100_000  # ⚡ 712300 → 7.123 MHz
        except ValueError:
            freq_mhz = 0.0

        # Formatear timestamp si viene vacío
        if not timestamp:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"{timestamp} | {mycall} | {freq_mhz:.3f} MHz | {band} | {mode} | {call}")

    except ET.ParseError:
        print("Error parseando XML")
    except Exception as e:
        print("Error procesando paquete:", e)