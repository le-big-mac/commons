# Do the pulses in (observed - predicted) travel north along the coast?  Method and lines Q1-Q3 fixed in ~/journal.md (25 Nov, 15:50 UTC) before the June-September data were fetched.
# Hourly (observed - NOAA prediction), 17 Jun - 25 Nov 2026; band = Gaussian smooth (sigma 1 d) minus Gaussian smooth (sigma 8 d); cross-correlation with San Diego at lags -8..+8 days.
# Run with python -I (reads downloaded CSV as data).
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from tide import load_noaa, when, day_of, design, STATIONS
T0, T1 = day_of('2026-06-17 00:00'), day_of('2026-11-25 15:00'); th = np.arange(T0, T1, 1 / 24.0)
def gsm(x, sig_h):
    k = np.arange(-4 * sig_h, 4 * sig_h + 1); w = np.exp(-0.5 * (k / sig_h) ** 2); ok = ~np.isnan(x)
    return np.convolve(np.where(ok, x, 0), w, 'same') / np.maximum(np.convolve(ok.astype(float), w, 'same'), 1e-9)
def band(x): return gsm(x, 24) - gsm(x, 192)
def hourly(t, r):
    i = np.round((t - T0) * 24).astype(int); mk = (i >= 0) & (i < len(th)); s = np.bincount(i[mk], r[mk], len(th)); n = np.bincount(i[mk], minlength=len(th))
    return np.where(n >= 5, s / np.maximum(n, 1), np.nan)
ST = (('9410170', 'San Diego', 0), ('9410230', 'La Jolla', 20), ('9410660', 'Los Angeles', 150), ('9414290', 'San Francisco', 740), ('9432780', 'Charleston, Oregon', 1400), ('9447130', 'Seattle', 1900))
R, B = {}, {}
for st, name, km in ST:
    to, yo = load_noaa(st, 'water_level'); tp, yp = load_noaa(st, 'predictions'); R[st] = hourly(to, yo - np.interp(to, tp, yp)); B[st] = band(R[st])
    print(f'{name:20s} hours present {np.mean(~np.isnan(R[st])):.3f}; mean {100 * np.nanmean(R[st]):+.1f} cm; sd of the band {100 * np.std(B[st][192:-192]):.1f} cm')
cut = slice(192, -192)                       # drop 8 days at each end, where the long smooth is one-sided
def xc(a, b, maxlag=8 * 24):
    out = []
    for L in range(-maxlag, maxlag + 1):      # positive L: b repeats a, L hours later
        x = a[cut]; y = np.roll(b, -L)[cut]; out.append(np.corrcoef(x, y)[0, 1])
    out = np.array(out); j = out.argmax(); return (j - maxlag) / 24.0, out[j], out[maxlag]
half = len(th) // 2
print('\ncross-correlation of the band with San Diego (positive lag: the station repeats San Diego later); whole span, then its two halves')
print('station               km up the coast (rough)   lag at peak (d)   r at peak   r at zero lag     first half: lag, r     second half: lag, r    speed if a wave (m/s)')
RES = {}
for st, name, km in ST[1:]:
    lag, r, r0 = xc(B['9410170'], B[st]); RES[st] = (lag, r)
    def halfxc(sl):
        a = B['9410170'][sl]; b = B[st][sl]; best = (-9, -9)
        for L in range(-192, 193):
            x = a[192:-192]; y = np.roll(b, -L)[192:-192]; c = np.corrcoef(x, y)[0, 1]
            if c > best[1]: best = (L / 24.0, c)
        return best
    h1 = halfxc(slice(0, half)); h2 = halfxc(slice(half, None))
    sp = f'{km * 1000 / (lag * 86400):.1f}' if lag > 0.05 else '   .'
    print(f'{name:20s}  {km:6d}                    {lag:+6.2f}           {r:.2f}        {r0:.2f}             {h1[0]:+6.2f}, {h1[1]:.2f}          {h2[0]:+6.2f}, {h2[1]:.2f}        {sp}')
yes = lambda b: 'HELD' if b else 'FAILED'
lag, r = RES['9414290']; print(f'\nQ1  San Francisco: lag {lag:+.2f} d, r {r:.2f} (bar: lag 1.5..6 d and r >= 0.4): {yes(1.5 <= lag <= 6 and r >= 0.4)}')
lag, r = RES['9410660']; print(f'Q2  Los Angeles: lag {lag:+.2f} d, r {r:.2f} (bar: lag 0.2..1.5 d): {yes(0.2 <= lag <= 1.5)}')
# Q3: my own fit's residual at San Francisco (weights of the sealed forecast, fitted on hourly observations to 15:00 on 25 Nov)
w = np.load(os.path.dirname(os.path.abspath(__file__)) + '/weights_9414290.npy'); to, yo = load_noaa('9414290', 'water_level')
mine = design(th, STATIONS['9414290'][1]) @ w; obs_h = hourly(to, yo); bm = band(obs_h - mine); c = np.corrcoef(bm[cut], B['9414290'][cut])[0, 1]
print(f'Q3  San Francisco, band of (observed - mine) against band of (observed - NOAA): r = {c:.3f} (bar >= 0.9): {yes(c >= 0.9)};  sd {100 * np.std(bm[cut]):.1f} cm against {100 * np.std(B["9414290"][cut]):.1f} cm')
np.save('/tmp/northward_bands.npy', np.array([th] + [B[s] for s, _, _ in ST]))
