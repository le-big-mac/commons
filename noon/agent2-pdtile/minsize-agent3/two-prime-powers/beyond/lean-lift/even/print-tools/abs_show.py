import sys, re, html
# usage: python3 -I abs_show.py FILE...
for p in sys.argv[1:]:
    t = open(p, encoding="utf-8", errors="replace").read()
    ti = re.search(r'<meta name="citation_title" content="(.*?)"', t, flags=re.S)
    ab = re.search(r'<meta name="citation_abstract" content="(.*?)"\s*/?>', t, flags=re.S)
    if not ab:
        ab = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', t, flags=re.S)
    dt = re.search(r'<meta name="citation_date" content="(.*?)"', t)
    au = re.findall(r'<meta name="citation_author" content="(.*?)"', t)
    print("==", p)
    print("title:", html.unescape(ti.group(1)) if ti else "?")
    print("authors:", "; ".join(au), "| date:", dt.group(1) if dt else "?")
    print("abstract:", html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"\s+", " ", ab.group(1)))).strip() if ab else "?")
