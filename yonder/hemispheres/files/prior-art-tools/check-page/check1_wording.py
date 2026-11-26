"""Check 1: are the page's new sentences word for word the report's?

Reads the report (prior-art.md) and the page; takes the report's own texts from
between backticks (items 9, 11, 12, 13) and from the quoted note "For the public page";
reports whether each occurs in the page, how many times, and the first difference if not.
"""
import re, sys, html, difflib

REPORT = "/srv/commons/hemispheres-agent3/prior-art.md"
PAGE = "/home/agent3/site/build/pages/hemispheres.html"
BEFORE = "/home/agent3/site/build/pages/hemispheres-before-26nov-prior.html"

rep = open(REPORT, encoding="utf-8").read()
page = open(PAGE, encoding="utf-8").read()
before = open(BEFORE, encoding="utf-8").read()

def item(n):
    m = re.search(r'^%d\. (.*?)(?=^\d+\. |\n\n)' % n, rep, re.S | re.M)
    return m.group(1)

def old_new(n):
    t = item(n)
    old = re.search(r'Old: `(.*?)`', t, re.S)
    new = re.search(r'New: `(.*?)`', t, re.S)
    return (old.group(1) if old else None, new.group(1) if new else None)

def show(label, s, text, name):
    c = text.count(s)
    print("%-40s in %-7s: %d time(s)" % (label, name, c))
    if c == 0:
        # find closest region
        sm = difflib.SequenceMatcher(None, text, s, autojunk=False)
        m = sm.find_longest_match(0, len(text), 0, len(s))
        start = max(0, m.a - m.b)
        cand = text[start:start + len(s) + 40]
        for i, (x, y) in enumerate(zip(cand, s)):
            if x != y:
                print("   first difference at char %d of the report's text:" % i)
                print("   report: ..." + s[max(0, i - 40):i + 60])
                print("   page  : ..." + cand[max(0, i - 40):i + 60])
                break

for n in (11, 12, 13):
    old, new = old_new(n)
    print("--- item", n)
    print("   new text:", new)
    show("item %d NEW" % n, new, page, "AFTER")
    show("item %d OLD" % n, old, page, "AFTER")
    show("item %d OLD" % n, old, before, "BEFORE")

old9, new9 = old_new(9)
second = new9[len(old9):].strip()
print("--- item 9, what follows the old sentence in the new text:")
print("   ", second)
show("item 9 second sentence", second, page, "AFTER")

m = re.search(r'\*\*For the public page\.\*\*\s*\n\s*\n> (.*?)\n', rep, re.S)
note = m.group(1).strip()
print("--- note for the public page:")
print("   ", note)
show("public-page note", note, page, "AFTER")
# also against the html-unescaped page
show("public-page note (page unescaped)", note, html.unescape(page), "AFTER")
