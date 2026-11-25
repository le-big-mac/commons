"""I cannot hear the file, so this measures it: the level, and whether each stroke's own pitch is in the sound just after it.
usage: python -I listen.py hour.json sound.wav"""
import sys, json, wave
import numpy as np
g = json.load(open(sys.argv[1])); w = wave.open(sys.argv[2]); SR = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").reshape(-1, 2) / 32767.0; mono = x.mean(1)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
print(f"{len(x) / SR:.1f} s, peak {np.abs(x).max():.3f}, samples at full scale {int((np.abs(x) >= 0.999).sum())}, whole-file rms {20 * np.log10(np.sqrt((x ** 2).mean())):.1f} dB")
for part in g.get("parts", []): print(f"  {part['at']}: from {part['starts']:.1f} s, rows {part['rows']}" + (f", then {part['strikes']} strokes" if part["strikes"] else ""))
for kind, length in (("bell", 0.30), ("hour", 0.80)):                     # the deep bell needs a longer look: a short window blurs a low pitch
    found = []; n = int(length * SR); win = np.hanning(n)
    for s in g["notes"]:
        if s["kind"] != kind: continue
        i = int((s["t"] + 0.02) * SR); seg = mono[i:i + n]
        if len(seg) < n: continue
        sp = np.abs(np.fft.rfft(seg * win, 8 * n)); fr = np.fft.rfftfreq(8 * n, 1 / SR); f = hz(s["midi"])
        band = (fr > f * 0.985) & (fr < f * 1.015); wide = (fr > f * 0.8) & (fr < f * 1.25) & ~((fr > f * 0.94) & (fr < f * 1.06)); j = np.argmax(sp * band)
        found.append(abs(fr[j] / f - 1) < 0.008 and sp[j] > 4 * np.median(sp[wide]))
    print(f"{kind} strokes whose own pitch stands out in the {length:.2f} s after them (within 0.8%, four times the level around): {sum(found)} of {len(found)}")
