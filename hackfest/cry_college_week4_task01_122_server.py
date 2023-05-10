from week1.communication import send_receive
from week4.curve25519 import X25519
from week1.cipher import XORCipher

# Do a full X25519 key-agreement against the following UDP server:
# (hackfest.redrocket.club,24001)


if __name__ == "__main__":
    curve = X25519(1234)
    data = send_receive('hackfest.redrocket.club', 24001, curve.pk_bytes)

    pub_key = data[0][:32]
    shared_key = curve.exchange(pub_key)
    cipher = XORCipher(shared_key)
    encrypted_msg = data[0][32:]
    decrypted_msg = cipher.decrypt(encrypted_msg)

    print(f"Flag: {decrypted_msg.decode('utf-8')}")
