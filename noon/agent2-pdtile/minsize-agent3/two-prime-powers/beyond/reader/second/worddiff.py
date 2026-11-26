"""Reader's own word-by-word comparison of the note as read with the revised note.   usage: worddiff.py OLD NEW"""
import sys, difflib
old = open(sys.argv[1]).read().split('\n'); new = open(sys.argv[2]).read().split('\n')
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
nblocks = 0; same = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal': same += i2 - i1; continue
    nblocks += 1
    print(f'=== block {nblocks}: {tag}; old lines {i1 + 1}-{i2}, new lines {j1 + 1}-{j2}')
    ow = ' \n '.join(old[i1:i2]).split(' '); nw = ' \n '.join(new[j1:j2]).split(' ')
    wm = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
    for t, a1, a2, b1, b2 in wm.get_opcodes():
        if t == 'equal': continue
        print(f'   - {" ".join(ow[a1:a2])!r}\n   + {" ".join(nw[b1:b2])!r}')
print(f'{nblocks} changed blocks; {same} lines the same; old {len(old)} lines, new {len(new)} lines')
