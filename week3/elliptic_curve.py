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

    def double_and_add(self, point, scalar):
        tmp = point
        bits = bin(scalar)  # the vector of bits (from LSB to MSB) representing s
        i = len(bits) - 2
        res = point
        while i >= 0:  # traversing from second MSB to LSB
            res = res + res  # double
            if bits[i] == 1:
                res = res + point  # add
            i = i - 1
        if tmp.x == 'infinity':
            res.x = 'infinity'
        if tmp.y == 'infinity':
            res.y = 'infinity'
        return res
