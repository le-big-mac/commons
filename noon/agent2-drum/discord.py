"""How the discord figures move with the base note and the measure's window.   usage: python -u discord.py results.json layers-2.json
The strokes are rendered as in sound2.py (same modes, strengths, decays); the measure is ~/court/clash.py's, copied here so that its
window (35 cents there) and the base note can be changed. A tone with exactly harmonic partials 1 to 6 is added as a floor.
Also Sethares' roughness (the formula in ~/court/listen.py) on the partials themselves, which uses no scale of notes."""
import sys, json, math
import numpy as np
from scipy.signal import stft
from scipy.linalg import eigh_tridiagonal
SR = 44100; RS = 0.5
def modes_of(rho_of_r, top=6.6, N=1500):
    h = 1.0 / N; r = (np.arange(N) + 0.5) * h; rho = rho_of_r(r); re = np.arange(N + 1) * h; sc = np.sqrt(r * rho); out = []; w01 = None
    for m in range(0, 10):
        d = (re[:-1] + re[1:]) / (h * h * r) + m * m / r ** 2; d[-1] += re[-1] / (h * h * r[-1]); off = -re[1:-1] / (h * h)
        ev, vec = eigh_tridiagonal(d * r / sc ** 2, off / (sc[:-1] * sc[1:]), select='i', select_range=(0, 7)); w = np.sqrt(ev)
        if m == 0: w01 = w[0]
        for j in range(8):
            if w[j] > top * w01: break
            out.append((w[j] / w01, float(np.interp(RS, r, vec[:, j] / sc)) / (2 if m == 0 else 1), m))
    return sorted(out)
def parts(modes, f0): return [(f0 * r, abs(a) / math.sqrt(r) * math.exp(-(r / 7.0) ** 2), 1.3 * r ** -0.8) for r, a, m in modes if f0 * r <= 9000]
def strokes(modes, f0, n=4, dur=3.2):
    t = np.arange(int(dur * SR)) / SR; x = np.zeros_like(t)
    for (f, amp, tau), (r, a, m) in zip(parts(modes, f0), [q for q in modes if f0 * q[0] <= 9000]): x += math.copysign(amp, a) * np.exp(-t / tau) * np.sin(2 * math.pi * f * t)
    x *= np.minimum(1.0, t / 0.004); x = np.concatenate([x] * n); x = np.round(x / np.abs(x).max() * 0.8 * 32767) / 32768; return x
def clash(x, ref=440.0, window=0.35):
    f, t, Z = stft(x, SR, nperseg=16384, noverlap=16384 - 4096); P = np.abs(Z) ** 2; keep = (f > 100) & (f < 4000); pc = 12 * np.log2(f[keep] / ref); near = np.abs(pc - np.rint(pc)) < window
    cls = (np.rint(pc).astype(int) % 12)[near]; C = np.zeros((12, P.shape[1])); np.add.at(C, cls, P[keep][near]); w = int(round(2.0 * SR / 4096)); Cw = np.stack([np.convolve(C[i], np.ones(w), mode='valid') for i in range(12)])
    tot = Cw.sum(0); ok = tot > 0.05 * np.median(tot); Cn = Cw[:, ok] / tot[ok]; return float((12 * (Cn * np.roll(Cn, -1, axis=0)).sum(0)).mean())
def sethares(modes, f0):
    p = parts(modes, f0); f = np.array([q[0] for q in p]); a = np.array([q[1] for q in p]); i, j = np.triu_indices(len(f), 1); fmin, d = np.minimum(f[i], f[j]), np.abs(f[i] - f[j]); s = 0.24 / (0.021 * fmin + 19)
    return float((a[i] * a[j] * (np.exp(-3.5 * s * d) - np.exp(-5.75 * s * d))).sum() / (a[i] * a[j]).sum())
R = json.load(open(sys.argv[1])); L2 = json.load(open(sys.argv[2]))
SK = {"plain": modes_of(lambda r: np.ones_like(r)), "disc": modes_of(lambda r: np.where(r < R['best_k'], R['best_s'], 1.0)), "two layers": modes_of(lambda r: 1.0 + sum(a * (r < k) for a, k in zip(L2['a'], L2['k']))), "harmonic 1 to 6": [(float(h), 1.0, 0) for h in range(1, 7)]}
print("the semitone clash of four strokes:            plain    disc   two layers   harmonic 1 to 6")
for label, f0, win in (("as published: 146.83 Hz, 35 cents", 146.83, 0.35), ("base 220 Hz", 220.0, 0.35), ("base 293.66 Hz (an octave up)", 293.66, 0.35), ("base 196 Hz", 196.0, 0.35), ("window 30 cents", 146.83, 0.30), ("window 25 cents", 146.83, 0.25), ("window 45 cents", 146.83, 0.45), ("base 10 cents sharp", 146.83 * 2 ** (10 / 1200), 0.35), ("base 20 cents flat", 146.83 * 2 ** (-20 / 1200), 0.35)):
    print(f"   {label:40s} " + "   ".join(f"{clash(strokes(SK[k], f0), window=win):6.3f}" for k in SK), flush=True)
print("Sethares' roughness of the partials (no scale of notes), base 146.83 Hz: " + "; ".join(f"{k} {sethares(SK[k], 146.83):.3f}" for k in SK))
print("                                         base 293.66 Hz: " + "; ".join(f"{k} {sethares(SK[k], 293.66):.3f}" for k in SK))
