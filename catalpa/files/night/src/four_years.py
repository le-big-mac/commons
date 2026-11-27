# The four years together (2022 to 2025), by the frozen method's cleaned nights with two things settled after the fact:
#  - the photometer stars477 is placed at Arkaroola all through 2022 and 2023, where the checker's fit of its twilight
#    readings puts it (cache_placed/, made by years_cache_placed.py; the sealed score of the third sheet left those
#    files out because their headers give no position);
#  - a night whose level is more than 1 magnitude from the station's usual level in 2024 is left out (it removes ten
#    nights at Santa Cruz de La Palma in 2022 and 2023 and none elsewhere).
# Prints every figure the page's story uses, writes the table t_stations4.html, and draws the page's four pictures.
import pickle, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('sky', '/home/agent1/night/src/sky.py'); sky = importlib.util.module_from_spec(spec); spec.loader.exec_module(sky)
YEARS = (2022, 2023, 2024, 2025); N = []
_ref = pickle.load(open('/home/agent1/night/cache_placed/nights2024.pkl', 'rb')); LEV24 = {st: float(np.median([c['lev'] for c in _ref if c['st'] == st])) for st in {c['st'] for c in _ref}}
for y in YEARS:
    for c in pickle.load(open(f'/home/agent1/night/cache_placed/nights{y}.pkl', 'rb')):
        if abs(c['lev'] - LEV24[c['st']]) > 1.0: continue
        c['y'] = y; st = lambda t: ((sky.gmst_deg(sky.jd(t)) + c['lon']) % 360) / 15.0
        tm = c['dusk'] + dt.timedelta(hours=(c['tenth'] + 0.5) / 10 * c['L']); c['lst'] = st(tm); c['lst0'] = st(c['dusk']); c['lst1'] = st(c['dawn'])
        def sol(t):
            s = (t.hour + t.minute / 60 + t.second / 3600 + c['lon'] / 15.0) % 24; return s - 24 if s > 12 else s
        c['sol'] = sol(tm); c['s0'] = sol(c['dusk']); c['s1'] = sol(c['dawn']); c['doy'] = (c['d'] - dt.date(c['d'].year, 1, 1)).days; N.append(c)
ORDER = ['stars33', 'stars76', 'stars1', 'stars52', 'stars7', 'stars36', 'stars19', 'stars9', 'stars225', 'stars4', 'stars24', 'stars426', 'stars35', 'stars477', 'stars62', 'stars289']
CLS = {c['st']: c['cls'] for c in N}
NAME = {'stars33': "Madrid, by the ring road", 'stars76': "Valencia", 'stars1': "Coslada, beside Madrid", 'stars52': "Huércal de Almería", 'stars7': "Pamplona", 'stars36': "Northampton, Massachusetts", 'stars4': "Santa Cruz de La Palma", 'stars19': "Tucson, Arizona", 'stars9': "Añora, a village in Andalusia", 'stars225': "Morata de Jalón, a village in Aragon", 'stars24': "Temisas, Gran Canaria", 'stars426': "Teide Observatory, Tenerife", 'stars62': "Àger, Catalonia", 'stars35': "Otlica, Slovenia", 'stars477': "Arkaroola, South Australia", 'stars289': "Nerpio, in the mountains of Albacete"}
SHORT = {'stars33': "Madrid ring road", 'stars76': "Valencia", 'stars1': "Coslada", 'stars52': "Almería", 'stars7': "Pamplona", 'stars36': "Northampton, USA", 'stars4': "La Palma, a town", 'stars19': "Tucson, USA", 'stars9': "Añora, a village", 'stars225': "Morata, a village", 'stars24': "Temisas, Canaries", 'stars426': "Teide Observatory", 'stars62': "Àger, Catalonia", 'stars35': "Otlica, Slovenia", 'stars477': "Arkaroola, Australia", 'stars289': "Nerpio, Spain"}
def sh(v): v = list(v); return (100 * float(np.mean(v)), int(np.sum(v)), len(v)) if v else (float('nan'), 0, 0)
def f(s): return f'{s[0]:.0f} in 100 ({s[1]} of {s[2]})'
def rate(S):
    if len(S) < 20: return 'too few nights'
    x = np.array([c['doy'] for c in S], float); yv = np.array([c['sol'] for c in S]) * 60; a, b = np.polyfit(x, yv, 1); r = yv - (a * x + b)
    return f'{a:+.1f} minutes a day, give or take {np.sqrt(np.sum(r ** 2) / (len(S) - 2) / np.sum((x - x.mean()) ** 2)):.1f} ({len(S)} nights)'
