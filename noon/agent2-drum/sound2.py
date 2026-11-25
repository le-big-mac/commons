"""The sound of any radially loaded skin, by adding up its modes (found by finite differences), and the piece.
usage: python sound2.py results.json layers-2.json layers-3.json drum.wav
Decay times and the softness of the stroke are invented; the frequencies and the strength of each mode at the striking point are the model's."""
import sys, json, math, wave
import numpy as np
from scipy.linalg import eigh_tridiagonal
import os
SR = 44100; RS = float(os.environ.get('DRUM_RS', '0.5')); TAG = os.environ.get('DRUM_TAG', ''); D3 = 146.83      # the striking point; 0.5 unless DRUM_RS is set (used only for a check)
def modes_of(rho_of_r, top=6.6, N=1500):
    h = 1.0 / N; r = (np.arange(N) + 0.5) * h; rho = rho_of_r(r); re = np.arange(N + 1) * h; sc = np.sqrt(r * rho); out = []; w01 = None
    for m in range(0, 10):
        d = (re[:-1] + re[1:]) / (h * h * r) + m * m / r ** 2; d[-1] += re[-1] / (h * h * r[-1]); off = -re[1:-1] / (h * h)
        ev, vec = eigh_tridiagonal(d * r / sc ** 2, off / (sc[:-1] * sc[1:]), select='i', select_range=(0, 7)); w = np.sqrt(ev)
        if m == 0: w01 = w[0]
        for j in range(8):
            if w[j] > top * w01: break
            shape = vec[:, j] / sc; a = float(np.interp(RS, r, shape)) / (2 if m == 0 else 1); out.append((w[j] / w01, a, m))
    return sorted(out)
def stroke(modes, f0, dur=3.2, gain=1.0):
    t = np.arange(int(dur * SR)) / SR; x = np.zeros_like(t)
    for ratio, a, m in modes:
        f = f0 * ratio
        if f > 9000: continue
        x += a / math.sqrt(ratio) * math.exp(-(ratio / 7.0) ** 2) * np.exp(-t / (1.3 * ratio ** -0.8)) * np.sin(2 * math.pi * f * t)
    return gain * x * np.minimum(1.0, t / 0.004)
def save(name, x, ch=1):
    with wave.open(name, "wb") as wf: wf.setnchannels(ch); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((x * 32767).astype(np.int16).tobytes())
R = json.load(open(sys.argv[1])); L2 = json.load(open(sys.argv[2])); L3 = json.load(open(sys.argv[3]))
layered = lambda L: (lambda r: 1.0 + sum(a * (r < k) for a, k in zip(L['a'], L['k'])))
SKINS = [("plain", lambda r: np.ones_like(r)), ("disc", lambda r: np.where(r < R['best_k'], R['best_s'], 1.0)), ("two-layers", layered(L2)), ("three-layers", layered(L3))]
M = {name: modes_of(f) for name, f in SKINS}; G = {name: 1 / np.abs(stroke(M[name], D3)).max() for name in M}
for name in M:
    x = np.concatenate([stroke(M[name], D3, gain=0.8 * G[name]) for _ in range(4)]); save(f"strokes-{name}{TAG}.wav", x / np.abs(x).max() * 0.8)
    st = sorted(((abs(a / math.sqrt(r) * math.exp(-(r / 7.0) ** 2)), r) for r, a, m in M[name]), reverse=True)[:8]
    print(f"{name:13s} {len(M[name]):2d} modes up to 6.6 times the lowest; the eight strongest when struck at half the radius: " + ", ".join(f"{r:.3f}" for v, r in sorted(st, key=lambda z: z[1])))
SCALE = [D3 * 2 ** (n / 12) for n in (0, 2, 4, 7, 9, 12, 14, 16)]; ev = []
for i in range(3): ev.append((0.5 + 2.0 * i, "plain", D3, 0.8))
for i in range(3): ev.append((7.0 + 2.0 * i, "disc", D3, 0.8))
for i in range(3): ev.append((13.5 + 2.0 * i, "two-layers", D3, 0.8))
for i in range(3): ev.append((20.5 + 2.4 * i, "plain", D3, 0.8)); ev.append((21.7 + 2.4 * i, "two-layers", D3, 0.8))
rng = np.random.default_rng(1920); t0 = 29.5; idx = 2; beat = 1.05
for bar in range(10):
    ev.append((t0 + bar * 4 * beat, "two-layers", D3, 0.55))
    for b in range(4):
        if bar == 9 and b > 0: break
        if rng.random() < 0.82 or b == 0:
            idx = int(np.clip(idx + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(SCALE) - 1)); ev.append((t0 + (bar * 4 + b) * beat + (0.5 * beat if rng.random() < 0.18 else 0), "two-layers", SCALE[idx], 0.5))
end = max(e[0] for e in ev) + 5.0; y = np.zeros(int(end * SR))
for t, name, f0, g in ev:
    x = stroke(M[name], f0, gain=g * G[name]); i = int(t * SR); y[i:i + len(x)] += x[:len(y) - i]
y *= 0.85 / np.abs(y).max(); fade = int(2.5 * SR); y[-fade:] *= np.linspace(1, 0, fade); save(sys.argv[4], np.stack([y, y], axis=1), ch=2)
print(f"{len(ev)} strokes; {end:.1f} seconds: plain skin from 0.5 s, even disc from 7 s, two layers from 13.5 s, plain and two layers by turns from 20.5 s, a tune on two-layer skins from 29.5 s")
