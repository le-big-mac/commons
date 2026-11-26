# For patterns that the plain enumeration (enum.c) did not reach: per-pattern exhaustive search (perpat.c)
# up to the largest value the page allows, for patterns whose free dimension f makes that feasible.
import sys, subprocess, math
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor
from polylib import *
from rules import page_rule, theorem1, read_enum, presentations

MAXLEAVES = float(sys.argv[1]) if len(sys.argv) > 1 else 3e9

def job(M, pat, B):
    ds = [d for d in divisors(M) if d > 1]
    G = [1]
    for d in pat: G = polymul(G, list(cyclo(d)))
    D = len(G) - 1; f = M - D
    others = [d for d in ds if d not in pat]
    lines = [f"{M} {D} {f} {B}", " ".join(map(str, G)), str(len(others))]
    for d in others:
        phi = len(cyclo(d)) - 1; lines.append(str(phi))
        for h in range(M):
            _, r = polydivmod([0] * h + [1], list(cyclo(d))); r = r + [0] * (phi - len(r))
            lines.append(" ".join(map(str, r)))
    out = subprocess.run(["./perpat"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.strip()
    return out

todo = []
for M, S in [(20, 20), (24, 18)]:
    best, _ = read_enum(M, S)
    ds = [d for d in divisors(M) if d > 1]
    (p, n, q), = presentations(M)
    for r in range(len(ds) + 1):
        for c in combinations(ds, r):
            pat = frozenset(c)
            if pat in best: continue
            allowed = page_rule(M, p, n, q, pat); B = max(allowed)
            D = sum(len(cyclo(d)) - 1 for d in pat); f = M - D
            leaves = math.comb(B + f, f)
            todo.append((M, p, n, q, pat, allowed, B, f, leaves))
todo.sort(key=lambda t: t[-1])
run = [t for t in todo if t[-1] <= MAXLEAVES]
with ThreadPoolExecutor(8) as ex:
    outs = list(ex.map(lambda t: job(t[0], sorted(t[4]), t[6]), run))
res = dict(zip([(t[0], t[4]) for t in run], outs))
ok = bad = skipped = 0
for (M, p, n, q, pat, allowed, B, f, leaves) in todo:
    thm = theorem1(M, p, n, q, pat)
    if (M, pat) not in res:
        skipped += 1
        print(f"clock {M} pattern {sorted(pat)}: page allows {sorted(allowed)}, Theorem 1 says {thm}; NOT SEARCHED beyond the plain enumeration (free dimension {f}, {leaves:.2e} candidates)")
        continue
    out = res[(M, pat)]
    if out.startswith("least"):
        found = int(out.split()[1]); marks = [int(x) for x in out.split("marks")[1].split()]
        assert len(marks) == found and pattern_exact(marks, M) == pat      # witness divided again in Python
        verdict = "one of the page's values" if found in allowed else "NOT a value the page allows"
        if found in allowed and found == thm: ok += 1
        else: bad += 1
        print(f"clock {M} pattern {sorted(pat)}: least number {found} ({verdict}; page allows {sorted(allowed)}; Theorem 1 says {thm}); candidates tried {out.split()[3]}; a marking: {marks}")
    else:
        bad += 1
        print(f"clock {M} pattern {sorted(pat)}: NO marking with <= {B} marks; page allows {sorted(allowed)}", out)
print(f"settled and agreeing with the page (and equal to Theorem 1's value): {ok}; disagreeing: {bad}; not searched: {skipped}")
