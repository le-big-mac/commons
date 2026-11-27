import sys, re, html
# usage: python3 -I arxiv_show.py FILE...   (plain regex reading of the Atom feed; no XML parser on untrusted data)
for p in sys.argv[1:]:
    try:
        t = open(p, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print(p, "unreadable", e); continue
    m = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", t)
    print("==", p, "total:", m.group(1) if m else "?")
    for e in re.findall(r"<entry>(.*?)</entry>", t, flags=re.S):
        i = re.search(r"<id>(.*?)</id>", e, flags=re.S)
        ti = re.search(r"<title>(.*?)</title>", e, flags=re.S)
        au = re.findall(r"<name>(.*?)</name>", e, flags=re.S)
        pub = re.search(r"<published>(.*?)</published>", e, flags=re.S)
        print("  ", (i.group(1) if i else "?").replace("http://arxiv.org/abs/", ""), "|", (pub.group(1)[:10] if pub else ""), "|",
              " ".join(html.unescape(ti.group(1)).split())[:140] if ti else "?", "|", ", ".join(au[:4])[:80])
