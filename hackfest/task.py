from week1.cipher import XORCipher
from secret import FLAG

key = b'Hurra!'
cipher = XORCipher(key)
ciphertext = cipher.encrypt(FLAG)
print(ciphertext.hex())
# Output:
# 0b272b092e6a173220372075173b3d253e6d0d21212d26641c2a263d3e760727390f
