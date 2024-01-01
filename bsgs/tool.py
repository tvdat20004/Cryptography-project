from sage.all import * 
from Crypto.Cipher import AES 
from Crypto.Util.Padding import unpad
from hashlib import sha3_512

a = 676104023
b = 752683016
p = 855369017
P = (180536981, 236442799)
Q = (644641297, 320792528)
ciphertext = open("cipher.enc", "rb").read()

E = EllipticCurve(GF(p),[a,b])
P = E(*P)
Q = E(*Q)

d = discrete_log(Q,P, operation="+")
print(d)
assert d* P == Q
key = sha3_512(str(d).encode()).digest()[:16]
iv = ciphertext[:16]
ciphertext = ciphertext[16:]
cipher = AES.new(key, AES.MODE_CBC, iv)
with open("recovered.pdf", "wb") as file:
    file.write(unpad(cipher.decrypt(ciphertext),16))
print("Successfully generate recovered.pdf!!!")
