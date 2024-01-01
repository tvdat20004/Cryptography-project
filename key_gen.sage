# Step 1: Choose parameter 
p = 0xffffffffffffffffffffffffffffffff000000000000000000000001
K = GF(p)
a = K(0xfffffffffffffffffffffffffffffffefffffffffffffffffffffffe)
b = K(0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4)
E = EllipticCurve(K, (a, b))
G = E(0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21, 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34)
# Step 2: generate private key
import random
priv = random.randint(1, G.order() - 1)
# Step 3: Compute public key
public = priv * G 

# Print public key and all parameters
print(f'{p = }')
print(f'{a = }')
print(f'{b = }')
print(f'{G = }')
print(f'{public = }')
