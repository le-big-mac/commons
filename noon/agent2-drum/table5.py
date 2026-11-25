"""The weight table, in Markdown, from the outputs.   usage: python -I table5.py onedisc.json twodisc2.out chain-free-down.json chain-free-up.json chain-piled-down.json chain-piled-up.json exact3.out pieces2.out"""
import sys, json, re, math
ONE = {r['weight']: r for r in json.load(open(sys.argv[1]))}; TWO = {float(m): float(t) / 100 for m, t in re.findall(r"added mass\s+([\d.]+): two discs with free radii, least largest miss ([\d.]+)%", open(sys.argv[2]).read())}
def chain(f): return {r['weight']: r for r in json.load(open(f))}
FD, FU, PD, PU = (chain(f) for f in sys.argv[3:7]); OLD = {float(m): (float(a) / 100, float(b) / 100) for m, a, b in re.findall(r"^\s+([\d.]+)\s+([\d.]+)% \(used.*?steps\) ([\d.]+)% \(used", open(sys.argv[7]).read(), re.M)}
P3 = {}; cur = None
for line in open(sys.argv[8]):
    h = re.match(r"added mass ([\d.]+):", line); cur = float(h.group(1)) if h else cur; e = re.search(r"with edges and shares free: ([\d.]+)% \(([\d.]+)% with 4,000 cells\)", line)
    if e: P3[cur] = float(e.group(2)) / 100
EDGE = [j / 40 for j in range(41)]
def out_to(a): return EDGE[max(j for j, x in enumerate(a) if x > 1e-6) + 1]
print("| added mass, in skins | one even disc | two discs, free radii | discs piled on discs, 40 rings | any radial load, 40 rings | in cents | three even pieces, free edges |"); print("|---|---|---|---|---|---|---|")
wf = wp = 0.0
for m in sorted(ONE):
    f = min((FD[m], FU[m]), key=lambda r: r['miss']); p = min((PD[m], PU[m]), key=lambda r: r['miss'])
    wf = max(wf, abs(FD[m]['miss'] - FU[m]['miss'])); wp = max(wp, abs(PD[m]['miss'] - PU[m]['miss']))
    print(f"| {m:g} | {100 * ONE[m]['miss']:.2f}% | {100 * TWO[m]:.2f}% | {100 * p['miss']:.2f}% | {100 * f['miss']:.2f}% | {1200 * math.log2(1 + f['miss']):.0f} | {(f"{100 * P3[m]:.2f}%" if m in P3 else "")} |")
print(f"\nthe two walks (down from 12 skins and up from 1) differ by at most {100 * wf:.3f} points at any weight for any radial load, and by at most {100 * wp:.3f} for piled discs; the table has the lower of the two")
for m in sorted(ONE): print(f"   {m:5.2f}: any radial load, down {100 * FD[m]['miss']:.3f}% up {100 * FU[m]['miss']:.3f}%" + (f" (three starts, exact3.py: {100 * OLD[m][0]:.3f}%)" if m in OLD else "") + f"; piled, down {100 * PD[m]['miss']:.3f}% up {100 * PU[m]['miss']:.3f}%" + (f" (exact3.py: {100 * OLD[m][1]:.3f}%)" if m in OLD else ""))
