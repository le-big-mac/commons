"""Referee checks, weak-pqr.tex:
 (a) Lemma 'dich': summing mu_T N_T(v) over the coordinates of v outside S gives
     prod_{i not in S u T} p_i * N_{S n T}(v); the mixed difference in the coordinates of S kills
     every term with S not a subset of T.  Checked on random sets in several boxes.
 (b) Remark 1 of the last section: {(0,0),(1,1)} x Z in Z_2 x Z_2 x Z, by brute force.
 (c) for that example: ALL step complements (LP vertices not needed; we just test the stated one and
     test the seven conditions), and what projections it is a transversal of.
"""
import itertools, random
from fractions import Fraction

coords = (0, 1, 2)
subsets = [frozenset(c) for r in range(4) for c in itertools.combinations(coords, r)]

def N(A, T, v):
    return sum(1 for a in A if all(a[i] == v[i] for i in T))

def check_dich(P, trials=30):
    pts = list(itertools.product(*[range(n) for n in P]))
    random.seed(7)
    for _ in range(trials):
        A = [v for v in pts if random.random() < random.choice([0.2, 0.5, 0.8])]
        for S in subsets:
            out = [i for i in coords if i not in S]
            for T in subsets:
                factor = 1
                for i in coords:
                    if i not in S and i not in T:
                        factor *= P[i]
                # summed function of the S-coordinates
                def summed(vS):
                    tot = 0
                    for w in itertools.product(*[range(P[i]) for i in out]):
                        v = [None] * 3
                        for i, t in zip(sorted(S), vS):
                            v[i] = t
                        for i, t in zip(out, w):
                            v[i] = t
                        tot += N(A, T, v)
                    return tot
                for vS in itertools.product(*[range(P[i]) for i in sorted(S)]):
                    v = [0] * 3
                    for i, t in zip(sorted(S), vS):
                        v[i] = t
                    assert summed(vS) == factor * N(A, S & T, v), (P, S, T)
                # mixed difference in the coordinates of S annihilates N_{S n T} when S is not inside T
                if not S <= T and S:
                    Ss = sorted(S)
                    for v0 in itertools.product(*[range(P[i]) for i in Ss]):
                        for v1 in itertools.product(*[range(P[i]) for i in Ss]):
                            md = 0
                            for eps in itertools.product((0, 1), repeat=len(Ss)):
                                v = [0] * 3
                                for i, e, a0, a1 in zip(Ss, eps, v0, v1):
                                    v[i] = a1 if e else a0
                                md += (-1) ** sum(eps) * N(A, S & T, v)
                            assert md == 0
    return True

for P in [(2, 3, 5), (3, 2, 2), (2, 2, 3), (3, 4, 5)]:
    print('Lemma dich term-by-term claim, box', P, ':', check_dich(P, trials=12 if max(P) > 4 else 30))

# ---------- Remark 1
def conditions(A, P):
    pts = list(itertools.product(*[range(n) for n in P]))
    a = {v: (1 if v in A else 0) for v in pts}
    res = {}
    for i in coords:
        cnt = [sum(a[v] for v in pts if v[i] == t) for t in range(P[i])]
        res['F' + 'xyz'[i]] = len(set(cnt)) == 1
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        Nij = {(s, t): sum(a[v] for v in pts if v[i] == s and v[j] == t) for s in range(P[i]) for t in range(P[j])}
        res['F' + 'xyz'[i] + 'xyz'[j]] = all(Nij[s, t] + Nij[s2, t2] == Nij[s, t2] + Nij[s2, t]
                                              for s in range(P[i]) for s2 in range(P[i]) for t in range(P[j]) for t2 in range(P[j]))
    res['Fxyz'] = all(a[i, j, k] + a[i2, j2, k] + a[i2, j, k2] + a[i, j2, k2] == a[i2, j, k] + a[i, j2, k] + a[i, j, k2] + a[i2, j2, k2]
                      for i in range(P[0]) for i2 in range(P[0]) for j in range(P[1]) for j2 in range(P[1])
                      for k in range(P[2]) for k2 in range(P[2]))
    return res

def remark1(nz):
    P = (2, 2, nz)
    pts = list(itertools.product(*[range(n) for n in P]))
    A = {(t, t, k) for t in range(2) for k in range(nz)}
    gamma = {T: 0 for T in subsets}
    gamma[frozenset({0, 1, 2})] = 1
    gamma[frozenset({1, 2})] = 1
    ok = all(sum(gamma[frozenset(i for i in coords if v[i] == a[i])] for a in A) == 1 for v in pts)
    cond = conditions(A, P)
    transversal = {}
    for E in subsets:
        proj = [tuple(a[i] for i in sorted(E)) for a in A]
        full = 1
        for i in E:
            full *= P[i]
        transversal[''.join('xyz'[i] for i in sorted(E))] = (len(set(proj)) == len(proj) == full)
    return ok, cond, len(A), len(pts), [k for k, v in transversal.items() if v]

for nz in (2, 3, 4, 5):
    ok, cond, nA, nall, tr = remark1(nz)
    print('Remark 1, |Z| =', nz, ': stated gamma is a step complement:', ok, '| |A| =', nA, 'of', nall,
          '| conditions holding:', [k for k, v in cond.items() if v], '| bijective projections onto coordinates:', tr)
