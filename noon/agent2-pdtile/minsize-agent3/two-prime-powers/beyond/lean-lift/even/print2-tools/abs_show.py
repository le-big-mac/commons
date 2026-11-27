import sys, re, html
# usage: python3 -I abs_show.py FILE...
strip = lambda s: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()
for p in sys.argv[1:]:
    t = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r'<h1 class="title mathjax">(.*?)</h1>', t, flags=re.S)
    a = re.search(r'<blockquote class="abstract mathjax">(.*?)</blockquote>', t, flags=re.S)
    au = re.search(r'<div class="authors">(.*?)</div>', t, flags=re.S)
    j = re.search(r'<td class="tablecell jref">(.*?)</td>', t, flags=re.S)
    print("==", p); print(strip(m.group(1)) if m else "?"); print(strip(au.group(1)) if au else "?")
    print(strip(a.group(1)) if a else "?"); print("JREF:", strip(j.group(1)) if j else "-"); print()
