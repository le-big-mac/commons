import sys, difflib
a = open(sys.argv[1], encoding='utf-8').read().split('\n')
b = open(sys.argv[2], encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal': continue
    for la, lb in zip(a[i1:i2], b[j1:j2]):
        wa, wb = la.split(' '), lb.split(' ')
        s2 = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
        for t, x1, x2, y1, y2 in s2.get_opcodes():
            if t == 'equal': continue
            print(f"--- line {i1+1} [{t}]")
            print("  OLD:", ' '.join(wa[max(0,x1-8):x1]), '⟦' + ' '.join(wa[x1:x2]) + '⟧', ' '.join(wa[x2:x2+8]))
            print("  NEW:", ' '.join(wb[max(0,y1-8):y1]), '⟦' + ' '.join(wb[y1:y2]) + '⟧', ' '.join(wb[y2:y2+8]))
    if (i2 - i1) != (j2 - j1): print("line count differs at", i1+1, i2-i1, j2-j1)
