"""Reader's checks of corner.run.

1. Against the study's own evolve.run: from the all-defect start with no misreading, corner.run should be the same
   process draw for draw. evolve.run is used as it stands except that its line "if g % 10 == 0:" is made "if True:" so
   that it reports cooperation every generation. Its occupancy counts are cumulative, so the last 100 generations are
   got as (run of 500) minus (run of 400) with the same seed.
2. A loop of the reader's own that keeps every generation's population and works the measures out afterwards
   (commonest machine over the last 100 generations by individual-generations, cooperation, open-loop by a product
   construction), compared with what corner.run returned for the same seeds.

usage: python -I -B check_run.py /home/agent3/welch-prior/corner/corner_run.json
"""
import sys, json, inspect
from collections import Counter
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner
import evolve
from ipd import FSM, canonical

R = json.load(open(sys.argv[1]))
by_seed = {r['seed']: r for r in R}
J = corner.jobs(30, 500)
assert [j[3] for j in J] == [r['seed'] for r in R], 'job order and file order differ'
for j, r in zip(J, R):
    assert (j[0], j[1], j[8], j[4], j[5]) == (r['e_move'], r['e_read'], r['start'], r['gens'], r['N'])
    assert abs(j[6] - r['mu']) < 1e-15 and j[7] == r['beta'] and j[2] == r['delta']
print('corner_run.json: 480 records in job order; settings of each record equal those of corner.jobs(30, 500)')

# ---- 1. the study's evolve.run, reporting every generation
src = inspect.getsource(evolve.run)
assert src.count('if g % 10 == 0:') == 1
ns = dict(vars(evolve)); exec(src.replace('if g % 10 == 0:', 'if True:'), ns); study_run = ns['run']
ALLD_REPR = repr(canonical(FSM(0, [1], [[0, 0]])))
def study_tail(e, seed, gens=500, N=30, mu=1 / 3):
    a = study_run((e, 0.995, seed, gens, N, mu, 1.0, 0.0)); b = study_run((e, 0.995, seed, gens - 100, N, mu, 1.0, 0.0))
    assert np.array_equal(a['series'][:gens - 100], b['series'])          # same seed, same first 400 generations
    occ_a = dict(a['occ']); occ_b = dict(b['occ'])
    alld = (occ_a.get(ALLD_REPR, 0) - occ_b.get(ALLD_REPR, 0)) / (100 * N)
    return float(a['series'][-100:, 1].mean()), alld
worst_c = worst_a = 0.0; n = 0
for j in list(range(0, 120, 7)) + [29, 59, 89, 119]:                      # all-defect start, slips only: jobs 0 to 119
    args = J[j]; assert args[8] == 'alld' and args[1] == 0.0
    c, a = study_tail(args[0], args[3]); r = R[j]
    worst_c = max(worst_c, abs(c - r['coop'])); worst_a = max(worst_a, abs(a - r['alld_share'])); n += 1
print(f'study\'s evolve.run against corner_run.json, {n} runs from the all-defect start with slips only: '
      f'largest difference in tail cooperation {worst_c:.2e}, in all-defect share of the tail {worst_a:.2e}')

# ---- 2. the reader's own loop and measures
def open_loop_by_product(m):
    """Open-loop if no two input histories can lead to different intended moves: walk pairs of states reached from
    (start, start) when the two copies are fed inputs independently; closed-loop if some pair plays differently."""
    seen = set(); todo = [(m.start, m.start)]
    while todo:
        s, t = todo.pop()
        if (s, t) in seen: continue
        seen.add((s, t))
        if m.play[s] != m.play[t]: return False
        for a in (0, 1):
            for b in (0, 1): todo.append((int(m.nxt[s][a]), int(m.nxt[t][b])))
    return True

