# Second look.  (A) The plain rule for the severe test against "S(zeta) in 3 Z[zeta]".
# (B) the steps of the ladder as the page now words them.  (C) every hour marked once: the count of falls that fail.
import itertools, cmath, os, sys
from math import comb
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check1 import rem_table, divisors, signs_matrix, cyclo  # noqa


def part_A():
    print("== (A) severe test at d: exact (remainder modulo Phi_d has every coefficient divisible by 3)")
    print("       against the plain rule, by search: some whole numbers c_0..c_(d-1), one for each of the d points of the walk,")
    print("       with  signed sum + 3 * sum c_j * point_j = 0  (numerically, then confirmed exactly)")
    total = agree = 0
    bad_found = 0
    for d, box in ((1, 3), (2, 3), (4, 2), (5, 2), (7, 1), (8, 1), (10, 1)):
        n = {1: 12, 2: 12, 4: 12, 5: 20, 7: 14, 8: 8, 10: 20}[d]
        mmax = {1: 6, 2: 6, 4: 5, 5: 4, 7: 4, 8: 5, 10: 4}[d]
        z = cmath.exp(2j * cmath.pi / d)
        pts = [z ** j for j in range(d)]
        T = rem_table(n, d)
        Td = rem_table(d, d)           # remainders of X^j, j < d
        table = {}
        for c in itertools.product(range(-box, box + 1), repeat=d):
            v = 3 * sum(cj * p for cj, p in zip(c, pts))
            table.setdefault((round(v.real * 1e6), round(v.imag * 1e6)), c)
        cnt = ok = nbad = 0
        for m in range(1, mmax + 1):
            S = signs_matrix(m)
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                marks = (0,) + rest
                R = S @ T[list(marks)]
                exact = ~(R % 3).any(axis=1)
                for i, signs in enumerate(S):
                    s = sum(int(e) * z ** h for e, h in zip(signs, marks))
                    key = (round(-s.real * 1e6), round(-s.imag * 1e6))
                    c = table.get(key)
                    found = False
                    if c is not None:
                        # confirm exactly: remainder of S + 3 sum c_j X^j modulo Phi_d is 0
                        chk = R[i] + 3 * (np.array(c) @ Td)
                        found = not chk.any()
                    cnt += 1
                    if found == bool(exact[i]):
                        ok += 1
                    nbad += bool(exact[i])
        print(f"   d = {d:2d} (clock {n}, 1 to {mmax} marks, every choice of signs; c_j from -{box} to {box}): "
              f"{cnt} signed markings, {nbad} fail the severe test, rule and definition agree in {ok}")
        total += cnt; agree += ok; bad_found += nbad
    print(f"   in all {total} signed markings, agreement in {agree}; {bad_found} fail the severe test")
    # the rule read with ANY point of the circle is another test: one plus at the divisor 1
    th = cmath.acos(-1 / 6)
    v = 1 + 3 * cmath.exp(1j * th) + 3 * cmath.exp(-1j * th)
    print(f"   one mark, a plus, at the divisor 1: with three weights at each of two points OFF the walk (cos = -1/6) the sum is {abs(v):.1e};")
    print("   so if 'one point' may be any point of the circle a single mark fails the test, which by the definition it passes (1 is no multiple of 3)")


