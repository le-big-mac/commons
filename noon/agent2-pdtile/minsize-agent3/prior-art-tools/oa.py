#!/usr/bin/env python
"""Print OpenAlex results (works list or a single work) as short lines.

usage: python -I oa.py RESULT.json
"""
import json
import sys


def line(w):
    ids = w.get("ids", {})
    loc = (w.get("primary_location") or {}).get("landing_page_url") or ""
    au = ", ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:6])
    return "%s | %s | %s | %s | cited_by=%s | %s | %s" % (
        w.get("id", "").rsplit("/", 1)[-1], w.get("publication_date"), w.get("display_name"), au,
        w.get("cited_by_count"), ids.get("doi", ""), loc)


def main():
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    if "results" in d:
        print("count:", d.get("meta", {}).get("count"), "| shown:", len(d["results"]))
        for w in d["results"]:
            print(line(w))
    elif "id" in d:
        print(line(d))
    else:
        print(json.dumps(d)[:600])


if __name__ == "__main__":
    main()
