"""Multisets on Z_{p^2 q} containing 0, of size <= T: exact zero pattern and size of every one.

Why: for *sets*, four of the seven Case-2 patterns never occur at all (see report), so an enumeration
of sets does not exercise the second bullets of (X) and (Y).  Lemma 3 and the counting in (X), (Y) never
use that the multiplicities are 0/1, so they must hold for multisets too, and there the patterns do occur.

Usage: multi_p2q.py p q T
"""
import sys
import time
import numpy as np
import core

p, q, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
M = p * p * q
ORD = [p, p * p, q, p * q, p * p * q]
NAME = {p: "p", p * p: "p2", q: "q", p * q: "pq", p * p * q: "p2q"}
t0 = time.time()
Rs = [core.res(M, d).astype(np.int8) for d in ORD]
Rcat = np.concatenate(Rs, axis=1)
cuts = np.cumsum([0] + [R.shape[1] for R in Rs])

hist = np.zeros((32, T + 1), dtype=np.int64)
# level 1: the multiset {0}
resv = Rcat[0:1].copy()
last = np.zeros(1, dtype=np.int16)
total = 0
for s in range(1, T + 1):
    pat = np.zeros(len(resv), dtype=np.int64)
    for i in range(5):
        z = ~resv[:, cuts[i]:cuts[i + 1]].any(axis=1)
        pat |= z.astype(np.int64) << i
    hist[:, s] = np.bincount(pat, minlength=32)
    total += len(resv)
    if s == T:
        break
    new_res, new_last = [], []
    for e in range(M):
        m = last <= e
        if m.any():
            new_res.append(resv[m] + Rcat[e])
            new_last.append(np.full(int(m.sum()), e, dtype=np.int16))
    resv = np.concatenate(new_res)
    last = np.concatenate(new_last)
print(f"M={M} p={p} q={q}: {total} multisets containing 0 with size <= {T}  ({time.time()-t0:.1f}s)")

fail = 0


def claim(name, pats, okfun):
    """for all patterns in pats and all sizes with hist>0, okfun(size) must hold"""
    global fail
    n_cases = 0
    bad = []
    sizes = set()
    for pt in pats:
        for s in range(1, T + 1):
            if hist[pt, s]:
                n_cases += int(hist[pt, s])
                sizes.add(s)
                if not okfun(s):
                    bad.append((pt, s, int(hist[pt, s])))
    print(f"  [{'ok' if not bad else 'FAIL'}] {name}: {n_cases} multisets, sizes occurring {sorted(sizes)} {bad if bad else ''}")
    if bad:
        fail += 1


def has(pt, d):
    return bool(pt >> ORD.index(d) & 1)


P_, P2, Q_, PQ, P2Q = p, p * p, q, p * q, p * p * q
allp = range(32)
repA = {P_ * q * a + q * x + p * y for a in range(T) for x in range(1, T + 1) for y in range(1, T + 1)}
repB = {q * x + p * y for x in range(1, T + 1) for y in range(1, T + 1)}
claim("3(a): pq in Z, p,q not in Z => n = pq a + q x + p y, x,y>=1",
      [t for t in allp if has(t, PQ) and not has(t, P_) and not has(t, Q_)], lambda s: s in repA)
claim("(X) 2nd bullet: also p2 in Z => n >= pq+p",
      [t for t in allp if has(t, PQ) and not has(t, P_) and not has(t, Q_) and has(t, P2)], lambda s: s >= p * q + p)
claim("3(b): p2q in Z, p2,q not in Z => n = q x + p y, x,y>=1",
      [t for t in allp if has(t, P2Q) and not has(t, P2) and not has(t, Q_)], lambda s: s in repB)
claim("(Y) 2nd bullet: also p in Z => n > p*min(p,q)",
      [t for t in allp if has(t, P2Q) and not has(t, P2) and not has(t, Q_) and has(t, P_)], lambda s: s > p * min(p, q))
if T >= p * q:
    cnt = sum(int(hist[t, p * q]) for t in allp if has(t, P_) and has(t, P2Q))
    bad = sum(int(hist[t, p * q]) for t in allp if has(t, P_) and has(t, P2Q) and not has(t, PQ))
    print(f"  [{'ok' if bad == 0 else 'FAIL'}] 3(c): n = pq, p, p2q in Z => pq in Z: {cnt} multisets, {bad} violations")
    fail += bad > 0
else:
    print("  (3(c) not covered: T < pq)")
# Fact 4 / Prop 1(iii) for multisets: k | n
bad = 0
for t in allp:
    k = p ** (has(t, P_) + has(t, P2)) * q ** has(t, Q_)
    for s in range(1, T + 1):
        if hist[t, s] and s % k:
            bad += 1
print(f"  [{'ok' if bad == 0 else 'FAIL'}] k(Z) | n for every multiset")
fail += bad > 0
print("  patterns occurring (pattern: sizes):")
for t in allp:
    sz = [s for s in range(1, T + 1) if hist[t, s]]
    if sz:
        print("    {" + ",".join(NAME[d] for d in ORD if has(t, d)) + "}: " + str(sz))
print(f"FAILED CHECKS: {fail}   time {time.time()-t0:.1f}s")
