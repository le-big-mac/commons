"""Referee's analysis of the histogram produced by enum.c (or mitm.c): for every realised (pattern, size)
 - decide pd-tiling by |A| == D+(Z_A) (exact rationals; Prop. 1 of flatness.md), and separately (lpdef.py) by the
   LP of the definition;
 - check (T1), (T2);
 - compare with brute-force tiling counts (when present);
 - check every counting step of Section 5 that can be read off (pattern, size);
 - classify the pattern into the bullets of Section 5 and check the upper bound each bullet uses against exact D+.
usage: analyse.py p0 p1 p2 histfile
"""
import sys
from fractions import Fraction as Fr
from collections import defaultdict
sys.path.insert(0, '/tmp/agent2_referee3')
from dplus import dplus, describe

p = tuple(int(a) for a in sys.argv[1:4])
M = p[0] * p[1] * p[2]
histfile = sys.argv[4]
PB = {frozenset((0, 1)): 3, frozenset((0, 2)): 4, frozenset((1, 2)): 5}


def EPt(mask):
    E = {w for w in range(3) if mask >> w & 1}
    P = {pr for pr, b in PB.items() if mask >> b & 1}
    return E, P, mask >> 6 & 1


def T1(mask, n):
    E, P, t = EPt(mask)
    k = 1
    for w in E:
        k *= p[w]
    return n == k


def T2(mask):
    E, P, t = EPt(mask)
    for a in E:
        for b in E:
            if a < b and frozenset((a, b)) not in P:
                return False
    if len(E) == 3 and not t:
        return False
    return True


def bullet(mask):
    """Classification of a pattern into the bullets of Section 5.
    Returns (label, U, L, verdict) where U is the upper bound on D+ the bullet invokes (None if none),
    L a lower bound on |A| valid for every set with exactly this pattern as claimed by the bullet (None if none),
    verdict in {'T1T2', 'contradiction', 'T1T2-or-contradiction'}; plus Lstrict flag folded into L."""
    E, P, t = EPt(mask)
    pr = lambda a, b: frozenset((a, b)) in P
    if len(E) == 3:
        return ("|E|=3", M, M, "T1T2")
    if len(E) == 2:
        x, y = sorted(E)
        U = p[x] * p[y]                       # Lemma 1, U = {x,y}
        if pr(x, y):
            return ("E={x,y}; {x,y} in P", U, U, "T1T2")
        if not t:
            return ("E={x,y}; {x,y} not in P; t=0 (Lemma 2)", max(p[x], p[y]), U, "contradiction")
        return ("E={x,y}; {x,y} not in P; t=1 (Lemma 5)", U, U + 1, "contradiction")   # Lemma 5: n = p_x p_y impossible
    if len(E) == 1:
        (x,) = E
        y, z = [w for w in range(3) if w != x]
        if not pr(y, z):
            return ("E={x}; {y,z} not in P (Lemma 1, U={x})", p[x], p[x], "T1T2")
        U = p[x] * min(p[y], p[z])
        if pr(x, y) or pr(x, z):
            # bullets 1 and 2; if both pairs are present both bullets apply, take the stronger lower bound
            Ls = []
            if pr(x, y):
                Ls.append(p[z] * p[x] + p[y])
            if pr(x, z):
                Ls.append(p[y] * p[x] + p[z])
            return ("E={x}; {y,z} in P; a second pair in P", U, max(Ls), "contradiction")
        if not t:
            U2 = min(U, max(p[x], p[y]), max(p[x], p[z]))    # Lemma 2 twice
            if p[x] > p[y] or p[x] > p[z]:
                return ("E={x}; P={{y,z}}; t=0; p_x not smallest (n<=p_x)", p[x], p[y] + p[z], "T1T2-or-contradiction")
            return ("E={x}; P={{y,z}}; t=0; p_x smallest", U2, p[y] + p[z], "contradiction")
        return ("E={x}; P={{y,z}}; t=1 (Lemma 4b)", U, U + 1, "contradiction")
    # E empty
    if mask == 0:
        return ("E=0; Z_A empty", 1, 1, "T1T2")
    if not P:
        return ("E=0; P=0; t=1 (Lemma 4b)", min(p), min(p) + 1, "contradiction")
    common = set.intersection(*[set(q) for q in P]) if P else set()
    if common:
        x = min(common, key=lambda w: p[w])       # any common index will do; Lemma 1 with U = {x}
        L = max(p[a] + p[b] for a, b in [tuple(q) for q in P])   # Lemma 3 for a pair of P
        return ("E=0; 1 or 2 pairs", p[x], L, "contradiction")
    pi = sorted(p)[0] * sorted(p)[1]
    return ("E=0; P = all three pairs", pi, pi + 1, "contradiction")


