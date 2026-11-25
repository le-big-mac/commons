"""Print the context of a phrase in a text file (read only). usage: ctx.py FILE PHRASE [WIDTH]"""
import sys, re
f, phrase = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 300
t = open(f, encoding='utf-8', errors='replace').read()
t = re.sub(r'\s+', ' ', t)
n = 0
for m in re.finditer(re.escape(phrase), t, flags=re.I):
    n += 1
    print(f'[{n}] ...' + t[max(0, m.start() - w): m.end() + w] + '...\n')
    if n >= 6: break
print('matches shown:', n)
