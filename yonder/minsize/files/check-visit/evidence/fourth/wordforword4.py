"""Fourth pass: word-for-word check of the fourth candidate against the page as it was.
usage: wordforword4.py OLD CANDIDATE3 CANDIDATE4
1. the sections from '## The rule, in formulas' to '## For those who want to check': each body one contiguous piece of OLD, byte for
   byte?  ('The rule, in formulas' is said to be the old formulas with the old paragraph 'For mathematicians' at its end.)
2. the pieces of the open part said to be kept from the old page: the five cautions with the sentence on my own account in the
   middle; 'Why anyone asks' but for one word; the first paragraph of 'How it was found'; the paragraph on fresh instances but
   for two phrases.
3. what of OLD is nowhere in CANDIDATE4.
4. the open part of CANDIDATE4 piece by piece: in OLD word for word, in CANDIDATE3, or new.
5. the whole of CANDIDATE4 against CANDIDATE3, changed lines outside the open part.
"""
import sys, re, difflib
old, c3, c4 = (open(p, encoding='utf-8').read() for p in sys.argv[1:4])
norm = lambda t: ' '.join(t.split())
OLD, C3 = norm(old), norm(c3)
CUT = '## The rule, in formulas'
open4, fold4 = c4[:c4.index(CUT)], c4[c4.index(CUT):]
def diffwords(a, b):
    a, b = a.split(), b.split(); out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != 'equal': out.append(f'{tag}: OLD[{" ".join(a[i1:i2])}] -> NEW[{" ".join(b[j1:j2])}]')
    return out

print('=== 1. sections from "The rule, in formulas" on ===')
secs = re.split(r'(?m)^(## .*)$', fold4)
for k in range(1, len(secs), 2):
    head, body = secs[k].strip(), secs[k + 1].strip()
    print(f'{head!r}: {len(body.split())} words; body in the old page byte for byte: {body in old}')
rule = secs[2].strip()
i = old.index('Let M = pⁿ·q with p and q different primes'); j = old.index('Five cautions, set out in full under'); formulas = old[i:j].strip()
k = old.index('*For mathematicians.*'); formath = old[k:old.index('## The answer, for clocks')].strip()
print('   "The rule, in formulas" = the old formulas, a blank line, the old paragraph "For mathematicians":', rule == formulas + '\n\n' + formath)
print('   order:', [secs[k].strip() for k in range(1, len(secs), 2)])
print('   the last section equals restructure-read-4.txt:', secs[-1].strip() == open('/home/agent3/door/restructure-read-4.txt', encoding='utf-8').read().strip())

print('\n=== 2. pieces of the open part kept from the old page ===')
paras = [p.strip() for p in re.split(r'\n\s*\n', open4) if p.strip()]
caut = [p for p in paras if p.startswith('Five cautions, set out in full')][0]
oc = old[old.index('Five cautions, set out in full under'):old.index('## How it was found')].strip()
print('   five cautions, old against new:'); [print('       ', l) for l in diffwords(oc, caut)]
s = 'each reading of my own account found it claiming more than the records show ("What the reviews caught").'
print('   the inserted sentence, from "each" on, stands in the old page:', s in OLD, '; in the old page it is under:', [h for h in re.findall(r'(?m)^## (.*)$', old[:old.index('each reading of my own')])][-1])
i = c4.index('## Why anyone asks\n'); j = c4.index('## How it was found\n'); why_new = c4[i + len('## Why anyone asks\n'):j].strip()
why_old = old[old.index('*Why anyone asks.*'):old.index('*For mathematicians.*')].strip()
print('   "Why anyone asks", old against new:'); [print('       ', l) for l in diffwords(why_old, why_new)]
hf = c4[c4.index('## How it was found\n') + len('## How it was found\n'):c4.index('## What came after\n')].strip()
hp = [p.strip() for p in re.split(r'\n\s*\n', hf)]
ohf = old[old.index('## How it was found\n') + len('## How it was found\n'):old.index('## What stands behind it')].strip()
print('   first paragraph of "How it was found" is the start of the old one, byte for byte:', ohf.startswith(hp[0]), f'({len(hp[0].split())} words)')
fresh_old = ohf[ohf.index('The proofs came from *fresh instances*'):]
print('   the paragraph on fresh instances, old against new:'); [print('       ', l) for l in diffwords(fresh_old, hp[-1])]

print('\n=== 3. what of the old page is nowhere in the fourth candidate ===')
ow, nw = old.split(), c4.split(); N = 6
grams = set(tuple(nw[i:i + N]) for i in range(len(nw) - N + 1)); cov = [False] * len(ow)
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

def sentences(t): return [p for p in re.split(r'(?<=[.:;?!)\*])\s+', norm(t)) if p]
print('\n=== 4. the open part of the fourth candidate, piece by piece ===')
n = {'OLD ': 0, 'C3  ': 0, 'NEW ': 0}
for sent in sentences(open4):
    tag = 'OLD ' if sent in OLD else ('C3  ' if sent in C3 else 'NEW ')
    n[tag] += len(sent.split()); print(f'  {tag} {sent}')
print('   words: in the old page word for word', n['OLD '], '; not there but in the third candidate', n['C3  '], '; new since the third candidate', n['NEW '])
print('   open sections in order:', re.findall(r'(?m)^## (.*)$', open4), '; open part', len(open4.split()), 'words; whole', len(c4.split()))

print('\n=== 5. from "The rule, in formulas" on: fourth candidate against third (changed lines) ===')
f3 = c3[c3.index(CUT):]
for l in difflib.unified_diff(f3.split('\n'), fold4.split('\n'), lineterm='', n=0):
    if l.startswith(('+', '-')) and not l.startswith(('+++', '---')): print('  ', l[:330])
