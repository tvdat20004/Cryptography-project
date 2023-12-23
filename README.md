# Cryptanalysis on ECC-based Algorithms

Students: 
- Thái Vĩnh Đạt - 22520235
- Đinh Lê Thành Công - 22520167

Lecturer: Nguyễn Ngọc Tự

## Overview
- 	Scenario:
A tech company has integrated ECC-based algorithms for secure communications in their IoT devices. They want to validate the strength and security of their ECC implementation to prevent potential breaches.
- Gaps: 
ECC, while offering good security with shorter key lengths compared to traditional methods, can be vulnerable if not implemented correctly or if weak curves are chosen.
- Motivations:
 To ensure secure communication between IoT devices and to maintain user trust and data integrity.
## Proposed solution
### Solution architecture

![image](https://github.com/tvdat20004/Cryptography-project/assets/117071011/e85fb08a-0539-48a0-88ce-ba2cf1db4c11)

- Key Generation and Collection:
	- Elliptic curve:
	    - An elliptic curve is defined by the equation:  $y^2+xy=x^3+ax+b$
	    - Equation: $y^2+xy=x^3+ax+b$
	    - Weierstrass form: $y^2= x^3+ax+b$ $(4a^3+27b^2  ≠0)$
	    - "Montgomery form": $By^2  = x^3  +Ax^2  +x$
      
![image](https://github.com/tvdat20004/Cryptography-project/assets/117071011/76ef9eed-2a49-4b35-92f0-1fc9b613fd14)

- Finite fields
- Elliptic curves over Finite fields
- Point addition

![image](https://github.com/tvdat20004/Cryptography-project/assets/117071011/d8698b8c-5a04-42eb-aa4c-90acd1c481f2)

- Point scalar multiplication: $nP=P+P+⋯+P$ (n times)
- Elliptic Curve Discrete Logarithm Problem (ECDLP): It is the problem of finding an integer n such that $Q=nP$. By analogy with the discrete logarithm problem for $F_p^*$, we denote this integer n by $n = log_{P}Q$.
- __Key generation of ECC__
Key generation in elliptic curve cryptography (ECC) is a fundamental process that involves generating pairs of cryptographic keys—a private key and a corresponding public key. Here is step-by-step of key generation in ECC: 
    - **Selecting Parameters**: The first step in key generation is to select the parameters for the elliptic curve. These parameters include the equation defining the curve, the base point on the curve, and the order of the base point. The choice of parameters is critical for the security and efficiency of the ECC system.
    - **Generating the Private Key**: The private key in ECC is a randomly selected integer within a specific range. The size of the private key depends on the desired level of security. The private key should be kept secret and not shared with anyone.
    - **Computing the Public Key**: The public key is derived from the private key and the chosen elliptic curve parameters. It is computed by performing scalar multiplication of the base point on the curve with the private key. This process involves adding the base point to itself multiple times according to the binary representation of the private key.
    - **Storing and Sharing Keys**: The private key must be securely stored and protected from unauthorized access. On the other hand, the public key can be freely shared with others. It is common to represent the public key as a point on the elliptic curve or as a compressed or uncompressed binary representation.
    - **Key Validation**: After generating the key pair, it is essential to validate the keys to ensure they meet certain criteria. This may involve checking whether the private key is within the valid range, whether the computed public key lies on the elliptic curve, and whether it has the expected properties.
    - **Key Management**: Proper key management practices should be followed to safeguard the generated key pair. This includes securely storing the private key, using secure key storage mechanisms or hardware security modules. Additionally, key rotation and key revocation mechanisms should be implemented as part of a comprehensive key management strategy.
### Cryptanalysis Tools:
- [Sagemath](https://www.sagemath.org/): SageMath (previously Sage or SAGE, "System for Algebra and Geometry Experimentation") is a computer algebra system (CAS) with features covering many aspects of mathematics, including algebra, combinatorics, graph theory, numerical analysis, number theory, calculus and statistics.
- Python 3.x 
- [Pycryptodome](https://pycryptodome.readthedocs.io/en/latest/index.html#): PyCryptodome is a self-contained Python package of low-level cryptographic primitives.
### Attack models
#### Polard-rho attack
The strategy of the algorithm is to produce a sequence of randomly generated terms (Ri,ai,bi), where Ri is a point on the the curve E and ai,bi lie in Fp,over which the elliptic curve E is defined. Since E(Fp) is a finite group, the sequence eventually becomes periodic and loops back to an earlier term in the sequence.

![image](https://hackmd.io/_uploads/rJkR5YVDa.png)
#### Baby-step giant-step
- The baby-step giant-step is a meet-in-the-middle algorithm for computing the discrete logarithm or order of an element in a finite abelian group by Daniel Shanks. The discrete log problem is of fundamental importance to the area of public key cryptography.Baby-step Giant-step method for discrete logarithm problem can be extended for ECDLP simply

#### Pohlig-Hellman attack:
- The Pohlig-Hellman algorithm was presented by Stephan C. Pohlig and Martin E. Hellman in 1978. In the original paper it is presented as an improved algorithm used to compute discrete logarithms over the cyclic field $G = GF(p)$, and how their findings impact elliptic curve cryptography. Given the ECDLP $Q=l*P$, the Pohlig-Hellman algorithm is a recursive algorithm that reduces the problem by computing discrete logarithms in the prime order subgroups of `<P>`. Each of these smaller subproblems can then be solved using methods, such the Pollard’s rho alogrithm.
#### Smart attack
- Context: When the order of elliptic curve equal to p (`E.order() == p`)
- Smart in “Smart attack” describes a linear time method of computing the ECDLP in curves over a field 𝐹𝑝 such that #𝐸(𝐹𝑝) = 𝑝, or in other words such that the trace of Frobenius is one, 𝑡 = 𝑝 + 1 + #𝐸(𝐹𝑝 ) = 1. 
#### Invalid curve attack
-	An attacker can choose a public key (x_a, y_a) such that it lies on a curve other than the equation y2 = x3 + ax + c (where c differs from the coefficient b of the curve Valid ECC). Since the addition formula in ECC does not use the constant b, this point can still be processed by the device.
-	When the device performs math on this point, it can reveal information about the secret key. This allows the attacker to find the secret key and thus decrypt the data.
### Implementation and testing:
-	Python 3.x 
-	Sagemath
-	Pycryptodome 

#### Deployment
+   Avoid weak curve attacks: Choose a safe curve according to NIST standards (https://safecurves.cr.yp.to/)
+  Avoid invalid curve attacks: check public key (x,y) if it lies on original elliptic curve.
+  Regularly upgrade, update and periodically test security measures for IOT systems.
### Reference
- Hoffstein, Pipher, Silverman, An Introduction to Mathematical Cryptography 2014 (https://sci-hub.hkvisa.net/10.1007/978-1-4939-1711-2)
- Renaud Dubois, Trapping ECC with Invalid Curve Bug Attacks (https://eprint.iacr.org/2017/554.pdf?ref=notamonadtutorial.com)
- Peter Novotney, Weak Curves In Elliptic Curve Cryptography
(https://wstein.org/edu/2010/414/projects/novotney.pdf)
- Junfeng Fan, Xu Guo, Elke De Mulder, Patrick Schaumont, Bart Preneel and Ingrid Verbauwhede, State-of-the-art of secure ECC implementations: a survey on known side-channel attacks and countermeasures (https://sci-hub.hkvisa.net/10.1109/hst.2010.5513110)
- Loren D. Olson, Side-Channel Attacks in ECC: A General Technique for Varying the Parametrization of the Elliptic Curve (https://www.iacr.org/archive/ches2004/31560220/31560220.pdf)
- Mandy Zandra Seet, ELLIPTIC CURVE CRYPTOGRAPHY Improving the Pollard-Rho Algorithm (https://www.maths.unsw.edu.au/sites/default/files/mandyseetthesis.pdf)
- Wienardo, Fajar Yuliawan, Intan Muchtadi-Alamsyah, and Budi Rahardjo, Implementation of Pollard Rho attack on elliptic curve cryptography over binary fields (https://sci-hub.hkvisa.net/10.1063/1.4930641#google_vignette)
