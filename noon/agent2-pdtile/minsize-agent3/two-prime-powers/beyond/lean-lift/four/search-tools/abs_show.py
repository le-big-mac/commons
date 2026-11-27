# Print title, authors and abstract from saved arXiv abstract pages (paths given as arguments).
import sys, re, html
for path in sys.argv[1:]:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except Exception as exc:
        print(path, "unreadable:", exc); continue
    def meta(name):
        m = re.findall(r'<meta name="%s" content="([^"]*)"' % name, text)
        return [html.unescape(x) for x in m]
    print("==", path)
    print("title:", "; ".join(meta("citation_title")))
    print("authors:", "; ".join(meta("citation_author")))
    print("date:", "; ".join(meta("citation_date")), "| online:", "; ".join(meta("citation_online_date")))
    m = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', text, re.S)
    if m:
        a = re.sub(r"<[^>]+>", "", m.group(1))
        print("abstract:", " ".join(html.unescape(a).split()))
    m = re.search(r'<td class="tablecell comments[^"]*">(.*?)</td>', text, re.S)
    if m:
        print("comments:", " ".join(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split()))
    m = re.search(r'<td class="tablecell jref">(.*?)</td>', text, re.S)
    if m:
        print("journal:", " ".join(html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).split()))
    print()
