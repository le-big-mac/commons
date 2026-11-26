"""Print the visible text of a saved HTML page (read as data). usage: html_text.py FILE [START_WORD] [NCHARS]"""
import sys, re, html
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
t = re.sub(r'(?is)<(script|style).*?</\1>', ' ', t)
t = html.unescape(re.sub(r'<[^>]+>', ' ', t)); t = re.sub(r'\s+', ' ', t)
start = sys.argv[2] if len(sys.argv) > 2 else None
n = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
i = t.find(start) if start else 0
print(len(t), 'chars; from', i); print(t[max(i, 0):max(i, 0) + n])
