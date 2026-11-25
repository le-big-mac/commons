"""q5btest.py: the addendum's scoring (study5b.py) tried on made-up figures from each reading, and with a file missing.
python -I q5btest.py [a copy of study5b.py]     (as first run, before the addendum was sealed, it was typed at the prompt; this is the same test kept)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) > 1: sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))
sys.path.append(HERE)
import study5b, theory
D3 = {300: -0.0401, 1000: -0.0450, 3000: -0.0471}; E = {300: 0.0014, 1000: 0.0022, 3000: 0.0044}; npass = nfail = 0
def check(name, cond):
    global npass, nfail
    if cond: npass += 1; print('pass  ' + name)
    else: nfail += 1; print('FAIL  ' + name)
def share(sh): return {n: D3[n] * theory.predictions(sh, n)['exact'] / theory.predictions('disc', n)['exact'] for n in D3}
CASES = [('the same amount for every shape', -0.045, D3, D3, 'nnnn'), ('the same share', -0.045, share('triangle'), share('rtriangle'), 'Ynnn'), ('corners add 0.012', -0.045, {n: D3[n] - 0.012 for n in D3}, D3, 'YYYY'), ('corners add 0.045', -0.045, {n: D3[n] - 0.045 for n in D3}, D3, 'nYYY'),
         ('the triangle 0.02 above', -0.045, {n: D3[n] + 0.02 for n in D3}, D3, 'nnnn'), ('corners add 0.012 at 300 points only', -0.045, {300: D3[300] - 0.012, 1000: D3[1000], 3000: D3[3000]}, D3, 'nnYn'),
         ('corners add 0.012 at 1,000 points only, and the control disc 0.01 lower', -0.055, {300: D3[300], 1000: D3[1000] - 0.012, 3000: D3[3000]}, D3, 'nYnn'), ('corners add 0.03 at 3,000 points only', -0.045, {300: D3[300], 1000: D3[1000], 3000: D3[3000] - 0.03}, D3, 'nnnn'),
         ('the triangle 0.0199 below the control and 0.0081 below the rounded triangle at every size', -0.045, {n: D3[n] - 0.0199 for n in D3}, {n: D3[n] - 0.0118 for n in D3}, 'YYYY'), ('the triangle 0.0201 below the control, 0.0079 below the rounded triangle', -0.045, {n: D3[n] - 0.0201 for n in D3}, {n: D3[n] - 0.0122 for n in D3}, 'nnnn')]
for lab, Bc, Bt, Br, want in CASES:
    v, fig = study5b.verdicts(Bc, Bt, Br, E, E); got = ''.join('Y' if v[t] else 'n' for t in ('Q10', 'Q11', 'Q12', 'Q13')); check('%s: %s' % (lab, want), got == want)
w = {n: 1 / (2 * E[n] ** 2) for n in D3}; Bt = {300: -0.05, 1000: -0.06, 3000: -0.09}; v, fig = study5b.verdicts(-0.045, Bt, D3, E, E); mine = sum(w[n] * (Bt[n] - D3[n]) for n in D3) / sum(w.values())
check('the pooled figure is the mean weighted by the errors (%+.5f), and its error %.5f' % (mine, sum(w.values()) ** -0.5), abs(fig['Q13'] - mine) < 1e-12 and abs(fig['Q13se'] - sum(w.values()) ** -0.5) < 1e-12)
v, fig = study5b.verdicts(None, {300: -0.05, 1000: None, 3000: -0.06}, D3, E, E); check('with the control and the 1,000-point triangles missing, Q10, Q11 and Q13 are not run and Q12 is judged', v == {'Q10': None, 'Q11': None, 'Q12': True, 'Q13': None})
print('%d passed, %d failed' % (npass, nfail)); sys.exit(1 if nfail else 0)
