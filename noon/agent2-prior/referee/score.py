"""Referee: the scorecard by the letter with the blind classes; the Dupuy table pooled; half.py's four nearby attitudes by closed form.
usage: python -I score.py"""
import itertools, numpy as np
odds = dict(W1=.25, W2=.15, W3=.60, W4=.85, W5=.55, W6=.35, W7=.92, W8=.85, W9=.80, W10=.95, W11=.65, W12=.60, W13=.93, W14=.95, W15=.85, W16=.40)
mark = dict(W1='g', W2='g', W3='r', W4='r', W5='g', W6='g', W7='r', W8='r', W9='r', W10='r', W11='g', W12='g', W13='r', W14='r', W15='r', W16='g')
F, P, N = 'found', 'found in part', 'not found'
author = dict(W1=N, W2=N, W3=F, W4=F, W5=P, W6=N, W7=F, W8=F, W9=F, W10=F, W11=P, W12=N, W13=F, W14=F, W15=F, W16=P)
blind = dict(author, W1=P, W7=P, W15=P)
val = {F: 1.0, P: 0.5, N: 0.0}
def card(c, name):
    v = {k: val[c[k]] for k in c}; tot = sum(v.values()); w17 = 1.0 if tot >= 10 else 0.0
    br = (sum((odds[k] - v[k]) ** 2 for k in c) + (0.60 - w17) ** 2) / 17; flat = (sum((0.5 - v[k]) ** 2 for k in c) + (0.5 - w17) ** 2) / 17
    cnt = lambda m, x: sum(1 for k in c if mark[k] == m and c[k] == x)
    print(f"{name}: found {sum(x == F for x in c.values())}, in part {sum(x == P for x in c.values())}, not found {sum(x == N for x in c.values())}; W17 total {tot} ({'holds' if w17 else 'fails'}); Brier {br:.4f}; flat 0.5: {flat:.4f}")
    print(f"   remembered (9): found {cnt('r', F)}, part {cnt('r', P)}, not {cnt('r', N)};  guessed (7): found {cnt('g', F)}, part {cnt('g', P)}, not {cnt('g', N)}")
card(author, "author's classes"); card(blind, "referee's blind classes")
card(dict(blind, W3=P, W15=F), "blind, then W3 down and W15 up after reading the sources")
card(dict(blind, W3=P), "blind, then W3 down only")
# the Dupuy Institute table, all ten rows as in the saved text: (low ratio, percent attacker wins, cases)
rows = [(0.26, 54, 13), (0.50, 54, 81), (1.00, 56, 71), (1.50, 63, 38), (2.00, 50, 16), (2.58, 57, 7), (3.00, 100, 5), (3.75, 0, 2), (4.00, 75, 4), (7.78, 67, 6)]
n = sum(r[2] for r in rows); big = sum((p if lo >= 1 else 100 - p) / 100 * c for lo, p, c in rows)
att3 = sum(p / 100 * c for lo, p, c in rows if lo >= 3); n3 = sum(c for lo, p, c in rows if lo >= 3)
print(f"Dupuy table: {n} battles; larger side wins {big:.1f} of {n} = {100 * big / n:.1f}% (rows at 1.00-1.47 counted as attacker larger; no draws assumed); attackers at 3:1 or more {att3:.0f} of {n3} = {100 * att3 / n3:.1f}%")
EPS = np.array(list(itertools.product((-1, 1), repeat=3)), float); SG = EPS.prod(1)
def Ehalf(n):
    n = np.asarray(n, float); n = n / np.linalg.norm(n); h = EPS @ n / 2; return 0.5 * float((SG * np.abs(h) * h ** 3).sum() / 24 / n.prod())   # E|S| = (1/abc) sum prod(eps) G(eps.n/2), G = |t| t^3 / 24
for v in ((1, 1, 1), (0.975, 1, 1), (0.95, 0.95, 1), (0.9, 1, 1), (0.8, 0.9, 1)): print(f"closed form at density 1/2, {v}: {Ehalf(v):.10f}")
