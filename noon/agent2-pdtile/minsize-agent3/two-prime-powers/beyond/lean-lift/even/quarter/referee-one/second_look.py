"""Referee, second look (after the author's revision): the changed places only.

1. the new example for eleven elements on Z_1155 (item (ii) of the head; example11.out): recounted by the definition,
   with every check of ref_odd.analyse, and the four events at 3, 5, 7, 11 compared with the sum of the signs
2. the recounts for 14 and 16 elements on Z_27 (recount14.out, recount16.out): the shape named there, and my own maxima
3. "2k = 138" of section 9
4. the remark after Lemma 2: the inequality of (b) for ANY sizes (z_t = 0 for an odd size)
5. two numbers of my own first report: how many moduli the chain runs used; where each text's bound is the sharper
"""
import re, glob
from fractions import Fraction as Fr
from math import comb
import numpy as np
from cyc import signs, bad_at, divisors
from ref_odd import analyse, share
import ref_tree3 as T

# ---- 1
n = 1155
r3 = [0] * 9 + [1, 2]; r5 = [0] * 7 + [1, 2, 3, 4]; r7 = [0] * 5 + [1, 2, 3, 4, 5, 6]; r11 = list(range(11))
B = [next(x for x in range(n) if (x % 3, x % 5, x % 7, x % 11) == t) for t in zip(r3, r5, r7, r11)]
assert B == [0, 210, 420, 630, 840, 225, 765, 381, 1152, 1153, 1154], B          # the multiset of example11.out
s_bad, s_3, s_rest, where = analyse(n, B)
print(f"1. Z_1155, m = 11, B = {B}: bad share {s_bad} (= 43/256: {s_bad == Fr(43, 256)}; > 171/1024: {s_bad > Fr(171, 1024)}); "
      f"at a power of 3: {s_3}; by d: " + ", ".join(f"{d}: {v}" for d, v in where.items()))
E = signs(11); sig = E.sum(axis=1)
for q in (3, 5, 7, 11):
    v = bad_at(n, B, q, E)
    print(f"   bad at {q}: {int(v.sum())} of 2048 signings, sums of signs there: {sorted(set(sig[v].tolist()))}")
tot = np.zeros(2048, dtype=bool)
for d in divisors(n):
    tot |= bad_at(n, B, d, E)
print(f"   bad at some d | 1155: {int(tot.sum())} of 2048 = {Fr(int(tot.sum()), 2048)}; the four prime events are pairwise disjoint: "
      f"{int(tot.sum()) == sum(int(bad_at(n, B, q, E).sum()) for q in (3, 5, 7, 11))}; residues modulo 3, 5, 7, 11: "
      f"{[sorted([sum(1 for b in B if b % q == r) for r in range(q)], reverse=True) for q in (3, 5, 7, 11)]}")

# ---- 2
s16 = (((2, 2, 2), (0, 0, 0), (0, 0, 0)), ((2, 0, 0), (2, 0, 0), (2, 0, 0)), ((4, 0, 0), (0, 0, 0), (0, 0, 0)))
s14 = (((2, 2, 2), (2, 0, 0), (2, 0, 0)), ((2, 0, 0), (0, 0, 0), (0, 0, 0)), ((2, 0, 0), (0, 0, 0), (0, 0, 0)))
print(f"2. the shape of recount16.out: {T.size(s16)} elements, X = {T.numbers(s16)['X']}; the shape of recount14.out: {T.size(s14)} elements, X = {T.numbers(s14)['X']}")
for f in ('tree-shapes-d3-16.out', 'tree-shapes-d3-18.out'):
    t = open(f).read()
    for m in (14, 16):
        mm = re.search(r"^m = %d: +(\d+) shapes; largest X = (\S+) " % m, t, re.M)
        print(f"   my run {f}: m = {m}: {mm.group(1)} shapes on Z_27, largest X = {mm.group(2)}")
t = open('tree-shapes-d2-20.out').read()
print("   my run on Z_9: " + "; ".join(f"m = {m}: largest X = " + re.search(r"^m = %d: +\d+ shapes; largest X = (\S+) " % m, t, re.M).group(1) for m in (14, 16, 18)))

