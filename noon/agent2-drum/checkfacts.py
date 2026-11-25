"""Evidence for the checklist: the README's numbers against the outputs, its tallies against the scorecards, and its risky words.
usage: python -I checkfacts.py README.md > checkfacts.out"""
import sys, re
RAW = open(sys.argv[1]).read(); R = ' '.join(RAW.split())      # line breaks in the README are not part of its sentences
rd = lambda f: open(f).read(); ok = bad = 0
def check(name, cond, detail=""):
    global ok, bad; ok += bool(cond); bad += (not cond); print(("PASS  " if cond else "FAIL  ") + name + (("   " + detail) if detail else ""))
v1, v2 = rd("verdicts.out"), rd("verdicts2.out")
held = v1.count(" held ") + v2.count(" held  ") ; lines = len(re.findall(r"^[DGL]\d ", v1 + v2, re.M)); heldn = len(re.findall(r"^[DGL]\d .*?odds \d\.\d\d  held", v1 + v2, re.M)); guessed = len(re.findall(r"^[DGL]\d\s+guessed", v1 + v2, re.M)); gheld = len(re.findall(r"^[DGL]\d\s+guessed\s+odds \d\.\d\d  held", v1 + v2, re.M))
words = {12: "Twelve", 10: "ten"}
check("the tally in 'In short' equals the scorecards", f"{words.get(lines, '?')} sealed lines on three sheets; {words.get(heldn, '?')} held" in R and f"marked guessed, {guessed} lines, {gheld} held" in R, f"scorecards: {lines} lines, {heldn} held; guessed {guessed}, held {gheld}")
for line in re.findall(r"^[DGL]\d .*$", v1 + v2, re.M):
    lab = line.split()[0]; h = "  held" in line; row = re.search(rf"^\| {lab} \|.*$", RAW, re.M); check(f"table row {lab} says {'held' if h else 'failed'}", row and (("**failed**" in row.group(0)) != h))
for name, f, strings in (("plain ratios", "modes.out", ["1.5933", "2.1355", "2.2954", "2.6531", "2.9173", "3.1555", "3.5001", "3.5985"]), ("best disc", "modes.out", ["s = 9.938, k = 0.4004", "3.157%", "1.9369", "2.9467", "3.0541", "3.9653", "4.1029", "4.9625", "5.1579", "4.8421", "3.51%", "3.35%", "5.9330", "6.2520", "5.4677"]),
                         ("s = 4", "modes.out", ["1.6857", "1.8921", "1.9528", "1.8771", "1.7871", "1.7113"]), ("other measures", "after.out", ["s =   8.37, k = 0.425: 2.56%", "2.35%", "s =   8.91, k = 0.414: 2.14%"]),
                         ("sharpness", "after.out", ["s = 8: 8.4%", "s = 12: 5.3%", "k = 0.35: 9.2%", "k = 0.45: 6.4%"]), ("graded", "after2.out", ["s =   80: k = 0.563; largest miss 2.37%", "s =  120: k = 0.564; largest miss 2.31%", "s =  240: k = 0.566; largest miss 2.24%", "s =  640: k = 0.567; largest miss 2.21%", "s =   20: k = 0.543; largest miss 3.26%", "s =   20: k = 0.543"]),
                         ("layers", "layers-2.out", ["1.555%", "12.94 inside 0.438; 5.63 inside 0.234", "-27, +4, -27, +22, -14, +25, +18, +26"]), ("layers 3", "layers-3.out", ["1.433%", "-24, +6, -24, +23, -21, +25, -0, +25"]), ("layers longer", "layers-2-s201.out", ["1.481%", "18.15 inside 0.447; 8.85 inside 0.244"]),
                         ("layers 3 seeds", "layers-3-s301.out", ["1.404%"]), ("", "layers-3-s302.out", ["1.464%"]), ("", "layers-3-s303.out", ["1.569%"]), ("", "layers-3-s304.out", ["1.457%"]), ("four layers", "layers-4-s401.out", ["1.344%"]),
                         ("discord", "clash.out", ["strokes-plain.wav          semitone clash 0.589", "strokes-disc.wav           semitone clash 1.576", "strokes-two-layers.wav     semitone clash 0.061", "strokes-three-layers.wav   semitone clash 0.080", "plain-at0.3.wav    semitone clash 0.478", "disc-at0.3.wav     semitone clash 1.523", "two-layers-at0.3.wav semitone clash 0.068", "plain-at0.7.wav    semitone clash 0.443", "disc-at0.7.wav     semitone clash 1.271", "two-layers-at0.7.wav semitone clash 0.061"])):
    t = rd(f); miss = [x for x in strings if x not in t]; check(f"numbers quoted from {f} are in it", not miss, "missing: " + "; ".join(miss) if miss else "")