def covers(c, h):
    a, b = c['lst0'], c['lst1']; mid = h + 1.0
    return (a <= mid <= b) if a <= b else (mid >= a or mid <= b)
def span(x, spans): return any(lo <= x < hi for lo, hi in spans)
print(f'FOUR YEARS, {len(N)} nights: ' + ', '.join(f"{y}: {sum(1 for c in N if c['y'] == y)}" for y in YEARS))
tn = np.array([c['tenth'] for c in N]); share = [100 * np.mean(tn == k) for k in range(10)]
print('A. which tenth was the darkest, nights in 100: ' + ', '.join(f'{x:.1f}' for x in share))
print(f'   the last tenth {f(sh(tn == 9))}; the ninth or the last {f(sh(tn >= 8))}; the last three {f(sh(tn >= 7))}; the first half {f(sh(tn < 5))}; the second half {f(sh(tn >= 5))}')
print('   by year, the last tenth: ' + '; '.join(f"{y}: {f(sh([c['tenth'] == 9 for c in N if c['y'] == y]))}" for y in YEARS))
print('   by year, the second half: ' + '; '.join(f"{y}: {f(sh([c['tenth'] >= 5 for c in N if c['y'] == y]))}" for y in YEARS))
print('   by kind of place, the last tenth: ' + '; '.join(f"{k}: {f(sh([c['tenth'] == 9 for c in N if c['cls'] == k]))}" for k in ('lit', 'between', 'dark')))
print('   by kind of place, the second half: ' + '; '.join(f"{k}: {f(sh([c['tenth'] >= 5 for c in N if c['cls'] == k]))}" for k in ('lit', 'between', 'dark')))
for k in ('lit', 'between', 'dark'): print(f'   {k}, the last tenth by year: ' + '; '.join(f"{y}: {f(sh([c['tenth'] == 9 for c in N if c['y'] == y and c['cls'] == k]))}" for y in YEARS))
print('\nB. the end of the night darker than its beginning (last half hour against first half hour)')
E = [c for c in N if c['ends']]
print(f"   all: {f(sh([c['dd'] > 0 for c in E]))}")
for k in ('lit', 'between', 'dark'): print(f"   {k}: {f(sh([c['dd'] > 0 for c in E if c['cls'] == k]))}; by year " + '; '.join(f"{y}: {f(sh([c['dd'] > 0 for c in E if c['cls'] == k and c['y'] == y]))}" for y in YEARS))
tab = []
print('   place by place: nights; last tenth the darkest; second half; end darker; by year (end darker)')
for st in ORDER:
    v = [c for c in N if c['st'] == st]; e = [c for c in v if c['ends']]; s = sh([c['dd'] > 0 for c in e])
    tab.append((st, len(v), sum(c['tenth'] == 9 for c in v), sum(c['tenth'] >= 5 for c in v), s))
    print(f"   {SHORT[st]:<22}{CLS[st]:<8}{len(v):>4} {tab[-1][2]:>4} {tab[-1][3]:>4}   {f(s):<22} " + '; '.join(f"{y}: {sh([c['dd'] > 0 for c in e if c['y'] == y])[1]} of {sh([c['dd'] > 0 for c in e if c['y'] == y])[2]}" for y in YEARS))
