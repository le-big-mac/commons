# The table of computed times for the eclipse page, straight from JPL Horizons (DE441), for the clock correction of the published curve (4.07 s for August 1868);
# give another value on the command line to see its effect.
# Local apparent solar time ("the Sun's own time") = local apparent sidereal time - the Sun's apparent right ascension + 12 h.
import numpy as np, sys
sys.path.insert(0, '/home/agent1/wander')
import hz_eclipse as H
AU = H.AU
def table(name, lon, lat, dt, guess, rad):
    pre = H.fetch(f'{name}_pre', 301, [JD0], lon, lat, 0.005, 'UT'); lon2 = lon + (pre[0, -1] - dt) * 15.04107 / 3600.0; out = {}
    for k in ('c1', 'c2', 'c3', 'c4'):
        tl = [JD0 + (guess[k] + dt + j * 4.0) / 86400.0 for j in range(-25, 26)]
        m = H.fetch(f'{name}_T{k}_{dt:.2f}', 301, tl, lon2, lat, 0.005); s = H.fetch(f'{name}_T{k}_{dt:.2f}', 10, tl, lon2, lat, 0.005)
        t = (m[:, 0] - JD0) * 86400 - dt
        ram, dem, ras, des = np.radians(m[:, 1]), np.radians(m[:, 2]), np.radians(s[:, 1]), np.radians(s[:, 2])
        sep = np.arccos(np.sin(dem) * np.sin(des) + np.cos(dem) * np.cos(des) * np.cos(ram - ras)); rm = np.arcsin(H.K[rad] / (m[:, 4] * AU)); rs = np.arcsin(H.RS / (s[:, 4] * AU))
        g = sep - (rm + rs) if k in ('c1', 'c4') else sep - (rm - rs); falling = k in ('c1', 'c2')
        for i in range(len(g) - 1):
            if (g[i] > 0 >= g[i + 1]) if falling else (g[i] <= 0 < g[i + 1]):
                f = (0 - g[i]) / (g[i + 1] - g[i]); ut = t[i] + f * (t[i + 1] - t[i]); lst = m[i, 3] + f * ((m[i + 1, 3] - m[i, 3] + 12) % 24 - 12); ra = (s[i, 1] + f * (s[i + 1, 1] - s[i, 1])) / 15.0
                out[k] = (ut, (lst - ra + 12) % 24); break
    return out
def hms(sec): sec = sec % 86400; return f'{int(sec // 3600):02d}:{int(sec % 3600 // 60):02d}:{sec % 60:04.1f}'
JD0 = 2403562.5
DT = float(sys.argv[1]) if len(sys.argv) > 1 else 4.07
guess = {'c1': 3 * 3600 + 32 * 60 + 20, 'c2': 5 * 3600 + 0 * 60 + 26, 'c3': 5 * 3600 + 7 * 60 + 13, 'c4': 6 * 3600 + 35 * 60 + 6}
for name, lon, lat, what in (('wha', 99.7588, 11.7214, 'memorial'), ('whaS2', 99.7500, 11.7097, 'shore at the French latitude')):
    for rad in ('smaller', 'standard'):
        r = table(name, lon, lat, DT, guess, rad)
        print(f'{what} ({lon} E, {lat} N), clock correction {DT} s, {rad} lunar radius:')
        for k, w in (('c1', 'the Moon first touches the Sun'), ('c2', 'darkness begins'), ('c3', 'darkness ends'), ('c4', 'the Moon leaves the Sun')):
            ut, ast = r[k]; print(f'   {w:32s} UT {hms(ut)}   Sun\'s own time {hms(ast * 3600)}   local mean time {hms(ut + lon * 240)}   mean time of 100d30\' E {hms(ut + 100.5 * 240)}')
        print(f'   darkness lasts {r["c3"][0] - r["c2"][0]:.1f} s')
