"""Fills the README's tables from tables.md and the few fields that change.   usage: python build-readme.py README.src.md tables.md README.md KEY=VALUE..."""
import sys, re
src = open(sys.argv[1], encoding='utf-8').read(); tab = open(sys.argv[2], encoding='utf-8').read()
parts = re.split(r"^\*\*Table (\d)\..*$", tab, flags=re.M)
for i in range(1, len(parts), 2): src = src.replace("{{TABLE%s}}" % parts[i], parts[i + 1].strip())
for kv in sys.argv[4:]:
    k, v = kv.split("=", 1); src = src.replace("{{%s}}" % k, v)
left = re.findall(r"\{\{[A-Z0-9\-]+\}\}", src)
open(sys.argv[3], 'w', encoding='utf-8').write(src); print("written;", "unfilled:", left or "none")
