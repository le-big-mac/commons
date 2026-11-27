"""Totals for the report, read from the outputs of the tests (nothing is computed here)."""
import glob
import os
import re
import sys

here = os.path.dirname(os.path.abspath(__file__))


def rd(name):
    return open(os.path.join(here, name)).read().splitlines()


# ---- part T ----
# chain C repeats the smaller sizes of chains A and B: of the exhaustive runs keep, for each (group, range of
# positions), the one with the most elements, so that no family is counted twice
runs = {}
rand = []
incomplete = 0
for f in ('t1_twice_A.out', 't1_twice_B.out', 't1_twice_C.out'):
    for line in rd(f):
        m = re.match(r"(exh|rand) (\w+)(.*?): families (\d+), inequalities checked (\d+), violations (\d+), families "
                     r"with level 0 bad for some signing (\d+), with equality \(factor 2 attained\) (\d+), with a level "
                     r"beyond the largest position bad (\d+), largest ratio (\S+)", line)
        if m:
            kind, g, mid = m.group(1), m.group(2), m.group(3)
            nums = tuple(int(m.group(i)) for i in range(4, 10)) + (m.group(10),)
            if kind == 'exh':
                mm = re.search(r"positions < (\d+), .* up to (\d+) elements", mid)
                key = (g, int(mm.group(1)))
                if key not in runs or runs[key][0] < int(mm.group(2)):
                    runs[key] = (int(mm.group(2)), nums)
            else:
                rand.append((g, nums))
        if 'stopped by the clock' in line:
            incomplete += 1
        if 'VIOLATION' in line:
            print("T: VIOLATION LINE:", line)
tot = [0] * 6
per = {}
for (g, P), (M, nums) in runs.items():
    for i in range(6):
        tot[i] += nums[i]
    p = per.setdefault(g, dict(exh=0, rand=0, viol=0, eq=0, ratio=set(), cfg=[]))
    p['exh'] += nums[0]
    p['viol'] += nums[2]
    p['eq'] += nums[4]
    p['ratio'].add(nums[6])
    p['cfg'].append((P, M))
tr = [0] * 6
for g, nums in rand:
    for i in range(6):
        tr[i] += nums[i]
    p = per.setdefault(g, dict(exh=0, rand=0, viol=0, eq=0, ratio=set(), cfg=[]))
    p['rand'] += nums[0]
    p['viol'] += nums[2]
    p['eq'] += nums[4]
    p['ratio'].add(nums[6])
print(f"T, complete enumerations (each family once): valued families {tot[0]} (every signing of each), inequalities "
      f"checked (one for each K) {tot[1]}, violations {tot[2]}; families where level 0 is bad for some signing {tot[3]}; "
      f"with equality for some K {tot[4]}; with a level beyond the largest position bad {tot[5]}; runs cut by the clock "
      f"{incomplete}")
print(f"T, random families: {tr[0]}, inequalities {tr[1]}, violations {tr[2]}, level 0 bad for some signing {tr[3]}, "
      f"equality {tr[4]}, a level beyond the largest position bad {tr[5]}")
for g, p in per.items():
    print(f"   {g}: exhaustive {p['exh']} (positions below P, up to M elements: (P, M) = {sorted(p['cfg'])}), random "
          f"{p['rand']}, violations {p['viol']}, with equality {p['eq']}, largest ratios {sorted(p['ratio'])}")

# ---- A' and B ----
for mode, f in (('A', 't4_A.out'), ('B', 't4_B.out')):
    n3 = {'all multisets': 0, 'multisets containing 0': 0}          # multisets with m >= 3
    fail3 = 0
    plus3 = {'all multisets': 0, 'multisets containing 0': 0}
    by_n = {}
    by_n_all = {}
    maxtried = 0
    inc = []
    small = dict()
    for line in rd(f):
        m = re.match(r"(\w) n=(\d+) m=(\d+) (all multisets|multisets containing 0): (\d+) multisets, without a \S+ "
                     r"signing: (\d+); 'all \+' fails for (\d+); most signings tried (\d+)(.*)", line)
        if not m:
            continue
        n, mm, kind, cnt, fail, plus, tried = (int(m.group(2)), int(m.group(3)), m.group(4), int(m.group(5)),
                                               int(m.group(6)), int(m.group(7)), int(m.group(8)))
        if 'INCOMPLETE' in m.group(9):
            inc.append((n, mm, cnt))
        if mm >= 3:
            n3[kind] += cnt
            fail3 += fail
            plus3[kind] += plus
            maxtried = max(maxtried, tried)
            d = by_n_all if kind == 'all multisets' else by_n
            d[n] = max(d.get(n, 0), mm) if 'INCOMPLETE' not in m.group(9) else d.get(n, 0)
        else:
            s = small.setdefault(mm, [0, 0])
            s[0] += cnt
            s[1] += fail
    z = 'multisets containing 0'
    a = 'all multisets'
    print(f"{mode}: multisets of 3 or more elements: {n3[z]} containing 0 (one from each class of translates), and in the "
          f"runs over every multiset {n3[a]} (these repeat multisets of the first kind); without a "
          f"{'3-good' if mode == 'A' else 'good'} signing: {fail3}; 'all +' fails for {plus3[z]} and {plus3[a]}; most "
          f"signings tried {maxtried}; incomplete runs (n, m, done) {inc}")
    print(f"   multisets containing 0, complete up to size (n: size): "
          f"{', '.join(f'{n}: {s}' for n, s in sorted(by_n.items()))}")
    print(f"   every multiset (no translation), complete up to size (n: size): "
          f"{', '.join(f'{n}: {s}' for n, s in sorted(by_n_all.items()))}")
    print(f"   sizes 0, 1, 2 in the runs over every multiset (size: multisets, without): "
          f"{ {k: tuple(v) for k, v in sorted(small.items())} }")

# ---- the final statements ----
tot = exc = good = mis = wd = 0
rng = {}
for f in sorted(glob.glob(os.path.join(here, 't5_final_*.out'))):
    if f.endswith('t5_final_16_4.out'):
        continue        # the first trial run, contained in the later ones
    for line in open(f):
        m = re.match(r"n=(\d+): nonempty multisets of size <= (\d+): (\d+); exceptional pairs \(definition\) (\d+); with "
                     r"a good\s+splitting (\d+); mismatches of 'good splitting iff not exceptional' (\d+); definition "
                     r"against\s+'two elements with 2\^k not dividing a - b': (\d+) differences", line)
        if m:
            n, s, t, e, g, mi, w = (int(x) for x in m.groups())
            tot += t
            exc += e
            good += g
            mis += mi
            wd += w
            rng[n] = s
        if 'stopped by the clock' in line or 'MISMATCH' in line or 'DIFFER' in line:
            print("final:", line.strip())
sizes = {}
for n, s in rng.items():
    sizes.setdefault(s, []).append(n)
print(f"finals: nonempty multisets {tot} (every multiset on Z_n, every splitting), exceptional pairs {exc}, with a good "
      f"splitting {good} (sum {exc + good}), mismatches {mis}, differences between the definition and the paper's words "
      f"{wd}")
print("   sizes up to s for n in:", {s: (min(v), max(v)) for s, v in sorted(sizes.items())})
