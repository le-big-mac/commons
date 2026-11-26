"""Strip tags from the archived page; print text with rough block structure.
Usage: python -I strip.py PAGE.html [--raw-around WORD]
Reads the file as data only."""
import sys, re, html
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if tag in ('p', 'br', 'div', 'tr', 'li', 'h1', 'h2', 'h3', 'h4', 'table', 'ul', 'ol', 'blockquote', 'hr', 'td', 'title'):
            self.out.append('\n<%s>' % tag)
        if tag in ('a',):
            d = dict(attrs)
            if 'name' in d:
                self.out.append('[anchor name=%s]' % d['name'])
        if tag in ('i', 'em', 'b', 'strong', 'sup', 'font', 'span'):
            self.out.append('{%s}' % tag)
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip -= 1
        if tag in ('i', 'em', 'b', 'strong', 'sup', 'font', 'span'):
            self.out.append('{/%s}' % tag)
        if tag in ('p', 'div', 'blockquote', 'td', 'title'):
            self.out.append('</%s>\n' % tag)
    def handle_data(self, data):
        if self.skip:
            return
        self.out.append(data)

def main():
    path = sys.argv[1]
    raw = open(path, 'rb').read()
    try:
        s = raw.decode('utf-8')
        enc = 'utf-8'
    except UnicodeDecodeError:
        s = raw.decode('cp1252', errors='replace')
        enc = 'cp1252'
    p = P()
    p.feed(s)
    text = ''.join(p.out)
    text = re.sub(r'[ \t\r\f\v]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n', text)
    sys.stdout.write('ENCODING USED: %s; bytes %d\n' % (enc, len(raw)))
    sys.stdout.write(text)

main()
