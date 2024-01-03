#!/usr/bin/python3 
from sage.all import * 
from Crypto.Util.number import getPrime
import random

p = 2**256 - 2**224 + 2**192 + 2**96 - 1
F = GF(p)
a = -3
n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
res = []
while 1:
    b = random.randint(0, p-1)
    print(f"tmp_b: {b}")
    E = EllipticCurve(F, [a, b])
    G = E.gen(0)
    od = G.order()
    fac = list(od.factor())
    ar = []
    for f, e in fac:
        if(f**e < 2**40):
            ar.append(f**e)
    if prod(ar) >= 2**128:
        res.append((b, G.xy(), od, ar))
        print(f"final b: {b}")
        print(f"ar: {ar}")
    if len(res) == 2:
        break

print(res)
