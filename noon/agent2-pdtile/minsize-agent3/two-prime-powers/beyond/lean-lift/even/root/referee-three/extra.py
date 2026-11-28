"""Referee's tests, second part (own code, exact):
  A   Lemma A on single cells on Z_p: every choice of the merged pair
  C   Lemma C on single cells on Z_pq: the pieces of the proof for EVERY pair of columns; the count with the proof's choice
  C2  cells of exactly q elements full for p and q: never bad at pq
  H   Theorem H: values v_d, P(v_d exists) <= 2^(1-kappa(d)), every value from d = 1 or a fully live d of D + {0}, E|V|
  K   the named decorations and the examples of section 2
usage: extra.py SEED"""
import sys, math, random, itertools
import numpy as np
from fractions import Fraction as Fr
from eng import *

def c(r): return Fr(math.comb(r, r // 2), 2 ** r)
def prodc(sizes):
    t = Fr(1)
    for r in sizes: t *= c(r)
    return t
def share_at(n, ms, d):
    res = sorted(ms); T, w = grid([ms[b] for b in res])
    fl = ~(T @ redmat(n, d)[res]).any(axis=1)
    return Fr(int(w[fl].sum()) if fl.any() else 0, 2 ** sum(ms.values()))
def share_bad(n, ms):
    res = sorted(ms); T, w = grid([ms[b] for b in res]); fl = bad_flags(n, res, T)
    a = np.zeros(T.shape[0], dtype=bool)
    for d in fl: a |= fl[d]
    return Fr(int(w[a].sum()) if a.any() else 0, 2 ** sum(ms.values()))

def testA():
    n = 0; fails = 0; eq = 0
    for p, top in ((3, 9), (5, 5), (7, 3)):
        for rs in itertools.product(range(1, top + 1), repeat=p):
            if sum(rs) > 26: continue
            P = share_at(p, {t: rs[t] for t in range(p)}, p)
            for u, v in itertools.combinations(range(p), 2):
                b = prodc([rs[t] for t in range(p) if t not in (u, v)] + [rs[u] + rs[v]]); n += 1
                if P > b: fails += 1; print("FAIL A", p, rs, u, v, P, b)
                if P == b: eq += 1
    print(f"A: Lemma A, single cells on Z_3 (classes <= 9), Z_5 (<= 5), Z_7 (<= 3): {n} (cell, merged pair) cases, equalities {eq}, failures {fails}")

def col_pieces(col, p):
    O = [s for s in range(p) if col[s] > 0]
    if len(O) == 1: return [col[O[0]]]
    if len(O) <= p - 1: return [col[s] for s in O]
    return [col[s] for s in range(p - 2)] + [col[p - 2] + col[p - 1]]
def lemmaC_pieces(N, p, q, t1, t2):
    """N[s][t] sizes of the subclasses.  pieces of the proof for the pair (t1, t2)."""
    pieces = []
    for t in range(q):
        if t in (t1, t2): continue
        pieces += col_pieces([N[s][t] for s in range(p)], p)
    pieces += col_pieces([N[s][t1] + N[s][t2] for s in range(p)], p)
    return pieces
def choice(N, p, q):
    occ = [[s for s in range(p) if N[s][t] > 0] for t in range(q)]
    multi = [t for t in range(q) if len(occ[t]) >= 2]
    if multi:
        t0 = multi[0]; others = [t for t in range(q) if t != t0]
        return others[0], others[1]
    for t1, t2 in itertools.combinations(range(q), 2):
        if occ[t1][0] != occ[t2][0]: return t1, t2
def testC(rng, count):
    n = 0; pos = 0; fails = 0; eq = 0; least = {}
    for _ in range(count):
        p, q = rng.choice([(3, 5), (3, 7), (5, 7), (3, 11)])
        N = [[0] * q for _ in range(p)]
        kind = rng.randrange(4)
        if kind == 0:                      # one row per column, onto
            rows = [rng.randrange(p) for _ in range(q)]
            pos_ = rng.sample(range(q), p)
            for s in range(p): rows[pos_[s]] = s
            for t in range(q): N[rows[t]][t] = rng.choice([1, 1, 2, 2, 3, 4])
        elif kind == 1:                    # sparse random
            rows = [rng.randrange(p) for _ in range(q)]
            pos_ = rng.sample(range(q), p)
            for s in range(p): rows[pos_[s]] = s
            for t in range(q): N[rows[t]][t] = rng.choice([1, 2])
            for _ in range(rng.randint(1, 3)): N[rng.randrange(p)][rng.randrange(q)] += rng.choice([1, 2])
        elif kind == 2:                    # even sizes
            rows = [rng.randrange(p) for _ in range(q)]
            pos_ = rng.sample(range(q), p)
            for s in range(p): rows[pos_[s]] = s
            for t in range(q): N[rows[t]][t] = 2
            for _ in range(rng.randint(0, 2)): N[rng.randrange(p)][rng.randrange(q)] += 2
        else:                              # a full column or a heavy subclass
            rows = [rng.randrange(p) for _ in range(q)]
            pos_ = rng.sample(range(q), p)
            for s in range(p): rows[pos_[s]] = s
            for t in range(q): N[rows[t]][t] = rng.choice([1, 2])
            t0 = rng.randrange(q)
            if rng.random() < 0.5:
                for s in range(p): N[s][t0] = max(N[s][t0], rng.choice([1, 2]))
            N[rng.randrange(p)][rng.randrange(q)] += rng.randint(2, 9)
        ms = {}
        for s in range(p):
            for t in range(q):
                if N[s][t]:
                    k = next(k for k in range(p * q) if k % p == s and k % q == t); ms[k] = N[s][t]
        g = math.prod(h + 1 for h in ms.values())
        if g > 60000: continue
        P = share_at(p * q, ms, p * q); n += 1; m = sum(ms.values())
        if P > 0: pos += 1
        for t1, t2 in itertools.combinations(range(q), 2):
            pc = lemmaC_pieces(N, p, q, t1, t2)
            assert sum(pc) == m
            if P > prodc(pc): fails += 1; print("FAIL C", p, q, N, t1, t2, P, prodc(pc))
        t1, t2 = choice(N, p, q); pc = lemmaC_pieces(N, p, q, t1, t2)
        least[(p, q)] = min(least.get((p, q), 99), len(pc))
        if len(pc) < q: fails += 1; print("FAIL C count", p, q, N, len(pc))
        if P == prodc(pc): eq += 1
        # the consequence used in Lemma B+: P <= 2^(1-q) c*_(m-2q+2)
        if P > Fr(1, 2 ** (q - 1)) * cstar(m - 2 * q + 2): fails += 1; print("FAIL C consequence", p, q, N, P)
    print(f"C: Lemma C, {n} single cells on Z_pq ((3,5), (3,7), (5,7), (3,11)); with P > 0: {pos}; least number of pieces with the proof's choice {least}; equalities {eq}; failures {fails}")

def testC2():
    for p, q in ((3, 5), (3, 7)):
        n = 0; bad = 0
        for rows in itertools.product(range(p), repeat=q):
            if len(set(rows)) < p: continue
            ms = {next(k for k in range(p * q) if k % p == rows[t] and k % q == t): 1 for t in range(q)}
            n += 1
            if share_at(p * q, ms, p * q) > 0: bad += 1
        print(f"C2: cells of exactly q = {q} elements full for ({p}, {q}): {n} cells, bad at pq: {bad}")

# ---- Theorem H
W1 = Fr(0)
def value_sets(n, D):
    """returns E|V|, K_same, K_other, and the checks of Theorem H's proof.  D: dict residue -> multiplicity; heavy element at 0."""
    res = sorted(D); mult = [D[b] for b in res]; r = sum(mult)
    T, w = grid(mult); N = T.shape[0]
    ex = {}; val = {}
    for d in divisors(n):
        M = T @ redmat(n, d)[res]
        ex[d] = ~M[:, 1:].any(axis=1) if M.shape[1] > 1 else np.ones(N, dtype=bool)
        val[d] = -M[:, 0]
    FL = fully_live(n, sorted(set(res) | {0}))
    fld = {f['d']: f for f in FL}
    fails = []
    for d, f in fld.items():
        P = Fr(int(w[ex[d]].sum()) if ex[d].any() else 0, 2 ** r)
        if P > Fr(1, 2 ** (f['kap'] - 1)): fails.append(('H-prob', n, D, d, P, f['kap']))
    ds = divisors(n)
    E = 0; Ks = 0; Ko = 0
    for i in range(N):
        vs = {}
        for d in ds:
            if ex[d][i]: vs.setdefault(int(val[d][i]), []).append(d)
        for v, dl in vs.items():
            if not (1 in dl or any(d in fld for d in dl)): fails.append(('H-cover', n, D, v, dl))
            if 1 not in dl and min(dl) not in fld: fails.append(('H-least', n, D, v, dl))
        wi = int(w[i]); E += wi * len(vs)
        same = sum(1 for v in vs if (v - r) % 2 == 0); Ks += wi * same; Ko += wi * (len(vs) - same)
    bound = 1 + sum(Fr(1, 2 ** (f['kap'] - 1)) for f in FL)
    EV = Fr(E, 2 ** r)
    if EV > bound: fails.append(('H-sum', n, D, EV, bound))
    return EV, Fr(Ks, 2 ** r), Fr(Ko, 2 ** r), fails, len(FL)

def testH(rng, count):
    NS = [3, 9, 27, 5, 25, 7, 15, 45, 75, 21, 63, 105, 35, 135, 315]
    n_ = 0; fl = 0; allf = []; best = (Fr(0), None); bestKo = (Fr(0), None)
    while n_ < count:
        n = rng.choice(NS); D = {}
        kind = rng.randrange(4)
        if kind == 0:
            for _ in range(rng.randint(1, 9)):
                b = rng.randrange(n); D[b] = D.get(b, 0) + 1
        elif kind == 1:
            for _ in range(rng.randint(1, 5)):
                b = rng.randrange(n); D[b] = D.get(b, 0) + 2
        elif kind == 2:
            for p, a in factor(n).items():
                for i in range(1, a + 1):
                    if rng.random() < 0.8:
                        for t in range(1, p):
                            b = t * (n // p ** i) % n; D[b] = D.get(b, 0) + rng.choice([1, 1, 2])
        else:
            for p in factor(n):
                if rng.random() < 0.8:
                    base = rng.randrange(n)
                    for t in range(p):
                        b = (base + t * (n // p)) % n; D[b] = D.get(b, 0) + 1
        if not D or math.prod(h + 1 for h in D.values()) > 5000: continue
        EV, Ks, Ko, fails, nfl = value_sets(n, D); n_ += 1; fl += nfl; allf += fails
        if EV > best[0]: best = (EV, (n, D))
        if Ko > bestKo[0]: bestKo = (Ko, (n, D))
    print(f"H: Theorem H on {n_} decorations, {fl} fully live d of D + {{0}}: failures {len(allf)}; largest E|V| {best[0]} = {float(best[0]):.4f} at {best[1]}; largest K_other {bestKo[0]} = {float(bestKo[0]):.4f} at {bestKo[1]}")
    for f in allf[:10]: print("   FAIL", f)

def named():
    def lift(pairs, n):  # pairs: list of (dict modulus -> residue), CRT
        out = {}
        for cond, h in pairs:
            b = next(b for b in range(n) if all(b % mo == re for mo, re in cond.items())); out[b] = out.get(b, 0) + h
        return out
    print("K: named decorations (E|V|, K_same, K_other)")
    D = {1: 2, 2: 2}; print("   Z_3 pairs at 1, 2:", *value_sets(3, D)[:3])
    D = {1: 4, 2: 4}; print("   Z_3 four at 1, four at 2:", *value_sets(3, D)[:3])
    D = {1: 2, 2: 2, 3: 2, 6: 2}; print("   Z_9 pairs at 1, 2, 3, 6:", *value_sets(9, D)[:3])
    D = lift([({9: x, 5: 0}, 2) for x in (1, 2, 3, 6)] + [({9: 0, 5: y}, 2) for y in (1, 2, 3, 4)], 45); print("   Z_45 the same with pairs in the nonzero classes mod 5:", *value_sets(45, D)[:3])
    D = {1: 2, 2: 2, 3: 2, 6: 2, 9: 2, 18: 2}; print("   Z_27 chain a = 3:", *value_sets(27, D)[:3])
    D = {1: 2, 2: 2, 3: 2, 6: 2, 9: 2, 18: 2, 27: 2, 54: 2}; print("   Z_81 chain a = 4:", *value_sets(81, D)[:3])
    D = lift([({27: x, 5: 0}, 2) for x in (1, 2, 3, 6, 9, 18)] + [({27: 0, 5: y}, 2) for y in (1, 2, 3, 4)], 135); r = value_sets(135, D); print("   Z_135 chain a = 3 with pairs mod 5:", *r[:3], "failures", len(r[3]))
    D = lift([({3: x, 35: 0}, 1) for x in (1, 2)] + [({5: y, 21: 0}, 1) for y in (1, 2, 3, 4)] + [({7: z, 15: 0}, 1) for z in range(1, 7)], 105); r = value_sets(105, D); print("   Z_105 one element in each nonzero class mod 3, 5, 7:", *r[:3], "failures", len(r[3]))
    print("examples of section 2 and 3:")
    print("   Z_15, two copies of 0..4: P(bad at 15) =", share_at(15, {i: 2 for i in range(5)}, 15), "(text: 1/32)")
    print("   Z_15, {0, 10, 11, 2, 8, 14}: P(bad at 15) =", share_at(15, {0: 1, 10: 1, 11: 1, 2: 1, 8: 1, 14: 1}, 15), "(text: 1/32)")
    ms = {0: 1, 6: 1, 12: 1, 13: 1, 14: 1}
    print("   Z_15, {0, 6, 12, 13, 14}: P(bad) =", share_bad(15, ms), " at 3:", share_at(15, ms, 3), " at 5:", share_at(15, ms, 5), "(text: 1/4, 3/16, 1/16)")
    for m in (11, 21):
        print(f"   ({m - 2}, 1, 1) mod 3: P(bad at 3) = {share_at(3, {0: m - 2, 1: 1, 2: 1}, 3)}, c_(m-2)/2 = {c(m - 2) / 2};  ({m - 4}, 1, 1, 1, 1) mod 5: {share_at(5, {0: m - 4, 1: 1, 2: 1, 3: 1, 4: 1}, 5)}, c_(m-4)/8 = {c(m - 4) / 8}")
    for m in (10, 30, 100):
        P = share_at(3, {0: m - 4, 1: 2, 2: 2}, 3); E1 = Fr(3, 8) * c(m - 4)
        print(f"   ({m - 4}, 2, 2) mod 3: P(bad at 3)/E1 = {float(P / E1):.4f}; formula c_(m-4)(1/4 + (m-4)/(8(m-2))) agrees: {P == c(m - 4) * (Fr(1, 4) + Fr(m - 4, 8 * (m - 2)))}")
    ms = {0: 2, 3: 2, 4: 2, 6: 2, 13: 2, 17: 4, 22: 2}
    print("   Z_27, m = 16 multiset of section 5: share =", share_bad(27, ms), "(text: 7539/32768)")

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]))
    named(); sys.stdout.flush()
    testA(); sys.stdout.flush()
    testC2(); sys.stdout.flush()
    testC(rng, 1500); sys.stdout.flush()
    testH(rng, 1200)
