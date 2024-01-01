#!/usr/bin/python3 
from sage.all import * 
from Crypto.Cipher import AES
import hashlib
from tqdm import trange
p = 255323935218170062404631265715751866767
a = 165215949739654367733138784456328004818
b = 67589529911274220250907684697333922377

E = EllipticCurve(GF(p), [a,b])

P = E.gen(0)

with open('cipher.txt', 'r') as f:
    dataCipher = f.read()
    iv = bytes.fromhex(dataCipher[0:32])
    encrypted_flag = bytes.fromhex(dataCipher[32:])

Q = E(62346538674783463848877272148696432571, 250434738461211621900702825288932669267)
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
    for j in range(m):
        PP = j*P
        baby_list.append(PP)
        sorted_list.append(PP)
    sorted_list.sort()

    for i in range(m):
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

# Q = P[x]
n = P.order()
fac = factor(n)
print(f"factors: {fac}")
d = []
subgroup = []
for prime, exponent in fac:
    P0 = (n // (prime ** exponent)) * P 
    Q0 = (n // (prime ** exponent)) * Q
    x = BSGS_ECDLP(P0, Q0, E)
    d.append(x)
    print(f"x = {x}  mod({prime**exponent})")
    subgroup.append(prime**exponent)

secret = crt(d, subgroup)
print("Calculating in CRT...")
print(f"=> x = {secret} mod ({n})")
assert secret * P == Q
sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv) 
recover = cipher.decrypt(encrypted_flag)

with open('recoveredfile2.pdf', 'wb') as file:
    file.write(recover)
