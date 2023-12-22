from sage.all import *
from Crypto.Util.number import *
import random
import secrets
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad
from hashlib import sha3_512 # most secure hash I've heard :v


flag = b'flag{fake_fl4g_for_tssting_123123123}'
def encrypt(key, mess):
    key = sha3_512(str(key).encode()).digest()[:16]
    iv = secrets.token_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(mess, AES.block_size))
    return iv + ct

def genPara(p):
    while True:
        a,b = random.randrange(0,p-1), random.randrange(0,p-1)
        if (4*a**3 + 27 * b**2) % p != 0: # make sure it's not a singular curve
            return a,b


p = getPrime(30)
secret = random.randint(0,p-1)

F = GF(p)
a,b = genPara(p)
E = EllipticCurve(F, [a,b])
P = E.gens()[0] 
Q = P * secret

print(f'{a = }')
print(f'{b = }')
print(f'{p = }')
print('P =', P.xy())
print('Q =', Q.xy())

ciphertext = encrypt(secret, flag).hex()
print(f'{ciphertext = }')