rows = []
tile_present = False
for line in open(histfile):
    if line.startswith('#'):
        continue
    f = line.split()
    mask, n, cnt = int(f[0]), int(f[1]), int(f[2])
    tl = int(f[3]) if len(f) > 3 else None
    if tl is not None:
        tile_present = True
    rows.append((mask, n, cnt, tl))

D = {mask: dplus(p, mask) for mask in range(128)}
by_mask = defaultdict(list)
for mask, n, cnt, tl in rows:
    by_mask[mask].append((n, cnt, tl))

print(f"M = {M}, primes {p}; {len(rows)} realised (pattern, size) classes, {len(by_mask)} realised patterns of 128")
tot = sum(r[2] for r in rows)
print("total subsets counted:", tot)

# ---------------- theorem at this M ----------------
viol = 0
pd_classes = 0
pd_sets = 0
dp_gt_n = 0
tile_mismatch = 0
print("\npd-tiling classes (|A| = D+(Z_A)):")
for mask, n, cnt, tl in rows:
    if D[mask] > n:
        dp_gt_n += 1            # would contradict Prop. 1(i)
    ispd = (D[mask] == n)
    if ispd:
        pd_classes += 1
        pd_sets += cnt
        ok = T1(mask, n) and T2(mask)
        if not ok:
            viol += 1
        print(f"  Z={describe(p, mask):22s} n={n:2d} sets={cnt:8d} T1={T1(mask, n)} T2={T2(mask)}" +
              (f" tiling sets={tl}" if tl is not None else ""))
        if tl is not None and tl != cnt:
            tile_mismatch += 1
    else:
        if tl:
            tile_mismatch += 1
            print(f"  !! non-pd class with tiling sets: Z={describe(p, mask)} n={n} tiles={tl}")
print(f"pd-tiling classes: {pd_classes}, pd-tiling sets: {pd_sets}, classes violating (T1)/(T2): {viol}")
print(f"classes with D+(Z_A) > |A| (would contradict Prop 1(i)): {dp_gt_n}")
if tile_present:
    print(f"classes where [pd-tiling] and [all sets tile / no set tiles] disagree: {tile_mismatch}")
    print("total tiling sets (brute force):", sum(r[3] for r in rows))

# ---------------- bullets of Section 5 ----------------
print("\nSection 5 bullets: for every one of the 128 patterns, exact D+ against the bound the bullet invokes,")
print("and the bullet's lower bound against the smallest realised |A| (min n) with exactly that pattern.")
agg = defaultdict(lambda: dict(patterns=0, realised=0, sets=0, Ufail=0, Lfail=0, concl_fail=0, tight=0))
for mask in range(128):
    lab, U, L, verdict = bullet(mask)
    a = agg[lab]
    a['patterns'] += 1
    if D[mask] > U:
        a['Ufail'] += 1
        print("   U FAIL", describe(p, mask), lab, "D+ =", D[mask], "U =", U)
    ns = by_mask.get(mask, [])
    if ns:
        a['realised'] += 1
        a['sets'] += sum(c for _, c, _ in ns)
        nmin = min(n for n, _, _ in ns)
        if nmin < L:
            a['Lfail'] += 1
            print("   L FAIL", describe(p, mask), lab, "min n =", nmin, "L =", L)
        if nmin == L:
            a['tight'] += 1
        for n, c, _ in ns:
            if D[mask] == n:
                if verdict == 'contradiction':
                    a['concl_fail'] += 1
                    print("   CONCLUSION FAIL (pd-tiling set in a 'contradiction' bullet)", describe(p, mask), n)
                elif not (T1(mask, n) and T2(mask)):
                    a['concl_fail'] += 1
                    print("   CONCLUSION FAIL (T1/T2)", describe(p, mask), n)
for lab, a in agg.items():
    print(f"  {lab:52s} patterns={a['patterns']:3d} realised={a['realised']:3d} sets={a['sets']:10d} "
          f"U-fail={a['Ufail']} L-fail={a['Lfail']} L-tight={a['tight']} concl-fail={a['concl_fail']}")

# ---------------- individual counting statements, with premise counts ----------------
print("\nCounting statements read off the histogram (premise count = number of sets meeting the premise):")


def stat(name, prem, concl):
    np_, nf, classes = 0, 0, 0
    worst = None
    for mask, n, cnt, tl in rows:
        if prem(mask, n):
            np_ += cnt
            classes += 1
            if not concl(mask, n):
                nf += cnt
                worst = (describe(p, mask), n)
    print(f"  {name:95s} premise sets={np_:10d} classes={classes:4d} violations={nf}" + (f" e.g. {worst}" if worst else ""))


