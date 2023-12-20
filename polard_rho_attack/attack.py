from sage.all import * 
from Crypto.Util.number import * 
from fractions import Fraction
a = 830932838
b = 1398984515
p = 2625198833
E = EllipticCurve(GF(p), [a,b])
n = E.order()

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

def implement_pseudocode(P, Q, n):
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
    try:
        x = a * pow(b,-1, n)
    except:
        print("Can't not attack!!!")
        quit()
    return x

# 1638559
P = E(556319051, 44577141 )
Q = E(2394329308, 1701568078)
x = implement_pseudocode(P,Q,n)
print(x)
assert int(x)*P == Q
