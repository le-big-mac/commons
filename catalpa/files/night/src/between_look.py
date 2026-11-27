# What the even months show beyond the eighth sheet's lines: a description made after the score was known, not a test.
# Every month of 2022 and 2023 at the eleven southern photometers of the page (the ten of the sheet and Arkaroola, whose
# every month was already in hand) and at the twenty northern ones that have every month (the fifteen northern ones of
# the dawn page and the five of the sheet). Draws the page's first picture again with every month in it.
import importlib.util, io, contextlib
import numpy as np
spec = importlib.util.spec_from_file_location('between', '/home/agent1/night/src/between.py'); BT = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(BT)
geo = BT.geo; B = BT.B
SOUTH = BT.SOUTH + ['stars477']; NAME = dict(BT.NAME, stars477='Arkaroola')
NORTH = BT.NORTH + ['stars1', 'stars19', 'stars225', 'stars24', 'stars289', 'stars33', 'stars35', 'stars36', 'stars4', 'stars426', 'stars52', 'stars62', 'stars7', 'stars76', 'stars9']
A = {st: BT.series(st) for st in SOUTH + NORTH}; lat = {st: float(geo[st]['latitude']) for st in SOUTH + NORTH}
def pct(mag): return 100 * (10 ** (-0.4 * mag) - 1)
MON = [(y, m) for y in (2021, 2022, 2023, 2024) for m in range(1, 13)]; M2 = [k for k in MON if k[0] in (2022, 2023)]
def mid(group, k):
    v = [A[st][k] for st in group if k in A[st]]; return (float(np.median(v)), len(v)) if v else (None, 0)
order = sorted(SOUTH, key=lambda s: -lat[s])
print('A. the eleven southern photometers, every month of 2022 and 2023 (hundredths of a magnitude; negative: a brighter twilight), from the tropics southward')
for st in order:
    print(f"   {NAME[st]:<14} {lat[st]:+6.1f}  " + ' | '.join(' '.join(f"{100 * A[st][(y, m)]:+4.0f}" if (y, m) in A[st] else '   .' for m in range(1, 13)) for y in (2022, 2023)))
print('   the middle             ' + ' | '.join(' '.join(f"{100 * mid(SOUTH, (y, m))[0]:+4.0f}" for m in range(1, 13)) for y in (2022, 2023)))
print('   the middle, per cent   ' + ' | '.join(' '.join(f"{pct(mid(SOUTH, (y, m))[0]):+4.0f}" for m in range(1, 13)) for y in (2022, 2023)))
print('   at -0.10 or below      ' + ' | '.join(' '.join(f"{sum(1 for st in SOUTH if (y, m) in A[st] and A[st][(y, m)] <= -0.10):4d}" for m in range(1, 13)) for y in (2022, 2023)))
print('   have the month         ' + ' | '.join(' '.join(f"{mid(SOUTH, (y, m))[1]:4d}" for m in range(1, 13)) for y in (2022, 2023)))
print('\nB. when it came and went, place by place: the first month of 2022 at -0.10 or below; the first of two months in a row; the brightest month; the last month of two in a row at -0.10 or below')
first2 = {}
for st in order:
    ks = [k for k in M2 if k in A[st]]; f1 = next((k for k in ks if A[st][k] <= -0.10), None)
    f2 = next((k for i, k in enumerate(ks[:-1]) if A[st][k] <= -0.10 and A[st][ks[i + 1]] <= -0.10 and (ks[i + 1][0] * 12 + ks[i + 1][1]) - (k[0] * 12 + k[1]) == 1), None)
    l2 = next((ks[i + 1] for i in range(len(ks) - 2, -1, -1) if A[st][ks[i]] <= -0.10 and A[st][ks[i + 1]] <= -0.10 and (ks[i + 1][0] * 12 + ks[i + 1][1]) - (ks[i][0] * 12 + ks[i][1]) == 1), None)
    pk = min(ks, key=lambda k: A[st][k]); first2[st] = f2
    fm = lambda k: f'{k[0]}-{k[1]:02d}' if k else '   -   '
    miss = [f'{k[0]}-{k[1]:02d}' for k in M2 if k not in A[st] and k <= (2022, 6)]
    print(f"   {NAME[st]:<14} {lat[st]:+6.1f}   first {fm(f1)}   first of two {fm(f2)}   brightest {fm(pk)} ({100 * A[st][pk]:+.0f})   last of two {fm(l2)}" + (f"   (no figure for {', '.join(miss)})" if miss else ''))
