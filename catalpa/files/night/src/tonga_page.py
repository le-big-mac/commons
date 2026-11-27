# Figures, a table and two pictures for the page on the southern twilight. Reads the four files of twilight reductions
# (the sixteen of the dawn page, the twenty-two of the sixth sheet, and the two fetches of the seventh).
# Every instrument: each month's twilight figure (the Sun's altitude when the raw-count reading passes 14.0, evening and
# morning averaged) less the mean of the same calendar month in 2021 and 2024, whichever it has; turned into magnitudes
# by the instrument's own twilight slope, and into "parts in 100 brighter" by 100 x (10^(-0.4 x magnitudes) - 1).
import pickle, csv, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('tongasheet', '/home/agent1/night/src/tongasheet.py'); TS = importlib.util.module_from_spec(spec); spec.loader.exec_module(TS)
TW = TS.TW; geo = TS.geo; B = '/home/agent1/night/'
R = {}; tested_south = []; tested_north = []
for fn in ('cache2/twilight16.pkl', 'cache2/twilight_new.pkl', 'cache2/twilight_south.pkl', 'cache2/twilight_south2.pkl'):
    X = pickle.load(open(B + fn, 'rb')); m = X.pop('meta', None); R.update(X)
    if m and 'south' in m: tested_south += list(m['south']); tested_north += list(m.get('north', []))
SEEN_SOUTH = ['stars477', 'stars456', 'stars221', 'stars29']
PLACE = {'stars477': 'Arkaroola, South Australia', 'stars456': 'Mudgee, New South Wales', 'stars221': 'El Leoncito, Argentina', 'stars29': 'Bahía Blanca, Argentina',
         'stars634': 'Martinborough, New Zealand', 'stars215': 'Mount Martha, Victoria', 'stars220': 'Malargüe, Argentina', 'stars315': 'Coonabarabran, New South Wales',
         'stars722': 'southern Queensland', 'stars391': 'San Pedro de Atacama, Chile', 'stars251': 'Réunion'}
def pct(mag): return 100 * (10 ** (-0.4 * mag) - 1)
def series(st):
    chips = {}
    for (s, y, m), r in R.items():
        if s == st and r is not None and TW.month_value(r): chips.setdefault(TS.chip(r), []).append((y, m))
    if not chips: return None
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; E = {}; Mo = {}; sl = []; name = ''
    for (s, y, m), r in R.items():
        if s != st or r is None or TS.chip(r) != ch: continue
        mv = TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; E[(y, m)] = mv[1]; Mo[(y, m)] = mv[2]; sl += r['sl']; name = r.get('name') or name
    s = abs(float(np.median(sl)))
    def anom(W):
        out = {}
        for (y, m), v in W.items():
            base = [W[(yy, m)] for yy in (2021, 2024) if (yy, m) in W]
            if base: out[(y, m)] = s * (v - float(np.mean(base)))
        return out
    return dict(a=anom(V), e=anom(E), mo=anom(Mo), name=name, lat=float(geo[st]['latitude']) if st in geo and geo[st]['latitude'] else float('nan'), lon=float(geo[st]['longitude']) if st in geo and geo[st]['longitude'] else float('nan'))
stations = sorted({k[0] for k in R}, key=lambda s: int(s.replace('stars', ''))); S = {st: series(st) for st in stations}; S = {k: v for k, v in S.items() if v}
south = [st for st in S if S[st]['lat'] < 0]; north = [st for st in S if S[st]['lat'] >= 30]; canary = [st for st in S if 0 <= S[st]['lat'] < 30]
def d2(st):
    v = [S[st]['a'][(2022, m)] for m in (5, 7, 9, 11) if (2022, m) in S[st]['a']]
    return float(np.mean(v)) if len(v) >= 2 else None
