# A second year for the dawn page: 2025 through the frozen method (src/dawnlib.py). Rules and lines in expectations-2025.md,
# fixed before any 2025 reading was read. Run: ~/ipd/.venv/bin/python -I src/dawn2025.py > dawn2025.out
import sys, importlib.util, csv
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
YEAR = int(sys.argv[1]) if len(sys.argv) > 1 else 2025; FOLDER = sys.argv[2] if len(sys.argv) > 2 else '/home/agent1/night/data/ida2025'
# ---- the method on made-up nights with the readings' own grain (rounded to 0.01)
rng = np.random.default_rng(2025); tg = np.arange(0.5 / 60, 8, 1 / 60)
for name, shape in (("flat", lambda t: 21.0 + 0 * t), ("darkening 0.05 an hour to the end", lambda t: 18.0 + 0.05 * t), ("darkest in the middle", lambda t: 21.0 - 0.01 * (t - 4) ** 2), ("darkening for half the night, then flat", lambda t: 18.0 + 0.13 * np.minimum(t, 4))):
    tn = []
    for _ in range(400):
        m = np.round(shape(tg) + rng.normal(0, 0.02, len(tg)), 2); tn.append(L.tenth(dict(t=tg, m=m, L=8.0))[0])
    tn = np.array(tn); print(f"made-up nights, rounded to 0.01, {name}: the last tenth the darkest on {100 * np.mean(tn == 9):.0f} in 100; the darkest tenth in the second half on {100 * np.mean(tn >= 5):.0f}")
# ---- the year
N = L.load(YEAR, FOLDER); F = L.figures(N); clean = [c for c in N if c['clean']]
print(f"\n{YEAR}: moonless covered nights {len(N)}; clear {sum(1 for c in N if c['clear'])}; cleaned {F['nights']}; left out as not the sky {sum(1 for c in N if c['clear'] and not c['sky'])}, by the infrared test {sum(1 for c in N if c['clear'] and c['sky'] and c['ir'] is False)}")
print("   place, class: cleaned nights; last tenth the darkest; darkest tenth in the second half; end of night darker than its beginning")
for st in sorted(F['stations'], key=lambda s: ('lit', 'between', 'dark').index(L.CLASS[s])):
    v = F['stations'][st]; print(f"      {L.NAME[st]:<18} {L.CLASS[st]:<8} {v[0]:3d} {v[1]:3d} {v[2]:3d}   {v[3][1]} of {v[3][2]}")
print(f"   all nights: the last tenth the darkest on {F['last']:.1f} in 100; the darkest tenth in the second half on {F['second']:.1f}; nights by tenth {F['by_tenth']}")
for k in ('lit', 'between', 'dark'): print(f"   end of the night darker than its beginning, {k}: {F['before_' + k][0]:.0f} in 100 ({F['before_' + k][1]} of {F['before_' + k][2]})")
towns = [c for c in clean if L.CLASS[c['st']] == 'lit']
h1 = [L.slope(c['t'][c['t'] <= c['L'] / 2], c['m'][c['t'] <= c['L'] / 2]) for c in towns]; h2 = [L.slope(c['t'][c['t'] > c['L'] / 2], c['m'][c['t'] > c['L'] / 2]) for c in towns]
with open(f'/home/agent1/night/dawn{YEAR}_nights.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['station', 'class', 'evening of', 'night length h', 'darkest tenth (1 to 10)', 'last half hour less first, mag', 'last tenth within 0.02 of the darkest'])
    for c in clean: w.writerow([c['st'], L.CLASS[c['st']], c['d'], f"{c['L']:.2f}", L.tenth(c)[0] + 1, f"{L.dd(c):.3f}" if L.has_ends(c) else '', int(L.last_near(c))])
# ---- the lines
print(f"\nTHE LINES OF expectations-2025.md ({YEAR})")
def verdict(ok, n=None, need=8): return 'VOID (too few nights)' if n is not None and n < need else ('HELD' if ok else 'FAILED')
print(f"R1 (last tenth the darkest on 12 to 24 in 100): {F['last']:.1f} -> {verdict(12 <= F['last'] <= 24)}")
print(f"R2 (darkest tenth in the second half on 74 to 90 in 100): {F['second']:.1f} -> {verdict(74 <= F['second'] <= 90)}")
b = F['before_lit']; print(f"R3 (the five towns: end darker than beginning on 85 in 100 or more): {b[0]:.0f} ({b[1]} of {b[2]}) -> {verdict(b[0] >= 85, b[2])}")
b = F['before_two_darkest']; print(f"R4 (Nerpio and Arkaroola together: 35 to 65 in 100): {b[0]:.0f} ({b[1]} of {b[2]}) -> {verdict(35 <= b[0] <= 65, b[2])}")
b = F['before_otlica_ager']; print(f"R5 (Otlica and Ager together: 75 in 100 or more): {b[0]:.0f} ({b[1]} of {b[2]}) -> {verdict(b[0] >= 75, b[2])}")
b = F['towns_summer']; print(f"R6 (towns, May to August: last tenth darkest or within 0.02 on 45 in 100 or more): {b[0]:.0f} ({b[1]} of {b[2]}) -> {verdict(b[0] >= 45, b[2])}")
b = F['towns_winter']; print(f"R7 (towns, November to February: on 35 in 100 or fewer): {b[0]:.0f} ({b[1]} of {b[2]}) -> {verdict(b[0] <= 35, b[2])}")
mk = {st: v for st, v in F['milky'].items() if v[1] >= 8}; k = sum(1 for v in mk.values() if v[0] >= 65)
print("R8 (Milky Way: 65 in 100 or more at three or more of the four dark places): " + "; ".join(f"{L.NAME[st]} {v[0]:.0f} ({v[1]} nights)" for st, v in F['milky'].items()) + f" -> {'VOID (fewer than three places with eight nights)' if len(mk) < 3 else ('HELD' if k >= 3 else 'FAILED')}")
big = [(L.NAME[st], v[1], v[0]) for st, v in F['stations'].items() if v[0] >= 15]; worst = max(big, key=lambda x: x[1] / x[2]) if big else None
print("R9 (no place with fifteen nights or more has the last tenth the darkest on half or more): " + (f"the most is {worst[0]}, {worst[1]} of {worst[2]}" if worst else "no such place") + f" -> {verdict(all(x[1] / x[2] < 0.5 for x in big))}")
print(f"R10 (towns: darkening 0.08 an hour or more over the first half, under 0.03 either way over the second): {np.median(h1):+.3f} and {np.median(h2):+.3f} ({len(towns)} nights) -> {verdict(np.median(h1) >= 0.08 and abs(np.median(h2)) < 0.03, len(towns))}")
