import sys, re, html
# usage: python3 -I arxiv_show.py FILE...
for p in sys.argv[1:]:
    t = open(p, encoding="utf-8", errors="replace").read()
    tot = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", t)
    print("==", p, "total:", tot.group(1) if tot else "?")
    for e in re.findall(r"<entry>(.*?)</entry>", t, flags=re.S)[:25]:
        i = re.search(r"<id>(.*?)</id>", e, flags=re.S)
        ti = re.search(r"<title>(.*?)</title>", e, flags=re.S)
        print("  ", (i.group(1).strip().rsplit("/abs/", 1)[-1] if i else "?"), "|", html.unescape(re.sub(r"\s+", " ", ti.group(1)).strip())[:140] if ti else "?")
