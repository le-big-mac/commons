# How loud does the long note come out beside the short one through a filter that cuts the bass (a stand-in for a small loudspeaker, not a measured one)?  (After Yonder's run of 26 Nov, which showed that this, and not any meeting of overtones,
# is what its bass-less stand-ins change.)  Notes are made as the page makes them: a triangle wave with the page's envelope, long = two beats of 0.14 s at peak 0.20, short = one beat
# at peak 0.16.  The stand-ins are Yonder's reader's: a one-pole high-pass filter, y[i] = a (y[i-1] + x[i] - x[i-1]) with a = exp(-2 pi fc / rate), applied two or four times.
# Printed: the long note's level minus the short note's, in decibels (root mean square over the stretch in which each note sounds).    Run: ~/ipd/.venv/bin/python -I listen_levels.py
import numpy as np
SR = 44100
def note(f, dur, peak):
    n = int(SR * (dur - 0.02)); t = np.arange(n) / SR                         # the stretch in which the note sounds (a first version took in 0.04 s of silence, which put every figure 0.6 dB too high for the long note; a reader found it)
    tri = 2 / np.pi * np.arcsin(np.sin(2 * np.pi * f * t))                    # a triangle wave of height 1
    end = dur - 0.02; knee = max(0.03, end - 0.03); g = np.zeros(n)
    def ramp(t0, v0, t1, v1): m = (t >= t0) & (t < t1); g[m] = v0 * (v1 / v0) ** ((t[m] - t0) / (t1 - t0))
    ramp(0, 1e-4, 0.012, peak); ramp(0.012, peak, knee, peak * 0.45); ramp(knee, peak * 0.45, end, 1e-4)
    return tri * g
def hp(x, fc, times):
    a = np.exp(-2 * np.pi * fc / SR)
    for _ in range(times):
        y = np.empty_like(x); py = 0.0; px = 0.0
        for i in range(len(x)): py = a * (py + x[i] - px); px = x[i]; y[i] = py
        x = y
    return x
db = lambda x: 10 * np.log10(np.mean(x ** 2))
STAND = [('no filter', None, 0), ('600 Hz, twice', 600, 2), ('1,000 Hz, twice', 1000, 2), ('1,000 Hz, four times', 1000, 4), ('2,000 Hz, four times', 2000, 4)]
PAIRS = [('G and D, a fifth (the page until 26 Nov, 09:26)', 392.0, 587.33), ('G and F sharp (the page from 09:26 on 26 Nov until the long note was raised)', 392.0, 739.99), ('C and E, a major third, higher', 523.25, 659.26),
         ('D and F sharp (the page now)', 587.33, 739.99), ('D and F, a minor third, higher', 587.33, 698.46), ('E and G, a minor third, higher still', 659.26, 783.99)]
print(f"{'long note minus short note, dB':80s}" + ''.join(f'{s[0]:>22s}' for s in STAND) + '   widest swing')
for name, fl, fs in PAIRS:
    L = note(fl, 0.28, 0.20); S = note(fs, 0.14, 0.16); row = []
    for _, fc, k in STAND:
        row.append(db(hp(L, fc, k)) - db(hp(S, fc, k)) if fc else db(L) - db(S))
    print(f'{name:80s}' + ''.join(f'{v:+22.1f}' for v in row) + f'   {max(row) - min(row):6.1f}')
print('\nHow much of each note is left, dB below the same note with no filter, through the steepest two stand-ins:')
for f in (392.0, 523.25, 587.33, 659.26, 698.46, 739.99, 783.99):
    N = note(f, 0.28, 0.20); print(f'   {f:7.2f} Hz: ' + ', '.join(f'{s[0]} {db(hp(N, s[1], s[2])) - db(N):+.1f}' for s in STAND[3:]))
