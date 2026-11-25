"""Do the facts used in Section 5 of agent2's pqr-agent2.md suffice for EVERY pattern and EVERY ordering of the primes?  (agent3 / Yonder)
For each triple of distinct primes and each of the 128 patterns (E, P, t), collect every constraint on n = |A| that the note's lemmas
give for a pd-tiling set with that pattern, transcribed from the lemma STATEMENTS (not from the case tree):
   divisibility   prod_{x in E} p_x | n
   Lemma 1        n <= prod_{x in U} p_x  for every nonempty U meeting every element of Z_A           (needs Z_A nonempty)
   Lemma 2        n <= max(p_x, p_y)      whenever p_x p_y, p_z, M are all outside Z_A
   Lemma 3        n >= p_x + p_y          whenever {x,y} in P, x and y not in E
   Lemma 5        n != p_x p_y            whenever x, y in E, t = 1, {x,y} not in P
   sub-case (S1)  n >= p_z p_x + p_y      whenever x in E, y and z not in E, {y,z} in P, {x,y} in P
   sub-case (S2)  n >  p_x min(p_y, p_z)  whenever x in E, y and z not in E, {y,z} in P, t = 1
   sub-case (S3)  n >  p_min or n >= p_max   when Z_A = {M}
   sub-case (S4)  n >= min( min over pairs of p_x p_y + p_x + p_y,  max over x of p_y p_z + p_x )   when E is empty and P has all three pairs
   empty pattern  n = 1
   whole group    n = M only for the full pattern (the note's case |E| = 3)
Then every n in 1..M that survives must satisfy (T1) and (T2).  If the case analysis had a hole for some ordering, a survivor would show it.
With --drop NAME one family of constraints is left out, to see that each is needed (a control on the check itself)."""
import sys, itertools
drop = sys.argv[sys.argv.index("--drop") + 1] if "--drop" in sys.argv else None
primes = [p for p in range(2, 48) if all(p % q for q in range(2, p))]
PAIRS = [(0, 1), (0, 2), (1, 2)]
def survivors(pr, E, P, t):
    M = pr[0] * pr[1] * pr[2]; k = 1
    for x in E: k *= pr[x]
    Z = [frozenset([x]) for x in E] + [frozenset(pq) for pq in P] + ([frozenset([0, 1, 2])] if t else [])
    if not Z: return [1]
    hi = M; lo = 1; excl = set(); conds = []
    if drop != "L1":
        for r in (1, 2, 3):
            for U in itertools.combinations(range(3), r):
                if all(d & set(U) for d in Z):
                    b = 1
                    for x in U: b *= pr[x]
                    hi = min(hi, b)
    for z in range(3):
        x, y = [w for w in range(3) if w != z]
        if drop != "L2" and (x, y) not in P and z not in E and not t: hi = min(hi, max(pr[x], pr[y]))
        if drop != "L3" and (x, y) in P and x not in E and y not in E: lo = max(lo, pr[x] + pr[y])
        if drop != "L5" and x in E and y in E and t and (x, y) not in P: excl.add(pr[x] * pr[y])
    for x in range(3):
        y, z = [w for w in range(3) if w != x]
        if x in E and y not in E and z not in E and (y, z) in P:
            if drop != "S1":
                if tuple(sorted((x, y))) in P: lo = max(lo, pr[z] * pr[x] + pr[y])
                if tuple(sorted((x, z))) in P: lo = max(lo, pr[y] * pr[x] + pr[z])
            if drop != "S2" and t: lo = max(lo, pr[x] * min(pr[y], pr[z]) + 1)
    if drop != "S3" and not E and not P and t: conds.append(lambda n: n > min(pr) or n >= max(pr))
    if drop != "S4" and not E and len(P) == 3:
        lo = max(lo, min(min(pr[x] * pr[y] + pr[x] + pr[y] for x, y in PAIRS), max(pr[y] * pr[z] + pr[x] for x in range(3) for y, z in [[w for w in range(3) if w != x]])))
    if drop != "FULL" and len(Z) < 7: hi = min(hi, M - 1)          # a set with M elements is Z_M, whose pattern is everything
    first = ((max(lo, 1) + k - 1) // k) * k
    return [n for n in range(first, hi + 1, k) if n not in excl and all(c(n) for c in conds)]
def T12(pr, E, P, t, n):
    k = 1
    for x in E: k *= pr[x]
    return n == k and all(pq in P for pq in itertools.combinations(sorted(E), 2)) and not (len(E) == 3 and not t)
n_tr = holes = with_surv = 0; example = None
for pr in itertools.combinations(primes, 3):
    for perm in itertools.permutations(pr):                         # every assignment of sizes to the coordinates
        n_tr += 1
        for code in range(128):
            E = tuple(x for x in range(3) if code >> x & 1); P = tuple(PAIRS[q] for q in range(3) if code >> (3 + q) & 1); t = code >> 6 & 1
            sv = survivors(perm, E, P, t); with_surv += bool(sv)
            bad = [n for n in sv if not T12(perm, E, P, t, n)]
            if bad:
                holes += 1
                if example is None: example = (perm, E, P, t, bad[:3])
print(f"{len(primes)} primes below 48: {n_tr} ordered triples x 128 patterns = {n_tr * 128} cases" + (f"   [constraint family {drop} left out]" if drop else ""))
print(f"   cases with a surviving n: {with_surv};  cases where a survivor violates (T1) or (T2): {holes}" + (f"   first: primes {example[0]}, E = {[example[0][x] for x in example[1]]}, P = {[(example[0][a], example[0][b]) for a, b in example[2]]}, t = {example[3]}, n = {example[4]}" if example else ""))
