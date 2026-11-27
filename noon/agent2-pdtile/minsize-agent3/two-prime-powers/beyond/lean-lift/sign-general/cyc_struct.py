# cyc_struct.py -- structured sets in Z_n (unions of cosets of subgroups, product sets, with a few points
# changed): is "all +" good, is some single turn good, and if not, all signings by enumeration (|B| <= 18).
# "good" = remainder of the signed mask modulo Phi_d is nonzero for every d | n.  Exact integers.
import sys, random, itertools
import numpy as np
from sympy import divisors, cyclotomic_poly, Poly, symbols, factorint
X = symbols('X')
def reduction(d):
    """integer matrix R (phi(d) x d): column j = coefficients of X^j mod Phi_d"""
    phi = Poly(cyclotomic_poly(d, X), X); deg = phi.degree()
    c = [int(a) for a in phi.all_coeffs()][::-1]            # c[0..deg], monic
    R = np.zeros((max(deg, 1), d), dtype=np.int64)
    if deg == 0: return R
    cur = np.zeros(deg, dtype=np.int64); cur[0] = 1
    for j in range(d):
        R[:, j] = cur
        top = cur[deg - 1]; nxt = np.zeros(deg, dtype=np.int64); nxt[1:] = cur[:-1]
        nxt -= top * np.array(c[:deg], dtype=np.int64); cur = nxt
    return R
def main():
    n = int(sys.argv[1]); trials = int(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    rnd = random.Random(seed)
    ds = divisors(n); Rs = {d: reduction(d) for d in ds}
    primes = sorted(factorint(n))
    def resid(B):  # dict d -> residue vector of the all-plus mask
        out = {}
        for d in ds:
            f = np.zeros(d, dtype=np.int64)
            for x in B: f[x % d] += 1
            out[d] = Rs[d] @ f
        return out
    def gen():
        kind = rnd.randrange(5)
        B = set()
        if kind == 0:    # union of a few cosets of subgroups of prime order
            for _ in range(rnd.randrange(1, 5)):
                p = rnd.choice(primes); a = rnd.randrange(n); B |= {(a + i * (n // p)) % n for i in range(p)}
        elif kind == 1:  # product set: residues allowed modulo each prime power part
            parts = [p ** e for p, e in factorint(n).items()]
            allowed = [set(rnd.sample(range(q), rnd.choice([1, 1, 2, 3, q]) if q >= 3 else 1)) for q in parts]
            B = {x for x in range(n) if all(x % q in A for q, A in zip(parts, allowed))}
            if len(B) > 60: B = set(rnd.sample(sorted(B), 60))
        elif kind == 2:  # two points in one class modulo d, plus cosets (the shape 2 delta_c + cosets modulo d)
            d = rnd.choice([t for t in ds if 1 < t < n]); c = rnd.randrange(n)
            B = {c, (c + d * rnd.randrange(1, n // d)) % n}
            for _ in range(rnd.randrange(1, 4)):
                p = rnd.choice(primes); a = rnd.randrange(n); B |= {(a + i * (n // p)) % n for i in range(p)}
        elif kind == 3:  # one point from each class modulo p, constrained modulo the other primes
            p = rnd.choice(primes); q = rnd.choice(primes)
            B = set()
            for i in range(p):
                x = rnd.randrange(n); x = x - (x % p) + i
                if rnd.random() < 0.7: x = x - (x % q) * 0
                B.add(x % n)
            for _ in range(rnd.randrange(0, 3)):
                pp = rnd.choice(primes); a = rnd.randrange(n); B |= {(a + i * (n // pp)) % n for i in range(pp)}
        else:            # small sum set A + H, H a subgroup of prime order, A a few points
            p = rnd.choice(primes); A = [rnd.randrange(n) for _ in range(rnd.randrange(1, 4))]
            B = {(a + i * (n // p)) % n for a in A for i in range(p)}
            B |= {rnd.randrange(n) for _ in range(rnd.randrange(0, 3))}
        for _ in range(rnd.randrange(0, 4)):   # change a few points
            if B and rnd.random() < 0.5: B.discard(rnd.choice(sorted(B)))
            else: B.add(rnd.randrange(n))
        return sorted(B)
    stats = {"sets": 0, "all+ good": 0, "one turn": 0, "more turns needed": 0, "no good signing": 0, "not decided (too big)": 0}
    hist = {}; biggest = None
    for _ in range(trials):
        B = gen()
        if not B or len(B) > 70: continue
        stats["sets"] += 1
        r = resid(B)
        if all(np.any(r[d] != 0) for d in ds): stats["all+ good"] += 1; continue
        ok = False
        for x in B:
            if all(np.any(r[d] - 2 * Rs[d][:, x % d] != 0) for d in ds): ok = True; break
        if ok: stats["one turn"] += 1; continue
        if len(B) > 18:
            stats["not decided (too big)"] += 1; print("ONE TURN FAILS, too big to enumerate:", n, B); continue
        # enumerate all signings
        best = None
        cols = {d: np.stack([Rs[d][:, x % d] for x in B], axis=1) for d in ds}
        for t in range(2, len(B) // 2 + 1):
            for T in itertools.combinations(range(len(B)), t):
                if all(np.any(r[d] - 2 * cols[d][:, list(T)].sum(axis=1) != 0) for d in ds): best = t; break
            if best: break
        if best is None: stats["no good signing"] += 1; print("NO GOOD SIGNING:", n, B)
        else:
            stats["more turns needed"] += 1; hist[best] = hist.get(best, 0) + 1
            print("needs %d turns: n = %d, B = %s" % (best, n, B))
        sys.stdout.flush()
    print("n = %d, seed %d:" % (n, seed), stats, "turns needed beyond one:", hist)
if __name__ == "__main__":
    main()
