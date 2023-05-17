from week3.elliptic_curve import AffinePoint, EllipticCurve
from week2.finitefield import PrimeField


class MontgommeryCurve(EllipticCurve):

    def __init__(self, A, B, field):
        """
        Montgommery Curve, equivalent to twisted edwards basic_curves.
        """
        self.field = field
        self.A = field(A)
        self.B = field(B)
        self.poif = AffinePoint(self, "infinity", "infinity")
        if B * (A ** 2 - 4) == 0:
            raise ValueError("Parameters do not form a montgommery basic_curves")

    def is_on_curve(self, P):
        if P is self.poif:
            return True
        return self.B * P.y ** 2 == (P.x ** 3 + self.A * P.x ** 2 + P.x)

    def add(self, P, Q):
        """
        Point addition of P and Q on this Montgommery Curve
        """
        if not (self.is_on_curve(P) and self.is_on_curve(Q)):
            raise ValueError("Points not on curve.")

        if P == self.poif:
            x3 = Q.x
            y3 = Q.y
        elif Q == self.poif:
            x3 = P.x
            y3 = P.y
        elif P == Q:
            x3 = (3 * P.x ** 2 + 2 * P.x * self.A + 1) ** 2
            x3 *= (4 * P.y ** 2 * self.B) ** -1
            x3 -= 2 * P.x + self.A
            y3 = (3 * P.x ** 2 + 2 * P.x * self.A + 1) * (3 * P.x + self.A) * (2 * P.y * self.B) ** -1
            y3 -= (3 * P.x ** 2 + 2 * P.x * self.A +1) ** 3 * (8 * P.y ** 3 * self.B ** 2) ** -1
            y3 -= P.y
        else:
            x_nom = self.B * (Q.x * P.y - P.x * Q.y) ** 2
            x_den = P.x * Q.x * (Q.x - P.x) ** 2

            y_nom = (2 * P.x + Q.x + self.A) * (Q.y - P.y)
            y_den = Q.x - P.x

            y1_nom = self.B * (Q.y - P.y) ** 3
            y1_den = (Q.x - P.x) ** 3

            x3 = x_nom * x_den ** -1
            y3 = y_nom * y_den ** -1 - y1_nom * y1_den ** -1
            y3 -= P.y

        """
        x1, y1 = P.x, P.y
        x2, y2 = Q.x, Q.y

        u = (y2 - y1) / (x2 - x1)
        v = y1 - u * x1

        x3 = (self.B * u * u - self.A - x1 - x2) / (self.A * self.A - 4)
        y3 = u * x3 + v
        """

        return AffinePoint(self, x3, y3)

    def __str__(self):
        return "{}y^2 = x^3 + {}x^2 + x mod {}".format(self.B, self.A, self.field.mod)


def test_curve25519():
    # Curve25519 is a Montgommery Curve
    # Every montgommery curves is birationally equivalent
    # to a twisted edwards curve.
    # Which means every montgommery curve can be converted
    # to a twisted edwards curve.
    # Which means Curve25519 can be converted to ed25519 and vice versa.
    field = PrimeField(2 ** 255 - 19)
    Curve25519 = MontgommeryCurve(486662, 1, field)

    # Generator
    G = AffinePoint(
        Curve25519,
        # x coordinate
        9,
        # y coordinate, note that in the actual ECDH setting, we don't need the y coordinate
        # which is a feature of montgommery curves
        14781619447589544791020593568409986887264606134616475288964881837755586237401,
        # order
        0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
    )
    N = AffinePoint(
        Curve25519,
        # x coordinate
        0,
        # y coordinate, note that in the actual ECDH setting, we don't need the y coordinate
        # which is a feature of montgommery curves
        1,
        # order
        0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
    )

    assert (Curve25519.is_on_curve(G))
    assert (G.order * G) == Curve25519.poif
    assert ((G.order + 1) * G == G)
    assert ((G.order * G) + G == G)


test_curve25519()
