import re, sys, html
t = open(sys.argv[1], encoding='utf-8', errors='replace').read()
t = re.sub(r'(?is)<(script|style).*?</\1>', ' ', t)
t = re.sub(r'(?s)<[^>]+>', ' ', t)
t = html.unescape(t)
t = re.sub(r'\s+', ' ', t)
for m in re.finditer(r'(?i)(rankin|switzerland|92\.9|hemisphere)', t):
    s = max(0, m.start()-200); e = min(len(t), m.end()+300)
    print('...', t[s:e], '...')
    print('-----')
