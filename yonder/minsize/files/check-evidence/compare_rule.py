# Compares (1) the least number of marks found by exhaustive enumeration (enum.c) with
# (2) the rule as the PAGE words it (section "The answer"), programmed in rules.py from the page's words only, and
# (3) Theorem 1 of the paper with its four clauses (programmed separately in rules.py, from the paper).
import math
from itertools import combinations
from polylib import divisors, pattern_exact
from rules import page_rule, theorem1, read_enum, presentations

def main(cases):
    rows = []
    for M, S in cases:
        best, nodes = read_enum(M, S)
        expected_nodes = math.comb(M + S - 1, S - 1)   # multisets of size <= S containing hour 0
        ds = [d for d in divisors(M) if d > 1]
        allpats = [frozenset(c) for r in range(len(ds) + 1) for c in combinations(ds, r)]
        # every witness re-divided exactly in Python
        for pat, (size, marks) in best.items():
            assert len(marks) == size and pattern_exact(marks, M) == pat, (M, pat, marks)
        for (p, n, q) in presentations(M):
            exact_ok = exact_bad = two_ok = two_bad = notreached_ok = notreached_bad = thm_bad = 0
            x1_cases = 0; bad = []
            for pat in allpats:
                allowed = page_rule(M, p, n, q, pat)
                thm = theorem1(M, p, n, q, pat)
                if thm not in allowed: thm_bad += 1; bad.append(("page!=theorem", sorted(pat), sorted(allowed), thm))
                if pat in best:
                    found = best[pat][0]
                    if found != thm: thm_bad += 1; bad.append(("search!=theorem", sorted(pat), found, thm))
                    if q not in pat:
                        if allowed == {found}: exact_ok += 1
                        else: exact_bad += 1; bad.append(("case1", sorted(pat), found, sorted(allowed)))
                    else:
                        if found in allowed: two_ok += 1
                        else: two_bad += 1; bad.append(("case2", sorted(pat), found, sorted(allowed)))
                        if len(allowed) == 2 and found == max(allowed): x1_cases += 1
                else:
                    # no marking with this pattern and <= S marks: consistent iff every allowed value is > S
                    if min(allowed) > S and thm > S: notreached_ok += 1
                    else: notreached_bad += 1; bad.append(("not reached", sorted(pat), sorted(allowed)))
            rows.append((M, p, n, q, S, nodes, expected_nodes, len(allpats), len(best), exact_ok, exact_bad, two_ok, two_bad, x1_cases, notreached_ok, notreached_bad, thm_bad))
            print(f"clock {M} = {p}^{n}*{q}: all multisets with <= {S} marks containing hour 0: {nodes} (expected C({M+S-1},{S-1}) = {expected_nodes}, {'equal' if nodes == expected_nodes else 'DIFFERENT'});"
                  f" patterns {len(allpats)}, settled {len(best)};"
                  f" first case: page value = least found {exact_ok}, not {exact_bad};"
                  f" second case: least found is one of the page's values {two_ok}, not {two_bad} (x = 1 needed in {x1_cases});"
                  f" not reached with <= {S} marks and page value > {S}: {notreached_ok}, page value <= {S}: {notreached_bad};"
                  f" disagreements with Theorem 1 as printed: {thm_bad}")
            for b in bad: print("   BAD", b)

if __name__ == "__main__":
    main([(6, 6), (10, 10), (12, 18), (18, 18), (20, 20), (24, 18)])
