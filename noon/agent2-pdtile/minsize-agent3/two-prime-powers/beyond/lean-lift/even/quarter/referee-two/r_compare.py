#!/usr/bin/env python3
"""Referee: compare (1) the author's lo2_exact_46.out with r_tables_46.out, field by field, as exact fractions;
(2) the tables printed in result.md (sections 4 and 5) with the referee's outputs; (3) PP_p(m) >= exact U_p(m)."""
import re, sys, glob
from fractions import Fraction as F
import r_tables as RT

TWO = "/home/agent3/lean/lift-check/even/quarter/two/"
diff = 0

# ---- (1)
def parse(fn, mine):
    out = {}
    for line in open(fn):
        if line.startswith('#') or '|' not in line:
            continue
        f = [x.strip() for x in line.split('|')]
        m = int(f[0])
        lvl0 = F(f[1]); pp = F(f[2].replace('*', '').strip()); comp = F(f[3].split()[0]); t = F(f[4].split('=')[0].strip())
        det = dict((int(a), F(b)) for a, b in (x.split(':') for x in f[6].split()))
        out[m] = (lvl0, pp, comp, t, det)
    return out

a = parse(TWO + "lo2_exact_46.out", False); b = parse("r_tables_46.out", True)
n = 0
for m in sorted(set(a) | set(b)):
    if m not in a or m not in b:
        print("missing m", m); diff += 1; continue
    for i, name in enumerate(["level 0", "prime powers", "COMP", "T2"]):
        n += 1
        if a[m][i] != b[m][i]:
            diff += 1; print("DIFFERENT m=%d %s: author %s, referee %s" % (m, name, a[m][i], b[m][i]))
    for p in sorted(set(a[m][4]) | set(b[m][4])):
        n += 1
        if a[m][4].get(p) != b[m][4].get(p):
            diff += 1; print("DIFFERENT m=%d prime %d: author %s, referee %s" % (m, p, a[m][4].get(p), b[m][4].get(p)))
print("(1) lo2_exact_46.out against r_tables_46.out: m = %d..%d, %d numbers compared, differences so far: %d" % (min(b), max(b), n, diff))
print("    largest T2 for 9 <= m <= 46: %s at m=%d; largest for odd m >= 5: %s; m with T2 = 3/8: %s; m with T2 > 3/8: %s" % (
    max(b[m][3] for m in b if m >= 9), max((b[m][3], m) for m in b if m >= 9)[1], max(b[m][3] for m in b if m >= 5 and m % 2),
    [m for m in b if b[m][3] == F(3, 8)], [m for m in b if b[m][3] > F(3, 8)]))
second = sorted(((F(3, 8) - b[m][3]), m) for m in b)[:6]
print("    thinnest margins:", ", ".join("m=%d: %.6f" % (m, float(x)) for x, m in second))

# ---- (2) the tables in result.md
text = open(TWO + "result.md").read().split("\n")
tree = {}
for fn in glob.glob("r_tree_*.out"):
    for line in open(fn):
        mm = re.match(r'p=(\d+) m=(\d+) depth=(\d+) ndist=\d+ T=(\S+) U=(\S+)', line)
        if mm:
            p, m, dep = int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
            assert dep == (m - 1) // (p - 1)
            tree[(p, m)] = (F(mm.group(4)), F(mm.group(5)))
n2 = 0
for line in text:
    f = [x.strip() for x in line.split('|')]
    if len(f) > 3 and f[1] in ("T_3(m)", "U_3(m)", "U_5(m)", "U_7(m)"):
        p = int(f[1][2]); which = 0 if f[1][0] == 'T' else 1
        for m, cell in zip(range(3, 17), f[2:16]):
            if cell == "":
                continue
            n2 += 1
            if (p, m) not in tree or tree[(p, m)][which] != F(cell):
                diff += 1; print("DIFFERENT section 4 table %s m=%d: text %s, referee %s" % (f[1], m, cell, tree.get((p, m))))
# the sentence U_11 = ..., U_13 = ...
for p, m0, vals in ((11, 11, "1/1024 0 3/4096 0 5/8192 0"), (13, 13, "1/4096 0 3/16384 0")):
    for m, v in zip(range(m0, 17), vals.split()):
        n2 += 1
        if tree[(p, m)][1] != F(v):
            diff += 1; print("DIFFERENT U_%d(%d)" % (p, m))
# U_TEXT typed in r_tables against the tree outputs
for p in RT.U_TEXT:
    for m, v in RT.U_TEXT[p].items():
        n2 += 1
        if tree.get((p, m), (None, None))[1] != F(v):
            diff += 1; print("DIFFERENT U table p=%d m=%d: %s vs %s" % (p, m, v, tree.get((p, m))))
# odd m: 2^(2-p) c_(m-p+1)
for (p, m), (T, U) in tree.items():
    if m % 2 == 1 and U != F(1, 2 ** (p - 2)) * RT.c(m - p + 1):
        diff += 1; print("pattern fails", p, m)
    if m % 2 == 0 and T < RT.c(m):
        diff += 1; print("T below level 0", p, m)
print("(2a) section 4: %d table entries compared with the referee's tree program (%d pairs (p, m) computed); differences so far: %d" % (n2, len(tree), diff))
print("     T_p(m) <= T_3(m) for p = 5, 7, 11, 13, m <= 16:", all(tree[(p, m)][0] <= tree[(3, m)][0] for (p, m) in tree if p > 3 and m <= 16))
n3 = 0
for line in text:
    f = [x.strip() for x in line.split('|')]
    if len(f) >= 12 and re.fullmatch(r'\d+', f[1] or 'x'):
        m = int(f[1])
        for i, name in enumerate(["level 0", "prime powers", "COMP", "T2"]):
            n3 += 1
            if F(f[2 + i]) != b[m][i]:
                diff += 1; print("DIFFERENT section 5 table m=%d %s: text %s, referee %s" % (m, name, f[2 + i], b[m][i]))
    for i in range(len(f) - 1):
        if re.fullmatch(r'\d+', f[i]) and re.fullmatch(r'0\.\d{6}', f[i + 1]):
            m = int(f[i]); n3 += 1
            if "%.6f" % float(b[m][3]) != f[i + 1]:
                diff += 1; print("DIFFERENT section 5 table m=%d: text %s, referee %.6f" % (m, f[i + 1], float(b[m][3])))
print("(2b) section 5: %d table entries compared; differences so far: %d" % (n3, diff))

# ---- (3)
n4 = 0; low = 0; eq = 0
for (p, m), (T, U) in sorted(tree.items()):
    pp = RT.PP(p, m); n4 += 1
    if pp < U:
        low += 1; print("PP BELOW EXACT p=%d m=%d: PP=%s U=%s" % (p, m, pp, U))
    if pp == U:
        eq += 1
print("(3) PP_p(m) >= exact U_p(m): %d pairs, PP below exact in %d, equal in %d" % (n4, low, eq))
print("TOTAL DIFFERENCES:", diff + low)
