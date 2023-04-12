import pytest


alphabet = "abcdefghijklmnopqrstuvwxyz"
letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def xor(a, b):
    result = bytearray(a_bit ^ b_bit for a_bit, b_bit in zip(a, b))
    return result


class XORCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        if not isinstance(data, bytes):
            raise ValueError("You can only encrypt bytes.")
        
        """
        Encrypt the data using the Vigenère cipher
        """
        plaintext = data
        key = self.key
        ciphertext = bytearray()
        key_index = 0
        for byte in plaintext:
            key_byte = key[key_index % len(key)]
            ciphertext_byte = (byte + key_byte) % 256
            ciphertext.append(ciphertext_byte)
            key_index += 1
        return bytes(ciphertext)

    def decrypt(self, data):
        """
        Decrypt the data using the Vigenère cipher
        """
        ciphertext = data
        key = self.key
        plaintext = bytearray()
        key_index = 0
        for byte in ciphertext:
            # Get the key for this byte
            key_byte = key[key_index % len(key)]
            # Subtract the key from the byte, modulo 256 to get the plaintext byte
            plaintext_byte = (byte - key_byte) % 256
            # Add the plaintext byte to the plaintext
            plaintext.append(plaintext_byte)
            # Increment the key index
            key_index += 1
        return bytes(plaintext)


@pytest.fixture
def xor_cipher():
    key = bytes.fromhex("AB CD EF AFFE AFFE DEADBEEF")
    cipher = XORCipher(key)
    return cipher


def test_xor_enc(xor_cipher):
    res = xor_cipher.encrypt(b"HALLO!")
    assert(res == b'\xe3\x8c\xa3\xe3\xb1\x8e')


def test_xor_dec(xor_cipher):
    res = xor_cipher.decrypt(b'\xe3\x8c\xa3\xe3\xb1\x8e')
    assert(res == b"HALLO!")


def test_xor_equiv(xor_cipher):
    msg = b"dkahsdjkasdhashdahsdha"
    assert(xor_cipher.encrypt(msg) == xor_cipher.decrypt(msg))


def test_shortkey():
    msg = b"a" * 1000
    key = b"1337"

    cipher = XORCipher(key)
    assert cipher.decrypt(cipher.encrypt(msg)) == msg
