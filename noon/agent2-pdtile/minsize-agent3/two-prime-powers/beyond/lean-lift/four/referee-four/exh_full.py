# exh_full.py n mmin mmax mode [step [offset]] -- every multiset of mmin..mmax elements on Z_n (mode "zero": those that contain 0,
# which loses nothing: X^c is a unit modulo every Phi_d; mode "all": every multiset), all 2^m signings, exact division.
# With step > 1 only the multisets whose number in the enumeration is offset modulo step are taken.
# For each multiset B:
#  A. Lemma L, first part, on B itself (not contracted): for every d | n, d > 1, and every prime p | d:
#     #{eps : Phi_d | S_eps} <= 2^(m - e), e = sum over occupied groups D at level v_p(d) of min(k_D, p-1).
#  B. Lemma 1(b) of the note: "bad at d" (division) equals "flat on every group at level i" (slices mod Phi_{d''}).
#  C. Contraction (my routine, three orders: deepest first, shallowest first, random): the end B_flat on Z_{n_flat} has
#     (2) a full group at every level of every tree, (3) n_flat | n'_m, (1) every signing good for B_flat is good for B.
#     Also the note's canonical form: deepest-first ends on prod p^{r_p}, r_p = number of levels of B with a full group.
#  D. Corollary L on B_flat: for every d | n_flat, d > 1: #bad at d <= 2^(m - mu(d)).
#  E. Union bound: #not good for B_flat <= 2^m ([m even] c_m + sum_{d | n_flat, d > 1} 2^(-mu(d))).
#  F. The stated bounds for the fraction of good signings of B.
import sys, math, itertools, random, time
from fractions import Fraction
import numpy as np
from rlib import *

n = int(sys.argv[1]); mmin = int(sys.argv[2]); mmax = int(sys.argv[3]); mode = sys.argv[4]
step = int(sys.argv[5]) if len(sys.argv) > 5 else 1
offset = int(sys.argv[6]) if len(sys.argv) > 6 else 0
rng = random.Random(n * 1000 + mmax)
t0 = time.time()


