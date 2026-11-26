"""How long does a hold on the bed last, counting the holds still running when a run stopped (they are longer than they look)?
Product-limit (Kaplan-Meier) estimate of the median from bed_core_beta*.out.
usage: bed_core_holds.py"""
import re, glob
for beta in (2, 1):
    done, running = [], []
    for f in sorted(glob.glob(f'bed_core_beta{beta}_*.out')):
        for line in open(f):
            m = re.search(r'finished episodes \(generations\): \[(.*?)\](; one still running after (\d+))?', line)
            done += [int(x) for x in m.group(1).split(', ') if x]
            if m.group(3): running.append(int(m.group(3)))
    ev = sorted([(d, 1) for d in done] + [(r, 0) for r in running])
    n = len(ev); s = 1.0; med = None; q1 = None
    for i, (t, e) in enumerate(ev):
        at_risk = n - i
        if e: s *= 1 - 1 / at_risk
        if q1 is None and s <= 0.75: q1 = t
        if med is None and s <= 0.5: med = t
    print(f'selection {beta}: {len(done)} holds ended, {len(running)} still running at the end of a run; a quarter ended within {q1:,} generations, half within {med if med is None else format(med, ",")}; the longest seen {max(t for t, _ in ev):,}')
