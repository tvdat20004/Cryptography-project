from sage.all import * 
from Crypto.Util.number import * 
from fractions import Fraction
from pwn import * 
from Crypto.Util.Padding import unpad
# connect to server to get parameter
def getPara():
    p = getPrime(40)
    r.sendlineafter(b'Enter your prime: ', str(p).encode())
    a = int(r.recvlineS().split('=')[1].strip())
    b = int(r.recvlineS().split('=')[1].strip())
    p = int(r.recvlineS().split('=')[1].strip())
    P = eval(r.recvlineS().split('=')[1].strip())
    Q = eval(r.recvlineS().split('=')[1].strip())
    r.recvline()
    return a,b,p,P,Q


def f(Ri, P, Q):
    y = Ri.xy()[1]
    if 0 < y <= p//3:
        return Q + Ri
    elif p//3 < y < 2*p//3:
        return 2*Ri
    else:
        return P+ Ri

def update_ab(Ri, ai, bi):
    y = Ri.xy()[1]
    if 0 < y <= p//3:
        return ai, (bi + 1) % n
    elif p//3 < y < 2*p//3:
        return 2*ai % n, 2*bi % n
    else:
        return (ai +1) % n, bi

def attack(P, Q, n):
    a = []
    b = []
    R = []
    R.append(P)
    a.append(1)
    b.append(0)
    i = 1
    while True:
        R.append(f(R[i-1], P,Q))
        ab = update_ab(R[i-1], a[i-1], b[i-1])
        a.append(ab[0])
        b.append(ab[1])
        if i % 2 == 0 and R[i] == R[i//2]:
            m = i//2
            break
        i += 1
    # print(R)
    fr = Fraction(int(a[2*m] - a[m]), int(b[m] - b[2*m]))
    a,b = int(fr.numerator), int(fr.denominator)
    x = a * pow(b,-1, n)
    return x

while True:
    r = process(["python3", "server.py"])
    a,b,p,P,Q = getPara()
    E = EllipticCurve(GF(p), [a,b])
    n = E.order()
    P = E(*P)
    Q = E(*Q)
    try:
        x = attack(P,Q,n)
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
