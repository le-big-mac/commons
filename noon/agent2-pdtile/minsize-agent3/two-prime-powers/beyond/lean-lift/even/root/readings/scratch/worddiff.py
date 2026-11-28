# Word-level differences between the section as first read and the present draft, paragraph by paragraph.
import difflib, re, sys
A = open('/home/agent3/lean/lift-check/even/root/readings/section-18-as-first-read.md', encoding='utf-8').read()
B = open('/home/agent3/pq2/rule-drafts/root-section.draft.md', encoding='utf-8').read()
pa = A.split('\n'); pb = B.split('\n')
print('lines:', len(pa), len(pb))
n = 0
for i, (x, y) in enumerate(zip(pa, pb), 1):
    if x == y: continue
    wa = x.split(' '); wb = y.split(' ')
    sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': continue
        n += 1
        ctx = ' '.join(wa[max(0, i1 - 6):i1])
        print(f'[{n}] line {i} ({tag})  …{ctx} >>>')
        print('     OLD:', ' '.join(wa[i1:i2]))
        print('     NEW:', ' '.join(wb[j1:j2]))
print('hunks:', n)
