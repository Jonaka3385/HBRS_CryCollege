"""
Sources:
[1] Guide to Elliptic Curve Cryptography, Hankerson
"""
from week2.finitefield import PrimeField, FieldElement

PRIME = 2**255-19
BASE_X = 9
A = 486662
ORDER = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
FIELD = PrimeField(PRIME)


def jacobian_to_affine(P, modulus):
    if P[2] == 0:
        return None
    else:
        return (P[0] * pow(P[2], -2, modulus)) % modulus, (P[1] * pow(P[2], -3, modulus)) % modulus


class XZPoint:

    def __init__(self, x, z=1):
        self.x = FIELD(x)
        self.z = FIELD(x)

    @property
    def affine(self):
        """
        Converts the projective coordinates into the affine
        x value.
        """
        return self.x * self.z**-1

    def _double(self):
        """
        Double function used to calculate the x value of 2P.
        Since z1 is set to 1, this has to be used in the montgommery latter
        where the x value of the base point is used as x1 in the add step.
        """
        Xp_Zp = ((self.x + self.z)**2) - ((self.x - self.z)**2)
        X_2p = ((self.x + self.z)**2) * ((self.x - self.z)**2)
        Z_2p = Xp_Zp * (((self.x - self.z)**2) + (((A+2)//4) * Xp_Zp))

        return XZPoint(X_2p.elem, Z_2p.elem)

    def _add(self, Q, base):
        """
        Add function used to calculate P + Q.
        This uses the value x1 = x value of base point.
        This works since we use the montgommery ladder and
        r[1] is always r[0] + base point.
        So, we know that r[1] - r[0] = BASE_POINT, so we can just set x1 = BASE_POINT
        :param Q: Point to add to this point
        :param base: This is the base point, in other words r[1] - r[0], P - Q
        :return: Jacobian point P + Q
        """
        basepoint = XZPoint(base)
        X_pq = basepoint.z * ((self.x - self.z)*(Q.x + Q.z) + (self.x + self.z)*(Q.x - Q.z))**2
        Z_pq = basepoint.x * ((self.x - self.z)*(Q.x + Q.z) - (self.x + self.z)*(Q.x - Q.z))**2

        return XZPoint(X_pq.elem, Z_pq.elem)

    def copy(self):
        return XZPoint(self.x, self.z)

    def __rmul__(self, k):
        if type(k) != int:
            raise ValueError("Can't multiply point by type {}".format(type(k)))
        return self.scalarmult(k)

    def scalarmult(self, k):
        """
        This implements the scalarmultiplication kP.
        It uses the montgommery ladder to do so.
        https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Montgomery_ladder
        We go through all bits of the multiplier k,
        if the current bit is 0:
            set r[0] = (2l)P
                r[1] = (2l+1)P
        if the current bit is 1:
            set r[0] = (2l+1)P
                r[1] = (2l+2)P
        where l is the integer represented by the l leftmost bits of k.
        For details see [1] (p. 102).
        """
        if type(k) != int:
            raise ValueError("Can't multiply point by type {}".format(type(k)))

        return self

    def __str__(self):
        return "XZPoint({},{})".format(self.x, self.z)


BASE_POINT = XZPoint(BASE_X)


class X25519:

    def __init__(self, sk):
        self.sk = sk
        self._pub_point = self.sk * BASE_POINT
        self.pk = self._pub_point.affine
        self.pk_bytes = self.pk.elem.to_bytes(32, "little")

    def compute_shared(self, pk):
        """
        Compute the shared point with the provided public key
        :param pk: public key as affine point (X value)
        :return: shared secret as affine point (X value)
        """
        pub_point = XZPoint(pk)
        return (self.sk * pub_point).affine

    def exchange(self, pk):
        """
        Compute the shared secret with provided (encoded) public key
        :param pk: public key as bytes
        :return: shared secret as bytes
        """
        if not isinstance(pk, bytes):
            raise ValueError("Only byte encoded pubkeys are allowed for exchange.")

        pkInt = int.from_bytes(pk, "little")
        pub_point = XZPoint(pkInt)
        secret = self.sk * pub_point
        return secret.affine.to_bytes((secret.affine.elem.bit_length()+7)//8, "little")


def test_X25519():
    G = XZPoint(BASE_X)
    assert(((ORDER+1) * G).affine == BASE_X)

    P = 1337 * G
    Q = 1234 * G

    assert P.affine != Q.affine
    X = 1234 * P
    Y = 1337 * Q
    assert(X.affine == Y.affine)


def test_X25519_compute_shared():
    alice = X25519(8765)
    bob = X25519(1234)

    shared_key_bob = bob.compute_shared(alice.pk)
    shared_key_alice = alice.compute_shared(bob.pk)
    assert(shared_key_bob == shared_key_alice)


def test_X25519_exchange():
    alice = X25519(8765)
    bob = X25519(1234)

    shared_key_bob = bob.exchange(alice.pk_bytes)
    shared_key_alice = alice.exchange(bob.pk_bytes)
    assert(shared_key_bob == shared_key_alice)


def test_Curve25519_format():
    scalar = bytes.fromhex("b823686b94b2074146f7c7ed67344b23d52a39672d2cdb9b44d3e8eb0c023e5d")
    scalar = int.from_bytes(scalar, "little")
    x_val = bytes.fromhex("632ba02eb1e96270f9e7a2a6f1240e4d635ac9497c7957572967fc29899ccf18")
    x_val = int.from_bytes(x_val, "little")

    G = XZPoint(BASE_X)
    P = scalar * G

    assert P.affine == x_val
