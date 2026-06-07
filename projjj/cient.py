import socket
import ssl
from typing import Final
import time
from datetime import datetime 


PORT_TELECOMANDA: Final[int] = 5005
TIMEOUT: Final[int] = 5
ADRESA_TELECOMANDA: Final[str] = 'proiectt.sbs'
#ADRESA_TELECOMANDA: Final[str] = '192.168.0.93'


context = ssl.create_default_context()
telecomanda_nesecurizata = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
telecomanda_nesecurizata.settimeout(TIMEOUT)
#telecomanda = context.wrap_socket(telecomanda_nesecurizata, server_hostname='proiectt.sbs')
telecomanda = telecomanda_nesecurizata
print("telecomanda creata, asteapta conexiune...")

try:
    print(f"incerc conexiune la {ADRESA_TELECOMANDA}:{PORT_TELECOMANDA}...")
    telecomanda.connect((ADRESA_TELECOMANDA, PORT_TELECOMANDA))
    print("conexiune stabilita cu telecomanda")
    mesaj="Lumina: OFF, Temperatura: 22C, Alarma: ON"
    telecomanda.send(mesaj.encode())
    print("telecomanda trimisa")


except socket.timeout:
    print("❌ Timeout (host unreachable / firewall drop)")

except ConnectionRefusedError:
    print("❌ Connection refused (port closed)")

except socket.gaierror:
    print("❌ DNS resolution failed")

except OSError as e:
    print(f"❌ OS error: {e}")

finally:
    telecomanda.close()
