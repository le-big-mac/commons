"""Second reader: count the leaders of the sealed second run from elite_run.json, cell by cell, by exact match of the minimised machine
(not by substring), and the scatter of payoff and cooperation between runs.   usage: python -I -B count_leaders.py RUN.json"""
import sys, json
from collections import Counter
import numpy as np
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical
R = json.load(open(sys.argv[1]))
T = ([1, 1, 0], [[0, 1], [0, 2], [2, 0]])                      # 0: D (C->0, D->1); 1: D (C->0, D->2); 2: C (C->2, D->0)
HS = {repr(canonical(FSM(st, *T))): st for st in (0, 1, 2)}
for k, st in HS.items(): print('handshake entered at state', st, 'is', k)
ALLD = repr(canonical(FSM(0, [1], [[0, 0]]))); ALLC = repr(canonical(FSM(0, [0], [[0, 0]])))
tot = 0
for rate in (0.0, 0.01, 0.02, 0.04):
    c = [x for x in R if x['rate'] == rate]; tops = Counter(x['top'] for x in c)
    hs = {st: sum(x['top'] == k for x in c) for k, st in HS.items()}; tot += sum(hs.values())
    sub = sum(any(k[8:-1] in x['top'] for k in HS) for x in c)   # the score script's way, by substring
    pay = np.array([x['payoff'] for x in c]); coop = np.array([x['coop'] for x in c])
    print(f'\nerror {rate:.2f}: {len(c)} runs; all-defect commonest in {tops[ALLD]} (flag in file: {sum(x["top_is_alld"] for x in c)}); all-cooperate in {tops[ALLC]}')
    print(f'   handshake by entry state {hs}, together {sum(hs.values())} (by substring: {sub})')
    print(f'   mean payoff {pay.mean():.3f} (s.d. between runs {pay.std(ddof=1):.3f}, standard error {pay.std(ddof=1) / len(c) ** .5:.3f}; lowest {pay.min():.2f}, highest {pay.max():.2f})')
    print(f'   cooperation {coop.mean():.3f} (s.d. {coop.std(ddof=1):.3f}, standard error {coop.std(ddof=1) / len(c) ** .5:.3f})')
    print(f'   share of the commonest machine: mean {np.mean([x["top_share"] for x in c]):.2f}, lowest {min(x["top_share"] for x in c):.2f}; {len(tops)} different leaders; leaders with more than one run:')
    for k, v in tops.most_common():
        if v > 1 or k in HS or k == ALLD: print(f'      {v:2d}  {k}' + ('   <- handshake, entry %d' % HS[k] if k in HS else ''))
print('\nhandshake at any entry, all 120 runs:', tot)
