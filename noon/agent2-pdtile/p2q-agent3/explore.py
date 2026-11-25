"""Minimal patterns of Z_{p^2 q}: which are not 'safe', as functions of (p, q)?  (agent3 / Yonder; uses agent2's exact lp.py)"""
import sys, itertools
sys.path.insert(0, "/srv/commons/agent2-pdtile/flat")
from lp import Setup
def name(d, p, q):
    a = b = 0
    while d % p == 0: d //= p; a += 1
    while d % q == 0: d //= q; b += 1
    return ("p" + (str(a) if a > 1 else "") if a else "") + ("q" + (str(b) if b > 1 else "") if b else "")
def patterns(p, q):
    M = p * p * q; S = Setup(M); O = S.orders
    D = {}
    for r in range(len(O) + 1):
        for Z in itertools.combinations(O, r): D[frozenset(Z)] = S.Dplus(list(Z))[0]
    out = []
    for Z, v in D.items():
        if v.denominator != 1 or not Z: continue
        if all(D[Z - {d}] < v for d in Z):
            k = 1
            for s in (p, p * p, q):
                if s in Z: k *= (p if s != q else q)
            n = int(v)
            closed = all(d in Z for d in (p * q, p * p * q) if all(s in Z for s in ((p if d == p * q else p * p), q)))
            kind = "impossible" if n % k else "safe" if (k == n and closed) else "T2-open" if k == n else "T1-short"
            out.append((kind, sorted(name(d, p, q) for d in Z), n, k))
    return D, out
for p, q in [(2, 3), (2, 5), (2, 7), (2, 11), (2, 13), (3, 2), (3, 5), (3, 7), (3, 11), (5, 2), (5, 3), (5, 7), (7, 2), (7, 3), (7, 5), (5, 11), (3, 13), (11, 2), (11, 3)]:
    D, out = patterns(p, q)
    ns = [(k_, Z, n, k) for k_, Z, n, k in out if k_ != "safe"]
    print(f"p={p} q={q} M={p*p*q}: " + "; ".join(f"{k_} {{{','.join(Z)}}} n={n} k={k}" for k_, Z, n, k in sorted(ns, key=lambda t: (t[2], t[1]))), flush=True)
