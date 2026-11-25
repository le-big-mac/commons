"""Referee's controls for step 2.  usage: controls.py referee/lines-held.csv sealed_dir"""
import sys, csv, re, os
import numpy as np
from scipy.optimize import minimize
from scipy.stats import binom

rows = list(csv.DictReader(open(sys.argv[1])))
sealed = sys.argv[2]
for r in rows:
    r['p'] = float(r['my_odds']); r['y'] = None if r['outcome'] == '' else int(r['outcome'])
    r['q'] = None if r['forecasters'] == '' else float(r['forecasters'])

def brier(p, y): return float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))
def pairs(p, y):
    p, y = np.asarray(p, float), np.asarray(y, int); h, f = p[y == 1], p[y == 0]
    s = sum(float(np.sum(a > f + 1e-12) + 0.5 * np.sum(np.abs(a - f) <= 1e-12)) for a in h)
    return s, len(h) * len(f)

M = [r for r in rows if r['q'] is not None and r['y'] is not None]
print("== A. Ranking within a sheet only (pairs of a held and a failed line on the same sealed file), pair-weighted")
for name, sel in (('six at the time', lambda r: r['src'] == 'ledger'), ('four late', lambda r: r['src'] == 'late'), ('all ten', lambda r: True),
                  ('all ten less aztec', lambda r: not r['file'].startswith('aztec')), ('four late less aztec', lambda r: r['src'] == 'late' and not r['file'].startswith('aztec'))):
    S = [r for r in M if sel(r)]
    sm = sq = n = 0
    for f in sorted(set(r['file'] for r in S)):
        g = [r for r in S if r['file'] == f]
        a, k = pairs([r['p'] for r in g], [r['y'] for r in g]); b, _ = pairs([r['q'] for r in g], [r['y'] for r in g])
        sm += a; sq += b; n += k
    a, k = pairs([r['p'] for r in S], [r['y'] for r in S]); b, _ = pairs([r['q'] for r in S], [r['y'] for r in S])
    print(f"  {name:22s} within-sheet pairs {n:4d}: mine {sm/n:.3f} theirs {sq/n:.3f}   | pooled pairs {k:4d}: mine {a/k:.3f} theirs {b/k:.3f}")

print("== B. How much of the gap is level? my odds moved (added constant, clipped to .01-.99) to the forecasters' mean")
def shifted(S, per_sheet):
    out = []
    if per_sheet:
        for f in sorted(set(r['file'] for r in S)):
            g = [r for r in S if r['file'] == f]
            d = np.mean([r['q'] for r in g]) - np.mean([r['p'] for r in g])
            out += [((np.clip(r['p'] + d, .01, .99)), r['y']) for r in g]
    else:
        d = np.mean([r['q'] for r in S]) - np.mean([r['p'] for r in S])
        out = [((np.clip(r['p'] + d, .01, .99)), r['y']) for r in S]
    return brier([o[0] for o in out], [o[1] for o in out])
for name, sel in (('six at the time', lambda r: r['src'] == 'ledger'), ('four late', lambda r: r['src'] == 'late'), ('all ten', lambda r: True)):
    S = [r for r in M if sel(r)]
    bm = brier([r['p'] for r in S], [r['y'] for r in S]); bq = brier([r['q'] for r in S], [r['y'] for r in S])
    s1 = shifted(S, False); s2 = shifted(S, True)
    print(f"  {name:16s} mine {bm:.4f} theirs {bq:.4f} gap {bm-bq:+.4f} | one shift for the set: {s1:.4f} (closes {100*(bm-s1)/(bm-bq):.0f}% of gap) | "
          f"a shift per sheet to their mean on that sheet: {s2:.4f} (closes {100*(bm-s2)/(bm-bq):.0f}%)")

print("== C. Share of the gaps that is the arctic circle sheet")
for name, sel in (('four late', lambda r: r['src'] == 'late'), ('all ten', lambda r: True)):
    S = [r for r in M if sel(r)]; A = [r for r in S if r['file'].startswith('aztec')]
    tot = sum((r['p'] - r['y']) ** 2 - (r['q'] - r['y']) ** 2 for r in S); az = sum((r['p'] - r['y']) ** 2 - (r['q'] - r['y']) ** 2 for r in A)
    R = [r for r in S if not r['file'].startswith('aztec')]
    print(f"  {name:10s} summed squared-error difference {tot:.3f}, of which aztec's six lines {az:.3f} = {100*az/tot:.0f}%; without aztec: mine {brier([r['p'] for r in R],[r['y'] for r in R]):.4f} theirs {brier([r['q'] for r in R],[r['y'] for r in R]):.4f} closer me {sum(abs(r['p']-r['y'])<abs(r['q']-r['y'])-1e-12 for r in R)} them {sum(abs(r['q']-r['y'])<abs(r['p']-r['y'])-1e-12 for r in R)}")
