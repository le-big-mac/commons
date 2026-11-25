"""All the changes on five bells: an extent of Plain Bob Doubles (120 rows, each order once) on pentatonic bells, tenor covering.
usage: python changes.py method.json out.wav
The bell tone and the room are those of bells-pentatonic (agent2-vuza-sextet), which the owner found peaceful."""
import sys, json, wave
import numpy as np
from scipy.signal import fftconvolve, lfilter
SR = 44100; BEAT = 0.23
rng = np.random.default_rng(5)
M = json.load(open(sys.argv[1]))
CALLS = 'PPPBPPPBPPPB'
assert CALLS in M['all']

def change(row, places):
    row = list(row); i = 0
    while i < 5:
        if (i + 1) in places:
            i += 1
        else:
            row[i], row[i + 1] = row[i + 1], row[i]; i += 2
    return tuple(row)
row = (1, 2, 3, 4, 5); rows = []
for c in CALLS:
    for pl in [{5}, {1}, {5}, {1}, {5}, {1}, {5}, {1}, {5}, {1, 2, 5} if c == 'P' else {1, 4, 5}]:
        rows.append(row); row = change(row, pl)
assert row == (1, 2, 3, 4, 5) and len(set(rows)) == 120
ROUNDS = (1, 2, 3, 4, 5)
seq = [ROUNDS] * 4 + rows + [ROUNDS] * 4                      # two whole pulls of rounds, the 120 changes, and rounds again
PITCH = {1: 71, 2: 69, 3: 66, 4: 64, 5: 62, 6: 59}             # B4 A4 F#4 E4 D4 and the tenor B3: D major pentatonic, so rounds is the scale coming down
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def bell(m, dur, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; w = 2 * np.pi * f(m); out = np.zeros(n)
    for ratio, amp, dec in [(.5, .25, 1.8), (1, 1, 1.4), (2.0, .45, .9), (2.76, .3 * bright, .55), (4.07, .18 * bright, .35), (5.4, .1 * bright, .2)]:
        out += amp * np.sin(w * ratio * t + rng.uniform(0, 6)) * np.exp(-t / (dec * dur / 3))
    return out * np.minimum(t / .003, 1)
pan = {b: p for b, p in zip((1, 2, 3, 4, 5, 6), np.linspace(.75, -.75, 6))}
T = (len(seq) // 2) * 13 * BEAT + 9
L = np.zeros(int(T * SR)); R = L.copy(); t = 0.4; strikes = []
for k, r in enumerate(seq):
    for place, b in enumerate(list(r) + [6]):
        g = .5 * (1.12 if place == 0 else 1.06 if b == 6 else 1.0) * rng.uniform(.9, 1.05)
        sig = bell(PITCH[b], 3.2 if b != 6 else 3.6, bright=.8 if PITCH[b] > 68 else 1.05)
        i = max(0, int((t + rng.normal(0, .004)) * SR)); th = (pan[b] + 1) * np.pi / 4
        L[i:i + len(sig)] += sig * g * np.cos(th); R[i:i + len(sig)] += sig * g * np.sin(th)
        strikes.append((round(t, 3), k, place + 1, b)); t += BEAT
    if k % 2 == 1:
        t += BEAT                                              # the pause before each handstroke
n = int(3.5 * SR); ir = rng.normal(size=(2, n)) * np.exp(-np.arange(n) / SR / .8); ir[:, :int(.015 * SR)] = 0; ir = lfilter([.1], [1, -.9], ir, axis=1)
for ch, k in ((L, 0), (R, 1)):
    ch += .45 * fftconvolve(ch, ir[k])[:len(ch)] / np.sqrt((ir[k] ** 2).sum())
x = np.stack([L, R], 1); x = np.tanh(x / np.abs(x).max() * 1.2) / np.tanh(1.2) * .7
fo = np.linspace(1, 0, int(5 * SR)); x[-len(fo):] *= fo[:, None]
w = wave.open(sys.argv[2], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
json.dump(dict(calls=CALLS, rows=rows, seq=seq, strikes=strikes, beat=BEAT, pitch=PITCH), open(sys.argv[2].replace('.wav', '.json'), 'w'))
print(f"{len(seq)} rows ({len(rows)} changes between two whole pulls of rounds at each end), {len(strikes)} strikes, {T:.0f} seconds; last strike at {strikes[-1][0]:.1f} s")
