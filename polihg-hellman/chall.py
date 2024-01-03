#!/usr/bin/python3 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randint
import hashlib
import os
from sage.all import * 
with open('input1.pdf', "rb") as f:
    flag = f.read()

def encrypt_flag(n: int) -> str:
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(n).encode('ascii'))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(flag, 16))
    # Prepare data to send
    data = ""
    data = str(iv.hex()) + str(ciphertext.hex())
    return data

# Define the curve
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951  
a = 115792089210356248762697446949407573530086143415290314195533631308867097853948  
b = 1235004111951061474045987936620314048836031279781573542995567934901240450608  
E = EllipticCurve(GF(p), [a,b])

# Generator
G = E.gen(0)

# My secret int, different every time!!
n = randint(1, G.order() - 1)

# Send this to Bob!
public = G * n 

# Send this to Bob!
ciphertext = encrypt_flag(n)

try:
    with open("cipher.txt", "w") as file:
        file.write(ciphertext)
    print(f'{G = }')
    print(f"{public = }" )
    print(f"n: {n}")
    print('''cipher was written in "cipher.txt"''')
except:
    print("Error!!!!")
    exit(1)


