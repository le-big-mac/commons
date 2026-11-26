"""Theorem 1 against exhaustive search.

Runs dp.c (all classes with at most B elements) and compares, for every pattern of Z_{p^n q}
(and of Z_{p^j q}, j < n, which the same run contains), the least size of a NONEMPTY multiset
with exactly that pattern against the formula of Theorem 1 as printed (lib.theorem_value).
Patterns whose formula value exceeds B are checked one-sidedly: no multiset with <= B elements.
usage: t3_theorem.py p q n B
"""
import sys, subprocess, os
from lib import theorem_value, all_patterns, clauses


def read_dp(p, q, n, B):
    fn = f"dpout/dp-{p}-{q}-{n}-B{B}.txt"
    if not os.path.exists(fn):
        with open(fn, "w") as f:
            subprocess.run(["./dp", str(p), str(q), str(n), str(B)], stdout=f, check=True)
    table = {}
    for line in open(fn):
        t = list(map(int, line.split()))
        j = t[0]
        E = frozenset(l for l in range(1, j + 1) if t[1] >> (l - 1) & 1)
        F = frozenset(l for l in range(1, j + 1) if t[2] >> (l - 1) & 1)
        table[(j, E, F, bool(t[3]))] = t[4:]
    return table


def main():
    p, q, n, B = map(int, sys.argv[1:5])
    table = read_dp(p, q, n, B)
    for j in range(0, n + 1):
        M = p ** j * q
        decided = onesided = bad = 0
        clause_seen = {"b": 0, "c1": 0, "c2": 0, "c3": 0, "c4": 0, "several": 0, "x1": 0, "a_k0": 0, "a_k>0": 0}
        badlist = []
        for E, F, bal in all_patterns(j):
            want = theorem_value(p, q, j, E, F, bal)
            sizes = [s for s in table.get((j, E, F, bal), []) if s > 0]
            got = min(sizes) if sizes else None
            if want <= B:
                decided += 1
                if got != want:
                    bad += 1
                    badlist.append((sorted(E), sorted(F), bal, want, got))
                else:
                    if not bal:
                        clause_seen["a_k0" if F <= E else "a_k>0"] += 1
                    else:
                        cl = clauses(p, q, j, E, F)
                        if cl is None:
                            clause_seen["b"] += 1
                        elif not any(cl):
                            clause_seen["x1"] += 1
                        elif sum(cl) == 1:
                            clause_seen[f"c{cl.index(True)+1}"] += 1
                        else:
                            clause_seen["several"] += 1
            else:
                onesided += 1
                if got is not None:
                    bad += 1
                    badlist.append((sorted(E), sorted(F), bal, want, got))
        print(f"p={p} q={q} n={j} Z_{M} B={B}: patterns {2**(2*j+1)}; least size found = formula: {decided - bad if bad==0 else 'SEE BELOW'} "
              f"of {decided} decided; formula > B and none found <= B: {onesided}; disagreements: {bad}; "
              f"decided patterns by case (c_i = clause (i) of part (c) is the only clause that holds): {clause_seen}")
        for b in badlist:
            print("   DISAGREE (E, F, balanced, formula, found):", b)


if __name__ == "__main__":
    main()
