"""Builds the page: puts the tested core into play.src.html.   usage: python -I build.py OUT.html"""
import sys
core = open("core.js").read(); core = core[:core.index("if (typeof module !== 'undefined')")]; src = open("play.src.html").read(); assert "/*__CORE__*/" in src
open(sys.argv[1], "w").write(src.replace("/*__CORE__*/", core)); print(len(src) + len(core), "bytes")
