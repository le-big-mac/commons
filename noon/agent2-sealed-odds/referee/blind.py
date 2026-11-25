"""Blind rebuild of the report's table.
Usage: blind.py sealed_dir sealed-list.txt forecast_dir
Outcomes are typed here by hand from each study's published README (read by me, the referee), by the letter
as that README rules. 1 = held, 0 = failed, None = not scored (void / not settled).
"""
import sys, os, json, csv, math
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import parse

sealed_dir, listfile, forecast_dir = sys.argv[1], sys.argv[2], sys.argv[3]
J6 = sys.argv[4] if len(sys.argv) > 4 else 'held'   # held | failed | void : the J6 convention

H, F, V = 1, 0, None
OUT = {
 'birth/expectations.md': dict(M1=H, M2=H, M3=H, M4=F, M5=H, M6=H, M7=H, M8=H, M9=H, M10=F, M11=H),
 'battles/expectations.md': dict(W1=H, W2=H, W3=H, W4=H, W5=H, W6=H, W7=H, W8=H, W9=H, W10=H, W11=F),
 'transits/expectations.md': dict(X1=F, X2=H, X3=H, X4=H, X5=H, X6=H, X7=H, X8=H, X9=H, X10=H, X11=F, X12=H),
 'vacancy/expectations.md': dict(V1=H, V2=H, V3=H, V4=H, V5=H, V6=H, V7=H, V8=F, V9=H, V10=H, V11=H, V12=H),
 'vacancy/meta.md': dict(Z1=F),
 'authors/expectations.md': dict(R1=H, R2=H, R3=F, R4=H, R5=H),
 'authors2/expectations.md': dict(S1=H, S2=V, S3=V, S4=F, S5=H, S6=F),
 'authors2/expectations-quick.md': dict(Q1=H, Q2=F, Q3=F),
 'float/expectations.md': dict(F1=H, F2=H, F3=H, F4=H, F5=F, F6=V, F7=F),
 'onset/expectations.md': dict(O1=H, O2=H, O3=H, O4=H, O5=H, O6=H, O7=F, O8=H, O9=H, O10=H),
 'onset/meta.md': dict(Z1=H),
 'onset/plateau-prediction.md': dict(P1=H, P2=F, P3=H, P4=H),
 'onset/long-prediction.md': dict(L1=H, L2=F),
 'onset/climb-prediction.md': dict(C1=H, C2=H, C3=H),
 'onset/dip-prediction.md': dict(D1=H, D2=H),
 'onset/long2-prediction.md': dict(M1=H, M2=H),
 'onset/long3-prediction.md': dict(N1=H, N2=H),
 'onset/long4-prediction.md': dict(Q1=H, Q2=H, Q3=H, Q4=H),
 'onset/long5-prediction.md': dict(R1=H, R2=H, R3=F, R4=H),
 'onset/long6-prediction.md': dict(S1=H, S2=F),
 'onset/long7-prediction.md': dict(U1=H, U2=H, U3=H),
 'taffy/expectations.md': dict(T1=H, T2=H, T3=H, T4=H, T5=H, T6=H, T7=H, T8=H, T9=H, T10=H),
 'taffy/meta.md': dict(Z1=F),
 'impetus/expectations.md': dict(J1=H, J2=H, J3=H, J4=H, J5=H, J6={'held': H, 'failed': F, 'void': V}[J6],
                                 J7=H, J8=H, J9=H, J10=H),
 'aztec/expectations.md': dict(A1=F, A2=F, A3=H, A4=F, A5=H, A6=F),
 'aztec/corners-prediction.md': dict(B1=H, B2=H, B3=H, B4=H, B5=H, B6=H),
 'aztec/tw-prediction.md': dict(W1=H, W2=H, W3=H, W4=F, W5=H),
}
LEDGER_STUDY = {'birth/expectations.md': 'birth-months', 'battles/expectations.md': 'battles',
                'transits/expectations.md': 'transits', 'vacancy/expectations.md': 'vacancy',
                'onset/expectations.md': 'onset', 'taffy/expectations.md': 'taffy'}

# ---- read everything
rows = []
for ln in open(listfile).read().splitlines()[1:]:
    if not ln.strip():
        continue
    f, study, kind, folder = [x.strip() for x in ln.split('|')]
    lines, _ = parse(os.path.join(sealed_dir, f))
    assert set(l['label'] for l in lines) == set(OUT[f]), (f, [l['label'] for l in lines], list(OUT[f]))
    for l in lines:
        assert l['odds'] is not None
        rows.append(dict(file=f, study=study, kind=kind, label=l['label'], p=l['odds'], y=OUT[f][l['label']], fc=None))

# forecasters: ledger medians
led = {}
ledger_studies = set()
with open(os.path.join(sealed_dir, 'calib', 'ledger.csv')) as fh:
    for r in csv.DictReader(fh):
        led[(r['study'], r['label'])] = (float(r['forecasters_median']), float(r['my_odds']))
        ledger_studies.add(r['study'])
