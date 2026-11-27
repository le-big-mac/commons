# Collects the numbers quoted in audit.md from the output files of this folder (nothing is computed here).
import re, os, json, glob
H = os.path.dirname(os.path.abspath(__file__))


def rd(name):
    p = os.path.join(H, name)
    return open(p).read() if os.path.exists(p) else ''


print("== t0 self-test")
print(rd('t0_selftest.out').strip().split('\n\n')[0])

print("\n== t1 exists_signs, main")
s = rd('t1_signs_main.out')
rows = re.findall(r'n= *(\d+) S= *(\d+) (full |quick) multisets= *(\d+) all-plus-fails= *(\d+) without-good-signing= *(\d+) max-index-of-first-good=(\d+)', s)
ns = sorted({int(r[0]) for r in rows})
print("moduli:", len(ns), ns)
print("quick: multisets", sum(int(r[3]) for r in rows if r[2] == 'quick'), "all-plus fails", sum(int(r[4]) for r in rows if r[2] == 'quick'),
      "without good signing", sum(int(r[5]) for r in rows if r[2] == 'quick'))
print("full : multisets", sum(int(r[3]) for r in rows if r[2] == 'full '), "all-plus fails", sum(int(r[4]) for r in rows if r[2] == 'full '),
      "without good signing", sum(int(r[5]) for r in rows if r[2] == 'full '))
print("largest index of the first good signing:", max(int(r[6]) for r in rows))
print("bounds S (quick) by n:", ", ".join(f"{r[0]}:{r[1]}" for r in rows if r[2] == 'quick'))
print("bounds S (full) by n:", ", ".join(f"{r[0]}:{r[1]}" for r in rows if r[2] == 'full '))
m = re.search(r'TOTAL.*', s)
print(m.group(0) if m else 'no TOTAL line')
fr = re.findall(r'n= *(\d+) S= *\d+ full .*fewest-good-signings-by-size=(\S+)', s)
worst = {}
for n, lst in fr:
    for t, x in enumerate(lst.split(','), 1):
        a, b = x.split('/')
        if t not in worst or int(a) < worst[t][0]:
            worst[t] = (int(a), int(b), int(n))
print("fewest good signings (first sign fixed +), over all moduli, by size:", ", ".join(f"{t}: {a}/{b} (n={n})" for t, (a, b, n) in sorted(worst.items())))

print("\n== t1 control")
s = rd('t1_signs_control.out')
for r in re.findall(r'n= *(\d+) S= *(\d+) quick multisets= *(\d+) all-plus-fails= *(\d+) without-good-signing= *(\d+)', s):
    print("  n", r[0], "S", r[1], "multisets", r[2], "without good signing", r[4])

print("\n== t1b the paper's construction")
m = re.search(r'TOTAL.*', rd('t1b_construction.out'))
print(m.group(0) if m else '')

for name in ['t2_lift2_main.out', 't2_lift2_deep_partial.out', 't2_lift2_control.out']:
    print("\n==", name)
    s = rd(name)
    rows = re.findall(r'N= *(\d+) 2N= *\d+ new divisors=\[[0-9, ]*\] S= *(\d+) multisets= *(\d+) all-low-fails= *(\d+) without-lift= *(\d+) max-index-of-first-good-lift=(\d+) old-divisor-disagreements=(\d+)', s)
    print("values of N:", len(rows), "from", min(int(r[0]) for r in rows), "to", max(int(r[0]) for r in rows))
    print("multisets", sum(int(r[2]) for r in rows), "all-low fails", sum(int(r[3]) for r in rows), "without lift", sum(int(r[4]) for r in rows),
          "largest index of first good lift", max(int(r[5]) for r in rows), "old-divisor disagreements", sum(int(r[6]) for r in rows))
    print("bounds S by N:", ", ".join(f"{r[0]}:{r[1]}" for r in rows))

print("\n== t2b lifts for a general factor s")
s = rd('t2b_lifts_main.out')
rows = re.findall(r'N= *(\d+) s= *(\d+) M= *(\d+) new divisors: *\d+ +S= *(\d+) multisets= *(\d+) all-low-fails= *(\d+) without-lift= *(\d+) most-lifts-tried=(\d+)', s)
print("pairs:", len(rows), "largest M:", max(int(r[2]) for r in rows), "multisets", sum(int(r[4]) for r in rows), "all-low fails",
      sum(int(r[5]) for r in rows), "without lift", sum(int(r[6]) for r in rows), "most lifts tried", max(int(r[7]) for r in rows))
print("even s:", sum(1 for r in rows if int(r[1]) % 2 == 0), "pairs; odd s:", sum(1 for r in rows if int(r[1]) % 2 == 1))
print("S range:", min(int(r[3]) for r in rows), "..", max(int(r[3]) for r in rows))

print("\n== t3 census")
tot = 0
groups = []
for f in sorted(glob.glob(os.path.join(H, 'census', 'M*.json')), key=lambda f: int(os.path.basename(f)[1:-5])):
    c = json.load(open(f))
    tot += c['nodes']
    groups.append((c['M'], c['S']))
