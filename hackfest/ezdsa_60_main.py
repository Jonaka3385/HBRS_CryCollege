import secret
import ecdsa
import os

os.chdir("/opt")

key = open("secp256k1-key.pem").read()
sk = ecdsa.SigningKey.from_pem(key)

pubkey = open("pub.pem").read()
vk = ecdsa.VerifyingKey.from_pem(pubkey)


def sony_rand(n):
    return secret.LONG_CONSTANT


def sign(data):
    if data == b"admin":
        raise ValueError("Not Permitted!")
    signature = sk.sign(data, entropy=sony_rand)
    return signature


def check_signature(msg, sig):
    try:
        vk.verify(sig, msg)
        return True
    except ecdsa.BadSignatureError:
        return False


def sign_user():
    # sign
    data = input("Your username:").encode()
    sig = sign(data).hex()
    print("Your token:" + data.decode() + "," + sig)


def verify_user():
    # verify
    data = input("Submit signed user token:")
    user, signature = data.split(",")
    sig = bytes.fromhex(signature)
    if check_signature(user.encode(), sig):
        if user == "admin":
            print("Holy 1337, here have a flag:")
            print(secret.FLAG)
        else:
            print("Hello ", user)
            print("NO FLG 4 U")
    else:
        print("Invalid Signature Detected. This incident will be reported!")


sign_user()
verify_user()
