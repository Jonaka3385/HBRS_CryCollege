import socketserver
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey


# Do a full X25519 key-agreement against the following UDP server:
# (hackfest.redrocket.club,24001)


class XORCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        if not isinstance(data, bytes):
            raise ValueError("You can only encrypt bytes.")
        output = bytearray()

        for i in range(len(data)):
            output.append(data[i] ^ self.key[i % len(self.key)])

        return bytes(output)

    def decrypt(self, data):
        return self.encrypt(data)


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        socket = self.request[1]

        # First 32 bytes are the public key
        peer_pubkey = data[:32]

        private_key = X25519PrivateKey.generate()
        public_key = private_key.public_key()

        enc_key = private_key.exchange(X25519PublicKey.from_public_bytes(peer_pubkey))

        msg = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

        cipher = XORCipher(enc_key)

        msg += cipher.encrypt(FLAG)

        # Send 32 bytes public key + ciphertext
        socket.sendto(msg, self.client_address)


class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 24001
    with ThreadingUDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
