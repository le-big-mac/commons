# check_texts.py -- numbers of the three texts (A: section 12 of the working note, B: the paper's paragraph, C: the
# plain paragraphs) against the referee's outputs in ../ and against the definitions.  Reads files, computes little.
import re, glob, math, sys
from fractions import Fraction
sys.path.insert(0, "..")
from rlib import mu, divisors, factor

# ---- 1. the 3,099,711 multisets of exh_full.py: complete runs, sampled runs, runs with every multiset ----
tot = {"complete, multisets that contain 0": 0, "sampled (one size further, every k-th multiset that contains 0)": 0, "every multiset (not only those with 0)": 0}
groups = set()
rows = []
for f in sorted(glob.glob("../exh_*.out")):
    s = open(f).read()
    h = re.search(r"Z_(\d+), multisets of (\d+)\.\.(\d+) elements, mode (\w+), step (\d+), offset (\d+)", s)
    n, lo, hi, mode, step = int(h.group(1)), int(h.group(2)), int(h.group(3)), h.group(4), int(h.group(5))
    c = sum(int(a.group(2)) for a in re.finditer(r"m = +(\d+): (\d+) multisets", s))
    groups.add(n)
    if mode == "all":
        k = "every multiset (not only those with 0)"
    elif step > 1 and not re.search(r"_b[01]\.out$", f):
        k = "sampled (one size further, every k-th multiset that contains 0)"
    else:
        k = "complete, multisets that contain 0"
    tot[k] += c
    rows.append((n, lo, hi, mode, step, c, k.split(",")[0].split(" (")[0]))
print("1. exh_full.py: %d multisets on %d groups: %s" % (sum(tot.values()), len(groups), sorted(groups)))
for k, v in tot.items():
    print("     %-70s %9d" % (k, v))
print("   (runs split in two halves, *_b0/*_b1, are complete together; listed by group:)")
for n in sorted(groups):
    print("     Z_%-4d" % n, "; ".join("m %d..%d %s%s: %d" % (lo, hi, mode, "" if step == 1 else " step %d" % step, c) for (nn, lo, hi, mode, step, c, k) in rows if nn == n))

# ---- 2. Z_9, every multiset of 14, 16, .., 24 elements ----
z9 = {}
for f in ["../z9_14.out", "../z9_16.out", "../z9_18.out", "../z9_20a.out", "../z9_20b.out", "../z9_22_h0.out", "../z9_22_h1.out"] + sorted(glob.glob("../z9_24_p?.out")):
    s = open(f).read()
    m = int(re.search(r"m = (\d+):", s).group(1))
    rep = int(re.search(r"multisets represented: (\d+)", s).group(1))
    cl = int(re.search(r"classes done: (\d+)", s).group(1))
    z9.setdefault(m, [0, 0])
    z9[m][0] += rep
    z9[m][1] += cl
print("2. Z_9 through coefficient vectors, one multiset of each class under the affine maps:")
for m in sorted(z9):
    print("     m = %d: %d multisets (C(m+8,8) = %d) in %d classes" % (m, z9[m][0], math.comb(m + 8, 8), z9[m][1]))
    assert z9[m][0] == math.comb(m + 8, 8)
print("     together %d multisets in %d classes; sizes covered: %s (even sizes only)" % (sum(v[0] for v in z9.values()), sum(v[1] for v in z9.values()), sorted(z9)))

# ---- 3. attained.py ----
a = sum(int(re.search(r"seed \d+: (\d+) multisets", open(f).read()).group(1)) for f in sorted(glob.glob("../attained_*.out")))
print("3. multisets built so that Lemma L is attained at one level:", a)

# ---- 4. the plain numbers of (C) ----
by = {}
for d in range(3, 2000, 2):
    by.setdefault(mu(d), []).append(d)
print("4. odd d with mu(d) = 2:", by[2], "; = 4:", by[4], "; = 6:", by[6], "(%d of them)" % len(by[6]))


def A(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


def Wm(m):
    return sum(Fraction(A(t) - A(t - 2), 2 ** t) for t in range(2, m, 2))


W1000 = sum(Fraction(A(t) - A(t - 2), 2 ** t) for t in range(2, 1001, 2))
print("   W: sum up to mu = 1000 is %.12f; less than 0.845: %s; 1 - W = %.6f (more than 15 in 100: %s)" % (float(W1000), W1000 + Fraction(1, 10 ** 20) < Fraction(845, 1000), float(1 - W1000), 1 - W1000 > Fraction(15, 100)))
c = lambda k: Fraction(math.comb(k, k // 2), 2 ** k)
marg = {}
for m in range(2, 401, 2):
    s = c(m) + Wm(m)
    if m >= 14:
        s = s - Fraction(1, 4) + Fraction(5, 32)
    marg[m] = 1 - s
mm = min(marg, key=lambda m: marg[m])
print("   even m <= 400, the proof's count (5/32 at d = 3 from m = 14): least margin below 1 is %s at m = %d; six sums for m <= 12: %s" % (marg[mm], mm, [str(1 - marg[m]) for m in range(2, 13, 2)]))
print("   the proof's own bound for m >= 14 is 0.961, margin 0.039 = %.1f parts in 1,024; 23/1024 = %.5f" % (0.039 * 1024, 23 / 1024))

# ---- 5. multisets counted twice in the 3,099,711 ----
twice = sum(math.comb(9 + m - 2, m - 1) for m in range(1, 9)) + sum(math.comb(15 + m - 2, m - 1) for m in range(1, 6))
allruns = tot["every multiset (not only those with 0)"]
print("5. the two runs with every multiset (Z_9 up to 8 elements, Z_15 up to 5) hold %d multisets, of which %d contain 0 and are in the other runs too;" % (allruns, twice))
print("   different multisets: %d - %d = %d; of them %d complete (with 0), %d sampled, %d without 0" % (sum(tot.values()), twice, sum(tot.values()) - twice,
      tot["complete, multisets that contain 0"], tot["sampled (one size further, every k-th multiset that contains 0)"], allruns - twice))

# ---- 6. "one factor can divide the mask for half of all signings, and several factors at once" ----
from rlib import bad_all
for B, n in (([0, 15], 45), ([0, 5], 15)):
    bad = bad_all(B, n)
    print("6. %s on Z_%d: share of the signings with Phi_d | S, for d | n: %s; their sum %s" % (B, n, {d: str(Fraction(int(v.sum()), len(v))) for d, v in bad.items()}, sum(Fraction(int(v.sum()), len(v)) for v in bad.values())))
