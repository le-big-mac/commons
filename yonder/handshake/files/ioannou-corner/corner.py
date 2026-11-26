"""Ioannou's corner, tried with the welch study's own machinery: a small population (30), heavy mutation (a third of the
population mutated every generation), a short run (500 generations), games of about 200 rounds, and errors of two kinds.

What is the study's and what is new here. From the study (/srv/commons/welch/src): machines, canonical(), mutate(), exact payoffs,
Wright-Fisher selection. New here: (1) perception errors as well as implementation errors (a machine may misread the other's move;
payoffs follow the moves as they came out, transitions follow the moves as they were read); (2) a start from 30 random
eight-state machines as well as from all-defect.

usage: corner.py trial | corner.py run OUT.json      (under -I)"""
import sys, json, time
from collections import Counter
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, '/srv/commons/welch/src')
from ipd import FSM, canonical, PAY
from evolve import mutate

def payoff2(a, b, e_move, e_read, delta):
    """Exact expected normalised discounted payoff and cooperation rate, each for a and for b. e_move: chance an intended move comes out
    flipped; e_read: chance a machine misreads the other's move (independently for each machine and round)."""
    na, nb = a.n, b.n; N = na * nb
    pa = np.where(a.play[:, None] == np.arange(2)[None], 1 - e_move, e_move)
    pb = np.where(b.play[:, None] == np.arange(2)[None], 1 - e_move, e_move)
    pj = pa[:, None, :, None] * pb[None, :, None, :]                       # [i, j, x, y]: moves as they come out
    ua = (pj * PAY[None, None]).sum((2, 3)).reshape(N); ub = (pj * PAY.T[None, None]).sum((2, 3)).reshape(N)
    P = np.zeros((N, N)); ii, jj = np.meshgrid(np.arange(na), np.arange(nb), indexing='ij'); src = (ii * nb + jj).ravel()
    for x in (0, 1):
        for y in (0, 1):
            for fa, pfa in ((0, 1 - e_read), (1, e_read)):                # a misreads b's move
                for fb, pfb in ((0, 1 - e_read), (1, e_read)):            # b misreads a's move
                    if pfa * pfb == 0: continue
                    dst = (a.nxt[ii, y ^ fa] * nb + b.nxt[jj, x ^ fb]).ravel()
                    np.add.at(P, (src, dst), (pj[:, :, x, y] * pfa * pfb).ravel())
    e0 = np.zeros(N); e0[a.start * nb + b.start] = 1.0
    occ = (1 - delta) * np.linalg.solve((np.eye(N) - delta * P).T, e0)
    return occ @ ua, occ @ ub, occ @ pj[:, :, 0, :].sum(2).reshape(N), occ @ pj[:, :, :, 0].sum(2).reshape(N)

ALLD = canonical(FSM(0, [1], [[0, 0]]))
def random_machine(rng, n=8):
    return canonical(FSM(0, rng.integers(0, 2, n), rng.integers(0, n, (n, 2))))
def open_loop(m):
    """True if the machine's play does not depend on what it reads (every state reachable from the start has both arrows to the same place)."""
    seen, todo = set(), [m.start]
    while todo:
        s = todo.pop()
        if s in seen: continue
        seen.add(s)
        if m.nxt[s][0] != m.nxt[s][1]: return False
        todo.append(int(m.nxt[s][0]))
    return True

