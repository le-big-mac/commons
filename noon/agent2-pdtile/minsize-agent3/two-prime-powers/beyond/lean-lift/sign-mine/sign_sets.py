"""The sign lemma for SETS (to which the multiset case reduces): for odd n and a nonempty subset O of Z_n, do all signs +, or one sign
turned, give a signed mask divisible by no Phi_d, d | n?  Exhaustive for small n (subsets containing 0), random subsets for larger n.
Exact arithmetic (integer remainders modulo Phi_d).  Reports any set that needs two or more turned signs, and then the least number.
usage: sign_sets.py"""
import itertools, random, sys
import numpy as np
from sympy import Poly, cyclotomic_poly, symbols, ZZ
X = symbols('X'); random.seed(1)
def remainder_maps(n):
    out = []
    for d in range(1, n + 1):
        if n % d: continue
        phi = Poly(cyclotomic_poly(d, X), X, domain=ZZ); deg = phi.degree(); R = np.zeros((deg, n), dtype=np.int64)
        for i in range(n):
            for j, cj in enumerate(Poly(X**i, X, domain=ZZ).rem(phi).all_coeffs()[::-1]): R[j, i] = int(cj)
        out.append(R)
    return out
def least_flips(pts, n, RM, kmax=4):
    base = np.zeros(n, dtype=np.int64); base[list(pts)] = 1
    rb = [R @ base for R in RM]
    if all(v.any() for v in rb): return 0
    for g in pts:
        if all((v - 2 * R[:, g]).any() for v, R in zip(rb, RM)): return 1
    for k in range(2, kmax + 1):
        for fl in itertools.combinations(pts, k):
            s = base.copy(); s[list(fl)] = -1
            if all((R @ s).any() for R in RM): return k
    return None
def report(n, sets, label):
    RM = remainder_maps(n); hist = {}; worst = []
    for pts in sets:
        k = least_flips(pts, n, RM); hist[k] = hist.get(k, 0) + 1
        if (k is None or k >= 2) and len(worst) < 3: worst.append((pts, k))
    print(f'n = {n}, {label}: least number of turned signs -> number of sets: {dict(sorted(hist.items(), key=lambda t: (t[0] is None, t[0])))}; needing two or more: {worst}', flush=True)
for n in (9, 15, 21):
    def allsets(n=n):
        for mask in range(1 << (n - 1)):
            yield [0] + [i + 1 for i in range(n - 1) if mask >> i & 1]
    report(n, allsets(), 'every subset containing 0')
for n, trials in ((27, 60000), (45, 60000), (63, 40000), (75, 40000), (105, 40000), (135, 20000), (225, 10000), (315, 10000)):
    def rnd(n=n, trials=trials):
        for _ in range(trials):
            if random.random() < 0.5:
                k = random.randint(1, n); yield sorted(random.sample(range(n), k))
            else:                                   # structured: a union of a few cosets of subgroups, plus or minus a few points
                s = set()
                for _ in range(random.randint(1, 4)):
                    c = random.choice([d for d in range(1, n + 1) if n % d == 0]); x0 = random.randrange(n); s |= {(x0 + c * j) % n for j in range(n // c)}
                for _ in range(random.randint(0, 3)): s ^= {random.randrange(n)}
                if s: yield sorted(s)
    report(n, rnd(), f'{trials} random subsets (half uniform, half unions of cosets with a few points changed)')
