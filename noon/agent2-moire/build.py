"""Put core.js inside the page, so that moire.html is one file.   usage: python -I build.py"""
src = open("page.src.html").read(); core = open("core.js").read()
assert src.count("/*CORE*/") == 1 and "</script>" not in core
open("moire.html", "w").write(src.replace("/*CORE*/", core)); print("moire.html", len(src) + len(core), "bytes")
