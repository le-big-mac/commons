"""Word-level changes between two texts, line by line.   usage: python3 -I wdiff.py OLD NEW
Lines are matched by difflib first; inside each replaced line the changed words are printed with a few words of context."""
import sys, difflib
a = open(sys.argv[1], encoding='utf-8').read().split('\n')
b = open(sys.argv[2], encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    print('=== %s old lines %d-%d, new lines %d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))
    if tag == 'replace' and i2 - i1 == j2 - j1:
        for k in range(i2 - i1):
            x = a[i1 + k].split(' '); y = b[j1 + k].split(' ')
            s2 = difflib.SequenceMatcher(None, x, y, autojunk=False)
            for t, p1, p2, q1, q2 in s2.get_opcodes():
                if t == 'equal':
                    continue
                print('  [line %d, %s]' % (j1 + k + 1, t))
                print('    before: ...%s' % ' '.join(x[max(0, p1 - 8):p1]))
                print('    OLD: %s' % ' '.join(x[p1:p2]))
                print('    NEW: %s' % ' '.join(y[q1:q2]))
                print('    after: %s...' % ' '.join(x[p2:p2 + 8]))
    else:
        for l in a[i1:i2]:
            print('  - ' + l)
        for l in b[j1:j2]:
            print('  + ' + l)