def reader_run(args, matrix_product=True):
    e_move, e_read, delta, seed, gens, N, mu, beta, start = args
    rng = np.random.default_rng(seed); machines = {}; pop = {}
    for _ in range(N):
        m = canonical(FSM(0, [1], [[0, 0]])) if start == 'alld' else canonical(FSM(0, rng.integers(0, 2, 8), rng.integers(0, 8, (8, 2))))
        machines.setdefault(m.key(), m); pop[m.key()] = pop.get(m.key(), 0) + 1
    memo = {}
    def pay(ka, kb):
        if (ka, kb) not in memo:
            ua, ub, ca, cb = corner.payoff2(machines[ka], machines[kb], e_move, e_read, delta)
            memo[(ka, kb)] = (ua, ca); memo[(kb, ka)] = (ub, cb)
        return memo[(ka, kb)]
    history = []
    for g in range(gens):
        history.append(dict(pop))                                        # the population that plays in generation g
        keys = list(pop); freq = np.array([pop[k] for k in keys], float) / N
        U = np.array([[pay(ki, kj)[0] for kj in keys] for ki in keys])
        fit = U @ freq if matrix_product else np.array([sum(f * pay(ki, kj)[0] for kj, f in zip(keys, freq)) for ki in keys])
        w = freq * np.exp(beta * fit); w /= w.sum()
        draw = rng.multinomial(N, w)                                      # selection: N offspring, weights share x exp(payoff)
        pop = {k: int(c) for k, c in zip(keys, draw) if c > 0}
        for _ in range(rng.binomial(N, mu)):                              # then mutation, one individual at a time
            ks = list(pop); p = np.array([pop[k] for k in ks], float)
            parent = ks[rng.choice(len(ks), p=p / p.sum())]; child = evolve.mutate(machines[parent], rng)
            if child.key() == parent: continue
            pop[parent] -= 1
            if pop[parent] == 0: del pop[parent]
            machines.setdefault(child.key(), child); pop[child.key()] = pop.get(child.key(), 0) + 1
    tail = history[-100:]; occ = Counter(); coop = []
    for h in tail:
        for k, c in h.items(): occ[k] += c
        coop.append(sum(c1 * c2 * pay(k1, k2)[1] for k1, c1 in h.items() for k2, c2 in h.items()) / N ** 2)
    total = 100 * N; assert sum(occ.values()) == total
    best = max(occ.values()); leaders = [k for k, c in occ.items() if c == best]
    top = machines[leaders[0]]
    return dict(coop=float(np.mean(coop)), top=repr(top), tie=len(leaders) > 1, top_share=best / total,
                top_is_alld=bool(top.n == 1 and top.play[0] == 1), top_open_loop=open_loop_by_product(top),
                open_loop_share=sum(c for k, c in occ.items() if open_loop_by_product(machines[k])) / total,
                alld_share=sum(c for k, c in occ.items() if machines[k].n == 1 and machines[k].play[0] == 1) / total)

n = 0; bad = 0; worst = 0.0; ties = 0
picks = [0, 31, 62, 93, 120, 151, 182, 213, 240, 247, 271, 302, 333, 360, 361, 367, 391, 398, 422, 429, 453, 460, 479]
for j in picks:
    mine = reader_run(J[j]); r = R[j]; n += 1; ties += mine['tie']
    for k in ('top', 'top_is_alld', 'top_open_loop'):
        if mine[k] != r[k]: bad += 1; print('  DIFFERENT', j, k, mine[k], r[k])
    for k in ('coop', 'top_share', 'open_loop_share', 'alld_share'):
        worst = max(worst, abs(mine[k] - r[k]))
print(f'reader\'s own loop and measures against corner_run.json, {n} runs across all sixteen cells: {bad} differences in the leading machine or its flags; '
      f'largest numerical difference {worst:.2e}; runs with a tie for commonest machine: {ties}')
# The same loop with each machine's payoff added up term by term instead of by a matrix product. The two agree to the
# last place or the one before it; where payoffs are exact ties (zero error) that can tip a draw and the run goes another way.
moved = []
for j in picks:
    mine = reader_run(J[j], matrix_product=False); r = R[j]
    if abs(mine['alld_share'] - r['alld_share']) > 1e-12: moved.append((j, J[j][0], round(mine['alld_share'] - r['alld_share'], 4), mine['top_is_alld']))
print('payoffs added term by term instead: runs whose course changed (job, error rate, change in all-defect share, all-defect still commonest):', moved)
