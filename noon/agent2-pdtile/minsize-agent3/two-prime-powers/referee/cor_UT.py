"""Corollaries U and T by the referee's integer programme (milp.py), for every up-set D of Z_M.

For each up-set D with corners C and each subset T of C:
    least size of a nonempty multiset with Phi_d | A (d in D) and Phi_c not dividing A (c in T)
is computed and set beside Corollary T's value (sum of M/c over T; the least M/c if T is empty).  For T = C the run is
Corollary U's lower bound in its stronger form (non-divisors only at the corners); a further run asks for the exact pattern
(every d > 1 outside D a non-divisor).  The upper bound given to the solver is the predicted value, so a smaller true
minimum would be found.  The exact pattern of sum_c 1_{cZ_M} is checked by lib.pattern.
For M = p^n q the value for the exact pattern is also set beside the rule of the paper for Z_{p^n q} (written here from the
statement of its theorem).

usage: cor_UT.py M [solver] [tlimit] [maxT]      (maxT: only subsets T of at most this size besides T = C; default all)
"""
import sys, time, json, itertools
from lib import divisors, upsets, corners, pattern, prime_factors
from milp import least, check


def paper_rule(p, q, n, E, F, balanced):
    """Theorem of minsize.pdf for Z_{p^n q}: E = {a in [1,n]: Phi_{p^a} | A}, F = {a in [1,n]: Phi_{p^a q} | A}, balanced = Phi_q | A."""
    E, F = set(E), set(F); e = len(E)
    if not balanced:
        return p ** e if F <= E else p ** e * (p ** len(F - E) + q)
    if F == set(range(1, n + 1)): return q * p ** e
    a0 = min(a for a in range(1, n + 1) if a not in F)
    G = sorted(a for a in F - E if a > a0); k = len(G)
    x0 = (k == 0) or any(a in E for a in range(1, a0)) or (a0 in E and p >= 3) or \
         (k >= 1 and a0 in E and p == 2 and any(a in E and a not in F for a in range(a0 + 1, G[0])))
    return q * p ** e * (p ** k + (0 if x0 else 1))


def paper_value(M, D):
    ps = prime_factors(M)
    if len(ps) != 2: return None
    for p, q in (ps, ps[::-1]):
        n = 0
        while M % (p ** (n + 1) * q) == 0 and (M // q) % p ** (n + 1) == 0: n += 1
        if p ** n * q == M:
            Ds = set(D)
            return paper_rule(p, q, n, [a for a in range(1, n + 1) if p ** a in Ds], [a for a in range(1, n + 1) if p ** a * q in Ds], q in Ds)
    return None


def main():
    M = int(sys.argv[1]); solver = sys.argv[2] if len(sys.argv) > 2 else 'highs'; tl = float(sys.argv[3]) if len(sys.argv) > 3 else 120
    maxT = int(sys.argv[4]) if len(sys.argv) > 4 else 99
    dv = [d for d in divisors(M) if d > 1]
    tot = agree = notproved = wrong = 0; t00 = time.time()
    for D in upsets(M):
        C = corners(M, D); full = sum(M // c for c in C)
        # the example: one coset through 0 for each corner
        ex = [0] * M
        for c in C:
            for y in range(0, M, c): ex[y] += 1
        assert sum(ex) == full and pattern(M, ex) == list(D), ('example fails', D)
        pv = paper_value(M, D)
        if pv is not None: assert pv == full, ('paper rule differs from the corner sum', D, pv, full)
        subsets = [T for k in range(len(C) + 1) for T in itertools.combinations(C, k) if k <= maxT or k == len(C)]
        for T in subsets:
            want = sum(M // c for c in T) if T else min(M // c for c in C)
            forbid = list(T) if T else [1]
            if 1 in forbid and len(forbid) > 1: forbid.remove(1)
            t0 = time.time(); st, sz, v = least(M, list(D), forbid, ub=want, solver=solver, tlimit=tl)
            if v: check(M, list(D), [c for c in forbid if c > 1], v)
            tot += 1
            if st == 'optimal' and sz == want: agree += 1; verdict = 'agrees'
            elif st == 'optimal' or st == 'infeasible': wrong += 1; verdict = 'DIFFERS'
            else: notproved += 1; verdict = 'not proved'
            print(json.dumps(dict(M=M, D=list(D), corners=C, T=list(T), kind='corollary T', predicted=want, status=st, least=sz, verdict=verdict, seconds=round(time.time() - t0, 1))), flush=True)
        # exact pattern
        forbid = [d for d in dv if d not in set(D)] or [1]
        t0 = time.time(); st, sz, v = least(M, list(D), forbid, ub=full, solver=solver, tlimit=tl)
        if v: check(M, list(D), [c for c in forbid if c > 1], v); assert pattern(M, v) == list(D)
        tot += 1
        if st == 'optimal' and sz == full: agree += 1; verdict = 'agrees'
        elif st == 'optimal' or st == 'infeasible': wrong += 1; verdict = 'DIFFERS'
        else: notproved += 1; verdict = 'not proved'
        print(json.dumps(dict(M=M, D=list(D), corners=C, kind='exact pattern', predicted=full, paper_rule=pv, status=st, least=sz, verdict=verdict, seconds=round(time.time() - t0, 1))), flush=True)
    print(f'# Z_{M} ({solver}, {tl:.0f} s each): {len(upsets(M))} up-sets, {tot} programmes; proved equal to the predicted value: {agree}; proved different: {wrong}; not proved in time: {notproved}; {time.time() - t00:.0f} s', flush=True)


if __name__ == '__main__':
    main()
