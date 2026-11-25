# Are the days-to-weeks pulses in (observed - predicted) the inverted barometer (about -1 cm per hPa)?  Line Q4 in ~/journal.md (25 Nov), written before the pressure was fetched.
# Same band as northward.py.  Run with python -I (reads downloaded CSV as data).
import numpy as np, sys, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); from tide import load_noaa, day_of, J2000
T0, T1 = day_of('2026-06-17 00:00'), day_of('2026-11-25 15:00'); th = np.arange(T0, T1, 1 / 24.0)
def gsm(x, sig_h):
    k = np.arange(-4 * sig_h, 4 * sig_h + 1); w = np.exp(-0.5 * (k / sig_h) ** 2); ok = ~np.isnan(x)
    return np.convolve(np.where(ok, x, 0), w, 'same') / np.maximum(np.convolve(ok.astype(float), w, 'same'), 1e-9)
band = lambda x: gsm(x, 24) - gsm(x, 192)
def hourly(t, r, need):
    i = np.round((t - T0) * 24).astype(int); mk = (i >= 0) & (i < len(th)); s = np.bincount(i[mk], r[mk], len(th)); n = np.bincount(i[mk], minlength=len(th))
    return np.where(n >= need, s / np.maximum(n, 1), np.nan)
cut = slice(192, -192); out = {}
for st, name in (('9410170', 'San Diego'), ('9414290', 'San Francisco')):
    to, yo = load_noaa(st, 'water_level'); tp, yp = load_noaa(st, 'predictions'); r = hourly(to, 100 * (yo - np.interp(to, tp, yp)), 5)
    t, p = [], []
    for line in open(f'{HERE}/data/{st}_air_pressure_2026JunNov.csv'):
        w = line.split(',')
        if line[:2] == '20' and len(w) > 1 and w[1].strip() != '':
            t.append((datetime.datetime.strptime(w[0], '%Y-%m-%d %H:%M') - J2000).total_seconds() / 86400.0); p.append(float(w[1]))
    ph = hourly(np.array(t), np.array(p), 1); a, b = band(r)[cut], band(ph)[cut]; c = np.corrcoef(a, b)[0, 1]; slope = (a * b).sum() / (b * b).sum()
    left = a - slope * b; out[st] = (c, slope)
    print(f'{name:14s} pressure hours present {np.mean(~np.isnan(ph)):.3f}; sd of the band: sea {a.std():.2f} cm, air {b.std():.2f} hPa; r = {c:+.2f}; slope {slope:+.2f} cm per hPa; sea-level band after removing it: sd {left.std():.2f} cm; after removing exactly -1 cm/hPa: sd {(a + b).std():.2f} cm')
    out[st + 'left'] = left
c, slope = out['9410170']; print(f"\nQ4  San Diego: r {c:+.2f} (bar <= -0.5), slope {slope:+.2f} cm/hPa (bar -1.6..-0.6): {'HELD' if c <= -0.5 and -1.6 <= slope <= -0.6 else 'FAILED'}")
print(f"with the barometer's part removed at both, San Diego and San Francisco bands correlate at zero lag: r = {np.corrcoef(out['9410170left'], out['9414290left'])[0, 1]:+.2f}")
