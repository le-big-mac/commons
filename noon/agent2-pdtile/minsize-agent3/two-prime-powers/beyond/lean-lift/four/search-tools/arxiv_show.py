# Print id, date, title, authors from saved arXiv API (Atom) results. Usage: arxiv_show.py FILE [FILE ...]
import sys, re, html
for path in sys.argv[1:]:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    total = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", text)
    entries = re.findall(r"<entry>(.*?)</entry>", text, re.S)
    print("==", path, "total:", total.group(1) if total else "?", "shown:", len(entries))
    for e in entries:
        def one(tag):
            m = re.search(r"<%s>(.*?)</%s>" % (tag, tag), e, re.S)
            return " ".join(html.unescape(m.group(1)).split()) if m else ""
        authors = re.findall(r"<name>(.*?)</name>", e)
        print("  %s | %s | %s | %s" % (one("id").replace("http://arxiv.org/abs/", ""), one("published")[:10], one("title"), ", ".join(authors[:4])))
