"""After the second sealed run (not sealed): why did my writing of the scheme and the reader's give different counts?
The two differ in how a newcomer is mutated. Mine keeps strings of exactly eight states and changes each of 25 elements with a 4%
chance (his paper's way; about a third of newcomers come out unchanged, and changes in unused states are kept). The reader's
minimises each machine and applies the study's mutate() once (always one change, which may add or remove a state).
Here my script is run with the reader's kind of mutation and nothing else changed.   usage: elite_after.py OUT.json"""
import sys, json, time
from collections import Counter
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, '/home/agent3/welch-prior/corner'); sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical
from evolve import mutate
from corner import payoff2, open_loop, ALLD
import elite

def run(args):
    rate, seed, gens = args
    rng = np.random.default_rng(seed)
    can = [elite.canon(elite.rand_string(rng)) for _ in range(30)]
    cache = {}
    def pay(a, b):
        k = (a.key(), b.key()); v = cache.get(k)
        if v is None:
            ua, ub, ca, cb = payoff2(a, b, rate, rate, 0.995); cache[k] = v = (ua, ca); cache[(b.key(), a.key())] = (ub, cb)
        return v
    occ, pay_tail, coop_tail = Counter(), [], []; kept = {}
    for g in range(gens):
        score = np.zeros(30); coop = np.zeros(30)
        for i in range(30):
            for j in range(30):
                u, c = pay(can[i], can[j]); score[i] += u; coop[i] += c
        if g >= gens - 100:
            pay_tail.append(float(score.mean() / 30)); coop_tail.append(float(coop.mean() / 30))
            for m in can: occ[m.key()] += 1; kept[m.key()] = m
        order = np.argsort(-score, kind='stable'); best = [int(i) for i in order[:20]]
        p = score / score.sum(); new = []
        for _ in range(10):
            a, b = rng.choice(30, 2, p=p); w = a if score[a] >= score[b] else b
            new.append(canonical(mutate(can[w], rng)))                       # the reader's kind of mutation: one change to the minimised machine
        can = [can[i] for i in best] + new
        if g % 25 == 24:
            live = {m.key() for m in can}; cache = {k: v for k, v in cache.items() if k[0] in live and k[1] in live}
    topk, topc = occ.most_common(1)[0]; top = kept[topk]
    return dict(rate=rate, seed=seed, gens=gens, top=repr(top), top_is_alld=bool(topk == ALLD.key()), top_open_loop=bool(open_loop(top)),
                top_share=topc / sum(occ.values()), payoff=float(np.mean(pay_tail)), coop=float(np.mean(coop_tail)))

if __name__ == '__main__':
    J = [(r, 8000000 + 1000 * k + s, 500) for k, r in enumerate(elite.RATES) for s in range(30)]; t = time.time()
    with Pool(14) as p: res = p.map(run, J, chunksize=1)
    json.dump(res, open(sys.argv[1], 'w'))
    T = ([1, 1, 0], [[0, 1], [0, 2], [2, 0]]); HS = tuple(repr(canonical(FSM(st, *T)))[1:-1].split(' ', 2)[2] for st in (0, 1, 2))
    print(len(res), 'runs in', round(time.time() - t), 's; my script with the reader\'s kind of mutation')
    print('error rate: all-defect commonest of 30, mean payoff, cooperation, runs led by the handshake at any entry')
    for r in elite.RATES:
        c = [x for x in res if x['rate'] == r]
        print(f'  {r:.2f}: {sum(x["top_is_alld"] for x in c):2d}  {sum(x["payoff"] for x in c) / 30:.3f}  {sum(x["coop"] for x in c) / 30:.3f}  {sum(any(h in x["top"] for h in HS) for x in c)}')
