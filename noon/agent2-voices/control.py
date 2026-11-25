"""The control: the same method on three human writers on one subject.   usage: python -I control.py BOOKDIR [permutations [pieces per book [out.json]]]
Darwin, Wallace, Huxley; four books each from Project Gutenberg; 300-word pieces cut exactly as our files were;
at most 150 pieces a book; a whole book held out in turn; the corrected counting of voices2.py."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from prose import clean, pieces
from voices2 import f_function, f_punct, held_out, permutation, tokens

BOOKS = {'Darwin': [1228, 3704, 2300, 5765], 'Wallace': [14558, 32021, 73563, 53177], 'Huxley': [6919, 7150, 15905, 2940]}
NAMES = list(BOOKS)
d = sys.argv[1]
nperm = int(sys.argv[2]) if len(sys.argv) > 2 else 500
PER = int(sys.argv[3]) if len(sys.argv) > 3 else 150
OUTJ = sys.argv[4] if len(sys.argv) > 4 else 'control.json'
rng = np.random.default_rng(3)
texts, y, book = [], [], []
for a, ids in BOOKS.items():
    for i in ids:
        raw = open(f"{d}/{i}.txt", 'rb').read()
        try:
            t = raw.decode('utf-8')
        except UnicodeDecodeError:
            t = raw.decode('latin-1')
        t = t.replace('\r\n', '\n').replace('﻿', '')
        s = re.search(r"\*\*\* ?START OF.*?\*\*\*", t, flags=re.S)
        e = re.search(r"\*\*\* ?END OF", t)
        t = t[s.end() if s else 0: e.start() if e else len(t)]
        t = t.replace('--', '—')
        ps = pieces(clean(t))
        ps = ps[len(ps) // 20:]                                         # skip the front matter
        pick = sorted(rng.choice(len(ps), min(PER, len(ps)), replace=False).tolist())
        for k in pick:
            texts.append(ps[k]), y.append(NAMES.index(a)), book.append(i)
        print(f"   {a:8s} {i:6d}: {len(ps)} pieces, {len(pick)} used")
y, book = np.array(y), np.array(book)
XF = np.array([f_function(t) for t in texts])
XP = np.array([f_punct(t) for t in texts])
print("three-way, a whole book held out (chance 0.33):")
out = {}
for name, X in (("little words", XF), ("punctuation and shape", XP), ("both", np.hstack([XF, XP]))):
    s, r = held_out(X, y, book, [0, 1, 2])
    null = permutation(X, y, book, [0, 1, 2], book, nperm, rng)
    out[name] = s
    print(f"   {name:22s}: {s:.3f}  [" + ", ".join(f"{a} {x:.2f}" for a, x in zip(NAMES, r)) + f"]   shuffled labels: mean {null.mean():.3f}, 95th pct {np.percentile(null, 95):.3f}; at or above: {int((null >= s).sum())} of {len(null)}")
print("pairs, both kinds of feature (chance 0.5):")
XB = np.hstack([XF, XP])
pairs = {}
for a in range(3):
    for b in range(a + 1, 3):
        k = (y == a) | (y == b)
        s, r = held_out(XB[k], y[k], book[k], [a, b])
        s2, _ = held_out(XF[k], y[k], book[k], [a, b])
        pairs[f"{NAMES[a]}-{NAMES[b]}"] = (s, s2)
        print(f"   {NAMES[a]} against {NAMES[b]}: {s:.3f}  [{r[0]:.2f}, {r[1]:.2f}];  little words alone {s2:.3f}")
print("as the amount of text grows (three-way, both kinds of feature):")
curve = []
for size in (150, 300, 600, 1200, 2400):
    docs, lab, grp = [], [], []
    for i in sorted(set(book.tolist())):
        cur, n = [], 0
        for t in [tx for tx, b in zip(texts, book) if b == i]:
            for part in ([t] if size >= 300 else [" ".join(t.split()[:len(t.split()) // 2]), " ".join(t.split()[len(t.split()) // 2:])]):
                cur.append(part)
                n += len(tokens(part))
                if n >= size:
                    docs.append(" ".join(cur)), lab.append(int(y[book == i][0])), grp.append(i)
                    cur, n = [], 0
    lab, grp = np.array(lab), np.array(grp)
    X = np.array([np.concatenate([f_function(t), f_punct(t)]) for t in docs])
    s, r = held_out(X, lab, grp, [0, 1, 2])
    curve.append((size, s, len(docs)))
    print(f"   at least {size:4d} words: {s:.3f}  [" + ", ".join(f"{a} {x:.2f}" for a, x in zip(NAMES, r)) + f"]  ({len(docs)} pieces)")
json.dump({'scores': out, 'curve': curve, 'pairs': pairs}, open(OUTJ, 'w'))
