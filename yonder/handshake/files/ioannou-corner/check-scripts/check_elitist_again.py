"""Reader's second writing of the side run in check_elitist.py, individual by individual and in a different order of
draws, to guard against a slip in the first. Not sealed, checked by nobody.
usage: python -I -B check_elitist_again.py [PROCESSES]"""
import sys, random
from multiprocessing import Pool
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner
from evolve import mutate

def run(args):
    e, seed = args
    rng = np.random.default_rng(seed); pyr = random.Random(seed)
    pop = [corner.random_machine(rng) for _ in range(30)]                 # thirty individuals, each a machine
    memo = {}
    def u(a, b):                                                          # payoff and cooperation of a against b
        k = (a.key(), b.key())
        if k not in memo:
            ua, ub, ca, cb = corner.payoff2(a, b, e, e, 0.995); memo[k] = (ua, ca); memo[(k[1], k[0])] = (ub, cb)
        return memo[k]
    tally = {}; coop = []
    for g in range(500):
        scores = [round(sum(u(a, b)[0] for b in pop), 8) for a in pop]    # the 29 others and a twin of itself; rounded so that exact ties rank as ties
        assert len(pop) == 30
        if g >= 400:
            for a in pop: tally[repr(a)] = tally.get(repr(a), 0) + 1
            coop.append(sum(u(a, b)[1] for a in pop for b in pop) / 900)
        ranked = sorted(range(30), key=lambda i: (-scores[i], pyr.random()))
        keep = [pop[i] for i in ranked[:20]]
        assert min(scores[i] for i in ranked[:20]) >= max(scores[i] for i in ranked[20:]) - 1e-12
        newcomers = []
        for _ in range(10):
            i = pyr.choices(range(30), weights=scores)[0]; j = pyr.choices(range(30), weights=scores)[0]
            better = pop[i] if scores[i] >= scores[j] else pop[j]
            newcomers.append(mutate(better, rng))
        pop = keep + newcomers
        if g % 50 == 49:
            live = {a.key() for a in pop}; memo = {k: v for k, v in memo.items() if k[0] in live and k[1] in live}
    top = max(tally, key=tally.get)
    return e, top, float(np.mean(coop))

if __name__ == '__main__':
    procs = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    J = [(e, 8800000 + 1000 * i + s) for i, e in enumerate((0.0, 0.01, 0.02, 0.04)) for s in range(30)]
    with Pool(procs) as p: res = p.map(run, J, chunksize=1)
    for e in (0.0, 0.01, 0.02, 0.04):
        c = [r for r in res if r[0] == e]
        print(f'second writing, all ten newcomers mutated, errors {e:.2f}: all-defect commonest in {sum(r[1] == "<fsm s0 0:D[0,0]>" for r in c)} of {len(c)}; mean cooperation {sum(r[2] for r in c) / len(c):.3f}')
