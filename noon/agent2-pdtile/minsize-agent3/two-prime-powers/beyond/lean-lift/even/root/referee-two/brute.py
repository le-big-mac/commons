# Referee's exact test by ALL signings, from the definition: a signing is bad at d iff Phi_d divides its signed mask.
# For every multiset of m elements of Z_n containing 0 (every multiset is a translate of one of these; translation
# multiplies the mask by a power of X), or for a random sample, every signing with first sign + is listed (the bad
# set is closed under negation), and "bad at d" is decided for every d | n by reducing the mask modulo Phi_d in
# integers (matrix of X^j mod Phi_d; small integers, exact in float32).
# usage: brute.py n mmin mmax [sample N seed]
import sys, itertools, math, time
import numpy as np
from fractions import Fraction as F
from math import comb

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def pdiv(num, den):
    num = num[:]; q = [0] * (len(num) - len(den) + 1)
    for i in range(len(q) - 1, -1, -1):
        t = num[i + len(den) - 1]; q[i] = t
        for j, dj in enumerate(den): num[i + j] -= t * dj
    assert not any(num)
    return q
_cy = {}
def cyclo(d):
    if d not in _cy:
        num = [-1] + [0] * (d - 1) + [1]
        for e in divisors(d):
            if e < d: num = pdiv(num, cyclo(e))
        _cy[d] = num
    return _cy[d]
def redmat(d):
    ph = cyclo(d); k = len(ph) - 1
    cols = []; cur = [1] + [0] * (k - 1)
    for j in range(d):
        cols.append(cur[:])
        t = cur[-1]; cur = [0] + cur[:-1]
        if t:
            for i in range(k): cur[i] -= t * ph[i]
    return np.array(cols, dtype=np.float32).T          # (k, d)
def factor(n):
    f = {}; p = 3
    while n > 1:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 2
    return f

def load(name):
    T = {}
    try:
        for line in open(name):
            w = line.split(); T[int(w[0])] = int(w[1], 16)
    except FileNotFoundError:
        pass
    return T
E3 = load("mytable3-1000.txt"); E5 = load("mytable5.txt"); E7 = load("mytable7.txt")
ETAB = {3: E3, 5: E5, 7: E7}
def a_p(p):
    tau = math.sqrt(p) * 2.0 ** (1 - p); return tau / (1 - 0.8165 * math.sqrt(p) * 2.0 ** (2 - p))

n = int(sys.argv[1]); mmin = int(sys.argv[2]); mmax = int(sys.argv[3])
sample = None
if len(sys.argv) > 4 and sys.argv[4] == "sample":
    sample = int(sys.argv[5]); rng = np.random.default_rng(int(sys.argv[6]))
