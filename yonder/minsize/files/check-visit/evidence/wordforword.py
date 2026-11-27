"""Word-for-word check of the candidate page against the page as posted.
usage: wordforword.py OLD NEW
1. Every section of NEW from '## The rule, in formulas' to the end: is its body (whitespace-normalised) a contiguous piece of OLD?
2. What of OLD is nowhere in NEW (by sentence, whitespace-normalised)?
3. What of NEW's open part is not in OLD (by sentence)?
"""
import sys, re, difflib
old = open(sys.argv[1], encoding='utf-8').read()
new = open(sys.argv[2], encoding='utf-8').read()
norm = lambda t: ' '.join(t.split())
OLD = norm(old); NEW = norm(new)

cut = new.index('## The rule, in formulas')
open_part, folded = new[:cut], new[cut:]

print('=== 1. folded sections of NEW, each as one contiguous piece of OLD ===')
secs = re.split(r'(?m)^(## .*)$', folded)
# secs = ['', head1, body1, head2, body2, ...]
allok = True
for k in range(1, len(secs), 2):
    head, body = secs[k].strip(), secs[k + 1]
    nb = norm(body)
    whole = nb in OLD
    head_in_old = (head + '\n') in old
    print(f'{head!r}: body {len(body.split())} words; body contiguous in OLD: {whole}; heading itself in OLD: {head_in_old}')
    if not whole:
        allok = False
        # paragraph by paragraph
        for para in re.split(r'\n\s*\n', body.strip()):
            if norm(para) not in OLD:
                print('   PARAGRAPH NOT IN OLD:', norm(para)[:200])
print('all folded bodies contiguous in OLD:', allok)

# order check: are folded bodies in NEW in the same relative order as in OLD?
print('\n=== 1b. position in OLD of each folded body (character offset in normalised OLD) ===')
for k in range(1, len(secs), 2):
    head, body = secs[k].strip(), norm(secs[k + 1])
    print(f'{head!r}: at {OLD.find(body)} .. {OLD.find(body) + len(body)} of {len(OLD)}')

# exact (not whitespace-normalised) check as well
print('\n=== 1c. exact byte check of folded bodies (no whitespace normalisation, bodies stripped) ===')
for k in range(1, len(secs), 2):
    head, body = secs[k].strip(), secs[k + 1].strip()
    print(f'{head!r}: exact in OLD: {body in old}')

def sentences(t):
    t = norm(t)
    # split on sentence end followed by space and capital/quote/star/paren/bracket/dash; crude but symmetric for both texts
    parts = re.split(r'(?<=[.:;?!)\*])\s+', t)
    return [p for p in parts if p]

print('\n=== 2. pieces of OLD that are nowhere in NEW ===')
miss = []
for sent in sentences(old):
    if sent not in NEW:
        miss.append(sent)
for m in miss: print(' -', m)
print(f'({len(miss)} pieces; {sum(len(m.split()) for m in miss)} words)')

print('\n=== 3. pieces of the open part of NEW that are not in OLD ===')
missn = []
for sent in sentences(open_part):
    if sent not in OLD:
        missn.append(sent)
for m in missn: print(' +', m)
print(f'({len(missn)} pieces; {sum(len(m.split()) for m in missn)} words; open part {len(open_part.split())} words)')

print('\n=== 3b. pieces of the open part of NEW that ARE in OLD word for word ===')
for sent in sentences(open_part):
    if sent in OLD: print(' =', sent)

print('\n=== 4. word-level diff of OLD "How it was found" against NEW "How it was found" ===')
def sec(t, a, b):
    i = t.index(a); j = t.index(b, i + len(a)); return t[i:j]
of = sec(old, '## How it was found\n', '## What stands behind it\n').split()
nf = sec(new, '## How it was found\n', '## What came after\n').split()
sm = difflib.SequenceMatcher(None, of, nf, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print(f' {tag}: OLD[{" ".join(of[i1:i2])}] -> NEW[{" ".join(nf[j1:j2])}]')

print('\n=== 5. word counts ===')
af = sec(new, '## What came after, in full\n', '## What this does not say\n')
print('words in "What came after, in full" including heading:', len(af.split()))
print('words in its body without heading:', len(af.split()) - 6)
print('open part words:', len(open_part.split()), ' whole new page:', len(new.split()), ' old page:', len(old.split()))

print('\n=== 6. the old page, with every stretch found in NEW removed: what is left (word-level, longest-match) ===')
ow, nw = old.split(), new.split()
sm = difflib.SequenceMatcher(None, ow, nw, autojunk=False)
# difflib is order-sensitive; do instead a greedy cover: mark old words covered by any 8-gram present in new
N = 6
newgrams = set(tuple(nw[i:i + N]) for i in range(len(nw) - N + 1))
cov = [False] * len(ow)
for i in range(len(ow) - N + 1):
    if tuple(ow[i:i + N]) in newgrams:
        for k in range(i, i + N): cov[k] = True
run = []
for i, w in enumerate(ow):
    if not cov[i]: run.append(w)
    else:
        if run: print(' ~', ' '.join(run)); run = []
if run: print(' ~', ' '.join(run))
