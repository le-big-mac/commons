"""(1) Does sqrt(m) Psi(m) fall along odd m and along even m for 161 <= m <= 3000 (floating point, kappa <= 160 only)?
(2) Totals over the test outputs in this folder (last report line of each file)."""
import math, re, glob
import psi as PSI
P = PSI.pairs_upto(160)
def psif(m):
    t = math.exp(PSI.lncstar(m)) if m % 2 == 0 else 0.0
    for (q, s, pp, nc) in P:
        if q + 2 * s > m: continue
        kap = s + q - 1
        if pp: t += math.exp(-(kap - 1) * math.log(2) + PSI.lncstar(m - 2 * kap + 2))
        if nc: t += nc * math.exp(-kap * math.log(2) + PSI.lncstar(m - 2 * kap))
    return t
v = {m: psif(m) * math.sqrt(m) for m in range(159, 3001)}
for par, nm in ((1, 'odd'), (0, 'even')):
    ms = [m for m in v if m % 2 == par]
    rises = [m for m in ms[1:] if v[m] > v[m - 2] + 1e-13]
    print(f"{nm} m, 159..3000 (floating point): sqrt(m) Psi rises at {rises[:10]}{' ...' if len(rises) > 10 else ''} ({len(rises)} places); value at the end {v[ms[-1]]:.5f}")
tot = dict(multisets=0, fl=0, fl2=0, pos=0, eq=0, ecases=0, fails=0); files = 0
for f in sorted(glob.glob('exh-*.out') + glob.glob('exh2-*.out') + glob.glob('rand-10?.out') + glob.glob('gon-*.out') + ['heavy.out', 'c2more.out', 'beta7.out']):
    lines = [l for l in open(f) if l.startswith('[')]
    if not lines: print("no report line in", f); continue
    l = lines[-1]; files += 1
    g = re.search(r"multisets (\d+); fully live d (\d+) \(two or more primes (\d+); with P > 0: (\d+); m = need: (\d+)\); Lemma B/B\+ max ratio ([\d.]+) \(equalities (\d+).*Lemma E cases (\d+), max ratio ([\d.]+).*max share sqrt\(m\) ([\d.]+); FAILURES (\d+)", l)
    a = list(g.groups())
    tot['multisets'] += int(a[0]); tot['fl'] += int(a[1]); tot['fl2'] += int(a[2]); tot['pos'] += int(a[3]); tot['eq'] += int(a[6]); tot['ecases'] += int(a[7]); tot['fails'] += int(a[10])
    print(f"{f:14s} multisets {a[0]:>7s} fully live d {a[1]:>7s} (two+ primes {a[2]:>6s}, P > 0 {a[3]:>6s}) B max {a[5]} eq {a[6]:>6s}; E cases {a[7]:>7s} max {a[8]}; share sqrt(m) max {a[9]}; failures {a[10]}")
print(f"TOTAL over {files} files:", tot)
