# Referee's blind computation. Counts typed by the referee from mendel.txt (lines 381-512, 613-698, 896-962).
import numpy as np
from scipy import stats
from itertools import product

F2 = [(5474, 1850), (6022, 2001), (705, 224), (882, 299), (428, 152), (651, 207), (787, 277)]
PLANTS = [(45, 12), (27, 8), (24, 7), (19, 10), (32, 11), (26, 6), (88, 24), (22, 10), (28, 6), (25, 7),
          (25, 11), (32, 7), (14, 5), (70, 27), (24, 13), (20, 6), (32, 13), (44, 9), (50, 14), (44, 18)]
F3 = [(372, 193), (353, 166), (64, 36), (71, 29), (60, 40), (67, 33), (72, 28), (65, 35)]
BI = {'AB': 38, 'Ab': 35, 'aB': 28, 'ab': 30, 'ABb': 65, 'aBb': 68, 'AaB': 60, 'Aab': 67, 'AaBb': 138}
TRI = {'ABC': 8, 'ABc': 14, 'AbC': 9, 'Abc': 11, 'aBC': 8, 'aBc': 10, 'abC': 10, 'abc': 7,
       'ABCc': 22, 'AbCc': 17, 'aBCc': 25, 'abCc': 20, 'ABbC': 15, 'ABbc': 18, 'aBbC': 19, 'aBbc': 24,
       'AaBC': 14, 'AaBc': 18, 'AabC': 20, 'Aabc': 16,
       'ABbCc': 45, 'aBbCc': 36, 'AaBCc': 38, 'AabCc': 40, 'AaBbC': 49, 'AaBbc': 48, 'AaBbCc': 78}
BACK = {'bc1': {'AB': 20, 'ABb': 23, 'AaB': 25, 'AaBb': 22},
        'bc3': {'AB': 25, 'ABb': 19, 'AaB': 22, 'AaBb': 21},
        'bc2': {'AaBb': 31, 'Aab': 26, 'aBb': 27, 'ab': 26},
        'bc4': {'AaBb': 24, 'Aab': 25, 'aBb': 22, 'ab': 27},
        'flower-stem': {'AaBb': 47, 'aBb': 40, 'Aab': 38, 'ab': 41}}


def parse(label):
    """label -> tuple of states per character: D (constant dominant), H (hybrid), R (constant recessive)."""
    out, i = [], 0
    while i < len(label):
        ch = label[i]
        if ch.isupper() and i + 1 < len(label) and label[i + 1] == ch.lower():
            out.append('H'); i += 2
        else:
            out.append('D' if ch.isupper() else 'R'); i += 1
    return tuple(out)


def chi_multi(d):
    n = sum(d.values())
    w = {k: 2 ** parse(k).count('H') for k in d}
    W = sum(w.values())
    return sum((d[k] - n * w[k] / W) ** 2 / (n * w[k] / W) for k in d)


def chi_equal(d):
    n = sum(d.values()); e = n / len(d)
    return sum((v - e) ** 2 / e for v in d.values())


def zbin(a, b, p):
    n = a + b
    return (a - n * p) / np.sqrt(n * p * (1 - p))


def split(d, order=None, contrast='hyb'):
    """Split a multi-class table into 1:1 tests. Returns list of (name, a, b)."""
    st = {parse(k): v for k, v in d.items()}
    k = len(next(iter(st)))
    order = list(range(k)) if order is None else order
    names = 'ABC'
    tests = []
    for depth, ch in enumerate(order):
        earlier = order[:depth]
        combos = sorted({tuple(s[e] for e in earlier) for s in st})
        for combo in combos:
            cnt = {}
            for s, v in st.items():
                if tuple(s[e] for e in earlier) == combo:
                    cnt[s[ch]] = cnt.get(s[ch], 0) + v
            ctx = ','.join(f'{names[e]}={c}' for e, c in zip(earlier, combo)) or 'all'
            if len(cnt) == 3:
                tests.append((f'{names[ch]}: H vs D+R | {ctx}', cnt['H'], cnt['D'] + cnt['R']))
                tests.append((f'{names[ch]}: D vs R | {ctx}', cnt['D'], cnt['R']))
            else:
                (s1, v1), (s2, v2) = sorted(cnt.items())
                tests.append((f'{names[ch]}: {s1} vs {s2} | {ctx}', v1, v2))
    return tests


