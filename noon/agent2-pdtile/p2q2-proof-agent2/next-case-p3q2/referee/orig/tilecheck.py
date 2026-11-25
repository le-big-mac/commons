"""Soundness check of the classification on real tiles: draw random tiles of Z_{p^a q^b} (random complements of digit
sets, moved by units and translations, and the digit sets themselves), compute their exact zero sets on integer counts, and
look up the category.  A tile is a weak tile, so its pattern must be in L2, a, R, T or U and never in b, N or H.
usage: tilecheck.py p a q b [number of tiles] [seed]            (Noon = agent2, 21 November 2026)"""
import sys, os, itertools, random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact
p, a, q, b = (int(v) for v in sys.argv[1:5]); NT = int(sys.argv[5]) if len(sys.argv) > 5 else 400; random.seed(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
M = p**a * q**b; cnt, hard = exact.classify(p, a, q, b); CAT = dict(exact.CAT)
assert len(CAT) == 2 ** ((a + 1) * (b + 1) - 1), len(CAT)
ords = [(l, m) for l in range(a + 1) for m in range(b + 1) if (l, m) != (0, 0)]; val = lambda o: p**o[0] * q**o[1]
def is_zero(A, o):
    l, m = o; d = val(o); N = [0] * d
    for x in A: N[x % d] += 1
    if l and m: return all(N[c] - N[(c + d // p) % d] - N[(c + d // q) % d] + N[(c + d // p + d // q) % d] == 0 for c in range(d))
    if l: return all(N[c] == N[(c + d // p) % d] for c in range(d))
    return all(N[c] == N[(c + d // q) % d] for c in range(d))
def digit(Sset):
    T = [0]
    for s in Sset:
        pr = p if s % p == 0 else q; e = 0; x = s
        while x % pr == 0: x //= pr; e += 1
        Mp = M
        while Mp % pr == 0: Mp //= pr
        g = pr**(e - 1) * Mp; T = [(t + c * g) % M for t in T for c in range(pr)]
    return sorted(T)
def random_tile(B):
    cov = [False] * M; A = [0]
    for c in B: cov[c] = True
    while True:
        x = next((i for i in range(M) if not cov[i]), None)
        if x is None: return A
        cand = [(x - bb) % M for bb in B if not any(cov[((x - bb) + c) % M] for c in B)]
        if not cand: return None
        t = random.choice(cand)
        for c in B: cov[(t + c) % M] = True
        A.append(t)
PP = [p**e for e in range(1, a + 1)] + [q**e for e in range(1, b + 1)]
seen = Counter(); pats = set(); n = 0
for _ in range(NT):
    Sset = random.choice([c for r in range(1, len(PP)) for c in itertools.combinations(PP, r)]); B = digit(Sset); A = None
    for _try in range(20):
        A = random_tile(B)
        if A: break
    if not A: continue
    for T in (A, B):
        u = random.choice([t for t in range(1, M) if t % p and t % q]); sh = random.randrange(M); T2 = sorted({(u * x + sh) % M for x in T})
        Z = frozenset(o for o in ords if is_zero(T2, o)); n += 1; seen[CAT[Z]] += 1; pats.add(Z)
print(f"Z_{M} (p = {p}, a = {a}, q = {q}, b = {b}): {n} tiles, {len(pats)} distinct zero patterns; categories met: {dict(seen)};  in b, N or H: {seen['b'] + seen['N'] + seen['H']}")
