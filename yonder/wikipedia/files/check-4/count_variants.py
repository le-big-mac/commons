"""Second, independent count of the quoted passage (HTMLParser route) and a search for
any way of counting that gives 940 or 964. Usage: python -I count_variants.py PAGE.html"""
import sys, re
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'p'):
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('p', 'blockquote'):
            self.parts.append('\n')
    def handle_data(self, d):
        self.parts.append(d)

raw = open(sys.argv[1], 'rb').read().decode('utf-8')
p = P(); p.feed(raw)
txt = ''.join(p.parts)
a = txt.index('"King Mongkut\'s prediction surpassed')
b = txt.index('[L. Robert Morris')
c = txt.index('See Bradley, W.L.')
d = txt.index('1981.', c) + len('1981.')
e0 = txt.rindex('2 Apr 1833', 0, a)
oberlin_a = txt.rindex('"The family papers', 0, a)
segs = {
 'quoted passage (first line to closing mark)': txt[a:b],
 'quoted passage without first line': txt[txt.index('"In the 19th century', a):b],
 'passage + bracketed attribution': txt[a:c],
 'passage + attribution + See line': txt[a:d],
 'two date lines + Oberlin passage + all': txt[e0:d],
 'Oberlin passage + its attribution': txt[oberlin_a:a],
}
def counts(t):
    ws = t.split()
    return {
      'ws': len(ws),
      'ws_no_dash': len([x for x in ws if re.search(r'\w', x)]),
      'split_hyphen': len([x for x in re.split(r'[\s\-]+', t) if re.search(r'\w', x)]),
      'alnum_runs': len(re.findall(r'[A-Za-z0-9]+', t)),
      'alpha_runs': len(re.findall(r"[A-Za-z]+", t)),
    }
for k, t in segs.items():
    print('%-46s %s' % (k, counts(t)))
