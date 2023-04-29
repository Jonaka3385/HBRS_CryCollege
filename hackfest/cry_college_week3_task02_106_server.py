import socket
from week1.cipher import XORCipher
from week3 import curves
from week3.elliptic_curve import AffinePoint
import random

GEN = curves.CurveP256.gen
curve = curves.CurveP256
rng = random.Random()
CURVE_COORDINATE_BYTES = 32

# Zieladresse und Port des Servers
SERVER_ADDRESS = ('hackfest.redrocket.club', 21002)


def main():
    # Socket erstellen und Verbindung zum Server aufbauen
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Zufälligen privaten Schlüssel und öffentlichen Schlüssel generieren
    client_private = rng.randint(0, GEN.order)
    client_public = client_private * GEN

    # Nachricht an den Server senden
    # Erste 32 Bytes der Nachricht sind x-Koordinate des öffentlichen Schlüssels
    # Letzte 32 Bytes sind y-Koordinate des öffentlichen Schlüssels
    msg = abs(round(client_public.x)).to_bytes(CURVE_COORDINATE_BYTES*2, "big")
    msg += abs(round(client_public.y)).to_bytes(CURVE_COORDINATE_BYTES*2, "big")
    sock.sendto(msg, SERVER_ADDRESS)

    # Antwort des Servers empfangen
    response, server_address = sock.recvfrom(128 + 29) # 128 Bytes für den öffentlichen Schlüssel, 29 Bytes für den verschlüsselten Flag
    server_public_x = int.from_bytes(response[:CURVE_COORDINATE_BYTES], "big")
    server_public_y = int.from_bytes(response[CURVE_COORDINATE_BYTES:2*CURVE_COORDINATE_BYTES], "big")
    server_public = AffinePoint(curve, server_public_x, server_public_y)
    ciphertext = response[2*CURVE_COORDINATE_BYTES:]

    # Schlüsselaustausch mit dem Server durchführen
    key = client_private * server_public
    key = key.x.elem.to_bytes(CURVE_COORDINATE_BYTES, "big")[:32]

    # Flag entschlüsseln
    cipher = XORCipher(key)
    flag = cipher.decrypt(ciphertext).decode()

    # Flag ausgeben
    print(flag)


if __name__ == "__main__":
    main()
