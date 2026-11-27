# Referee test of the recursion for c(m) (section 4) against the definition of c(L) in Theorem P' on the digit box
# with the family of tree levels written out, and of the coverage claim.
import itertools, sys
from fractions import Fraction
from functools import lru_cache
from sympy import factorint, divisor_count


@lru_cache(None)
def c_rec(m):
    if m == 1:
        return Fraction(1)
    best = Fraction(-1)
    for p, a in factorint(m).items():
        cm = c_rec(m // p)
        if cm > 0:
            mp = m // p ** a
            best = max(best, min(cm / 2, cm - divisor_count(mp) * Fraction(2, 2 ** p)))
    return best


def c_def(coords, levels):
    """definition of Theorem P': coords = tuple of (p,e); levels = frozenset of frozensets of coords"""
    @lru_cache(None)
    def go(coords, levels):
        if not coords:
            return Fraction(1)
        best = Fraction(-1)
        for j in coords:
            rest = tuple(x for x in coords if x != j)
            L0 = frozenset(P for P in levels if j not in P)
            L1 = frozenset(P - {j} for P in levels if j in P)
            assert L1 <= L0
            c0 = go(rest, L0)
            if c0 > 0:
                best = max(best, min(c0 / 2, c0 - len(L1) * Fraction(2, 2 ** j[0])))
        return best
    return go(coords, levels)


def tree_levels(m):
    fac = factorint(m)
    out = set()
    for ch in itertools.product(*[range(a + 1) for a in fac.values()]):
        out.add(frozenset((p, i) for p, i in zip(fac, ch) if i))
    return frozenset(out)


bad = 0
tested = 0
for m in range(1, 6000, 2):
    fac = factorint(m)
    if sum(fac.values()) > 7:
        continue
    coords = tuple((p, e) for p in fac for e in range(1, fac[p] + 1))
    a, b_ = c_rec(m), c_def(coords, tree_levels(m))
    tested += 1
    # compare as "positive or not" and the value when positive (a nonpositive value has no meaning)
    if (a > 0) != (b_ > 0) or (a > 0 and a != b_):
        bad += 1
        print('MISMATCH recursion vs definition at m =', m, a, b_)
print('recursion of section 4 against the definition of Theorem P\' (tree levels): m odd < 6000 tested', tested, 'mismatches', bad)
for m in (9, 27, 45, 63, 75, 175, 441, 189, 3 ** 3 * 5 ** 3 * 7 ** 3, 5 ** 4 * 7, 3 ** 3 * 7, 3 ** 3 * 5 ** 4):
    print('  c(%d) = %s' % (m, c_rec(m)))

# Theorem P hypothesis for "digits in increasing order n_j >= 2j" implies c(m) >= 2^-k ?
viol = 0
for m in range(3, 200000, 2):
    fac = factorint(m)
    ds = sorted(p for p, a in fac.items() for _ in range(a))
    if all(ds[j - 1] >= 2 * j for j in range(2, len(ds) + 1)):
        if c_rec(m) < Fraction(1, 2 ** len(ds)):
            viol += 1
print('digits increasing with n_j >= 2j but c(m) < 2^-k:', viol)

# coverage for odd n < LIM
LIM = 200000
unc = []
only6 = []
for n in range(3, LIM, 2):
    fac = factorint(n)
    ps = sorted(fac)
    t23 = len(ps) <= 2 or (len(ps) == 3 and sorted(fac.values())[:2] == [1, 1])
    t6 = c_rec(n) > 0 or any(c_rec(n // p ** a) > 0 for p, a in fac.items())
    if not t23 and not t6:
        unc.append(n)
    if t6 and not t23:
        only6.append(n)
print('odd n <', LIM, 'covered by nothing:', unc)
print('covered by Theorem 6 and not by the forms p^a q^b, p r q^b:', len(only6), 'first', only6[:7])
sqf_fail = [n for n in range(3, LIM, 2) if all(a == 1 for a in factorint(n).values()) and c_rec(n) < Fraction(1, 2 ** len(factorint(n)))]
print('squarefree odd n with c(n) < 2^-omega:', len(sqf_fail))