# ---- 3
d = lambda k: Fr(comb(2 * k, k), 4 ** k)
holds = [k for k in range(0, 400) if d(k) + Fr(1, 15) <= 2 * d(k + 1)]
print(f"3. c_(2k) + 1/15 <= 2 d_(k+1) holds exactly for k in 0..{max(holds)} without a break: {holds == list(range(max(holds) + 1))}; so for 2k <= {2 * max(holds)} (checked k < 400)")

# ---- 4
cnt = 0; odd_cases = 0
for a, mmax in ((2, 14), (3, 11), (4, 9)):
    for m in range(1, mmax + 1):
        for s in T.all_shapes(a, m):
            rs = [T.size(t) for t in s]
            if sum(1 for r in rs if r) < 2:
                continue
            nb = T.numbers(s); kids = [T.numbers(t) for t in s]
            zs = [k['z'] for k in kids]; Xs = [k['X'] for k in kids]
            assert all(zs[t] == 0 for t in range(3) if rs[t] % 2), ("z for an odd size", s)
            assert all(kids[t]['U'] == zs[t] + Xs[t] for t in range(3))
            rhs = (zs[0] + Xs[0]) * (zs[1] + Xs[1]) * (zs[2] + Xs[2]) - zs[0] * zs[1] * zs[2]
            assert nb['HX'] <= rhs, ("Lemma 2 (b), any sizes", s)
            cnt += 1
            if any(r % 2 for r in rs):
                odd_cases += 1
        T.law.cache_clear()
print(f"4. Lemma 2 (b) for any sizes: {cnt} shapes with a branching root (Z_9 to m = 14, Z_27 to m = 11, Z_81 to m = 9), {odd_cases} of them with an odd size: no failure")

# ---- 5
mods = set(); per = {}
for f in sorted(glob.glob('odd-chain-*.out')):
    lst = re.search(r"on \[([0-9, ]+)\]", open(f).read()).group(1)
    per[f] = [int(x) for x in lst.split(',')]; mods |= set(per[f])
print(f"5. moduli of my chain runs: {sorted(mods)}: {len(mods)} moduli")
xi = T.xi_table(46)
one = {}
txt = open('ref_rec-240.out').read()
for m in range(3, 27):
    mm = re.search(r"^ +%d +\S+ +\S+ \(\d+ e\*\) +\S+ +(\S+) = " % m, txt, re.M)
    one[m] = Fr(mm.group(1))
for m in range(27, 47):
    one[m] = (T.cc(m) if m % 2 == 0 else 0) + xi[m] + Fr(118569, 10 ** 6)
two = {3: Fr(1, 4), 4: Fr(3, 8), 5: Fr(5, 16), 6: Fr(3, 8), 7: Fr(5, 16), 8: Fr(3, 8), 9: Fr(71, 256), 10: Fr(47, 128), 11: Fr(265, 1024),
       12: Fr(707, 2048), 13: Fr(1033, 4096), 14: Fr(175, 512), 15: Fr(1971, 8192), 16: Fr(10737, 32768)}
dec = "0.249557 0.366203 0.236824 0.349281 0.221837 0.334183 0.208458 0.320811 0.196207 0.304530 0.185741 0.290239 0.175215 0.278365 " \
      "0.166942 0.266245 0.159746 0.255903 0.153502 0.248232 0.147865 0.239581 0.142856 0.231802 0.138279 0.226072 0.134185 0.219407 0.130451 0.213360"
for m, x in zip(range(17, 47), dec.split()):
    two[m] = Fr(x)
eq = [m for m in range(3, 47) if one[m] == two[m]]
one_sharper = [m for m in range(3, 47) if one[m] < two[m] and abs(one[m] - two[m]) > Fr(1, 10 ** 6)]
two_sharper = [m for m in range(3, 47) if two[m] < one[m] and abs(one[m] - two[m]) > Fr(1, 10 ** 6)]
print(f"   bounds for beta(m), 3 <= m <= 46 (text one: b(m), from 27 on tbar + 0.118569; text two: its table T2, decimals from 17 on):")
print(f"   equal: {eq}; text one sharper: {one_sharper}; text two sharper: {two_sharper}")
print("   m = 25, 26: one", float(one[25]), float(one[26]), " two", float(two[25]), float(two[26]))
