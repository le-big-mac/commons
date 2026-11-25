"""The sound of a plain skin and of the loaded one, by adding up their modes.   usage: python sound.py results.json drum.wav
Each mode rings at its own frequency and dies away, higher ones sooner; how strongly a stroke at radius 0.5 excites it comes from the
mode's shape there. The decay times and the softness of the stroke are invented; the frequencies are the model's."""
import sys, json, math, wave
import numpy as np
from scipy.special import jv, yv, jn_zeros
import drum
SR = 44100; R = json.load(open(sys.argv[1])); S, K = R['best_s'], R['best_k']; RS = 0.5
def shapes(s, k, top=6.6):
    """modes up to top times the lowest: (ratio to the lowest, strength when struck at RS)"""
    r = np.linspace(0, 1, 4001)[1:]; out = []; w01 = drum.roots(0, s, k, 1)[0]
    for m in range(0, 10):
        for w in drum.roots(m, s, k, 8, wmax=top * w01 + 0.1):
            if w > top * w01: break
            if s == 1.0: sh = jv(m, w * r); rho = np.ones_like(r)
            else:
                phi = lambda x: jv(m, w * x) * yv(m, w) - yv(m, w * x) * jv(m, w); c = jv(m, math.sqrt(s) * w * k) / phi(k)
                sh = np.where(r < k, jv(m, math.sqrt(s) * w * r), c * phi(r)); rho = np.where(r < k, s, 1.0)
            norm = np.trapezoid(rho * sh * sh * r, r) * (2 if m == 0 else 1); a = float(np.interp(RS, r, sh)) / norm
            out.append((w / w01, a, m))
    return sorted(out)
PLAIN = shapes(1.0, 0.5); LOADED = shapes(S, K)
def stroke(modes, f0, dur=3.2, gain=1.0):
    t = np.arange(int(dur * SR)) / SR; x = np.zeros_like(t)
    for ratio, a, m in modes:
        f = f0 * ratio
        if f > 9000: continue
        amp = a / math.sqrt(ratio) * math.exp(-(ratio / 7.0) ** 2); tau = 1.3 * ratio ** -0.8
        x += amp * np.exp(-t / tau) * np.sin(2 * math.pi * f * t)
    att = np.minimum(1.0, t / 0.004); return gain * x * att
def norm_of(modes): return np.abs(stroke(modes, 146.83)).max()
GP, GL = 1 / norm_of(PLAIN), 1 / norm_of(LOADED)
D3 = 146.83; SCALE = [D3 * 2 ** (n / 12) for n in (0, 2, 4, 7, 9, 12, 14, 16)]          # D major pentatonic from D3
events = []                                                                              # (time, modes, f0, gain)
for i in range(4): events.append((0.5 + 2.0 * i, PLAIN, D3, 0.8 * GP))
for i in range(4): events.append((9.0 + 2.0 * i, LOADED, D3, 0.8 * GL))
for i in range(4): events.append((18.0 + 2.4 * i, PLAIN, D3, 0.8 * GP)); events.append((19.2 + 2.4 * i, LOADED, D3, 0.8 * GL))
rng = np.random.default_rng(1920); t0 = 29.0; idx = 2; beat = 1.05
for bar in range(10):
    events.append((t0 + bar * 4 * beat, LOADED, D3 / 2 * 2, 0.55 * GL))                  # a low stroke on each bar
    for b in range(4):
        if bar == 9 and b > 0: break
        if rng.random() < 0.82 or b == 0:
            idx = int(np.clip(idx + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, len(SCALE) - 1)); events.append((t0 + (bar * 4 + b) * beat + (0.5 * beat if rng.random() < 0.18 else 0), LOADED, SCALE[idx], 0.5 * GL))
end = max(e[0] for e in events) + 5.0; y = np.zeros(int(end * SR))
for t, modes, f0, g in events:
    x = stroke(modes, f0, gain=g); i = int(t * SR); y[i:i + len(x)] += x[:len(y) - i]
y *= 0.85 / np.abs(y).max(); fade = int(2.5 * SR); y[-fade:] *= np.linspace(1, 0, fade)
pan = np.stack([y, y], axis=1)
with wave.open(sys.argv[2], "wb") as wf: wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((pan * 32767).astype(np.int16).tobytes())
for name, modes, g in (("plain.wav", PLAIN, GP), ("loaded.wav", LOADED, GL)):
    x = np.concatenate([stroke(modes, D3, gain=0.8 * g) for _ in range(4)])
    with wave.open(name, "wb") as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((x / np.abs(x).max() * 0.8 * 32767).astype(np.int16).tobytes())
print(f"{len(events)} strokes; {end:.1f} seconds; plain skin: {len(PLAIN)} modes up to 6.6 times the lowest; loaded: {len(LOADED)}")
print("the six strongest modes of a stroke at half the radius (ratio to the lowest; strength as a share of the strongest):")
for name, modes in (("plain", PLAIN), ("loaded", LOADED)):
    st = sorted(((abs(a / math.sqrt(r) * math.exp(-(r / 7.0) ** 2)), r, m) for r, a, m in modes), reverse=True)[:6]; print(f"   {name:6s} " + ", ".join(f"{r:.3f} ({v / st[0][0]:.2f}; m = {m})" for v, r, m in st))
