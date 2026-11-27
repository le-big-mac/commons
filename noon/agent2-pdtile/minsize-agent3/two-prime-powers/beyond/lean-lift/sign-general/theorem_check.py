# theorem_check.py -- end-to-end test of Theorem 6: for n = m * q^b, sets B in Z_n, look for a signing whose
# fold to Z_m is (product pattern on the digit box of m) * g, g = indicator of the odd cells (or 2 delta);
# check it by exact cyclotomic remainders for every d | n.  Also checked on every pattern tried:
# "fold good in the digit box modulo q"  ==>  "S(zeta) != 0 for all n-th roots of unity"  (the chain of the proof).
# usage: theorem_check.py m q b trials seed        (q = 0: n = m, arithmetic over the integers)
import sys, random, itertools
import numpy as np
from sympy import divisors, factorint
from cyc_struct import reduction
def main():
    m, q, b, trials, seed = [int(a) for a in sys.argv[1:6]]
    tree_only = len(sys.argv) > 6 and sys.argv[6] == 'tree'
    n = m * (q ** b if q else 1)
    rnd = random.Random(seed)
    fm = factorint(m)
    coords = [(p, e) for p in sorted(fm) for e in range(1, fm[p] + 1)]
    sides = [p for p, e in coords]; k = len(sides)
    srt = sorted(sides)
    hyp = srt[0] >= 3 and all(srt[j - 1] >= 2 * j for j in range(2, k + 1))
    digs = lambda c: tuple((c % p ** e) // p ** (e - 1) for p, e in coords)
    cellidx = [digs(c) for c in range(m)]
    box = list(itertools.product(*[range(s) for s in sides]))
    T = np.zeros((m, m), dtype=np.int64)
    for a, j in enumerate(box):
        for c in range(m):
            x = cellidx[c]; v = 1
            for i in range(k):
                if j[i] >= 1: v *= 1 if x[i] == j[i] else (-1 if x[i] == 0 else 0)
            T[a, c] = v
    lev = np.array([sum(1 << i for i in range(k) if j[i] >= 1) for j in box])
    def is_tree(L):
        ps = [coords[i][0] for i in range(k) if L >> i & 1]
        return len(ps) == len(set(ps))
    levels = [L for L in range(1 << k) if (is_tree(L) or not tree_only)]
    ds = divisors(n); Rs = {d: reduction(d) for d in ds}
    primes = sorted(factorint(n))
    def gen():
        kind = rnd.randrange(6); B = set()
        if kind == 0:
            B = set(rnd.sample(range(n), rnd.randrange(1, 40)))
        elif kind == 1:
            for _ in range(rnd.randrange(1, 5)):
                p = rnd.choice(primes); a = rnd.randrange(n); B |= {(a + i * (n // p)) % n for i in range(p)}
        elif kind == 2 and q:   # cosets of the subgroup of order q: all multiplicities of the fold divisible by q
            for _ in range(rnd.randrange(1, 4)):
                a = rnd.randrange(n); B |= {(a + i * (n // q)) % n for i in range(q)}
        elif kind == 3 and n > m:   # two points in one cell
            c = rnd.randrange(n); B = {c, (c + m * rnd.randrange(1, n // m)) % n}
        elif kind == 4:   # one class modulo a divisor, thinned
            d = rnd.choice([t for t in ds if t > 1]); a = rnd.randrange(d)
            cl = [x for x in range(n) if x % d == a]; B = set(rnd.sample(cl, min(len(cl), rnd.randrange(1, 30))))
        else:
            parts = [p ** e for p, e in factorint(n).items()]
            allowed = [set(rnd.sample(range(t), rnd.choice([1, 2, 3, t]) if t >= 3 else 1)) for t in parts]
            B = {x for x in range(n) if all(x % t in A for t, A in zip(parts, allowed))}
            if len(B) > 80: B = set(rnd.sample(sorted(B), 80))
        for _ in range(rnd.randrange(0, 4)):
            if B and rnd.random() < 0.5: B.discard(rnd.choice(sorted(B)))
            else: B.add(rnd.randrange(n))
        return sorted(B)
    nsets = 0; found = 0; tried_total = 0; maxtried = 0; violations = 0; gridgood = 0; notfound = 0
    for _ in range(trials):
        B = gen()
        if not B: continue
        nsets += 1
        cells = {}
        for x in B: cells.setdefault(x % m, []).append(x)
        O = [c for c in cells if len(cells[c]) % 2 == 1]
        g = np.zeros(m, dtype=np.int64)
        if O:
            for c in O: g[c] = 1
        else:
            g[min(cells)] = 2
        ok = False
        for attempt in range(1, 4001):
            sgn = [[rnd.choice((1, -1)) for _ in range(s)] for s in sides]
            sigma = np.array([int(np.prod([sgn[i][cellidx[c][i]] for i in range(k)])) for c in range(m)], dtype=np.int64)
            fold = sigma * g
            I = T @ fold
            if q: I = I % q
            ggood = all(np.any(I[lev == L] != 0) for L in levels)
            # lift to a signing of B with this fold
            S = {}
            for c, pts in cells.items():
                tgt = int(fold[c])
                if tgt == 2 or tgt == -2:
                    sg = [tgt // 2] * 2 + [(-1) ** i for i in range(len(pts) - 2)]
                elif tgt == 0:
                    sg = [(-1) ** i for i in range(len(pts))]
                else:
                    sg = [tgt] + [(-1) ** i for i in range(len(pts) - 1)]
                assert sum(sg) == tgt
                for x, e in zip(pts, sg): S[x] = e
            cyc = True
            for d in ds:
                f = np.zeros(d, dtype=np.int64)
                for x, e in S.items(): f[x % d] += e
                if not np.any(Rs[d] @ f != 0): cyc = False; break
            if ggood:
                gridgood += 1
                if not cyc: violations += 1; print("VIOLATION of the chain: n =", n, "B =", B)
            if ggood and cyc: ok = True; tried_total += attempt; maxtried = max(maxtried, attempt); break
        if ok: found += 1
        else: notfound += 1; print("NO GOOD PRODUCT PATTERN FOUND in 4000 tries: n =", n, "B =", B)
    print("levels used: %d of %d%s" % (len(levels), 1 << k, " (at most one digit of each prime)" if tree_only else ""))
    print("n = %d = %d * %d^%d, digit box of m: sides %s (hypothesis of Theorem P: %s); sets %d; a pattern that is good in the box%s and passes the cyclotomic test found for %d; not found %d; mean tries %.2f, most %d; violations of 'box-good => cyclotomic-good': %d"
          % (n, m, q, b, sides, hyp, nsets, " mod %d" % q if q else "", found, notfound, tried_total / max(found, 1), maxtried, violations))
main()
