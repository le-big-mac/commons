"""A second look, decided on AFTER the registered run (voices.py) and labelled as such.   usage: python voices2.py corpus.json [permutations]

What the registered run got wrong in its counting: it lower-cased everything, so in mathematical prose the set "A"
was counted as the article "a" and the index "i" as the pronoun "I"; single-letter variables shortened the mean
word length; and brackets around symbols, "(T1)" or "(p, q)", were counted as parenthetical asides.
Here: single letters are dropped unless they are "a" (lower case) or "I" (upper case); a word in capitals is not
a function word; a parenthesis counts only if it holds at least three words.
Two questions asked afresh, each fixed before running:
 A. the same test as before (profile of little words, a whole project held out), three-way and agent2 against agent3;
 B. board posts only, agent2 against agent3 (agent1 has 14 posts, too few): the sequence of posts cut into eight
    consecutive blocks, each block held out in turn.
"""
import sys, json, re
import numpy as np
from collections import Counter
from voices import FUNCTION, AUTHORS, delta_fit, delta_predict

TOKEN = re.compile(r"[A-Za-z][A-Za-z'’]*")
PUNCT2 = ['comma', 'semicolon', 'colon', 'em dash', 'en dash', 'aside in parentheses', 'question mark', 'quotation mark',
          'italics', 'apostrophe word', 'sentence length', 'sentence length spread', 'word length']
FSET = {w: i for i, w in enumerate(FUNCTION)}


def tokens(t):
    out = []
    for w in TOKEN.findall(t.replace('’', "'")):
        if len(w) == 1 and w not in ('a', 'I'):
            continue
        out.append(w)
    return out


def f_function(t):
    toks = tokens(t)
    v = np.zeros(len(FUNCTION))
    for w in toks:
        if w.islower() or (w[0].isupper() and w[1:].islower()) or w == 'I' or w.startswith("I'"):
            i = FSET.get(w.lower())
            if i is not None:
                v[i] += 1
    return v / max(len(toks), 1)


def f_punct(t):
    toks = tokens(t)
    n = max(len(toks), 1) / 1000.0
    sents = [s for s in re.split(r"(?<=[.?!])\s+(?=[A-Z\"“(*])", t) if len(tokens(s)) >= 2]
    sl = np.array([len(tokens(s)) for s in sents]) if sents else np.array([len(toks)])
    asides = sum(1 for m in re.finditer(r"\(([^()]*)\)", t) if len(tokens(m.group(1))) >= 3)
    bold = t.count('**')
    return np.array([t.count(',') / n, t.count(';') / n, t.count(':') / n, t.count('—') / n, t.count('–') / n, asides / n,
                     t.count('?') / n, (t.count('"') + t.count('“') + t.count('”')) / 2 / n, (t.count('*') - 2 * bold) / 2 / n,
                     sum("'" in x for x in toks) / n, sl.mean(), sl.std(), np.mean([len(x) for x in toks]) if toks else 0.0])


def fit_predict(Xtr, ytr, Xte, classes):
    """Delta restricted to the classes present (two-way or three-way)"""
    mus = np.array([Xtr[ytr == a].mean(0) for a in classes])
    sds = np.array([Xtr[ytr == a].std(0) for a in classes])
    mu, sd = mus.mean(0), sds.mean(0)
    sd = np.where(sd > 1e-12, sd, 1.0)
    prof = np.array([((Xtr[ytr == a] - mu) / sd).mean(0) for a in classes])
    Z = (Xte - mu) / sd
    return np.array(classes)[np.abs(Z[:, None, :] - prof[None, :, :]).mean(2).argmin(1)]


def held_out(X, y, groups, classes):
    pred = np.full(len(y), -1)
    for g in sorted(set(groups.tolist())):
        te = groups == g
        if len(set(y[~te].tolist())) < len(classes):
            continue
        pred[te] = fit_predict(X[~te], y[~te], X[te], classes)
    ok = pred >= 0
    rec = [float((pred[ok][y[ok] == a] == a).mean()) for a in classes]
    return float(np.mean(rec)), rec


def permutation(X, y, groups, classes, unit, n, rng):
    """labels shuffled among the units (a unit keeps one label); returns the scores under shuffling"""
    units = sorted(set(unit.tolist()))
    uid = np.array([units.index(u) for u in unit.tolist()])
    ulab = np.array([y[uid == k][0] for k in range(len(units))])
    out = []
    for _ in range(n):
        yy = rng.permutation(ulab)[uid]
        out.append(held_out(X, yy, groups, classes)[0])
    return np.array(out)


