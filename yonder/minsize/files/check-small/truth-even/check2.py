# Checks for the paragraphs on the severe test and on the ladder, by all signings, exact integer arithmetic.
# usage: check2.py n mmax
import itertools, os, sys
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # my own folder (the interpreter runs isolated)
from check1 import rem_table, divisors, signs_matrix  # noqa


def main(n, mmax):
    k = 0
    while n % (2 ** (k + 1)) == 0:
        k += 1
    nodd = n // 2 ** k
    n3 = n
    while n3 % 3 == 0:
        n3 //= 3
    ds = divisors(n)
    T = {d: rem_table(n, d) for d in ds}
    odd_divs = divisors(nodd)
    stats = dict(multisets=0, ladders=0, max_ratio_plain=Fraction(0), max_ratio_severe=Fraction(0),
                 crit_plain_fail=0, crit_severe_fail=0, bij_plain_fail=0, bij_severe_fail=0, nest_fail=0,
                 severe_implies_fail=0, plain_ineq_fail=0, severe_ineq_fail=0, tprime_fail=0,
                 threegood_not_good=0, p_m_fail=0)
    least_share_3good = {}
    least_share_good = {}
    for m in range(3, mmax + 1):
        S = signs_matrix(m)
        N = len(S)
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            marks = np.array((0,) + rest)
            stats['multisets'] += 1
            # plain and severe failure at every divisor of n
            bad = {}
            bad3 = {}
            for d in ds:
                v = S @ T[d][marks]
                bad[d] = ~v.any(axis=1)
                bad3[d] = ~(v % 3).any(axis=1)
            anybad = np.zeros(N, dtype=bool)
            for d in ds:
                anybad |= bad[d]
            not3good = np.zeros(N, dtype=bool)
            for d in divisors(n3):
                not3good |= bad3[d]
            # signs that pass the severe test at every divisor without a factor 3 are good at every divisor
            if (anybad & ~not3good).any():
                stats['threegood_not_good'] += 1
            # severe failure at 1: pluses minus minuses a multiple of 3
            diff = S.sum(axis=1)
            if not np.array_equal(bad3[1], diff % 3 == 0):
                stats['p_m_fail'] += 1
            g3 = Fraction(int((~not3good).sum()), N)
            g = Fraction(int((~anybad).sum()), N)
            if m not in least_share_3good or g3 < least_share_3good[m][0]:
                least_share_3good[m] = (g3, tuple(int(x) for x in marks))
            if m not in least_share_good or g < least_share_good[m][0]:
                least_share_good[m] = (g, tuple(int(x) for x in marks))
            for e in odd_divs:
                stats['ladders'] += 1
                rungs = [2 ** j * e for j in range(k + 1)]
                for (B, key_ratio, key_ineq, zero) in ((bad, 'max_ratio_plain', 'plain_ineq_fail', 'plain'),
                                                      (bad3, 'max_ratio_severe', 'severe_ineq_fail', 'severe')):
                    some = np.zeros(N, dtype=bool)
                    for d in rungs:
                        some |= B[d]
                    q, z = int(some.sum()), int(B[e].sum())
                    if q > 2 * z:
                        stats[key_ineq] += 1
                    if z:
                        r = Fraction(q, z)
                        if r > stats[key_ratio]:
                            stats[key_ratio] = r
                    # heaps: F[dep] = every heap by remainder modulo 2^dep weighs nothing at e
                    F = []
                    halves_equal = []
                    for dep in range(k + 1):
                        allzero = np.ones(N, dtype=bool)
                        for r_ in range(2 ** dep):
                            c = (marks % 2 ** dep) == r_
                            if not c.any():
                                continue
                            v = S[:, c] @ T[e][marks[c]]
                            if zero == 'severe':
                                v = v % 3
                            allzero &= ~v.any(axis=1)
                        F.append(allzero)
                    for j in range(1, k + 1):
                        eq = np.ones(N, dtype=bool)
                        for r_ in range(2 ** (j - 1)):
                            c1 = (marks % 2 ** j) == r_
                            c2 = (marks % 2 ** j) == r_ + 2 ** (j - 1)
                            v = S[:, c1] @ T[e][marks[c1]] - S[:, c2] @ T[e][marks[c2]]
                            if zero == 'severe':
                                v = v % 3
                            eq &= ~v.any(axis=1)
                        halves_equal.append(eq)
                    # lowest rung: the one heap of all the marks weighs nothing
                    if not np.array_equal(F[0], B[e]):
                        stats['crit_' + zero + '_fail'] += 1
                    for j in range(1, k + 1):
                        # criterion: fails at rung 2^j e exactly when in every heap of the step before the halves weigh the same
                        if not np.array_equal(halves_equal[j - 1], B[2 ** j * e]):
                            stats['crit_' + zero + '_fail'] += 1
                        # one for one: as many falls fail at the rung as have every heap of the step before weighing nothing
                        if int(B[2 ** j * e].sum()) != int(F[j - 1].sum()):
                            stats['bij_' + zero + '_fail'] += 1
                        # nested
                        if (F[j] & ~F[j - 1]).any():
                            stats['nest_fail'] += 1
                    if q > 2 * z - int(F[k].sum()):
                        stats['tprime_fail'] += 1
    print(f"clock {n} (largest power of 2: {2**k}; odd part {nodd}), every marking of 3 to {mmax} marks with a mark at 0:")
    for key, val in stats.items():
        print(f"   {key}: {val}")
    for m in sorted(least_share_good):
        print(f"   {m} marks: least share of good signs {least_share_good[m][0]} at {least_share_good[m][1]};"
              f" least share passing the severe test everywhere {least_share_3good[m][0]} at {least_share_3good[m][1]}")


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]))
