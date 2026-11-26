"""Second reader: the played-out tournament of replay.py (vectorised) against one written again move by move in plain Python, and
against exact 200-round payoffs: mean and spread of each machine's score over repeated tournaments of one population.
usage: python -I -B played_check.py"""
import sys, random
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner/check-2-scripts')
import replay, elite
PAYOFF = {(0, 0): 3, (0, 1): 0, (1, 0): 5, (1, 1): 1}            # (my move, the other's move), 0 = cooperate
def match(A, B, e, rnd, T=200):
    sa, sb = A[2], B[2]; ua = ub = 0
    for _ in range(T):
        xa = int(A[0][sa]); xb = int(B[0][sb])
        if rnd.random() < e: xa = 1 - xa                         # the move comes out wrong
        if rnd.random() < e: xb = 1 - xb
        ua += PAYOFF[(xa, xb)]; ub += PAYOFF[(xb, xa)]
        seen_by_a = 1 - xb if rnd.random() < e else xb           # the other's move is misread
        seen_by_b = 1 - xa if rnd.random() < e else xa
        sa = int(A[1][sa][seen_by_a]); sb = int(B[1][sb][seen_by_b])
    return ua / T, ub / T
def tournament(pop, e, rnd):
    score = [0.0] * 30
    for i in range(30):
        for j in range(i, 30):
            ua, ub = match(pop[i], pop[j], e, rnd); score[i] += ua
            if j != i: score[j] += ub
    return score
for e in (0.02, 0.04):
    rng = np.random.default_rng(11); rnd = random.Random(12)
    pop = [elite.rand_string(rng) for _ in range(30)]; can = [elite.canon(s) for s in pop]
    ex = np.array([sum(replay.payoff_fixed(can[i], can[j], e)[0] for j in range(30)) for i in range(30)])
    V = np.array([replay.played(pop, e, rng)[0].sum(1) / 200 for _ in range(300)]); P = np.array([tournament(pop, e, rnd) for _ in range(300)])
    print(f'error {e}: one random population, 300 tournaments each way; scores run from {ex.min():.1f} to {ex.max():.1f}')
    print(f'   mean score, largest difference over the 30 machines: vectorised against exact {abs(V.mean(0) - ex).max():.3f}; plain against exact {abs(P.mean(0) - ex).max():.3f}; '
          f'(standard error of such a mean about {V.std(0, ddof=1).mean() / 300 ** .5:.3f})')
    print(f'   spread of one machine\'s score from tournament to tournament (s.d., mean over machines): vectorised {V.std(0, ddof=1).mean():.3f}; plain {P.std(0, ddof=1).mean():.3f}')
    print(f'   largest ratio of the two spreads over the 30 machines: {(V.std(0, ddof=1) / P.std(0, ddof=1)).max():.2f}, smallest {(V.std(0, ddof=1) / P.std(0, ddof=1)).min():.2f}')
