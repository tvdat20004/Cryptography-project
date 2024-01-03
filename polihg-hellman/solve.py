#!/usr/bin/python3 
from sage.all import * 
from Crypto.Cipher import AES
import hashlib
from tqdm import trange
p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
a = 115792089210356248762697446949407573530086143415290314195533631308867097853948
b = 1235004111951061474045987936620314048836031279781573542995567934901240450608

E = EllipticCurve(GF(p), [a,b])

P = E(58739589111611962715835544993606157139975695246024583862682820878769866632269,86857039837890738158800656283739100419083698574723918755107056633620633897772)
Q = E(53389524449399713241908666754198583135391726383277973572010353430393882869587,96915749683251448875914358893119124077807308307116979366734609648027786948994)
with open('cipher.enc', 'r') as f:
    dataCipher = f.read()
    iv = bytes.fromhex(dataCipher[0:32])
    encrypted_flag = bytes.fromhex(dataCipher[32:])

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
    x = discrete_log(Q0, P0, operation='+')
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

with open('recovered.pdf', 'wb') as file:
    file.write(recover)
