import sys, difflib
a = open(sys.argv[1], encoding='utf-8').read().split('\n')
b = open(sys.argv[2], encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    print('LINES', tag, 'old', i1 + 1, i2, 'new', j1 + 1, j2)
    if tag == 'replace' and i2 - i1 == j2 - j1:
        for x, y in zip(a[i1:i2], b[j1:j2]):
            s = difflib.SequenceMatcher(None, x, y, autojunk=False)
            for t, p1, p2, q1, q2 in s.get_opcodes():
                if t != 'equal':
                    print('   ', t, 'at char', p1)
                    print('    OLD:', repr(x[max(0, p1 - 150):p2 + 150]))
                    print('    NEW:', repr(y[max(0, q1 - 150):q2 + 150]))
    else:
        for y in b[j1:j2]:
            print('    +', y[:1500])
        for x in a[i1:i2]:
            print('    -', x[:1500])
