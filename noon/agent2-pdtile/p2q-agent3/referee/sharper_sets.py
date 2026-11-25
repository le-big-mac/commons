"""Set-level checks for lemmas-sharper-agent3.md in Z_M, M = p^4 q^2 (referee's own code).

mode 'build p,q ...' : build random sets with the structure of Lemma A+ and near-misses; exact divisibility.
mode 'milp p,q ...'  : HiGHS feasibility / random-objective probes (a solver's "infeasible" is its word only;
                       every returned set is re-verified exactly).
"""
import sys
import time
import numpy as np
import core

rng = np.random.default_rng(7)


def setup(p, q):
    M = p ** 4 * q ** 2
    crt = {}
    for x in range(M):
        crt[(x % p ** 4, x % q ** 2)] = x
    return M, crt


def structured(p, q, crt):
    """random set with the structure of Lemma A+"""
    A = []
    for j in range(q):
        rho = int(rng.integers(p))
        t = j + q * int(rng.integers(q))
        for m in range(p * p):
            r3 = rho + p * m                       # class mod p^3 over rho
            r = r3 + p ** 3 * int(rng.integers(p))  # free lift to Z_{p^4}
            A.append(crt[(r, t)])
    return A


def has_structure(p, q, A):
    for j in range(q):
        cls = [x for x in A if x % q == j]
        if len(cls) != p * p:
            return False
        if len({x % p for x in cls}) != 1 or len({x % q ** 2 for x in cls}) != 1:
            return False
        if len({x % p ** 3 for x in cls}) != p * p:
            return False
    return True


