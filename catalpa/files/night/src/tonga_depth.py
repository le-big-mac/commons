# How much the figure grows with the depth of the Sun, south against north, from the two saved sets of reductions at the
# levels 13.0, 14.0 and 15.0 (tonga_levels.py, tonga_levels_north.py). The figure is May to November 2022 against the
# same months of 2021 and 2024, in magnitudes (negative: a brighter twilight); "growth" is the figure at 15.0 less the
# figure at 13.0.
import pickle, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('tln', B + 'src/tonga_levels_north.py'); TLN = importlib.util.module_from_spec(spec); spec.loader.exec_module(TLN)
spec = importlib.util.spec_from_file_location('tl', B + 'src/tonga_levels.py'); TL = importlib.util.module_from_spec(spec); spec.loader.exec_module(TL)
RS = pickle.load(open(B + 'cache2/tonga_levels.pkl', 'rb')); RN = pickle.load(open(B + 'cache2/tonga_levels_north.pkl', 'rb'))
LEVELS = (13.0, 14.0, 15.0)
def south_fig(st, level, months):
    V = {(y, m): RS[(s, y, m, l)][0] for (s, y, m, l) in RS if s == st and l == level and RS[(s, y, m, l)] and RS[(s, y, m, l)][0] is not None}
    sl = [abs(RS[k][1]) for k in RS if k[0] == st and k[3] == level and RS[k] and RS[k][1] is not None]
    if not V or not sl: return None
    s = float(np.median(sl)); a = []
    for m in months:
        base = [V[(yy, m)] for yy in (2021, 2024) if (yy, m) in V]
        if (2022, m) in V and base: a.append(s * (V[(2022, m)] - float(np.mean(base))))
    return float(np.mean(a)) if len(a) >= min(2, len(months)) else None
print('A. the eleven southern photometers: the figure at 13.0, 14.0, 15.0 and its growth; then July 2022 alone')
gs = []; gj = []
for st, name in TL.SOUTH.items():
    f = [south_fig(st, l, (5, 7, 9, 11)) for l in LEVELS]; j = [south_fig(st, l, (7,)) for l in LEVELS]
    gs.append(f[2] - f[0]); gj.append(j[2] - j[0])
    print(f"   {name:<14} " + '  '.join(f'{x:+.2f}' for x in f) + f'   growth {f[2] - f[0]:+.2f}      July: ' + '  '.join(f'{x:+.2f}' for x in j) + f'   growth {j[2] - j[0]:+.2f}')
print(f'   growth, May to November: from {max(gs):+.2f} to {min(gs):+.2f}, middle {np.median(gs):+.2f}; at -0.10 or below: {sum(1 for g in gs if g <= -0.10)} of {len(gs)}')
print(f'   growth, July 2022: from {max(gj):+.2f} to {min(gj):+.2f}, middle {np.median(gj):+.2f}; at -0.25 or below: {sum(1 for g in gj if g <= -0.25)} of {len(gj)}')
print('\nB. the northern photometers (north of the equator) with the figure at all three levels: the growth, from the most southern-like')
NORTH = sorted({k[0] for k in RN}, key=lambda s: int(s.replace('stars', ''))); G = {}
for st in NORTH:
    f = [TLN.figure(RN, st, l)[0] for l in LEVELS]
    if None not in f: G[st] = (f[2] - f[0], f)
for st, (g, f) in sorted(G.items(), key=lambda kv: kv[1][0]):
    if g <= -0.10 or f[1] <= -0.15: print(f"   {st:<9} " + '  '.join(f'{x:+.2f}' for x in f) + f'   growth {g:+.2f}')
gn = [g for g, f in G.values()]
print(f'   {len(gn)} photometers; growth within 0.05 of nothing at {sum(1 for g in gn if abs(g) <= 0.05)}; at -0.10 or below at {sum(1 for g in gn if g <= -0.10)} ({", ".join(s for s, (g, f) in G.items() if g <= -0.10)}); middle {np.median(gn):+.3f}')
both = [s for s, (g, f) in G.items() if g <= -0.10 and f[1] <= -0.15]
print(f'   brighter by 0.15 or more at 14.0 AND growing by 0.10 or more with depth: {len(both)} of {len(gn)} northern ({", ".join(both) if both else "none"}); of the southern eleven: {sum(1 for st in TL.SOUTH if south_fig(st, 14.0, (5, 7, 9, 11)) <= -0.15 and south_fig(st, 15.0, (5, 7, 9, 11)) - south_fig(st, 13.0, (5, 7, 9, 11)) <= -0.10)}')
print('\nC. the made-up change of 0.3 magnitude (three steady northern photometers): growth of what was found')
for st in TLN.PLANT:
    d = [TLN.figure(RN, st, l, True)[0] - TLN.figure(RN, st, l, False)[0] for l in LEVELS]
    print(f"   {st:<9} " + '  '.join(f'{x:+.2f}' for x in d) + f'   growth {d[2] - d[0]:+.2f}')
# ---- D. could a lamp near the meter do it? The extra light of May to November 2022 at the page's level (14.0), set
# against all the light of the same meter's moonless night sky (the middle reading of its moonless nights, 2021 to 2024).
print('\nD. the extra light at 14.0, May to November 2022, as a multiple of the whole moonless night sky at the same meter')
RR = {}
for fn in ('cache2/twilight16.pkl', 'cache2/twilight_new.pkl', 'cache2/twilight_south.pkl', 'cache2/twilight_south2.pkl'):
    X = pickle.load(open(B + fn, 'rb')); X.pop('meta', None); RR.update(X)
mult = {}
for st, name in TL.SOUTH.items():
    lev = [n[2] for k, r in RR.items() if k[0] == st and r and 2021 <= k[1] <= 2024 for n in r.get('nights', [])]
    f = south_fig(st, 14.0, (5, 7, 9, 11)); night = float(np.median(lev)); extra = (10 ** (-0.4 * f) - 1) * 10 ** (0.4 * (night - 14.0)); mult[name] = extra
    print(f"   {name:<14} night {night:5.2f} ({len(lev)} nights)   brighter by {100 * (10 ** (-0.4 * f) - 1):3.0f} per cent at 14.0   = {extra:5.0f} times its night sky")
print(f'   at 100 times or more: {sum(1 for v in mult.values() if v >= 100)} of {len(mult)}; the least {min(mult.values()):.0f} ({min(mult, key=mult.get)}), the most {max(mult.values()):.0f} ({max(mult, key=mult.get)})')
