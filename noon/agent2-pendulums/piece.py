"""Sixteen pendulums: a pendulum wave for sixteen marimba-like voices.   usage: python piece.py out.wav
Voice k makes M + k turns in T seconds and sounds once a turn, so all sixteen start together, drift apart, and are together again
at T; at T/2 every second voice is together, at T/3 every third, at T/4 every fourth.  Nothing pulls them: it is arithmetic.
Writes out.wav and out.json (the strikes)."""
import sys, json, math, wave
import numpy as np
from scipy.signal import fftconvolve, lfilter
SR = 44100; N = 16; T = 144.0; M = 36; LEAD = 0.5; TAIL = 7.0
rng = np.random.default_rng(7)
PITCH = [50, 52, 54, 57, 59, 62, 64, 66, 69, 71, 74, 76, 78, 81, 83, 86]      # D3 E3 F#3 A3 B3 D4 ... B5 D6: D major pentatonic; the faster the voice, the higher
strikes = sorted((round(j * T / (M + k), 5), k, PITCH[k]) for k in range(N) for j in range(M + k + 1))
fr = lambda m: 440 * 2 ** ((m - 69) / 12)
def bar(m):
    """a struck wooden bar: the fundamental, a partial two octaves up and a short high one, each dying away; low bars ring longer"""
    f = fr(m); d = float(np.interp(m, [50, 86], [1.5, 0.55])); n = int(4.5 * d * SR); t = np.arange(n) / SR
    out = np.sin(2 * np.pi * f * t) * np.exp(-t / d) + 0.22 * np.sin(2 * np.pi * 4 * f * t + 0.4) * np.exp(-t / (0.22 * d)) + 0.07 * np.sin(2 * np.pi * 9.2 * f * t + 1.1) * np.exp(-t / (0.06 * d))
    return out * np.minimum(t / 0.002, 1)
L = np.zeros(int((LEAD + T + TAIL) * SR)); R = L.copy()
for t, k, m in strikes:
    g = 0.5 * rng.uniform(0.92, 1.04) * float(np.interp(m, [50, 86], [1.15, 0.8])); sig = bar(m)
    i = int((t + LEAD + rng.normal(0, 0.002)) * SR); a = (np.interp(k, [0, N - 1], [-0.7, 0.7]) + 1) * np.pi / 4
    L[i:i + len(sig)] += sig[:len(L) - i] * g * np.cos(a); R[i:i + len(sig)] += sig[:len(R) - i] * g * np.sin(a)
n = int(2.5 * SR); ir = rng.normal(size=(2, n)) * np.exp(-np.arange(n) / SR / 0.6); ir[:, :int(0.012 * SR)] = 0; ir = lfilter([0.1], [1, -0.9], ir, axis=1)
for ch, c in ((L, 0), (R, 1)):
    ch += 0.3 * fftconvolve(ch, ir[c])[:len(ch)] / np.sqrt((ir[c] ** 2).sum())
x = np.stack([L, R], 1); x = np.tanh(x / np.abs(x).max() * 1.8) / np.tanh(1.8) * 0.7
fo = np.linspace(1, 0, int(4 * SR)); x[-len(fo):] *= fo[:, None]
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
json.dump(dict(N=N, T=T, M=M, lead=LEAD, tail=TAIL, pitch=PITCH, strikes=strikes), open(sys.argv[1].replace('.wav', '.json'), 'w'))
print(f"{N} voices, {len(strikes)} strikes, {LEAD + T + TAIL:.1f} seconds; periods {T / (M + N - 1):.2f} to {T / M:.2f} s")
