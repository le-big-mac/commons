# After the sealed lines were scored (dawn.out): looking, not sealed. Same nights and rules as src/dawn.py.
#  A. When the darkest moment falls: hours before dawn, and local solar time, station by station.
#  B. The average night: the reading less the night's darkest, against hours before dawn and hours after dusk.
#  C. How much darker the darkest moment is than the last half hour before dawn.
#  D. The same counts under other choices (clear rule, smoothing, what counts as "just before").
#  E. By season.
# Run: ~/ipd/.venv/bin/python -I src/dawn_look.py > dawn_look.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('dawn', '/home/agent1/night/src/dawn.py'); D = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(D)
level = {s['st']: s['level'] for s in D.summary}; place = {s['st']: s['place'].split('/')[0].strip() for s in D.summary}
def cls(st): return 'lit' if level[st] < 19.5 else ('dark' if level[st] >= 21.0 else 'between')
N = []          # every moonless covered night with its arrays
for st in D.STATIONS:
    T, M, lat, lon, _ = D.read(st)
    if not T: continue
    t0 = dt.datetime(2024, 1, 1); tsec = np.array([(t - t0).total_seconds() for t in T]); cand = []
    for d, dusk, dawn, moon in D.nights(lat, lon):
        if moon >= 0: continue
        a = (dusk - t0).total_seconds(); b = (dawn - t0).total_seconds(); i0, i1 = np.searchsorted(tsec, a), np.searchsorted(tsec, b)
        if i1 - i0 < 10: continue
        mins = np.floor((tsec[i0:i1] - a) / 60).astype(int); nmin = int((b - a) // 60); um = np.unique(mins)
        if len(um) < 0.9 * nmin: continue
        m = np.array([np.median(M[i0:i1][mins == k]) for k in um]); t = (um + 0.5) / 60
        cand.append(dict(st=st, d=d, L=(b - a) / 3600, t=t, m=m, s=D.spread(m), dawn=dawn, lon=lon, lat=lat))
    if not cand: continue
    floor = float(np.percentile([c['s'] for c in cand], 20))
    for c in cand: c['floor'] = floor; c['sm'] = D.runmed(c['m'], 31); N.append(c)
clear = [c for c in N if c['s'] <= 2 * c['floor']]
def tstar(c, key='sm'): return c['t'][int(np.argmax(c[key]))]
print(f"nights: moonless and covered {len(N)}; clear by the sealed rule {len(clear)}")
print("\nA. WHEN THE DARKEST MOMENT FALLS (clear moonless nights; middle value, and the middle half of nights)")
print(f"  {'station':<9} {'class':<8} {'nights':>6} {'hours before dawn':>24} {'local solar time':>22} {'night length':>14}  place")
def q(v): return f"{np.median(v):5.1f} ({np.percentile(v, 25):4.1f} to {np.percentile(v, 75):4.1f})"
def solar(c): return ((c['dawn'] - dt.timedelta(hours=c['L'] - tstar(c))) + dt.timedelta(hours=c['lon'] / 15))
def hod(x): h = x.hour + x.minute / 60; return h if h < 12 else h - 24      # hours from midnight, evening negative
for st in sorted(level, key=lambda s: level[s]):
    v = [c for c in clear if c['st'] == st]
    if len(v) < 5: continue
    print(f"  {st:<9} {cls(st):<8} {len(v):6d} {q([c['L'] - tstar(c) for c in v]):>24} {q([hod(solar(c)) for c in v]):>22} {q([c['L'] for c in v]):>14}  {place[st][:34]}")
for k in ('lit', 'between', 'dark'):
    v = [c for c in clear if cls(c['st']) == k]
    print(f"  all {k:<8} {len(v):4d} nights: hours before dawn {q([c['L'] - tstar(c) for c in v])}; local solar time {q([hod(solar(c)) for c in v])}; within one hour of dawn {100 * np.mean([c['L'] - tstar(c) <= 1 for c in v]):.0f} in 100; within two {100 * np.mean([c['L'] - tstar(c) <= 2 for c in v]):.0f} in 100")
print("\nB. THE AVERAGE NIGHT: how much brighter than its own darkest moment, in hundredths of a magnitude (0 = as dark as it gets); nights of 7 hours or more")
for k in ('lit', 'between', 'dark'):
    v = [c for c in clear if cls(c['st']) == k and c['L'] >= 7]
    hb = []; ha = []
    for h in np.arange(0.25, 7, 0.5):
        hb.append(np.mean([c['sm'].max() - np.interp(c['L'] - h, c['t'], c['sm']) for c in v])); ha.append(np.mean([c['sm'].max() - np.interp(h, c['t'], c['sm']) for c in v]))
    print(f"  {k} ({len(v)} nights)")
    print("     hours before dawn 6.75 ... 0.25: " + " ".join(f"{100 * x:4.0f}" for x in hb[::-1]))
    print("     hours after dusk  0.25 ... 6.75: " + " ".join(f"{100 * x:4.0f}" for x in ha))
print("\nC. THE DARKEST MOMENT AGAINST THE LAST HALF HOUR BEFORE DAWN (magnitudes; 0.01 is about 1 in 100 of brightness)")
for k in ('lit', 'between', 'dark'):
    v = [c for c in clear if cls(c['st']) == k and np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)]; dlt = [c['sm'].max() - np.median(c['m'][c['t'] >= c['L'] - 0.5]) for c in v]; d0 = [c['sm'].max() - np.median(c['m'][c['t'] <= 0.5]) for c in v]
    print(f"  {k}: darker than the last half hour by {np.median(dlt):.3f} in the middle night ({np.percentile(dlt, 25):.3f} to {np.percentile(dlt, 75):.3f}); darker than the first half hour by {np.median(d0):.3f} ({np.percentile(d0, 25):.3f} to {np.percentile(d0, 75):.3f}); last half hour within 0.02 of the darkest on {100 * np.mean(np.array(dlt) <= 0.02):.0f} nights in 100")
