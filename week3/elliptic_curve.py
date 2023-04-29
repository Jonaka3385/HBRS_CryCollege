from week2.finitefield import FieldElement


class AffinePoint:

    def __init__(self, curve, x, y, order=None):
        self.curve = curve
        if isinstance(x, int) and isinstance(y, int):
            self.x = curve.field(x)
            self.y = curve.field(y)
        else:  # for POIF and field elements
            self.x = x
            self.y = y
        self.order = order

    def __add__(self, other):
        return self.curve.add(self, other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __rmul__(self, scalar):
        return self.curve.mul(self, scalar)

    def __str__(self):
        return "Point({},{}) on {}".format(self.x, self.y, self.curve)

    def copy(self):
        return AffinePoint(self.curve, self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, AffinePoint):
            raise ValueError("Can't compare Point to {}".format(type(other)))
        if hasattr(self.curve, "poif") and self is self.curve.poif:
            if other is self.curve.poif:
                return True
            return False
        return self.curve == other.curve and self.x == other.x and self.y == other.y


class EllipticCurve:

    def __init__(self):
        self.identity_element = None

    def invert(self, point):
        """
        Invert a point.
        """
        return AffinePoint(self, point.x, (-1 * point.y))

    def mul(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        """
        if isinstance(scalar, FieldElement):
            scalar = scalar.elem
        return self.double_and_add(point, scalar)

    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P

        # werte
        if isinstance(P.x, int) or isinstance(P.x, float):
            px = P.x
        else:  # for POIF and field elements
            px = P.x.elem
        if isinstance(P.y, int) or isinstance(P.y, float):
            py = P.y
        else:  # for POIF and field elements
            py = P.y.elem
        if isinstance(Q.x, int) or isinstance(Q.x, float):
            qx = Q.x
        else:  # for POIF and field elements
            qx = Q.x.elem
        if isinstance(Q.y, int) or isinstance(Q.y, float):
            qy = Q.y
        else:  # for POIF and field elements
            qy = Q.y.elem

        p = int(P.curve.field.mod)
        if px == qx and py != qy:
            return None
        if P == Q:
            return self.double(P)
        m = (qy - py) * pow(qx - px, -1, p)
        x = (m * m - px - qx) % p
        y = (m * (px - x) - py) % p
        R = AffinePoint(curve=P.curve, x=x, y=y)
        return R

    def double(self, P):
        if P is None:
            return None

        # werte
        if isinstance(P.x, int) or isinstance(P.x, float):
            px = P.x
        else:  # for POIF and field elements
            px = P.x.elem
        if isinstance(P.y, int) or isinstance(P.y, float):
            py = P.y
        else:  # for POIF and field elements
            py = P.y.elem

        a = int(P.curve.a.elem)
        p = int(P.curve.field.mod)
        m = (3 * px * px + a) * pow(2 * P[1], -1, p)
        x = (m * m - 2 * px) % p
        y = (m * (px - x) - py) % p
        R = AffinePoint(curve=P.curve, x=x, y=y)
        return R

    def double_and_add(self, P, scalar):
        Q = AffinePoint(curve=P.curve, x=0, y=0)
        while scalar > 0:
            if scalar & 1:
                Q = self.add(Q, P)
            P = self.double(P)
            scalar >>= 1
        return Q
