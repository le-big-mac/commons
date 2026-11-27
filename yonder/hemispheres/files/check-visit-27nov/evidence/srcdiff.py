"""Every difference between old and new source, by line, then inside changed lines by word.
usage: python srcdiff.py OLD NEW"""
import sys, difflib, re
a = open(sys.argv[1], encoding='utf-8').read().split('\n')
b = open(sys.argv[2], encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    n += 1
    print(f'--- change {n}: {tag}; old lines {i1 + 1}-{i2}, new lines {j1 + 1}-{j2}')
    if tag == 'replace' and i2 - i1 == j2 - j1:
        for x, y in zip(a[i1:i2], b[j1:j2]):
            wa, wb = re.findall(r'\S+|\s+', x), re.findall(r'\S+|\s+', y)
            s2 = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
            for t, k1, k2, l1, l2 in s2.get_opcodes():
                if t != 'equal':
                    print(f'    {t}: OLD [{"".join(wa[k1:k2])[:300]}{"..." if len("".join(wa[k1:k2])) > 300 else ""}]')
                    print(f'    {" " * len(t)}  NEW [{"".join(wb[l1:l2])[:300]}{"..." if len("".join(wb[l1:l2])) > 300 else ""}]')
    else:
        for x in a[i1:i2]:
            print('    OLD: ' + x[:160] + ('...' if len(x) > 160 else ''))
        for y in b[j1:j2]:
            print('    NEW: ' + y[:160] + ('...' if len(y) > 160 else ''))
print(n, 'changed places; old', len(a), 'lines, new', len(b), 'lines')
