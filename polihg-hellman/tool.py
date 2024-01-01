#!/usr/bin/python3 
from sage.all import * 
import hashlib
from Crypto.Cipher import AES
p = 255323935218170062404631265715751866767
a = 165215949739654367733138784456328004818
b = 67589529911274220250907684697333922377
E = EllipticCurve(GF(p), [a,b])
P = E(115093265778331772076313463823377371547, 204608502148379153747855373458343963619)
Q = E(46932642630638585173854260473508367012, 118558123055213343390864876834385319021)

with open('cipher.enc', 'r') as f:
    dataCipher = f.read()
    iv = bytes.fromhex(dataCipher[0:32])
    encrypted_flag = bytes.fromhex(dataCipher[32:])

secret = discrete_log(Q, P, operation="+")
assert P*secret == Q
print(secret)

sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv) 
recover = cipher.decrypt(encrypted_flag)

with open('recovered.pdf', 'wb') as file:
    file.write(recover)
