from sage.all import * 
from Crypto.Util.number import * 
from fractions import Fraction
from pwn import * 
from Crypto.Util.Padding import unpad
# connect to server to get parameter
def getPara():
    p = getPrime(36)
    r.sendlineafter(b'Enter your prime: ', str(p).encode())
    a = int(r.recvlineS().split('=')[1].strip())
    b = int(r.recvlineS().split('=')[1].strip())
    p = int(r.recvlineS().split('=')[1].strip())
    P = eval(r.recvlineS().split('=')[1].strip())
    Q = eval(r.recvlineS().split('=')[1].strip())
    r.recvline()
    return a,b,p,P,Q

while True:
    # r = process(["python3", "server.py"])
    r = remote('localhost', 6002)
    a,b,p,P,Q = getPara()
    E = EllipticCurve(GF(p), [a,b])
    n = E.order()
    P = E(*P)
    Q = E(*Q)
    try:
        x = discrete_log_rho(Q,P,operation="+")
        assert int(x)*P == Q
        print(x)    
        break
    except:
        print("Polard-rho can't solve this!!!")


from Crypto.Cipher import AES 
from hashlib import sha3_512
ciphertext = open("cipher.enc", 'rb').read()

key = sha3_512(str(x).encode()).digest()[:16]
iv = ciphertext[:16]
ciphertext = ciphertext[16:]
cipher = AES.new(key, AES.MODE_CBC, iv)
with open("recovered.pdf", 'wb') as write:
    write.write(unpad(cipher.decrypt(ciphertext),16))
print("Generate recovered.pdf successfully!!!")
