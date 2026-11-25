"""Verdicts on the ten sealed expectations, by the letter.   usage: python verdicts.py sheet.json sizes-random.json sizes-regular.json results.json"""
import sys, json, math
import numpy as np
S = json.load(open(sys.argv[1])); RA = json.load(open(sys.argv[2]))['sizes']; RE = json.load(open(sys.argv[3]))['sizes']
P = {(p['shape'], p['K']): p for p in S['points']}
V = {}; M = {}
r = lambda sh, K: P[(sh, K)]['r']
V['O1'] = abs(r('lorentz', 2.0) - 0.707) <= 0.03 and abs(r('lorentz', 1.5) - 0.577) <= 0.03
M['O1'] = f"{r('lorentz', 2.0):.3f} at K = 2 and {r('lorentz', 1.5):.3f} at K = 1.5"
V['O2'] = 0.82 <= r('gauss', 1.5) <= 0.88; M['O2'] = f"{r('gauss', 1.5):.3f}"
V['O3'] = r('uniform', 0.9) < 0.2 and 0.78 <= r('uniform', 1.05) <= 0.90; M['O3'] = f"{r('uniform', 0.9):.3f} at K = 0.9 and {r('uniform', 1.05):.3f} at K = 1.05"
up = [s for s in S['sweep'] if s['leg'] == 'up']; down = [s for s in S['sweep'] if s['leg'] == 'down']
k_up = next(s['K'] for s in up if s['r'] > 0.5); k_down = [s['K'] for s in down if s['r'] > 0.5][-1]
V['O4'] = abs(k_up - k_down) <= 0.06 + 1e-9; M['O4'] = f"up at {k_up:.2f}, down to {k_down:.2f}"
p5 = P[('gauss', 0.5)]; x5 = p5['N'] * p5['r2']
V['O5'] = 1.5 <= x5 <= 2.6; M['O5'] = f"{x5:.2f}"
def slope(rows):
    return float(np.polyfit(np.log([q['N'] for q in rows]), np.log([q['r'] for q in rows]), 1)[0])
s6, s7 = slope(RA), slope(RE)
V['O6'] = -0.26 <= s6 <= -0.14; M['O6'] = f"{s6:+.3f}"
V['O7'] = -0.46 <= s7 <= -0.30; M['O7'] = f"{s7:+.3f}"
pairs = [(a['N'], e['r'], a['r']) for a, e in zip(RA, RE) if a['N'] >= 400]
V['O8'] = all(e < a for _, e, a in pairs); M['O8'] = f"regular below random at {sum(e < a for _, e, a in pairs)} of {len(pairs)} sizes"
med = {}
for q in S['rise']:
    t = sorted(x if x is not None else math.inf for x in q['times']); med[q['K']] = (t[len(t) // 2 - 1] + t[len(t) // 2]) / 2
ratio = med[1.2] / med[2.0]
V['O9'] = ratio >= 3; M['O9'] = f"median {med[1.2]:.1f} at K = 1.2 and {med[2.0]:.1f} at K = 2: ratio {ratio:.2f}"
ks = (1.02, 1.05, 1.10); s10 = float(np.polyfit(np.log([k - 1 for k in ks]), np.log([r('gauss', k) for k in ks]), 1)[0])
V['O10'] = 0.35 <= s10 <= 0.55; M['O10'] = f"{s10:.3f} (r = " + ", ".join(f"{r('gauss', k):.3f}" for k in ks) + ")"
for k in sorted(V, key=lambda k: int(k[1:])):
    print(f"{k:4s} {'held  ' if V[k] else 'failed'}  {M[k]}")
print("sizes at K = 1 (Gaussian): N, runs, mean measured r random (sd between runs), regular (sd)")
for a, e in zip(RA, RE):
    print(f"   {a['N']:6d} {a['runs']:4d}   {a['r']:.4f} ({a['sd']:.4f})   {e['r']:.4f} ({e['sd']:.4f})")
json.dump(dict(verdicts={k: bool(v) for k, v in V.items()}, measured=M, slopes=dict(random=s6, regular=s7), medians={str(k): v for k, v in med.items()}), open(sys.argv[4], 'w'), indent=1)
