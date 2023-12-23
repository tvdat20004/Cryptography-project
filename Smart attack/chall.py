from sage.all import * 
import random 
from hashlib import sha1
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
# Curve params
p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece
E = EllipticCurve(GF(p), [a,b])

# prime order may protect us from Pohlig-Hellman, right ? :v
assert is_prime(E.order())
# open file to get plaintext
with open("test.pdf", "rb") as f:
    pt = f.read()

def encrypt(key):
    key = sha1(str(key).encode()).digest()[:16]
    iv = random.randbytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv) 
    return iv + cipher.encrypt(pad(pt, 16))

P = E.gen(0)
n = random.randint(1,P.order() - 1)
print(f'{P = }')
print(f'Public key: {P*n}')
# write ciphertext to cipher.enc
encrypted = encrypt(n)
with open("cipher.enc", "wb") as cipher:
    cipher.write(encrypted)
