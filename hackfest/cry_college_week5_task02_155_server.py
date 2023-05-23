from week1.communication import send_receive
import ecdsa


if __name__ == '__main__':
    msg = 'Yes, I did east the last cookie!'

    path_priv = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/CryCollege/hackfest/prime256v1-key.pem"
    key = open(path_priv).read()
    sk = ecdsa.SigningKey.from_pem(key)
    path_pub = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/CryCollege/hackfest/mypubkey.pem"
    pubkey = open(path_pub).read()
    vk = ecdsa.VerifyingKey.from_pem(pubkey)

    send_receive('hackfest.redrocket.club', 21555, '')
