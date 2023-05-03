import socketserver
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from week1 import communication


# Do a full X25519 key-agreement against the following UDP server:
# (hackfest.redrocket.club,24001)


if __name__ == "__main__":
    HOST, PORT = "hackfest.redrocket.club", 24001
    communication.send_receive(HOST, PORT, b'')
