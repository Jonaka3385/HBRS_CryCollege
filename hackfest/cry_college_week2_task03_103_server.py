import socketserver
import random
from week2 import finitefield
from week1.cipher import XORCipher


# Use a safe RNG
rng = random.SystemRandom()
# The Prime and generator is given as the first oakley group: https://tools.ietf.org/html/rfc2409#section-6.1
PRIME = """
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A63A3620 FFFFFFFF FFFFFFFF
"""
oakley_prime = int(PRIME.replace("\n", "").replace(" ", ""), 16)

F = finitefield.PrimeField(oakley_prime)
# generator of oakley group
GENERATOR = F(2)
DH_KEY_BYTE_LEN = 96

class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        socket = self.request[1]

        server_privkey = rng.randint(0, oakley_prime)
        server_pubkey = GENERATOR**server_privkey
        
        # First 96 bytes of message are the public key
        client_pubkey_bytes = data[:DH_KEY_BYTE_LEN]
        # Convert to int, big-endian
        client_pubkey = int.from_bytes(client_pubkey_bytes, "big")
        # Convert to field element
        client_pubkey = F(client_pubkey)

        # do FFDH
        key = client_pubkey**server_privkey
        # Use first 32 bytes of FFDH agreed secret as key
        key = key.elem.to_bytes(DH_KEY_BYTE_LEN, "big")[:32]
        # Encrypt flag
        cipher = XORCipher(key)
        ciphertext = cipher.encrypt(FLAG.encode())

        # Return server pubkey + encrypted flag
        # 96 bytes pubkey
        msg = server_pubkey.elem.to_bytes(96, "big")
        # 29 bytes flag
        msg += ciphertext

        socket.sendto(msg, self.client_address)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 21001
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
