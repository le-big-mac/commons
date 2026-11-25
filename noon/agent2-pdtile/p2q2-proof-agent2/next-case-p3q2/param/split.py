"""Inner regions of the (p, q) plane for Z_{p^3 q^2}: certificates with case distinctions.
For a band (a region with polynomial bounds) and a pattern for which no single basis is certified on the whole band,
branch on the sign of the polynomial factor that could not be signed: on the branch F >= 0 (and on F <= 0) the factor F is
taken as known, sample points are restricted to the branch, and the pattern is analysed again (recursively, to a small
depth).  Every pair in the band lies in one of the two branches, so the leaves cover the band.
usage: split.py BAND [depth]             (Noon = agent2, 21 November 2026)"""
import sys, pickle, time
from collections import Counter
import sympy as sp
import region as R
from region import P, Q
from empty import refute

ASSUME = []                                               # list of (polynomial, +1 or -1): sign * polynomial >= 0 on the current branch
_orig_sign_factor = R.sign_factor
def sign_factor(g, reg):
    for F, sg in ASSUME:
        if sp.expand(g - F) == 0: return '+0' if sg > 0 else '-0'
        if sp.expand(g + F) == 0: return '-0' if sg > 0 else '+0'
    return _orig_sign_factor(g, reg)
R.sign_factor = sign_factor
_orig_sign = R.sign
def sign(expr_K, reg):
    """as region.sign, but a factor known only weakly (an assumed one, or one that vanishes at the corner) may not sit in a denominator"""
    if expr_K == R.K2.zero: return '0', None
    num, den = sp.fraction(sp.cancel(R.K2.to_sympy(expr_K)))
    for f, mult in sp.factor_list(den)[1]:
        if sign_factor(f, reg) in ('+0', '-0', '0', '?'): return '?', f
    return _orig_sign(expr_K, reg)
R.sign = sign

def pool(band):
    """many prime pairs of the band"""
    fixed, lo, up, p0 = BANDS[band]; out = []
    for pv in [101, 53, 31, 23, 17, 13, 11, 7, 5, 3, 2, 211, 499]:
        if pv < p0: continue
        L, U = int(lo.subs(fixed, pv)), int(sp.floor(up.subs(fixed, pv)))
        if L > U: continue
        xs = sorted({L + (U - L) * k // 24 for k in range(25)})
        for x in xs:
            c = int(sp.nextprime(x - 1))
            if c > U or c == pv: continue
            out.append((pv, c) if fixed == P else (c, pv))
    return list(dict.fromkeys(out))
BANDS = {'B1': (P, P**2 + 1, P**2 + P, 5), 'B2': (P, P**2 + P + 1, P**3 - P**2 + P - 1, 3), 'B3': (P, P**3 - P**2 + P, P**3 - 1, 3),
         'Ap1': (Q, Q + 1, Q**2 - Q + 1, 3), 'Ap2': (Q, Q**2 - Q + 1, Q**2 - 1, 3), 'A1a': (P, P + 2, 2 * P - sp.Rational(5, 2), 5), 'A1b': (P, 2 * P - 1, P**2 - P + 1, 5), 'A2': (P, P**2 - P + 1, P**2 - 1, 3)}

def analyse_branch(Z, band, POOL, assume, depth, maxdepth):
    global ASSUME
    pts = [pt for pt in POOL if all(sg * F.subs({P: pt[0], Q: pt[1]}) >= 0 for F, sg in assume)]
    if not pts:
        proof = refute(assume, *BANDS[band])                 # no sample point: try to prove that the branch contains no point at all
        if proof: return dict(cat='empty', proof=proof)
        return dict(cat='empty?', assume=[(str(F), sg) for F, sg in assume])
    ASSUME = list(assume); R.SIGN_CACHE.clear()
    saved = R.REGIONS[band]; R.REGIONS[band] = (saved[0], pts[:14])
    try: res = R.analyse(Z, band)
    finally: R.REGIONS[band] = saved
    if res['cat'] != '?' or depth >= maxdepth: res['npts'] = len(pts); return res
    cands = [f for kind, f in res.get('fails', []) if kind in ('primal', 'dual') and f not in ('?', '-', '-0', None)]
    for fs in cands:
        F = sp.sympify(fs, locals={'p': P, 'q': Q})
        if any(sp.expand(F - G) == 0 or sp.expand(F + G) == 0 for G, _ in assume): continue
        if _orig_sign_factor(F, band) != '?': continue      # a definite factor with the wrong sign: this basis is simply not optimal here
        pos = analyse_branch(Z, band, POOL, assume + [(F, 1)], depth + 1, maxdepth)
        neg = analyse_branch(Z, band, POOL, assume + [(F, -1)], depth + 1, maxdepth)
        return dict(cat='split', factor=str(F), pos=pos, neg=neg)
    return res

def leaves(res, path=()):
    if res['cat'] == 'split':
        yield from leaves(res['pos'], path + ((res['factor'], 1),)); yield from leaves(res['neg'], path + ((res['factor'], -1),))
    else: yield path, res

if __name__ == '__main__':
    band = sys.argv[1]; maxdepth = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    base = pickle.load(open(f"region_{band}.pkl", "rb")); POOL = pool(band); t0 = time.time(); out = dict(base); stat = Counter()
    for Z, r in base.items():
        if r['cat'] != '?': continue
        res = analyse_branch(Z, band, POOL, [], 0, maxdepth); res['t2'] = r.get('t2'); out[Z] = res
        lv = list(leaves(res)); ok = all(l['cat'] not in ('?', 'empty?') for _, l in lv)
        stat['settled' if ok else 'open'] += 1
        desc = "; ".join(("&".join(f"{'+' if sg > 0 else '-'}[{f[:28]}]" for f, sg in path) or 'whole band') + f": {l['cat']}{'/' + str(l.get('kind')) if l.get('kind') else ''}" for path, l in lv)
        print(('OK  ' if ok else 'OPEN'), sorted(Z), '|', desc[:330], flush=True)
    print(f"band {band}: {sum(stat.values())} patterns re-analysed with case distinctions: settled {stat['settled']}, open {stat['open']}   [{time.time() - t0:.0f} s]")
    pickle.dump(out, open(f"split_{band}.pkl", "wb"))
