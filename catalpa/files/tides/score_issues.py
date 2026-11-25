# Score the daily issues (issues/<id>/) against observations that did not exist when each was made.  Written on 25 Nov 2026 before the first issue.
# usage: python -I score_issues.py [as-of 'YYYY-MM-DD HH:MM']     (fetch first: ./daily.sh fetchonly).  An issue counts once its 72 hours have passed with >= 90% of the hours observed.
# Errors are hourly, by lead time = hours since the last observation the issue used.
#   mine = my tide + my carried offset;  NOAA+ = NOAA's prediction + the same recipe of carried offset;  published = NOAA's prediction alone.
import numpy as np, sys, os, csv, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tide import load_noaa, when, day_of, STATIONS
BINS = ((0, 12), (12, 24), (24, 48), (48, 72)); rms = lambda v: 100 * np.sqrt(np.mean(np.asarray(v) ** 2)) if len(v) else np.nan
asof = day_of(sys.argv[1]) if len(sys.argv) > 1 else None
OBS = {st: load_noaa(st, 'water_level') for st in STATIONS}
pool = {st: {k: [] for k in ('lead', 'mine', 'noaa', 'pub')} for st in STATIONS}; ratios = {st: [] for st in STATIONS}; counted = []
for d in sorted(glob.glob(os.environ.get('ISSUES', f'{HERE}/issues') + '/2*')):     # ISSUES=<dir> scores another set (the hindcasts)
    if not os.path.exists(f'{d}/meta.txt'): continue
    meta = {l.split()[0]: day_of(' '.join(l.split()[2:4])) for l in open(f'{d}/meta.txt') if l.strip()}; lines = []; complete = True
    for st, (name, lon) in STATIONS.items():
        rows = list(csv.DictReader(open(f'{d}/forecast_{st}.csv'))); tf = np.array([day_of(r['UTC']) for r in rows]); col = lambda k: np.array([float(r[k]) for r in rows])
        mine, noaa, om, on = col('mine_m'), col('noaa_m'), col('mine_offset_m'), col('noaa_offset_m'); t0 = meta[st]
        t, y = OBS[st]; mk = (t > t0 + 1e-9) & (t <= t0 + 3.0 + 1e-9) & (np.abs((t * 24) % 1.0) < 1e-6)
        if asof is not None: mk &= t <= asof
        t, y = t[mk], y[mk]
        if len(t) < 65: complete = False; lines.append(f'      {name:22s} {len(t):2d} of 72 hours observed so far'); continue
        I = lambda v: np.interp(t, tf, v); lead = (t - t0) * 24; em, en, ep = y - I(mine) - I(om), y - I(noaa) - I(on), y - I(noaa); tm, tn = y - I(mine), y - I(noaa)
        lines.append(f'      {name:22s} rms: mine {rms(em):6.2f}  NOAA+ {rms(en):6.2f}  published {rms(ep):6.2f}   | tide alone, means removed: sd mine {100 * tm.std():5.2f}  NOAA {100 * tn.std():5.2f}   | by lead ' + '  '.join(f'{a}-{b} h: {rms(em[(lead > a) & (lead <= b)]):.1f}/{rms(en[(lead > a) & (lead <= b)]):.1f}' for a, b in BINS))
        lines[-1] = (st, lead, em, en, ep, tm.std() / tn.std(), lines[-1])
    print(f'issue {os.path.basename(d)} (last observation used {when(min(meta.values()))} UTC): ' + ('complete' if complete else 'not yet complete'))
    for l in lines:
        if isinstance(l, tuple):
            print(l[6])
            if complete: st = l[0]; pool[st]['lead'] += list(l[1]); pool[st]['mine'] += list(l[2]); pool[st]['noaa'] += list(l[3]); pool[st]['pub'] += list(l[4]); ratios[st].append(l[5])
        else: print(l)
    if complete: counted.append(os.path.basename(d))
print(f'\npooled over the {len(counted)} complete issues ({", ".join(counted)}); rms in cm; mine / NOAA+ / published')
print('station                  all 72 h                 ' + '   '.join(f'{a:2d}-{b:2d} h            ' for a, b in BINS) + '   tide alone: mean of sd(mine)/sd(NOAA) over issues')
for st, (name, lon) in STATIONS.items():
    P = {k: np.array(v) for k, v in pool[st].items()}
    if not len(P['lead']): continue
    cell = lambda mk: f'{rms(P["mine"][mk]):5.2f} / {rms(P["noaa"][mk]):5.2f} / {rms(P["pub"][mk]):5.2f}'
    print(f'{name:22s}  {cell(P["lead"] > -1)}    ' + '   '.join(cell((P['lead'] > a) & (P['lead'] <= b)) for a, b in BINS) + f'      {np.mean(ratios[st]):.3f}')
