"""Third pass: word-for-word check of the third candidate against the page as it was.
usage: wordforword3.py OLD CANDIDATE2 CANDIDATE3
1. every section of CANDIDATE3 from '## The rule, in formulas' to the end of '## For those who want to check': is its body one
   contiguous piece of OLD, byte for byte?  And the last section ('How this page was rebuilt'): is it the paragraph in the file given?
2. the paragraphs of the open part that are said to be the old page's: 'Why anyone asks', 'For mathematicians', the five cautions,
   the paragraph on fresh instances (with two changes of words), the sentence 'Each reading of my own account ...'.
3. what of OLD is nowhere in CANDIDATE3.
4. the open part of CANDIDATE3 piece by piece: in OLD word for word, in CANDIDATE2, or new.
5. word counts.
"""
import sys, re, difflib
old, c2, c3 = (open(p, encoding='utf-8').read() for p in sys.argv[1:4])
norm = lambda t: ' '.join(t.split())
OLD, C2 = norm(old), norm(c2)
CUT = '## The rule, in formulas'
open3, fold3 = c3[:c3.index(CUT)], c3[c3.index(CUT):]

print('=== 1. sections of the third candidate from "The rule, in formulas" on ===')
secs = re.split(r'(?m)^(## .*)$', fold3)
for k in range(1, len(secs), 2):
    head, body = secs[k].strip(), secs[k + 1].strip()
    print(f'{head!r}: {len(body.split())} words; body in the old page byte for byte: {body in old}; heading in the old page as a heading: {(head + chr(10)) in old}')
order = [secs[k].strip() for k in range(1, len(secs), 2)]
print('order:', order)
rb = secs[order.index('## How this page was rebuilt') * 2 + 2].strip()
print('the last section equals restructure-read-3.txt:', rb == open('/home/agent3/door/restructure-read-3.txt', encoding='utf-8').read().strip())
c2fold = c2[c2.index(CUT):]
for name in ('## The rule, in formulas', '## What stands behind it', '## What the reviews caught', '## What came after, in full', '## What this does not say', '## For those who want to check'):
    def body_of(t):
        i = t.index(name + '\n'); j = t.find('\n## ', i + 1); return t[i:j if j > 0 else len(t)].strip()
    print(f'   {name!r} the same in the second and third candidates: {body_of(c2fold) == body_of(fold3)}')

print('\n=== 2. paragraphs of the open part that are said to be the old page\'s ===')
paras = [p for p in re.split(r'\n\s*\n', open3) if p.strip()]
def find(start): return [p for p in paras if p.strip().startswith(start)]
for start in ('*Why anyone asks.*', '*For mathematicians.*', 'Five cautions, set out in full'):
    ps = find(start); print(f'   {start!r}: paragraphs {len(ps)}; in the old page byte for byte: {[p.strip() in old for p in ps]}')
i = old.index('*Why anyone asks.*'); j = old.index('## The answer, for clocks')
both = old[i:j].strip(); print('   "Why anyone asks" with "For mathematicians", as one stretch of the old page, stands in the third candidate:', both in c3, '; and where the old page had it (just before the heading of "The answer"):', (both + '\n\n## The answer') in c3)
fresh_new = find('The proofs came from *fresh instances*')[0].strip()
fresh_old = old[old.index('The proofs came from *fresh instances*'):old.index('## What stands behind it')].strip()
sm = difflib.SequenceMatcher(None, fresh_old.split(), fresh_new.split(), autojunk=False)
print('   the paragraph on fresh instances, old against new:')
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal': print(f'        {tag}: OLD[{" ".join(fresh_old.split()[i1:i2])}] -> NEW[{" ".join(fresh_new.split()[j1:j2])}]')
s = 'ach reading of my own account found it claiming more than the records show ("What the reviews caught").'
print('   "Each reading of my own account ...": in the old page (with a small e)', ('e' + s) in OLD, '; in the open part (with a capital)', ('E' + s) in norm(open3))

print('\n=== 3. what of the old page is nowhere in the third candidate ===')
ow, nw = old.split(), c3.split(); N = 6
grams = set(tuple(nw[i:i + N]) for i in range(len(nw) - N + 1))
cov = [False] * len(ow)
for i in range(len(ow) - N + 1):
    if tuple(ow[i:i + N]) in grams:
        for k in range(i, i + N): cov[k] = True
run = []; nlost = 0
for i, w in enumerate(ow):
    if not cov[i]: run.append(w); nlost += 1
    else:
        if run: print('  ~', ' '.join(run)); run = []
if run: print('  ~', ' '.join(run))
print(f'   ({nlost} words of {len(ow)})')
hf_old = old[old.index('## How it was found\n') + len('## How it was found\n'):old.index('## What stands behind it')].split()
hf_new = c3[c3.index('## How it was found\n'):c3.index('## What came after\n')].split()
g2 = set(tuple(hf_new[i:i + 4]) for i in range(len(hf_new) - 3)); cv = [False] * len(hf_old)
for i in range(len(hf_old) - 3):
    if tuple(hf_old[i:i + 4]) in g2:
        for k in range(i, i + 4): cv[k] = True
print(f'   of the old "How it was found" ({len(hf_old)} words), words still standing in the new one in stretches of four or more: {sum(cv)}')

def sentences(t): return [p for p in re.split(r'(?<=[.:;?!)\*])\s+', norm(t)) if p]
print('\n=== 4. the open part of the third candidate, piece by piece ===')
n = {'OLD ': 0, 'C2  ': 0, 'NEW ': 0}
for sent in sentences(open3):
    tag = 'OLD ' if sent in OLD else ('C2  ' if sent in C2 else 'NEW ')
    n[tag] += len(sent.split()); print(f'  {tag} {sent}')
print('   words: in the old page word for word', n['OLD '], '; not there but in the second candidate', n['C2  '], '; new since the second candidate', n['NEW '])

print('\n=== 5. word counts ===')
i = c3.index('## What came after, in full'); j = c3.index('## What this does not say')
print('full account (with its heading):', len(c3[i:j].split()), ' open part:', len(open3.split()), ' whole:', len(c3.split()), ' old page:', len(old.split()))
for h in ('## In short', '## The question', '## The answer', '## How it was found', '## What came after\n'):
    a = c3.index(h); b = c3.find('\n## ', a + 1); print(f'   {h.strip()}: {len(c3[a:b].split())} words')
