from week3.weierstrass_curve import WeierstrassCurve
from week2.finitefield import PrimeField


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

size = 160
p_field = 0xe95e4a5f737059dc60dfc7ad95b3d8139515620f
a = 0x340e7be2a280eb74e2be61bada745d97e8f7c300
b = 0x1e589a8595423412134faa2dbdec95c8d8675e58
G_generator = (0xbed5af16ea3f6a4f62938c4631eb5af7bdbcdbc3, 0x1667cb477a1a8ec338f94741669c976316da6321)
n_order = 0xe95e4a5f737059dc60df5991d45029409e60fc09
h_cofactor = 0x1
# mögliche andere Reihenfolge: size/field/gen/order/cofactor/a/b
field = PrimeField(p_field)

CurveBrainpoolP160r1 = WeierstrassCurve(
    a=a,
    b=b,
    field=field,
    generator=G_generator,
    generator_order=n_order
)