print(f'photometers in the four sets of reductions: {len(stations)}; '); print(f'instruments with a twilight figure: {len(S)}; south of the equator {len(south)}; north of 30 degrees {len(north)}; between {len(canary)}')
print('\nA. the southern photometers: latitude; May to November 2022 against the same months of 2021 and 2024 (magnitudes; parts in 100 brighter); the brightest month and its size; seen first or tested')
tab = []
for st in sorted(south, key=lambda s: S[s]['lat']):
    d = d2(st); a22 = {k: v for k, v in S[st]['a'].items() if k[0] in (2022, 2023)}; pk = min(a22, key=a22.get) if a22 else None
    tab.append((st, S[st]['lat'], d, pk, a22.get(pk)))
    print(f"   {PLACE.get(st, st):<32} {S[st]['lat']:+6.1f}   {d:+.2f}  {pct(d):+4.0f}    " + (f"{pk[0]}-{pk[1]:02d} {a22[pk]:+.2f} ({pct(a22[pk]):+.0f})" if pk else '-') + ('   seen first' if st in SEEN_SOUTH else '   tested'))
ds = np.array([t[2] for t in tab]); dt_ = np.array([t[2] for t in tab if t[0] in tested_south])
print(f'   all {len(ds)}: from {ds.max():+.2f} to {ds.min():+.2f} magnitude, middle {np.median(ds):+.2f}; in parts in 100 brighter: {pct(ds.max()):.0f} to {pct(ds.min()):.0f}, middle {pct(np.median(ds)):.0f}')
print(f'   the seven tested: from {dt_.max():+.2f} to {dt_.min():+.2f}, middle {np.median(dt_):+.2f}; parts in 100: {pct(dt_.max()):.0f} to {pct(dt_.min()):.0f}, middle {pct(np.median(dt_)):.0f}')
dn = {st: d2(st) for st in north}; dn = {k: v for k, v in dn.items() if v is not None}
print(f'\nB. the northern photometers (north of 30 degrees) with the same figure: {len(dn)}; within 0.10 magnitude of nothing: {sum(1 for v in dn.values() if abs(v) < 0.10)}; at -0.15 or below: {sum(1 for v in dn.values() if v <= -0.15)} ({", ".join(k for k, v in dn.items() if v <= -0.15)}); middle {np.median(list(dn.values())):+.3f} ({pct(np.median(list(dn.values()))):+.0f} in 100)')
print(f"   the five tested: " + ', '.join(f'{st} {dn[st]:+.2f}' for st in tested_north if st in dn))
dc = {st: d2(st) for st in canary}; print('   between the equator and 30 north (the Canaries and Lanzarote): ' + ', '.join(f'{st} {v:+.2f}' for st, v in dc.items() if v is not None))
MON = [(y, m) for y in (2021, 2022, 2023, 2024) for m in (1, 3, 5, 7, 9, 11)]
def middle(group, W='a', need=3):
    out = {}
    for k in MON:
        v = [S[st][W][k] for st in group if k in S[st][W]]
        if len(v) >= need: out[k] = (float(np.median(v)), len(v), float(np.min(v)), float(np.max(v)))
    return out
ms = middle(south); mn = middle(north)
print('\nC. month by month, the middle of the southern photometers (magnitudes; parts in 100 brighter; how many), and of the northern')
for k in MON:
    print(f"   {k[0]}-{k[1]:02d}   south " + (f"{ms[k][0]:+.2f} {pct(ms[k][0]):+4.0f} ({ms[k][1]}; from {pct(ms[k][3]):+.0f} to {pct(ms[k][2]):+.0f})" if k in ms else '      -          ') + '    north ' + (f"{mn[k][0]:+.2f} {pct(mn[k][0]):+4.0f} ({mn[k][1]})" if k in mn else '-'))
