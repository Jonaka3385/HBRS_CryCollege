from week1.communication import send_receive
import ecdsa


if __name__ == '__main__':
    msg = 'Yes, I did east the last cookie!'

    gg = ecdsa
    path_priv = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/CryCollege/hackfest/prime256v1-key.pem"
    key = open(path_priv).read()
    sk = gg.SigningKey.from_pem(key)
    path_pub = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/CryCollege/hackfest/mypubkey.pem"
    pubkey = open(path_pub).read()
    vk = gg.VerifyingKey.from_pem(pubkey)

    signed = b'MEUCIDohwrOqfygcgP68/OIcZnmeSMVifM8079JKSEO4u9XxAiEA6eDMWIDae79Ah//6DcfR9jA4sYn7HKiJUa62wZKJ92A='

    send_receive('hackfest.redrocket.club', 21555, signed)
