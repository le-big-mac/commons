# The least-size statements on Z_{p^n q s}, directly on the big group, for the instances whose Lean value V lies beyond the
# census of that group: the integer programme of t5_cpsat.py with ALL the clauses of the statement (the divisors d | p^n q as the
# pattern says, and every d | p^n q s with d not dividing p^n q forbidden), minimising the size.  Nothing is taken from the
# base group here.  A result counts as "equal" only if the solver reports a proved optimum equal to V, and the multiset it
# returns passes the transcribed clauses by long division.
# usage: t6_direct.py <time limit per instance, seconds> p q n s [p q n s ...]
import sys, os, json, time
from core import divisors, pattern_slow
from t4_minsize import parse_lean, hypotheses, holds, load
from t5_cpsat import base_pattern, solve

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    tlimit = float(sys.argv[1])
    args = [int(x) for x in sys.argv[2:]]
    rows = parse_lean(os.path.join(HERE, 'A3_rule_eval.out'))
    tot = dict(instances=0, equal=0, notproved=0, bad=0)
    t00 = time.time()
    for i in range(0, len(args), 4):
        p, q, n, s = args[i:i + 4]
        M0 = p ** n * q
        M = M0 * s
        c = load(M)
        S = c['S'] if c else 0
        cnt = dict(instances=0, equal=0, notproved=0, bad=0)
        for (kind, p_, q_, n_, Es, Fs, a0, V) in rows:
            if (p_, q_, n_) != (p, q, n) or not hypotheses(kind, n, Es, Fs, a0) or V <= S:
                continue
            need, _ = base_pattern(kind, p, q, n, Es, Fs)
            forbid = [d for d in divisors(M) if d > 1 and d not in need]
            assert holds(kind, p, q, n, s, Es, Fs, set(need))
            name = f"{kind} Es={sorted(Es)}" + ("" if kind == 'A' else f" Fs={sorted(Fs)}") + (f" a0={a0}" if kind == 'B' else "")
            t0 = time.time()
            st, el, bound = solve(M, need, forbid, None, V, tlimit)
            cnt['instances'] += 1
            if el is not None:
                assert holds(kind, p, q, n, s, Es, Fs, pattern_slow(el, M))
            if st == 'OPTIMAL' and len(el) == V:
                cnt['equal'] += 1
                print(f"   {p} {q} {n} {s} Z_{M} {name}: Lean {V}; least = {V} proved [{time.time() - t0:.0f}s]", flush=True)
            elif st == 'INFEASIBLE' or (el is not None and len(el) < V) or (st == 'OPTIMAL' and len(el) != V):
                cnt['bad'] += 1
                print(f"   {p} {q} {n} {s} Z_{M} {name}: Lean {V}; DISAGREE: status {st}, multiset {el}", flush=True)
            else:
                cnt['notproved'] += 1
                print(f"   {p} {q} {n} {s} Z_{M} {name}: Lean {V}; not proved in {tlimit:.0f}s: member of size "
                      f"{None if el is None else len(el)} found, solver's lower bound {bound}", flush=True)
        for k in tot:
            tot[k] += cnt[k]
        print(f"{p} {q} {n} {s} | Z_{M} | census bound S={S} | instances with Lean value > S: {cnt['instances']} | least = Lean value, "
              f"proved: {cnt['equal']} | not proved in time: {cnt['notproved']} | DISAGREEMENTS: {cnt['bad']}", flush=True)
    print(f"TOTAL {tot} [{time.time() - t00:.0f}s]")