print("groups:", len(groups), "multisets in all:", tot)
print("bound S by M:", ", ".join(f"{M}:{S}" for M, S in groups))

print("\n== t3 compare")
s = rd('t3_compare.out')
for line in s.split('\n'):
    if re.match(r'^(two|odd|mul|none) *:', line) or line.startswith('all pairs'):
        print(line)
rows = re.findall(r'N= *(\d+) s= *(\d+) M= *(\d+) (\S+) +S= *(\d+) multisets: (\d+) on Z_N, (\d+) on Z_M; sets P with a nonempty side: *(\d+) of *(\d+); P where the two sets differ: (\d+); reduction inconsistencies: (\d+)', s)
for kind in ['two', 'odd', 'mul']:
    rk = [r for r in rows if kind in r[3].split('+')]
    print(kind, ": pairs", len(rk), "; largest N", max(int(r[0]) for r in rk), "; largest M", max(int(r[2]) for r in rk), "; S from", min(int(r[4]) for r in rk),
          "to", max(int(r[4]) for r in rk), "; pairs with N > 1:", sum(1 for r in rk if int(r[0]) > 1),
          "; sets P (nonempty side) for N > 1:", sum(int(r[7]) for r in rk if int(r[0]) > 1))
rk = [r for r in rows if 'mul' in r[3].split('+') and int(r[1]) % 2 == 0]
print("mul with s even: pairs", len(rk), "sets P", sum(int(r[7]) for r in rk))
print("distinct larger groups in the pairs of the three kinds:", len({int(r[2]) for r in rows if r[3] != 'none'}))

print("\n== t4 least sizes from the censuses")
s = rd('t4_minsize.out')
agg = {}
for line in s.split('\n'):
    m = re.match(r'^(\d+) (\d+) (\d+) +(\d+) \| Z_(\d+) *\| +(\d+) \((\d+)/(\d+)/(\d+)\) \| +(\d+) \| S= *(\d+) \(base Z_\d+: +(\d+)\) \| +(\d+) \| +(\d+) \| +(\d+) \| +(\d+) \| (\d+)', line)
    if m:
        g = [int(x) for x in m.groups()]
        key = 's=1' if g[3] == 1 else ('s even' if g[3] % 2 == 0 else 's odd>1')
        a = agg.setdefault(key, dict(rows=0, inst=0, exact=0, lifted=0, open=0, bad=0))
        a['rows'] += 1; a['inst'] += g[5]; a['exact'] += g[12]; a['lifted'] += g[13]; a['open'] += g[15]; a['bad'] += g[16]
for k, a in agg.items():
    print(k, a)
m = re.search(r'TOTAL.*', s)
print(m.group(0) if m else '')

t5 = dict(base=0, member=0, optimal=0, notproved=0, lifts=0, liftfail=0, bad=0)
for name in ['t5_cpsat_M28.out', 't5_cpsat_M45.out', 't5_cpsat_M54.out']:
    s = rd(name)
    m = re.search(r'TOTAL (\{.*?\})', s)
    print("\n==", name, m.group(0) if m else '')
    if m:
        for k, v in eval(m.group(1)).items():
            t5[k] += v
    np_ = [re.match(r'^(.*?): Lean (\d+);.*lower bound (\d+)', line) for line in s.split('\n') if 'not proved' in line]
    by = {}
    for mm in np_:
        key = re.search(r'p=(\d+) q=(\d+) n=(\d+)', mm.group(1)).groups()
        by.setdefault(key, []).append(int(mm.group(2)))
    for key, vals in by.items():
        print(f"   least size on the base group not proved in the time limit: p q n = {' '.join(key)}: {len(vals)} instances, Lean values {min(vals)}..{max(vals)}")
print("t5 in all:", t5)

for name in sorted(glob.glob(os.path.join(H, 't6_direct_n*.out'))):
    s = open(name).read()
    print("\n==", os.path.basename(name))
    for line in s.split('\n'):
        if 'not proved in' in line and ' | ' not in line:
            print("  ", line.strip()[:150])
    rows = re.findall(r'^(\d+) (\d+) (\d+) (\d+) \| Z_(\d+) \| census bound S=(\d+) \| instances with Lean value > S: (\d+) \| least = Lean value, proved: (\d+) \| not proved in time: (\d+) \| DISAGREEMENTS: (\d+)', s, re.M)
    print("cases (p q n s):", len(rows), "; with at least one instance beyond the census:", sum(1 for r in rows if int(r[6])))
    for par in ['even', 'odd']:
        rk = [r for r in rows if (int(r[3]) % 2 == 0) == (par == 'even')]
        print("  s", par, ": instances", sum(int(r[6]) for r in rk), "proved equal", sum(int(r[7]) for r in rk), "not proved", sum(int(r[8]) for r in rk),
              "disagreements", sum(int(r[9]) for r in rk))
    m = re.search(r'TOTAL.*', s)
    print(m.group(0) if m else 'no TOTAL line (run not finished or stopped)')