def A_formula(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


WUP = sum(Fraction(A_formula(t) - A_formula(t - 2), 2 ** t) for t in range(2, 401, 2)) + Fraction(1, 10 ** 9)
SIX = {2: Fraction(1, 2), 4: Fraction(3, 8), 6: Fraction(3, 16), 8: Fraction(9, 128), 10: Fraction(11, 256), 12: Fraction(23, 1024)}


def c(k):
    return Fraction(math.comb(k, k // 2), 2 ** k)


def stated_ok(m, frac):
    if m % 2 == 1:
        return frac > 1 - WUP
    if m <= 12:
        return frac >= SIX[m]
    return frac > Fraction(39, 1000)


MU = {}


def mu_c(d):
    if d not in MU:
        MU[d] = mu(d)
    return MU[d]


divs_n = divisors(n)
fac_d = {d: factor(d) for d in divs_n}
print("Z_%d, multisets of %d..%d elements, mode %s, step %d, offset %d" % (n, mmin, mmax, mode, step, offset))
viol = {"A": 0, "B": 0, "C1": 0, "C2": 0, "C3": 0, "Ccanon": 0, "D": 0, "E": 0, "F": 0}
for m in range(mmin, mmax + 1):
    E = signs(m)
    full = 1 << m
    it = itertools.combinations_with_replacement(range(n), m - 1) if mode == "zero" else itertools.combinations_with_replacement(range(n), m)
    cnt = 0; ncontr = 0; attA = 0; attD = 0; nflat_hist = {}; order_diff = 0
    minfrac = (Fraction(2), None); maxratioE = Fraction(0); checksA = checksB = checksD = 0
    minfrac_flat = (Fraction(2), None)
    for idx, tup in enumerate(it):
        if idx % step != offset:
            continue
        B = ([0] + list(tup)) if mode == "zero" else list(tup)
        cnt += 1
        bad = {d: bad_at(B, n, d, E) for d in divs_n}
        anybad = np.zeros(full, dtype=bool)
        for v in bad.values():
            anybad |= v
        good = ~anybad
        ngood = int(good.sum())
        # A, B
        for d in divs_n:
            if d == 1:
                continue
            nb = int(bad[d].sum())
            for p, i in fac_d[d].items():
                e = lemmaL_e(B, p, i)
                checksA += 1
                if nb << e > full:
                    viol["A"] += 1
                    print("VIOLATION A", n, B, d, p, nb, e)
                if nb << e == full:
                    attA += 1
                fl = flat_everywhere(B, n, p, i, d // p ** i, E)
                checksB += 1
                if (fl != bad[d]).any():
                    viol["B"] += 1
                    print("VIOLATION B", n, B, d, p)
        # d = 1: bad iff the signs sum to 0
        if (bad[1] != (E.sum(axis=1) == 0)).any():
            viol["B"] += 1
            print("VIOLATION B (d = 1)", n, B)
        # C, D, E
        seen = set()
        rp = {p: sum(1 for i in range(1, a + 1) if has_full_group(B, p, i)) for p, a in factor(n).items()}
        canon = math.prod(p ** r for p, r in rp.items())
        for order in ("deep", "shallow", "random"):
            Bf, nf, steps = contract_all(B, n, order, rng)
            if order == "deep":
                nflat_hist[nf] = nflat_hist.get(nf, 0) + 1
                if steps:
                    ncontr += 1
                if nf != canon:
                    viol["Ccanon"] += 1
                    print("VIOLATION Ccanon", n, B, nf, canon)
            key = (tuple(Bf), nf)
            if key in seen:
                continue
            if seen:
                order_diff += 1
            seen.add(key)
            if not all_levels_full(Bf, nf):
                viol["C2"] += 1
                print("VIOLATION C2", n, B, Bf, nf)
            if nprime(m) % nf:
                viol["C3"] += 1
                print("VIOLATION C3", n, B, Bf, nf)
            if steps:
                badf = {d: bad_at(Bf, nf, d, E) for d in divisors(nf)}
            else:
                badf = bad
            anyf = np.zeros(full, dtype=bool)
            for v in badf.values():
                anyf |= v
            if (~anyf & anybad).any():
                viol["C1"] += 1
                print("VIOLATION C1", n, B, Bf, nf)
            bound = c(m) if m % 2 == 0 else Fraction(0)
            for d, v in badf.items():
                if d == 1:
                    continue
                nb = int(v.sum())
                checksD += 1
                if nb << mu_c(d) > full:
                    viol["D"] += 1
                    print("VIOLATION D", n, B, Bf, nf, d, nb)
                if nb << mu_c(d) == full:
                    attD += 1
                bound += Fraction(1, 2 ** mu_c(d))
            nbadf = int(anyf.sum())
            if Fraction(nbadf, full) > bound:
                viol["E"] += 1
                print("VIOLATION E", n, B, Bf, nf, nbadf, bound)
            if bound > 0:
                maxratioE = max(maxratioE, Fraction(nbadf, full) / bound)
            ff = Fraction(full - nbadf, full)
            if ff < minfrac_flat[0]:
                minfrac_flat = (ff, (Bf, nf))
        # F
        frac = Fraction(ngood, full)
        if not stated_ok(m, frac):
            viol["F"] += 1
            print("VIOLATION F", n, B, frac)
        if frac < minfrac[0]:
            minfrac = (frac, B)
    print("m = %2d: %d multisets, %d contractible; ends of the deepest-first contraction: %s" % (m, cnt, ncontr, dict(sorted(nflat_hist.items()))))
    print("        A: %d (d, p) checks, bound attained %d times; B: %d checks; D: %d (B_flat, d) checks, attained %d times; other orders gave a different end %d times" % (checksA, attA, checksB, checksD, attD, order_diff))
    print("        least fraction of good signings: %s = %.4f at %s; for a contracted multiset: %s at %s; largest (bad fraction)/(union bound): %.4f" % (minfrac[0], float(minfrac[0]), minfrac[1], minfrac_flat[0], minfrac_flat[1], float(maxratioE)))
    sys.stdout.flush()
print("violations:", viol, "  seconds %.0f" % (time.time() - t0))
