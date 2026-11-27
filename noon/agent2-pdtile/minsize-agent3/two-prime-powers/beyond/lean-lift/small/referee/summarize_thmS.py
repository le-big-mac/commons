"""Table of the runs of ref_thmS.py from their output files thmS_*.out."""
import re, glob, sys
rows = []
tot = dict(cases=0, fail=0, plusbad=0, ld=0, psi=0, allsign=0, sampled=0, gf=0, viol=0, conv=0)
sizes = {}
for fn in sorted(glob.glob('thmS_*.out')):
    t = open(fn).read()
    head = re.search(r'group (\w): n = (\d+) = ([^;]*); kind (\w+); seed (\d+); (\d+) multisets', t)
    if not head: continue
    G, n, shape, kind, seed, want = head.groups()
    cases = re.findall(r'^case \d+ \((\w+)\): m = (\d+),', t, flags=re.M)
    ms = [int(m) for _, m in cases]
    for m in ms: sizes[m] = sizes.get(m, 0) + 1
    fail = len(re.findall(r'NO GOOD SIGNING', t))
    plusbad = len(re.findall(r'all signs \+: Phi_d divides for [1-9]\d* of', t))
    tries = [int(x) for x in re.findall(r'good signing found at try (\d+)', t)]
    full = len(re.findall(r'\(full search\)', t))
    ld = len(re.findall(r'confirmed by long division: \d+ divisors d, \d+ divisions, a nonzero remainder for every d: True', t))
    psi = len(re.findall(r'confirmed with Psi \(no long division\): \d+ divisors d, none divides: True', t))
    alls = re.findall(r'all (\d+) signings: good for B-flat (\d+), of these bad for B (\d+); good for B and bad for B-flat (\d+)', t)
    samp = re.findall(r'(\d+) random signings: good for B-flat (\d+), each of them good for B', t)
    nfl = [int(x) for x in re.findall(r'contracted in \d+ steps to Z_(\d+)', t)]
    viol = len(re.findall(r'VIOLATION', t))
    status = re.search(r'exit status (\d+)', t)
    rows.append((G, shape, kind, len(ms), want, min(ms) if ms else '-', max(ms) if ms else '-', plusbad, max(tries) if tries else '-', full, ld, psi, max(nfl) if nfl else '-', status.group(1) if status else 'running'))
    tot['cases'] += len(ms); tot['fail'] += fail; tot['plusbad'] += plusbad; tot['ld'] += ld; tot['psi'] += psi
    tot['allsign'] += len(alls); tot['sampled'] += len(samp); tot['viol'] += viol
    tot['gf'] += sum(int(a[1]) for a in alls) + sum(int(s[1]) for s in samp)
    tot['conv'] += sum(int(a[3]) for a in alls)
print('group | n | kind | multisets done (asked) | sizes | all + bad | most tries | full searches | confirmed by long division | confirmed with Psi | largest contracted group | exit')
for r in rows:
    print(f'{r[0]} | {r[1]} | {r[2]} | {r[3]} ({r[4]}) | {r[5]}..{r[6]} | {r[7]} | {r[8]} | {r[9]} | {r[10]} | {r[11]} | {r[12]} | {r[13]}')
print(f'TOTAL: multisets {tot["cases"]}; no good signing found: {tot["fail"]}; all signs + bad: {tot["plusbad"]}; good signing confirmed by long division: {tot["ld"]}, with Psi only: {tot["psi"]}')
print(f'       route of the note: all signings compared for {tot["allsign"]} multisets, sampled for {tot["sampled"]}; signings good for B-flat tested on B: {tot["gf"]}; violations: {tot["viol"]}; good for B and bad for B-flat (all-signings cases): {tot["conv"]}')
print('       sizes:', ', '.join(f'{m}: {c}' for m, c in sorted(sizes.items())))
