#!/usr/bin/python3 
from sage.all import*
from pwn import*
from Crypto.Util.number import bytes_to_long
from Crypto.Cipher import ARC4 

params = [(1, (111400716329737223151348215591382049163897085784802947255747133622415879105394, 39992761736411400081935771079229874378216016675324636692947348968013201165276), 115792089210356248762697446949407573529578712231346505346655645343696123459399, [71, 823, 1229, 7489, 30203, 1275057701]), (3, (34266504726973447486459180548292643487847724337670171426426712711400387750583, 60138371845611831098044044361051001381561906121645034148367646836258728425794), 57896044605178124381348723474703786764997697290226498635390133450806309414504, [8, 3, 7, 13, 37, 97, 113]), (4, (60994461011195962431939286456844848923647297199347611431191729822246532069553, 62426215642616303247152786006182702061125085742424406842130689349645400096097), 115792089210356248762697446949407573530301458765764575276748425375978192226668, [19, 179, 13003, 1307093479]), (5, (71313685395178834326364531604654869231864467434116851696884560517318161987679, 101821340297271060469660525972572910942517532355430866592133202449535450498864), 115792089210356248762697446949407573530623378430069411602317684396560437888076, [2447]), (6, (98328297292892910073911108288034018739288802240138328982286164487793843645967, 85875970977714582966534270743420950587010634395302449855090814348562252891660), 57896044605178124381348723474703786765170399658733765334296124169948290588710, [5, 4003, 16033, 102001]), (7, (32182267415664188206799024401454157828877342569034947936468251469301214685887, 81714608356807778323795954214457068204235719807356138251488922465561886798710), 57896044605178124381348723474703786764895334266363519119496655336633469253476, [1151, 7103]), (8, (52964478139609867925944358664879267005927312195945554573928053288055034858008, 28457342866386542781597316732785161846891520538541679020399804279100937535370), 115792089210356248762697446949407573530645391408947993867093428060464810786860, [81173])]
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


# E(Fp), p = f1.f2...fn (factor) and p is prime
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