def models(z, tag):
    z = np.abs(np.asarray(z)); n = len(z)
    s2 = np.mean(z ** 2); c = z.max()
    honest = np.sum(stats.norm.logpdf(z))
    shrunk = np.sum(stats.norm.logpdf(z, scale=np.sqrt(s2))) - honest
    cut = -n * np.log(2 * stats.norm.cdf(c) - 1)
    p = 2 * stats.norm.sf(z)
    # better of two: density 2p (p<=a), 1+a (p>a). Likelihood is piecewise increasing in a, jumps at each p.
    best, besta = 0.0, 0.0
    cands = list(np.linspace(0, 1, 2001)) + [x - 1e-12 for x in p] + list(p)
    for a in cands:
        ll = np.sum(np.where(p <= a, np.log(2 * p), np.log1p(a)))
        if ll > best:
            best, besta = ll, a
    print(f'[{tag}] n={n} mean z^2={s2:.4f} spread={np.sqrt(s2):.4f} c={c:.4f}')
    print(f'[{tag}] logL minus honest: shrunk {shrunk:.3f}  cut-off {cut:.3f}  better-of-two {best:.3f} (a={besta:.4f})')
    print(f'[{tag}] likelihood ratio cut-off/shrunk = {np.exp(cut - shrunk):.2f}; cut-off/better-of-two = {np.exp(cut - best):.2f}; shrunk/better-of-two = {np.exp(shrunk - best):.2f}')
    return shrunk, cut, best


def tests84(order3=None, order2=None):
    t = []
    t += [(f'F2 expt {i+1}', zbin(a, b, .75)) for i, (a, b) in enumerate(F2)]
    t += [(f'F3 test {i+1}', zbin(a, b, 2 / 3)) for i, (a, b) in enumerate(F3)]
    t += [(f'plant {i+1}', zbin(a, b, .75)) for i, (a, b) in enumerate(PLANTS)]
    multi = [('bifactorial', BI, order2)] + [('trifactorial', TRI, order3)] + [(k, v, order2) for k, v in BACK.items()]
    for nm, d, o in multi:
        t += [(f'{nm} {name} ({a} v {b})', (a - b) / np.sqrt(a + b)) for name, a, b in split(d, o)]
    return t


if __name__ == '__main__':
    print('== 1. chi-squared by group ==')
    g = [('seven F2 (3:1)', sum(zbin(a, b, .75) ** 2 for a, b in F2), 7),
         ('twenty single plants (3:1)', sum(zbin(a, b, .75) ** 2 for a, b in PLANTS), 20),
         ('eight F3 (2:1)', sum(zbin(a, b, 2 / 3) ** 2 for a, b in F3), 8),
         ('two characters (9 kinds)', chi_multi(BI), 8),
         ('three characters (27 kinds)', chi_multi(TRI), 26),
         ('five back-crosses', sum(chi_equal(d) for d in BACK.values()), 15)]
    for nm, x, df in g:
        print(f'{nm:30s} chi2={x:8.4f} df={df}')
    tot = sum(x for _, x, _ in g); df = sum(d for _, _, d in g)
    print(f'total chi2={tot:.4f} df={df}  P(chi2<=total)={stats.chi2.cdf(tot, df):.3e}  P(larger)={stats.chi2.sf(tot, df):.6f}')
    print('totals: bifactorial', sum(BI.values()), ' trifactorial', sum(TRI.values()), len(TRI), ' backcrosses', [sum(d.values()) for d in BACK.values()])

    print('== 2. six tests of 100 ==')
    h = sum(a for a, b in F3[2:]); n = 600
    p2 = (2 / 3) * (1 - .75 ** 10)
    print(f'hybrids {h} of {n}; vs 2/3: {(h - n*2/3)/np.sqrt(n*2/9):.3f} sd; vs {p2:.5f}: {(h - n*p2)/np.sqrt(n*p2*(1-p2)):.3f} sd')

    print('== 3. the 35 ==')
    t = tests84()
    z35 = np.array([z for _, z in t[:35]])
    i = np.argmax(np.abs(z35))
    print(f'largest z^2 = {z35[i]**2:.4f} ({t[i][0]}, z={z35[i]:.3f}); |z|<0.3: {np.sum(np.abs(z35) < .3)}; mean z^2 = {np.mean(z35**2):.4f}; sum = {np.sum(z35**2):.4f}')
    print('sorted |z|:', np.round(np.sort(np.abs(z35)), 3))
    print('== 4. models on the 35 ==')
    models(z35, '35')

    print('== 5. the 84 ==')
    z84 = np.array([z for _, z in t])
    i = np.argmax(np.abs(z84))
    print(f'n={len(z84)} sum z^2 = {np.sum(z84**2):.4f}; largest |z| = {abs(z84[i]):.4f}: {t[i][0]}; |z|<0.3: {np.sum(np.abs(z84) < .3)}')
    print(f'expected |z|<0.3 under N(0,1): {84*(2*stats.norm.cdf(.3)-1):.2f}; under fitted shrunk: {84*(2*stats.norm.cdf(.3/np.sqrt(np.mean(z84**2)))-1):.2f}')
    print('five largest:', sorted([(round(abs(z), 3), nm) for nm, z in t])[-5:])
    print('== 6. models on the 84 ==')
    models(z84, '84')
