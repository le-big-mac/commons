"""Score the sealed sheet from results-S/T.json and results-S/T.npz (written by run.py)."""
import json, os, numpy as np, gears
H = os.path.dirname(os.path.abspath(__file__))
J = {f: json.load(open(os.path.join(H, f'results-{f}.json'))) for f in 'ST'}
Z = {f: np.load(os.path.join(H, f'results-{f}.npz')) for f in 'ST'}
S, T = J['S'], J['T']
rms = lambda x: float(np.sqrt(np.mean(np.asarray(x) ** 2)))
yrs = S['years']
dS, dT = S['drift'], T['drift']
asin = lambda e: float(np.degrees(np.arcsin(e)))
moon_today = S['today']['moon']
prec = T['sun_advance'] - S['sun_advance']
ratio = {}
for p in gears.SYNODIC:
    syn = dS[p] / yrs if p in gears.INFERIOR else -dS[p] / yrs
    ratio[p] = abs(syn) / abs(gears.PAPER_EY[p])
floor = {b: rms(Z['S']['res_then_' + b]) for b in ('sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn')}
now = {b: rms(Z['S']['err_' + b]) for b in floor}
k18 = {p: now[p] / floor[p] for p in gears.SYNODIC}
today = {p: S['today'][p] for p in gears.SYNODIC}
L = [
 ('K1', 0.85, -275 <= dS['moon'] <= -250, f"Moon's drift, S: {dS['moon']:.2f}"),
 ('K2', 0.80, 110 <= dT['moon'] <= 132, f"Moon's drift, T: {dT['moon']:.2f}"),
 ('K3', 0.75, -350 <= dS['apsides'] <= -310, f"apsides' drift, S: {dS['apsides']:.2f}"),
 ('K4', 0.70, -1 <= dS['node'] <= 5, f"node's drift, S: {dS['node']:.2f}"),
 ('K5', 0.80, 0.95 <= floor['moon'] <= 1.15, f"Moon's floor rms: {floor['moon']:.3f}"),
 ('K6', 0.85, 6.1 <= asin(S['fit']['then']['moon']['e']) <= 6.5, f"Moon's fitted inequality: {asin(S['fit']['then']['moon']['e']):.3f}"),
 ('K7', 0.80, 85 <= moon_today <= 115, f"Moon pointer today, S: {moon_today:.2f}"),
 ('K8', 0.90, floor['sun'] < 0.03, f"Sun's floor rms: {floor['sun']:.4f}"),
 ('K9', 0.85, 1.97 <= asin(S['fit']['then']['sun']['e']) <= 2.07, f"Sun's fitted inequality: {asin(S['fit']['then']['sun']['e']):.4f}"),
 ('K10', 0.85, 30.85 <= prec <= 31.20, f"precession over the span: {prec:.4f}"),
 ('K11', 0.80, -16 <= dS['mercury'] <= -8, f"Mercury's drift, S: {dS['mercury']:.2f}"),
 ('K12', 0.80, 11 <= dS['venus'] <= 22, f"Venus's drift, S: {dS['venus']:.2f}"),
 ('K13a', 0.80, 2 <= abs(dS['mars']) <= 8, f"Mars's drift, S: {dS['mars']:.2f}"),
 ('K13b', 0.65, dS['mars'] > 0, "and its sign"),
 ('K14', 0.80, -3 <= dS['jupiter'] <= -0.5, f"Jupiter's drift, S: {dS['jupiter']:.2f}"),
 ('K15', 0.80, -12 <= dS['saturn'] <= -7, f"Saturn's drift, S: {dS['saturn']:.2f}"),
 ('K16a', 0.70, sum(0.75 <= r <= 1.25 for r in ratio.values()) >= 3, 'ratio to the paper\'s printed error: ' + ', '.join(f'{p} {r:.2f}' for p, r in ratio.items())),
 ('K16b', 0.70, ratio['mars'] < 0.8, f"Mars's ratio {ratio['mars']:.2f}"),
 ('K17a', 0.70, 30 <= float(np.max(np.abs(Z['S']['res_then_mars']))) <= 46, f"Mars's floor, largest: {float(np.max(np.abs(Z['S']['res_then_mars']))):.2f}"),
 ('K17b', 0.75, 8 <= floor['mars'] <= 12, f"Mars's floor rms: {floor['mars']:.2f}"),
 ('K18', 0.60, all(k18[p] < 1.5 for p in ('mercury', 'mars', 'jupiter')) and all(k18[p] >= 1.5 for p in ('venus', 'saturn')), 'rms now over floor: ' + ', '.join(f'{p} {r:.2f}' for p, r in k18.items())),
 ('K19a', 0.45, sum(abs(v) <= 15 for v in today.values()) >= 3, 'today, S: ' + ', '.join(f'{p} {v:+.1f}' for p, v in today.items())),
 ('K19b', 0.75, abs(today['venus']) > 12, f"Venus today {today['venus']:+.1f}"),
 ('K20', 0.85, all(-45 <= dT[p] <= -5 for p in gears.SUPERIOR) and dT['mercury'] > 60, 'T: ' + ', '.join(f'{p} {dT[p]:.1f}' for p in gears.SYNODIC)),
]
held = 0; brier = 0.0
for name, odds, ok, what in L:
    ok = bool(ok); held += ok; brier += (odds - ok) ** 2
    print(f'{name:5s} {int(odds * 100):3d}%  {"held  " if ok else "FAILED"}  {what}')
print(f'\n{held} of {len(L)} held; Brier {brier / len(L):.4f} (always saying 50%: 0.2500); mean odds {np.mean([l[1] for l in L]):.3f}')
