"""Can the small drum's taps be found in the sound?   usage: python taps.py court.wav events.json
Spectral flux in the kakko's band (400-1400 Hz), 5 ms hops; a tap counts as found if the flux within 25 ms of its
time in the score is a local peak above the 90th percentile of the flux in the surrounding two seconds.
The same test at times shifted by half the gap to the next tap gives the rate of false finds."""
import sys, json
import numpy as np
from scipy.signal import stft
from listen import load
sr, x = load(sys.argv[1])
ev = json.load(open(sys.argv[2]))
hop = int(0.005 * sr)
f, t, Z = stft(x, sr, nperseg=1024, noverlap=1024 - hop)
A = np.abs(Z)[(f >= 400) & (f <= 1400)]
flux = np.maximum(np.diff(A, axis=1), 0).sum(0)
flux = np.concatenate([[0], flux])
taps = sorted((e[2], e[3]) for e in ev['events'] if e[0] == 'kakko' and e[2] >= ev['T_NETORI'])
times = np.array([a for a, _ in taps])
gain = np.array([g for _, g in taps])


def found(tt):
    out = []
    for q in tt:
        k = int(round(q / (hop / sr)))
        near = flux[max(k - 5, 0):k + 6]
        around = flux[max(k - 200, 0):k + 200]
        out.append(near.max() > np.percentile(around, 90) and near.max() >= flux[max(k - 12, 0):k + 13].max() * 0.999)
    return np.array(out)


hit = found(times)
gaps = np.diff(times)
shifted = times[:-1] + gaps / 2
false = found(shifted[gaps > 0.12])
print(f"taps of the small drum in the piece proper: {len(times)}; found in the sound: {hit.sum()} ({100 * hit.mean():.0f}%)")
print(f"the same test between taps (where there should be nothing): {false.sum()} of {len(false)} ({100 * false.mean():.0f}%)")
for lo, hi, name in ((0, 0.45, 'softest taps (start of a run)'), (0.45, 0.7, 'middle'), (0.7, 2, 'loudest (the single strokes and ends of runs)')):
    k = (gain >= lo) & (gain < hi)
    print(f"   {name}: {hit[k].sum()} of {k.sum()}")
