"""Put core.js and the numbers in the notes inside the page, so that thunen.html is one file.   usage: python -I build.py"""
import re, subprocess, json
src = open("page.src.html").read(); core = open("core.js").read()
assert src.count("/*CORE*/") == 1 and "</script>" not in core
# the three numbers in the notes come from core.js itself, run in node
vals = json.loads(subprocess.run(["node", "-e", "const T=require('./core.js'); const r=T.rings(1.5,8); console.log(JSON.stringify({zero: T.distance(0,1.5).toFixed(0), r4: r[3].toFixed(1), r5: r[4].toFixed(1)}))"], capture_output=True, text=True, check=True).stdout)
out = src.replace("/*CORE*/", core); out = re.sub(r"\{\{([a-z0-9]+)\}\}", lambda m: vals[m.group(1)], out); assert "{{" not in out
open("thunen.html", "w").write(out); print("thunen.html", len(out.encode()), "bytes", vals)
