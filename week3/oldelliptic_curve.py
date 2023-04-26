from week2.finitefield import FieldElement


def inv_mod_p(x, p):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % p == 0:
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, p-2, p)


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

    def double_point(self, point):
        x = int(point.x.elem)
        y = int(point.y.elem)
        A = int(point.curve.a.elem)
        P = int(point.curve.field.mod)
        s = (3 * x * x + A) * pow(2 * y, -1, P)
        xr = (s ** 2 - 2 * x) % P
        yr = (s * (x - xr) - y) % P
        R = AffinePoint(curve=point.curve, x=xr, y=yr)
        return R

    def add_points(self, point1, point2):
        x1 = int(point1.x.elem)
        y1 = int(point1.y.elem)
        x2 = int(point2.x.elem)
        y2 = int(point2.y.elem)
        P = int(point1.curve.field.mod)
        s = ((y2 - y1) * pow(x2 - x1, -1, P)) % P
        xr = (s ** 2 - x1 - x2) % P
        yr = (s * (x1 - xr) - y1) % P
        R = AffinePoint(curve=point1.curve, x=xr, y=yr)
        return R

    def double_and_add(self, point, scalar):
        """
        Do scalar multiplication Q = dP using double and add.
        As here: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Double-and-add
        """
        Q = point
        for bit in bin(scalar)[3:]:
            Q = self.double_point(Q)
            if bit == '1':
                Q = self.add_points(Q, point)
        return Q
