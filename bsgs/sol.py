#!/usr/bin/python3 
from sage.all import *
from tqdm import trange
from hashlib import sha3_512 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
def binary_search(array, value):
    n = len(array)
    left = 0
    right = n-1
    while left <= right:
        mid = floor((left + right) / 2) 
        if array[mid] < value:
            left = mid + 1
        elif array[mid] > value:
            right = mid - 1
        else:
            return mid
    return None

def BSGS_ECDLP(P, Q, E):
    if P == Q:
        return 1
    m = ceil(sqrt(P.order()))
    baby_list = []
    sorted_list = []
    for j in trange(m):
        PP = j*P
        baby_list.append(PP)
        sorted_list.append(PP)
    sorted_list.sort()

    for i in trange(m):
        result = Q - (i*m)*P
        pos = binary_search(sorted_list, result)
        
        if pos != None:
            idx = baby_list.index(result)
            print("A match has been found for: i =",i, ",",
            "j =", idx, "where m =", m)
            x = (i*m + idx)  % P.order()
            print("The solution for ECDLP is ", x)
            return x
    return False

def decrypt(key, ct):
    key = sha3_512(str(key).encode()).digest()[:16]
    iv = ct[:16]
    ct = ct[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    mess = cipher.encrypt(ct)
    return mess

a = 83204266
b = 742414288
p = 815188303
P = (760488765, 17976372)
Q = (413918203, 521801124)
ciphertext = open("cipher.enc", "rb").read()

E = EllipticCurve(GF(p),[a,b])
P = E(*P)
Q = E(*Q)

d = BSGS_ECDLP(P, Q, E)
assert d* P == Q
key = sha3_512(str(d).encode()).digest()[:16]
iv = ciphertext[:16]
ciphertext = ciphertext[16:]
cipher = AES.new(key, AES.MODE_CBC, iv)
with open("recovered.pdf", "wb") as file:
    file.write(unpad(cipher.decrypt(ciphertext),16))