print("\nD. OTHER CHOICES (all stations together): share of nights with the darkest moment in the last tenth / in the second half / middle f")
def tally(sel, key='sm', win=None):
    f = []
    for c in sel:
        sm = c[key] if win is None else D.runmed(c['m'], win); f.append(c['t'][int(np.argmax(sm))] / c['L'])
    f = np.array(f); return f"{len(f):4d} nights: {100 * np.mean(f >= 0.9):3.0f} in 100 / {100 * np.mean(f > 0.5):3.0f} in 100 / {np.median(f):.2f}; last twentieth {100 * np.mean(f >= 0.95):.0f} in 100; last fifth {100 * np.mean(f >= 0.8):.0f} in 100"
print("  the sealed rule:                         " + tally(clear))
for mult in (1.5, 3.0, 5.0): print(f"  clear = spread up to {mult} times the floor:  " + tally([c for c in N if c['s'] <= mult * c['floor']]))
for w in (11, 61, 121): print(f"  running median of {w:3d} minutes:            " + tally(clear, win=w))
print("  nights of 8 hours or more:               " + tally([c for c in clear if c['L'] >= 8])); print("  nights under 7 hours:                    " + tally([c for c in clear if c['L'] < 7]))
print("\nE. BY SEASON AND CLASS: share with the darkest moment in the last tenth; middle hours before dawn")
for k in ('lit', 'between', 'dark'):
    for tag, months in (("November to February", (11, 12, 1, 2)), ("March, April, September, October", (3, 4, 9, 10)), ("May to August", (5, 6, 7, 8))):
        v = [c for c in clear if cls(c['st']) == k and ((c['d'].month in months) if c['lat'] > 0 else (((c['d'].month + 5) % 12 + 1) in months))]
        if v: print(f"  {k:<8} {tag:<34} {len(v):4d} nights: {100 * np.mean([tstar(c) / c['L'] >= 0.9 for c in v]):3.0f} in 100; {np.median([c['L'] - tstar(c) for c in v]):4.1f} h before dawn; local solar time {np.median([hod(solar(c)) for c in v]):+5.1f}; night {np.median([c['L'] for c in v]):4.1f} h")
print("\nF. BEFORE DAWN AGAINST AFTER DUSK: the last half hour of the night against the first (magnitudes; positive = darker before dawn)")
for k in ('lit', 'between', 'dark', 'all'):
    v = [c for c in clear if (k == 'all' or cls(c['st']) == k) and np.any(c['t'] >= c['L'] - 0.5) and np.any(c['t'] <= 0.5)]
    d = np.array([np.median(c['m'][c['t'] >= c['L'] - 0.5]) - np.median(c['m'][c['t'] <= 0.5]) for c in v])
    print(f"  {k:<8} {len(d):4d} nights: darker before dawn than after dusk on {100 * np.mean(d > 0):.0f} in 100; by {np.median(d):.2f} in the middle night ({np.percentile(d, 25):.2f} to {np.percentile(d, 75):.2f}), which is {100 * (10 ** (0.4 * np.median(d)) - 1):.0f} in 100 of brightness")
print("\nG. BY THE CLOCK ON THE WALL, the four Spanish towns and Madrid's ring road (clock = UTC + 1, or + 2 from 31 March to 27 October 2024)")
for tag, months in (("November to February", (11, 12, 1, 2)), ("March, April, September, October", (3, 4, 9, 10)), ("May to August", (5, 6, 7, 8)), ("all year", tuple(range(1, 13)))):
    v = [c for c in clear if c['st'] in ('stars1', 'stars7', 'stars52', 'stars76', 'stars33') and c['d'].month in months]
    if not v: continue
    ck = []
    for c in v:
        u = c['dawn'] - dt.timedelta(hours=c['L'] - tstar(c)); off = 2 if dt.datetime(2024, 3, 31, 1) <= u < dt.datetime(2024, 10, 27, 1) else 1; ck.append(hod(u + dt.timedelta(hours=off)))
    dk = []
    for c in v:
        u = c['dawn']; off = 2 if dt.datetime(2024, 3, 31, 1) <= u < dt.datetime(2024, 10, 27, 1) else 1; dk.append(hod(u + dt.timedelta(hours=off)))
    f2 = lambda x: f"{int(x):02d}:{int(round((x - int(x)) * 60)):02d}"
    print(f"  {tag:<34} {len(v):3d} nights: darkest at {f2(np.median(ck))} by the clock in the middle night ({f2(np.percentile(ck, 25))} to {f2(np.percentile(ck, 75))}); astronomical dawn begins at {f2(np.median(dk))}")
print("\nH. NIGHTS AND STATIONS: " + "; ".join(f"{k}: {sum(1 for c in clear if cls(c['st']) == k)} nights at {len(set(c['st'] for c in clear if cls(c['st']) == k))} stations" for k in ('lit', 'between', 'dark')))
