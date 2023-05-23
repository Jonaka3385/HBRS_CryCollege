from week1.communication import send_receive
import hashlib
import ecdsa

# Nachricht, die signiert werden soll
message = "Yes, I did east the last cookie!"

# Privaten Schlüssel generieren
private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)

# Öffentlichen Schlüssel aus dem privaten Schlüssel ableiten
public_key = private_key.get_verifying_key()

# Nachricht hashen
message_hash = hashlib.sha256(message.encode()).digest()

# Nachricht mit dem privaten Schlüssel signieren
signature = private_key.sign(message_hash)

# Die signierte Nachricht besteht aus der ursprünglichen Nachricht und der Signatur
signed_message = (message, signature)
signed_message2 = signature + message_hash

# Verifikation der Signatur mit dem öffentlichen Schlüssel
is_valid = public_key.verify(signature, message_hash)

print("Signierte Nachricht:", signed_message)
print("Signatur gültig?", is_valid)


path_priv = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/CryCollege/hackfest/prime256v1-key.pem"
key = open(path_priv).read()
sk = ecdsa.SigningKey.from_pem(key)
path_pub = "/Users/jonas/Documents/JetBrains_Projects/PyCharm/CryCollege/hackfest/mypubkey.pem"
pubkey = open(path_pub).read()
vk = ecdsa.VerifyingKey.from_pem(pubkey)

send_receive('hackfest.redrocket.club', 21555, signed_message2)
