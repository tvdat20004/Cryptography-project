from sage.all import * 
import random 
a = -3
b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
p = 2**256 - 2**224 + 2**192 + 2**96 - 1

E = EllipticCurve(GF(p), [a, b])

n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
assert n == E.order()

Gx = 48439561293906451759052585252797914202762949526041747995844080717082404635286
Gy = 36134250956749795798585127919587881956611106672985015071877198253568414405109
G = E(Gx, Gy)

def gen_good_curve():
    # generate curve with small order
    order = 1
    good_curve = []
    while order < n:
        b_ = random.randint(0,n-1)
        E_ = EllipticCurve(GF(p), [a,b_])
        new_order = E_.order()
        for (prime, exponent) in factor(new_order):
            if (1<<20) < prime < (1<<40):
                print(prime)
                good_curve.append((b_, prime))
                order *= prime
                break
    return good_curve
param = gen_good_curve()
print(param)