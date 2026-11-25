"""Puts the tables and the scorecard into the README.   usage: python -I build-readme.py README.src.md README.md"""
import sys, re
src = open(sys.argv[1]).read(); t = open("tables.out").read(); blocks = dict(re.findall(r"^([A-Z]+-ROWS)\n((?:\|.*\n)+)", t, re.M))
for k, v in blocks.items(): assert src.count(k) == 1, k; src = src.replace(k + "\n", v)
src = src.replace("VERDICTS-HERE", open("verdicts.out").read().rstrip("\n")); open(sys.argv[2], "w").write(src); print(len(blocks), "tables;", len(src.splitlines()), "lines;", "placeholders left:", re.findall(r"[A-Z]+-(?:HERE|NOTE|ROWS|CHANGES|SAMPLED)|WRITTEN", src))
