"""Score the second sealed sheet by its letter. usage: elite_score.py RUN.json"""
import sys, json
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical
R = json.load(open(sys.argv[1]))
T = ([1, 1, 0], [[0, 1], [0, 2], [2, 0]])
HS = tuple(repr(canonical(FSM(st, *T)))[1:-1].split(' ', 2)[2] for st in (0, 1, 2))
cell = {r: [x for x in R if x['rate'] == r] for r in (0.0, 0.01, 0.02, 0.04)}
w = {r: sum(x['top_is_alld'] for x in c) for r, c in cell.items()}
pay = {r: sum(x['payoff'] for x in c) / len(c) for r, c in cell.items()}
coop = {r: sum(x['coop'] for x in c) / len(c) for r, c in cell.items()}
hs = sum(any(h in x['top'] for h in HS) for x in R)
print('error rate: runs, all-defect commonest, mean payoff, cooperation, runs led by an open-loop machine')
for r, c in cell.items(): print(f'  {r:.2f}: {len(c)}  {w[r]:2d}  {pay[r]:.3f}  {coop[r]:.3f}  {sum(x["top_open_loop"] for x in c):2d}')
print('runs led by the handshake at any entry:', hs)
res = dict(D1=w[0.04] >= 24, D2=13 <= w[0.02] <= 25, D3=10 <= w[0.01] <= 24, D4=w[0.0] <= 10, D5=w[0.0] <= w[0.01] <= w[0.02] <= w[0.04],
           D6=pay[0.0] > pay[0.01] > pay[0.02] > pay[0.04], D7=coop[0.01] < coop[0.0] and coop[0.02] < coop[0.0], D8=hs <= 1)
odds = dict(D1=.85, D2=.80, D3=.75, D4=.85, D5=.70, D6=.90, D7=.90, D8=.85)
for k in sorted(res): print(k, f'{int(odds[k] * 100)}%', 'held' if res[k] else 'FAILED')
print(sum(res.values()), 'of', len(res), 'held; Brier', round(sum((odds[k] - (1 if res[k] else 0)) ** 2 for k in res) / len(res), 4), '(always saying 50%: 0.25)')
