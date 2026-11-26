"""Summarise bed_core_beta*.out: the live page's own core run without a browser, 24 runs of 500,000 generations at the page's
opening settings (3% slips, games of 50 rounds, 100 machines, selection "strong" = 2) and 24 with selection 1 (the strength of
the study's runs)."""
import re, glob, statistics as st
for beta in (2, 1):
    rows = []
    for f in sorted(glob.glob(f'bed_core_beta{beta}_*.out')):
        for line in open(f):
            m = re.match(r'run \d+ seed (\d+): first take-over (none|at generation (\d+) by (\w+)); cooperative moves (\d+)%; commonest kind, % of generations: (.*?); finished episodes \(generations\): \[(.*?)\](; one still running after (\d+))?', line)
            if not m: print('unparsed', line[:80]); continue
            sh = dict((a.strip(' ,'), float(b)) for a, b in re.findall(r'([A-Za-z][A-Za-z ,\-]*?) (\d+\.\d)', m.group(6)))
            rows.append(dict(first=int(m.group(3)) if m.group(3) else None, entry=m.group(4), coop=int(m.group(5)), sh=sh,
                             eps=[int(x) for x in m.group(7).split(', ') if x], open=int(m.group(9)) if m.group(9) else None))
    n = len(rows); firsts = sorted(r['first'] for r in rows if r['first'] is not None)
    print(f'\nselection {beta}: {n} runs of 500,000 generations')
    print(f'  first take-over (the machine at any entry state, at least 60% of the bed): in {len(firsts)} of {n} runs; generations min {firsts[0]:,}, median {int(st.median(firsts)):,}, max {firsts[-1]:,}; within 20,000: {sum(f <= 20000 for f in firsts)}, within 75,000: {sum(f <= 75000 for f in firsts)}')
    ent = {}
    for r in rows: ent[r['entry']] = ent.get(r['entry'], 0) + 1
    print('  which entry state took over first:', ent)
    for k in ('all-defect', 'handshake', 'shifty', 'wooer', 'unnamed'):
        v = [r['sh'].get(k, 0) for r in rows]; print(f'  commonest kind is {k:11s}: mean {st.mean(v):5.1f}% of generations (runs from {min(v):.1f} to {max(v):.1f})')
    fam = [r['sh'].get('handshake', 0) + r['sh'].get('shifty', 0) + r['sh'].get('wooer', 0) for r in rows]
    print(f'  the machine at any entry state: mean {st.mean(fam):.1f}% (runs from {min(fam):.1f} to {max(fam):.1f}); cooperative moves mean {st.mean(r["coop"] for r in rows):.0f}%')
    eps = sorted(e for r in rows for e in r['eps']); opens = [r['open'] for r in rows if r['open'] is not None]
    print(f'  finished holds (from take-over until all-defect again has 60% of the bed): {len(eps)}; generations min {eps[0]:,}, quartiles {eps[len(eps)//4]:,} / {int(st.median(eps)):,} / {eps[3*len(eps)//4]:,}, max {eps[-1]:,}; shorter than 30,000: {sum(e < 30000 for e in eps)}; still running at the end: {len(opens)}')
    lost = sum(1 for r in rows if r['eps']); print(f'  runs in which the bed was lost to all-defect at least once after a take-over: {lost} of {n}')
