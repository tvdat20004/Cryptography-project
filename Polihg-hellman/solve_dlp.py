from sage.all import * 
import hashlib
from Crypto.Cipher import AES
p = 255323935218170062404631265715751866767
a = 165215949739654367733138784456328004818
b = 67589529911274220250907684697333922377
E = EllipticCurve(GF(p), [a,b])

P = E.gen(0)

iv = bytes.fromhex('e74fd008ec95f4e282dd7c9f01138f10')
encrypted_flag = bytes.fromhex('731d7dbccf6290378d5cd84c774a016fb6feb99b811055d9b1e0abc741496b53')
Q = E(27220587029019095613966886875345166790, 226629191509625454105263154801554340291)

secret = P.discrete_log(Q)
assert P*secret == Q
print(secret)

sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, iv) 
print(cipher.decrypt(encrypted_flag))