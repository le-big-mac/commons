import sys, re, html
# usage: python3 -I abs_show.py FILE...   (prints title and abstract from an arXiv API answer)
for p in sys.argv[1:]:
    t = open(p, encoding="utf-8", errors="replace").read()
    for e in re.findall(r"<entry>(.*?)</entry>", t, flags=re.S):
        ti = re.search(r"<title>(.*?)</title>", e, flags=re.S)
        su = re.search(r"<summary>(.*?)</summary>", e, flags=re.S)
        au = re.findall(r"<name>(.*?)</name>", e, flags=re.S)
        print("TITLE:", " ".join(html.unescape(ti.group(1)).split()) if ti else "?")
        print("AUTHORS:", ", ".join(au)[:200])
        print("ABSTRACT:", " ".join(html.unescape(su.group(1)).split())[:1500] if su else "?")