print('\nC. the five towns by season: the last tenth the darkest or within 0.02 magnitude of it; and the darkest outright')
for s in ('summer', 'between', 'winter'):
    v = [c for c in N if c['cls'] == 'lit' and c['season'] == s]; print(f"   {s}: within 0.02 {f(sh([c['near'] for c in v]))}; the darkest {f(sh([c['tenth'] == 9 for c in v]))}")
north = [c for c in N if c['lat'] > 0]; aut = lambda S: [c for c in S if 213 <= c['doy'] < 304]
print('\nD. how fast the darkest part moves by the Sun\'s clock, August to October (a patch fixed to the stars gives about -3; the clock about 0)')
for k in ('lit', 'between', 'dark'): print(f"   {k}: " + rate(aut([c for c in north if c['cls'] == k])))
for st in ORDER:
    S = aut([c for c in north if c['st'] == st]); print(f'   {SHORT[st]:<22}{CLS[st]:<8}' + rate(S))
nt = [c for c in north if c['cls'] != 'lit']; tw = [c for c in north if c['cls'] == 'lit']
print('\nE. star time, northern places not in towns (and the towns beside them)')
for lab, S in (('not in towns', nt), ('towns', tw)):
    print(f"   {lab}: dawn at star time 4-6 or 18-20 h, the last tenth the darkest on {f(sh([c['tenth'] == 9 for c in S if span(c['lst1'], ((4, 6), (18, 20)))]))}; dawn at 22-2 or 12-14 h: {f(sh([c['tenth'] == 9 for c in S if span(c['lst1'], ((22, 24), (0, 2), (12, 14)))]))}")
    print(f"   {lab}: darkest tenth at star time 0-2 h on {f(sh([0 <= c['lst'] < 2 for c in S if covers(c, 0)]))} of the nights that reach it; at 20-22 h on {f(sh([20 <= c['lst'] < 22 for c in S if covers(c, 20)]))}")
print('   by month, not in towns: nights / last tenth the darkest / middle clock hour of the darkest part (hours after midnight)')
print('   ' + '  '.join(f"{'JFMAMJJASOND'[m - 1]}:{sum(1 for c in nt if c['d'].month == m)}/{sum(1 for c in nt if c['d'].month == m and c['tenth'] == 9)}/{np.median([c['sol'] for c in nt if c['d'].month == m]):+.1f}" for m in range(1, 13)))
print('   by month, towns: ' + '  '.join(f"{'JFMAMJJASOND'[m - 1]}:{sum(1 for c in tw if c['d'].month == m)}/{sum(1 for c in tw if c['d'].month == m and c['tenth'] == 9)}/{np.median([c['sol'] for c in tw if c['d'].month == m]):+.1f}" for m in range(1, 13)))
print('   by month, the three northern dark places: ' + '  '.join(f"{'JFMAMJJASOND'[m - 1]}:{sum(1 for c in nt if c['cls'] == 'dark' and c['d'].month == m)}/{sum(1 for c in nt if c['cls'] == 'dark' and c['d'].month == m and c['tenth'] == 9)}" for m in range(1, 13)))
for lab, S in (('not in towns', nt), ('towns', tw)):
    print(f"   {lab}, the clock hour of the darkest part: scatter (half the spread between the 16th and 84th in 100) {np.subtract(*np.percentile([c['sol'] for c in S], [84, 16])) / 2:.1f} hours; middle {np.median([c['sol'] for c in S]):+.1f}; between 1 and 4 in the morning on {f(sh([1 <= c['sol'] < 4 for c in S]))}")
G = {'the three northern dark places': ('stars35', 'stars62', 'stars289'), 'Teide, Temisas and Añora': ('stars426', 'stars24', 'stars9'), 'the seven (four dark, and Teide, Temisas, Añora), northern six': ('stars35', 'stars62', 'stars289', 'stars426', 'stars24', 'stars9'),
     'Northampton, Tucson and La Palma': ('stars36', 'stars19', 'stars4'), 'Morata': ('stars225',), 'the five towns': ('stars33', 'stars76', 'stars1', 'stars52', 'stars7')}
