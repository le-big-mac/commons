"""Item 4: every start from 300 BC to 1 BC with the checker's own scoring and the catalogue's Delta T.
Syzygy times outside the JPL windows are from the author's phases.py (accepted after c3_phases.py); inside the 'then' window the
checker's own JPL syzygies are used as a cross-check on the same starts."""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, own
import phases                 # the author's Meeus (see c3_phases.py)

cat = own.catalogue(-299, 100)
cj = np.array([r['jd'] for r in cat]); cd = np.array([r['dt'] for r in cat])
def dT(jd):
    return float(np.interp(jd, cj, cd))
K0 = -27255.5                 # Meeus k of the full moon of 12 May 205 BC (month 1 at start 0); checked below against JPL
full, new = own.syz('then')
print(f'Meeus full moon k = {K0}: JDE {phases.true_phase(K0):.4f}; my first JPL full moon {full[0]:.4f}')

def ut_h(k, month, kind):
    t = phases.true_phase(K0 + k + month - 1 + (0.5 if kind == 'S' else 0.0))
    return ((t - dT(t) / 86400.0 + 0.5) % 1.0) * 24.0

JD_300BC = own.jd_julian(-299, 1, 1); JD_1AD = own.jd_julian(1, 1, 1)
K = [k for k in range(-1400, 2900) if JD_300BC <= phases.true_phase(K0 + k) < JD_1AD]
print(f'starts whose first full moon falls from 1 Jan 300 BC to 31 Dec 1 BC (Julian calendar): {len(K)}; k from {K[0]} to {K[-1]}')
def bc(k):
    jd = phases.true_phase(K0 + k); return 1 - math.floor(-4712 + (jd + 0.5) / 365.25)

g22 = own.glyphs(); g18 = own.glyphs(drop=own.OUT4)
L025 = np.arange(-180, 180, 0.25)
def table(g, lons=L025):
    am = np.array([h for m, kind, h in g], float)
    out = {}
    for k in K:
        ut = np.array([ut_h(k, m, kind) for m, kind, h in g])
        out[k] = own.best(am, ut, lons)
    return out
S18 = table(g18); S22 = table(g22)
SIX = {299: -1162, 223: -223, 205: 0, 187: 223, 183: 270, 169: 446, 165: 493, 147: 716, 129: 939, 111: 1162, 93: 1385, 89: 1432, 71: 1655, 53: 1878, 35: 2101, 17: 2324}
for b, k in SIX.items(): assert bc(k) == b, (b, k, bc(k))
auth = json.load(open(os.path.join(os.path.dirname(HERE), 'hours_run.json')))
a18 = {int(k): v for k, v in auth['18']['scores'].items()}; a22 = {int(k): v for k, v in auth['22']['scores'].items()}
print('author\'s starts:', len(a18), '; same set of k as mine:', sorted(a18) == K)
common = [k for k in K if k in a18]
d = np.array([S18[k][0] - a18[k][0] for k in common]); dl = np.array([((S18[k][1] - a18[k][1] + 180) % 360) - 180 for k in common])
print(f'18: my score - author\'s over {len(common)} starts: mean {d.mean():+.4f}, largest {np.abs(d).max():.4f} h; longitude mine - author\'s: median {np.median(dl):+.2f}, |.| > 3 deg: {int((np.abs(dl) > 3).sum())}')
d = np.array([S22[k][0] - a22[k][0] for k in common])
print(f'22: my score - author\'s: mean {d.mean():+.4f}, largest {np.abs(d).max():.4f} h')

for name, S in (('18', S18), ('22', S22)):
    order = sorted(K, key=lambda k: S[k][0]); v = np.array([S[k][0] for k in K])
    print(f'\n== {name} hours: median {np.median(v):.2f}, sd {v.std():.2f}; 205 BC {S[0][0]:.3f} h at {S[0][1]:+.2f}; strictly lower than 205 BC: {int((v < S[0][0]).sum())}; rank {1 + order.index(0)}')
    print('   the sixteen: ' + '; '.join(f'{b} BC {S[k][0]:.2f} at {S[k][1]:+.0f} (rank {1 + order.index(k)})' for b, k in SIX.items()))
    better = [k for k in K if S[k][0] < S[0][0]]
    inv = {k: b for b, k in SIX.items()}
    print('   of those better than 205 BC, among the sixteen:', [inv[k] for k in better if k in inv])
    print('   best fifteen (score, k, BC, longitude, k mod 223, as cycles+months):')
    for k in order[:15]:
        m = k // 223 if k >= 0 else -((-k) // 223)
        print(f'     {S[k][0]:.2f} k={k:5d} {bc(k):3d} BC {S[k][1]:+7.1f}  k mod 223 = {k % 223:3d}   {m:+d} cycles {k - 223 * m:+d} months')
    print(f'   +767: {S[767][0]:.2f} h ({bc(767)} BC, at {S[767][1]:+.0f}); -767: {S[-767][0]:.2f} h ({bc(-767)} BC, at {S[-767][1]:+.0f})')
    print('   whole cycles: ' + '; '.join(f'{k // 223:+d}: {S[k][0]:.2f}, {S[k][1]:+.0f}' for k in K if k % 223 == 0))
    if name == '18':
        print('   under 3.0 h:', int((v < 3.0).sum()), '; under 2.3 h:', int((v < 2.3).sum()), '; 18 best scores range', round(v.min(), 2))
        steps = [((S[b][1] - S[a][1] + 180) % 360) - 180 for a, b in ((-223, 0), (0, 223), (223, 446))]
        print('   longitude steps 223->205->187->169 BC:', [round(s, 2) for s in steps], '; three cycles (-3, 0, +3):', S[-669][1], S[0][1], S[669][1])
        within = [k // 223 for k in K if k % 223 == 0 and S[k][0] - min(S[kk][0] for kk in K if kk % 223 == 0) <= 0.4]
        print('   whole cycles within 0.4 h of the best whole cycle:', within)
        # k mod 223 classes of everything better than 205 BC
        from collections import Counter
        print('   k mod 223 of the starts better than 205 BC:', sorted(Counter(k % 223 for k in better).items()))
json.dump({'18': {str(k): S18[k] for k in K}, '22': {str(k): S22[k] for k in K}}, open(os.path.join(HERE, 'c4_all.json'), 'w'))

# longitude kept to 10..40 E
G = table(g18, np.arange(10, 40.0001, 0.25))
order = sorted(K, key=lambda k: G[k][0])
print(f'\n== 18 hours, longitude 10..40 E: 205 BC {G[0][0]:.2f} at {G[0][1]:+.1f}, rank {1 + order.index(0)}; under 3.0 h: {sum(G[k][0] < 3.0 for k in K)}; of those among the sixteen: {[b for b, k in SIX.items() if G[k][0] < 3.0]}')
print('   the sixteen in order:', sorted((round(G[k][0], 2), b) for b, k in SIX.items())[:5])
print('   best ten:', [(round(G[k][0], 2), bc(k), k, G[k][1]) for k in order[:10]])
print('   259 BC (k=-669) and 151 BC (k=669) in the range:', G[-669], G[669])
# sensitivity of "only one of the sixteen" to the range chosen
for lo, hi in ((0, 50), (15, 35), (20, 30), (5, 45), (-10, 60)):
    Gx = {k: own.best([h for m, kind, h in g18], [ut_h(k, m, kind) for m, kind, h in g18], np.arange(lo, hi + 1e-9, 0.25)) for b, k in SIX.items()}
    print(f'   range {lo}..{hi} E: the sixteen in order:', sorted((round(Gx[k][0], 2), b) for b, k in SIX.items())[:3])
