"""Referee's own replayer for Noon's strategy files (reads the files only; own answer function).
usage: replay.py file d Q K|W [file d Q mode ...]"""
import sys, itertools
from collections import Counter
codes = [''.join(p) for p in itertools.product('123456', repeat=4)]
def ans(g, c):
    b = sum(x == y for x, y in zip(g, c))
    cg, cc = Counter(g), Counter(c)
    return f"{b}{sum(min(cg[q], cc[q]) for q in '123456') - b}"
args = sys.argv[1:]
for i in range(0, len(args), 4):
    f, d, Q, mode = args[i], int(args[i+1]), int(args[i+2]), args[i+3]
    book = {}; bad_hist = 0; dup = 0; tmax = 0
    for line in open(f):
        if not line.startswith('S '): continue
        _, t, rest = line.split(); t = int(t); hist, g = rest.split(':')
        h = () if hist == '-' else tuple(hist.split(','))
        if len(h) != max(0, t - 1 - d): bad_hist += 1          # a guess that uses more (or fewer) answers than the lag allows
        if (t, h) in book and book[(t, h)] != g: dup += 1
        book[(t, h)] = g; tmax = max(tmax, t)
        assert len(g) == 4 and set(g) <= set('123456')
    sigs = {}; unsent = []; clash = []; longest = 0; nlines_used = set()
    for c in codes:
        sent = []; told = False
        for t in range(1, Q + 1):
            h = tuple(ans(g, c) for g in sent[:max(0, t - 1 - d)])   # only answers 1..t-1-d
            if mode == 'W' and '40' in h: told = True; break
            if (t, h) not in book: break
            nlines_used.add((t, h)); sent.append(book[(t, h)])
        longest = max(longest, len(sent))
        if mode == 'W':
            if c not in sent: unsent.append(c)
        else:
            sig = (tuple(sent), tuple(ans(g, c) for g in sent))
            if sig in sigs: clash.append((c, sigs[sig]))
            sigs[sig] = c
    res = (f"unsent {len(unsent)} {unsent[:4]}" if mode == 'W' else f"codes not told apart {len(clash)} {clash[:3]}")
    print(f"{f.split('/')[-1]:14s} lag {d} Q {Q} {mode}: lines {len(book)}, used {len(nlines_used)}, lines with wrong number of answers {bad_hist}, conflicting lines {dup}, deepest line t={tmax}, most guesses sent {longest}; {res}")