pk = min((k for k in ms if k[0] in (2022, 2023)), key=lambda k: ms[k][0]); print(f'   the southern middle is brightest in {pk[0]}-{pk[1]:02d}: {ms[pk][0]:+.2f} magnitude, {pct(ms[pk][0]):.0f} in 100 brighter')
print('   southern photometers by month of 2022, each one: ' + '; '.join(f"{PLACE.get(st, st).split(',')[0]} " + ' '.join(f"{pct(S[st]['a'][(2022, m)]):+.0f}" if (2022, m) in S[st]['a'] else '.' for m in (1, 3, 5, 7, 9, 11)) for st in sorted(south, key=lambda s: S[s]['lat'])))
jan = [S[st]['a'][(2022, 1)] for st in south if (2022, 1) in S[st]['a']]; mar = [S[st]['a'][(2022, 3)] for st in south if (2022, 3) in S[st]['a']]; may = [S[st]['a'][(2022, 5)] for st in south if (2022, 5) in S[st]['a']]
print(f'   January 2022: {len(jan)} photometers, from {min(jan):+.2f} to {max(jan):+.2f}; March 2022: {len(mar)}, from {min(mar):+.2f} to {max(mar):+.2f}; May 2022: {len(may)}, from {min(may):+.2f} to {max(may):+.2f}, at -0.15 or below at {sum(1 for x in may if x <= -0.15)}')
print('   southern photometers brighter by 0.10 magnitude or more, of those with the month: ' + ', '.join(f"{k[0]}-{k[1]:02d} {sum(1 for st in south if k in S[st]['a'] and S[st]['a'][k] <= -0.10)} of {sum(1 for st in south if k in S[st]['a'])}" for k in MON if k[0] in (2022, 2023)))
print('   January 2022, each southern photometer that has it (magnitudes; positive: a darker twilight): ' + ', '.join(f"{PLACE.get(st, st).split(',')[0]} {S[st]['a'][(2022, 1)]:+.2f}" for st in sorted(south, key=lambda s: S[s]['lat']) if (2022, 1) in S[st]['a']))
late = {k: ms[k] for k in ms if k >= (2023, 7)}; print('   from July 2023: ' + ', '.join(f'{k[0]}-{k[1]:02d} {pct(v[0]):+.0f}' for k, v in late.items()))
print('\nD. evening and morning apart, May to November 2022, each southern photometer (magnitudes): ' + '; '.join(f"{PLACE.get(st, st).split(',')[0]} {np.mean([S[st]['e'][(2022, m)] for m in (5, 7, 9, 11) if (2022, m) in S[st]['e']]):+.2f} and {np.mean([S[st]['mo'][(2022, m)] for m in (5, 7, 9, 11) if (2022, m) in S[st]['mo']]):+.2f}" for st in sorted(south, key=lambda s: S[s]['lat'])))
# ---- table for the page
rows = ['<tr><th>place</th><th class="n">degrees south</th><th class="n">brighter, May to November 2022, per cent</th><th>how it came into this page</th></tr>']
for st, lat, d, pk_, v in sorted(tab, key=lambda t: -t[1]): rows.append(f'<tr><td>{PLACE.get(st, st)}</td><td class="n">{-lat:.0f}</td><td class="n">{pct(d):.0f}</td><td>{"seen first" if st in SEEN_SOUTH else "tested"}</td></tr>')
open(B + 't_tonga.html', 'w', encoding='utf-8').write('<div class="tablewrap"><table>\n' + '\n'.join(rows) + '\n</table></div>\n')
# ---- pictures
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'; ORANGE = '#eb6834'
x = {k: (k[0] - 2021) + (k[1] - 0.5) / 12 for k in MON}
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.11, 0.845, 0.71]); ax.set_facecolor(SURF)
for st in south:
    ks = [k for k in MON if k in S[st]['a']]; ax.plot([x[k] for k in ks], [pct(S[st]['a'][k]) for k in ks], color='#c9d8ee', lw=1.0, zorder=2)
