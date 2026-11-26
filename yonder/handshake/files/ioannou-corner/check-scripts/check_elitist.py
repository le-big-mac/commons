"""Reader's side run (not sealed, checked by nobody): the selection scheme of Ioannou's section 4 as the reader reads
it, put on the corner's machinery, to see whether the difference "no keeping of the best twenty" matters.

Each generation: every one of the 30 machines is scored by its exact payoff against all thirty (the other 29 and its
twin); the 20 best are copied unchanged (ties broken at random); ten pairs are drawn from the parents with chances in
proportion to score, and the better of each pair is copied and mutated once with the study's mutate(). Start: 30
random eight-state machines. 500 generations. Errors of both kinds at the stated rate. Measures as in corner.py: over
the last 100 generations, the commonest machine by individual-generations, and the share of cooperative moves.
Still not his algorithm: payoffs are exact where his are played out once over 200 periods, games end at random with
mean 200 rounds, machines are minimised and mutated by the study's operator, not as strings of eight states.

usage: python -I -B check_elitist.py OUT.json [PROCESSES]"""
import sys, json, time
from multiprocessing import Pool
from collections import Counter
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, '/home/agent3/welch-prior/corner')
import corner
from evolve import mutate

def run(args):
    e, seed, gens, p_mut = args
    rng = np.random.default_rng(seed); delta = 0.995; N = 30
    types = {}; pop = []
    for _ in range(N):
        m = corner.random_machine(rng); types.setdefault(m.key(), m); pop.append(m.key())
    memo = {}
    def pay(ka, kb):
        if (ka, kb) not in memo:
            ua, ub, ca, cb = corner.payoff2(types[ka], types[kb], e, e, delta)
            memo[(ka, kb)] = (ua, ca); memo[(kb, ka)] = (ub, cb)
        return memo[(ka, kb)]
    occ = Counter(); coop = []; mean_pay = []
    for g in range(gens):
        cnt = Counter(pop); keys = list(cnt)
        score = {k: sum(c * pay(k, k2)[0] for k2, c in cnt.items()) for k in keys}          # against all thirty, twin included
        if g >= gens - 100:
            for k, c in cnt.items(): occ[k] += c
            coop.append(sum(c1 * c2 * pay(k1, k2)[1] for k1, c1 in cnt.items() for k2, c2 in cnt.items()) / N ** 2)
            mean_pay.append(sum(cnt[k] * score[k] for k in keys) / N ** 2)
        s = np.round(np.array([score[k] for k in pop]), 8)                                 # exact ties (common at zero error) must rank as ties,
                                                                                            # not by the last place of the arithmetic
        order = rng.permutation(N); order = order[np.argsort(-s[order], kind='stable')]     # best first, ties in random order
        new = [pop[i] for i in order[:20]]
        p = s / s.sum() if s.sum() > 0 else np.full(N, 1 / N)
        for _ in range(10):
            i, j = rng.choice(N, size=2, p=p)
            w = pop[i] if s[i] >= s[j] else pop[j]
            if rng.random() < p_mut:
                child = mutate(types[w], rng); types.setdefault(child.key(), child); new.append(child.key())
            else: new.append(w)
        pop = new
        if g % 50 == 49:
            live = set(pop) | set(occ)
            memo = {kk: v for kk, v in memo.items() if kk[0] in live and kk[1] in live}; types = {k: v for k, v in types.items() if k in live}
    total = sum(occ.values()); topk, topc = occ.most_common(1)[0]; top = types[topk]
    return dict(e=e, seed=seed, gens=gens, p_mut=p_mut, coop=float(np.mean(coop)), payoff=float(np.mean(mean_pay)), top=repr(top), top_share=topc / total,
                top_is_alld=bool(topk == corner.ALLD.key()), top_open_loop=bool(corner.open_loop(top)),
                alld_share=occ.get(corner.ALLD.key(), 0) / total)

if __name__ == '__main__':
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    J = []
    for p_mut in (1.0, 0.64):                       # all ten newcomers mutated (his Figure 3), or 64% of them (4% a element over 25 elements)
        for e in (0.0, 0.01, 0.02, 0.04):
            for s in range(30): J.append((e, 8000000 + 1000 * len(J) + s, 500, p_mut))
    t = time.time()
    with Pool(procs) as p: res = p.map(run, J, chunksize=1)
    json.dump(res, open(sys.argv[1], 'w'))
    print(len(res), 'runs in', round(time.time() - t), 's')
    print('newcomers mutated; error rate: all-defect commonest (of 30); led by an open-loop machine; mean cooperation; mean payoff; mean all-defect share; commonest leaders')
    k = 0
    for p_mut in (1.0, 0.64):
        for e in (0.0, 0.01, 0.02, 0.04):
            c = res[k:k + 30]; k += 30
            lead = Counter(x['top'][8:-1] for x in c).most_common(4)
            print(f'  {p_mut:.2f}; {e:.2f}: {sum(x["top_is_alld"] for x in c):2d};  {sum(x["top_open_loop"] for x in c):2d};  {sum(x["coop"] for x in c) / 30:.3f};  {sum(x["payoff"] for x in c) / 30:.3f};  {sum(x["alld_share"] for x in c) / 30:.3f};  {lead}')
