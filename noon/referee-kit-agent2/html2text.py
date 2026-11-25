"""Plain text of a saved HTML page, for reading (scripts and styles dropped).   usage: python -I html2text.py page.html > page.txt"""
import sys, html, re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(self): super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"): self.skip += 1
        if tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr", "td", "th"): self.out.append("\n")
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"): self.skip = max(0, self.skip - 1)
    def handle_data(self, data):
        if not self.skip: self.out.append(data)
p = P(); p.feed(open(sys.argv[1], errors="replace").read()); t = re.sub(r"[ \t]+", " ", "".join(p.out)); print(re.sub(r"\n\s*\n+", "\n", t))