check("the three equal misses", all(x in rd("modes.out") for x in ["(1,1)   1.9369   2     -3.16%", "(2,2)   5.1579   5     +3.16%", "(0,3)   4.8421   5     -3.16%"]))
check("two discs at fixed weight and beyond the cap", all(x in rd("after3-3.out") for x in ("1.43: largest miss 3.16%", "1.50: largest miss 2.43%", "1.60: largest miss 1.72%", "2.00: largest miss 1.61%", "2.79: largest miss 1.53%", "4.60: largest miss 1.46%", "9.60: largest miss 1.36%")) and all(x in rd("after3-2.out") for x in ("80: largest miss 1.305%", "160: largest miss 1.282%", "640: largest miss 1.264%")) and "1.361%" in rd("after3-1.out"))
check("the parabola at fixed weight and heavier discs", all(x in rd("after3-45.out") for x in ("1.43: largest miss 6.72%", "2.00: largest miss 4.43%", "3.00: largest miss 3.10%", "4.00: largest miss 2.79%", "12.00: best k = 0.417; largest miss 4.02%", "14.00: best k = 0.423; largest miss 4.23%", "40.00: best k = 0.440; largest miss 5.51%", "are 62 apart", "(1,2) 59", "span 109")))
check("the discord table", all(x in rd("discord.out") for x in ("0.589    1.576    0.061    0.072", "0.600    0.609", "0.602    0.563", "0.616    0.303", "0.658    2.222", "plain 0.023; disc 0.021; two layers 0.012; harmonic 1 to 6 0.003")))
check("3.16% is 54 cents", abs(1200 * __import__('math').log2(1.03157) - 54) < 0.6, f"{1200 * __import__('math').log2(1.03157):.1f}")
check("added mass: disc 1.4 skins, graded at 20 is 2.8", "disc 1.43" in rd("after.out") and "added mass   2.80" in rd("after2.out"))
import json, math
cents = []
for f in ("layers-2.json", "layers-2-s201.json", "layers-3.json", "layers-3-s301.json", "layers-3-s302.json", "layers-3-s303.json", "layers-3-s304.json", "layers-4-s401.json"):
    r = json.load(open(f))['ratios']; cents.append((1200 * math.log2(r[1] / 2), 1200 * math.log2(r[3] / 3), 1200 * math.log2(r[4] / 4)))
check("in all eight layered answers (1,1) and (0,2) are 23 to 27 cents flat and (3,1) 21 to 24 sharp", all(-27.5 <= a <= -22.5 and -27.5 <= b <= -22.5 and 20.5 <= c <= 24.5 for a, b, c in cents) and "every layered answer of mine" in R, "; ".join(f"{a:.0f}, {b:.0f}, {c:+.0f}" for a, b, c in cents))
check("the two methods: 4 parts in ten million; 3 in ten thousand", all(x in rd("check.out") for x in ("3.4e-07", "2.7e-07", "3.9e-07")) and "2.7e-04" in rd("after.out"))
# the note of 04:37 UTC, 23 November: the 2000 paper's ring load beside mine
import os
_mp = os.path.expanduser("~/drumair-data/malu/0001030.txt")
if os.path.exists(_mp):
    _mt = ' '.join(open(_mp, errors='replace').read().split()); _lab = ("1(0,0) 1.00 1.07", "2(1,0) 1.59 2.00", "3(2,0) 3.14 2.98", "4(0,1) 2.30 2.99", "5(3,0) 3.65 4.00", "6(1,1) 2.92 4.00", "7(4,0) 3.16 5.01", "8(2,1) 3.50 5.01", "9(0,2) 3.60 5.02")
    _rg = [1.00, 1.96, 2.98, 3.03, 4.02, 3.95, 5.02, 5.00, 4.80]; _w = max(abs(r / t - 1) for r, t in zip(_rg, (1, 2, 3, 3, 4, 4, 5, 5, 5)))
    _rows = [l.split("|") for l in RAW.split("\n") if re.match(r"\| [\d.]+ \| [\d.]+% \| [\d.]+% \| [\d.]+% \| [\d.]+% \| [\d.]+% \| [\d.]+% \| \d+ \|", l)]; _m = {float(c[1]): float(c[6].strip(" %")) for c in _rows}; _sel = [v for k, v in _m.items() if k >= 1.43]
    check("the 2000 paper's ring load: nine modes as printed, within 4%; mine 0.77% (1.43 skins) to 0.53% (12 skins) on 40 rings",
          all(f"{l} {r:.2f}" in _mt for l, r in zip(_lab, _rg)) and "Concentric rings with varying density were con- sidered." in _mt and f"{100 * _w:.0f}" == "4" and _m[1.43] == 0.77 == max(_sel) and _m[12.0] == 0.53 == min(_sel)
          and "at 1.00, 1.96, 2.98, 3.03, 4.02, 3.95, 5.02, 5.00 and 4.80, so within 4% of 1, 2, 3, 3, 4, 4, 5, 5, 5 as printed" in R and "within 0.77% (1.43 skins) to 0.53% (12 skins) on 40 rings" in R, f"{100 * _w:.2f}")
else: print("SKIP  the saved text of the 2000 paper is not here")
print(f"\n{ok} checks passed, {bad} failed\n\nRisky words in the README, each with its line, for reading one by one:")
for wds in ("sing", "tun", "best", "every", " all ", "never", "must", "ruled", "because", "better", "worse", "halve", "sharp"):
    hits = [(i + 1, l.strip()) for i, l in enumerate(RAW.split("\n")) if wds in l.lower()]
    print(f"  '{wds.strip()}': {len(hits)} lines" + ("" if not hits else ": " + "; ".join(str(i) for i, _ in hits)))
