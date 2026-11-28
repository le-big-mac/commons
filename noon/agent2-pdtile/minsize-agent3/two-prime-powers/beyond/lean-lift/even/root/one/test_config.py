"""Lemmas B, C, E, E', F on abstract configurations of a prime power level, exhaustively over small shapes.

At d = p^i the events "bad at d" and "bad at 1" depend only on the sizes of the classes inside the cells:
a configuration is a list of cells, a cell a tuple of class sizes (p of them: a full cell; fewer: not full).
bad at d  <=> every full cell has its p class sums equal (to v_D), every other cell has all class sums 0;
then the signs add up to p * (sum of the v_D).  The program computes exactly (fractions)
   P(bad at d)   and   P(bad at d and not bad at 1)
and compares with
   Lemma B:  P(bad) <= 2^-(N-2) c_ceil(m/N),                               N = k + p - 1
   Lemma C:  P(bad) <= 2^-(N-3) c_(r1) c_(m - r0 - r1 - 2(N-3))            for every full cell (r0 <= r1 its two smallest classes)
   Lemma F:  P(bad) <= 2^-(N-3) c_l c_(ceil(s/2) - 2(N-3)),                l the largest class, s = m - l
   Lemma E (m even):  P(bad, not at 1) <= 2^-(k+2p-5) c_L  for EVERY class size L of the configuration
   Lemma E' (m even, p = 3, k = 1):  P(bad, not at 1) <= (17/128) c_L  for every class size L.

usage: test_config.py P KMAX RMAX [HEAVY ...]     class sizes 1..RMAX, and each HEAVY size allowed as one further size
"""
import sys, math
from fractions import Fraction
from itertools import combinations_with_replacement

def cfrac(r): return Fraction(math.comb(r, r // 2), 2 ** r) if r >= 1 else Fraction(1)
def Pr(r, v): return Fraction(math.comb(r, (r + v) // 2), 2 ** r) if abs(v) <= r and (r + v) % 2 == 0 else Fraction(0)

def main():
    p, kmax, rmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    sizes = list(range(1, rmax + 1)) + [int(x) for x in sys.argv[4:]]
    full = list(combinations_with_replacement(sizes, p))
    notfull = [t for q in range(1, min(p, 3)) for t in combinations_with_replacement(sizes, q)]
    dist = {}
    for cell in full:
        lo = min(cell)
        d = {}
        for v in range(-lo, lo + 1):
            x = Fraction(1)
            for r in cell: x *= Pr(r, v)
            if x: d[v] = x
        dist[cell] = d
    zero = {}
    for cell in notfull:
        x = Fraction(1)
        for r in cell: x *= Pr(r, 0)
        zero[cell] = x
    types = [(c, True) for c in full] + [(c, False) for c in notfull]
    stat = dict(configs=0, even=0, E_checks=0, E_equal=0, E_pos=0, Eprime=0, Eprime_equal=0, C_checks=0, C_equal=0, F_checks=0, F_equal=0, B_equal=0)
    worstE = Fraction(0)
    for k in range(1, kmax + 1):
        for conf in combinations_with_replacement(range(len(types)), k):
            cells = [types[i] for i in conf]
            if not any(f for _, f in cells): continue
            m = sum(sum(c) for c, _ in cells); N = k + p - 1
            stat['configs'] += 1
            # distribution of the sum of the v_D
            acc = {0: Fraction(1)}
            for c, f in cells:
                if f:
                    new = {}
                    for s0, x in acc.items():
                        for v, y in dist[c].items(): new[s0 + v] = new.get(s0 + v, 0) + x * y
                    acc = new
                else:
                    z = zero[c]; acc = {s0: x * z for s0, x in acc.items()} if z else {}
            bad = sum(acc.values(), Fraction(0)); e = bad - acc.get(0, Fraction(0))
            allsizes = sorted({r for c, _ in cells for r in c})
            ell = allsizes[-1]; s = m - ell
            bB = Fraction(1, 2 ** (N - 2)) * cfrac(-(-m // N))
            assert bad <= bB, ("Lemma B", cells, bad, bB)
            if bad == bB: stat['B_equal'] += 1
            for c, f in cells:
                if f:
                    r0, r1 = c[0], c[1]
                    bC = Fraction(1, 2 ** (N - 3)) * cfrac(r1) * cfrac(m - r0 - r1 - 2 * (N - 3))
                    stat['C_checks'] += 1
                    assert bad <= bC, ("Lemma C", cells, bad, bC)
                    if bad == bC: stat['C_equal'] += 1
            bF = Fraction(1, 2 ** (N - 3)) * cfrac(ell) * cfrac(-(-s // 2) - 2 * (N - 3))
            stat['F_checks'] += 1
            assert bad <= bF, ("Lemma F", cells, bad, bF)
            if bad == bF: stat['F_equal'] += 1
            if m % 2 == 0:
                stat['even'] += 1
                if e > 0: stat['E_pos'] += 1
                for L in allsizes:
                    bE = Fraction(1, 2 ** (k + 2 * p - 5)) * cfrac(L)
                    stat['E_checks'] += 1
                    assert e <= bE, ("Lemma E", cells, e, bE, L)
                    if e == bE: stat['E_equal'] += 1
                    if e / bE > worstE: worstE = e / bE
                    if p == 3 and k == 1:
                        stat['Eprime'] += 1
                        assert e <= Fraction(17, 128) * cfrac(L), ("Lemma E'", cells, e, L)
                        if e == Fraction(17, 128) * cfrac(L): stat['Eprime_equal'] += 1
    print(' '.join(sys.argv[1:]), '| no failure |', ' '.join(f"{a}={b}" for a, b in stat.items()), f"| largest P(E)/bound of Lemma E: {worstE} = {float(worstE):.4f}")

if __name__ == '__main__':
    main()
