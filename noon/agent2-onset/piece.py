"""Falling into step: twenty-four pentatonic bells as Kuramoto oscillators.   usage: python piece.py out.wav
Each bell is a phase oscillator with its own tempo and strikes once a turn.  The coupling is nothing at first, rises through
the critical value to three times it, is held, and is let go.  Writes out.wav, out.json (strikes, r(t), K(t)) and out.npz (phases 30 times a second).
The bell tone and the room are those of bells-pentatonic and of the changes piece."""
import sys, json, math, wave
import numpy as np
from scipy.stats import norm
from scipy.signal import fftconvolve, lfilter
SR = 44100; N = 24; PERIOD = 3.6; W0 = 2 * math.pi / PERIOD; SIG = 0.12 * W0; KC = SIG * math.sqrt(8 / math.pi)
T1, T2, T3, TEND, KMAX = 35.0, 150.0, 185.0, 232.0, 3.0            # no coupling; rising; held at KMAX times critical; let go
rng = np.random.default_rng(11)
om = W0 + SIG * norm.ppf((np.arange(N) + 0.5) / N)[::-1]           # bell 0 is the fastest
PITCHES = [57, 59, 62, 64, 66, 69, 71, 74, 76, 78, 81, 83]          # A3 B3 D4 E4 F#4 A4 B4 D5 E5 F#5 A5 B5: D major pentatonic
pitch = [PITCHES[i // 2] for i in range(N)]                         # the fastest bells are the lowest, so a locked chord rolls upward
def coupling(t):
    return 0.0 if t < T1 or t >= T3 else KC * KMAX * min(1.0, (t - T1) / (T2 - T1))
DT = 0.005; steps = int(TEND / DT); th = rng.uniform(0, 2 * math.pi, N)
def f(x, K):
    z = np.exp(1j * x).mean(); return om + K * (z.imag * np.cos(x) - z.real * np.sin(x))
strikes = []; rs = []; ph = []
for n in range(steps):
    t = n * DT; K = coupling(t)
    if n % 10 == 0: rs.append(float(abs(np.exp(1j * th).mean())))
    if abs(t * 30 - round(t * 30)) < 1e-6 or int(t * 30) != int((t - DT) * 30): ph.append(th.copy())
    k1 = f(th, K); k2 = f(th + 0.5 * DT * k1, K); k3 = f(th + 0.5 * DT * k2, K); k4 = f(th + DT * k3, K)
    new = th + (DT / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    for i in np.nonzero(np.floor(new / (2 * math.pi)) > np.floor(th / (2 * math.pi)))[0]:
        frac = (2 * math.pi * math.floor(new[i] / (2 * math.pi)) - th[i]) / (new[i] - th[i]); strikes.append((round(t + frac * DT, 4), int(i), pitch[i]))
    th = new
strikes.sort()
fr = lambda m: 440 * 2 ** ((m - 69) / 12)
def bell(m, dur, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; w = 2 * np.pi * fr(m); out = np.zeros(n)
    for ratio, amp, dec in [(.5, .25, 1.8), (1, 1, 1.4), (2.0, .45, .9), (2.76, .3 * bright, .55), (4.07, .18 * bright, .35), (5.4, .1 * bright, .2)]:
        out += amp * np.sin(w * ratio * t + rng.uniform(0, 6)) * np.exp(-t / (dec * dur / 3))
    return out * np.minimum(t / .003, 1)
L = np.zeros(int((TEND + 6) * SR)); R = L.copy()
for t, i, m in strikes:
    g = .5 * rng.uniform(.9, 1.05) * (1.0 if m > 60 else 1.08)
    sig = bell(m, 3.2 if m > 60 else 3.6, bright=.8 if m > 68 else 1.05)
    k = int((t + 0.3) * SR); a = (np.interp(m, [57, 83], [-.7, .7]) + 1) * np.pi / 4
    L[k:k + len(sig)] += sig * g * np.cos(a); R[k:k + len(sig)] += sig * g * np.sin(a)
n = int(3.5 * SR); ir = rng.normal(size=(2, n)) * np.exp(-np.arange(n) / SR / .8); ir[:, :int(.015 * SR)] = 0; ir = lfilter([.1], [1, -.9], ir, axis=1)
for ch, k in ((L, 0), (R, 1)):
    ch += .45 * fftconvolve(ch, ir[k])[:len(ch)] / np.sqrt((ir[k] ** 2).sum())
x = np.stack([L, R], 1); x = np.tanh(x / np.abs(x).max() * 1.6) / np.tanh(1.6) * .7
fo = np.linspace(1, 0, int(7 * SR)); x[-len(fo):] *= fo[:, None]
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
json.dump(dict(N=N, period=PERIOD, sigma=SIG, kc=KC, kmax=KMAX, t1=T1, t2=T2, t3=T3, tend=TEND, omega=om.tolist(), pitch=pitch, strikes=strikes, r=rs, r_dt=10 * DT, lead=0.3),
          open(sys.argv[1].replace('.wav', '.json'), 'w'))
np.savez_compressed(sys.argv[1].replace('.wav', '.npz'), phases=np.array(ph))
print(f"{N} bells, {len(strikes)} strikes, {TEND:.0f} seconds; critical coupling {KC:.3f} rad/s reached at {T1 + (T2 - T1) / KMAX:.0f} s; phases saved: {len(ph)} frames")
