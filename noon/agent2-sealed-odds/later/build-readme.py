"""Fill README.src.md from analyse.out, after.out, verdicts.out and fill.json.   usage: python -I build-readme.py"""
import json, re
s = open("README.src.md").read(); a = open("analyse.out").read(); fill = json.load(open("fill.json"))
m = re.search(r"sealed odds ([\d.]+); correction A .*? ([\d.]+) \(.*?\); correction B .*? ([\d.]+) \(", a); lo = re.findall(r"([AB]) minus sealed: .*?resampling whole studies ([+-][\d.]+) to ([+-][\d.]+)", a)
allm = re.search(r"   all +135 lines; .*?share that held ([\d.]+); my mean odds ([\d.]+)", a)
num = {"A-SEALED": m.group(1), "A-A": m.group(2), "A-BLO": lo[1][1].replace("-", "−"), "A-BHI": lo[1][2], "A-ALO": lo[0][1].replace("-", "−"), "A-AHI": lo[0][2], "A-B": m.group(3), "A-SHARE": allm.group(1), "A-MEAN": allm.group(2)}
for k in sorted(num, key=len, reverse=True): s = s.replace(k, num[k])
s = s.replace("ANALYSE-HERE", a[:a.index("\n6. The sealed sheet")].rstrip("\n")).replace("AFTER-HERE", open("after.out").read().rstrip("\n")).replace("VERDICTS-HERE", open("verdicts.out").read().rstrip("\n")).replace("AFTER2-HERE", open("after2.out").read().rstrip("\n"))
for k, v in fill.items(): assert s.count(k) >= 1, k; s = s.replace(k, v)
left = re.findall(r"[A-Z0-9]+-HERE|REFEREE-[A-Z]+|WRITTEN|A-[A-Z]+", s); assert not left, left
open("README.md", "w").write(s); print("README.md", len(s), "bytes")
