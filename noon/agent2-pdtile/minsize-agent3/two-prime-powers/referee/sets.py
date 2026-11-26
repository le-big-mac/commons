"""The proposition on sets (S5), by the referee's integer programme with 0/1 variables, for every up-set D of Z_M.

Predicted: a set with pattern exactly D exists  iff  D has one corner or the corners have a common prime factor; the least
such set has sum of M/c elements; when no such set exists there is not even a set with the divisors D and the corners as
non-divisors.
Two programmes for each up-set:
   weak : Phi_d | A (d in D), Phi_c not dividing A (c a corner), A a set: least size, or proved infeasible;
   exact: pattern exactly D, A a set: least size, or proved infeasible (skipped when 'weak' is proved infeasible).
usage: sets.py M [solver] [tlimit]
"""
import sys, time, json, math
from lib import divisors, upsets, corners, pattern
from milp import least, check


def main():
    M = int(sys.argv[1]); solver = sys.argv[2] if len(sys.argv) > 2 else 'highs'; tl = float(sys.argv[3]) if len(sys.argv) > 3 else 300
    dv = [d for d in divisors(M) if d > 1]; t00 = time.time()
    n = good = bad = unproved = 0
    for D in upsets(M):
        C = corners(M, D); full = sum(M // c for c in C); g = 0
        for c in C: g = math.gcd(g, c)
        has = (len(C) == 1) or g > 1
        rec = dict(M=M, D=list(D), corners=C, gcd=g, predicted=('set of %d' % full) if has else 'no set')
        t0 = time.time()
        st, sz, v = least(M, list(D), [c for c in C if c > 1] or [1], binary=True, ub=M, solver=solver, tlimit=tl)
        if v: check(M, list(D), [c for c in C if c > 1], v); assert max(v) <= 1
        rec['weak'] = (st, sz)
        if st == 'infeasible': st2, sz2 = 'infeasible', None
        else:
            st2, sz2, v2 = least(M, list(D), [d for d in dv if d not in set(D)] or [1], binary=True, ub=M, solver=solver, tlimit=tl)
            if v2: assert pattern(M, v2) == list(D) and max(v2) <= 1
        rec['exact'] = (st2, sz2); rec['seconds'] = round(time.time() - t0, 1)
        n += 1
        if has: okk = (st == 'optimal' and sz == full and st2 == 'optimal' and sz2 == full)
        else: okk = (st == 'infeasible')
        proved = st in ('optimal', 'infeasible') and st2 in ('optimal', 'infeasible')
        if okk: good += 1; rec['verdict'] = 'agrees'
        elif proved: bad += 1; rec['verdict'] = 'DIFFERS'
        else: unproved += 1; rec['verdict'] = 'not proved'
        print(json.dumps(rec), flush=True)
    print(f'# Z_{M} sets ({solver}, {tl:.0f} s each): {n} up-sets; as predicted {good}; proved different {bad}; not proved in time {unproved}; {time.time() - t00:.0f} s', flush=True)


if __name__ == '__main__':
    main()
