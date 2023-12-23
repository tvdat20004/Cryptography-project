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

iv = bytes.fromhex('b23d6b13c1f8d5bc9de7b37cb768858e')
encrypted_flag = bytes.fromhex('e4118b4d1059291e081b6f5df4745ccef4abb3ab2a6aad5262fd10133835a3e6e956234897e48a15210a4f54f07639bf')
Q = E(237602427863073591012663205511996249190, 179014942844906640909305117077921301751)
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
n = P.order()
fac = factor(n)
print(fac)
d = []
subgroup = []
for prime, exponent in fac:
    P0 = (n // (prime ** exponent)) * P 
    Q0 = (n // (prime ** exponent)) * Q
    d.append(BSGS_ECDLP(P0, Q0, E))
    subgroup.append(prime**exponent)

secret = crt(d, subgroup)
print(secret)
assert secret * P == Q
sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv) 
print(cipher.decrypt(encrypted_flag))