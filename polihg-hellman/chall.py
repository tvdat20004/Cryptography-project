#!/usr/bin/python3 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randint
import hashlib
import os
from sage.all import * 
flag = b'flag{t3st_fl@g_4_PolligH3llm4n_att4ck}'

def encrypt_flag(n: int):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(n).encode('ascii'))
    key = sha1.digest()[:16]
    # Encrypt flag
    iv = os.urandom(16)
    print(key)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(flag, 16))
    # Prepare data to send
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data

# Define the curve
p = 255323935218170062404631265715751866767
a = 165215949739654367733138784456328004818
b = 67589529911274220250907684697333922377
E = EllipticCurve(GF(p), [a,b])


# Generator
G = E.gen(0)

# My secret int, different every time!!
n = randint(1, G.order() - 1)

# Send this to Bob!
public = G * n 
print(f'{G = }')
print(f"{public = }" )


# Send this to Bob!
ciphertext = encrypt_flag(n)
print(ciphertext)
print(n)
