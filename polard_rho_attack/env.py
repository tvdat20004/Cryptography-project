from sage.all import *
from Crypto.Util.number import getPrime, bytes_to_long
import random
# from secret.flag import flag 
p = getPrime(32) # gen prime

secret = random.randint(0,p-1)

F = GF(p) # create finite field mod p 
a,b = random.randrange(0,p-1), random.randrange(0,p-1)

E = EllipticCurve(F, [a,b])

P = E.gens()[0]
Q = P * secret

print(f'{a = }')
print(f'{b = }')
print(f'{p = }')
print(f'{P = }')
print(f'{Q = }')
# for testing
print(secret)
# a = 830932838
# b = 1398984515
# p = 2625198833
# P = (556319051 : 44577141 : 1)
# Q = (2394329308 : 1701568078 : 1)
# 413204738