have = [st for st in order if first2[st]]
x = np.array([-lat[st] for st in have]); y = np.array([first2[st][0] * 12 + first2[st][1] for st in have], float)
def rank(v): r = np.empty(len(v)); o = np.argsort(v, kind='stable'); r[o] = np.arange(len(v)); return np.array([np.mean(r[v == t]) for t in v])
rho = float(np.corrcoef(rank(x), rank(y))[0, 1]); print(f'   rank correlation between degrees south and the first of two months, {len(have)} places: {rho:+.2f}')
print('\nC. the twenty northern photometers with every month: the middle by month of 2022 and 2023 (hundredths), and how many stand beyond 0.10 either way')
print('   the middle     ' + ' | '.join(' '.join(f"{100 * mid(NORTH, (y, m))[0]:+4.0f}" for m in range(1, 13)) for y in (2022, 2023)))
print('   brighter 0.10+ ' + ' | '.join(' '.join(f"{sum(1 for st in NORTH if (y, m) in A[st] and A[st][(y, m)] <= -0.10):4d}" for m in range(1, 13)) for y in (2022, 2023)))
print('   darker 0.10+   ' + ' | '.join(' '.join(f"{sum(1 for st in NORTH if (y, m) in A[st] and A[st][(y, m)] >= 0.10):4d}" for m in range(1, 13)) for y in (2022, 2023)))
print('   have the month ' + ' | '.join(' '.join(f"{mid(NORTH, (y, m))[1]:4d}" for m in range(1, 13)) for y in (2022, 2023)))
print('\nD. the even months that do not lie between their neighbours widened by 0.10 (line V10), the ten of the sheet')
missm = {}
for st in BT.SOUTH:
    a = A[st]
    for (yy, m) in M2:
        if m % 2 or not ((2022, 2) <= (yy, m) <= (2023, 10)): continue
        i = yy * 12 + m - 1; p = ((i - 1) // 12, (i - 1) % 12 + 1); q = ((i + 1) // 12, (i + 1) % 12 + 1)
        if (yy, m) in a and p in a and q in a and not (min(a[p], a[q]) - 0.10 <= a[(yy, m)] <= max(a[p], a[q]) + 0.10): missm.setdefault((yy, m), []).append(f"{NAME[st]} {100 * a[(yy, m)]:+.0f} (neighbours {100 * a[p]:+.0f}, {100 * a[q]:+.0f})")
for k in sorted(missm): print(f"   {k[0]}-{k[1]:02d}: " + '; '.join(missm[k]))
print('\nE. the comparison years each southern photometer has: months of the year with both 2021 and 2024, with 2021 alone, with 2024 alone')
R = BT.R
for st in order:
    V = {}
    for (s, yy, m), r in R.items():
        if s == st and r is not None and BT.TW.month_value(r): V[(yy, m)] = 1
    # months as the series sees them: use the anomalies' own years
    both = sum(1 for m in range(1, 13) if (2021, m) in A[st] and (2024, m) in A[st]); o21 = sum(1 for m in range(1, 13) if (2021, m) in A[st] and (2024, m) not in A[st]); o24 = sum(1 for m in range(1, 13) if (2024, m) in A[st] and (2021, m) not in A[st])
    print(f"   {NAME[st]:<14} both {both:2d}   2021 alone {o21:2d}   2024 alone {o24:2d}")
print('\nF. October 2022 and December 2023 with their neighbours, each southern photometer (hundredths)')
for st in order:
    g = lambda k: f"{100 * A[st][k]:+4.0f}" if k in A[st] else '   .'
    print(f"   {NAME[st]:<14} Sep, Oct, Nov 2022: {g((2022, 9))} {g((2022, 10))} {g((2022, 11))}     Nov, Dec 2023: {g((2023, 11))} {g((2023, 12))}     the same Decembers apart, 2021 and 2024: {g((2021, 12))} {g((2024, 12))}")
print('\nG. has it stayed away? The four southern photometers with later years: each month less the mean of the same month in every year but 2022 and 2023 (hundredths; negative: brighter)')
def rawseries(st):
    chips = {}
    for (s_, y, m), r in R.items():
        if s_ == st and r is not None and BT.TW.month_value(r): chips.setdefault(BT.TS.chip(r), []).append((y, m))
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; sl = []
    for (s_, y, m), r in R.items():
        if s_ != st or r is None or BT.TS.chip(r) != ch: continue
        mv = BT.TW.month_value(r)
        if mv: V[(y, m)] = mv[0]; sl += r['sl']
    return V, abs(float(np.median(sl)))
later = []
for st in ('stars477', 'stars456', 'stars221', 'stars29'):
    V, sl_ = rawseries(st); years = sorted({y for y, m in V})
    for y in years:
        row = []
        for m in range(1, 13):
            base = [V[(yy, m)] for yy in years if (yy, m) in V and yy not in (2022, 2023)]
            ok = (y, m) in V and len(base) >= 2; val = 100 * sl_ * (V[(y, m)] - np.mean(base)) if ok else None
            row.append(f"{val:+4.0f}" if ok else '   .')
            if ok and y >= 2025: later.append(val)
        if y >= 2021: print(f"   {NAME[st]:<12} {y} " + ' '.join(row))
print(f'   months of 2025 and 2026 at the four: {len(later)}; the middle {np.median(later):+.0f}; within 10 of nothing: {sum(1 for v in later if abs(v) <= 10)}; the brightest {min(later):+.0f}, the darkest {max(later):+.0f}')
print('\nH. the same figures from the clearest twilights only: in place of the middle crossing of each month, the quarter-point on the bright side (the 25th percentile of the Sun\'s altitude at the crossing, evening and morning apart, five crossings or more of each), in every month alike')
def qseries(st):
    chips = {}
    for (s_, y, m), r in R.items():
        if s_ == st and r is not None and BT.TW.month_value(r): chips.setdefault(BT.TS.chip(r), []).append((y, m))
    if not chips: return {}
    ch = max(chips, key=lambda c: len(chips[c])); V = {}; sl = []
    for (s_, y, m), r in R.items():
        if s_ != st or r is None or BT.TS.chip(r) != ch or len(r['ev']) < 5 or len(r['mo']) < 5: continue
        V[(y, m)] = 0.5 * (np.percentile(r['ev'], 25) + np.percentile(r['mo'], 25)); sl += r['sl']
    sl_ = abs(float(np.median(sl))); out = {}
    for (y, m), v in V.items():
        base = [V[(yy, m)] for yy in (2021, 2024) if (yy, m) in V]
        if base: out[(y, m)] = sl_ * (v - float(np.mean(base)))
    return out
Q = {st: qseries(st) for st in SOUTH}
def qmid(k):
    v = [Q[st][k] for st in SOUTH if k in Q[st]]; return float(np.median(v)) if v else float('nan')
print('   the middle of the eleven   ' + ' | '.join(' '.join(f"{100 * qmid((y, m)):+4.0f}" for m in range(1, 13)) for y in (2022, 2023)))
print('   as the page reckons it     ' + ' | '.join(' '.join(f"{100 * mid(SOUTH, (y, m))[0]:+4.0f}" for m in range(1, 13)) for y in (2022, 2023)))
print('   October 2022, the five places from 32 to 41 degrees south, clearest quarter (and as the page reckons it): ' + '; '.join(f"{NAME[st]} {100 * Q[st][(2022, 10)]:+.0f} ({100 * A[st][(2022, 10)]:+.0f})" for st in ('stars456', 'stars220', 'stars215', 'stars29', 'stars634') if (2022, 10) in Q[st]))
print('   December 2023, each place, clearest quarter (and as the page reckons it): ' + '; '.join(f"{NAME[st]} {100 * Q[st][(2023, 12)]:+.0f} ({100 * A[st][(2023, 12)]:+.0f})" for st in order if (2023, 12) in Q[st]))
print('   January 2022, each place, clearest quarter (and as the page reckons it): ' + '; '.join(f"{NAME[st]} {100 * Q[st][(2022, 1)]:+.0f} ({100 * A[st][(2022, 1)]:+.0f})" for st in order if (2022, 1) in Q[st]))
print('\nI. the score of the eighth sheet (verdicts as between.out prints them)')
odds = dict(V1=.90, V2=.70, V3=.70, V4=.60, V5=.65, V6=.75, V7=.60, V8=.55, V9=.80, V10=.70, V11=.65); verd = {}
for line in open(B + 'between.out', encoding='utf-8'):
    if line[:1] == 'V' and '.' in line[:4]: verd[line.split('.')[0]] = line.rstrip().rsplit(': ', 1)[-1]
print('   ' + ', '.join(f'{k} {verd[k]}' for k in odds))
scored = [k for k in odds if verd[k] in ('held', 'failed')]
print(f"   lines scored: {len(scored)}; held {sum(1 for k in scored if verd[k] == 'held')}; my odds expected {sum(odds[k] for k in scored):.1f} to hold; Brier score {np.mean([(odds[k] - (verd[k] == 'held')) ** 2 for k in scored]):.3f} (0.250 for odds of one in two on every line)")
print('\nJ. the longest run of months in a row at -0.10 or below, 2022 and 2023, each photometer with every month')
def longest(st, W=None):
    a = W if W is not None else A[st]; best = 0; run = 0; prev = None
    for k in M2:
        i = k[0] * 12 + k[1]
        if k in a and a[k] <= -0.10: run = run + 1 if (prev is not None and i - prev == 1) else 1; prev = i; best = max(best, run)
        else: run = 0; prev = None
    return best
ls = {st: longest(st) for st in SOUTH}; ln = {st: longest(st) for st in NORTH}
print('   south: ' + ', '.join(f"{NAME[st]} {ls[st]}" for st in order))
print('   north: ' + ', '.join(f"{st} {ln[st]}" for st in NORTH))
print(f'   the eleven southern: {sum(1 for v in ls.values() if v >= 5)} with a run of five months or more (the shortest {min(ls.values())}, the longest {max(ls.values())}); the twenty northern: {sum(1 for v in ln.values() if v >= 3)} with three or more ({", ".join(st for st, v in ln.items() if v >= 3)}), {sum(1 for v in ln.values() if v >= 4)} with four or more, {sum(1 for v in ln.values() if v >= 5)} with five or more')
# ---- the page's first picture again, with every month
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SURF, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'; BLUE = '#2a78d6'; ORANGE = '#eb6834'
xx = {k: (k[0] - 2021) + (k[1] - 0.5) / 12 for k in MON}
fig = plt.figure(figsize=(5.0, 4.0), facecolor=SURF); ax = fig.add_axes([0.135, 0.12, 0.845, 0.68]); ax.set_facecolor(SURF)
for st in SOUTH:
    ks = [k for k in MON if k in A[st]]; run = []   # a line only between months next to each other; a month standing alone is a dot
    for k in ks + [None]:
        if run and (k is None or (k[0] * 12 + k[1]) - (run[-1][0] * 12 + run[-1][1]) != 1):
            ax.plot([xx[q] for q in run], [pct(A[st][q]) for q in run], color='#c9d8ee', lw=0.9, zorder=2, marker='o' if len(run) == 1 else None, ms=2.5); run = []
        if k is not None: run.append(k)
ks = [k for k in MON if mid(NORTH, k)[1] >= 8]; ax.plot([xx[k] for k in ks], [pct(mid(NORTH, k)[0]) for k in ks], color=ORANGE, lw=2.0, zorder=4)
ks = [k for k in MON if mid(SOUTH, k)[1] >= 5]; ax.plot([xx[k] for k in ks], [pct(mid(SOUTH, k)[0]) for k in ks], color=BLUE, lw=2.6, zorder=5)
ax.axhline(0, color=INK2, lw=1.0, zorder=3); ax.axvline(1 + 14.5 / 365, color=INK2, lw=1.2, ls=(0, (4, 3)), zorder=3)
ax.text(1 + 14.5 / 365 - 0.05, -31, 'eruption,\n15 Jan 2022', fontsize=13, color=INK2, ha='right', va='top')
ax.plot([2.42, 2.60], [112, 112], color=BLUE, lw=3.2, zorder=6, solid_capstyle='round'); ax.text(2.67, 112, 'south', fontsize=14.5, color=INK, ha='left', va='center')
ax.plot([2.42, 2.60], [90, 90], color=ORANGE, lw=2.6, zorder=6, solid_capstyle='round'); ax.text(2.67, 90, 'north', fontsize=14.5, color=INK, ha='left', va='center')
top = max(pct(A[st][k]) for st in SOUTH for k in A[st]); bot = min(pct(A[st][k]) for st in SOUTH for k in A[st])
ax.set_xlim(0, 4); ax.set_ylim(min(-66, bot - 5), max(118, top + 6)); ax.set_xticks([0.5, 1.5, 2.5, 3.5]); ax.set_xticklabels(['2021', '2022', '2023', '2024'], fontsize=15)
yt = [t for t in (0, 50, 100, 150) if t < max(118, top + 6)]; ax.set_yticks(yt); ax.set_yticklabels([str(t) for t in yt], fontsize=15)
for v in (1, 2, 3): ax.axvline(v, color=GRID, lw=1, zorder=1)
ax.grid(True, axis='y', color=GRID, lw=1); ax.set_axisbelow(True); ax.tick_params(colors=INK2, length=0)
for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
ax.spines['bottom'].set_color(INK2)
fig.text(0.015, 0.978, 'twilight overhead: per cent brighter', fontsize=14, color=INK2, va='top'); fig.text(0.015, 0.912, 'than the same month of 2021 and 2024', fontsize=14, color=INK2, va='top')
fig.savefig(B + 'img/tonga-every-month.png', dpi=140, facecolor=SURF); plt.close(fig)
print(f'\npicture: img/tonga-every-month.png ({len(SOUTH)} southern photometers month by month, their middle, and the middle of {len(NORTH)} northern; the highest single month {top:.0f} per cent, the lowest {bot:.0f})')
