"""Is the sound the page makes the sound its bells call for?  shot-river.js has the page render a minute of its bells with no room
(seedN-page-dry.f32) and with the room and the limiter (seedN-page-wet.f32); this builds the first from the list of bells in numpy
and compares, and reports how loud the second gets.   usage: python -I drycheck.py shots/seed3-bells.json shots/seed3-page-dry.f32 shots/seed3-page-wet.f32"""
import sys, json, re
import numpy as np
SR = 44100; g = json.load(open(sys.argv[1]))
core = open("core.js").read()
BELL = json.loads(re.search(r"var BELL = (\[\[.*?\]\]);", core).group(1))
raw = np.fromfile(sys.argv[2], "<f4"); n = len(raw) // 2; page = np.stack([raw[:n], raw[n:]], 1); secs = n / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12); ref = np.zeros((n + 8 * SR, 2)); count = 0
for s in g["strikes"]:
    if s["t"] >= secs: continue
    length = 7.0; m = s["midi"]; bright = 0.8 if m > 68 else 1.05
    k = int(length * SR); i0 = int(np.ceil(s["t"] * SR)); t = np.arange(k) / SR + (i0 / SR - s["t"]); sig = np.zeros(k)     # t: time since the strike, at each sample
    for j, (ratio, level, tau) in enumerate(BELL):
        env = np.where(t < 0.003, np.maximum(t, 0) / 0.003, np.exp(-(t - 0.003) / tau)) * level * (bright if j >= 3 else 1)
        sig += env * np.sin(2 * np.pi * hz(m) * ratio * np.maximum(t, 0))
    sig *= s["gain"] * np.clip((length - t) / 0.4, 0, 1); th = (s["pan"] + 1) * np.pi / 4
    ref[i0:i0 + k, 0] += sig * np.cos(th); ref[i0:i0 + k, 1] += sig * np.sin(th); count += 1
ref = ref[:n]; d = page - ref
print(f"{secs:.0f} s, {count} bells; page rms {np.sqrt((page ** 2).mean()):.4f}, mine {np.sqrt((ref ** 2).mean()):.4f}")
print(f"correlation left {np.corrcoef(page[:, 0], ref[:, 0])[0, 1]:.5f}, right {np.corrcoef(page[:, 1], ref[:, 1])[0, 1]:.5f}; difference {20 * np.log10(np.sqrt((d ** 2).mean()) / np.sqrt((ref ** 2).mean())):.1f} dB below the signal")
wet = np.fromfile(sys.argv[3], "<f4"); wet = np.stack([wet[:len(wet) // 2], wet[len(wet) // 2:]], 1)
win = SR // 2; rms = np.sqrt(np.array([(wet[i:i + win] ** 2).mean() for i in range(0, len(wet) - win, win)]))
print(f"with the room and the limiter: peak {np.abs(wet).max():.3f} of full scale, samples at or above 0.99: {int((np.abs(wet) >= 0.99).sum())}; loudest half second rms {rms.max():.3f}, quietest {rms.min():.4f}")
gaps = np.diff(sorted(s["t"] for s in g["strikes"] if s["t"] < secs))
print(f"bells per minute {count / secs * 60:.0f}; longest silence between bells {gaps.max():.1f} s, shortest gap {gaps.min():.2f} s; notes used: {sorted(set(s['midi'] for s in g['strikes']))}")
