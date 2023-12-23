from sage.all import * 
from hashlib import sha1
from Crypto.Cipher import AES 
from Crypto.Util.Padding import unpad
p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece
E = EllipticCurve(GF(p), [a,b])

P = E(3034712809375537908102988750113382444008758539448972750581525810900634243392172703684905257490982543775233630011707375189041302436945106395617312498769005, 4986645098582616415690074082237817624424333339074969364527548107042876175480894132576399611027847402879885574130125050842710052291870268101817275410204850)
Q = E(4291286204233095982097800355773277585779404466780414050012742967338559375384333553359168679684660883036032513788206717842802139715511290878394214809153312,  8349514892065946466466283818540954348260388496316002710682277135347900874015407524217085428004334348077911686735943079124530402068375600288296266068163389)
enc = open("cipher.enc", "rb").read()

# Lifts a point to the p-adic field.
def _lift(E, P, gf):
    x, y = map(ZZ, P.xy())
    for point_ in E.lift_x(x, all=True):
        _, y_ = map(gf, point_.xy())
        if y == y_:
            return point_
def attack(G, P):
    """
    Solves the discrete logarithm problem using Smart's attack.
    More information: Smart N. P., "The discrete logarithm problem on elliptic curves of trace one"
    :param G: the base point
    :param P: the point multiplication result
    :return: l such that l * G == P
    """
    E = G.curve()
    gf = E.base_ring()
    p = gf.order()
    assert E.trace_of_frobenius() == 1, f"Curve should have trace of Frobenius = 1."

    E = EllipticCurve(Qp(p), [int(a) + p * ZZ.random_element(1, p) for a in E.a_invariants()])
    G = p * _lift(E, G, gf)
    P = p * _lift(E, P, gf)
    Gx, Gy = G.xy()
    Px, Py = P.xy()
    return int(gf((Px / Py) / (Gx / Gy)))

secret = attack(P,Q)
assert P*secret == Q 
print(secret)
key = sha1(str(secret).encode()).digest()[:16]
iv, ct = enc[:16], enc[16:]
cipher = AES.new(key, AES.MODE_CBC, iv)
with open("recovered.pdf", "wb") as file:
    file.write(unpad(cipher.decrypt(ct),16))
print("Write to recovered.pdf successfully!!!")