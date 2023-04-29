from week1.cipher import XORCipher
from week3.curves import CurveBrainpoolP160r1

ciphertext = b'4352597b4253495f427261696e706f6f6c5f4375727665735f486176655f436f666163746f725f317d'
print(ciphertext)
print(ciphertext.decode('utf-8'))

GEN = CurveBrainpoolP160r1.gen
key = 1337 * GEN
# Use first 32 bytes of x value as key
x_val = int(key.x)
key = x_val.to_bytes(32, "big")
cipher = XORCipher(key)

flag = cipher.decrypt(ciphertext)
print(flag)
print(flag.hex())
print(flag.decode('ISO-8859-1'))
print(flag.decode('latin-1'))
print(flag.decode('utf-8'))
