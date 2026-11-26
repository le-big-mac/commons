"""Search for efficient robust machines: maximise self-payoff subject to no invader in a test set
(all <=3-state machines + every one-step mutant of the candidate) earning more against it than it does itself."""
import sys, time, pickle, numpy as np
from multiprocessing import Pool
sys.argv = [sys.argv[0], "3", sys.argv[1], sys.argv[2]] + sys.argv[3:]
from census import enumerate_machines, pad
from ipd import FSM, canonical, PAY, payoff
EPS = float(sys.argv[2]); DELTA = float(sys.argv[3]); NS = int(sys.argv[4]); SECS = float(sys.argv[5])

def batch(rp, rn, rs, IP, IN, IS):
    """resident (play[S1], nxt[S1,2], start) vs K invaders (play[K,S2], nxt[K,S2,2], start[K]).
    returns (resident payoff[K], invader payoff[K])"""
    S1 = len(rp); K, S2 = IP.shape; N = S1 * S2
    pa = np.where(rp[:, None] == np.arange(2), 1 - EPS, EPS)
    pb = np.where(IP[:, :, None] == np.arange(2), 1 - EPS, EPS)
    pj = pa[None, :, None, :, None] * pb[:, None, :, None, :]
    ua = (pj * PAY).sum((3, 4)).reshape(K, N); ub = (pj * PAY.T).sum((3, 4)).reshape(K, N)
    P = np.zeros((K, N, N))
    kk = np.broadcast_to(np.arange(K)[:, None, None], (K, S1, S2))
    src = np.broadcast_to(np.arange(S1)[None, :, None] * S2 + np.arange(S2)[None, None, :], (K, S1, S2))
    for x in (0, 1):
        for y in (0, 1):
            dst = rn[:, y][None, :, None] * S2 + IN[:, :, x][:, None, :]
            np.add.at(P, (kk, src, dst), pj[:, :, :, x, y])
    A = np.eye(N)[None] - DELTA * np.transpose(P, (0, 2, 1))
    e0 = np.zeros((K, N, 1)); e0[np.arange(K), rs * S2 + IS, 0] = 1
    occ = (1 - DELTA) * np.linalg.solve(A, e0)[:, :, 0]
    return (occ * ua).sum(1), (occ * ub).sum(1)

def neighbours(p, n, s):
    S = len(p); out = []
    for i in range(S):
        q = p.copy(); q[i] ^= 1; out.append((q, n, s))
        for a in (0, 1):
            for t in range(S):
                if t != n[i, a]:
                    m = n.copy(); m[i, a] = t; out.append((p, m, s))
    for t in range(S):
        if t != s: out.append((p, n, t))
    return out

SMALL = None
def setup():
    global SMALL
    ms = enumerate_machines(3)
    pl, nx = pad(ms, 3)
    SMALL = (pl, nx, np.zeros(len(ms), dtype=np.int64))

def evaluate(p, n, s):
    self_ = batch(p, n, s, p[None], n[None], np.array([s]))[0][0]
    v1 = batch(p, n, s, *SMALL)[1]
    nb = neighbours(p, n, s)
    v2 = batch(p, n, s, np.array([x[0] for x in nb]), np.array([x[1] for x in nb]), np.array([x[2] for x in nb]))[1]
    best = max(v1.max(), v2.max())
    return self_, best

def chain(seed):
    setup()
    rng = np.random.default_rng(seed)
    S = NS
    p = rng.integers(2, size=S); n = rng.integers(S, size=(S, 2)); s = 0
    if seed % 3 == 0:   # seed some chains from the known 4-state equilibrium, padded
        p = np.array([0, 0, 1, 1] + [0] * (S - 4)); n = np.array([[0, 1], [1, 2], [2, 3], [2, 1]] + [[0, 0]] * (S - 4))
    def score(e): return e[0] - 30 * max(0.0, e[1] - e[0])
    cur = evaluate(p, n, s); best = (score(cur), cur, p.copy(), n.copy(), s)
    t0 = time.time(); it = 0
    while time.time() - t0 < SECS:
        T = 0.05 * (1 - (time.time() - t0) / SECS) + 0.002
        q, m, r = p.copy(), n.copy(), s
        for _ in range(rng.integers(1, 3)):
            u = rng.random()
            if u < 0.25: q[rng.integers(S)] ^= 1
            elif u < 0.95: m[rng.integers(S), rng.integers(2)] = rng.integers(S)
            else: r = int(rng.integers(S))
        e = evaluate(q, m, r); it += 1
        if score(e) >= score(cur) or rng.random() < np.exp((score(e) - score(cur)) / T):
            p, n, s, cur = q, m, r, e
            if score(cur) > best[0]: best = (score(cur), cur, p.copy(), n.copy(), s)
    return best + (it,)

if __name__ == "__main__":
    with Pool(14) as pool:
        res = pool.map(chain, range(14))
    res.sort(key=lambda r: -r[0])
    pickle.dump(res, open(f"climb_{NS}_{EPS}.pkl", "wb"))
    seen = set()
    for sc, (self_, inv), p, n, s, it in res:
        m = canonical(FSM(s, p, n))
        if m.key() in seen: continue
        seen.add(m.key())
        print(f"score {sc:.4f} self {self_:.4f} best test invader {inv:.4f} ({'robust' if inv <= self_ else 'beaten'}) iters {it}  {m}")