print("   their lines below 0.3:", [(r['file'].split('/')[0], r['label'], r['q'], 'held' if r['y'] else 'failed') for r in M if r['q'] < 0.3])
print("   their lines below 0.5:", sum(1 for r in M if r['q'] < 0.5), 'held', sum(r['y'] for r in M if r['q'] < 0.5), '; by set: early', sum(1 for r in M if r['q'] < 0.5 and r['src']=='ledger'), 'late', sum(1 for r in M if r['q'] < 0.5 and r['src']=='late'))

print("== D. Cannonballs under the other reading of J6 (failed), and not scored")
J = [r for r in M if r['file'].startswith('impetus')]
for conv, yj in (('held', 1), ('failed', 0)):
    y = [yj if r['label'] == 'J6' else r['y'] for r in J]
    print(f"  J6 {conv}: mine {brier([r['p'] for r in J], y):.4f} theirs {brier([r['q'] for r in J], y):.4f}")
K = [r for r in J if r['label'] != 'J6']
print(f"  J6 not scored: mine {brier([r['p'] for r in K],[r['y'] for r in K]):.4f} theirs {brier([r['q'] for r in K],[r['y'] for r in K]):.4f}")

# ---- correction
def logit(p): p = np.asarray(p, float); return np.log(p / (1 - p))
def fit(p, y, fix_b=False):
    x = logit(p); y = np.asarray(y, float)
    def nll(t):
        z = t[0] + (1.0 if fix_b else t[1]) * x
        return float(np.sum(np.logaddexp(0, z) - y * z))
    r = minimize(nll, [0.0] if fix_b else [0.0, 1.0], method='BFGS')
    return (float(r.x[0]), 1.0) if fix_b else (float(r.x[0]), float(r.x[1]))
def apply(a, b, p): return np.clip(1 / (1 + np.exp(-(a + b * logit(p)))), 0.01, 0.99)
ST = [r for r in rows if r['y'] is not None]
studies = []
for r in ST:
    if r['study'] not in studies: studies.append(r['study'])
print("== E. The correction: where the harm sits")
for r in ST: r['c'] = None
for s in studies:
    tr = [r for r in ST if r['study'] != s]; a, b = fit([r['p'] for r in tr], [r['y'] for r in tr])
    for r in ST:
        if r['study'] == s: r['c'] = float(apply(a, b, [r['p']])[0])
L = [r for r in ST if r['src'] == 'ledger']
print(f"  on the 66 ledger lines: sealed {brier([r['p'] for r in L],[r['y'] for r in L]):.4f} corrected {brier([r['c'] for r in L],[r['y'] for r in L]):.4f} forecasters {brier([r['q'] for r in L],[r['y'] for r in L]):.4f}")
d = sorted(((r['c'] - r['y']) ** 2 - (r['p'] - r['y']) ** 2, r['file'], r['label'], r['p'], round(r['c'], 3), r['y']) for r in ST)
tot = sum(x[0] for x in d)
print(f"  summed change in squared error over 142 lines: {tot:+.3f} (per line {tot/len(ST):+.4f})")
print("  the six lines it harms most:", [(x[1].split('/')[0], x[2], x[3], x[4], round(x[0], 3)) for x in d[-6:]])
az4 = sum(x[0] for x in d if x[1] == 'aztec/expectations.md' and x[5] == 0)
print(f"  the four failed lines of the aztec main sheet alone: {az4:+.3f}; all other 138 lines: {tot-az4:+.3f} (per line {(tot-az4)/138:+.4f})")
for excl in (['arctic circle'], ['arctic circle', 'readers and authors'], ['arctic circle', 'floating cube']):
    S = [r for r in ST if r['study'] not in excl]
    print(f"  without {excl}: sealed {brier([r['p'] for r in S],[r['y'] for r in S]):.4f} corrected {brier([r['c'] for r in S],[r['y'] for r in S]):.4f}")
# leave-one-study-out refit with aztec dropped from the data altogether (nine studies)
S9 = [r for r in ST if r['study'] != 'arctic circle']; c9 = {}
for s in [x for x in studies if x != 'arctic circle']:
    tr = [r for r in S9 if r['study'] != s]; a, b = fit([r['p'] for r in tr], [r['y'] for r in tr])
    for r in S9:
        if r['study'] == s: c9[(r['file'], r['label'])] = float(apply(a, b, [r['p']])[0])