def build(p, q, nsets=200):
    M, crt = setup(p, q)
    D3 = [q, p ** 3 * q ** 2, p ** 2 * q ** 2]
    t0 = time.time()
    n_ok = 0
    n_p4 = n_p = 0
    extra = {}
    seen = set()
    for _ in range(nsets):
        A = structured(p, q, crt)
        assert len(set(A)) == p * p * q and has_structure(p, q, A)
        seen.add(tuple(sorted(A)))
        ok = all(core.divides(M, d, A) for d in D3)
        n_ok += ok
        n_p4 += core.divides(M, p ** 4, A)
        n_p += core.divides(M, p, A)
    # which other cyclotomic divisors ever occur on a few of them (information only)
    for _ in range(10):
        A = structured(p, q, crt)
        for d in core.zero_set(M, A):
            extra[d] = extra.get(d, 0) + 1
    # near misses
    nm = {"NM1 two lifts t in one class j": 0, "NM2 a class mod p^3 doubled": 0, "NM3 one class j spread over all classes mod p": 0,
          "NM4 two classes rho in one class j": 0}
    trials = 50
    for _ in range(trials):
        A = structured(p, q, crt)
        j = int(rng.integers(q))
        cls = [x for x in A if x % q == j]
        rest = [x for x in A if x % q != j]
        # NM1: change the lift t of ONE element of class j
        x = cls[0]
        t = x % q ** 2
        t2 = (t + q) % q ** 2
        B = rest + cls[1:] + [crt[(x % p ** 4, t2)]]
        nm["NM1 two lifts t in one class j"] += all(core.divides(M, d, B) for d in D3)
        # NM2: move one element into the class mod p^3 of another (different lift to p^4)
        y = cls[1]
        r_new = (y % p ** 3) + p ** 3 * (((y % p ** 4) // p ** 3 + 1) % p)
        B = rest + cls[1:] + [crt[(r_new, t)]]
        assert len(set(B)) == len(B)
        nm["NM2 a class mod p^3 doubled"] += all(core.divides(M, d, B) for d in D3)
        # NM3: class j = one element in each class mod p^2 (so spread evenly over the classes mod p), same t
        B = rest + [crt[(c + p * p * int(rng.integers(p * p)), t)] for c in range(p * p)]
        nm["NM3 one class j spread over all classes mod p"] += all(core.divides(M, d, B) for d in D3)
        # NM4: half-and-half is impossible in general; move ONE element to another class rho (keeping its class mod p^3 count)
        x = cls[0]
        r_new = (x % p ** 4 + 1) % p ** 4
        B = rest + cls[1:] + [crt[(r_new, t)]]
        nm["NM4 two classes rho in one class j"] += all(core.divides(M, d, B) for d in D3)
    print(f"(p,q)=({p},{q}) M={M}: {nsets} structured sets ({len(seen)} distinct): all three of Phi_q, Phi_p3q2, Phi_p2q2 divide: {n_ok}; "
          f"Phi_p4 divides: {n_p4}; Phi_p divides: {n_p}; zero sets seen on 10 more: {dict(sorted(extra.items()))}; "
          f"near-misses still satisfying all three (of {trials} each): {nm}  [{time.time()-t0:.1f}s]")
    sys.stdout.flush()


def milp_mode(p, q, tl=40, nrand=25):
    from scipy.optimize import milp, LinearConstraint, Bounds
    M, crt = setup(p, q)
    n = p * p * q

    def solve(divs, obj=None, tl=tl, extra=None):
        cons = [LinearConstraint(core.res(M, d).T.astype(float), 0, 0) for d in divs]
        cons.append(LinearConstraint(np.ones((1, M)), n, n))
        fix0 = np.zeros((1, M))
        fix0[0, 0] = 1
        cons.append(LinearConstraint(fix0, 1, 1))          # 0 in A (translation)
        if extra is not None:
            cons.append(extra)
        c = np.zeros(M) if obj is None else obj
        t0 = time.time()
        r = milp(c=c, constraints=cons, integrality=np.ones(M), bounds=Bounds(0, 1), options={"time_limit": tl})
        dt = time.time() - t0
        if r.x is not None and r.status in (0, 1):
            A = [i for i in range(M) if r.x[i] > 0.5]
            assert len(A) == n and all(core.divides(M, d, A) for d in divs), "solver returned a non-solution"
            return "feasible", A, dt
        if r.status == 2:
            return "infeasible", None, dt
        return f"no answer (status {r.status})", None, dt

    P = {"p": p, "p2": p * p, "p3": p ** 3, "p4": p ** 4, "q": q, "q2": q * q, "pq": p * q, "pq2": p * q * q,
         "p2q": p * p * q, "p3q2": p ** 3 * q * q, "p2q2": p * p * q * q}

    def run(label, names, expect):
        st, A, dt = solve([P[x] for x in names])
        z = ""
        if A is not None:
            Z = core.zero_set(M, A)
            z = f" zero set {sorted(Z)}"
        print(f"   {label} {names}: {st}{z}  [expected {expect}; {dt:.1f}s]")
        sys.stdout.flush()
        return A

    print(f"(p,q)=({p},{q}) M={M}, |A|={n}")
    print("  Lemma A+:")
    run("A+ all four", ["q", "p4", "p3q2", "p2q2"], "infeasible")
    run("A+ with Phi_p instead of Phi_p4", ["q", "p", "p3q2", "p2q2"], "infeasible")
    for drop in ["q", "p4", "p3q2", "p2q2"]:
        run(f"A+ without {drop}", [x for x in ["q", "p4", "p3q2", "p2q2"] if x != drop], "feasible")
    # forward structure by random objectives
    divs = [P["q"], P["p3q2"], P["p2q2"]]
    found = set()
    bad = 0
    noans = 0
    for _ in range(nrand):
        st, A, dt = solve(divs, obj=rng.normal(size=M), tl=20)
        if A is None:
            noans += 1
            continue
        found.add(tuple(A))
        bad += not has_structure(p, q, A)
    print(f"   forward structure: {nrand} random objectives, {len(found)} distinct sets, {noans} without answer, "
          f"{bad} WITHOUT the claimed structure  [expected 0]")
    print("  Lemma B+:")
    run("B1", ["p2", "p3", "q2", "pq"], "infeasible")
    run("B2", ["p2", "p3", "pq", "pq2"], "infeasible")
    run("B3", ["p3", "q2", "pq", "p2q"], "infeasible")
    six = ["p2", "p3", "q2", "pq", "pq2", "p2q"]
    for dropped in [["p3"], ["pq"], ["p2", "q2"], ["p2", "p2q"], ["q2", "pq2"]]:
        run(f"B six without {dropped}", [x for x in six if x not in dropped], "feasible (maximal subset containing none of B1,B2,B3)")
    # intermediate claims
    for names, test, what in [
        (["p2", "p3", "pq"], lambda A: len({x % p for x in A}) == 1 and all(sum(1 for x in A if x % q == j) == p * p for j in range(q)),
         "one class mod p, p^2 in each class mod q"),
        (["q2", "pq", "p2q"], lambda A: len({x % q for x in A}) == 1, "one class mod q"),
    ]:
        dv = [P[x] for x in names]
        found = set()
        bad = noans = 0
        for _ in range(nrand):
            st, A, dt = solve(dv, obj=rng.normal(size=M), tl=20)
            if A is None:
                noans += 1
                continue
            found.add(tuple(A))
            bad += not test(A)
        print(f"   intermediate {names} => {what}: {nrand} random objectives, {len(found)} distinct sets, {noans} without answer, "
              f"{bad} violations  [expected 0]")
        sys.stdout.flush()


mode = sys.argv[1]
for a in sys.argv[2:]:
    p, q = map(int, a.split(","))
    if mode == "build":
        build(p, q)
    else:
        milp_mode(p, q)
