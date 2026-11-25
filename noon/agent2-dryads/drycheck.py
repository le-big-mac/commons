"""Is the sound the page makes the sound the grove's strikes call for? The page renders its first seconds with no room and no shaping
(shot-dryads.js); this builds the same from the JSON in numpy and compares.   usage: python -I drycheck.py grove.json page-dry.f32"""
import sys, json
import numpy as np
SR = 44100; g = json.load(open(sys.argv[1])); P = g["params"]; raw = np.fromfile(sys.argv[2], "<f4"); n = len(raw) // 2; page = np.stack([raw[:n], raw[n:]], 1); secs = n / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12); ref = np.zeros((n + 8 * SR, 2)); count = 0
for s in g["strikes"]:
    if s["t"] >= secs: continue
    leaf = s["kind"] == "leaf"; table = P["CHIME"] if leaf else P["BELL"]; length = 3.0 if leaf else 7.0; m = s["midi"]; bright = 0.6 if m > 76 else 0.8 if m > 68 else 1.05
    k = int(length * SR); i0 = int(round(s["t"] * SR)); t = np.arange(k) / SR + (i0 / SR - s["t"]); sig = np.zeros(k)       # t is time since the strike, at each sample
    for j, (ratio, level, tau) in enumerate(table):
        env = np.where(t < 0.003, np.maximum(t, 0) / 0.003, np.exp(-(t - 0.003) / tau)) * level * (bright if j >= 3 else 1)
        sig += env * np.sin(2 * np.pi * hz(m) * ratio * np.maximum(t, 0))
    sig *= s["gain"] * np.clip((length - t) / 0.4, 0, 1); th = (s["pan"] + 1) * np.pi / 4
    ref[i0:i0 + k, 0] += sig * np.cos(th); ref[i0:i0 + k, 1] += sig * np.sin(th); count += 1
ref = ref[:n]; d = page - ref
print(f"{secs:.0f} s, {count} strikes; page rms {np.sqrt((page ** 2).mean()):.4f}, mine {np.sqrt((ref ** 2).mean()):.4f}")
print(f"correlation left {np.corrcoef(page[:, 0], ref[:, 0])[0, 1]:.5f}, right {np.corrcoef(page[:, 1], ref[:, 1])[0, 1]:.5f}; difference {20 * np.log10(np.sqrt((d ** 2).mean()) / np.sqrt((ref ** 2).mean())):.1f} dB below the signal; largest {np.abs(d).max():.4f}")
