#!/usr/bin/python3 
from sage.all import*
from pwn import*
from Crypto.Util.number import bytes_to_long
from Crypto.Cipher import ARC4 

params = [(18331317884405018760029080278706955780602851668638697363351485068914830876691, (1745880509282835309044004562786164762877440806481601273526777226569615287830, 40445845084252171039722016236760990401916902494304573869713968464518952741298), 115792089210356248762697446949407573530696555606541666212351744760277115588753, [3, 169, 1849, 89, 1307, 1627, 3359, 30486032827, 63452063959, 117086506177]), (70223234998667467710302703071861433927811174799223906467597126690111708788279, (60382017490386168772210733476817549918577881820758892048222696262556155031493, 41192183457220774339748859920827611795364896924432997254933066083465137889439), 115792089210356248762697446949407573529721313359547594055581209495223727819825, [25, 61, 4391, 51859, 758047747, 3513669457, 13702407211])]
p = 2**256 - 2**224 + 2**192 + 2**96 - 1

r = remote("localhost", 2030)
# r = process(["python3", "server.py"])
r.recvuntil(b"watashi no public key: ")

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

def bytes_to_point(b : bytes):
    return bytes_to_long(b[:32]), bytes_to_long(b[32:])

def point_to_bytes(P):
    return P[0].to_bytes(32, "big") + P[1].to_bytes(32, "big")

def get_dlp(b, x, y):
    E = EllipticCurve(GF(p), [-3, b])
    Q = E(x, y)
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"x: ", str(x).encode())
    r.sendlineafter(b"y: ", str(y).encode())
    ct = bytes.fromhex(r.recvlineS().strip())
    for m in quotes:
        m = m.encode().ljust(64, b"\0")
        xy = ARC4.new(m).decrypt(ct)
        try:
            P = E(*bytes_to_point(xy))
            return P, Q
        except:
            pass

def get_encrypted_flag():
    r.sendlineafter(b'> ', b'2')
    E = EllipticCurve(GF(p), [-3, 41058363725152142129326129780047268409114441015993725554835256314039467401291])
    C1 = E(*bytes_to_point(bytes.fromhex(r.recvlineS().strip())))
    with open("output/cipher.enc", 'rb') as file:
        C2 = file.read()
    return C1, C2 


# E(Fp), p = f1.f2...fn (factor)
# CRT sol: x(p/fn)P = (p/fn)Q
def sol_dlp():
    sec = []
    mod = []
    for b, (x,y), od, subgroups in params:
        P,Q = get_dlp(b,x,y)
        for subgroup in subgroups:
            print(f"solving size {subgroup}")
            tmp = od // subgroup
            k = discrete_log(tmp * P, tmp * Q, ord=ZZ(subgroup), operation="+")
            print(f"k: {k} mod {subgroup}")
            sec.append(k)
            mod.append(subgroup)
    return crt(sec, mod)

d = sol_dlp()
print(f"secret = {d}")

C1, C2 = get_encrypted_flag()

# P = dG, C1 = rG => dC1 = rdG = rP
K = d*C1
key = point_to_bytes(list(map(int, K.xy())))

flag = ARC4.new(key).decrypt(C2)
with open('recover4.pdf', 'wb') as filee:
    filee.write(flag)
r.close()
# https://crypto.stackexchange.com/questions/81851/pohlig-hellman-and-small-subgroup-attacks
# https://risencrypto.github.io/PohligHellman/
