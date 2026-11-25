"""I cannot hear the file, so this measures it: level through the piece, and whether each strike's own pitch is in the sound when it should be.
usage: python -I listen.py grove.json sound.wav"""
import sys, json, wave
import numpy as np
g = json.load(open(sys.argv[1])); w = wave.open(sys.argv[2]); SR = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, 2) / 32767.0
hz = lambda m: 440 * 2 ** ((m - 69) / 12); mono = x.mean(1)
print(f"{len(x) / SR:.1f} s, peak {np.abs(x).max():.3f}, samples at full scale {int((np.abs(x) >= 0.999).sum())}, whole-file rms {20 * np.log10(np.sqrt((x ** 2).mean())):.1f} dB")
print("level in each 10 s (dB rms), with the strikes that fall in it:")
for k in range(int(np.ceil(len(x) / SR / 10))):
    seg = x[k * 10 * SR:(k + 1) * 10 * SR]; r = np.sqrt((seg ** 2).mean()); n = sum(1 for s in g["strikes"] if 10 * k <= s["t"] < 10 * k + 10)
    print(f"  {10 * k:3d} s  {20 * np.log10(max(r, 1e-9)):6.1f}  {n:3d}  " + "#" * int(max(0, 60 + 20 * np.log10(max(r, 1e-9))) / 1.5))
for length in (0.30, 0.60):
    found = {}; n = int(length * SR); win = np.hanning(n); off = []
    for s in g["strikes"]:
        i = int((s["t"] + 0.02) * SR); seg = mono[i:i + n]
        if len(seg) < n: continue
        sp = np.abs(np.fft.rfft(seg * win, 8 * n)); fr = np.fft.rfftfreq(8 * n, 1 / SR); f = hz(s["midi"])
        band = (fr > f * 0.985) & (fr < f * 1.015); wide = (fr > f * 0.8) & (fr < f * 1.25) & ~((fr > f * 0.94) & (fr < f * 1.06))
        j = np.argmax(sp * band); ok = abs(fr[j] / f - 1) < 0.008 and sp[j] > 4 * np.median(sp[wide])
        found.setdefault(s["kind"], []).append(ok)
        if not ok: off.append((s["midi"], abs(fr[j] / f - 1), sp[j] / np.median(sp[wide])))
    print(f"strikes whose own pitch stands out of the spectrum in the {length:.1f} s after them (within 0.8%, four times the level around):")
    for k, v in found.items(): print(f"  {k:6s} {sum(v):3d} of {len(v)}")
    if off: print(f"  the {len(off)} that do not: highest note MIDI {max(o[0] for o in off)}; their peaks are {100 * min(o[1] for o in off):.1f}% to {100 * max(o[1] for o in off):.1f}% off and {min(o[2] for o in off):.0f} to {max(o[2] for o in off):.0f} times the level around")
L, R = x[:, 0], x[:, 1]; print(f"left/right balance: {20 * np.log10(np.sqrt((L ** 2).mean()) / np.sqrt((R ** 2).mean())):+.1f} dB; correlation of the two channels {np.corrcoef(L, R)[0, 1]:.2f}")
