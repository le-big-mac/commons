"""Score the sealed sheet by its letter. usage: corner_score.py RUN.json"""
import sys, json
from collections import defaultdict
R = json.load(open(sys.argv[1]))
# the zero-error cells of the two kinds are separate runs with the same settings: tell them apart by job order (seed // 1000 is the job index)
cell = defaultdict(list)
for r in R:
    j = r['seed'] // 1000; kind = 'both' if (j // 120) % 2 == 1 else 'move'      # jobs: start (240) > kind (120) > rate (30)
    cell[(r['start'], kind, r['e_move'])].append(r)
def wins(c): return sum(1 for r in c if r['top_is_alld'])
def coop(c): return sum(r['coop'] for r in c) / len(c)
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical
T = ([1, 1, 0], [[0, 1], [0, 2], [2, 0]])                                   # the three-state table: defect, defect, cooperate
HS = tuple(repr(canonical(FSM(st, *T)))[1:-1].split(' ', 2)[2] for st in (0, 1, 2))   # entered at each of its three states, in the study's canonical form
print('the handshake at its three entries:', HS)
print('cell (start, kind, rate): runs, all-defect wins, mean cooperation, runs led by an open-loop machine, runs led by a handshake')
for k in sorted(cell):
    c = cell[k]; print(f'  {k[0]:6s} {k[1]:4s} {k[2]:.2f}: {len(c)}  {wins(c):2d}  {coop(c):.3f}  {sum(1 for r in c if r["top_open_loop"]):2d}  {sum(1 for r in c if any(h in r["top"] for h in HS))}')
res = {}
res['C1'] = wins(cell[('random', 'both', 0.04)]) >= 20
res['C2'] = wins(cell[('random', 'both', 0.02)]) >= 15
res['C3'] = wins(cell[('random', 'both', 0.01)]) >= 12 and wins(cell[('random', 'both', 0.0)]) >= 12
res['C4'] = all(wins(cell[(s, k, 0.04)]) >= wins(cell[(s, k, 0.0)]) for s in ('alld', 'random') for k in ('move', 'both'))
res['C5'] = all(coop(c) < 0.35 for c in cell.values())
res['C6'] = sum(1 for r in R if any(h in r['top'] for h in HS)) <= 2
res['C7'] = all(abs(wins(cell[('alld', k, e)]) - wins(cell[('random', k, e)])) <= 8 for k in ('move', 'both') for e in (0.0, 0.01, 0.02, 0.04))
odds = dict(C1=.80, C2=.65, C3=.60, C4=.70, C5=.55, C6=.80, C7=.60)
for k in sorted(res): print(k, f'{int(odds[k] * 100)}%', 'held' if res[k] else 'FAILED')
print(sum(res.values()), 'of', len(res), 'held; Brier', round(sum((odds[k] - (1 if res[k] else 0)) ** 2 for k in res) / len(res), 4), '(always saying 50%: 0.25)')