print(f"  nine studies only (aztec never seen), leave one out: sealed {brier([r['p'] for r in S9],[r['y'] for r in S9]):.4f} corrected {brier([c9[(r['file'], r['label'])] for r in S9],[r['y'] for r in S9]):.4f}")
# main sheets only in time order: fit on earlier studies, apply to the next (what was available at the time)
print("  forward in time (fit on all earlier studies, apply to the next; studies in the order of sealed-list):")
tot_p = tot_c = n = 0
for i, s in enumerate(studies):
    if i < 2: continue
    tr = [r for r in ST if r['study'] in studies[:i]]; te = [r for r in ST if r['study'] == s]
    a, b = fit([r['p'] for r in tr], [r['y'] for r in tr]); c = apply(a, b, [r['p'] for r in te]); y = [r['y'] for r in te]
    tot_p += sum((r['p'] - r['y']) ** 2 for r in te); tot_c += float(np.sum((c - np.array(y)) ** 2)); n += len(te)
    print(f"     {s:22s} a {a:+.2f} b {b:5.2f}  sealed {brier([r['p'] for r in te], y):.4f} corrected {brier(c, y):.4f}")
print(f"     together ({n} lines): sealed {tot_p/n:.4f} corrected {tot_c/n:.4f}")

# ---- doubts
print("== F. Doubts: the sheets' own words only")
body = {}
for f in sorted(set(r['file'] for r in rows)):
    t = open(os.path.join(sealed, f), encoding='utf-8').read()
    for b in re.split(r"^(?=[A-Z]+\d+\. )", t, flags=re.M)[1:]:
        body[(f, b.split('.')[0])] = ' '.join(b.split())
def grp(S, name):
    S = [r for r in S if r['y'] is not None]
    if not S: print(f"  {name}: none"); return
    h = sum(r['y'] for r in S); n = len(S); mo = np.mean([r['p'] for r in S])
    print(f"  {name:58s} n {n:3d} held {h:3d} ({h/n:.2f}) mean odds {mo:.3f} Brier {brier([r['p'] for r in S],[r['y'] for r in S]):.3f}")
    return h, n, mo
own = lambda r: ('Marked down' in body[(r['file'], r['label'])]) or ('Same doubt' in body[(r['file'], r['label'])])
OTHER = ("less sure", "I believe this jump", "memory alone", "guessing", "bet on my memory", "not a calculation")
oth = lambda r: (not own(r)) and any(w in body[(r['file'], r['label'])] for w in OTHER)
D = [r for r in rows if own(r)]; O7 = [r for r in rows if oth(r)]
print("  own words:", [(r['label'], r['p'], r['y']) for r in D])
print("  hand-picked:", [(r['label'], r['p'], r['y']) for r in O7])
h, n, mo = grp(D, "the sheet says Marked down / Same doubt")
fs = set(r['file'] for r in D)
grp([r for r in rows if r['file'] in fs and not own(r)], "others on the sheets that have such a line")
grp([r for r in rows if r['file'] in fs and not own(r) and not oth(r)], "  ... leaving out the seven hand-picked")
fs2 = set(r['file'] for r in D + O7)
grp(D + O7, "either (author's twenty)")
grp([r for r in rows if r['file'] in fs2 and not own(r) and not oth(r)], "neither, same sheets (author's 31)")
grp([r for r in rows if r['file'] in fs2 and not own(r) and not oth(r) and r['file'] != 'aztec/expectations.md'], "  ... without the aztec main sheet (in only through A1)")
grp([r for r in rows if not own(r) and not oth(r)], "every other settled line (all sheets)")
grp([r for r in rows if not own(r)], "every settled line not 'marked down' in the sheet's words")
print(f"  P(at least {h} of {n} hold | each holds with my mean odds {mo:.2f}, independent) = {binom.sf(h-1, n, mo):.3f};  exact 95% interval for the share held, 11 of 13: "
      f"{binom.ppf(0.025, 13, 11/13)/13:.2f}..; Clopper-Pearson computed below")
from scipy.stats import beta
lo, hi = beta.ppf(0.025, h, n - h + 1), beta.ppf(0.975, h + 1, n - h)
print(f"  Clopper-Pearson 95% for {h}/{n}: {lo:.2f} to {hi:.2f};  for 16/20: {beta.ppf(0.025,16,5):.2f} to {beta.ppf(0.975,17,4):.2f}; for 26/31: {beta.ppf(0.025,26,6):.2f} to {beta.ppf(0.975,27,5):.2f}")
se = (0.8 * 0.2 / 20 + (26 / 31) * (5 / 31) / 31) ** 0.5
print(f"  difference in share held, 16/20 minus 26/31: {16/20-26/31:+.3f}, normal 95% {16/20-26/31-1.96*se:+.2f} to {16/20-26/31+1.96*se:+.2f} (as if independent); the difference I priced: {0.630-0.840:+.2f}")
