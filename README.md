# Cryptanalysis on ECC-based Algorithms

Students: 
- Thái Vĩnh Đạt - 22520235
- Đinh Lê Thành Công - 22520167

Lecturer: Nguyễn Ngọc Tự

## Overview
- Scenario:
A tech company has integrated ECC-based algorithms for secure communications in their IoT devices. They want to validate the strength and security of their ECC implementation to prevent potential breaches.
- Gaps: 
ECC, while offering good security with shorter key lengths compared to traditional methods, can be vulnerable if not implemented correctly or if weak curves are chosen.
- Motivations:
 To ensure secure communication between IoT devices and to maintain user trust and data integrity.
## Proposed solution
### Solution architecture

![image](https://github.com/tvdat20004/Cryptography-project/assets/117071011/969af378-89f4-47fe-8ad9-cbf4561d2498)

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
<img width="531" alt="image" src="https://github.com/tvdat20004/Cryptography-project/assets/117071011/bb46894f-7598-4c43-a7fd-5655fe7633a3">

__The fastest known algorithm to solve ECDLP in E(Fp) takes approximately $\sqrt{p}$ steps__

- __Key generation of ECC__: Key generation in elliptic curve cryptography (ECC) is a fundamental process that involves generating pairs of cryptographic keys—a private key and a corresponding public key. Here is step-by-step of key generation in ECC: 
	- **Selecting Parameters**: The first step in key generation is to select the parameters for the elliptic curve. These parameters include the equation defining the curve, the base point on the curve, and the order of the base point. The choice of parameters is critical for the security and efficiency of the ECC system.
	- **Generating the Private Key**: The private key in ECC is a randomly selected integer within a specific range. The size of the private key depends on the desired level of security. The private key should be kept secret and not shared with anyone.
	- **Computing the Public Key**: The public key is derived from the private key and the chosen elliptic curve parameters. It is computed by performing scalar multiplication of the base point on the curve with the private key. This process involves adding the base point to itself multiple times according to the binary representation of the private key.

### Attack models

#### Baby-step giant-step
- The baby-step giant-step (BSGS) algorithm is a generic algorithm. It works for every finite cyclic group.
- Baby-step giant-step is the algorithm used to calculate DLP and presents several standard variants of it. The giant step small step algorithm uses space-time trade-offs to solve the discrete logarithm problem in arbitrary groups.
- The space complexity of the algorithm is $O(\sqrt{n})$, "while the time complexity of the algorithm is" $O(\sqrt{n})$". This running time is better than the "O(n) running time of the naive brute force calculation.
- While the BSGS method pre-computes an ordered list of powers and compares the value of another ordered sequence of powers against the former list to find a match.

#### Polard-rho attack
- Pollard’s rho is another algorithm for computing discrete logarithms. It has the same asymptotic time complexity $O(\sqrt{n})$ of the BSGS algorithm, but its space complexity is just 𝑂(1). 

- The strategy of the algorithm is to produce a sequence of randomly generated terms (Ri,ai,bi), where Ri is a point on the the curve E and ai,bi lie in Fp,over which the elliptic curve E is defined. Since E(Fp) is a finite group, the sequence eventually becomes periodic and loops back to an earlier term in the sequence.

![image](https://hackmd.io/_uploads/rJkR5YVDa.png)
#### Pohlig-Hellman attack:
- The Pohlig-Hellman algorithm is a general algorithm for solving DLP whose order can be factored into prime powers of smaller primes.
- Context: The elliptic curve has poorly chosen parameters, and the generator's order is smooth (“smooth” means it only has small prime factors)
- Attack scenario: The algorithm reduces the computation of the discrete log in the elliptic group to the computation of the discrete log in subgroups whose order is a small prime, then use CRT to combine these to a logarithm in the full group.
- We can use BSGS or Polard’s Rho algorithm to solve ECDLP on small subgroups.
<img width="594" alt="image" src="https://github.com/tvdat20004/Cryptography-project/assets/117071011/e770e220-a970-4df7-8162-3e68247deb5b">

#### Smart attack
- Context: When the order of elliptic curve equal to p (`E.order() == p`)
- Smart attack describes a linear time method of computing the ECDLP in curves over a field 𝐹𝑝 such that #𝐸(𝐹𝑝) = 𝑝, or in other words such that the trace of Frobenius is one, $𝑡 = 𝑝 + 1 + \#𝐸(𝐹𝑝) = 1$ (Elliptic curves that satisfy that condition are also called "anomalous" curves)

#### Invalid curve attack
- Invalid Curve Attack relies on the fact that given the Weierstrass equation y2 = x3+ax+b of an elliptic curve over a prime field E(Fp) with base point G, the doubling and addition formulas do not depend on the coefficient b.
![image](https://github.com/tvdat20004/Cryptography-project/assets/117071011/ce8154c0-2844-4935-af51-a508ea281ded)
- If a point is not checked to be on the curve, the attacker can send a point which lie on the curve E’(Fp) of equation $𝑦^2=𝑥^3+𝑎𝑥+𝑏_1$, and now the server will calculate point additions, multiplications on that curve, not the original curve.
- Attack scenario: Attacker choose an “invalid” point whose order is weak, so attacker can use BSGS, Polard’s Rho or Pohlig - Hellman to solve ECDLP. Repeatedly send invalid point to get more information about private key, then use CRT to combine them.

### Implementation and testing:
- Python 3.x 
- Sagemath
- Pycryptodome 

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
