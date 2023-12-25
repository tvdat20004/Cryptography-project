from sage.all import *
from Crypto.Util.number import *
import random
import secrets
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad
from hashlib import sha3_512 # most secure hash I've heard :v

# import os

def check(prime):
    if not isPrime(prime):
        print("Not a prime!!!")
        return False
    if prime <= (1>>40):
        print("Your prime is so weak!!!")
        return False
    return True

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


while True:
    p = int(input("Enter your prime: "))
    if check(p):
        break
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
with open("input.pdf", 'rb') as file:
    pt = file.read()

# os.system("mkdir /output")

ciphertext = encrypt(secret, pt)
with open("/output/cipher.enc", "wb") as file:
    file.write(ciphertext)
    print("Write ciphertext to cipher.enc successfully!!!")
