# z9_all.py m [step offset [budget]] -- every multiset of m elements on Z_9 up to the 54 affine maps x -> u x + c (u a unit),
# which do not change the number of good signings (X^c is a unit modulo Phi_d, and X -> X^u permutes the roots of
# Phi_d).  Good signings counted exactly through the coefficient vectors (division by Phi_1, Phi_3, Phi_9).
# For each multiset also: contraction (deepest first), Corollary L for the contracted multiset, the level d = 3
# against 5/32 (m >= 14, all three classes modulo 3 occupied), and the stated bound.
import sys, math, time, itertools
from fractions import Fraction
import numpy as np
from rlib import good_count_grid, contract_all, divisors, mu, xtable, all_levels_full, nprime

m = int(sys.argv[1])
step = int(sys.argv[2]) if len(sys.argv) > 2 else 1
offset = int(sys.argv[3]) if len(sys.argv) > 3 else 0
budget = float(sys.argv[4]) if len(sys.argv) > 4 else 270.0
t0 = time.time()
n = 9
maps = [[(u * x + c) % 9 for x in range(9)] for u in (1, 2, 4, 5, 7, 8) for c in range(9)]


def canon(cv):
    return min(tuple(cv[p[x]] for x in range(9)) for p in maps)


# multiplicity vectors with c_0 the largest (a translation brings a largest multiplicity to 0), then canonical forms
def vecs(m):
    def rec(pos, left, top, cur):
        if pos == 9:
            if left == 0:
                yield tuple(cur)
            return
        for v in range(min(left, top), -1, -1):
            if v * (9 - pos) + 0 < left - top * (9 - pos - 1) and False:
                continue
            cur.append(v)
            yield from rec(pos + 1, left - v, top, cur)
            cur.pop()
    for c0 in range(m, 0, -1):
        if c0 * 9 < m:
            break
        yield from rec(1, m - c0, c0, [c0])


orbits = set()
nvec = 0
for cv in vecs(m):
    nvec += 1
    orbits.add(canon(cv))
orbits = sorted(orbits)
print("Z_9, m = %d: %d multiplicity vectors with c_0 largest, %d classes under the affine maps (C(m+8,8) = %d multisets); step %d offset %d"
      % (m, nvec, len(orbits), math.comb(m + 8, 8), step, offset))
# check of the orbit count by Burnside would need more code; instead the orbit sizes are summed below.
maps_arr = maps


def orbit_size(cv):
    return len({tuple(cv[p[x]] for x in range(9)) for p in maps})


def A_formula(t):
    r = 1
    for p in range(3, t + 2, 2):
        if all(p % q for q in range(3, int(p ** 0.5) + 1, 2)):
            r *= 1 + t // (p - 1)
    return r


WUP = sum(Fraction(A_formula(t) - A_formula(t - 2), 2 ** t) for t in range(2, 401, 2)) + Fraction(1, 10 ** 9)
SIX = {2: Fraction(1, 2), 4: Fraction(3, 8), 6: Fraction(3, 16), 8: Fraction(9, 128), 10: Fraction(11, 256), 12: Fraction(23, 1024)}


def stated_ok(m, f):
    if m % 2 == 1:
        return f > 1 - WUP
    if m <= 12:
        return f >= SIX[m]
    return f > Fraction(39, 1000)


def bad_counts_grid(B, n):
    """weighted numbers of signings bad at each d | n, and good, through the coefficient vectors."""
    mult = {}
    for x in B:
        mult[x] = mult.get(x, 0) + 1
    supp = sorted(mult)
    A = np.zeros((1, 0), dtype=np.int64)
    W = np.ones(1, dtype=np.int64)
    for x in supp:
        cc = mult[x]
        vals = np.arange(-cc, cc + 1, 2, dtype=np.int64)
        wts = np.array([math.comb(cc, j) for j in range(cc + 1)], dtype=np.int64)
        A = np.concatenate([np.repeat(A, len(vals), axis=0), np.tile(vals, A.shape[0])[:, None]], axis=1)
        W = np.repeat(W, len(vals)) * np.tile(wts, W.shape[0])
    anyb = np.zeros(A.shape[0], dtype=bool)
    out = {}
    for d in divisors(n):
        b = ~(A @ xtable(n, d)[supp]).any(axis=1)
        out[d] = int(W[b].sum())
        anyb |= b
    return out, int(W[~anyb].sum())


full = 1 << m
viol = {"F": 0, "D": 0, "L3": 0, "C2": 0, "C3": 0, "E": 0}
done = 0
total_size = 0
best = (Fraction(2), None)
best3 = (Fraction(2), None)
max3 = (Fraction(0), None)
attD = 0
ends = {}
cm = Fraction(math.comb(m, m // 2), 2 ** m) if m % 2 == 0 else Fraction(0)
stopped = False
for k, cv in enumerate(orbits):
    if k % step != offset:
        continue
    if time.time() - t0 > budget:
        stopped = True
        break
    B = [x for x in range(9) for _ in range(cv[x])]
    bc, g = bad_counts_grid(B, 9)
    f = Fraction(g, full)
    done += 1
    total_size += orbit_size(cv)
    if not stated_ok(m, f):
        viol["F"] += 1
        print("VIOLATION F", B, f)
    if f < best[0]:
        best = (f, cv)
    occ3 = all(any(cv[x] for x in range(9) if x % 3 == r) for r in range(3))
    if occ3:
        if f < best3[0]:
            best3 = (f, cv)
        p3 = Fraction(bc[3], full)
        if p3 > max3[0]:
            max3 = (p3, cv)
        if m >= 14 and p3 > Fraction(5, 32):
            viol["L3"] += 1
            print("VIOLATION L3", B, p3)
    Bf, nf, steps = contract_all(B, 9, "deep")
    ends[nf] = ends.get(nf, 0) + 1
    if not all_levels_full(Bf, nf):
        viol["C2"] += 1
    if nprime(m) % nf:
        viol["C3"] += 1
    bcf, gf = bad_counts_grid(Bf, nf) if steps else (bc, g)
    if gf > g:
        viol["E"] += 1
        print("VIOLATION (more good signings for B_flat than for B)", B, Bf, nf)
    bound = cm
    for d, nb in bcf.items():
        if d > 1:
            if nb << mu(d) > full:
                viol["D"] += 1
                print("VIOLATION D", B, Bf, nf, d, nb)
            if nb << mu(d) == full:
                attD += 1
            bound += Fraction(1, 2 ** mu(d))
    if m % 2 == 0 and m >= 14 and nf % 3 == 0:
        bound += Fraction(5, 32) - Fraction(1, 4)
    if Fraction(full - gf, full) > bound:
        viol["E"] += 1
        print("VIOLATION E", B, Bf, nf)
print("classes done: %d of %d (multisets represented: %d)%s" % (done, len(range(offset, len(orbits), step)), total_size, "  STOPPED AT THE TIME BUDGET" if stopped else ""))
print("ends of the contraction:", dict(sorted(ends.items())), "; Corollary L attained %d times" % attD)
print("least fraction of good signings: %s = %.5f at multiplicities %s" % (best[0], float(best[0]), best[1]))
if best3[1]:
    print("with all three classes modulo 3 occupied: %s = %.5f at %s" % (best3[0], float(best3[0]), best3[1]))
    print("largest fraction bad at d = 3 (all three classes occupied): %s = %.5f at %s   (5/32 = 0.15625)" % (max3[0], float(max3[0]), max3[1]))
print("violations:", viol, "  seconds %.0f" % (time.time() - t0))
