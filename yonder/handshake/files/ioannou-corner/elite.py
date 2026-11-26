"""Ioannou's selection scheme, written from section 4 of his discussion paper, on this folder's exact payoffs with errors of two kinds.
Thirty machines of exactly eight states, random at the start. Each generation every machine plays every other machine and its own twin;
the twenty best scorers pass unchanged; ten newcomers are made by drawing ten pairs from the parents (chances in proportion to score),
taking the better of each pair, and mutating it: each of its 25 elements (eight moves, sixteen arrows, the start state) changes with a
4% chance. 500 generations. Not his: payoffs are exact where his are played out, and games end at random after 200 rounds on average.

usage: elite.py trial | elite.py run OUT.json      (under -I)"""
import sys, json, time
from collections import Counter
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, '/home/agent3/welch-prior/corner'); sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical
from corner import payoff2, open_loop, ALLD

S = 8
def rand_string(rng): return [rng.integers(0, 2, S), rng.integers(0, S, (S, 2)), int(rng.integers(0, S))]
def mutate_string(st, rng):
    play, nxt, start = st[0].copy(), st[1].copy(), st[2]
    for i in range(S):
        if rng.random() < 0.04: play[i] ^= 1
        for a in (0, 1):
            if rng.random() < 0.04: nxt[i, a] = (nxt[i, a] + rng.integers(1, S)) % S        # a different state
    if rng.random() < 0.04: start = int((start + rng.integers(1, S)) % S)
    return [play, nxt, start]
def canon(st): return canonical(FSM(st[2], st[0], st[1]))

def run(args):
    rate, seed, gens = args
    rng = np.random.default_rng(seed)
    pop = [rand_string(rng) for _ in range(30)]; can = [canon(s) for s in pop]
    cache = {}
    def pay(a, b):
        k = (a.key(), b.key()); v = cache.get(k)
        if v is None:
            ua, ub, ca, cb = payoff2(a, b, rate, rate, 0.995)
            cache[k] = v = (ua, ca); cache[(b.key(), a.key())] = (ub, cb)
        return v
    occ, pay_tail, coop_tail = Counter(), [], []; kept = {}
    for g in range(gens):
        score = np.zeros(30); coop = np.zeros(30)
        for i in range(30):
            for j in range(30):                       # j == i is the match against its own twin
                u, c = pay(can[i], can[j]); score[i] += u; coop[i] += c
        if g >= gens - 100:
            pay_tail.append(float(score.mean() / 30)); coop_tail.append(float(coop.mean() / 30))
            for m in can: occ[m.key()] += 1; kept[m.key()] = m
        order = np.argsort(-score, kind='stable'); best = [int(i) for i in order[:20]]
        p = score / score.sum(); new = []
        for _ in range(10):
            a, b = rng.choice(30, 2, p=p)             # a pair from the parents, chances in proportion to score
            w = a if score[a] >= score[b] else b
            new.append(mutate_string(pop[w], rng))
        pop = [pop[i] for i in best] + new; can = [can[i] for i in best] + [canon(s) for s in new]
        if g % 25 == 24:
            live = {m.key() for m in can}; cache = {k: v for k, v in cache.items() if k[0] in live and k[1] in live}
    topk, topc = occ.most_common(1)[0]; top = kept[topk]
    return dict(rate=rate, seed=seed, gens=gens, top=repr(top), top_is_alld=bool(topk == ALLD.key()), top_open_loop=bool(open_loop(top)),
                top_share=topc / sum(occ.values()), alld_share=occ.get(ALLD.key(), 0) / sum(occ.values()), payoff=float(np.mean(pay_tail)), coop=float(np.mean(coop_tail)))

RATES = (0.0, 0.01, 0.02, 0.04)
if __name__ == '__main__':
    if sys.argv[1] == 'trial':
        rng = np.random.default_rng(5); st = rand_string(rng); n = 0; ch = 0
        for _ in range(4000):
            m = mutate_string(st, rng); d = int((m[0] != st[0]).sum() + (m[1] != st[1]).sum() + (m[2] != st[2])); n += d; ch += d > 0
        print(f'mutation: {n / 4000:.3f} elements changed per string on average (25 x 0.04 = 1); {ch / 4000:.3f} of strings changed at all (1 - 0.96^25 = {1 - 0.96 ** 25:.3f})')
        t = time.time(); r = run((0.02, 12345, 12)); print('one run of 12 generations in %.1f s; fields:' % (time.time() - t), sorted(r))
    else:
        J = [(r, 7000000 + 1000 * k + s, 500) for k, r in enumerate(RATES) for s in range(30)]; t = time.time()
        with Pool(14) as p: res = p.map(run, J, chunksize=1)
        json.dump(res, open(sys.argv[2], 'w')); print(len(res), 'runs in', round(time.time() - t), 's')
