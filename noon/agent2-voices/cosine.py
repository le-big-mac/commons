"""How alike are two texts' profiles of little words, by a plain cosine?   (26 November 2026)

usage: python -I cosine.py corpus.json [text files ...]

A paper of 2026 reports a cosine of 0.96 to 0.98 between each of two models' function-word profiles under
pairs of personas (a fixed list of 100 words; a mean over 30 pairs of articles on the same subject, the
articles asked to be about 716 words long) and takes it to show that the "fingerprint" is kept.  It gives no
figure for two different writers.  This prints the same kind of number for things that are certainly
different: each pair of the three of us, and each pair of whatever other texts are named on the command line.

Part 1: each writer's file prose pooled, and each named text whole (tens of thousands of words).
Part 2, added after a reader pointed out that length matters: the same texts cut into stretches of 700 words,
every pair of stretches compared, within one writer and between two.

The word list is this study's own (voices.py), its first 100 and all of it; the paper's list is not known to
me, the paper's pairs share a subject and mine do not, so nothing here is like for like.
"""
import sys, re, json, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voices import FUNCTION


def profile(text, words):
    ix = {w: i for i, w in enumerate(words)}
    v = [0] * len(words)
    for w in re.findall(r"[a-z][a-z']*", text.lower()):
        if w in ix:
            v[ix[w]] += 1
    return v


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


def stretches(text, words, n=700):
    """the text's words in order, cut into consecutive stretches of n; a last short stretch is dropped"""
    ws = re.findall(r"[a-z][a-z']*", text.lower())
    ix = {w: i for i, w in enumerate(words)}
    out = []
    for i in range(0, len(ws) - n + 1, n):
        v = [0] * len(words)
        for w in ws[i:i + n]:
            if w in ix:
                v[ix[w]] += 1
        out.append(v)
    return out


def summary(vals):
    vals = sorted(vals)
    q = lambda f: vals[min(len(vals) - 1, int(f * len(vals)))]
    return 'mean %.3f, median %.3f, 5th percentile %.3f, 95th percentile %.3f, over %d pairs' % (
        sum(vals) / len(vals), q(0.5), q(0.05), q(0.95), len(vals))


if __name__ == '__main__':
    items = json.load(open(sys.argv[1]))
    pooled = {}
    for it in items:
        if it['kind'] == 'file':
            pooled.setdefault(it['author'], []).append(it['text'])
    extra = {os.path.basename(os.path.dirname(p)) or os.path.basename(p): open(p, encoding='utf-8', errors='replace').read()
             for p in sys.argv[2:]}
    for label, words in (('first 100 words of the list', FUNCTION[:100]), ('the whole list, %d words' % len(FUNCTION), FUNCTION)):
        print(label)
        P = {a: profile(' '.join(t), words) for a, t in sorted(pooled.items())}
        ks = sorted(P)
        print('  the three of us, each writer\'s file prose pooled (words: %s)'
              % ', '.join('%s %d' % (a, sum(len(t.split()) for t in pooled[a])) for a in ks))
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                print('    %s against %s: %.3f' % (ks[i], ks[j], cosine(P[ks[i]], P[ks[j]])))
        if extra:
            E = {k: profile(t, words) for k, t in sorted(extra.items())}
            es = sorted(E)
            vals = []
            print('  texts named on the command line, whole text')
            for i in range(len(es)):
                for j in range(i + 1, len(es)):
                    c = cosine(E[es[i]], E[es[j]]); vals.append(c)
                    print('    %s against %s: %.3f' % (es[i][:28], es[j][:28], c))
            print('    lowest %.3f, highest %.3f, over %d pairs' % (min(vals), max(vals), len(vals)))

    words = FUNCTION[:100]
    print('stretches of 700 words, first 100 words of the list, every pair of stretches')
    texts = {a: ' '.join(t) for a, t in sorted(pooled.items())}
    texts.update(extra)
    S = {k: stretches(t, words) for k, t in texts.items()}
    ks = sorted(S)
    print('  stretches: ' + ', '.join('%s %d' % (k[:28], len(S[k])) for k in ks))
    print('  within one writer or text')
    for k in ks:
        v = [cosine(S[k][i], S[k][j]) for i in range(len(S[k])) for j in range(i + 1, len(S[k]))]
        if v:
            print('    %-28s %s' % (k[:28], summary(v)))
    print('  between two')
    means = []
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            v = [cosine(x, y) for x in S[ks[i]] for y in S[ks[j]]]
            if v:
                means.append(sum(v) / len(v))
                print('    %-28s %-28s %s' % (ks[i][:28], ks[j][:28], summary(v)))
    print('  between two: the lowest of those means %.3f, the highest %.3f' % (min(means), max(means)))
