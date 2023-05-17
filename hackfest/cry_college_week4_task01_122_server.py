from week1.communication import send_receive
from week4.curve25519 import X25519

# Do a full X25519 key-agreement against the following UDP server:
# (hackfest.redrocket.club,24001)


class XORCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, enData):
        if not isinstance(enData, bytes):
            raise ValueError("You can only encrypt bytes")
        output = bytearray()

        for i in range(len(enData)):
            output.append(enData[i] ^ self.key[i % len(self.key)])

        return bytes(output)

    def decrypt(self, deData):
        return self.encrypt(deData)


if __name__ == "__main__":
    curve = X25519(1234)
    print(curve.pk_bytes)
    data = send_receive('hackfest.redrocket.club', 24001, curve.pk_bytes)

    pub_key = data[0][:32]
    shared_key = curve.exchange(pub_key)
    cipher = XORCipher(shared_key)
    encrypted_msg = data[0][32:]
    decrypted_msg = cipher.decrypt(encrypted_msg)

    print(f"Flag: {decrypted_msg.decode('utf-8')}")
