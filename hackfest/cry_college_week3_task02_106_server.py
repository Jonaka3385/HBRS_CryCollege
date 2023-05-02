import random

from week1.cipher import XORCipher
from week1.communication import send_receive
from week2.finitefield import PrimeField
from week3.elliptic_curve import AffinePoint
from week3.weierstrass_curve import WeierstrassCurve

# NIST's Curve P-256
NIST_P256_p = 2**256 - 2**224 + 2**192 + 2**96 - 1
NIST_P256_field = PrimeField(NIST_P256_p)


CurveP256 = WeierstrassCurve(
        -3, 
        41058363725152142129326129780047268409114441015993725554835256314039467401291, 
        NIST_P256_field,
        generator=(
            48439561293906451759052585252797914202762949526041747995844080717082404635286,
            36134250956749795798585127919587881956611106672985015071877198253568414405109
        ),
        generator_order=115792089210356248762697446949407573529996955224135760342422259061068512044369
    )

a = random.randint(0,CurveP256.gen.order)
G = CurveP256.gen
A = a * G
transfer = A.x.to_bytes(32,"big")
transfer += A.y.to_bytes(32,"big")
#transfer = NIST_P256_field(A)
data = send_receive("hackfest.redrocket.club",21002, transfer)

server_x = data[0][:32]
server_y = data[0][32:64]
msg = data[0][64:]

server_x_int = int.from_bytes(server_x,"big")
server_y_int = int.from_bytes(server_y,"big")

server_pub = AffinePoint(CurveP256,server_x_int,server_y_int)

key = a * server_pub
key = key.x.elem.to_bytes(32,"big")[:32]

cipher = XORCipher(key)
res = cipher.decrypt(msg)
print("Aufgabe 2: ",res)
