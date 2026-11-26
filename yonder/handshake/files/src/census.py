"""Exhaustive census: all behaviourally distinct machines with <= S states. Full payoff matrix, then
which are strict Nash (no other machine in the set does better against it than it does against itself)."""
import sys, itertools, pickle, time
import numpy as np
from multiprocessing import Pool
from ipd import FSM, canonical, PAY

S = int(sys.argv[1]); EPS = float(sys.argv[2]); DELTA = float(sys.argv[3])

def enumerate_machines(S):
    seen = {}
    for n in range(1, S + 1):
        for play in itertools.product((0, 1), repeat=n):
            for nx in itertools.product(range(n), repeat=2 * n):
                m = canonical(FSM(0, play, np.array(nx).reshape(n, 2)))
                if m.n == n:
                    seen.setdefault(m.key(), m)
    return list(seen.values())

def pad(ms, S):
    K = len(ms)
    play = np.zeros((K, S), dtype=np.int64); nxt = np.zeros((K, S, 2), dtype=np.int64)
    for i, m in enumerate(ms):
        play[i, :m.n] = m.play; nxt[i, :m.n] = m.nxt
        for s in range(m.n, S): nxt[i, s] = s
    return play, nxt

def init(p, n):
    global PLAY, NXT
    PLAY, NXT = p, n

def row(i):
    """payoffs U[i, :] (to i against every j) and U[:, i] is obtained by symmetry elsewhere; return (ui, uj)"""
    K, S = PLAY.shape; N = S * S
    pa = np.where(PLAY[i][:, None] == np.arange(2), 1 - EPS, EPS)            # [S,2]
    pb = np.where(PLAY[:, :, None] == np.arange(2), 1 - EPS, EPS)            # [K,S,2]
    pj = pa[None, :, None, :, None] * pb[:, None, :, None, :]                # [K,S,S,x,y]
    ua = (pj * PAY).sum((3, 4)).reshape(K, N)
    ub = (pj * PAY.T).sum((3, 4)).reshape(K, N)
    P = np.zeros((K, N, N))
    kk = np.arange(K)[:, None, None]
    ii = np.arange(S)[None, :, None]; jj = np.arange(S)[None, None, :]
    src = np.broadcast_to(ii * S + jj, (K, S, S))
    for x in (0, 1):
        for y in (0, 1):
            dst = NXT[i][:, y][None, :, None] * S + NXT[:, :, x][:, None, :]
            np.add.at(P, (np.broadcast_to(kk, (K, S, S)), src, dst), pj[:, :, :, x, y])
    A = np.eye(N)[None] - DELTA * np.transpose(P, (0, 2, 1))
    e0 = np.zeros((K, N, 1)); e0[:, 0, 0] = 1
    occ = (1 - DELTA) * np.linalg.solve(A, e0)[:, :, 0]
    return (occ * ua).sum(1), (occ * ub).sum(1)

if __name__ == "__main__":
    t = time.time()
    ms = enumerate_machines(S); K = len(ms)
    print("machines", K, "enum time", round(time.time() - t, 1), flush=True)
    play, nxt = pad(ms, S)
    with Pool(14, initializer=init, initargs=(play, nxt)) as p:
        out = p.map(row, range(K), chunksize=8)
    U = np.array([o[0] for o in out])          # U[i,j] payoff to i vs j
    V = np.array([o[1] for o in out])          # V[i,j] payoff to j vs i
    print("symmetry check", np.abs(U.T - V).max(), "time", round(time.time() - t, 1))
    pickle.dump((ms, U), open(f"census_{S}_{EPS}_{DELTA}.pkl", "wb"))
    self_ = np.diag(U)
    best_inv = (V - np.eye(K) * 1e9).max(1)     # best any other j earns against i
    margin = self_ - best_inv
    nash = np.where(margin > 1e-9)[0]
    print(f"strict Nash among {K}: {len(nash)}")
    for i in sorted(nash, key=lambda i: -self_[i])[:25]:
        print(f"  self {self_[i]:.3f}  margin {margin[i]:.3f}  {ms[i]}")
