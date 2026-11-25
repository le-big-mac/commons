import re, sys
def unwrap(text):
    blocks = text.rstrip('\n').split('\n\n'); res = []
    for b in blocks:
        ls = b.split('\n')
        if ls[0].startswith(('#', '|', '!')): res.append(b); continue
        if re.match(r'(- |\d+\. )', ls[0]):
            items = []
            for l in ls:
                if re.match(r'(- |\d+\. )', l): items.append(l)
                else: items[-1] += ' ' + l.strip()
            res.extend(items); continue
        res.append(' '.join(l.strip() for l in ls))
    return res
for src, out in [(sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])]:
    open(out,'w').write('\n'.join(unwrap(open(src).read()))+'\n')
