"""Exact noisy iterated prisoner's dilemma between finite-state machines.

A machine with n states is (start, play[n] in {0=C,1=D}, nxt[n,2]) where
nxt[s, a] is the next state after seeing the opponent do a.

Noise: each intended action is flipped independently with prob eps. The
flipped (realised) action is what earns payoffs and what the opponent sees.
A machine does not observe its own realised action.

Game continues after each round with prob delta. Payoff reported is the
normalised discounted average: (1-delta) * sum_t delta^t u_t, so it lives
in [S, T] and is comparable across delta.
"""
import json
import numpy as np

C, D = 0, 1
# payoff to row player: PAY[my_action, their_action]
PAY = np.array([[3.0, 0.0], [5.0, 1.0]])


class FSM:
    __slots__ = ("start", "play", "nxt", "name")

    def __init__(self, start, play, nxt, name=None):
        self.start = int(start)
        self.play = np.asarray(play, dtype=np.int8)
        self.nxt = np.asarray(nxt, dtype=np.int16).reshape(-1, 2)
        self.name = name

    @property
    def n(self):
        return len(self.play)

    def key(self):
        return (self.start, self.play.tobytes(), self.nxt.tobytes())

    def to_json(self):
        return {
            "name": self.name,
            "start": self.start,
            "states": [
                {"play": "CD"[p], "if_C": int(a), "if_D": int(b)}
                for p, (a, b) in zip(self.play, self.nxt)
            ],
        }

    @staticmethod
    def from_json(d):
        st = d["states"]
        if not (1 <= len(st) <= 16):
            raise ValueError("1..16 states")
        play = [{"C": 0, "D": 1}[s["play"]] for s in st]
        nxt = [[s["if_C"], s["if_D"]] for s in st]
        for row in nxt:
            for v in row:
                if not (0 <= v < len(st)):
                    raise ValueError("bad transition")
        if not (0 <= d.get("start", 0) < len(st)):
            raise ValueError("bad start")
        return FSM(d.get("start", 0), play, nxt, d.get("name"))

    def __repr__(self):
        body = " ".join(
            f"{i}:{'CD'[p]}[{a},{b}]" for i, (p, (a, b)) in enumerate(zip(self.play, self.nxt))
        )
        return f"<{self.name or 'fsm'} s{self.start} {body}>"


def canonical(m):
    """Minimise (reachable states + Moore partition refinement) and relabel
    in BFS order, so behaviourally identical machines compare equal."""
    # reachable
    seen = [m.start]
    idx = {m.start: 0}
    for s in seen:
        for a in (0, 1):
            t = int(m.nxt[s, a])
            if t not in idx:
                idx[t] = len(seen)
                seen.append(t)
    play = [int(m.play[s]) for s in seen]
    nxt = [[idx[int(m.nxt[s, a])] for a in (0, 1)] for s in seen]
    n = len(seen)
    # partition refinement
    cls = play[:]
    while True:
        sig = {}
        new = []
        for s in range(n):
            k = (cls[s], cls[nxt[s][0]], cls[nxt[s][1]])
            new.append(sig.setdefault(k, len(sig)))
        if len(sig) == len(set(cls)):
            cls = new
            break
        cls = new
    # quotient, BFS relabel from start class
    rep = {}
    for s in range(n):
        rep.setdefault(cls[s], s)
    order = [cls[0]]
    pos = {cls[0]: 0}
    for c in order:
        for a in (0, 1):
            t = cls[nxt[rep[c]][a]]
            if t not in pos:
                pos[t] = len(order)
                order.append(t)
    p2 = [play[rep[c]] for c in order]
    n2 = [[pos[cls[nxt[rep[c]][a]]] for a in (0, 1)] for c in order]
    return FSM(0, p2, n2, m.name)


