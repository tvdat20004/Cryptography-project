#!/usr/bin/python3 
from sage.all import * 
import hashlib
from Crypto.Cipher import AES
p = 255323935218170062404631265715751866767
a = 165215949739654367733138784456328004818
b = 67589529911274220250907684697333922377
E = EllipticCurve(GF(p), [a,b])

P = E.gen(0)

with open('cipher.txt', 'r') as f:
    dataCipher = f.read()
    iv = bytes.fromhex(dataCipher[0:32])
    encrypted_flag = bytes.fromhex(dataCipher[32:])

Q = E(41324044221887482254380150457319906053, 65969667437294267823394803695224442309)

secret = P.discrete_log(Q)
assert P*secret == Q
print(secret)

sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv) 
recover = cipher.decrypt(encrypted_flag)

with open('recoveredfile.pdf', 'wb') as file:
    file.write(recover)