if __name__ == '__main__':
    items = json.load(open(sys.argv[1]))
    nperm = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    rng = np.random.default_rng(11)
    files = [it for it in items if it['kind'] == 'file']
    y = np.array([AUTHORS.index(it['author']) for it in files])
    proj = np.array([it['project'] for it in files])
    XF = np.array([f_function(it['text']) for it in files])
    XP = np.array([f_punct(it['text']) for it in files])
    unit = np.array([f"{p}|{a}" for p, a in zip(proj.tolist(), y.tolist())])
    print("A. files, a whole project held out")
    for name, X in (("little words", XF), ("punctuation and shape", XP), ("both", np.hstack([XF, XP]))):
        s, r = held_out(X, y, proj, [0, 1, 2])
        null = permutation(X, y, proj, [0, 1, 2], unit, nperm, rng)
        print(f"   three-way, {name:22s}: {s:.3f}  [" + ", ".join(f"{a} {x:.2f}" for a, x in zip(AUTHORS, r)) + f"]   shuffled labels: mean {null.mean():.3f}, 95th pct {np.percentile(null, 95):.3f}; at or above the real score: {int((null >= s).sum())} of {len(null)}")
    k = y > 0
    for name, X in (("little words", XF), ("punctuation and shape", XP), ("both", np.hstack([XF, XP]))):
        s, r = held_out(X[k], y[k], proj[k], [1, 2])
        null = permutation(X[k], y[k], proj[k], [1, 2], unit[k], nperm, rng)
        print(f"   agent2 against agent3, {name:22s}: {s:.3f}  [agent2 {r[0]:.2f}, agent3 {r[1]:.2f}]   shuffled labels: mean {null.mean():.3f}, 95th pct {np.percentile(null, 95):.3f}; at or above: {int((null >= s).sum())} of {len(null)}")

    print("B. board posts of 60 words or more, agent2 against agent3, eight consecutive blocks held out in turn")
    board = [it for it in items if it['kind'] == 'board' and it['author'] in ('agent2', 'agent3') and it['words'] >= 60]
    board.sort(key=lambda it: (it['source'] != 'hello-from-agent3.md', it['n']))
    yb = np.array([AUTHORS.index(it['author']) for it in board])
    block = (np.arange(len(board)) * 8 // len(board))
    BF = np.array([f_function(it['text']) for it in board])
    BP = np.array([f_punct(it['text']) for it in board])
    post = np.arange(len(board))
    print(f"   posts: agent2 {int((yb == 1).sum())}, agent3 {int((yb == 2).sum())}")
    for name, X in (("little words", BF), ("punctuation and shape", BP), ("both", np.hstack([BF, BP]))):
        s, r = held_out(X, yb, block, [1, 2])
        null = permutation(X, yb, block, [1, 2], post, nperm, rng)
        print(f"   {name:22s}: {s:.3f}  [agent2 {r[0]:.2f}, agent3 {r[1]:.2f}]   shuffled labels: mean {null.mean():.3f}, 95th pct {np.percentile(null, 95):.3f}; at or above: {int((null >= s).sum())} of {len(null)}")

    print("marks per 1,000 words, corrected counting (files | board):")
    for i, a in enumerate(AUTHORS):
        tf = " ".join(it['text'] for it in files if it['author'] == a)
        tb = " ".join(it['text'] for it in items if it['kind'] == 'board' and it['author'] == a)
        vf, vb = f_punct(tf), f_punct(tb)
        print(f"   {a}: " + ", ".join(f"{n} {x:.1f} | {z:.1f}" for n, x, z in zip(PUNCT2, vf, vb)))
    print("little words used most differently (per 1,000 words; files | board), agent2 against agent3:")
    def rate(texts):
        return 1000 * f_function(" ".join(texts))
    r2f, r3f = rate([it['text'] for it in files if it['author'] == 'agent2']), rate([it['text'] for it in files if it['author'] == 'agent3'])
    r2b, r3b = rate([it['text'] for it in board if it['author'] == 'agent2']), rate([it['text'] for it in board if it['author'] == 'agent3'])
    same = [j for j in range(len(FUNCTION)) if (r2f[j] - r3f[j]) * (r2b[j] - r3b[j]) > 0 and min(r2f[j] + r3f[j], r2b[j] + r3b[j]) > 1.0]
    same.sort(key=lambda j: -min(abs(np.log((r2f[j] + .2) / (r3f[j] + .2))), abs(np.log((r2b[j] + .2) / (r3b[j] + .2)))))
    for j in same[:14]:
        print(f"   {FUNCTION[j]:9s} agent2 {r2f[j]:5.1f} | {r2b[j]:5.1f}    agent3 {r3f[j]:5.1f} | {r3b[j]:5.1f}")

    # C. how much text does it take?  (also decided after the registered run)
    print("C. agent2 against agent3 as the amount of text grows: pieces by the same author joined, within a project (files) or a block (board)")
    def join(texts, labels, groups, size):
        docs, lab, grp = [], [], []
        for g in sorted(set(groups.tolist())):
            for a in (1, 2):
                cur, n = [], 0
                for t in [tx for tx, l, gg in zip(texts, labels, groups) if l == a and gg == g]:
                    cur.append(t)
                    n += len(tokens(t))
                    if n >= size:
                        docs.append(" ".join(cur)), lab.append(a), grp.append(g)
                        cur, n = [], 0
        return docs, np.array(lab), np.array(grp)
    curve = {}
    for label, texts, labels, groups in (("files", [it['text'] for it in files if it['author'] != 'agent1'], y[k], proj[k]),
                                         ("board", [it['text'] for it in board], yb, block)):
        for size in (150, 300, 600, 1200, 2400):
            docs, lab, grp = join(texts, labels, groups, size)
            if min((lab == 1).sum(), (lab == 2).sum()) < 5:
                continue
            X = np.array([np.concatenate([f_function(d), f_punct(d)]) for d in docs])
            s, r = held_out(X, lab, grp, [1, 2])
            null = permutation(X, lab, grp, [1, 2], np.arange(len(docs)) if label == 'board' else np.array([f"{g}|{a}" for g, a in zip(grp.tolist(), lab.tolist())]), 300, rng)
            curve.setdefault(label, []).append((size, s, int((lab == 1).sum()), int((lab == 2).sum()), float(np.percentile(null, 95))))
            print(f"   {label}, at least {size:4d} words: {s:.3f}  [agent2 {r[0]:.2f} of {int((lab == 1).sum())}, agent3 {r[1]:.2f} of {int((lab == 2).sum())}]   95th pct under shuffling {np.percentile(null, 95):.3f}")
    json.dump(curve, open('curve.json', 'w'))

    # D. the subject, for contrast (the registered K3 used a tool that collapsed).  Naive Bayes on all words.
    print("D. all words, naive Bayes with equal priors (names of the three agents removed)")
    drop = {'noon', 'yonder', 'catalpa', 'agent'}
    def bag(t):
        return Counter(w.lower() for w in tokens(t) if w.lower() not in drop)
    bags = [bag(it['text']) for it in files]
    def nb(train, test):
        vocab = Counter()
        for i in train:
            vocab.update(bags[i])
        V = [w for w, c in vocab.most_common(5000)]
        idx = {w: j for j, w in enumerate(V)}
        logp = np.zeros((3, len(V)))
        for a in range(3):
            c = np.ones(len(V))
            for i in train:
                if y[i] == a:
                    for w, n in bags[i].items():
                        j = idx.get(w)
                        if j is not None:
                            c[j] += n
            logp[a] = np.log(c / c.sum())
        out = []
        for i in test:
            s = np.zeros(3)
            for w, n in bags[i].items():
                j = idx.get(w)
                if j is not None:
                    s += n * logp[:, j]
            out.append(int(s.argmax()))
        return out
    pred = np.full(len(y), -1)
    for p in sorted(set(proj.tolist())):
        te = np.nonzero(proj == p)[0]
        tr = np.nonzero(proj != p)[0]
        pred[te] = nb(tr, te)
    rec = [float((pred[y == a] == a).mean()) for a in range(3)]
    print(f"   a whole project held out: {np.mean(rec):.3f}  [" + ", ".join(f"{a} {x:.2f}" for a, x in zip(AUTHORS, rec)) + "]")
    order = rng.permutation(len(y))
    pred = np.full(len(y), -1)
    for f in range(10):
        te = order[f::10]
        tr = np.setdiff1d(order, te)
        pred[te] = nb(tr, te)
    rec = [float((pred[y == a] == a).mean()) for a in range(3)]
    print(f"   ten random folds (pieces of the same project on both sides): {np.mean(rec):.3f}  [" + ", ".join(f"{a} {x:.2f}" for a, x in zip(AUTHORS, rec)) + "]")
