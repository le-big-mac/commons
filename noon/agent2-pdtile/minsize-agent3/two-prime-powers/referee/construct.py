"""The construction of the sets proposition, (b)/(c), on larger groups, and the pattern of a sum of one coset for each corner
under OTHER shifts (the question the note leaves open for four or more corners).

For M = p^n q^m and every up-set D with at least KMIN corners:
  (A) if a prime divides every corner: the shifts of (b) (the common prime is called p, corners numbered by increasing
      exponent of p, x_i = p^i in the p-coordinate and 0 in the other): are the cosets pairwise disjoint, is the union's
      size the sum of M/c, is its pattern exactly D (referee's cuboid test)?
  (B) if no prime divides every corner: do the first and last corner's cosets meet for every pair of shifts (gcd = 1)?
  (C) shifts 0: pattern exactly D?
  (D) NR random shift tuples (any up-set with at least two corners): is the pattern exactly D each time?
  (E) with 'all': EVERY shift tuple (the first shift fixed at 0 by translation), for the up-sets with at least KMIN corners.

usage: construct.py p n q m KMIN NR [all]
"""
import sys, json, random, time, itertools, math
from lib import prime_factors


def upsets_staircase(p, n, q, m):
    """up-sets of the divisors of p^n q^m, 1 not in D: thresholds t_0 >= t_1 >= ... >= t_n in [0, m+1]; D = {p^u q^v : v >= t_u}"""
    out = []
    def rec(u, prev, ts):
        if u > n:
            if ts[0] != 0: out.append(tuple(ts))
            return
        for t in range(0, prev + 1): rec(u + 1, t, ts + [t])
    rec(0, m + 1, [])
    return out


def corners_of(p, n, q, m, ts):
    """maximal elements of the complement {p^u q^v : v < t_u}"""
    cs = []
    for u in range(n + 1):
        if ts[u] == 0: continue
        v = ts[u] - 1
        # maximal iff p^{u+1} q^v is not in the complement, i.e. u = n or v >= t_{u+1}
        if u == n or v >= ts[u + 1]: cs.append((u, v))
    return cs


def divides_sparse(M, d, pts):
    """Phi_d | A for A given as dict point -> multiplicity (cuboid criterion)"""
    B = {}
    for x, w in pts.items():
        y = x % d; B[y] = B.get(y, 0) + w
    for pr in prime_factors(d):
        s = d // pr; N = {}
        for y, w in B.items():
            N[y] = N.get(y, 0) + w
            y2 = (y + s) % d; N[y2] = N.get(y2, 0) - w
        B = {y: w for y, w in N.items() if w}
    return not B


def pattern_sparse(M, divs, pts):
    return [d for d in divs if divides_sparse(M, d, pts)]


def union(M, corners, shifts):
    pts = {}
    for c, x in zip(corners, shifts):
        for y in range(x % c, M, c): pts[y] = pts.get(y, 0) + 1
    return pts


def main():
    p, n, q, m, KMIN, NR = (int(t) for t in sys.argv[1:7]); ALL = len(sys.argv) > 7
    M = p ** n * q ** m; random.seed(M)
    divs = sorted(p ** u * q ** v for u in range(n + 1) for v in range(m + 1) if u + v > 0)
    ups = upsets_staircase(p, n, q, m); assert len(ups) == math.comb(n + m + 2, n + 1) - 1
    cnt = dict(upsets=len(ups), two_or_more_corners=0, with_KMIN=0, common_prime=0, A_ok=0, coprime=0, B_ok=0, C_ok=0, D_tuples=0, D_ok=0, E_tuples=0, E_ok=0)
    worst = []; t0 = time.time()
    for ts in ups:
        D = sorted(p ** u * q ** v for u in range(n + 1) for v in range(ts[u], m + 1))
        cs = corners_of(p, n, q, m, ts)                           # exponent pairs, exponent of p increasing
        C = [p ** u * q ** v for u, v in cs]; K = len(C); full = sum(M // c for c in C)
        # (C) shifts 0
        if K >= 2:
            cnt['two_or_more_corners'] += 1
            pat = pattern_sparse(M, divs, union(M, C, [0] * K))
            cnt['C_ok'] += (pat == D)
            if pat != D: worst.append(('shifts 0', C, pat))
            for _ in range(NR):
                sh = [random.randrange(c) for c in C]
                pat = pattern_sparse(M, divs, union(M, C, sh)); cnt['D_tuples'] += 1
                if pat == D: cnt['D_ok'] += 1
                else: worst.append(('random shifts', C, sh, [d for d in pat if d not in D]))
        if K < KMIN: continue
        cnt['with_KMIN'] += 1
        g = 0
        for c in C: g = math.gcd(g, c)
        if g > 1 or K == 1:
            cnt['common_prime'] += 1
            if K == 1: sh = [0]
            else:
                if all(u >= 1 for u, v in cs): P, e, order = p, n, list(range(K))             # exponent of p increasing with the index
                else: P, e, order = q, m, list(range(K - 1, -1, -1))                          # exponent of q increasing along the reversed order
                Pn = P ** e; rest = M // Pn; inv = pow(rest, -1, Pn) if Pn > 1 else 0
                sh = [0] * K
                for i, idx in enumerate(order): sh[idx] = (rest * inv * pow(P, i, Pn)) % M   # = P^i mod P^e, 0 mod the other part
            pts = union(M, C, sh)
            is_set = max(pts.values()) == 1 and len(pts) == full
            pat = pattern_sparse(M, divs, pts)
            if is_set and pat == D: cnt['A_ok'] += 1
            else: worst.append(('construction', C, sh, is_set, pat == D))
        else:
            cnt['coprime'] += 1
            # first and last corners coprime: their cosets meet whatever the shifts (checked on all pairs of shifts if small, else 200 random)
            c0, c1 = C[0], C[-1]; ok = math.gcd(c0, c1) == 1
            pairs = itertools.product(range(c0), range(c1)) if c0 * c1 <= 4000 else [(random.randrange(c0), random.randrange(c1)) for _ in range(200)]
            for x0, x1 in pairs:
                if not (set(range(x0, M, c0)) & set(range(x1, M, c1))): ok = False; break
            cnt['B_ok'] += ok
            if not ok: worst.append(('coprime corners with disjoint cosets', C))
        if ALL:
            for sh in itertools.product(*[range(c) for c in C[1:]]):
                pat = pattern_sparse(M, divs, union(M, C, (0,) + sh)); cnt['E_tuples'] += 1
                if pat == D: cnt['E_ok'] += 1
                else: worst.append(('some shifts', C, sh, [d for d in pat if d not in D]))
    cnt['seconds'] = round(time.time() - t0, 1)
    print(json.dumps(dict(M=M, p=p, n=n, q=q, m=m, KMIN=KMIN, counts=cnt, failures=worst[:10])), flush=True)


if __name__ == '__main__':
    main()
