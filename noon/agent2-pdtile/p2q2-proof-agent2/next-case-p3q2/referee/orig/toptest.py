"""Numerical tests of the reductions at the top level (Lemma E, Proposition F') for weak tiles of Z_M, M = p^a q^b.
P, Q = the subgroups of order p, q;  K = P + Q;  for a step complement f:  x, y, z = its values on P\\0, Q\\0, K\\(P u Q).
Tiles A are drawn at random (random complements of digit sets), step complements f at random from the optimal face.
  E1  if M is not a zero of A:  x + y = 1 + z, and f <= 1 everywhere
  E2  if x = 1:  A meets every coset of P at most once, and its image in Z_M / P is a weak tile with complement (push-forward of f)/p
  E3  if A + P = A:  the image of A in Z_M / P is a weak tile with complement the push-forward of f
  E4  if M is a zero of A:  A meets every coset of K in a union of cosets of P or a union of cosets of Q
  F'  f^ := f with the value on each class (a-1, j) replaced by the value on (a, j).  Its transform is Lambda_lm + (p-1) Lambda_am
      for l < a and 0 for l = a;  and if Lambda_a0 = 0 and [Lambda_am != 0, m >= 1  =>  (l, m) a zero of A for all l < a],
      then f^ is a weak complement of A, equal to 1 on P.
usage: toptest.py p a q b [number of tiles] [seed]          (Noon = agent2, 21 November 2026)"""
import sys, itertools, cmath, random
import numpy as np
sys.path.insert(0, '/home/agent2/p2q2/sands')
from steplp import Step
p, a, q, b = (int(v) for v in sys.argv[1:5]); NT = int(sys.argv[5]) if len(sys.argv) > 5 else 300; random.seed(int(sys.argv[6]) if len(sys.argv) > 6 else 1)
M = p**a * q**b; S = Step(p, a, q, b); pa, qb = p**a, q**b
def val(x, r, cap):
    if x == 0: return cap
    e = 0
    while x % r == 0: x //= r; e += 1
    return e
