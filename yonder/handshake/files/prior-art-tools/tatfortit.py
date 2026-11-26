"""Binmore and Samuelson's two-state "Tat for Tit" (as Schlag 1993 draws it) in this study's game with noise: is it an
equilibrium among all machines with up to three states, as the three-state handshake is?
usage: tatfortit.py     (reads nothing; imports ipd.py from the welch study)"""
import sys, itertools
import numpy as np
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical, payoff, M

def enumerate_machines(S):
    seen = {}
    for n in range(1, S + 1):
        for play in itertools.product((0, 1), repeat=n):
            for nx in itertools.product(range(n), repeat=2 * n):
                m = canonical(FSM(0, play, np.array(nx).reshape(n, 2)))
                if m.n == n: seen.setdefault(m.key(), m)
    return list(seen.values())

ALL = enumerate_machines(3)
print(len(ALL), 'behaviourally distinct machines with up to three states (the census has 1,054)')
TFT2 = M('Tat for Tit', 0, [('D', 0, 1), ('C', 1, 0)])                       # defect until the other defects once; then cooperate until crossed
HAND = M('handshake', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)])            # defect until the other has defected twice running
ALLD = M('all-defect', 0, [('D', 0, 0)]); ALLC = M('all-cooperate', 0, [('C', 0, 0)])
DELTA = 0.99
for eps in (0.0, 0.01, 0.05, 0.10):
    print(f'\nnoise {eps}')
    for m in (TFT2, HAND):
        self_ = payoff(m, m, eps, DELTA)[0]
        gains = sorted(((payoff(x, m, eps, DELTA)[0] - self_, x) for x in ALL), key=lambda t: -t[0])
        ck = canonical(m).key()
        others = [(g, x) for g, x in gains if x.key() != ck]
        best_g, best = others[0]
        n_better = sum(1 for g, x in others if g > 1e-12); n_equal = sum(1 for g, x in others if abs(g) <= 1e-12)
        print(f'  {m.name:12s} against itself {self_:.4f}; all-defect earns {payoff(ALLD, m, eps, DELTA)[0]:.4f} against it; all-cooperate earns {payoff(ALLC, m, eps, DELTA)[0]:.4f};'
              f' machines that do better against it than it does: {n_better}, exactly as well: {n_equal}; best: {best!r} by {best_g:+.4f}')