def payoff(a, b, eps=0.05, delta=0.98, detail=False):
    """Exact expected normalised discounted payoffs (to a, to b)."""
    na, nb = a.n, b.n
    N = na * nb
    # realised action distributions per state
    pa = np.where(a.play[:, None] == np.arange(2)[None], 1 - eps, eps)  # [na,2]
    pb = np.where(b.play[:, None] == np.arange(2)[None], 1 - eps, eps)  # [nb,2]
    # joint prob of realised (x,y) at joint state (i,j): [na,nb,2,2]
    pj = pa[:, None, :, None] * pb[None, :, None, :]
    ua = (pj * PAY[None, None]).sum((2, 3)).reshape(N)
    ub = (pj * PAY.T[None, None]).sum((2, 3)).reshape(N)
    P = np.zeros((N, N))
    ii, jj = np.meshgrid(np.arange(na), np.arange(nb), indexing="ij")
    src = (ii * nb + jj).ravel()
    for x in (0, 1):
        for y in (0, 1):
            dst = (a.nxt[ii, y] * nb + b.nxt[jj, x]).ravel()
            np.add.at(P, (src, dst), pj[:, :, x, y].ravel())
    # occupancy: v = (1-delta) e0 (I - delta P)^-1
    e0 = np.zeros(N)
    e0[a.start * nb + b.start] = 1.0
    occ = (1 - delta) * np.linalg.solve((np.eye(N) - delta * P).T, e0)
    if detail:
        coop_a = occ @ pj[:, :, 0, :].sum(2).reshape(N)
        coop_b = occ @ pj[:, :, :, 0].sum(2).reshape(N)
        return occ @ ua, occ @ ub, coop_a, coop_b
    return occ @ ua, occ @ ub


def simulate(a, b, eps, delta, rng, games=2000):
    """Monte Carlo check of payoff()."""
    ta = tb = 0.0
    for _ in range(games):
        sa, sb = a.start, b.start
        w = 1.0
        while True:
            x = a.play[sa] ^ (rng.random() < eps)
            y = b.play[sb] ^ (rng.random() < eps)
            ta += PAY[x, y]
            tb += PAY[y, x]
            sa, sb = a.nxt[sa, y], b.nxt[sb, x]
            if rng.random() > delta:
                break
    # per-round average weighted by geometric length == normalised discounted
    return ta * (1 - delta) / games, tb * (1 - delta) / games


def M(name, start, spec):
    """spec: list of (play, if_C, if_D)"""
    return FSM(start, [{"C": 0, "D": 1}[p] for p, _, _ in spec], [[c, d] for _, c, d in spec], name)


CLASSICS = [
    M("ALLC (patsy)", 0, [("C", 0, 0)]),
    M("ALLD (uncaring)", 0, [("D", 0, 0)]),
    M("TFT (reciprocal)", 0, [("C", 0, 1), ("D", 0, 1)]),
    M("suspicious TFT (shifty)", 1, [("C", 0, 1), ("D", 0, 1)]),
    M("GRIM (punisher)", 0, [("C", 0, 1), ("D", 1, 1)]),
    M("WSLS / Pavlov", 0, [("C", 0, 1), ("D", 1, 0)]),
    M("TF2T (forgiving)", 0, [("C", 0, 1), ("C", 0, 2), ("D", 0, 2)]),
    M("2TFT (stiffened)", 0, [("C", 0, 1), ("D", 2, 1), ("D", 0, 1)]),
    M("alternator", 0, [("C", 1, 1), ("D", 0, 0)]),
    # contrite TFT: knows when it's in bad standing and accepts one punishment
    # states: 0 content(C), 1 provoked(D), 2 contrite(C)
    # Approximation without self-observation: after punishing, return to C regardless.
    M("punish-once", 0, [("C", 0, 1), ("D", 0, 0)]),
    M("welcher", 0, [("C", 1, 0), ("C", 2, 0), ("D", 0, 0)]),  # cooperates twice then welches
]

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    for a, b in [(CLASSICS[2], CLASSICS[5]), (CLASSICS[4], CLASSICS[8]), (CLASSICS[6], CLASSICS[10])]:
        ex = payoff(a, b, 0.05, 0.9)
        mc = simulate(a, b, 0.05, 0.9, rng, 40000)
        print(a.name, "vs", b.name, "exact", np.round(ex, 4), "mc", np.round(mc, 4))
    print(canonical(M("x", 2, [("C", 0, 1), ("D", 0, 1), ("C", 3, 1), ("C", 0, 1)])))
