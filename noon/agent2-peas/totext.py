"""Turns the downloaded page into plain text, one paragraph a line.   usage: python -I totext.py PAGE.html OUT.txt"""
import sys, re, html
t = open(sys.argv[1], encoding='latin-1').read()
t = re.sub(r"(?is)<(script|style).*?</\1>", " ", t)
t = re.sub(r"(?i)<(p|br|h\d|li|tr|pre|hr|dd|dt|blockquote)[^>]*>", "\n", t)
t = re.sub(r"<[^>]+>", "", t); t = html.unescape(t)
lines = [" ".join(l.split()) for l in t.split("\n")]; lines = [l for l in lines if l]
open(sys.argv[2], 'w', encoding='utf-8').write("\n".join(lines) + "\n"); print(len(lines), "lines;", sum(len(l) for l in lines), "characters")
