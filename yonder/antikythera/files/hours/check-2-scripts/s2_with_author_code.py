"""Second reading: things worked with the author's own hours.py and phases.py (imported, not changed; run with -B so nothing is written beside them).
 A. The starts about December 178 BC, and the same one or two Saros cycles and one or two Metonic cycles later (the paper allows those), with ranks among all 3,711.
 B. The Moon's and the Sun's mean anomalies at the first full moon of those starts, against 205 BC (the formulae of hours_after.py, typed again).
 C. The first reader's new figures that after_check.py does not recompute but this folder's code can give: the six differences at 26.25 E,
    and the averages 185.4 and 181.5.
usage: s2_with_author_code.py   (under -I -B)"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, hours as H
from phases import true_phase

K = H.starts(); g18 = H.glyphs_real(drop=('13S', '120M', '125M', '184M')); g22 = H.glyphs_real()
sc = {k: H.score(k, g18) for k in K}; sc22 = {k: H.score(k, g22) for k in K}
order = sorted(K, key=lambda k: sc[k][0]); order22 = sorted(K, key=lambda k: sc22[k][0])
v = np.array([sc[k][0] for k in K])
print(f'all starts: {len(K)}; 18 hours: median {np.median(v):.2f}, sd {v.std():.2f}, quartiles {np.percentile(v, 25):.2f} and {np.percentile(v, 75):.2f}; under 3.0 h: {(v < 3.0).sum()}')

def cal(jd):
    z = math.floor(jd + 0.5); f = jd + 0.5 - z; b = z + 1524; c = math.floor((b - 122.1) / 365.25); d = math.floor(365.25 * c); e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e) + f; mon = e - 1 if e < 14 else e - 13; yr = c - 4716 if mon > 2 else c - 4715
    return f'{yr}-{mon:02d}-{day:05.2f}'

def anomalies(k):
    kk = H.K0_FULL + k + 1; T = kk / 1236.85
    return (2.5534 + 29.10535670 * kk - 0.0000014 * T * T) % 360, (201.5643 + 385.81693528 * kk + 0.0107582 * T * T) % 360
M0, Mp0 = anomalies(0); w = lambda x: (x + 180) % 360 - 180

print('\nA and B. start: new moon that begins month 1 (TT); 18 hours (h, longitude, rank of 3,711); 22 hours (h, rank); Moon\'s and Sun\'s anomaly at the first full moon against 205 BC')
for name, off in (('about December 178 BC', 0), ('one Saros later', 223), ('two Saros later', 446), ('one Metonic cycle later', 235), ('two Metonic cycles later', 470)):
    print('  ' + name)
    for k in (340, 341, 342, 343):
        kk = k + off; M, Mp = anomalies(kk)
        print(f'     k = {kk}: {cal(true_phase(H.K0_FULL + kk + 0.5))}; {sc[kk][0]:.2f} h at {sc[kk][1]:+6.1f}, rank {1 + order.index(kk)}; {sc22[kk][0]:.2f} h, rank {1 + order22.index(kk)}; Moon {w(Mp - Mp0):+6.1f}, Sun {w(M - M0):+6.1f}')
print(f'  for comparison, 205 BC: Moon {Mp0:.1f}, Sun {M0:.1f} from perigee; the thirty starts under 2.3 h have the Moon 0 to +25 and the Sun -5 to +42 against that (hours_after.out)')
kk = H.K0_FULL + 340 + 2 + 0.5; T = kk / 1236.85
print(f'  Moon\'s mean anomaly at the new moon of 22 December 178 BC (Meeus k = {kk:.0f}): {(201.5643 + 385.81693528 * kk + 0.0107582 * T * T) % 360:.1f} from perigee (180 is apogee)')

print('\nC. differences at 205 BC and 26.25 E (engraved minus real, hours):')
s, lon = H.score(0, g18); conv = lambda n, dn: (6 + n) % 24 if dn == 'd' else (18 + n) % 24
for c, m, kind, n, dn in (('120M as 6d (Carman and Evans)', 120, 'M', 6, 'd'), ('120M as 12d (Iversen and Jones)', 120, 'M', 12, 'd'), ('119S as 11n (Carman and Evans)', 119, 'S', 11, 'n'),
                          ('119S as 12n (Iversen and Jones)', 119, 'S', 12, 'n'), ('8M 2d', 8, 'M', 2, 'd'), ('8S 1d', 8, 'S', 1, 'd'), ('8S 4d', 8, 'S', 4, 'd'), ('67M 8n', 67, 'M', 8, 'n'), ('72S 2n', 72, 'S', 2, 'n')):
    ut = ((H.syzygy_ut_hours(0, m, kind) + 0.5) % 1.0) * 24.0
    print(f'     {c}: {float(H.wrap(conv(n, dn) - ut - lon / 15)):+.2f}')
good = [k for k in K if sc[k][0] < 2.3]
dM = np.mean([w(anomalies(k)[1] - Mp0) for k in good]); dS = np.mean([w(anomalies(k)[0] - M0) for k in good])
print(f'   the {len(good)} starts under 2.3 h: Moon on average {Mp0 + dM:.1f}, Sun {M0 + dS:.1f} from perigee (the note: 185.4 and 181.5)')

print('\nD. the four starts with 8 or 16 hours added to every engraved hour (the Exeligmos dial), longitude free:')
for k in (340, 341, 342, 343):
    r = []
    for add in (0, 8, 16):
        g = [(m, kind, (h + add) % 24) for m, kind, h in g18]; a = H.score(k, g); r.append(f'+{add} h: {a[0]:.2f} at {a[1]:+.1f}')
    print(f'   k = {k}: ' + '; '.join(r))