print('\nF. groups of places (northern): the slide; the last tenth the darkest by where the Milky Way is at dawn; by month')
for lab, sts in G.items():
    S = [c for c in north if c['st'] in sts]
    print(f"   {lab} ({len(S)} nights): slide, August to October: " + rate(aut(S)))
    print(f"      dawn at star time 4-6 or 18-20 h: the last tenth the darkest on {f(sh([c['tenth'] == 9 for c in S if span(c['lst1'], ((4, 6), (18, 20)))]))}; dawn at 22-2 or 12-14 h: {f(sh([c['tenth'] == 9 for c in S if span(c['lst1'], ((22, 24), (0, 2), (12, 14)))]))}")
    print('      by month, nights / last tenth the darkest / middle clock hour: ' + '  '.join(f"{'JFMAMJJASOND'[m - 1]}:{sum(1 for c in S if c['d'].month == m)}/{sum(1 for c in S if c['d'].month == m and c['tenth'] == 9)}/" + (f"{np.median([c['sol'] for c in S if c['d'].month == m]):+.1f}" if any(c['d'].month == m for c in S) else '-') for m in range(1, 13)))
    print(f"      last tenth the darkest: August, December and January {f(sh([c['tenth'] == 9 for c in S if c['d'].month in (8, 12, 1)]))}; July {f(sh([c['tenth'] == 9 for c in S if c['d'].month == 7]))}; March to June {f(sh([c['tenth'] == 9 for c in S if c['d'].month in (3, 4, 5, 6)]))}; September and October {f(sh([c['tenth'] == 9 for c in S if c['d'].month in (9, 10)]))}; all {f(sh([c['tenth'] == 9 for c in S]))}")
    print(f"      the clock hour of the darkest part: between 1 and 4 in the morning on {f(sh([1 <= c['sol'] < 4 for c in S]))}; correlation with the Milky Way's distance, middle night {float(np.median([np.corrcoef(c['mt'], c['gb'])[0, 1] for c in S])):+.2f}")
d3n = [c for c in north if c['st'] in G['the three northern dark places']]
for lab, sp in (('dawn at star time 22 to 2 h', ((22, 24), (0, 2))), ('dawn at 12 to 14 h', ((12, 14),)), ('dawn at 4 to 6 h', ((4, 6),)), ('dawn at 18 to 20 h', ((18, 20),))):
    S = sorted([c for c in d3n if span(c['lst1'], sp)], key=lambda c: ((c['d'].month + 6) % 12 if sp == ((12, 14),) else c['d'].month, c['d'].day))
    print(f"   the three northern dark places, {lab}: {len(S)} nights, the last tenth the darkest on {sum(c['tenth'] == 9 for c in S)}; dates from {S[0]['d'].strftime('%d %b')} to {S[-1]['d'].strftime('%d %b')}")
