"""Second pass: word-for-word check of the second candidate against the page as it was.
usage: wordforword2.py OLD CANDIDATE1 CANDIDATE2
1. every folded section of CANDIDATE2 (from '## The rule, in formulas' to the end): is its body one contiguous piece of OLD, byte for byte?
   For any that is not, what differs.
2. the folded part of CANDIDATE2 against the folded part of CANDIDATE1 (which was checked in the first pass).
3. what of OLD is nowhere in CANDIDATE2 (runs of words not covered by any six-word stretch of the candidate).
4. which sentences of the open part of CANDIDATE2 are in OLD word for word, which were in CANDIDATE1, and which are new.
5. word counts.
"""
import sys, re, difflib
old = open(sys.argv[1], encoding='utf-8').read()
c1 = open(sys.argv[2], encoding='utf-8').read()
c2 = open(sys.argv[3], encoding='utf-8').read()
norm = lambda t: ' '.join(t.split())
OLD, C1 = norm(old), norm(c1)
CUT = '## The rule, in formulas'
open2, fold2 = c2[:c2.index(CUT)], c2[c2.index(CUT):]
open1, fold1 = c1[:c1.index(CUT)], c1[c1.index(CUT):]

print('=== 1. folded sections of the second candidate against the old page ===')
secs = re.split(r'(?m)^(## .*)$', fold2)
for k in range(1, len(secs), 2):
    head, body = secs[k].strip(), secs[k + 1].strip()
    exact = body in old
    print(f'{head!r}: {len(body.split())} words; body in the old page byte for byte: {exact}; heading in the old page as a heading: {(head + chr(10)) in old}')
    if not exact:
        # find the nearest old stretch: try with a prefix restored
        for prefix in ('*Why anyone asks.* ',):
            if (prefix + body) in old:
                print(f'     with {prefix!r} put back at its head it is in the old page byte for byte')
        if norm(body) in OLD: print('     (it is in the old page when white space is squeezed)')

print('\n=== 2. folded part: second candidate against first candidate (line diff) ===')
d = list(difflib.unified_diff(fold1.split('\n'), fold2.split('\n'), lineterm='', n=0))
for l in d:
    if l.startswith(('+', '-')) and not l.startswith(('+++', '---')): print('  ', l[:260])
print(f'   ({sum(1 for l in d if l.startswith(("+", "-")) and not l.startswith(("+++", "---")))} changed lines)')

print('\n=== 3. what of the old page is nowhere in the second candidate ===')
ow, nw = old.split(), c2.split()
N = 6
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

def sentences(t):
    return [p for p in re.split(r'(?<=[.:;?!)\*])\s+', norm(t)) if p]
print('\n=== 4. the open part of the second candidate, piece by piece ===')
C2open = norm(open2)
n_old = n_c1 = n_new = 0
for sent in sentences(open2):
    if sent in OLD: tag = 'OLD '; n_old += len(sent.split())
    elif sent in C1: tag = 'C1  '; n_c1 += len(sent.split())
    else: tag = 'NEW '; n_new += len(sent.split())
    print(f'  {tag} {sent}')
print(f'   words: in the old page word for word {n_old}; not there but in the first candidate {n_c1}; new since the first candidate {n_new}')

print('\n=== 5. word counts ===')
i = c2.index('## What came after, in full'); j = c2.index('## What this does not say')
print('full account (with its heading):', len(c2[i:j].split()), ' open part:', len(open2.split()), ' open part without the paragraph on checking:', len(open2[:open2.index('*How this page was checked.*')].split()), ' whole:', len(c2.split()), ' old page:', len(old.split()))
