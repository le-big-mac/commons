import re, sys
t = open(sys.argv[1], encoding='utf-8').read()
i = t.index('<details class="fold">')
def words(s):
    s = re.sub(r'alt="[^"]*"', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return len(s.split())
print('story words (no alt):', words(t[:i]), ' fold words:', words(t[i:]))
for m in re.finditer(r'<h2>(.*?)</h2>', t[:i]):
    print('  section:', m.group(1))
