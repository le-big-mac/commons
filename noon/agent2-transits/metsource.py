"""metsource.py -- added on 26 November 2026. Where does each star's listed metal content come from, and does the
difference between hot Jupiters' stars and small planets' stars survive inside one source?
    python -I metsource.py pscomppars.csv refs.csv > metsource.out
pscomppars.csv is the table the study used (hash in data.sha256). refs.csv is a second query to the same archive,
made on 26 November 2026: select pl_name, hostname, discoverymethod, disc_facility, pl_rade, pl_orbper, st_met,
st_metratio, st_met_reflink, st_teff, sy_pnum from pscomppars. The reference of a value is used only where the
value in the second query equals the value the study used, so that it is the reference of that number.
A reference is one link, not one label: the archive gives some pairs of papers the same label ("Nielsen et al.
2020" is two papers), and those are kept apart here and named by label and the end of the link.  (Until a
reader's third check on 26 November this grouped by label, and counted seven references where there are six.)"""
import csv, re, sys, collections
import numpy as np

def num(x):
    try: return float(x)
    except Exception: return float('nan')

if __name__ == '__main__':
    old = {r['pl_name']: r for r in csv.DictReader(open(sys.argv[1], encoding='utf-8'))}
    new = {r['pl_name']: r for r in csv.DictReader(open(sys.argv[2], encoding='utf-8'))}
    rows = []
    for name, r in old.items():
        if r['discoverymethod'] != 'Transit': continue
        R, P, met = num(r['pl_rade']), num(r['pl_orbper']), num(r['st_met'])
        if not (R == R and P == P and met == met): continue
        kind = 'hot Jupiter' if (R >= 8 and P < 10) else 'small' if R < 4 else None
        if kind is None: continue
        n = new.get(name); ref = None
        if n is not None and abs(num(n['st_met']) - met) < 1e-9:
            m = re.search(r'target=ref>\s*(.*?)\s*</a>', n['st_met_reflink'] or ''); ref = (m.group(1) if m else (n['st_met_reflink'] or '')).replace('&amp;', '&').strip() or None
            h = re.search(r'href=([^ >]+)', n['st_met_reflink'] or ''); link = h.group(1) if h else ''
            if ref: ref = (ref, link)
        rows.append([kind, met, ref, r['st_metratio'], r['disc_facility'], r['hostname']])
    links = collections.defaultdict(set)
    for x in rows:
        if x[2]: links[x[2][0]].add(x[2][1])
    shared = sorted(l for l, v in links.items() if len(v) > 1)
    for x in rows:                                      # a label that stands for several links gets the end of its link
        if x[2]: x[2] = x[2][0] if len(links[x[2][0]]) == 1 else '%s [%s]' % (x[2][0], [t for t in x[2][1].split('/') if t and t != 'abstract'][-1])
    hj = [x for x in rows if x[0] == 'hot Jupiter']; sm = [x for x in rows if x[0] == 'small']
    mean = lambda v: float(np.mean([x[1] for x in v])) if v else float('nan')
    print('planets with a listed metal content: hot Jupiters %d, under 4 Earth radii %d' % (len(hj), len(sm)))
    print('all: hot Jupiters %+.3f, small %+.3f, difference %+.3f' % (mean(hj), mean(sm), mean(hj) - mean(sm)))
    got = [x for x in rows if x[2]]
    print('labels that stand for more than one link, kept apart below: %d (%s)' % (len(shared), '; '.join(shared)))
    print('with the reference of that same value found in the second query: %d of %d (hot Jupiters %d, small %d)' % (len(got), len(rows), sum(x[0] == 'hot Jupiter' for x in got), sum(x[0] == 'small' for x in got)))
    print()
    print('by the ratio the table quotes:')
    for ratio in sorted({x[3] for x in rows}):
        a = [x for x in hj if x[3] == ratio]; b = [x for x in sm if x[3] == ratio]
        print('   %-8s hot Jupiters %4d %+.3f | small %4d %+.3f | difference %s' % (ratio or '(none)', len(a), mean(a), len(b), mean(b), '%+.3f' % (mean(a) - mean(b)) if a and b else '   -'))
    print()
    refs = collections.Counter(x[2] for x in got)
    print('the references that supply the most values (share of each kind of planet that takes its value from it):')
    nh, ns = sum(x[0] == 'hot Jupiter' for x in got), sum(x[0] == 'small' for x in got)
    within = []
    for ref, c in refs.most_common(14):
        a = [x for x in got if x[2] == ref and x[0] == 'hot Jupiter']; b = [x for x in got if x[2] == ref and x[0] == 'small']
        print('   %-46s hot Jupiters %4d (%4.1f%%) %s | small %4d (%4.1f%%) %s | difference %s' % (ref[:46], len(a), 100 * len(a) / nh, '%+.3f' % mean(a) if a else '   -  ', len(b), 100 * len(b) / ns, '%+.3f' % mean(b) if b else '   -  ', '%+.3f' % (mean(a) - mean(b)) if len(a) >= 5 and len(b) >= 5 else '   -'))
    print()
    num_, den, var = 0.0, 0.0, 0.0; used = 0
    for ref in refs:                                    # the difference inside one reference, pooled over references that have both kinds
        a = [x[1] for x in got if x[2] == ref and x[0] == 'hot Jupiter']; b = [x[1] for x in got if x[2] == ref and x[0] == 'small']
        if len(a) >= 3 and len(b) >= 3:
            w = 1 / (1 / len(a) + 1 / len(b)); num_ += w * (np.mean(a) - np.mean(b)); den += w; used += 1; within.append((len(a), len(b)))
            var += w * w * (np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b))
    print('inside one reference (those with at least 3 of each kind: %d references, %d hot Jupiters and %d small planets): pooled difference %+.3f, one standard error %.3f'
          % (used, sum(a for a, b in within), sum(b for a, b in within), num_ / den if den else float('nan'), var ** 0.5 / den if den else float('nan')))
    m = [x for x in got if x[2] == 'Morton et al. 2016']; a = [x[1] for x in m if x[0] == 'hot Jupiter']; b = [x[1] for x in m if x[0] == 'small']
    if len(a) >= 3 and len(b) >= 3: print('inside the largest alone: %+.3f, one standard error %.3f' % (np.mean(a) - np.mean(b), (np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b)) ** 0.5))
    kep = lambda x: x[4] in ('Kepler', 'K2')
    print('share of values from the three largest references of Kepler\'s bulk lists (Morton et al. 2016, Q1-Q17 DR25 KOI Table, Gajdos et al. 2019): hot Jupiters %.1f%%, small %.1f%%'
          % (100 * sum(x[2] in ('Morton et al. 2016', 'Q1-Q17 DR25 KOI Table') or (x[2] or '').startswith('Gajdo') for x in hj) / len(hj), 100 * sum(x[2] in ('Morton et al. 2016', 'Q1-Q17 DR25 KOI Table') or (x[2] or '').startswith('Gajdo') for x in sm) / len(sm)))
    top = refs.most_common(1)[0][0]
    a = [x for x in hj if x[2] != top]; b = [x for x in sm if x[2] != top]
    print('leaving out every value from the largest single reference (%s): hot Jupiters %+.3f (%d), small %+.3f (%d), difference %+.3f' % (top, mean(a), len(a), mean(b), len(b), mean(a) - mean(b)))
    # added after a reader's check of the first corrections (26 November)
    print()
    print('the references with at least 3 of each kind, one by one (difference, one standard error):')
    per = []
    for ref, c in refs.most_common():
        a = [x[1] for x in got if x[2] == ref and x[0] == 'hot Jupiter']; b = [x[1] for x in got if x[2] == ref and x[0] == 'small']
        if len(a) >= 3 and len(b) >= 3:
            d = float(np.mean(a) - np.mean(b)); se = float((np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b)) ** 0.5)
            per.append((ref, len(a), len(b), d, se)); print('   %-46s %3d and %4d: %+.3f (%.3f)' % (ref[:46], len(a), len(b), d, se))
    d = np.array([x[3] for x in per]); se = np.array([x[4] for x in per]); wiv = 1 / se ** 2; wn = np.array([1 / (1 / x[1] + 1 / x[2]) for x in per])
    piv = float((wiv * d).sum() / wiv.sum()); Q = float((wiv * (d - piv) ** 2).sum())
    print('   they run from %+.2f to %+.2f; if they shared one true difference, the weighted sum of squares about it (Q) would be near %d; it is %.0f'
          % (d.min(), d.max(), len(per) - 1, Q))
    big = int(np.argmax([x[1] + x[2] for x in per]))
    print('   pooled four ways: by the numbers of planets (as above) %+.3f; by each one\'s own precision %+.3f; each reference counted once %+.3f; without the largest, each counted once %+.3f'
          % (float((wn * d).sum() / wn.sum()), piv, float(d.mean()), float(np.delete(d, big).mean())))
    a = [x[1] for x in hj if x[3] == '[M/H]']; b = [x[1] for x in sm if x[3] == '[M/H]']
    print('values the table labels [M/H]: %d hot Jupiters and %d small: difference %+.3f, one standard error %.3f' % (len(a), len(b), np.mean(a) - np.mean(b), (np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b)) ** 0.5))
    star = lambda v: {x[5]: x[1] for x in v}
    sa, sb = star(hj), star(sm)
    print('one value a star, not one a planet: %d stars of hot Jupiters %+.3f, %d stars of small planets %+.3f, difference %+.3f' % (len(sa), np.mean(list(sa.values())), len(sb), np.mean(list(sb.values())), np.mean(list(sa.values())) - np.mean(list(sb.values()))))
