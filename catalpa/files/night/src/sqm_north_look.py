# After the sixteenth sheet was scored (so nothing here is a test): the second network's northern stations month by
# month at 3 degrees, the month less the same month a year before, station by station, and the middle over the
# stations whose reading was steady before the eruption. "Steady" is fixed by months before the eruption alone:
# January to June 2019 less January to June 2018 within 0.10 magnitude of nothing (three months or more).
import json, importlib.util
import numpy as np
B = '/home/agent1/night/'
spec = importlib.util.spec_from_file_location('sn', B + 'src/sqm_north.py'); SN = importlib.util.module_from_spec(spec); spec.loader.exec_module(SN)
ST = SN.F4.stations(); bright = json.load(open(B + 'data/sqm3/brightest.json')); R = {}
for c, (lat, lon, country, inst) in ST.items():
    if lat < 15.0: continue
    for y in (2018, 2019, 2020):
        for m in range(1, 13): R[(c, y, m)] = SN.month(c, lat, lon, y, m)
def fig(c, y, m, dp=3.0): r = R.get((c, y, m)); return None if r is None else r[dp]
def early(c):
    d = [fig(c, 2019, m) - fig(c, 2018, m) for m in SN.EARLY if fig(c, 2019, m) is not None and fig(c, 2018, m) is not None]; return float(np.mean(d)) if len(d) >= 3 else None
order = sorted([c for c in ST if ST[c][0] >= 15.0], key=lambda c: -ST[c][0]); steady = [c for c in order if early(c) is not None and abs(early(c)) <= 0.10]
print('the steady stations (January to June 2019 within 0.10 of January to June 2018 at 3 degrees): ' + ', '.join(f"{c} ({ST[c][2]}, {ST[c][0]:+.1f}, {early(c):+.2f})" for c in steady))
print('the others that give that figure: ' + ', '.join(f"{c} ({ST[c][2]}, {early(c):+.2f})" for c in order if early(c) is not None and c not in steady))
for y in (2019, 2020):
    print(f'{y} less {y - 1}, the reading at 3 degrees month by month, hundredths of a magnitude (positive: darker; . no figure)')
    for c in steady:
        v = [(fig(c, y, m) - fig(c, y - 1, m)) if fig(c, y, m) is not None and fig(c, y - 1, m) is not None else None for m in range(1, 13)]
        print(f"   {c:<6} {ST[c][2][:9]:<9} " + ' '.join(f'{100 * x:+4.0f}' if x is not None else '   .' for x in v))
    v = [[fig(c, y, m) - fig(c, y - 1, m) for c in steady if fig(c, y, m) is not None and fig(c, y - 1, m) is not None] for m in range(1, 13)]
    print('   the middle       ' + ' '.join(f'{100 * np.median(x):+4.0f}' if len(x) >= 3 else '   .' for x in v) + '   | ' + ' '.join(f'{len(x):1d}' for x in v))
def diff(c, y1, y0, months, dp):
    d = [fig(c, y1, m, dp) - fig(c, y0, m, dp) for m in months if fig(c, y1, m, dp) is not None and fig(c, y0, m, dp) is not None]; return float(np.mean(d)) if len(d) >= 3 else None
for dp in (3.0, 5.0):
    a = [diff(c, 2019, 2018, SN.LATE, dp) for c in steady]; b = [diff(c, 2020, 2019, SN.LATE, dp) for c in steady]; e = [diff(c, 2019, 2018, SN.EARLY, dp) for c in steady]
    f = lambda v: 'none' if not [x for x in v if x is not None] else f"{np.median([x for x in v if x is not None]):+.3f} ({len([x for x in v if x is not None])}; from {min(x for x in v if x is not None):+.2f} to {max(x for x in v if x is not None):+.2f})"
    print(f'the steady stations at {dp:g} degrees: August to December 2019 less 2018: {f(a)}; January to June 2019 less 2018: {f(e)}; August to December 2020 less 2019: {f(b)}')