def run(args):
    e_move, e_read, delta, seed, gens, N, mu, beta, start = args
    rng = np.random.default_rng(seed); types = {}; counts = Counter()
    for _ in range(N):
        m = ALLD if start == 'alld' else random_machine(rng)
        types.setdefault(m.key(), m); counts[m.key()] += 1
    cache = {}
    def pay(ka, kb):
        v = cache.get((ka, kb))
        if v is None:
            ua, ub, ca, cb = payoff2(types[ka], types[kb], e_move, e_read, delta)
            cache[(ka, kb)] = v = (ua, ca); cache[(kb, ka)] = (ub, cb)
        return v
    coop_tail, occ_tail = [], Counter(); tail = 100
    for g in range(gens):
        keys = list(counts); cnt = np.array([counts[k] for k in keys], dtype=float); k = len(keys)
        U = np.empty((k, k)); Cm = np.empty((k, k))
        for i in range(k):
            for j in range(k): U[i, j], Cm[i, j] = pay(keys[i], keys[j])
        freq = cnt / N; fit = U @ freq
        if g >= gens - tail:
            coop_tail.append(float(freq @ (Cm @ freq)))
            for kk, c in zip(keys, cnt): occ_tail[kk] += int(c)
        w = freq * np.exp(beta * fit); w /= w.sum()
        counts = Counter({kk: int(c) for kk, c in zip(keys, rng.multinomial(N, w)) if c > 0})
        for _ in range(rng.binomial(N, mu)):
            ks = list(counts); p = np.array([counts[x] for x in ks], dtype=float)
            srck = ks[rng.choice(len(ks), p=p / p.sum())]; child = mutate(types[srck], rng); ck = child.key()
            if ck == srck: continue
            counts[srck] -= 1
            if counts[srck] == 0: del counts[srck]
            types.setdefault(ck, child); counts[ck] += 1
        if g % 50 == 49:
            live = set(counts) | set(occ_tail)
            cache = {kk: v for kk, v in cache.items() if kk[0] in counts and kk[1] in counts}
            types = {kk: v for kk, v in types.items() if kk in live}
    topk, topc = occ_tail.most_common(1)[0]; top = types[topk]
    lastk = max(counts, key=counts.get); last = types[lastk]
    ol = sum(c for kk, c in occ_tail.items() if open_loop(types[kk])) / sum(occ_tail.values())
    return dict(e_move=e_move, e_read=e_read, seed=seed, start=start, N=N, mu=mu, gens=gens, beta=beta, delta=delta,
                coop=float(np.mean(coop_tail)), top=repr(top), top_share=topc / sum(occ_tail.values()), top_is_alld=bool(topk == ALLD.key()),
                top_open_loop=bool(open_loop(top)), last=repr(last), last_is_alld=bool(lastk == ALLD.key()), open_loop_share=float(ol),
                alld_share=occ_tail.get(ALLD.key(), 0) / sum(occ_tail.values()))

def jobs(runs, gens):
    out = []
    for start in ('alld', 'random'):
        for kind in ('move', 'both'):
            for r in (0.0, 0.01, 0.02, 0.04):
                for s in range(runs):
                    out.append((r, r if kind == 'both' else 0.0, 0.995, 1000 * len(out) + s, gens, 30, 1 / 3, 1.0, start))
    return out

if __name__ == '__main__':
    if sys.argv[1] == 'trial':
        # 1. payoff2 with no misreading must equal the study's payoff(); 2. a few short runs, timed
        from ipd import payoff, M
        rng = np.random.default_rng(1); worst = 0
        for _ in range(200):
            a, b = random_machine(rng), random_machine(rng)
            x = payoff2(a, b, 0.03, 0.0, 0.99); y = payoff(a, b, 0.03, 0.99, detail=True)
            worst = max(worst, max(abs(p - q) for p, q in zip(x, y)))
        print('payoff2 with no misreading against the study\'s payoff(), 200 random pairs: largest difference', worst)
        H = M('handshake', 0, [('D', 0, 1), ('D', 0, 2), ('C', 2, 0)])
        for er in (0.0, 0.02): print(f'handshake against itself, moves flipped 2%, misreading {er}: {payoff2(H, H, 0.02, er, 0.995)[0]:.4f}')
        t = time.time(); res = [run(j) for j in jobs(1, 60)[::4]]
        print(f'{len(res)} runs of 60 generations in {time.time() - t:.1f} s')
        for r in res: print('  ', r['start'], r['e_move'], r['e_read'], 'coop %.2f' % r['coop'], 'alld share %.2f' % r['alld_share'], 'open-loop share %.2f' % r['open_loop_share'], r['top'][:60])
    else:
        J = jobs(30, 500); t = time.time()
        with Pool(14) as p: res = p.map(run, J, chunksize=1)
        json.dump(res, open(sys.argv[2], 'w'))
        print(len(res), 'runs in', round(time.time() - t), 's')
