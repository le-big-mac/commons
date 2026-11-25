"""Can the three agents' prose be told apart?   usage: python voices.py corpus.json [permutations]

Burrows' Delta: each feature is standardised (mean and spread taken per author and then averaged, so the author
with most text does not set the scale); an author's profile is the mean of their training pieces; a test piece
goes to the profile at the smallest mean absolute distance.  Testing is always on a whole project left out of
training.  Score: recall averaged over the three authors (chance 1/3)."""
import sys, json, re
import numpy as np
from collections import Counter, defaultdict

AUTHORS = ['agent1', 'agent2', 'agent3']
WORD = re.compile(r"[a-z][a-z']*")
FUNCTION = """the of and to a in that is it for as with was on be by this which or at from an are not but have has had its
one two all so if then than there their they i my me we our us you your he she his her no only also both each every any
some more most less least very much many such same other another these those here where when what who how why because
since while before after until between into over under about against through without within again still yet just even
now already never always often would could should may might must can will shall do does did done being been were am
itself themselves myself either neither nor though although however whether per up down out off own too enough rather
quite almost nearly exactly once twice first last next nothing something everything none few several whose whom upon
across along among around behind below beside beyond during except inside near outside past toward towards unless via
them him it's that's don't doesn't didn't isn't wasn't can't cannot i've i'm i'd i'll we've there's""".split()
assert len(FUNCTION) == len(set(FUNCTION)), [w for w, c in Counter(FUNCTION).items() if c > 1]
PUNCT = ['comma', 'semicolon', 'colon', 'em dash', 'en dash', 'parenthesis', 'question mark', 'exclamation mark', 'quotation mark',
         'italics', 'bold', 'contraction', 'sentence length', 'sentence length spread', 'word length']


def words(t):
    return WORD.findall(t.lower().replace('’', "'"))


def f_function(t):
    w = words(t)
    c = Counter(w)
    return np.array([c[x] for x in FUNCTION]) / max(len(w), 1)


def f_punct(t):
    w = words(t)
    n = max(len(w), 1) / 1000.0
    sents = [s for s in re.split(r"(?<=[.?!])\s+(?=[A-Z\"“(*])", t) if len(words(s)) >= 2]
    sl = np.array([len(words(s)) for s in sents]) if sents else np.array([len(w)])
    bold = t.count('**')
    return np.array([t.count(',') / n, t.count(';') / n, t.count(':') / n, t.count('—') / n, t.count('–') / n, t.count('(') / n,
                     t.count('?') / n, t.count('!') / n, (t.count('"') + t.count('“') + t.count('”')) / 2 / n,
                     (t.count('*') - 2 * bold) / 2 / n, bold / 2 / n, sum("'" in x for x in w) / n,
                     sl.mean(), sl.std(), np.mean([len(x) for x in w]) if w else 0.0])


class AllWords:
    """the most frequent words of the training pieces, whatever they are (so: topic, names, everything)"""
    def __init__(self, k=2000):
        self.k = k

    def fit(self, texts):
        c = Counter()
        for t in texts:
            c.update(words(t))
        self.vocab = {w: i for i, (w, _) in enumerate(c.most_common(self.k))}

    def __call__(self, t):
        v = np.zeros(len(self.vocab))
        w = words(t)
        for x in w:
            i = self.vocab.get(x)
            if i is not None:
                v[i] += 1
        return v / max(len(w), 1)


def delta_fit(X, y):
    mus = np.array([X[y == a].mean(0) for a in range(3)])
    sds = np.array([X[y == a].std(0) for a in range(3)])
    mu, sd = mus.mean(0), sds.mean(0)
    sd = np.where(sd > 1e-12, sd, 1.0)
    prof = np.array([((X[y == a] - mu) / sd).mean(0) for a in range(3)])
    return mu, sd, prof


def delta_predict(model, X):
    mu, sd, prof = model
    Z = (X - mu) / sd
    return np.abs(Z[:, None, :] - prof[None, :, :]).mean(2).argmin(1)


def macro_recall(y, pred):
    rec = [(pred[y == a] == a).mean() if (y == a).any() else np.nan for a in range(3)]
    return float(np.nanmean(rec)), rec


def leave_project_out(X, y, proj):
    pred = np.full(len(y), -1)
    for p in sorted(set(proj)):
        te = proj == p
        tr = ~te
        if len(set(y[tr])) < 3:
            continue
        pred[te] = delta_predict(delta_fit(X[tr], y[tr]), X[te])
    ok = pred >= 0
    return macro_recall(y[ok], pred[ok]) + (pred,)


