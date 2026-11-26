"""Wright-Fisher evolution of FSM strategies in the noisy IPD."""
import sys, json, pickle, time
from collections import Counter
from multiprocessing import Pool
import numpy as np
from ipd import FSM, canonical, payoff

MAXS = 8
import os
LOGCAP = int(os.environ.get("WELCH_LOGCAP", "60"))


def mutate(m, rng):
    play = m.play.copy()
    nxt = m.nxt.copy()
    start = m.start
    n = m.n
    r = rng.random()
    if n > 1 and rng.random() < 0.1:
        start = int(rng.integers(n))
    elif r < 0.25:
        play[rng.integers(n)] ^= 1
    elif r < 0.70 or (r >= 0.85 and n == 1) or (r < 0.85 and n >= MAXS):
        nxt[rng.integers(n), rng.integers(2)] = rng.integers(n)
    elif r < 0.85:
        # add a state, hook one existing transition to it
        play = np.append(play, rng.integers(2)).astype(np.int8)
        nxt = np.vstack([nxt, rng.integers(n + 1, size=2)]).astype(np.int16)
        nxt[rng.integers(n), rng.integers(2)] = n
    else:
        # delete a state; redirect arrows into it at random
        k = rng.integers(n)
        keep = [i for i in range(n) if i != k]
        remap = {s: i for i, s in enumerate(keep)}
        play = play[keep]
        new = np.zeros((n - 1, 2), dtype=np.int16)
        for i, s in enumerate(keep):
            for a in (0, 1):
                t = int(nxt[s, a])
                new[i, a] = remap[t] if t != k else rng.integers(n - 1)
        nxt = new
        start = remap[start] if start != k else int(rng.integers(n - 1))
    return canonical(FSM(start, play, nxt))


def run(args):
    eps, delta, seed, gens, N, mu, beta, cost = args[:8]
    init = args[8] if len(args) > 8 else None
    rng = np.random.default_rng(seed)
    types = {}  # key -> FSM
    alld = canonical(init) if init is not None else canonical(FSM(0, [1], [[0, 0]]))
    types[alld.key()] = alld
    counts = Counter({alld.key(): N})
    cache = {}

    def pay(ka, kb):
        v = cache.get((ka, kb))
        if v is None:
            ua, ub, ca, cb = payoff(types[ka], types[kb], eps, delta, detail=True)
            cache[(ka, kb)] = v = (ua, ca)
            cache[(kb, ka)] = (ub, cb)
        return v

    series = []  # (gen, coop, payoff, mean states, ntypes)
    dom = Counter()  # generations each type spent as most common
    occ = Counter()  # individual-generations
    trans = Counter()  # majority type A replaced by majority type B
    last = None
    log = []
    for g in range(gens):
        keys = list(counts)
        cnt = np.array([counts[k] for k in keys], dtype=float)
        k = len(keys)
        U = np.empty((k, k))
        Cm = np.empty((k, k))
        for i in range(k):
            for j in range(k):
                U[i, j], Cm[i, j] = pay(keys[i], keys[j])
        freq = cnt / N
        fit = U @ freq
        coop = freq @ (Cm @ freq)
        top = keys[int(np.argmax(cnt))]
        dom[top] += 1
        if cnt.max() > N / 2:
            if last is not None and top != last:
                trans[(last, top)] += 1
                if len(log) < LOGCAP: log.append((g, top))
            last = top
        for kk, c in zip(keys, cnt):
            occ[kk] += int(c)
        if g % 10 == 0:
            ns = np.array([types[kk].n for kk in keys])
            series.append((g, coop, freq @ fit, freq @ ns, k))
        w = freq * np.exp(beta * (fit - cost * np.array([types[kk].n for kk in keys])))
        w /= w.sum()
        new = rng.multinomial(N, w)
        counts = Counter({kk: int(c) for kk, c in zip(keys, new) if c > 0})
        # mutation
        nm = rng.binomial(N, mu)
        for _ in range(nm):
            ks = list(counts)
            p = np.array([counts[x] for x in ks], dtype=float)
            src = ks[rng.choice(len(ks), p=p / p.sum())]
            child = mutate(types[src], rng)
            ck = child.key()
            if ck == src:
                continue
            counts[src] -= 1
            if counts[src] == 0:
                del counts[src]
            types.setdefault(ck, child)
            counts[ck] += 1
        if g % 200 == 199:
            live = set(counts)
            cache = {kk: v for kk, v in cache.items() if kk[0] in live and kk[1] in live}
            types = {kk: v for kk, v in types.items() if kk in live or kk in dom}
    def desc(kk):
        return repr(types[kk]) if kk in types else "?"
    return dict(
        eps=eps, delta=delta, seed=seed, gens=gens, N=N, mu=mu, beta=beta, cost=cost,
        series=np.array(series),
        dom=[(desc(kk), v) for kk, v in dom.most_common(40)],
        occ=[(desc(kk), v) for kk, v in occ.most_common(40)],
        log=[(g, desc(k)) for g, k in log],
        trans=[(desc(a), desc(b), v) for (a, b), v in trans.most_common(200)],
    )


if __name__ == "__main__":
    out = sys.argv[1]
    gens = int(sys.argv[2])
    jobs = []
    for eps in (0.0, 0.01, 0.05, 0.1):
        for delta in (0.5, 0.8, 0.95, 0.99):
            for seed in range(4):
                jobs.append((eps, delta, seed, gens, 100, 0.01, 1.0, 0.0))
    t = time.time()
    with Pool(14) as p:
        res = p.map(run, jobs, chunksize=1)
    pickle.dump(res, open(out, "wb"))
    print("done", time.time() - t)
