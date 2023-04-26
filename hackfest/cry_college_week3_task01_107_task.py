from week1.cipher import XORCipher


curve, GEN = CurveBrainpoolP160r1

key = 1337 * GEN
# Use first 32 bytes of x value as key
x_val = key.x
key = x_val.elem.to_bytes(128, "big")[:32]
cipher = XORCipher(key)
ciphertext = cipher.encrypt(FLAG.encode())
print("Ciphertext:", ciphertext.hex())
# Output:
# Ciphertext: 4352597b4253495f427261696e706f6f6c5f4375727665735f486176655f436f666163746f725f317d