# forecasters: fN-K.json medians
fj = {}
for k in range(1, 5):
    d = [json.load(open(os.path.join(forecast_dir, f'f{n}-{k}.json'))) for n in (1, 2, 3)]
    keys = set(d[0])
    assert all(set(x) == keys for x in d), k
    for key in keys:
        fj[key] = float(np.median([x[key] for x in d]))
for r in rows:
    if r['file'] in LEDGER_STUDY:
        m, mine = led[(LEDGER_STUDY[r['file']], r['label'])]
        assert abs(mine - r['p']) < 1e-9, ('ledger my_odds differs from sealed', r, mine)
        r['fc'] = m; r['fcsrc'] = 'ledger'
    elif r['kind'] == 'main sheet':
        r['fc'] = fj[r['label']]; r['fcsrc'] = 'late'
used_fj = set(r['label'] for r in rows if r.get('fcsrc') == 'late')
assert used_fj == set(fj), (set(fj) - used_fj)

def out(*a):
    print(*a)

def brier(p, y):
    p, y = np.asarray(p, float), np.asarray(y, float)
    return float(np.mean((p - y) ** 2)) if len(p) else float('nan')

def auc(p, y):
    p, y = np.asarray(p, float), np.asarray(y, int)
    h, f = p[y == 1], p[y == 0]
    if len(h) == 0 or len(f) == 0:
        return float('nan'), 0
    s = 0.0
    for a in h:
        s += np.sum(a > f + 1e-12) + 0.5 * np.sum(np.abs(a - f) <= 1e-12)
    return s / (len(h) * len(f)), len(h) * len(f)

def summ(rs, name):
    n = len(rs); st = [r for r in rs if r['y'] is not None]
    h = sum(r['y'] for r in st); f = len(st) - h
    p = [r['p'] for r in st]; y = [r['y'] for r in st]
    mo = np.mean(p) if st else float('nan')
    out(f"{name:34s} sealed {n:3d}  settled {len(st):3d}  held {h:3d}  failed {f:3d}  share held {h/len(st) if st else float('nan'):.3f}  "
        f"mean odds {mo:.4f}  Brier {brier(p, y):.4f}")

out(f"### J6 convention: {J6}")
out("\n## 1. All sealed lines")
summ(rows, 'all')
out("   not scored:", [(r['file'], r['label']) for r in rows if r['y'] is None])
st_all = [r for r in rows if r['y'] is not None]
out(f"   mean odds over ALL sealed lines (settled or not): {np.mean([r['p'] for r in rows]):.4f}")

out("\n## 2. Per study and per kind")
studies = []
for r in rows:
    if r['study'] not in studies:
        studies.append(r['study'])
for s in studies:
    summ([r for r in rows if r['study'] == s], s)
out()
for k in ('main sheet', 'follow-up', 'bet on my odds'):
    summ([r for r in rows if r['kind'] == k], k)
out()
out("  per sealed file:")
files = []
for r in rows:
    if r['file'] not in files:
        files.append(r['file'])
for f in files:
    summ([r for r in rows if r['file'] == f], '  ' + f)

out("\n## 3. By band of my odds (lower end included), settled lines")
bands = [(0, 50, 'below 0.5'), (50, 60, '0.5-0.6'), (60, 70, '0.6-0.7'), (70, 80, '0.7-0.8'), (80, 90, '0.8-0.9'), (90, 101, '0.9+')]
for lo, hi, nm in bands:
    rs = [r for r in st_all if lo <= round(r['p'] * 100) < hi]
    if rs:
        h = sum(r['y'] for r in rs)
        out(f"  {nm:10s} lines {len(rs):3d}  mean odds {np.mean([r['p'] for r in rs]):.4f}  held {h:3d}  share held {h/len(rs):.4f}")
    else:
        out(f"  {nm:10s} lines 0")

def versus(rs, name):
    rs = [r for r in rs if r['y'] is not None and r['fc'] is not None]
    if not rs:
        out(f"  {name}: no lines"); return
    p = np.array([r['p'] for r in rs]); q = np.array([r['fc'] for r in rs]); y = np.array([r['y'] for r in rs])
    dm, dq = np.abs(p - y), np.abs(q - y)
    mc = int(np.sum(dm < dq - 1e-12)); qc = int(np.sum(dq < dm - 1e-12)); eq = len(rs) - mc - qc
    am, npair = auc(p, y); aq, _ = auc(q, y)
    out(f"  {name:28s} n {len(rs):3d} held {int(y.sum()):3d} failed {int(len(y)-y.sum()):2d} | Brier mine {brier(p,y):.4f} theirs {brier(q,y):.4f} "
        f"| closer: me {mc:2d} them {qc:2d} equal {eq:2d} | rank (pairs {npair:4d}): mine {am:.4f} theirs {aq:.4f} "
        f"| mean odds mine {p.mean():.3f} theirs {q.mean():.3f}")

