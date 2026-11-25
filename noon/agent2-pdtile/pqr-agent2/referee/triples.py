"""For many prime triples (in every order of the roles, since all 128 patterns are scanned):
 (1) Lemma 1 against exact D+: for every pattern Z and every nonempty U with every d in Z divisible by some p_x, x in U:
     D+(Z) <= prod_{x in U} p_x.
 (2) Lemma 2 against exact D+: for every pattern Z and every z with none of p_x p_y, p_z, M in Z: D+(Z) <= max(p_x, p_y).
 (3) the arithmetic of Section 5: every pattern falls into exactly one bullet (the classifier of analyse.py is a
     total function of the pattern), the upper bound U the bullet invokes is >= exact D+, and the bullet closes:
     'T1T2' bullets force n = prod_E p (U equals that product and it divides n) with (T2) true of the pattern;
     'contradiction' bullets have U < L (L = the bullet's lower bound for |A|); the mixed bullet has U = p_x.
 (4) by-product: list of patterns with D+(Z) an integer multiple of k(Z) that violate (T1) or (T2) ("dangerous"):
     these are the patterns for which the theorem needs a counting argument, and for each the gap L - D+.
"""
import sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/agent2_referee3')
from dplus import dplus, describe, BIT2SUB

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
PB = {frozenset((0, 1)): 3, frozenset((0, 2)): 4, frozenset((1, 2)): 5}

def EPt(mask):
    E = {w for w in range(3) if mask >> w & 1}
    P = {pr for pr, b in PB.items() if mask >> b & 1}
    return E, P, mask >> 6 & 1

def bullet(p, mask):
    M = p[0]*p[1]*p[2]
    E, P, t = EPt(mask)
    pr = lambda a, b: frozenset((a, b)) in P
    if len(E) == 3:
        return ("|E|=3", M, M, "A=Z_M")
    if len(E) == 2:
        x, y = sorted(E); U = p[x]*p[y]
        if pr(x, y): return ("E={x,y}; {x,y} in P", U, U, "T1T2")
        if not t: return ("E={x,y}; {x,y} not in P; t=0 (Lemma 2)", max(p[x], p[y]), U, "contradiction")
        return ("E={x,y}; {x,y} not in P; t=1 (Lemma 5)", U, U + 1, "contradiction")
    if len(E) == 1:
        (x,) = E; y, z = [w for w in range(3) if w != x]
        if not pr(y, z): return ("E={x}; {y,z} not in P", p[x], p[x], "T1T2")
        U = p[x]*min(p[y], p[z])
        if pr(x, y) or pr(x, z):
            Ls = []
            if pr(x, y): Ls.append(p[z]*p[x] + p[y])
            if pr(x, z): Ls.append(p[y]*p[x] + p[z])
            return ("E={x}; {y,z} in P; a second pair", U, min(Ls), "contradiction")   # min: weakest of the bullets that apply
        if not t:
            if p[x] > p[y] or p[x] > p[z]:
                return ("E={x}; P={{y,z}}; t=0; p_x not smallest", p[x], p[x], "T1T2")
            return ("E={x}; P={{y,z}}; t=0; p_x smallest", min(p[y], p[z]), p[y] + p[z], "contradiction")
        return ("E={x}; P={{y,z}}; t=1", U, U + 1, "contradiction")
    if mask == 0: return ("E=0; Z_A empty", 1, 1, "T1T2")
    if not P: return ("E=0; P=0; t=1", min(p), min(p) + 1, "contradiction")
    common = set.intersection(*[set(q) for q in P])
    if common:
        # the note: "some index x belongs to every pair of P" -- check the bullet for EVERY admissible choice of x and of the pair
        worstU = max(p[x] for x in common)
        worstL = min(p[x] + p[y] for x in common for q in P for y in q if y != x)
        return ("E=0; 1 or 2 pairs", worstU, worstL, "contradiction-each-x")
    s = sorted(p)
    return ("E=0; P = all three pairs", s[0]*s[1], s[0]*s[1] + 1, "contradiction")

def T2(mask):
    E, P, t = EPt(mask)
    return all(frozenset((a, b)) in P for a in E for b in E if a < b) and (len(E) < 3 or t)

ntr = 0; l1 = l1f = l2 = l2f = 0; bf = 0; uf = 0; dangerous = {}
labels = {}
for tr in itertools.combinations(primes, 3):
    p = tr; M = p[0]*p[1]*p[2]; ntr += 1
    D = {m: dplus(p, m) for m in range(128)}
    for mask in range(128):
        subs = [BIT2SUB[b] for b in range(7) if mask >> b & 1]
        # Lemma 1
        for U in range(1, 8):
            if all(s & U for s in subs):
                l1 += 1
                bound = 1
                for w in range(3):
                    if U >> w & 1: bound *= p[w]
                if D[mask] > bound: l1f += 1; print("LEMMA 1 FAIL", p, describe(p, mask), U, D[mask])
        # Lemma 2
        for z in range(3):
            x, y = [w for w in range(3) if w != z]
            if not (mask >> PB[frozenset((x, y))] & 1) and not (mask >> z & 1) and not (mask >> 6 & 1):
                l2 += 1
                if D[mask] > max(p[x], p[y]): l2f += 1; print("LEMMA 2 FAIL", p, describe(p, mask), z, D[mask])
        lab, U, L, verdict = bullet(p, mask)
        labels[lab] = labels.get(lab, 0) + 1
        if D[mask] > U: uf += 1; print("BULLET U FAIL", p, describe(p, mask), lab, D[mask], U)
        E, P, t = EPt(mask)
        k = 1
        for w in E: k *= p[w]
        if verdict == "A=Z_M":
            pass   # M | n <= M forces A = Z_M, whose pattern is the full one: nothing about D+ is used
        elif verdict == "T1T2":
            # n <= U, k | n, U == k  =>  n = k ; and (T2) must be true of the pattern
            if not (U == k and T2(mask)): bf += 1; print("BULLET LOGIC FAIL", p, describe(p, mask), lab)
        else:
            if not (U < L): bf += 1; print("BULLET LOGIC FAIL", p, describe(p, mask), lab, U, L)
        # dangerous patterns: D+ integer, k | D+, and (T1) or (T2) fails
        d = D[mask]
        if d.denominator == 1 and d.numerator % k == 0 and not (d == k and T2(mask)):
            dangerous.setdefault(lab, []).append((p, describe(p, mask), int(d), L))
print(f"triples of primes <= {primes[-1]}: {ntr}")
print(f"Lemma 1: {l1} (pattern, U) instances checked against exact D+, failures {l1f}")
print(f"Lemma 2: {l2} (pattern, z) instances checked against exact D+, failures {l2f}")
print(f"Section 5: bullet upper bound < exact D+ : {uf} ; bullets whose arithmetic does not close: {bf}")
print("patterns per bullet (summed over triples):")
for lab, c in sorted(labels.items()): print(f"   {lab:45s} {c}")
print("dangerous patterns (D+ an integer multiple of k(Z) but (T1) or (T2) false), by bullet; these are where the")
print("theorem genuinely needs the counting lemmas.  count, and the smallest margin L - D+ :")
for lab, lst in sorted(dangerous.items()):
    mm = min(lst, key=lambda r: r[3] - r[2])
    print(f"   {lab:45s} {len(lst):6d}   min margin {mm[3]-mm[2]} at {mm}")