print(f"   night length over all nights: {min(c['L'] for c in N):.1f} to {max(c['L'] for c in N):.1f} hours, so a tenth is {6 * min(c['L'] for c in N):.0f} to {6 * max(c['L'] for c in N):.0f} minutes")
ark = [c for c in N if c['st'] == 'stars477']
print(f"   Arkaroola ({len(ark)} nights): of nights whose dark hours take in star time 18 h, the darkest tenth at 16 to 20 h on {f(sh([16 <= c['lst'] < 20 for c in ark if covers(c, 17)]))}; by year " + ', '.join(f"{y}: {sum(1 for c in ark if c['y'] == y)}" for y in YEARS))
cd = lambda S: float(np.median([np.corrcoef(c['mt'], c['gb'])[0, 1] for c in S]))
print(f"   the night's ten parts against the distance from the Milky Way's plane (correlation, middle night): dark {cd([c for c in N if c['cls'] == 'dark']):+.2f}; between {cd([c for c in N if c['cls'] == 'between']):+.2f}; towns {cd([c for c in N if c['cls'] == 'lit']):+.2f}")
print('   the same by place: ' + '; '.join(f"{SHORT[st]} {cd([c for c in N if c['st'] == st]):+.2f}" for st in ORDER))
print('   brightest tenth less darkest tenth, middle night, magnitudes: ' + '; '.join(f"{k} {np.median([max(c['mt']) - min(c['mt']) for c in N if c['cls'] == k]):.2f}" for k in ('lit', 'between', 'dark')))
# ---- the table
lev24 = LEV24
rows = ['<tr><th>place</th><th class="n">level in 2024</th><th class="n">nights</th><th class="n">the last tenth the darkest</th><th class="n">darkest tenth in the second half</th><th class="n">darker before dawn than after dusk</th></tr>']
for r in tab: rows.append(f'<tr><td>{NAME[r[0]]}</td><td class="n">{lev24[r[0]]:.1f}</td><td class="n">{r[1]}</td><td class="n">{r[2]}</td><td class="n">{r[3]}</td><td class="n">{r[4][1]} of {r[4][2]}</td></tr>')
open('/home/agent1/night/t_stations4.html', 'w', encoding='utf-8').write('<div class="tablewrap"><table>\n' + '\n'.join(rows) + '\n</table></div>\n')
# ---- the pictures
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'; ORANGE = '#eb6834'
fig = plt.figure(figsize=(5.0, 3.7), facecolor=SURF); ax = fig.add_axes([0.115, 0.135, 0.865, 0.745]); ax.set_facecolor(SURF)
ax.bar(np.arange(10) + 0.5, share, width=0.86, color=BLUE, zorder=3)
ax.text(9.5, share[9] + 0.6, f'{share[9]:.0f}', fontsize=14, color=INK, ha='center', va='bottom', fontweight='bold')
ax.set_xlim(0, 10); ax.set_ylim(0, 24); ax.set_yticks([0, 5, 10, 15, 20]); ax.set_xticks([0, 5, 10]); ax.set_xticklabels(['end of dusk', 'middle of the night', 'start of dawn'], fontsize=13)
for lab, ha in zip(ax.get_xticklabels(), ('left', 'center', 'right')): lab.set_ha(ha)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0, labelsize=13)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.975, 'nights in 100 on which each tenth was the darkest', fontsize=12.5, color=INK2, va='top')
fig.savefig('/home/agent1/night/img/dawn-tenths-4y.png', dpi=140, facecolor=SURF); plt.close(fig)
groups = [("five Spanish towns", [r for r in tab if CLS[r[0]] == 'lit']), ("seven places in between", [r for r in tab if CLS[r[0]] == 'between']), ("the four darkest skies", [r for r in tab if CLS[r[0]] == 'dark'])]
fig = plt.figure(figsize=(5.0, 7.3), facecolor=SURF); ax = fig.add_axes([0.50, 0.075, 0.47, 0.875]); ax.set_facecolor(SURF)
y = 0.0; ticks = []; labs = []
for gname, g in groups:
    ax.text(34.0, -y, gname, fontsize=12.5, color=INK2, style='italic', ha='right', va='center', clip_on=False); y += 1.0
    for r in g:
        ax.plot([50, r[4][0]], [-y, -y], color=BLUE, lw=2.4, alpha=0.35, solid_capstyle='round', zorder=3); ax.plot([r[4][0]], [-y], 'o', ms=10, color=BLUE, mec=SURF, mew=1.4, zorder=4); ticks.append(-y); labs.append(SHORT[r[0]]); y += 1.0
    y += 0.6
