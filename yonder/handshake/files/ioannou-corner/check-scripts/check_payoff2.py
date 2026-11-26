"""Reader's check of corner.payoff2 by two routes of the reader's own.

Route A (exact, no linear solve, no numpy tables): carry the probability distribution over the pair of
states forward round by round in plain Python, enumerating intended move, slip of each player and misreading
by each player explicitly, and add up delta**t times the expected payoff and cooperation of round t.
Route B (simulation): play many games move by move with a random number for every slip, every misreading and
every "does the game go on", and average total payoff times (1 - delta).

usage: python -I -B check_payoff2.py
"""
import sys, itertools, math, random
import numpy as np
sys.path.insert(0, '/home/agent3/welch-prior/corner')
sys.dont_write_bytecode = True
import corner
from corner import payoff2
from ipd import FSM

PAYOFF = {(0, 0): 3.0, (0, 1): 0.0, (1, 0): 5.0, (1, 1): 1.0}   # (my move, their move) -> my payoff; 0 = C, 1 = D

def as_lists(m):
    return int(m.start), [int(x) for x in m.play], [[int(v) for v in row] for row in m.nxt]

def forward(a, b, e_move, e_read, delta, tol=1e-13):
    sa, pa, na = as_lists(a); sb, pb, nb = as_lists(b)
    dist = {(sa, sb): 1.0}; w = 1.0 - delta; ua = ub = ca = cb = 0.0; t = 0
    while w > tol * (1 - delta):
        new = {}
        for (i, j), p in dist.items():
            for fx, fy, ra, rb in itertools.product((0, 1), repeat=4):
                q = p * (e_move if fx else 1 - e_move) * (e_move if fy else 1 - e_move) * (e_read if ra else 1 - e_read) * (e_read if rb else 1 - e_read)
                if q == 0.0: continue
                x = pa[i] ^ fx; y = pb[j] ^ fy                    # moves as they come out
                ua += w * q * PAYOFF[(x, y)]; ub += w * q * PAYOFF[(y, x)]
                ca += w * q * (x == 0); cb += w * q * (y == 0)
                k = (na[i][y ^ ra], nb[j][x ^ rb])               # each moves on by what it read
                new[k] = new.get(k, 0.0) + q
        dist = new; w *= delta; t += 1
    return ua, ub, ca, cb

def simulate(a, b, e_move, e_read, delta, games, seed):
    """Many games at once, but each round every game gets its own five random numbers."""
    rng = np.random.default_rng(seed)
    play_a = np.array(as_lists(a)[1]); nxt_a = np.array(as_lists(a)[2]); play_b = np.array(as_lists(b)[1]); nxt_b = np.array(as_lists(b)[2])
    sa = np.full(games, a.start); sb = np.full(games, b.start); alive = np.ones(games, bool)
    PAYM = np.array([[3.0, 0.0], [5.0, 1.0]])
    tot = np.zeros((games, 4))
    while alive.any():
        n = int(alive.sum()); idx = np.flatnonzero(alive)
        x = play_a[sa[idx]] ^ (rng.random(n) < e_move); y = play_b[sb[idx]] ^ (rng.random(n) < e_move)
        tot[idx, 0] += PAYM[x, y]; tot[idx, 1] += PAYM[y, x]; tot[idx, 2] += (x == 0); tot[idx, 3] += (y == 0)
        seen_by_a = y ^ (rng.random(n) < e_read); seen_by_b = x ^ (rng.random(n) < e_read)
        sa[idx] = nxt_a[sa[idx], seen_by_a]; sb[idx] = nxt_b[sb[idx], seen_by_b]
        alive[idx] = rng.random(n) < delta
    per_game = tot * (1 - delta)
    return per_game.mean(0), per_game.std(0, ddof=1) / math.sqrt(games)

def M(start, spec):
    return FSM(start, [{'C': 0, 'D': 1}[p] for p, _, _ in spec], [[c, d] for _, c, d in spec])

NAMED = {
 'all-defect': M(0, [('D', 0, 0)]),
 'all-cooperate': M(0, [('C', 0, 0)]),
 'tit-for-tat': M(0, [('C', 0, 1), ('D', 0, 1)]),
 'grim': M(0, [('C', 0, 1), ('D', 1, 1)]),
 'Pavlov': M(0, [('C', 0, 1), ('D', 1, 0)]),
 'handshake': M(0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)]),
 'tit-for-two-tats': M(0, [('C', 0, 1), ('C', 0, 2), ('D', 0, 2)]),
}

