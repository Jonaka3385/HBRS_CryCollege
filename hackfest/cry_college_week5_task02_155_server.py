import socketserver
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

try:
    from secret import FLAG
except ImportError:
    # Fake flag for local testing
    FLAG = "CRY{????????????????}"

CHALLENGE = b"Yes, I did eat the last cookie!"


class MyUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0]
        socket = self.request[1]

        # First 32 bytes are the public key
        peer_pubkey = data[:32]
        peer_signature = data[32:]

        pubkey = ed25519.Ed25519PublicKey.from_public_bytes(peer_pubkey)

        try:
            pubkey.verify(peer_signature, CHALLENGE)
            msg = FLAG
        except InvalidSignature:
            msg = b"The signature did not verify!"

        # Send message back
        socket.sendto(msg, self.client_address)


class ThreadingUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 21555
    with ThreadingUDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
