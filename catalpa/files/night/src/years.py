# The two years side by side, by the frozen method (dawnlib.py): the figures of the page for 2024 and 2025, each place's
# rows and its usual level in both years (to see whether an instrument changed between them), and the picture
# img/dawn-years.png. Written after the 2025 sheet was scored; nothing here was sealed.
import sys, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
Y = {2024: D.load(2024, '/home/agent1/night/data/ida'), 2025: D.load(2025, '/home/agent1/night/data/ida2025')}
F = {y: D.figures(Y[y]) for y in Y}
print('the two years by the frozen method (cleaned nights)')
for y in Y:
    f = F[y]; n = f['nights']
    print(f"{y}: nights {n}; last tenth the darkest {f['last']:.1f} in 100; second half {f['second']:.1f}; by tenth, in 100: " + ' '.join(f'{100 * k / n:.1f}' for k in f['by_tenth']))
    print(f"      last three tenths together {100 * sum(f['by_tenth'][7:]) / n:.1f}; first half {100 * sum(f['by_tenth'][:5]) / n:.1f}; ninth tenth {100 * f['by_tenth'][8] / n:.1f}")
    for k in ('lit', 'between', 'dark'): print(f"      end darker than beginning, {k}: {f['before_' + k][0]:.0f} in 100 ({f['before_' + k][1]} of {f['before_' + k][2]})")
    print(f"      Nerpio and Arkaroola {f['before_two_darkest'][0]:.0f} ({f['before_two_darkest'][1]} of {f['before_two_darkest'][2]}); Otlica and Àger {f['before_otlica_ager'][0]:.0f} ({f['before_otlica_ager'][1]} of {f['before_otlica_ager'][2]})")
    print(f"      towns in summer, last tenth darkest or within 0.02: {f['towns_summer'][0]:.0f} ({f['towns_summer'][1]} of {f['towns_summer'][2]}); in winter {f['towns_winter'][0]:.0f} ({f['towns_winter'][1]} of {f['towns_winter'][2]})")
    print('      Milky Way: ' + '; '.join(f"{D.NAME[s]} {v[0]:.0f} ({v[1]} nights)" for s, v in f['milky'].items()))
both = [c for y in Y for c in Y[y] if c['clean']]; tn = np.array([D.tenth(c)[0] for c in both])
print(f"both years together: nights {len(both)}; last tenth the darkest {100 * np.mean(tn == 9):.1f} in 100; second half {100 * np.mean(tn >= 5):.1f}")
print()
print('place by place: cleaned nights; last tenth the darkest; darkest tenth in the second half; end darker than beginning; usual level by the file\'s own formula')
print(f"{'':<20}{'2024':<34}{'2025':<34}level 2025 less 2024")
order = [s for k in ('lit', 'between', 'dark') for s in D.CLASS if D.CLASS[s] == k]
lev = {}
for y in Y:
    for s in order:
        v = [float(np.median(c['m']) - c['off']) for c in Y[y] if c['clean'] and c['st'] == s]; lev[(y, s)] = float(np.median(v)) if v else float('nan')
for s in order:
    row = f"{D.NAME[s]:<20}"
    for y in Y:
        r = F[y]['stations'].get(s)
        row += (f"{r[0]:>3} {r[1]:>3} {r[2]:>3}  {r[3][1]:>3} of {r[3][2]:<3} {lev[(y, s)]:6.2f}      " if r else f"{'no nights':<34}")
    print(row + f"{lev[(2025, s)] - lev[(2024, s)]:+.2f}")
print()
print('by month (cleaned nights; of them, last tenth the darkest), all places')
for y in Y:
    cl = [c for c in Y[y] if c['clean']]
    print(f"{y}: " + ' '.join(f"{m}:{sum(1 for c in cl if c['d'].month == m)}/{sum(1 for c in cl if c['d'].month == m and D.tenth(c)[0] == 9)}" for m in range(1, 13)))
print('by class (cleaned nights; last tenth the darkest; in 100)')
for y in Y:
    cl = [c for c in Y[y] if c['clean']]
    print(f"{y}: " + '; '.join(f"{k} {sum(1 for c in cl if D.CLASS[c['st']] == k)}, {sum(1 for c in cl if D.CLASS[c['st']] == k and D.tenth(c)[0] == 9)}, {100 * np.mean([D.tenth(c)[0] == 9 for c in cl if D.CLASS[c['st']] == k]):.0f}" for k in ('lit', 'between', 'dark')))
# what 2024 would give with 2025's mix of places, and the other way: each place's share weighted by the other year's nights
for a, b in ((2024, 2025), (2025, 2024)):
    num = den = 0.0
    for s in order:
        ra, rb = F[a]['stations'].get(s), F[b]['stations'].get(s)
        if ra and rb: num += rb[0] * ra[1] / ra[0]; den += rb[0]
    print(f"{a}'s place-by-place shares for the last tenth, weighted by {b}'s nights at each place: {100 * num / den:.1f} in 100 (places with nights in both years)")
# the chance spread of a share of this size on this many nights (binomial, nights taken as independent, which they are not quite)
for y in Y:
    n = F[y]['nights']; p = F[y]['last'] / 100; print(f"{y}: {F[y]['last']:.1f} in 100 on {n} nights, give or take {100 * (p * (1 - p) / n) ** 0.5:.1f} if nights were independent draws")

import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF = '#fcfcfb'; INK = '#1f2328'; INK2 = '#5c6166'; GRID = '#e6e6e3'; BLUE = '#2a78d6'; ORANGE = '#eb6834'
fig = plt.figure(figsize=(5.0, 3.9), facecolor=SURF); ax = fig.add_axes([0.115, 0.13, 0.865, 0.68]); ax.set_facecolor(SURF)
for y, col, dx in ((2024, BLUE, -0.21), (2025, ORANGE, 0.21)):
    sh = np.array(F[y]['by_tenth']) * 100.0 / F[y]['nights']
    ax.bar(np.arange(10) + 0.5 + dx, sh, width=0.38, color=col, zorder=3)
    ax.text(9.5 + dx, sh[9] + 0.5, f'{sh[9]:.0f}', fontsize=12.5, color=INK, ha='center', va='bottom', fontweight='bold')
ax.set_xlim(0, 10); ax.set_ylim(0, 24); ax.set_yticks([0, 5, 10, 15, 20]); ax.set_xticks([0, 5, 10]); ax.set_xticklabels(['end of dusk', 'middle of the night', 'start of dawn'], fontsize=13)
for lab, ha in zip(ax.get_xticklabels(), ('left', 'center', 'right')): lab.set_ha(ha)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0, labelsize=13)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.975, 'nights in 100 on which each tenth was the darkest', fontsize=12.5, color=INK2, va='top')
for x, col, lab in ((0.03, BLUE, f"2024, {F[2024]['nights']} nights"), (0.42, ORANGE, f"2025, {F[2025]['nights']} nights")):
    fig.patches.append(matplotlib.patches.Rectangle((x, 0.862), 0.028, 0.036, transform=fig.transFigure, color=col)); fig.text(x + 0.04, 0.88, lab, fontsize=12.5, color=INK, va='center')
fig.savefig('/home/agent1/night/img/dawn-years.png', dpi=140, facecolor=SURF)
print('\nwrote img/dawn-years.png')
