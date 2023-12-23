#!/usr/bin/python3 
from sage.all import * 
import hashlib
from Crypto.Cipher import AES
p = 255323935218170062404631265715751866767
a = 165215949739654367733138784456328004818
b = 67589529911274220250907684697333922377
E = EllipticCurve(GF(p), [a,b])

P = E.gen(0)

iv = bytes.fromhex('b23d6b13c1f8d5bc9de7b37cb768858e')
encrypted_flag = bytes.fromhex('e4118b4d1059291e081b6f5df4745ccef4abb3ab2a6aad5262fd10133835a3e6e956234897e48a15210a4f54f07639bf')
Q = E(237602427863073591012663205511996249190, 179014942844906640909305117077921301751)

secret = P.discrete_log(Q)
assert P*secret == Q
print(secret)

sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv) 
print(cipher.decrypt(encrypted_flag))