"""Lemma B+ (ii) / Lemma C, last sentence, beyond (3,5) and (3,7): multisets of exactly q elements, one in each class
modulo the largest prime q, on Z_n with n = p q or n = p1 p2 q, residues modulo the smaller primes random (often onto).
Every check of tests.py is applied; in particular 'need': a fully live d with two or more primes and all ranks 1 must have
no bad signing when m = q.  Also m = q + 1 (one more element), where the bound 2^(-kappa) c*_(m - 2 kappa) = 2^(-q) applies.
usage: c2more.py SEED COUNT"""
import sys, math, random
import tests as TS
from eng import factor
rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
NS = [35, 33, 55, 77, 39, 65, 91, 143, 105, 165, 231, 385, 195, 273, 429]
done = 0; fullboth = 0
while done < count:
    n = rng.choice(NS); ps = sorted(factor(n)); q = ps[-1]
    els = []
    for t in range(q):
        # an element with residue t modulo q and random residues modulo the other primes
        b = next(b for b in rng.sample(range(n), n) if b % q == t)
        els.append(b)
    for p in ps[:-1]:
        if rng.random() < 0.85:                       # make the residues modulo p onto
            pos = rng.sample(range(q), p)
            for s in range(p):
                t = pos[s]; b = els[t]
                els[t] = next(x for x in range(n) if x % q == b % q and x % p == s and all(x % r == b % r for r in ps[:-1] if r != p))
    if rng.random() < 0.4: els.append(rng.randrange(n))    # m = q + 1
    ms = {}
    for b in els: ms[b] = ms.get(b, 0) + 1
    if any(len({b % p for b in els}) == p for p in ps[:-1]): fullboth += 1
    TS.check(n, ms); done += 1
print(f"{done} multisets of q or q + 1 elements on Z_n, n in {NS}; {fullboth} of them full for the largest prime and for another")
TS.report(f"c2more seed {sys.argv[1]} FINAL")
