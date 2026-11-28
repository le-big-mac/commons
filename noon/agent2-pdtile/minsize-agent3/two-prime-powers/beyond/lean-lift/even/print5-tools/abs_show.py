import sys, re, html
# usage: python3 -I abs_show.py FILE   -- prints title and abstract of each entry of an arXiv API answer
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
for e in re.findall(r"<entry>(.*?)</entry>", s, flags=re.S):
    i = re.search(r"<id>(.*?)</id>", e, flags=re.S); t = re.search(r"<title>(.*?)</title>", e, flags=re.S); a = re.search(r"<summary>(.*?)</summary>", e, flags=re.S)
    print("##", i.group(1) if i else "", "|", html.unescape(re.sub(r"\s+", " ", t.group(1))) if t else "")
    print(html.unescape(re.sub(r"\s+", " ", a.group(1))) if a else ""); print()