def part_B():
    print("== (B) the ladder as now worded, severe test and plain sense; every marking of 3..m marks with a mark at 0, every fall")
    for n, mmax in ((int(sys.argv[2]), int(sys.argv[3])),):
        k = 0
        while n % 2 ** (k + 1) == 0:
            k += 1
        nodd = n // 2 ** k
        ds = divisors(n)
        T = {d: rem_table(n, d) for d in ds}
        fails = dict(lowest=0, rung_rule=0, one_for_one=0, set_2d=0, inside=0, halves_nothing=0, adds=0, twice=0)
        cases = 0
        for m in range(3, mmax + 1):
            S = signs_matrix(m); N = len(S)
            idx = {tuple(row): i for i, row in enumerate(S.tolist())}
            for rest in itertools.combinations_with_replacement(range(n), m - 1):
                marks = np.array((0,) + rest)
                for d in divisors(nodd):
                    for sense in ('severe', 'plain'):
                        def nothing(mask, flip=None):
                            """falls in which the marks of mask, by themselves (signs of flip turned over), fail at d"""
                            if not mask.any():
                                return np.ones(N, dtype=bool)
                            SS = S[:, mask].copy()
                            if flip is not None:
                                SS[:, flip[mask]] *= -1
                            v = SS @ T[d][marks[mask]]
                            if sense == 'severe':
                                v = v % 3
                            return ~v.any(axis=1)
                        def fail_at(dd):
                            v = S @ T[dd][marks]
                            if sense == 'severe':
                                v = v % 3
                            return ~v.any(axis=1)
                        cases += 1
                        allm = np.ones(m, dtype=bool)
                        low = fail_at(d)
                        if not np.array_equal(low, nothing(allm)):
                            fails['lowest'] += 1
                        # sets[j] = falls in which every heap of step j (remainder modulo 2^j) weighs nothing
                        sets = []
                        for j in range(k + 1):
                            a = np.ones(N, dtype=bool)
                            for r in range(2 ** j):
                                a &= nothing((marks % 2 ** j) == r)
                            sets.append(a)
                        some = low.copy()
                        added_total = 0
                        for j in range(1, k + 1):
                            rung = fail_at(2 ** j * d)
                            some |= rung
                            # rule: in every heap of the step before the two halves weigh the same,
                            # that is: the heap weighs nothing once the signs in one half are turned over
                            upper = (marks % 2 ** j) >= 2 ** (j - 1)
                            a = np.ones(N, dtype=bool)
                            for r in range(2 ** (j - 1)):
                                a &= nothing((marks % 2 ** (j - 1)) == r, flip=upper)
                            if not np.array_equal(a, rung):
                                fails['rung_rule'] += 1
                            # turning over the signs in the upper halves carries the failures of the rung onto the rung's set
                            flipped = S.copy(); flipped[:, upper] *= -1
                            image = np.zeros(N, dtype=bool)
                            image[[idx[tuple(row)] for row in flipped[rung].tolist()]] = True
                            if not np.array_equal(image, sets[j - 1]):
                                fails['one_for_one'] += 1
                            if j == 1 and not np.array_equal(sets[0], low):
                                fails['set_2d'] += 1
                            if (sets[j] & ~sets[j - 1]).any():
                                fails['inside'] += 1
                            # halves weigh nothing: fails at the rung and at the lowest rung
                            if (sets[j] & ~(rung & low)).any():
                                fails['halves_nothing'] += 1
                            adds = int((rung & ~low).sum())
                            if adds > int(sets[j - 1].sum()) - int(sets[j].sum()):
                                fails['adds'] += 1
                            added_total += adds
                        if int(some.sum()) > 2 * int(low.sum()):
                            fails['twice'] += 1
        print(f"   clock {n}, 3 to {mmax} marks: {cases} (marking, ladder, sense); failures of each sentence: {fails}")


def part_C():
    print("== (C) every hour marked once: falls that fail somewhere, against twice those that fail at the divisor 1")
    for n in (2, 4, 6, 8, 10, 12, 14, 16):
        ds = divisors(n)
        S = signs_matrix(n)
        marks = list(range(n))
        bad = np.zeros(len(S), dtype=bool)
        for d in ds:
            v = S @ rem_table(n, d)[marks]
            bad |= ~v.any(axis=1)
        at1 = int((S.sum(axis=1) == 0).sum())
        print(f"   clock {n:2d}: {int(bad.sum())} falls fail somewhere; fail at 1: {at1} = C({n},{n//2}) {comb(n, n//2)}; twice that: {2*at1}"
              f"  -> {'equal' if int(bad.sum()) == 2*at1 else 'not equal'}")


if __name__ == '__main__':
    which = sys.argv[1]
    {'A': part_A, 'B': part_B, 'C': part_C}[which]()
