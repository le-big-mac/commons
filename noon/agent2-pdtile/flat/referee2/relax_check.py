"""Bonus: other (p,q), via sound relaxations (necessary conditions only), my own CP-SAT models.
INFEASIBLE here proves the lemma at that (p,q), even for multisets.
Lemma B relaxation: count vectors n on Z_{p^3} (Phi_{p^2}, Phi_{p^3}), n' on Z_{q^2} (Phi_{q^2}),
  n'' on Z_{pq} (Phi_{pq}), each of total p^2 q, with equal induced counts mod p and mod q.
Lemma A relaxation: count vector n on Z_{p^3 q^2} (Phi_q, Phi_{p^3 q^2}, Phi_{p^2 q^2}) and n' on
  Z_{p^4} (Phi_{p^4}), each of total p^2 q, with equal induced counts mod p^3.
All Phi conditions are exact polynomial-remainder equations (Facts 1/2 not used).
Usage: relax_check.py A|B timelimit p,q p,q ...
"""
import sys, time
from ortools.sat.python import cp_model
from common import residues, selftest

def add_level(m, mod, ds, size, name):
    x = [m.NewIntVar(0, size, f"{name}{c}") for c in range(mod)]
    m.Add(sum(x) == size)
    for d in ds:
        assert mod % d == 0
        R = residues(d, mod)
        for k in range(len(R[0])):
            m.Add(sum(R[c][k] * x[c] for c in range(mod) if R[c][k]) == 0)
    return x

def marg(x, mod, sub):
    return [sum(x[c] for c in range(mod) if c % sub == r) for r in range(sub)]

def run(which, p, q, tl, drop=None):
    size = p * p * q
    m = cp_model.CpModel()
    if which == "B":
        hy = [d for d in (p ** 2, p ** 3, q ** 2, p * q) if d != drop]
        a = add_level(m, p ** 3, [d for d in (p ** 2, p ** 3) if d in hy], size, "a")
        b = add_level(m, q ** 2, [d for d in (q ** 2,) if d in hy], size, "b")
        c = add_level(m, p * q, [d for d in (p * q,) if d in hy], size, "c")
        for u, v in zip(marg(a, p ** 3, p), marg(c, p * q, p)):
            m.Add(u == v)
        for u, v in zip(marg(b, q ** 2, q), marg(c, p * q, q)):
            m.Add(u == v)
    else:
        hy = [d for d in (q, p ** 4, p ** 3 * q ** 2, p ** 2 * q ** 2) if d != drop]
        L = p ** 3 * q ** 2
        a = add_level(m, L, [d for d in (q, L, p ** 2 * q ** 2) if d in hy], size, "a")
        b = add_level(m, p ** 4, [d for d in (p ** 4,) if d in hy], size, "b")
        for u, v in zip(marg(a, L, p ** 3), marg(b, p ** 4, p ** 3)):
            m.Add(u == v)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 8
    t0 = time.time()
    st = s.Solve(m)
    return s.StatusName(st), time.time() - t0

if __name__ == "__main__":
    selftest()
    which, tl = sys.argv[1], float(sys.argv[2])
    for pq in sys.argv[3:]:
        p, q = map(int, pq.split(","))
        st, dt = run(which, p, q, tl)
        # control: the relaxation must become feasible when a hypothesis is dropped
        dropd = p ** 3 if which == "B" else p ** 4
        st2, dt2 = run(which, p, q, tl, drop=dropd)
        print(f"Lemma {which} relaxation (p,q)=({p},{q}): {st} ({dt:.1f}s);  control without Phi_{dropd}: {st2} ({dt2:.1f}s)")
        sys.stdout.flush()