if __name__ == '__main__':
    items = json.load(open(sys.argv[1]))
    nperm = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    files = [it for it in items if it['kind'] == 'file']
    board = [it for it in items if it['kind'] == 'board']
    y = np.array([AUTHORS.index(it['author']) for it in files])
    proj = np.array([it['project'] for it in files])
    texts = [it['text'] for it in files]
    print("pieces of file prose:", {a: int((y == i).sum()) for i, a in enumerate(AUTHORS)}, "; projects:", len(set(proj)))
    bw = Counter()
    for it in board:
        bw[it['author']] += it['words']
    tot = sum(bw.values())
    print("K1  words on the two boards in signed posts:", {a: bw[a] for a in AUTHORS}, "; shares:", {a: round(bw[a] / tot, 3) for a in AUTHORS})
    print("    median length of a post (words):", {a: int(np.median([it['words'] for it in board if it['author'] == a])) for a in AUTHORS},
          "; posts:", {a: sum(it['author'] == a for it in board) for a in AUTHORS})

    XF = np.array([f_function(t) for t in texts])
    XP = np.array([f_punct(t) for t in texts])
    sF, rF, pF = leave_project_out(XF, y, proj)
    sP, rP, pP = leave_project_out(XP, y, proj)
    sFP, rFP, pFP = leave_project_out(np.hstack([XF, XP]), y, proj)
    # all words: the vocabulary must come from the training pieces only
    predW = np.full(len(y), -1)
    for p in sorted(set(proj)):
        te = proj == p
        aw = AllWords()
        aw.fit([t for t, k in zip(texts, te) if not k])
        Xa = np.array([aw(t) for t in texts])
        predW[te] = delta_predict(delta_fit(Xa[~te], y[~te]), Xa[te])
    sW, rW = macro_recall(y, predW)
    fmt = lambda r: "[" + ", ".join(f"{a} {x:.2f}" for a, x in zip(AUTHORS, r)) + "]"
    print(f"K2  function words alone:        {sF:.3f}  {fmt(rF)}")
    print(f"K3  all words:                   {sW:.3f}  {fmt(rW)}")
    print(f"K4  punctuation and shape alone: {sP:.3f}  {fmt(rP)}")
    print(f"    function words + punctuation: {sFP:.3f}  {fmt(rFP)}")
    conf = np.zeros((3, 3), int)
    for a, b in zip(y, pF):
        conf[a, b] += 1
    print("    confusion, function words (rows: who wrote it; columns: who it was given to):", conf.tolist())
    conf = np.zeros((3, 3), int)
    for a, b in zip(y, pFP):
        conf[a, b] += 1
    print("    confusion, function words + punctuation:", conf.tolist())

    # K5: trained on files, tested on board posts
    yb = np.array([AUTHORS.index(it['author']) for it in board if it['words'] >= 100])
    tb = [it['text'] for it in board if it['words'] >= 100]
    for name, f, X in (("function words", f_function, XF), ("punctuation and shape", f_punct, XP)):
        pb = delta_predict(delta_fit(X, y), np.array([f(t) for t in tb]))
        s, r = macro_recall(yb, pb)
        print(f"K5  trained on files, tested on {len(tb)} board posts of 100 words or more ({name}): {s:.3f}  {fmt(r)}")
    XB = np.hstack([XF, XP])
    pb = delta_predict(delta_fit(XB, y), np.array([np.concatenate([f_function(t), f_punct(t)]) for t in tb]))
    s, r = macro_recall(yb, pb)
    print(f"    the same with both kinds of feature: {s:.3f}  {fmt(r)}   posts per author: {[int((yb == a).sum()) for a in range(3)]}")

    # K6: the marks
    print("K6  marks per 1,000 words in the files (all of an author's pieces pooled):")
    for i, a in enumerate(AUTHORS):
        t = " ".join(tx for tx, k in zip(texts, y == i) if k)
        v = f_punct(t)
        print(f"    {a}: " + ", ".join(f"{n} {x:.1f}" for n, x in zip(PUNCT, v)))

    # K7: permutation test.  Author labels are shuffled among (project, author) groups, so each group stays whole.
    rng = np.random.default_rng(7)
    groups = sorted(set(zip(proj.tolist(), y.tolist())))
    gid = np.array([groups.index((p, a)) for p, a in zip(proj.tolist(), y.tolist())])
    glab = np.array([a for _, a in groups])
    null = {'F': [], 'P': []}
    for _ in range(nperm):
        yy = rng.permutation(glab)[gid]
        if len(set(yy.tolist())) < 3:
            continue
        null['F'].append(leave_project_out(XF, yy, proj)[0])
        null['P'].append(leave_project_out(XP, yy, proj)[0])
    for k, s in (('F', sF), ('P', sP)):
        v = np.array(null[k])
        print(f"K7  {'function words' if k == 'F' else 'punctuation and shape'}: {len(v)} shuffles of the labels; mean {v.mean():.3f}, 99th percentile {np.percentile(v, 99):.3f},"
              f" largest {v.max():.3f}; shuffles at or above the real score {s:.3f}: {int((v >= s).sum())}")

    # what tells them apart: the features on which each author's profile stands furthest from the average of the other two
    mu, sd, prof = delta_fit(np.hstack([XF, XP]), y)
    names = FUNCTION + PUNCT
    print("the strongest tells (standard deviations above or below the other two):")
    for i, a in enumerate(AUTHORS):
        d = prof[i] - np.delete(prof, i, 0).mean(0)
        top = np.argsort(-np.abs(d))[:12]
        print(f"    {a}: " + ", ".join(f"{names[j]} {d[j]:+.2f}" for j in top))
    json.dump({'pred_function': pF.tolist(), 'pred_both': pFP.tolist(), 'pred_all': predW.tolist(), 'y': y.tolist(),
               'null_F': null['F'], 'null_P': null['P'], 'scores': {'F': sF, 'P': sP, 'FP': sFP, 'W': sW}}, open('results.json', 'w'))
