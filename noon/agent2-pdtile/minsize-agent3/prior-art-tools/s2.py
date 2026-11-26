#!/usr/bin/env python
"""Print a Semantic Scholar citations result: date, arXiv id, title.

usage: python -I s2.py RESULT.json
"""
import json
import sys

d = json.load(open(sys.argv[1], encoding="utf-8"))
if "data" not in d:
    print(json.dumps(d)[:500])
    sys.exit(0)
print("shown:", len(d["data"]), "| next:", d.get("next"))
for it in d["data"]:
    p = it.get("citingPaper", {})
    ext = p.get("externalIds") or {}
    print(p.get("publicationDate") or p.get("year"), "|", ext.get("ArXiv", ext.get("DOI", "")), "|", p.get("title"))
