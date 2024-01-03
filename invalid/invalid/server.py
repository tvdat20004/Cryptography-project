#!/usr/bin/python3 
from elliptic_curve import Curve, Point
from Crypto.Util.number import bytes_to_long
import os
from random import choice
from secrets import randbelow
from Crypto.Cipher import ARC4

with open('input3.pdf', "rb") as f:
    flag = f.read()
f.close()

# NIST P-256
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
p = 2**256 - 2**224 + 2**192 + 2**96 - 1
E = Curve(p, a, b)
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
Gx = 48439561293906451759052585252797914202762949526041747995844080717082404635286
Gy = 36134250956749795798585127919587881956611106672985015071877198253568414405109
G = Point(E, Gx, Gy)

# server's secret
d = 11079208921356230762697446949407573529996920224135760342421115906106851204435
P = G * d


def point_to_bytes(P):
    return P.x.to_bytes(32, "big") + P.y.to_bytes(32, "big")

def encryptFlag(P, m):
    key = point_to_bytes(P)
    return ARC4.new(key).encrypt(m)


def encryptPoint(P, m):
    key = point_to_bytes(P)
    m = m.ljust(64, b"\0")
    return ARC4.new(m).encrypt(key)


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

print("Konpeko!")
print("watashi no public key: %s" % P)

for _ in range(3):
    try:
        print("nani wo shitai desuka?")
        print("1. Start a Diffie-Hellman key exchange")
        print("2. Get an encrypted flag")
        print("3. Exit")
        option = int(input("> "))
        if option == 1:
            print("Public key wo kudasai!")
            x = int(input("x: "))
            y = int(input("y: "))
            S = Point(E, x, y) * d
            print(encryptPoint(S,choice(quotes).encode()).hex())
        elif option == 2:
            r = randbelow(n)
            C1 = r * G
            C2 = encryptFlag(r * P, flag)
            print(point_to_bytes(C1).hex())
            with open("/output/cipher.enc", "wb") as fi:
                fi.write(C2)
            fi.close()
        elif option == 3:
            print("otsupeko!")
            break
        print()
    except Exception as ex:
        print("kusa peko")
        print(ex)
        break
