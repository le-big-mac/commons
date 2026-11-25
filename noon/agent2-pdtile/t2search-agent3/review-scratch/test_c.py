"""(c) cuboid criterion and the normalisation of the witness, M = 72 and 108 (and 36, 144, 200 for good measure).
For each (i, j):  N = counts of A modulo p^i q^j in CRT coordinates (u, v) = (x mod p^i, x mod q^j).
  cub(c; s, t) = N(c) - N(c + s e1) - N(c + t e2) + N(c + s e1 + t e2),  e1 = (p^(i-1), 0), e2 = (0, q^(j-1)), s = 1..p-1, t = 1..q-1.
 (i)   divides(p^i q^j, A, M)  <=>  all cub = 0                         [also: <=> all cub with s = t = 1 vanish]
 (ii)  if not: some translate / unit multiple B of A has  wit . 1_B >= 1  with wit exactly as built in t2search.py;
       and B has the same size and the same exact zero set as A.     [also recorded: whether a translate ALONE suffices]"""
import sys, random, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from common import *
random.seed(5); np.random.seed(5)
def wit_vector(M, p, q, i, j):
    # copied verbatim in substance from t2search.py lines 112-114
    X = np.arange(M); ui = X % p ** i; vj = X % q ** j
    N = lambda u, v: ((ui == u % p ** i) & (vj == v % q ** j)).astype(float)
    return N(0, 0) - N(p ** (i - 1), 0) - N(0, q ** (j - 1)) + N(p ** (i - 1), q ** (j - 1))
def counts(A, p, q, i, j):
    N = np.zeros((p ** i, q ** j), dtype=np.int64)
    for x in A: N[x % p ** i, x % q ** j] += 1
    return N
def cuboids(N, p, q, i, j):
    """dict (s, t) -> array of cub(c; s, t) over all c"""
    out = {}
    for s in range(1, p):
        for t in range(1, q):
            Ns = np.roll(N, -s * p ** (i - 1), axis=0); Nt = np.roll(N, -t * q ** (j - 1), axis=1); Nst = np.roll(Ns, -t * q ** (j - 1), axis=1)
            out[(s, t)] = N - Ns - Nt + Nst
    return out
def random_with_zeros(M, k, Zreq, RES):
    """a random set of size k with Phi_d | A for d in Zreq (0/1 programme with a random objective), or None"""
    rows = [np.ones((1, M))] + [RES[d] for d in Zreq]; Am = np.vstack(rows).astype(float); rhs = np.zeros(Am.shape[0]); rhs[0] = k
    r = milp(c=np.random.randn(M), constraints=LinearConstraint(Am, rhs, rhs), integrality=np.ones(M), bounds=Bounds(np.zeros(M), np.ones(M)), options={"time_limit": 20})
    if r.x is None: return None
    A = [x for x in range(M) if r.x[x] > 0.5]
    return A if len(A) == k and all(divides(d, A, M) for d in Zreq) else None
for (p, a, q, b) in [(2, 3, 3, 2), (2, 2, 3, 3), (2, 2, 3, 2), (2, 4, 3, 2), (2, 3, 5, 2), (3, 2, 5, 1), (5, 1, 7, 1)]:
    M = p ** a * q ** b; U = units(M); divs = [d for d in divisors(M) if d > 1]
    RES = {d: residues(d, M) for d in divs}
    stats = dict(sets=0, tests=0, div=0, nondiv=0, crit_ok=0, st11_ok=0, norm_ok=0, transl_only_ok=0, bad=0, nondiv_with_both_pp_zeros=0)
    pool = []
    nrand = 400 if M <= 108 else 120
    for _ in range(nrand): pool.append(sorted(random.sample(range(M), random.randint(1, M - 1))))
    # sets built from cosets (many zeros), and perturbations
    for _ in range(nrand):
        A = set()
        for _ in range(random.randint(1, 3)):
            r = random.choice([d for d in divs if d < M]); H = [(M // r) * t for t in range(r)]
            for _ in range(random.randint(1, max(1, M // r // 2))):
                c = random.randrange(M); co = {(c + h) % M for h in H}
                if not (co & A): A |= co
        if random.random() < 0.3: A ^= {random.randrange(M)}
        if A: pool.append(sorted(A))
    # sets with prescribed zeros from a 0/1 programme: p^i and q^j zeros (the situation of the search), with or without further zeros
    nsolve = 0
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            for rep in range(12 if M <= 108 else 4):
                extra = random.sample([d for d in divs if d not in (p ** i, q ** j, p ** i * q ** j)], random.randint(0, 3)) if rep % 2 else []
                k = p * q * random.randint(1, max(1, M // (p * q) - 1))
                A = random_with_zeros(M, k, [p ** i, q ** j] + extra, RES)
                if A is not None: pool.append(A); nsolve += 1
                if rep % 3 == 0:
                    A = random_with_zeros(M, k, [p ** i * q ** j] + extra, RES)
                    if A is not None: pool.append(A); nsolve += 1
    for A in pool:
        stats["sets"] += 1; ZA = zeros_exact(A, M); assert ZA == zeros_numeric(A, M)
        for i in range(1, a + 1):
            for j in range(1, b + 1):
                d0 = p ** i * q ** j; N = counts(A, p, q, i, j); cub = cuboids(N, p, q, i, j)
                allzero = all(not np.any(v) for v in cub.values()); zero11 = not np.any(cub[(1, 1)])
                dv = d0 in ZA; stats["tests"] += 1; stats["div" if dv else "nondiv"] += 1
                stats["crit_ok"] += (dv == allzero); stats["st11_ok"] += (dv == zero11)
                if dv != allzero or dv != zero11: stats["bad"] += 1; print("CRITERION FAILS", M, i, j, A)
                if not dv:
                    if p ** i in ZA and q ** j in ZA: stats["nondiv_with_both_pp_zeros"] += 1
                    w = wit_vector(M, p, q, i, j); x = np.zeros(M); x[A] = 1
                    # translate alone
                    tr = next((t for t in range(M) if w @ np.roll(x, -t) >= 1), None)
                    stats["transl_only_ok"] += tr is not None
                    found = None
                    for u in ([1] + [v for v in U if v != 1]):
                        for t in range(M):
                            B = sorted((u * y - t) % M for y in A)
                            xb = np.zeros(M); xb[B] = 1
                            if w @ xb >= 1: found = B; break
                        if found: break
                    if found is None: stats["bad"] += 1; print("NO NORMALISED WITNESS", M, i, j, A); continue
                    assert len(found) == len(A) and zeros_exact(found, M) == ZA, "symmetry changed size or zeros"
                    stats["norm_ok"] += 1
    print(f"M = {M} = {p}^{a} {q}^{b}: {stats['sets']} sets ({nsolve} from 0/1 programmes with prescribed zeros), {stats['tests']} (set, i, j) tests: "
          f"{stats['div']} divisible / {stats['nondiv']} not;  criterion 'all cuboids vanish' agrees in {stats['crit_ok']}, with s = t = 1 only in {stats['st11_ok']};  "
          f"normalised witness found in {stats['norm_ok']} of {stats['nondiv']} (by a translation alone in {stats['transl_only_ok']});  "
          f"non-divisible cases with p^i and q^j both zeros: {stats['nondiv_with_both_pp_zeros']};  failures: {stats['bad']}", flush=True)
