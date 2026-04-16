# UDPListener developed by LU2FTI
# N1MM to ADIF format + MiniLog API bridge
# Desde N1MM escribe en ADI el UDPListener escucha y tira los QSO al Minilog mediante la api de Minilog /api/qso
# v4.1
# https://github.com/nicosistemas/UDPListener
#

import socket
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import requests

UDP_IP = "0.0.0.0"
UDP_PORT = 12060
ADIF_FILE = Path("n1mm_udp_log.adi")

# MiniLog API endpoint
#MINILOG_URL = "http://localhost:5000/api/qso"
MINILOG_URL = "http://IPIPIPIPIPIPIP:5000/api/qso"

# Crear archivo ADIF con header si no existe
if not ADIF_FILE.exists():
    with ADIF_FILE.open("w", encoding="utf-8") as f:
        f.write("Generated UDPListener by LU2FTI\n<EOH>\n")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Escuchando N1MM UDP en puerto {UDP_PORT}...")

while True:
    data, addr = sock.recvfrom(4096)

    try:
        xml_str = data.decode("utf-8", errors="ignore")
        root = ET.fromstring(xml_str)

        # ================================
        # Extraer datos
        # ================================
        timestamp = root.findtext("timestamp", default="")
        mycall = root.findtext("mycall", default="")
        txfreq = root.findtext("txfreq", default="0")
        band = root.findtext("band", default="?")
        mode = root.findtext("mode", default="?")
        call = root.findtext("call", default="")

        # ================================
        # Fecha / hora
        # ================================
        if timestamp:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        else:
            dt = datetime.now()

        qso_date = dt.strftime("%Y%m%d")
        time_on = dt.strftime("%H%M%S")

        # ================================
        # Frecuencia
        # ================================
        try:
            freq_mhz = int(txfreq) / 100_000
        except ValueError:
            freq_mhz = 0.0

        # ================================
        # Log consola
        # ================================
        print(f"{qso_date} {time_on} | {mycall} | {freq_mhz:.3f} MHz | {band} | {mode} | {call}")

        # ================================
        # 1. Guardar SIEMPRE en ADIF
        # ================================
        with ADIF_FILE.open("a", encoding="utf-8") as f:
            f.write(f"<QSO_DATE:8>{qso_date} <TIME_ON:6>{time_on} ")
            f.write(f"<CALL:{len(call)}>{call} <BAND:{len(str(band))}>{band} ")
            f.write(f"<FREQ:{len(f'{freq_mhz:.3f}')}>{freq_mhz:.3f} ")
            f.write(f"<MODE:{len(mode)}>{mode} <MY_CALL:{len(mycall)}>{mycall} <EOR>\n")

        # ================================
        # 2. Enviar a MiniLog
        # ================================
        qso = {
            "call": call,
            "mode": mode,
            "freq": round(freq_mhz, 3),
            "mycall": mycall,
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "extra": ""
        }

        try:
            requests.post(MINILOG_URL, json=qso, timeout=1.5)
        except Exception:
            # Si MiniLog está caído no rompe nada
            pass

    except ET.ParseError:
        print("Error parseando XML")
    except Exception as e:
        print("Error procesando paquete:", e)
