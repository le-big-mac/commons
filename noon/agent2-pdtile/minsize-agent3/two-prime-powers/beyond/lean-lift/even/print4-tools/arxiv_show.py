import sys, re, html
# usage: python3 -I arxiv_show.py FILE...   -- prints id, date, title of each entry in an arXiv API answer
for p in sys.argv[1:]:
    try:
        s = open(p, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print(p, "unreadable", e); continue
    m = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", s)
    ents = re.findall(r"<entry>(.*?)</entry>", s, flags=re.S)
    print("  total:", m.group(1) if m else "?", "shown:", len(ents))
    for e in ents:
        i = re.search(r"<id>(.*?)</id>", e, flags=re.S)
        t = re.search(r"<title>(.*?)</title>", e, flags=re.S)
        d = re.search(r"<published>(.*?)</published>", e, flags=re.S)
        a = re.findall(r"<name>(.*?)</name>", e, flags=re.S)
        print("   ", (i.group(1) if i else "").replace("http://arxiv.org/abs/", ""), (d.group(1)[:10] if d else ""), "|", html.unescape(re.sub(r"\s+", " ", t.group(1)) if t else "")[:150], "|", ", ".join(a[:4])[:80])
