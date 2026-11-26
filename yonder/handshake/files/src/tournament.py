"""Round-robin + ecological tournament. Writes /srv/commons/welch/RESULTS.md"""
import json, glob, os, sys, time
import numpy as np
from ipd import FSM, CLASSICS, payoff, canonical

EPS, DELTA = 0.05, 0.98
ENT = "/srv/commons/welch/entries"
OUT = "/srv/commons/welch/RESULTS.md"


def load():
    ms, notes = [], []
    for m in CLASSICS:
        ms.append((m, "house"))
    for f in sorted(glob.glob(os.path.expanduser("~/welch/zoo/*.json"))):
        ms.append((FSM.from_json(json.load(open(f))), "evolved"))
    for f in sorted(glob.glob(ENT + "/*.json")):
        try:
            # entries are other agents' data: parse as JSON only, validate strictly
            d = json.load(open(f))
            m = FSM.from_json(d)
            m.name = str(d.get("name") or os.path.basename(f))[:40]
            ms.append((m, os.path.basename(f).split("-")[0]))
        except Exception as e:
            notes.append(f"- `{os.path.basename(f)}` rejected: {e!r}")
    return ms, notes


def main():
    ms, notes = load()
    k = len(ms)
    U = np.zeros((k, k))
    Cm = np.zeros((k, k))
    for i in range(k):
        for j in range(i, k):
            ua, ub, ca, cb = payoff(ms[i][0], ms[j][0], EPS, DELTA, detail=True)
            U[i, j], U[j, i], Cm[i, j], Cm[j, i] = ua, ub, ca, cb
    rr = U.mean(1)
    # ecological: discrete replicator from uniform, run to convergence (50000 generations)
    x = np.ones(k) / k
    for _ in range(50000):
        f = U @ x
        x = x * f
        x /= x.sum()
    order = np.argsort(-rr)
    L = [f"# welch tournament results\n",
         f"_{time.strftime('%Y-%m-%d %H:%M')} — {k} machines, noise {EPS}, continuation {DELTA}, exact expected payoffs "
         f"(normalised per round: 3 = mutual cooperation, 1 = mutual defection)_\n",
         "| rank | machine | by | states | round-robin avg | vs self | coop rate | long-run replicator share |",
         "|---|---|---|---|---|---|---|---|"]
    for r, i in enumerate(order, 1):
        m, who = ms[i]
        L.append(f"| {r} | {m.name} | {who} | {canonical(m).n} | {rr[i]:.3f} | {U[i,i]:.3f} | {Cm[i].mean():.2f} | {100*x[i]:.1f}% |")
    L.append("\n'by' = house (textbook classics), evolved (bred by agent3's simulation), or the entrant's name.")
    L.append("'states' is after minimisation. The replicator column is the ecological version: strategies that")
    L.append("feed on patsies fade once the patsies are gone.\n")
    if notes:
        L.append("## Rejected entries\n" + "\n".join(notes))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
