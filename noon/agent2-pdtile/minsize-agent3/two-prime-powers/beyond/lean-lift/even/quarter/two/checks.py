#!/usr/bin/env python3
"""checks of the numbers quoted in result.md against the outputs (text processing only)"""
import re, ast, sys
from fractions import Fraction
# largest bad share met per m in tests.out, tests2.out
best = {}
for fn in ('tests.out', 'tests2.out'):
    for line in open(fn):
        mm = re.search(r"largest bad share: (\{.*\}) NO FAILURE", line)
        if mm:
            d = ast.literal_eval(mm.group(1))
            for m, v in d.items():
                f = Fraction(v[0])
                if f > best.get(m, (Fraction(0),))[0]:
                    best[m] = (f, v[1], v[2])
brief = dict(zip(range(3, 13), map(Fraction, "1/4 3/8 1/4 11/32 7/32 39/128 3/16 145/512 171/1024 267/1024".split())))
for m in sorted(best):
    print("m=%d largest bad share met %s on Z_%d %s ; brief's list %s ; above it: %s" % (m, best[m][0], best[m][1], best[m][2], brief.get(m), best[m][0] > brief.get(m, 1)))
# table of section 5 against lo2_exact_46.out
rows = {}
for line in open('lo2_exact_46.out'):
    f = [x.strip() for x in line.split('|')]
    if len(f) >= 6 and f[0].isdigit():
        rows[int(f[0])] = (Fraction(f[1]), Fraction(f[2].replace('*', '').strip()), Fraction(f[3]), Fraction(f[4].split('=')[0].strip()), f[5])
txt = open('result.md').read()
sec5 = txt[txt.index('## 5. Theorem A'):txt.index('## 6. Theorem B')]
bad = 0
for line in sec5.splitlines():
    if not line.startswith('|') or '---' in line or 'level 0' in line:
        continue
    cells = [x.strip() for x in line.strip().strip('|').split('|')]
    # first block: m, level0, sum U, COMP, T2
    if cells[0].isdigit():
        m = int(cells[0]); want = rows[m]
        got = tuple(Fraction(x) for x in cells[1:5])
        if got != want[:4]:
            bad += 1; print("MISMATCH row", m, got, want[:4])
    for i in (6, 9):
        if i < len(cells) and cells[i].isdigit():
            m = int(cells[i]); val = float(cells[i + 1])
            if abs(val - float(rows[m][3])) > 5.1e-7:
                bad += 1; print("MISMATCH decimal", m, val, float(rows[m][3]))
print("table of section 5: mismatches", bad, "; all rows True:", all(r[4] == 'True' for r in rows.values()), "; m range", min(rows), max(rows))
print("max T2 for m>=9:", max((float(rows[m][3]), m) for m in rows if m >= 9), " max odd m>=5:", max((float(rows[m][3]), m) for m in rows if m >= 5 and m % 2))
# table of section 4 against ptree outputs
import glob
U, T = {}, {}
for fn in glob.glob('ptree_*.out'):
    for line in open(fn):
        mm = re.match(r'p=(\d+) m=(\d+) depth=(\d+) .*T_p\(m\)=(\S+)\s+U_p\(m\)=(\S+)', line)
        if mm:
            p, m = int(mm.group(1)), int(mm.group(2))
            T[(p, m)] = Fraction(mm.group(4)); U[(p, m)] = Fraction(mm.group(5))
sec4 = txt[txt.index('## 4. Powers of one prime'):txt.index('## 5. Theorem A')]
bad = 0
for line in sec4.splitlines():
    for name, tab, p in (('| T_3(m)', T, 3), ('| U_3(m)', U, 3), ('| U_5(m)', U, 5), ('| U_7(m)', U, 7)):
        if line.startswith(name):
            cells = [x.strip() for x in line.strip().strip('|').split('|')][1:]
            for m, x in zip(range(3, 17), cells):
                if x == '':
                    continue
                if Fraction(x) != tab[(p, m)]:
                    bad += 1; print("MISMATCH", name, m, x, tab[(p, m)])
print("table of section 4: mismatches", bad)
print("U_11:", [str(U[(11, m)]) for m in range(11, 17)], "U_13:", [str(U[(13, m)]) for m in range(13, 17)])
print("T_p <= T_3 for p > 3:", all(T[(p, m)] <= T[(3, m)] for (p, m) in T if p > 3 and (3, m) in T), "; max T_3:", max((T[(3, m)], m) for m in range(3, 17)))
print("odd m pattern U_p = 2^(2-p) c_(m-p+1):", all(U[(p, m)] == Fraction(1, 2 ** (p - 2)) * Fraction(__import__('math').comb(m - p + 1, (m - p + 1) // 2), 2 ** (m - p + 1)) for (p, m) in U if m % 2))