if __name__ == '__main__':
    # 0. hand cases
    for e in (0.0, 0.02, 0.04):
        got = payoff2(NAMED['all-defect'], NAMED['all-defect'], e, e, 0.995)
        want = (1 - e) ** 2 * 1 + (1 - e) * e * 5 + e * (1 - e) * 0 + e * e * 3
        print(f'all-defect against itself at {e}: payoff2 {got[0]:.6f}, by hand {want:.6f}; cooperation {got[2]:.4f} (by hand {e})')
    # a case where misreading must matter and the two players differ: grim against all-cooperate, no slips, misreading r.
    # grim leaves cooperation the first time it misreads; survival of cooperation to round t is (1-r)^t.
    r, d = 0.03, 0.9
    got = payoff2(NAMED['grim'], NAMED['all-cooperate'], 0.0, r, d)
    coop_grim = (1 - d) / (1 - d * (1 - r))            # sum (1-d) d^t (1-r)^t
    print(f'grim against all-cooperate, misreading {r}, no slips, delta {d}: grim cooperates {got[2]:.6f} (by hand {coop_grim:.6f}); '
          f'payoffs {got[0]:.6f}, {got[1]:.6f} (by hand {3 * coop_grim + 5 * (1 - coop_grim):.6f}, {3 * coop_grim:.6f})')
    # 1. exact forward route: named pairs and random machines, unequal error rates so the two kinds cannot be swapped unnoticed
    worst = 0.0; n = 0
    names = list(NAMED)
    for na_, nb_ in itertools.product(names, names):
        for (em, er, dl) in ((0.02, 0.02, 0.995), (0.04, 0.0, 0.99), (0.0, 0.05, 0.9), (0.03, 0.07, 0.95), (0.0, 0.0, 0.9)):
            x = payoff2(NAMED[na_], NAMED[nb_], em, er, dl); y = forward(NAMED[na_], NAMED[nb_], em, er, dl)
            worst = max(worst, max(abs(p - q) for p, q in zip(x, y))); n += 1
    print(f'forward route against payoff2, {n} cases of named pairs: largest difference {worst:.2e}')
    rng = np.random.default_rng(20261125); worst = 0.0; n = 0
    for _ in range(60):
        k1, k2 = int(rng.integers(1, 5)), int(rng.integers(1, 5))
        a = FSM(int(rng.integers(k1)), rng.integers(0, 2, k1), rng.integers(0, k1, (k1, 2)))
        b = FSM(int(rng.integers(k2)), rng.integers(0, 2, k2), rng.integers(0, k2, (k2, 2)))
        em, er, dl = float(rng.choice([0, 0.01, 0.02, 0.04, 0.1])), float(rng.choice([0, 0.01, 0.02, 0.04, 0.1])), float(rng.choice([0.9, 0.95, 0.98]))
        x = payoff2(a, b, em, er, dl); y = forward(a, b, em, er, dl)
        worst = max(worst, max(abs(p - q) for p, q in zip(x, y))); n += 1
    print(f'forward route against payoff2, {n} random pairs of machines with 1 to 4 states (start anywhere): largest difference {worst:.2e}')
    for _ in range(6):
        a, b = corner.random_machine(rng), corner.random_machine(rng)
        x = payoff2(a, b, 0.02, 0.02, 0.98); y = forward(a, b, 0.02, 0.02, 0.98)
        worst = max(worst, max(abs(p - q) for p, q in zip(x, y)))
    print(f'  and with six pairs of the run\'s own random eight-state machines at delta 0.98: largest difference so far {worst:.2e}')
    # 2. simulation at the run's own settings
    print('simulation, move by move, 40,000 games a pair; z = (simulated - payoff2) / standard error, for payoff a, payoff b, cooperation a, cooperation b')
    zs = []
    pairs = [('handshake', 'handshake'), ('handshake', 'all-defect'), ('tit-for-tat', 'Pavlov'), ('grim', 'tit-for-two-tats'), ('Pavlov', 'all-cooperate'), ('tit-for-tat', 'handshake')]
    for s, (na_, nb_) in enumerate(pairs):
        for (em, er, dl) in ((0.02, 0.02, 0.995), (0.04, 0.04, 0.995), (0.01, 0.05, 0.98)):
            ex = payoff2(NAMED[na_], NAMED[nb_], em, er, dl); mean, se = simulate(NAMED[na_], NAMED[nb_], em, er, dl, 40000, 1000 + 17 * s + int(1000 * em))
            z = [(m - e) / s_ if s_ > 0 else 0.0 for m, e, s_ in zip(mean, ex, se)]; zs += z
            print(f'  {na_:>16s} v {nb_:<16s} slips {em} misreadings {er} delta {dl}: payoff2 {ex[0]:.4f} {ex[1]:.4f} {ex[2]:.4f} {ex[3]:.4f}; simulated {mean[0]:.4f} {mean[1]:.4f} {mean[2]:.4f} {mean[3]:.4f}; z ' + ' '.join(f'{v:+.1f}' for v in z))
    zs = np.array(zs); print(f'{len(zs)} z-scores: mean {zs.mean():+.2f}, sd {zs.std():.2f}, largest |z| {np.abs(zs).max():.2f}')
