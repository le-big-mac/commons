# Where was the French camp?  Their clocks kept the true local mean time of the place (set by star transits), and they timed the second and third contacts by it.
# My computation gives the UT of each contact as a function of where the observer stands.  The longitude at which UT + longitude = their clock time is where they stood.
# Also: how much longer was totality at its longest than at the camp (the King's "two or three seconds")?   Lines S1, S2 in ~/journal.md, written first.
import sys, numpy as np, importlib.util
sys.argv = ['x']; spec = importlib.util.spec_from_file_location('siam', '/home/agent1/wander/siam1868.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LAT = 11 + 42 / 60 + 35 / 3600; LON_FR = 99 + 47 / 60 + 44 / 3600; MEM = (11.7214, 99.7588)      # the French latitude and adopted longitude; the modern memorial at Wa Ko (OpenStreetMap)
JPL = -2.5 / 86400.0                                                                             # JPL's Moon puts both contacts 2.5 s before mine (hz_check2.py)
OBS = {'c2': {'Tisserand': 11 * 3600 + 39 * 60 + 23.1, 'Olry': 11 * 3600 + 39 * 60 + 23.8}, 'c3': {'Tisserand': 11 * 3600 + 46 * 60 + 9.1, 'Hatt': 11 * 3600 + 46 * 60 + 3.1}}
def lmt(key, lon, k, lat=LAT):
    c = m.contacts(m.site(lat, lon), k); return ((c[key] + JPL - m.DT + 0.5 + lon / 360.0) % 1.0) * 86400, (c['c3'] - c['c2']) * 86400
def solve(key, target, k, lat=LAT):
    lo, hi = 99.4, 100.1
    for _ in range(40):
        mid = (lo + hi) / 2
        if lmt(key, mid, k, lat)[0] < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2
dm = lambda x: f'{int(x)}d{(x % 1) * 60:04.1f}\''
print(f'French adopted longitude {dm(LON_FR)} E; the memorial at Wa Ko {dm(MEM[1])} E ({(LON_FR - MEM[1]) * 60:.1f} arcmin, {(LON_FR - MEM[1]) * 240:.1f} s of time, to the west of the French figure); the King: 99d41\'-42\' E')
for k, kn in ((m.K_SMALL, 'smaller lunar radius'), (m.K_IAU, 'IAU lunar radius')):
    t2, dur = lmt('c2', LON_FR, k); t3, _ = lmt('c3', LON_FR, k)
    print(f'\n{kn}: at the French adopted longitude my contacts are at {m.hms(t2 / 86400)} and {m.hms(t3 / 86400)} local mean time (duration {dur:.1f} s); Tisserand timed 11:39:23.1 and 11:46:09.1 (duration 406.0 s)')
    for key in ('c2', 'c3'):
        for who, t in OBS[key].items():
            lon = solve(key, t, k); print(f'   {key} {who:10s}: clock time matched at longitude {dm(lon)} E  = {(lon - LON_FR) * 240:+.1f} s of time from the French figure, {(lon - MEM[1]) * 60:+.2f} arcmin ({(lon - MEM[1]) * 111.3 * np.cos(np.radians(LAT)):+.1f} km) from the memorial')
    both = np.mean([solve('c2', OBS['c2']['Tisserand'], k), solve('c3', OBS['c3']['Tisserand'], k)])
    print(f'   Tisserand, both contacts: {dm(both)} E, {(both - MEM[1]) * 60:+.2f} arcmin from the memorial; the same at the memorial\'s latitude: {dm(np.mean([solve("c2", OBS["c2"]["Tisserand"], k, MEM[0]), solve("c3", OBS["c3"]["Tisserand"], k, MEM[0])]))} E')
    if k == m.K_SMALL:
        s2 = (both - MEM[1]) * 60; print(f'S2  fitted longitude minus the memorial\'s: {s2:+.2f} arcmin (bar: within 1.5): {"HELD" if abs(s2) <= 1.5 else "FAILED"}')
# S1: the longest totality on the central line against the camp, same radius
ev = m.eclipse2.find('/home/agent1/orrery/states_1868.txt')[0][0]; best = (0, None)
for t in np.arange(ev - 0.012, ev + 0.012, 0.0005):
    g = m.axis_ground(t)
    if g is None: continue
    c = m.contacts(m.site(g[0], g[1], 0.0), m.K_SMALL, t - 0.2)
    if c['total'] and (c['c3'] - c['c2']) * 86400 > best[0]: best = ((c['c3'] - c['c2']) * 86400, g)
cam = lmt('c2', LON_FR, m.K_SMALL)[1]; cam2 = (lambda c: (c['c3'] - c['c2']) * 86400)(m.contacts(m.site(MEM[0], MEM[1]), m.K_SMALL))
print(f'\nlongest totality on the central line (smaller radius): {best[0]:.1f} s at {best[1][0]:.2f} N, {best[1][1]:.2f} E; at the French position {cam:.1f} s; at the memorial {cam2:.1f} s')
d = best[0] - cam; print(f'S1  longest minus the camp: {d:+.1f} s (bar: 0 to 3): {"HELD" if 0 <= d <= 3 else "FAILED"}')
