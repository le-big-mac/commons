"""Put core.js, the setting, the grown bed and the numbers in the notes inside the page, so that braid.html is one file.
usage: python -I build.py        (after build-readme.py, which writes tokens.json)"""
import json, re
src = open("page.src.html").read(); core = open("core.js").read(); grown = open("grown.json").read(); setting = open("setting.json").read().strip(); T = json.load(open("tokens.json"))
for mark in ("/*CORE*/", "/*GROWN*/", "/*SETTING*/"): assert src.count(mark) == 1, mark
assert "</script>" not in core
out = src.replace("/*CORE*/", core).replace("/*GROWN*/", grown).replace("/*SETTING*/", setting)
out = re.sub(r"\{\{([A-Za-z0-9_-]+)\}\}", lambda m: T[m.group(1)], out); assert "{{" not in out
open("braid.html", "w").write(out); print("braid.html", len(out), "bytes")