out("\n## 4. The 66 ledger lines (forecasters = ledger column forecasters_median; outcomes mine from the READMEs)")
L = [r for r in rows if r.get('fcsrc') == 'ledger']
versus(L, 'ledger, all 66')
for f in LEDGER_STUDY:
    versus([r for r in L if r['file'] == f], f.split('/')[0])

out("\n## 5. The other main sheets (forecasters = median of f1,f2,f3), settled lines")
O = [r for r in rows if r.get('fcsrc') == 'late']
versus(O, 'other main sheets, together')
for s in ('readers and authors', 'floating cube', 'cannonballs', 'arctic circle'):
    versus([r for r in O if r['study'] == s], s)
out("  (the readers-and-authors study split into its three sealed files)")
for f in ('authors/expectations.md', 'authors2/expectations.md', 'authors2/expectations-quick.md'):
    versus([r for r in O if r['file'] == f], f)
out("  all settled main-sheet lines:")
versus(L + O, 'all main sheets')
versus([r for r in L + O if r['study'] != 'arctic circle'], 'all main sheets less aztec')
versus([r for r in O if r['study'] != 'arctic circle'], 'other sheets less aztec')

# ---- 6. recalibration
def logit(p):
    p = np.asarray(p, float)
    return np.log(p / (1 - p))

def fit(p, y, fix_b=False):
    x = logit(p); y = np.asarray(y, float)
    def nll(t):
        a = t[0]; b = 1.0 if fix_b else t[1]
        z = a + b * x
        return float(np.sum(np.logaddexp(0, z) - y * z))
    t0 = [0.0] if fix_b else [0.0, 1.0]
    res = minimize(nll, t0, method='BFGS')
    res2 = minimize(nll, res.x, method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-12, maxiter=20000))
    t = res2.x if res2.fun <= res.fun else res.x
    return (float(t[0]), 1.0) if fix_b else (float(t[0]), float(t[1]))

def apply(a, b, p):
    z = a + b * logit(p)
    return np.clip(1 / (1 + np.exp(-z)), 0.01, 0.99)

out("\n## 6. Correction logit(p') = a + b logit(p), leave one study out, p' clipped to [0.01, 0.99]")
for fix_b, nm in ((False, 'a and b free'), (True, 'b fixed at 1')):
    corr = {}
    out(f"  -- {nm}")
    tot_raw = tot_cor = 0.0
    for s in studies:
        tr = [r for r in st_all if r['study'] != s]; te = [r for r in st_all if r['study'] == s]
        a, b = fit([r['p'] for r in tr], [r['y'] for r in tr], fix_b)
        pc = apply(a, b, [r['p'] for r in te]); y = np.array([r['y'] for r in te]); p = np.array([r['p'] for r in te])
        for r, v in zip(te, pc):
            corr[(r['file'], r['label'])] = v
        out(f"    left out {s:22s} n {len(te):3d}  a {a:+.4f} b {b:.4f}  Brier raw {brier(p,y):.4f}  corrected {brier(pc,y):.4f}  diff {brier(pc,y)-brier(p,y):+.4f}")
    pc = np.array([corr[(r['file'], r['label'])] for r in st_all]); y = np.array([r['y'] for r in st_all]); p = np.array([r['p'] for r in st_all])
    out(f"    ALL settled n {len(st_all)}: Brier raw {brier(p,y):.4f}  corrected {brier(pc,y):.4f}  diff {brier(pc,y)-brier(p,y):+.4f}; "
        f"studies where corrected is better: {sum(1 for s in studies if brier([corr[(r['file'], r['label'])] for r in st_all if r['study']==s],[r['y'] for r in st_all if r['study']==s]) < brier([r['p'] for r in st_all if r['study']==s],[r['y'] for r in st_all if r['study']==s]))} of {len(studies)}")
    na = [r for r in st_all if r['study'] != 'arctic circle']
    pc2 = np.array([corr[(r['file'], r['label'])] for r in na]); y2 = np.array([r['y'] for r in na]); p2 = np.array([r['p'] for r in na])
    out(f"    all but arctic circle n {len(na)}: Brier raw {brier(p2,y2):.4f}  corrected {brier(pc2,y2):.4f}")
p = [r['p'] for r in st_all]; y = [r['y'] for r in st_all]
a, b = fit(p, y); out(f"  fitted to all settled lines at once: a {a:+.4f} b {b:.4f}   (in-sample Brier {brier(apply(a,b,p), y):.4f}, raw {brier(p,y):.4f})")
a1, _ = fit(p, y, True); out(f"  fitted to all at once with b fixed at 1: a {a1:+.4f}   (in-sample Brier {brier(apply(a1,1,p), y):.4f})")

# dump lines for later use
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'lines-{J6}.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['file', 'study', 'kind', 'label', 'my_odds', 'outcome', 'forecasters', 'src'])
    for r in rows:
        w.writerow([r['file'], r['study'], r['kind'], r['label'], r['p'], '' if r['y'] is None else r['y'],
                    '' if r['fc'] is None else r['fc'], r.get('fcsrc', '')])
