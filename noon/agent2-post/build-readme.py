"""Fill README.src.md from tables.out, verdicts.out and fill.json (the few sentences written by hand).   usage: python -I build-readme.py"""
import json, re
s = open("README.src.md").read(); t = open("tables.out").read(); fill = json.load(open("fill.json"))
def table(k):
    m = re.search(rf"TABLE {k}\. (.*?)\n\n(.*?)(?=\n\nTABLE|\Z)", t, re.S); return f"**Table {k}.** {m.group(1)}\n\n{m.group(2).strip()}"
for k in (1, 2, 3, 4): s = s.replace(f"TABLE{k}-HERE", table(k))
s = s.replace("VERDICTS-HERE", open("verdicts.out").read().rstrip("\n"))
sec = open("second.out").read(); i = sec.index("The least number of codes left unnamed"); j = sec.index("The same by name2.py"); k = sec.index("W at every lag"); l = sec.index("\n\nF1 ")
s = s.replace("SECOND-HERE", "```\n" + sec[i:j].rstrip("\n") + "\n\n" + sec[k:l].rstrip("\n") + "\n```")
s = s.replace("VERDICTS2-HERE", open("verdicts2.out").read().rstrip("\n"))
for k, v in fill.items(): assert s.count(k) >= 1, k; s = s.replace(k, v)
left = re.findall(r"[A-Z0-9]+-HERE|REFEREE-[A-Z]+|WRITTEN", s); assert not left, left
open("README.md", "w").write(s); print("README.md", len(s), "bytes")
