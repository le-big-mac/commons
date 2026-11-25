"""(pattern, size) histogram over ALL subsets of Z_M containing 0, M = p^2 q, chunked (for M = 28).
Then the pattern/size-level claims of Lemma 3 and Section 3, with exact D+.
Usage: enum_big.py p q
"""
import sys
import time
import numpy as np
import core

p, q = int(sys.argv[1]), int(sys.argv[2])
M = p * p * q
ORD = [p, p * p, q, p * q, p * p * q]
NAME = {p: "p", p * p: "p2", q: "q", p * q: "pq", p * p * q: "p2q"}
t0 = time.time()
nlow = (M - 1) // 2 + 1          # low part: elements 1..nlow ; element 0 always present
nhigh = M - 1 - nlow             # high part: elements nlow+1 .. M-1
Rs = [core.res(M, d).astype(np.int16) for d in ORD]


def table(elems):
    n = len(elems)
    idx = np.arange(1 << n, dtype=np.int64)
    bits = np.stack([(idx >> b) & 1 for b in range(n)], axis=1).astype(np.int16)
    sz = bits.sum(axis=1).astype(np.int64)
    out = [bits @ R[elems] for R in Rs]
    return sz, out


sz_lo, res_lo = table(list(range(1, nlow + 1)))
sz_hi, res_hi = table(list(range(nlow + 1, M)))
res_lo = [r + R[0] for r, R in zip(res_lo, Rs)]     # element 0
sz_lo = sz_lo + 1
hist = np.zeros((32, M + 1), dtype=np.int64)
for h in range(1 << nhigh):
    pat = np.zeros(len(sz_lo), dtype=np.int64)
    for i in range(5):
        z = (res_lo[i] == -res_hi[i][h]).all(axis=1)
        pat |= z.astype(np.int64) << i
    hist += np.bincount(pat * (M + 1) + sz_lo + sz_hi[h], minlength=32 * (M + 1)).reshape(32, M + 1)
print(f"M={M} p={p} q={q}: {int(hist.sum())} subsets containing 0  ({time.time()-t0:.1f}s)")
np.save(f"hist_{M}.npy", hist)


def has(pt, d):
    return bool(pt >> ORD.index(d) & 1)


fail = 0


def claim(name, pats, okfun):
    global fail
    n_cases, bad, sizes = 0, [], set()
    for pt in pats:
        for s in range(1, M + 1):
            if hist[pt, s]:
                n_cases += int(hist[pt, s])
                sizes.add(s)
                if not okfun(s):
                    bad.append((pt, s, int(hist[pt, s])))
    print(f"  [{'ok' if not bad else 'FAIL'}] {name}: {n_cases} sets, sizes {sorted(sizes)} {bad if bad else ''}")
    fail += bool(bad)


P_, P2, Q_, PQ, P2Q = ORD
allp = range(32)
repA = {P_ * q * a + q * x + p * y for a in range(M) for x in range(1, M) for y in range(1, M)}
repB = {q * x + p * y for x in range(1, M) for y in range(1, M)}
claim("3(a): pq in Z, p,q not => n = pq a + q x + p y, x,y>=1",
      [t for t in allp if has(t, PQ) and not has(t, P_) and not has(t, Q_)], lambda s: s in repA)
claim("(X) 2nd bullet: also p2 in Z => n >= pq+p",
      [t for t in allp if has(t, PQ) and not has(t, P_) and not has(t, Q_) and has(t, P2)], lambda s: s >= p * q + p)
claim("3(b): p2q in Z, p2,q not => n = q x + p y, x,y>=1",
      [t for t in allp if has(t, P2Q) and not has(t, P2) and not has(t, Q_)], lambda s: s in repB)
claim("(Y) 2nd bullet: also p in Z => n > p*min(p,q)",
      [t for t in allp if has(t, P2Q) and not has(t, P2) and not has(t, Q_) and has(t, P_)], lambda s: s > p * min(p, q))
cnt = sum(int(hist[t, p * q]) for t in allp if has(t, P_) and has(t, P2Q))
bad = sum(int(hist[t, p * q]) for t in allp if has(t, P_) and has(t, P2Q) and not has(t, PQ))
print(f"  [{'ok' if bad == 0 else 'FAIL'}] 3(c): n = pq, p, p2q in Z => pq in Z: {cnt} sets, {bad} violations")
fail += bad > 0


def U_of(P):
    U = set()
    if p in P:
        U |= {p, p * q}
    if p * p in P:
        U |= {p * p, p * p * q}
    if q in P:
        U |= {q, p * q, p * p * q}
    return U


print("Pattern table: zero set | k | D+ exact | #sets | sizes | #pd-tiling")
tot_pd = 0
for pat in allp:
    Z = [d for d in ORD if has(pat, d)]
    cnt = int(hist[pat].sum())
    if not cnt:
        continue
    dp = core.dplus_exact(M, Z)
    P = set(Z) & {p, p * p, q}
    k = p ** len(P & {p, p * p}) * q ** len(P & {q})
    sizes = [s for s in range(M + 1) if hist[pat][s]]
    inU = set(Z) <= U_of(P)
    t2 = (not (p in Z and q in Z) or p * q in Z) and (not (p * p in Z and q in Z) or p * p * q in Z)
    npd = int(hist[pat][int(dp)]) if dp.denominator == 1 else 0
    tot_pd += npd
    badl = []
    if min(sizes) < dp:
        badl.append("SIZE<D+")
    if any(s % k for s in sizes):
        badl.append("k not| n")
    if npd and not (inU and t2 and k == dp):
        badl.append("PD-TILING SET VIOLATING (T1)/(T2)/U(P)")
    fail += len(badl)
    print(f"  {{{','.join(NAME[d] for d in Z)}}} | k={k} | D+={dp} | {cnt} | {sizes} | pd={npd} | inU={inU} T2closed={t2} {' '.join(badl)}")
print(f"pd-tiling sets containing 0: {tot_pd}")
print(f"FAILED CHECKS: {fail}   time {time.time()-t0:.1f}s")
