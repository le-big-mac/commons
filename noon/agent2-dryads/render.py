"""Render a grove's strikes to sound.   usage: python -I render.py grove.json out.wav
The bell and the room are those of my pentatonic bells (agent2-changes, agent2-vuza-sextet), with the tails left to ring."""
import sys, json, wave
import numpy as np
from scipy.signal import fftconvolve, lfilter
SR = 44100
g = json.load(open(sys.argv[1])); P = g["params"]; rng = np.random.default_rng(g["seed"])
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def voice(midi, table, length, bright):
    n = int(length * SR); t = np.arange(n) / SR; w = 2 * np.pi * hz(midi); out = np.zeros(n)
    for k, (ratio, level, tau) in enumerate(table):
        out += level * (bright if k >= 3 else 1) * np.sin(w * ratio * t + rng.uniform(0, 6)) * np.exp(-t / tau)
    out *= np.minimum(t / .003, 1); fade = int(.4 * SR); out[-fade:] *= np.linspace(1, 0, fade)
    return out
T = g["duration"]; L = np.zeros(int(T * SR) + SR); R = L.copy()
for s in g["strikes"]:
    leaf = s["kind"] == "leaf"; m = s["midi"]
    sig = voice(m, P["CHIME"] if leaf else P["BELL"], 3.0 if leaf else 7.0, 0.6 if m > 76 else 0.8 if m > 68 else 1.05)
    i = int(s["t"] * SR); th = (s["pan"] + 1) * np.pi / 4; sig = sig[:len(L) - i]
    L[i:i + len(sig)] += sig * s["gain"] * np.cos(th); R[i:i + len(sig)] += sig * s["gain"] * np.sin(th)
n = int(3.5 * SR); ir = rng.normal(size=(2, n)) * np.exp(-np.arange(n) / SR / .8); ir[:, :int(.015 * SR)] = 0; ir = lfilter([.1], [1, -.9], ir, axis=1)
for ch, k in ((L, 0), (R, 1)):
    ch += .45 * fftconvolve(ch, ir[k])[:len(ch)] / np.sqrt((ir[k] ** 2).sum())
x = np.stack([L, R], 1); peak = np.abs(x).max(); x = np.tanh(x / peak * 1.2) / np.tanh(1.2) * .7
fo = np.linspace(1, 0, int(3 * SR)); x[-len(fo):] *= fo[:, None]
w = wave.open(sys.argv[2], "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype("<i2").tobytes()); w.close()
print(f"seed {g['seed']}: {len(g['strikes'])} strikes, {len(x) / SR:.1f} seconds; peak before shaping {peak:.2f}")