perms = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
for (x, y, z) in perms:
    tag = f"[x,y,z = {p[x]},{p[y]},{p[z]}]"
    if x < y:
        stat(f"Lemma 3 {tag[:-1]} pair only]: {{x,y}} in P, x,y not in E => n >= p_x+p_y",
             lambda m, n: frozenset((x, y)) in EPt(m)[1] and x not in EPt(m)[0] and y not in EPt(m)[0],
             lambda m, n: n >= p[x] + p[y])
        stat(f"Lemma 5 {tag[:-1]} pair only]: n = p_x p_y, x,y in E, t=1 => {{x,y}} in P",
             lambda m, n: n == p[x] * p[y] and x in EPt(m)[0] and y in EPt(m)[0] and EPt(m)[2],
             lambda m, n: frozenset((x, y)) in EPt(m)[1])
        stat(f"  (control) n = p_x p_y, x,y in E, t=0: is {{x,y}} in P forced?  (violations = sets with {{x,y}} not in P)",
             lambda m, n: n == p[x] * p[y] and x in EPt(m)[0] and y in EPt(m)[0] and not EPt(m)[2],
             lambda m, n: frozenset((x, y)) in EPt(m)[1])
    stat(f"S5 E={{x}} {tag}: E={{x}}, {{y,z}},{{x,y}} in P => n >= p_x p_z + p_y",
         lambda m, n: EPt(m)[0] == {x} and frozenset((y, z)) in EPt(m)[1] and frozenset((x, y)) in EPt(m)[1],
         lambda m, n: n >= p[x] * p[z] + p[y])
    stat(f"   weaker premise {tag}: x in E, y,z not in E not required; {{y,z}},{{x,y}} in P, x in E, y not in E",
         lambda m, n: x in EPt(m)[0] and y not in EPt(m)[0] and frozenset((y, z)) in EPt(m)[1] and frozenset((x, y)) in EPt(m)[1],
         lambda m, n: n >= p[x] * p[z] + p[y])
    if y < z:
        stat(f"S5 E={{x}} {tag}: E={{x}}, P={{{{y,z}}}}, t=1 => n > p_x min(p_y,p_z)",
             lambda m, n: EPt(m)[0] == {x} and EPt(m)[1] == {frozenset((y, z))} and EPt(m)[2],
             lambda m, n: n > p[x] * min(p[y], p[z]))
        stat(f"S5 E={{x}} {tag}: x in E, {{y,z}} in P, t=1 => n >= p_x min(p_y,p_z)",
             lambda m, n: x in EPt(m)[0] and frozenset((y, z)) in EPt(m)[1] and EPt(m)[2],
             lambda m, n: n >= p[x] * min(p[y], p[z]))
        stat(f"S5 E={{x}} {tag}: E={{x}}, P={{{{y,z}}}}, t=0 => n >= p_y+p_z (Lemma 3)",
             lambda m, n: EPt(m)[0] == {x} and EPt(m)[1] == {frozenset((y, z))} and not EPt(m)[2],
             lambda m, n: n >= p[y] + p[z])
        stat(f"   of which with n = p_x (the surviving case when p_x is not the smallest)",
             lambda m, n: EPt(m)[0] == {x} and EPt(m)[1] == {frozenset((y, z))} and not EPt(m)[2] and n == p[x],
             lambda m, n: True)
pm = min(p)
pi = sorted(p)[0] * sorted(p)[1]
stat("S5 E=0: Z_A = {M} => n > smallest prime",
     lambda m, n: m == 64, lambda m, n: n > pm)
stat("   stronger: t=1 and n <= smallest prime => smallest prime in E",
     lambda m, n: EPt(m)[2] and n <= pm, lambda m, n: p.index(pm) in EPt(m)[0])
stat("   stronger: t=1 and n < largest prime => all three... {x,y} in P for the two smaller primes",
     lambda m, n: EPt(m)[2] and n < max(p), lambda m, n: frozenset(w for w in range(3) if p[w] != max(p)) in EPt(m)[1])
stat("S5 E=0: 1 or 2 pairs in P => n >= p_x+p_y for each pair of P (so n > the common prime)",
     lambda m, n: not EPt(m)[0] and 1 <= len(EPt(m)[1]) <= 2,
     lambda m, n: all(n >= p[a] + p[b] for a, b in [tuple(q) for q in EPt(m)[1]]))
stat("S5 E=0: P = all three pairs => n > product of the two smallest primes",
     lambda m, n: not EPt(m)[0] and len(EPt(m)[1]) == 3, lambda m, n: n > pi)
stat("   (control) all three pairs in P, E arbitrary",
     lambda m, n: len(EPt(m)[1]) == 3, lambda m, n: n > pi)
stat("E={x,y}: p_x p_y | n always (Prop 1(iii))",
     lambda m, n: True, lambda m, n: n % (lambda E: __import__('math').prod(p[w] for w in E))(EPt(m)[0]) == 0)