fac = factor(n); divs = divisors(n); RED = {d: redmat(d) for d in divs}
phimax = max(R.shape[0] for R in RED.values())
print(f"n = {n} = {fac}; divisors {divs}; " + (f"random sample of {sample} multisets per m (seed {sys.argv[6]})" if sample else "every multiset containing 0"))
fails = 0
for m in range(mmin, mmax + 1):
    t0 = time.time(); H = 1 << (m - 1)
    Sg = np.ones((H, m), dtype=np.float32)
    for j in range(1, m): Sg[:, j] = 1 - 2 * ((np.arange(H) >> (j - 1)) & 1)
    batch = max(1, min(200000, int(1.2e8 // (phimax * H * 4))))
    if sample:
        gen = None; total_N = sample
    else:
        gen = itertools.combinations_with_replacement(range(n), m - 1); total_N = comb(n + m - 2, m - 1)
    done = 0
    mx = dict(total=0, pp=0, comp=0, t5=0, t4=0); mxX = {p: 0 for p in fac}; mxP = {p: 0 for p in fac}
    arg = {}; n5 = 0; n4 = 0; neq5 = 0; nX = {p: 0 for p in fac}; nlive2 = 0; eqT = {p: 0 for p in fac}
    while done < total_N:
        nb = min(batch, total_N - done)
        if sample:
            Bs = rng.integers(0, n, size=(nb, m)); Bs[:, 0] = 0
            # half of the sample: residues drawn from a small random set (repeated elements, live groups)
            k = nb // 2
            if k:
                pool = rng.integers(0, n, size=(k, 6)); pool[:, 0] = 0
                pick = rng.integers(0, 6, size=(k, m)); pick[:, 0] = 0
                Bs[:k] = np.take_along_axis(pool, pick, axis=1)
        else:
            chunk = list(itertools.islice(gen, nb)); nb = len(chunk)
            Bs = np.zeros((nb, m), dtype=np.int64)
            if m > 1: Bs[:, 1:] = np.array(chunk, dtype=np.int64).reshape(nb, m - 1)
        done += nb
        res = {}
        for d in divs:
            V = RED[d][:, Bs % d].transpose(1, 0, 2)        # (nb, k, m)
            vals = V @ Sg.T                                  # (nb, k, H)
            res[d] = ~(vals != 0).any(axis=1)
        tot = np.zeros((nb, H), dtype=bool)
        for d in divs: tot |= res[d]
        ppb = {}; Xp = {}; live = {}
        pp = res[1].copy()
        for p, v in fac.items():
            x = np.zeros((nb, H), dtype=bool); lv = np.zeros(nb, dtype=bool)
            for i in range(1, v + 1):
                x |= res[p ** i]
                occ = np.zeros((nb, p ** i), dtype=bool)
                for j in range(m): occ[np.arange(nb), Bs[:, j] % (p ** i)] = True
                lv |= occ.reshape(nb, p, p ** (i - 1)).all(axis=1).any(axis=1)
            ppb[p] = x | res[1]; Xp[p] = x & ~res[1]; pp |= x; live[p] = lv
        ctot = tot.sum(axis=1); cpp = pp.sum(axis=1); ccomp = (tot & ~pp).sum(axis=1)
        for key, arr in (("total", ctot), ("pp", cpp), ("comp", ccomp)):
            i = int(arr.argmax())
            if arr[i] > mx[key]: mx[key] = int(arr[i]); arg[key] = sorted(Bs[i].tolist())
        for p in fac:
            cx = Xp[p].sum(axis=1); i = int(cx.argmax()); nX[p] += int((cx > 0).sum())
            if cx[i] > mxX[p]: mxX[p] = int(cx[i]); arg[("X", p)] = sorted(Bs[i].tolist())
            cp = ppb[p].sum(axis=1); mxP[p] = max(mxP[p], int(cp.max()))
            if p in ETAB and m in ETAB[p]: eqT[p] += int((2 * cx == ETAB[p][m]).sum()) if ETAB[p][m] else 0
        # Corollary 5: at most one prime with a live level
        nl = np.zeros(nb, dtype=int)
        for p in fac: nl += live[p]
        nlive2 += int((nl >= 2).sum())
        sel = nl <= 1; n5 += int(sel.sum())
        want = np.repeat(res[1][:, None, :], 1, axis=1)[:, 0, :].copy()
        for p in fac:
            rows = live[p] & sel
            want[rows] = ppb[p][rows]
        bad5 = (want != tot).any(axis=1) & sel
        neq5 += int(bad5.sum())
        if bad5.any() and "c5" not in arg: arg["c5"] = sorted(Bs[int(np.nonzero(bad5)[0][0])].tolist())
        if sel.any(): mx["t5"] = max(mx["t5"], int(ctot[sel].max()))
        srt = np.sort(Bs, axis=1); ndist = 1 + (np.diff(srt, axis=1) != 0).sum(axis=1)
        s4 = ndist <= 4; n4 += int(s4.sum())
        if s4.any(): mx["t4"] = max(mx["t4"], int(ctot[s4].max()))
        if time.time() - t0 > 500: print(f"   (stopped by the clock after {done} of {total_N} multisets)"); break
    rt = math.sqrt(m)
    sh = lambda cnt: cnt / H
    line = f"m = {m}: {done} multisets; max bad share {F(mx['total'], H)} (sqrt(m) x = {sh(mx['total'])*rt:.4f}) at {arg.get('total')};"
    line += f" bad at 1 or a prime power: {F(mx['pp'], H)} ({sh(mx['pp'])*rt:.4f}); bad only at composite d: {F(mx['comp'], H)} ({sh(mx['comp'])*rt:.4f}) at {arg.get('comp')};"
    ok = True
    for p in fac:
        line += f" X_{p}: {F(mxX[p], H)} ({sh(mxX[p])*rt:.4f}; nonempty in {nX[p]})"
        if p in ETAB and m in ETAB[p]:
            good = 2 * mxX[p] <= ETAB[p][m]; ok &= good
            line += f" table {F(ETAB[p][m], 1 << m)} {'ok' if good else 'EXCEEDED'} (equal {eqT[p]} times)"
        if p == 3:
            lim = 0.9487 if m % 2 == 0 else 0.4331
            good = sh(mxP[3]) * rt <= lim; ok &= good
            line += f"; bad at a power of 3: {F(mxP[3], H)} ({sh(mxP[3])*rt:.4f} against {lim}{'' if good else ' EXCEEDED'})"
            if m in E3:
                cm = comb(m, m // 2) if m % 2 == 0 else 0
                good = 2 * mxP[3] <= cm + E3[m]; ok &= good
                if not good: line += " c+E EXCEEDED"
        else:
            good = sh(mxX[p]) * rt <= a_p(p); ok &= good
            if not good: line += " a_p EXCEEDED"
    lim4 = 1.18 if m % 2 == 0 else 0.67
    good = sh(mx["pp"]) * rt <= lim4; ok &= good
    if not good: line += " COROLLARY 4 EXCEEDED"
    if len(fac) == 1:
        good = mx["total"] ** 2 * m <= H * H; ok &= good
        line += f" [prime power: bad share <= 1/sqrt(m): {good}]"
    # Corollary 5
    lim5 = 0.9487 if m % 2 == 0 else 0.4331
    lim5b = 1.0 if any(p >= 5 for p in fac) else lim5
    good = neq5 == 0 and sh(mx["t5"]) * rt <= lim5b and sh(mx["t4"]) * rt <= lim5; ok &= good
    line += f" | at most one live prime: {n5} multisets, sets differ in {neq5}, max share x sqrt(m) = {sh(mx['t5'])*rt:.4f}; at most four distinct residues: {n4} multisets, max {sh(mx['t4'])*rt:.4f} against {lim5}; two or more live primes: {nlive2}"
    if not good: line += f" COROLLARY 5 FAILS at {arg.get('c5')}"
    line += f" | {'no failure' if ok else 'FAILURE'} ({time.time()-t0:.0f} s)"
    if not ok: fails += 1
    print(line, flush=True)
print("FAILURES:", fails)
