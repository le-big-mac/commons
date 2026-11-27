# Is "pass the severe test at every divisor without a factor 3" the same as "pass it at every divisor"?
# And Proposition H / Theorem G as the page words them, on small clocks.
import itertools, os, sys
from fractions import Fraction
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check1 import rem_table, divisors, signs_matrix  # noqa

def severe_fail(S, T, marks):
    v = S @ T[list(marks)]
    return ~(v % 3).any(axis=1)

print("== severe test: failing at a divisor 3d or 9d forces failing at d ?  (then 'pass at every divisor without a factor 3' = 'pass at every divisor')")
for n, mmax in ((9, 5), (12, 5), (18, 4), (36, 3), (45, 3), (27, 4)):
    ds = divisors(n); T = {d: rem_table(n, d) for d in ds}
    viol = cnt = 0
    for m in range(1, mmax + 1):
        S = signs_matrix(m)
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            marks = (0,) + rest
            f = {d: severe_fail(S, T[d], marks) for d in ds}
            for d in ds:
                if d % 3 == 0:
                    cnt += 1
                    if (f[d] & ~f[d // 3]).any():
                        viol += 1
    print(f"   clock {n}: {cnt} (marking, divisor with a factor 3), violations {viol}")

print("== odd clocks, three or more marks: least share of falls that pass the severe test at every divisor without a factor 3")
for n, mmax in ((3, 8), (5, 6), (9, 5), (15, 5), (21, 4), (35, 4), (45, 3)):
    ds = [d for d in divisors(n) if d % 3]; T = {d: rem_table(n, d) for d in ds}
    out = []
    for m in range(3, mmax + 1):
        S = signs_matrix(m); least = None
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            marks = (0,) + rest
            bad = np.zeros(len(S), dtype=bool)
            for d in ds:
                bad |= severe_fail(S, T[d], marks)
            fr = Fraction(int((~bad).sum()), len(S))
            least = fr if least is None or fr < least else least
        out.append(f"{m} marks {least}")
    print(f"   clock {n}: " + "; ".join(out))

print("== clocks of twice an odd number: signs good exactly when two things are good on the clock of half as many hours")
print("   (the marks wound back; the signs as they are, and the signs with those at odd hours turned over)")
for n, mmax in ((6, 6), (10, 5), (18, 4), (30, 4), (42, 3)):
    h = n // 2
    ds = divisors(n); T = {d: rem_table(n, d) for d in ds}
    dh = divisors(h); Th = {d: rem_table(h, d) for d in dh}
    dh3 = [d for d in dh if d % 3]
    mism = cnt = notimplied = 0
    for m in range(1, mmax + 1):
        S = signs_matrix(m)
        for rest in itertools.combinations_with_replacement(range(n), m - 1):
            marks = np.array((0,) + rest); cnt += 1
            good = np.ones(len(S), dtype=bool)
            for d in ds:
                good &= (S @ T[d][marks]).any(axis=1)
            w = marks % h
            S2 = S.copy(); S2[:, marks % 2 == 1] *= -1
            g1 = np.ones(len(S), dtype=bool); g2 = g1.copy(); p1 = g1.copy(); p2 = g1.copy()
            for d in dh:
                g1 &= (S @ Th[d][w]).any(axis=1); g2 &= (S2 @ Th[d][w]).any(axis=1)
            for d in dh3:
                p1 &= ((S @ Th[d][w]) % 3).any(axis=1); p2 &= ((S2 @ Th[d][w]) % 3).any(axis=1)
            if not np.array_equal(good, g1 & g2):
                mism += 1
            if (p1 & p2 & ~good).any():
                notimplied += 1
    print(f"   clock {n}, 1 to {mmax} marks: {cnt} markings; 'good iff both good on the half clock' fails in {mism}; 'passes both severe tests but is not good' in {notimplied}")
