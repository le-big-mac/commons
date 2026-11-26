"""Reader's check of corner.open_loop on canonical machines against two definitions of the reader's own:
(a) the product construction (no two input histories lead to different intended moves), and
(b) brute force: the intended moves over 10 rounds are the same for all 2**9 input histories.
usage: python -I -B check_openloop.py"""
import sys, itertools
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner
from evolve import mutate

def by_product(m):
    seen = set(); todo = [(m.start, m.start)]
    while todo:
        s, t = todo.pop()
        if (s, t) in seen: continue
        seen.add((s, t))
        if m.play[s] != m.play[t]: return False
        for a in (0, 1):
            for b in (0, 1): todo.append((int(m.nxt[s][a]), int(m.nxt[t][b])))
    return True
def by_brute(m, rounds=10):
    outs = set()
    for hist in itertools.product((0, 1), repeat=rounds - 1):
        s = m.start; o = [int(m.play[s])]
        for a in hist: s = int(m.nxt[s][a]); o.append(int(m.play[s]))
        outs.add(tuple(o))
    return len(outs) == 1
rng = np.random.default_rng(7); n = 0; bad = 0; opens = 0
for _ in range(1500):
    m = corner.random_machine(rng)
    for _ in range(int(rng.integers(0, 6))): m = mutate(m, rng)
    a, b, c = corner.open_loop(m), by_product(m), by_brute(m)
    n += 1; opens += a; bad += not (a == b == c)
print(f'{n} canonical machines (random eight-state ones, some mutated up to five times): {opens} open-loop by corner.open_loop; disagreements with either of the reader\'s definitions: {bad}')
