"""Totals over the outputs levels_*.out, levels2_*.out, exhaust_*.out, big_*.out (reads the files, runs nothing)."""
import glob, re
ms = sg = 0; viol = 0; ctrl_v = ctrl_t = 0; full = 0
for f in sorted(glob.glob('levels_*.out') + glob.glob('levels2_*.out')):
    s = open(f).read()
    a = re.search(r'multisets (\d+), signings (\d+)', s)
    ms += int(a.group(1)); sg += int(a.group(2))
    viol += s.count('VIOLATED')
    for x in re.findall(r'good for B_flat but bad for B: (\d+)', s): viol += int(x)
    for x in re.findall(r'level bound violated: (\d+); finer bound violated: (\d+)', s): viol += int(x[0]) + int(x[1])
    for x in re.findall(r'union bound violated: (\d+)', s): viol += int(x)
    b = re.search(r'violated for (\d+) of (\d+) multisets', s)
    ctrl_v += int(b.group(1)); ctrl_t += int(b.group(2))
    if 'kind=full' in s: full += int(a.group(1))
print(f"random tests (levels_*.out, levels2_*.out): {ms} multisets ({full} of the kind 'full'), {sg} signings (first sign fixed), violations of (a), (b), (c): {viol}; "
      f"control without contraction: level bound fails for {ctrl_v} of {ctrl_t} multisets")
ms = 0; v = 0; ng = 0; fl = 0
for f in sorted(glob.glob('exhaust_*.out')):
    for line in open(f):
        a = re.search(r'multisets with 0: (\d+) \((\d+) with n_flat = n\); violations \(a\) (\d+), \(b\) (\d+), \(c\) (\d+); without a good signing: (\d+)', line)
        ms += int(a.group(1)); fl += int(a.group(2)); v += int(a.group(3)) + int(a.group(4)) + int(a.group(5)); ng += int(a.group(6))
print(f"all multisets with 0 (exhaust_*.out): {ms} multisets ({fl} with n_flat = n), violations {v}, without a good signing {ng}")
tot = good = sets = 0; least = 1.0
for f in sorted(glob.glob('big_*_*.out')):
    s = open(f).read()
    a = re.search(r'total: (\d+) of (\d+) random signings good', s)
    if not a: continue
    good += int(a.group(1)); tot += int(a.group(2)); sets += len(re.findall(r'^  set \d+', s, re.M))
    for x, y in re.findall(r'good among (\d+) random signings: (\d+)', s):
        least = min(least, int(y) / int(x))
print(f"large groups (big_*.out): {sets} multisets of 37 to 60 elements, {tot} random signings tested exactly, {good} good ({good/tot:.4f}); least fraction of good signings for one multiset {least:.2f}")
ap = sets2 = 0
for f in sorted(glob.glob('big_*_*.out')):
    s = open(f).read()
    a = re.search(r'all signs \+ bad for (\d+) of (\d+) sets', s)
    if a:
        ap += int(a.group(1)); sets2 += int(a.group(2))
print(f"large groups: all signs + is bad for {ap} of {sets2} multisets")
ms = 0; lv = 0; least = 1.0; sg = 0
for f in sorted(glob.glob('even_*.out')):
    for line in open(f):
        a = re.search(r'm=(\d+) set \d+: n_flat=\d+; fraction of good signings (\d+)/(\d+) .*level bound violated at \[(.*?)\]', line)
        if a:
            ms += 1; sg += int(a.group(3)); least = min(least, int(a.group(2)) / int(a.group(3))); lv += bool(a.group(4))
print(f"all signings, 14 to 18 elements (even_*.out): {ms} multisets, {sg} signings (first sign fixed), level bound violated for {lv}; least fraction of good signings {least:.4f}")