ks = [k for k in MON if k in mn]; ax.plot([x[k] for k in ks], [pct(mn[k][0]) for k in ks], color=ORANGE, lw=2.2, zorder=4, marker='o', ms=4, mec=SURF, mew=0.6)
ks = [k for k in MON if k in ms]; ax.plot([x[k] for k in ks], [pct(ms[k][0]) for k in ks], color=BLUE, lw=2.6, zorder=5, marker='o', ms=5, mec=SURF, mew=0.7)
ax.axhline(0, color=INK2, lw=1.0, zorder=3); ax.axvline(1 + 14.5 / 365, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=3)
ax.text(1 + 14.5 / 365 - 0.05, -27, 'eruption,\n15 Jan 2022', fontsize=11.5, color=INK2, ha='right', va='top')
ax.text(1.93, pct(ms[(2022, 7)][0]) + 4, 'south', fontsize=12.5, color=INK, ha='left', va='bottom'); ax.text(3.35, 12, 'north', fontsize=12.5, color=INK, ha='left', va='bottom')
ax.set_xlim(0, 4); ax.set_ylim(-50, 118); ax.set_xticks([0.5, 1.5, 2.5, 3.5]); ax.set_xticklabels(['2021', '2022', '2023', '2024'], fontsize=13); ax.set_yticks([-25, 0, 25, 50, 75, 100]); ax.set_yticklabels(['−25', '0', '25', '50', '75', '100'], fontsize=13)
for v in (1, 2, 3): ax.axvline(v, color=GRID, lw=1, zorder=1)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.975, 'twilight overhead: per cent brighter than', fontsize=12.5, color=INK2, va='top'); fig.text(0.015, 0.915, 'the same month of 2021 and 2024', fontsize=12.5, color=INK2, va='top')
fig.savefig(B + 'img/tonga-months.png', dpi=140, facecolor=SURF); plt.close(fig)
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.15, 0.845, 0.65]); ax.set_facecolor(SURF)
allp = [(S[st]['lat'], d2(st), st) for st in S if d2(st) is not None]
for lat, d, st in allp:
    v = pct(d); off = v > 95
    ax.plot([lat], [min(v, 90)], 'o' if not off else '^', ms=8, color=BLUE if lat < 0 else ORANGE, mec=SURF, mew=1.0, zorder=4, alpha=0.95)
ax.axhline(0, color=INK2, lw=1.0, zorder=3); ax.axvline(0, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=2); ax.text(1.5, 62, 'equator', fontsize=13, color=INK2, ha='left', va='top'); ax.text(39.5, 90, 'a broken meter,\noff the scale', fontsize=13, color=INK2, ha='right', va='center')
ax.text(S['stars251']['lat'] + 2.2, pct(d2('stars251')), 'Réunion', fontsize=13, color=INK2, ha='left', va='center')
ax.plot([S['stars634']['lat']] * 2, [pct(d2('stars634')) - 5, -9], color=INK2, lw=0.8, zorder=2); ax.text(S['stars634']['lat'] - 3.3, -15, 'New Zealand', fontsize=13, color=INK2, ha='left', va='center')
ax.set_xlim(-46, 50); ax.set_ylim(-25, 99); ax.set_xticks([-40, -20, 0, 20, 40]); ax.set_xticklabels(['40° S', '20° S', '0', '20° N', '40° N'], fontsize=15); ax.set_yticks([0, 25, 50, 75]); ax.set_yticklabels(['0', '25', '50', '75'], fontsize=15)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.978, 'twilight overhead, May to November 2022:', fontsize=14, color=INK2, va='top'); fig.text(0.015, 0.912, 'per cent brighter, each meter by latitude', fontsize=14, color=INK2, va='top')
fig.savefig(B + 'img/tonga-latitude.png', dpi=140, facecolor=SURF); plt.close(fig)
print(f'\npictures: img/tonga-months.png ({len(south)} southern photometers, their middle, and the middle of {len(north)} northern); img/tonga-latitude.png ({len(allp)} photometers; off the top: ' + ', '.join(st for lat, d, st in allp if pct(d) > 95) + ')')
