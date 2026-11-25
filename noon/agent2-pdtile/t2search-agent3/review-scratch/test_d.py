"""(d) residues(d, M): R x = 0  <=>  Phi_d | A ?   Three-way comparison: residues / divides / numeric evaluation at a root of unity."""
import random, sys, numpy as np
from common import *
random.seed(11)
def structured(M):
    """a set built to have zeros: a disjoint union of cosets of one or two subgroups, sometimes with a few points flipped"""
    ds = [d for d in divisors(M) if 1 < d < M]
    A = set()
    for _ in range(random.randint(1, 3)):
        r = random.choice(ds); H = [(M // r) * t for t in range(r)]           # subgroup of order r
        for _ in range(random.randint(1, max(1, M // r // 2))):
            c = random.randrange(M); co = {(c + h) % M for h in H}
            if not (co & A): A |= co
    if random.random() < 0.3:
        for _ in range(random.randint(1, 2)): A ^= {random.randrange(M)}
    return sorted(A)
tot = agree = npos = 0
for M in (36, 72, 108, 144, 200, 216, 100, 45):
    R = {d: residues(d, M) for d in divisors(M) if d > 1}
    for d in R: assert R[d].shape == (len(cyclo(d)) - 1, M)
    for trial in range(1500):
        if trial % 2 == 0:
            k = random.randint(1, M); A = sorted(random.sample(range(M), k))
        else: A = structured(M)
        if not A: continue
        x = np.zeros(M, dtype=np.int64); x[A] = 1
        Zn = zeros_numeric(A, M); Zf = zeros_fft(A, M)
        for d in R:
            r = not np.any(R[d] @ x); e = divides(d, A, M); n = d in Zn
            tot += 1; npos += e; agree += (r == e == n == (d in Zf))
            if not (r == e == n): print("DISAGREE", M, d, A, r, e, n)
print(f"(d) residues vs divides vs numeric evaluation vs FFT: {tot} (set, d) pairs, {agree} agree; {npos} of them are zeros")
