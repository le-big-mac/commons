"""Second look: checks behind the referee's answers on the changed text and on the referee's own first report.
(1) Lemma E, case (a): the translates of {0,0,1,2,4,5,7,8} on Z_9; how many multisets in all (not only those containing 0).
(2) Lemma B (i) with largest prime 5: a deeper tree attains it at m = 13 (e = 25); e = 5 itself (one cell, integer
    slices) for 6 <= m <= MTOP by the formula P = sum over v of prod P_r(v).
(3) the two K_same values of the hill-climbing in section 5 (decorations from kclimb-27.out, kclimb-45.out).
(4) Theorem H's checks on every named decoration, with the number of failed checks printed.
(5) counts: the exhaustive subtotal and the structured runs, file by file.
(6) the number 0.675 of the optional remark.
usage: second.py MTOP"""
import sys, math, re, glob, itertools
from fractions import Fraction as Fr
from eng import *
from extra import share_at, value_sets
import psi as PSI

MTOP = int(sys.argv[1])
def c(r): return Fr(math.comb(r, r // 2), 2 ** r)

print("(1) Lemma E, case (a), on Z_9")
found = [{0: 2, 1: 1, 2: 1, 4: 1, 5: 1, 7: 1, 8: 1}, {0: 1, 1: 2, 2: 1, 3: 1, 5: 1, 6: 1, 8: 1}, {0: 1, 1: 1, 2: 2, 3: 1, 4: 1, 6: 1, 7: 1},
         {0: 1, 1: 1, 3: 1, 4: 1, 5: 2, 6: 1, 7: 1}, {0: 1, 1: 1, 3: 1, 4: 1, 6: 1, 7: 1, 8: 2}, {0: 1, 2: 1, 3: 1, 4: 2, 5: 1, 6: 1, 8: 1},
         {0: 1, 2: 1, 3: 1, 5: 1, 6: 1, 7: 2, 8: 1}]
allt = set()
for ms in found:
    for t in range(9):
        allt.add(tuple(sorted(((b + t) % 9, a) for b, a in ms.items())))
base = found[0]
orbit = {tuple(sorted(((b + t) % 9, a) for b, a in base.items())) for t in range(9)}
E2 = Fr(1, 2 ** (4 + 3 - 3)) * cstar(8 - 8 - 6 + 6)
ok = all(share_at(9, dict(x), 9) == E2 for x in allt)
print(f"   the 7 multisets found (those containing 0) have {len(allt)} translates in all; they are one orbit of the first: {allt == orbit};"
      f" P(bad at 9) = E2 = {E2} for each of them: {ok}; of the {len(allt)}, those containing 0: {sum(1 for x in allt if any(b == 0 for b, a in x))}")

print("(2) Lemma B (i), largest prime 5")
ms = {0: 1, 5: 1, 10: 1, 15: 1, 20: 1, 1: 2, 2: 2, 3: 2, 4: 2}
res = sorted(ms); FL = {f['d']: f for f in fully_live(25, res)}
f = FL[25]; m = sum(ms.values()); P = share_at(25, ms, 25); k = f['kp']; bound = Fr(1, 2 ** (k - 1)) * cstar(m - 2 * k + 2)
print(f"   Z_25, {ms}: m = {m}, d = 25 fully live with ranks {f['ranks']}, e = {f['e']}, kappa = {f['kap']}, need = {f['need']}; P(bad at 25) = {P}; bound 2^(1-k) c*_(m-2k+2) = {bound}; equal: {P == bound}")
ms = {0: 1, 5: 1, 10: 1, 15: 1, 20: 1, 1: 2, 2: 2, 3: 2, 4: 2, 6: 0}
# the same shape for the prime 3 (e = 9, m = 7) and for 7 (e = 49, m = 19), to see that it is general
for (p, n) in ((3, 9), (7, 49)):
    ms = {p * t: 1 for t in range(p)}
    for t in range(1, p): ms[t] = 2
    f = {x['d']: x for x in fully_live(n, sorted(ms))}[n]; m = sum(ms.values()); P = share_at(n, ms, n); k = f['kp']; bound = Fr(1, 2 ** (k - 1)) * cstar(m - 2 * k + 2)
    print(f"   Z_{n}, one element in each class modulo {n} of the class 0 modulo {p}, pairs at 1..{p - 1}: m = {m}, e = {f['e']}, need = {f['need']}; P = {P}; bound = {bound}; equal: {P == bound}")
def Pr(r):
    return {v: Fr(math.comb(r, (r + v) // 2), 2 ** r) for v in range(-r, r + 1, 2)}
def parts5(m, k=5, lo=1):
    if k == 1:
        if m >= lo: yield (m,)
        return
    for r in range(lo, m // k + 1):
        for rest in parts5(m - r, k - 1, r): yield (r,) + rest
n = 0; eqs = []; best = (Fr(0), None)
for m in range(5, MTOP + 1):
    bound = Fr(1, 8) * cstar(m - 6)
    for rs in parts5(m):
        if len({r % 2 for r in rs}) > 1: continue          # different parities: no bad signing
        ds = [Pr(r) for r in rs]; P = Fr(0)
        for v in ds[0]:
            t = Fr(1)
            for d_ in ds: t *= d_.get(v, 0)
            P += t
        n += 1
        assert P <= bound
        if P == bound: eqs.append((m, rs))
        if m >= 6 and P / bound > best[0]: best = (P / bound, (m, rs))
print(f"   e = 5, one cell with classes of sizes r_0..r_4 >= 1 (one parity), 5 <= m <= {MTOP}: {n} shapes; equality with 2^(-3) c*_(m-6) at {eqs}; largest ratio for m >= 6: {float(best[0]):.4f} at {best[1]}")

print("(3) the K_same of the hill-climbing in section 5")
D = dict([(3, 4), (6, 4), (9, 4), (11, 2), (18, 4), (19, 2)]); r = value_sets(27, D)
print(f"   Z_27 {D}: K_same = {r[1]} = {float(r[1]):.6f} (text: 38105/32768 = 1.1629); K_other = {r[2]}; Theorem H checks failed: {len(r[3])}")
D = dict([(2, 2), (3, 1), (6, 2), (9, 2), (13, 1), (15, 2), (18, 2), (21, 1), (36, 1), (39, 2), (40, 1)]); r = value_sets(45, D)
print(f"   Z_45 {D}: K_same = {r[1]} = {float(r[1]):.6f} (text: 597/512 = 1.1660); K_other = {r[2]}; Theorem H checks failed: {len(r[3])}")

print("(4) Theorem H's checks on the named decorations (E|V|, K_same, K_other, number of failed checks)")
def lift(conds, n):
    out = {}
    for cond, h in conds:
        b = next(b for b in range(n) if all(b % mo == re_ for mo, re_ in cond.items())); out[b] = out.get(b, 0) + h
    return out
named = [(3, {1: 2, 2: 2}), (3, {1: 4, 2: 4}), (9, {1: 2, 2: 2, 3: 2, 6: 2}),
         (45, lift([({9: x, 5: 0}, 2) for x in (1, 2, 3, 6)] + [({9: 0, 5: y}, 2) for y in (1, 2, 3, 4)], 45)),
         (27, {1: 2, 2: 2, 3: 2, 6: 2, 9: 2, 18: 2}), (81, {1: 2, 2: 2, 3: 2, 6: 2, 9: 2, 18: 2, 27: 2, 54: 2}),
         (135, lift([({27: x, 5: 0}, 2) for x in (1, 2, 3, 6, 9, 18)] + [({27: 0, 5: y}, 2) for y in (1, 2, 3, 4)], 135)),
         (105, lift([({3: x, 35: 0}, 1) for x in (1, 2)] + [({5: y, 21: 0}, 1) for y in (1, 2, 3, 4)] + [({7: z, 15: 0}, 1) for z in range(1, 7)], 105)),
         (9, {1: 2, 2: 2, 3: 4, 6: 4}), (27, {1: 2, 2: 2, 3: 2, 6: 2, 9: 4, 18: 4}),
         (135, {5: 2, 10: 2, 15: 2, 30: 2, 45: 4, 90: 4, 27: 2, 54: 2, 81: 2, 108: 2})]
tot = 0
for n_, D in named:
    r = value_sets(n_, D); tot += len(r[3])
    print(f"   Z_{n_} {D}: {r[0]}, {r[1]}, {r[2]}, failed {len(r[3])}")
print(f"   {len(named)} named decorations (the twelfth, with 1265625 grid points, is in common.out): failed checks in all {tot}")

print("(5) counts")
sub = {}
for f_ in sorted(glob.glob('exh-*.out') + glob.glob('exh2-*.out') + glob.glob('rand-10?.out') + glob.glob('gon-*.out') + ['heavy.out', 'c2more.out', 'beta7.out']):
    l = [x for x in open(f_) if x.startswith('[')][-1]
    g = re.search(r"multisets (\d+); fully live d (\d+) \(two or more primes (\d+); with P > 0: (\d+)", l)
    sub[f_] = tuple(int(x) for x in g.groups())
ex = [f_ for f_ in sub if f_.startswith('exh')]
print(f"   exhaustive runs: {len(ex)} files, {sum(sub[f_][0] for f_ in ex)} multisets, {sum(sub[f_][1] for f_ in ex)} fully live d, {sum(sub[f_][2] for f_ in ex)} with two or more primes")
for f_ in sub:
    if f_ not in ex: print(f"   {f_}: {sub[f_][0]} multisets, {sub[f_][1]} fully live d, {sub[f_][2]} with two or more primes, {sub[f_][3]} with bad signings")
print(f"   not exhaustive, in all: {sum(sub[f_][0] for f_ in sub if f_ not in ex)} multisets; without beta7.out: {sum(sub[f_][0] for f_ in sub if f_ not in ex and f_ != 'beta7.out')}")
print(f"   all files: {sum(v[0] for v in sub.values())} multisets, {sum(v[1] for v in sub.values())} fully live d, {sum(v[2] for v in sub.values())} with two or more primes, {sum(v[3] for v in sub.values())} with bad signings")

print("(6) the optional remark")
P_ = PSI.pairs_upto(160)
Wp = sum(Fr(pp, 2 ** (s + q - 2)) + Fr(nc, 2 ** (s + q - 1)) for (q, s, pp, nc) in P_)
print(f"   sqrt(2/pi) (2W+ - 1/6) = {math.sqrt(2 / math.pi) * (float(Wp) - 1 / 6):.5f};  sum over j of 2^(1-2j) = 2/3;  sqrt(2/pi) 78764625/67108864 = {math.sqrt(2 / math.pi) * 78764625 / 67108864:.6f};  sqrt(2/pi) 19221/16384 = {math.sqrt(2 / math.pi) * 19221 / 16384:.6f}")