ax.axvline(50, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=2); ax.text(51.0, 0.75, 'a coin toss', fontsize=12.5, color=INK2, va='center', ha='left', bbox=dict(facecolor=SURF, edgecolor='none', pad=1.0), zorder=5)
ax.set_yticks(ticks); ax.set_yticklabels(labs, fontsize=12.5, color=INK); ax.set_ylim(-y + 0.9, 1.2); ax.set_xlim(35, 104); ax.set_xticks([50, 75, 100]); ax.set_xticklabels(['50', '75', '100'], fontsize=13)
ax.grid(True, axis='x', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.99, 'nights in 100 darker before dawn than after dusk', fontsize=12.5, color=INK2, va='top')
fig.savefig('/home/agent1/night/img/dawn-places-4y.png', dpi=140, facecolor=SURF); plt.close(fig)
def guide(T):
    xs, ys = [], []
    for k in range(365):
        d0 = dt.datetime(2023, 1, 1) + dt.timedelta(days=k + 1); l0 = sky.gmst_deg(sky.jd(d0)) / 15.0; xs.append(k + 0.5); ys.append(((T - l0 + 12) % 24 - 12) / 1.0027379)
    return np.array(xs), np.array(ys)
MON = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
def draw(S, col, fn, title, lines):
    fig = plt.figure(figsize=(5.0, 4.7), facecolor=SURF); ax = fig.add_axes([0.2, 0.095, 0.78, 0.765]); ax.set_facecolor(SURF)
    for c in S: ax.plot([c['doy'] + 0.5] * 2, [c['s0'], c['s1']], color='#e0dfda', lw=0.7, zorder=2, solid_capstyle='butt')
    for T in ((1.0, 13.0) if lines else ()):
        xs, ys = guide(T); brk = np.where(np.abs(np.diff(ys)) > 6)[0]; a = 0
        for b in list(brk) + [len(xs) - 1]:
            ax.plot(xs[a:b + 1], ys[a:b + 1], color=INK2, lw=1.3, ls=(0, (4, 3)), zorder=3); a = b + 1
    ax.plot([c['doy'] + 0.5 for c in S], [c['sol'] for c in S], 'o', ms=5.0, color=col, mec=SURF, mew=0.6, zorder=4, alpha=0.9)
    ax.set_xlim(-4, 369); ax.set_ylim(7.2, -7.2); ax.set_yticks([-6, -3, 0, 3, 6]); ax.set_yticklabels(['6 pm', '9 pm', 'midnight', '3 am', '6 am'], fontsize=12.5)
    ax.set_xticks([m + 15 for m in MON]); ax.set_xticklabels(list('JFMAMJJASOND'), fontsize=12.5)
    for m in MON[1:]: ax.axvline(m, color=GRID, lw=1, zorder=1)
    ax.axhline(0, color=GRID, lw=1, zorder=1); ax.tick_params(colors=INK2, length=0)
    for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
    ax.spines['bottom'].set_color(INK2)
    fig.text(0.015, 0.975, title, fontsize=12.5, color=INK2, va='top')
    box = dict(facecolor=SURF, edgecolor='none', pad=1.5)
    ax.text(78, -6.35, 'end of dusk', fontsize=12.5, color=INK2, ha='center', va='center', bbox=box, zorder=5)
    ax.text(292, 6.25, 'start of dawn', fontsize=12.5, color=INK2, ha='center', va='center', bbox=box, zorder=5)
    if lines: fig.text(0.015, 0.925, 'dashed lines: the same sky overhead', fontsize=12.5, color=INK2, va='top')
    fig.savefig(fn, dpi=140, facecolor=SURF); plt.close(fig)
d3 = [c for c in north if c['st'] in G['the three northern dark places']]
draw(d3, BLUE, '/home/agent1/night/img/dawn-stars.png', 'when each night was darkest: three dark skies', True)
draw(tw, ORANGE, '/home/agent1/night/img/dawn-towns.png', 'when each night was darkest: five towns', False)
print(f'\npictures: dawn-tenths-4y.png, dawn-places-4y.png ({len(N)} nights); dawn-stars.png ({len(d3)} nights at the three northern dark places); dawn-towns.png ({len(tw)} nights in the five towns)')
