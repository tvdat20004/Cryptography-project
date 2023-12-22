from sage.all import * 
from Crypto.Util.number import getPrime
import random
from factordb.factordb import FactorDB

while True:
    p = getPrime(128)
    # print(p)
    a = random.randint(0,p-1)
    b = random.randint(0,p-1)

    E = EllipticCurve(GF(p), [a,b])
    fac = factor(E.order())
    
    if all(prime < (1<<35) for prime, _ in fac):
        print(p)
        print(a)
        print(b)
        break