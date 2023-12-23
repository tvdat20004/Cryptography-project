#!/usr/bin/python3 
from sage.all import * 
from Crypto.Util.number import bytes_to_long
from pwn import * 
from Crypto.Cipher import ARC4 
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
p = 2**256 - 2**224 + 2**192 + 2**96 - 1

E = EllipticCurve(GF(p), [a, b])

n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
assert n == E.order()

Gx = 48439561293906451759052585252797914202762949526041747995844080717082404635286
Gy = 36134250956749795798585127919587881956611106672985015071877198253568414405109
G = E(Gx, Gy)

# r = process(["python3", "server.py"])
r = remote("localhost", 2030)
quotes = [
    "Konpeko, konpeko, konpeko! Hololive san-kisei no Usada Pekora-peko! domo, domo!",
    "Bun bun cha! Bun bun cha!",
    "kitira!",
    "usopeko deshou",
    "HA↑HA↑HA↓HA↓HA↓",
    "HA↑HA↑HA↑HA↑",
    "it's me pekora!",
    "ok peko",
]
def get_encrypted_quote(x,y):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'x: ',str(x).encode())
    r.sendlineafter(b'y: ', str(y).encode())
    return bytes.fromhex(r.recvlineS().strip())


def bytes_to_point(b : bytes):
    return bytes_to_long(b[:32]), bytes_to_long(b[32:])

def point_to_bytes(P):
    return P[0].to_bytes(32, "big") + P[1].to_bytes(32, "big")

def decryptRC4(key, m):
    return ARC4.new(key).decrypt(m)

def get_encrypted_flag():
    r.sendlineafter(b'> ', b'2')
    C1 = bytes.fromhex(r.recvlineS().strip())
    with open("output/cipher.enc", 'rb') as file:
        C2 = file.read()
    return C1, C2 

r.recvuntil(b'watashi no public key: ')
P = eval(r.recvuntilS(b'\n').strip())
P = E(*P)

# param from find_good_curve output
param = [(55374142742056320173571819787638777809472808911336014480884317286813436773845, 29445413), (18683340606237798162839665554819902562078278271152292185206948669269254230573, 162263531), (24624047588339450439272204081149894170198019866724433619179522253068021779886, 3476383747), (55902766844192818853349178750639525185968852147752636007309716099481040626885, 10487969), (52747115907965531604384938330824351387999587888780246057838615834696934575358, 2123141), (108232452892497826311561131892338314696129649158423199517090362383919394433991, 2203997), (90481521012725922649701551112858596167711449568080783403246099132591745270507, 539750069), (28011845194834396615899024385750801804824562202897145426874917021984099984567, 10629007), (113987535422036877277675647077877815533200060438538889639190756175419110124578, 3881443), (109509272759190264405760199419896053318904150440188275352947737728386878053685, 507508801), (83236566530711825898226925099842178605458817240088953369114820344421196003979, 8201753543)]

order = []
d = []
for b_, prime in param:
    order.append(prime)
    ec = EllipticCurve(GF(p), [a,b_])
    
    point = ec.gen(0) * (ec.order() // prime)
    assert prime == point.order()
    ct = get_encrypted_quote(*point.xy())
    for quote in quotes:
        ctt = ARC4.new(quote.encode().ljust(64, b'\0')).decrypt(ct)

        try:
            S = ec(*bytes_to_point(ctt))
        except:
            continue
        print(quote)
        d.append(point.discrete_log(S))
        print(d)


d = crt(d,order)
print("Found secret key:",d)

C1, C2 = get_encrypted_flag()
C1 = E(*bytes_to_point(C1)) * int(d)

C1 = point_to_bytes(list(map(int,C1.xy())))

flag = ARC4.new(C1).decrypt(C2)


with open('recover4.pdf', 'wb') as filee:
    filee.write(flag)
r.close()
