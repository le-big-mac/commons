# Was the gauge lower on the days the gliders were inshore than in October as a whole?  (A candidate, from the search for prior work, for part of the 13 cm that the warm water
# did not account for.)  San Diego gauge 9410170, hourly heights less hourly predictions (NOAA CO-OPS, MSL, GMT), averaged by day; glider days from glider/profiles_oct.npy (line 90).
import json, numpy as np, collections
D = '/home/agent1/tides/data/sd_oct/'
R = np.load('/home/agent1/tides/glider/profiles_oct.npy'); yr, day, lat, lon, km, Dh, z26, T100, T200, u, v, line, dep, D200, pmax = R.T
for y in (2015, 2026):
    h = {r['t']: float(r['v']) for r in json.load(open(D + f'hourly_height_{y}.json'))['data'] if r['v'] not in ('', None)}
    p = {r['t']: float(r['v']) for r in json.load(open(D + f'predictions_{y}.json'))['predictions']}
    res = collections.defaultdict(list); obs = collections.defaultdict(list)
    for t in h:
        if t in p: res[int(t[8:10])].append(h[t] - p[t]); obs[int(t[8:10])].append(h[t])
    daily = {d: 100 * np.mean(x) for d, x in res.items() if len(x) >= 20}; month = np.mean(list(daily.values()))
    print(f'{y}: {len(daily)} days; mean of observed less predicted over October {month:+.1f} cm; mean observed level {100 * np.mean([np.mean(x) for x in obs.values()]):.1f} cm above MSL')
    print('   by day: ' + ' '.join(f'{d}:{daily[d]:+.0f}' for d in sorted(daily)))
    for lim in (25, 50):
        m = (yr == y) & (line == 90) & (lat >= 32) & (lat <= 34.5) & (km < lim); dd = np.floor(day[m]).astype(int)
        w = np.array([daily[d] for d in dd if d in daily])          # one value per profile, so days with more dives weigh more, as they do in the glider average
        days = sorted(set(int(d) for d in dd))
        print(f'   dives inside {lim} km: {int(m.sum())} profiles on days {days}; gauge residual on those days, weighted by profiles {w.mean():+.1f} cm, by days {np.mean([daily[d] for d in days if d in daily]):+.1f}; less the October mean: {w.mean() - month:+.1f} cm (by profiles), {np.mean([daily[d] for d in days if d in daily]) - month:+.1f} (by days)')
