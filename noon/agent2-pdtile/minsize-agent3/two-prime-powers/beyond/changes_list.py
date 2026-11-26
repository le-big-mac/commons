"""Every line of the note that differs between two versions, with the words that differ.   usage: changes_list.py OLD NEW "TITLE" OUT.md"""
import sys, difflib
old = open(sys.argv[1]).read().split('\n'); new = open(sys.argv[2]).read().split('\n')
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
out = [f"# {sys.argv[3]}\n", "*Made by `changes_list.py`: every line of the note that differs between the two versions. Inside a changed line, the words that differ are listed.*\n"]
n = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal': continue
    n += 1
    ow, nw = '\n'.join(old[i1:i2]).split(' '), '\n'.join(new[j1:j2]).split(' ')
    parts = []
    for t2, a1, a2, b1, b2 in difflib.SequenceMatcher(None, ow, nw, autojunk=False).get_opcodes():
        if t2 != 'equal': parts.append(f"  - was: «{' '.join(ow[a1:a2])}»\n    now: «{' '.join(nw[b1:b2])}»")
    where = f"line {j1 + 1}" if j2 - j1 <= 1 else f"lines {j1 + 1} to {j2}"
    out.append(f"## Change {n} ({where} of the note)\n\n" + '\n'.join(parts) + '\n')
open(sys.argv[4], 'w').write('\n'.join(out)); print(n, 'changed blocks ->', sys.argv[4])