CL = [(val(x % pa, p, a), val(x % qb, q, b)) for x in range(M)]
P = [(M // p) * t for t in range(p)]; Q = [(M // q) * t for t in range(q)]; K = sorted({(g + h) % M for g in P for h in Q})
def digit(Sset):
    T = [0]
    for s in Sset:
        pr = p if s % p == 0 else q; e = val(s, pr, 99); Mp = M
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
def zeros(A):
    Z = set()
    for d in range(2, M + 1):
        if M % d == 0 and abs(sum(cmath.exp(2j * cmath.pi * x / d) for x in A)) < 1e-7: Z.add(S.order_of(d))
    return Z
def lam(g, o): return sum(float(S.C[(o, c)]) * g[c] for c in S.cls)
def is_complement(A, f, modulus):
    conv = np.array([sum(f[(v - x) % modulus] for x in A) for v in range(modulus)])
    return abs(f[0] - 1) < 1e-7 and f.min() > -1e-9 and np.max(np.abs(conv - 1)) < 1e-7
PP = [p**e for e in range(1, a + 1)] + [q**e for e in range(1, b + 1)]
tot = [float(S.C[((0, 0), c)]) for c in S.cls]; top = (a, b)
cnt = dict(tiles=0, comps=0, E1=0, E1bad=0, y0=0, y0bad=0, E2=0, E2bad=0, E3=0, E3bad=0, E4=0, E4bad=0, allP=0, allQ=0, both=0, mixed=0, Fform=0, Fformbad=0, Fhyp=0, Fbad=0,
           irreducibleN=0, reducibleN=0)
Mq = M // p                                                            # Z_M / P = Z_{M/p}; the quotient map is x -> x mod (M/p)
for _ in range(NT):
    Sset = random.choice([c for r in range(1, len(PP)) for c in itertools.combinations(PP, r)])
    A = None
    for _try in range(20):
        A = random_tile(digit(Sset))
        if A: break
    if not A: continue
    if random.random() < 0.5:                                           # sometimes take the digit set's own side instead
        A = digit(Sset)
    u = random.choice([t for t in range(1, M) if t % p and t % q]); sh = random.randrange(M); A = sorted({(u * x + sh) % M for x in A})
    Z = zeros(A); r0 = S.solve(Z)
    if r0 is None or abs(r0[0] * len(A) - M) > 1e-6: continue            # not a weak tile (should not happen for a tile)
    cnt["tiles"] += 1; v = r0[0]; Aset = set(A)
    if top in Z:                                                        # E4
        cnt["E4"] += 1; kinds = set()
        for c in range(M):
            cell = [(c + k) % M for k in K]
            if min(cell) != c or not any(x in Aset for x in cell): continue
            inA = {x for x in cell if x in Aset}
            unionP = all(((x + g) % M in inA) for x in inA for g in P); unionQ = all(((x + h) % M in inA) for x in inA for h in Q)
            if not (unionP or unionQ): cnt["E4bad"] += 1
            kinds.add("PQ" if unionP and unionQ else ("P" if unionP else "Q"))
        if kinds <= {"P", "PQ"} and kinds <= {"Q", "PQ"}: cnt["both"] += 1
        elif kinds <= {"P", "PQ"}: cnt["allP"] += 1
        elif kinds <= {"Q", "PQ"}: cnt["allQ"] += 1
        else: cnt["mixed"] += 1
    periodicP = all(((x + g) % M) in Aset for x in A for g in P)
    red = False
    for k in range(6):
        obj = [random.random() - (0.5 if k % 2 else 0.0) for _ in S.cls]
        r = S.solve(Z, obj=obj, extra_eq=[(tot, v)])
        if r is None: continue
        g = r[1]; f = np.array([g[c] for c in CL]); cnt["comps"] += 1
        x, y, z = g[(a - 1, b)], g[(a, b - 1)], g[(a - 1, b - 1)]
        if top not in Z:
            cnt["E1"] += 1
            if abs(x + y - 1 - z) > 1e-7 or f.max() > 1 + 1e-7: cnt["E1bad"] += 1
            if y < 1e-9:
                cnt["y0"] += 1
                if abs(x - 1) > 1e-7 or z > 1e-7: cnt["y0bad"] += 1
            if y < 1e-9 or x < 1e-9: red = True
        if abs(x - 1) < 1e-9:                                           # E2
            cnt["E2"] += 1; img = [t % Mq for t in A]
            fq = np.array([sum(f[(t + gg) % M] for gg in P) / p for t in range(Mq)])
            if len(set(img)) != len(A) or not is_complement(img, fq, Mq): cnt["E2bad"] += 1
        if periodicP:                                                   # E3
            cnt["E3"] += 1; img = sorted({t % Mq for t in A})
            fq = np.array([sum(f[(t + gg) % M] for gg in P) for t in range(Mq)])
            if len(img) * p != len(A) or not is_complement(img, fq, Mq): cnt["E3bad"] += 1
        gu = dict(g)                                                    # F'
        for j in range(b + 1): gu[(a - 1, j)] = g[(a, j)]
        cnt["Fform"] += 1
        okform = all(abs(lam(gu, (l, m)) - (lam(g, (l, m)) + (p - 1) * lam(g, (a, m)) if l < a else 0.0)) < 1e-7 for l in range(a + 1) for m in range(b + 1))
        if not okform: cnt["Fformbad"] += 1
        hyp = abs(lam(g, (a, 0))) < 1e-9 and all(abs(lam(g, (a, m))) < 1e-9 or all((l, m) in Z for l in range(a)) for m in range(1, b + 1))
        if hyp:
            cnt["Fhyp"] += 1; fu = np.array([gu[c] for c in CL])
            if not is_complement(A, fu, M) or any(abs(fu[gg] - 1) > 1e-9 for gg in P): cnt["Fbad"] += 1
    if top not in Z: cnt["reducibleN" if red else "irreducibleN"] += 1
print(f"Z_{M} = Z_({p}^{a} {q}^{b}), P of order {p}:  {cnt['tiles']} tiles, {cnt['comps']} step complements")
print(f"  E1  x + y = 1 + z and f <= 1 when M is not a zero:   {cnt['E1']} complements, failures {cnt['E1bad']};   with y = 0: {cnt['y0']}, of which not (x = 1, z = 0): {cnt['y0bad']}")
print(f"  E2  x = 1 => quotient by P is a weak tile:           {cnt['E2']} cases, failures {cnt['E2bad']}")
print(f"  E3  A + P = A => quotient is a weak tile:            {cnt['E3']} cases, failures {cnt['E3bad']}")
print(f"  E4  M a zero => every coset of K is lines:           {cnt['E4']} tiles, cosets failing {cnt['E4bad']};   tiles: only P-lines {cnt['allP']}, only Q-lines {cnt['allQ']}, whole cosets only {cnt['both']}, mixed {cnt['mixed']}")
print(f"  F'  transform of the top fold as stated:             {cnt['Fform']} complements, failures {cnt['Fformbad']};   hypothesis held {cnt['Fhyp']} times, fold not a complement equal to 1 on P: {cnt['Fbad']}")
print(f"  tiles with M not a zero: among the sampled complements, some had x = 0 or y = 0 for {cnt['reducibleN']} tiles, none for {cnt['irreducibleN']}")
