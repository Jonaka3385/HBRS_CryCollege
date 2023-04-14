from week1.cipher import XORCipher

key = b'Hurra!'
ciphertext = '0b272b092e6a173220372075173b3d253e6d0d21212d26641c2a263d3e760727390f'
cipher = XORCipher(key)
# klartext = cipher.encrypt(key)
# print(klartext)
# print(klartext.hex())
# print(klartext.decode())
# print(klartext.hex().encode())
# print(klartext.decode().encode())
print(cipher.decrypt(bytes.fromhex(ciphertext)))
# Output:
# 0b272b092e6a173220372075173b3d253e6d0d21212d26641c2a263d3e760727390f
