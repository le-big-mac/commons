"""usage: python -I totext.py FILE.html [--links]  -> prints the visible text (scripts and styles dropped).
With --links, link targets are printed in square brackets after the link text."""
import sys, re
from html.parser import HTMLParser

LINKS = "--links" in sys.argv[2:]

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.out = []
        self.href = []
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag in ("p", "br", "div", "tr", "li", "h1", "h2", "h3", "h4", "table", "td", "th", "dd", "dt"):
            self.out.append("\n" if tag not in ("td", "th") else " | ")
        if tag == "a" and LINKS:
            self.href.append(dict(attrs).get("href") or "")
        if tag == "img" and LINKS:
            a = dict(attrs)
            self.out.append(" [img %s alt=%r] " % (a.get("src"), a.get("alt")))
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1
        if tag in ("p", "div", "tr", "li", "h1", "h2", "h3", "h4"):
            self.out.append("\n")
        if tag == "a" and LINKS and self.href:
            h = self.href.pop()
            if h and not self.skip:
                self.out.append(" [%s] " % h)
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

raw = open(sys.argv[1], "rb").read().decode("utf-8", "replace")
p = P()
p.feed(raw)
text = "".join(p.out)
text = re.sub(r"[ \t\r\f\v]+", " ", text)
text = re.sub(r"\n\s*\n+", "\n", text)
print(text)
