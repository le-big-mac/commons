"""Referee, third pass: the recursion Gamma of sign-all-result.md (section 5), Corollary 8, and the bound N*.
Written from the text; exact fractions throughout (no floating point anywhere in a decision).

  omega = 2^(1-p);  lam(p, a) = omega + ... + omega^a;
  single(p, a) = 1/2 if a = 1 or p >= 5;  5/8 - lam(3, a) if p = 3, a >= 2;
  Gamma({(p, a)}) = single(p, a);  for more trees
  Gamma(S) = max over (p, a) in S with G' = Gamma(S - (p, a)) > 0 of
               min( single(p, a) G' , (3/4) G' - L' lam(p, a) ),  and if a = 1 also  min( G'/2 , G' - L' 2^(1-p) ),
             L' = product of (c + 1) over the other trees (r, c).
  Theorem 7: n = m q^b (q an odd prime not dividing m) or n = m, Gamma(m) > 0.
  Theorem 2: at most two primes.  Theorem 3: three primes, two of them to the first power.
  Theorem 6: n = m q^b or n = m with c(m) > 0 (the digit recursion; taken from ../coverage_own.py, my program of the first pass).

parts:  small   every odd n < LIMIT by Theorems 2, 3, 6, 7 (full Gamma, all orders)
        cor8    Corollary 8 against Gamma, and the claims for 3^a 5^b 7^c
        mono    the monotonicity used for the bound, on random cases
        nstar   N* itself: is it covered by anything?  (full Gamma for every choice of q; the digit recursion for every q)
        below   every exponent vector on an initial segment of the odd primes with product < N*
usage: coverage3_own.py PART [args]
"""
import sys, time, random
from fractions import Fraction as Fr
from functools import lru_cache
sys.path.insert(0, '/home/agent3/paper/referee-signs')
_argv = sys.argv; sys.argv = [_argv[0]]          # coverage_own.py reads its own command line when imported
from coverage_own import c_rec, factor, thm2, thm3
sys.argv = _argv

NSTAR = 6587407633447265625

@lru_cache(maxsize=None)
def lam(p, a):
    return sum(Fr(1, 2 ** ((p - 1) * l)) for l in range(1, a + 1))

@lru_cache(maxsize=None)
def single(p, a):
    return Fr(1, 2) if (a == 1 or p >= 5) else Fr(5, 8) - lam(3, a)

def step(G, L, p, a):
    """value after adding the tree (p, a) to a box with value G > 0 and L levels."""
    best = min(single(p, a) * G, Fr(3, 4) * G - L * lam(p, a))
    if a == 1:
        best = max(best, min(G / 2, G - L * Fr(2, 2 ** p)))
    return best

@lru_cache(maxsize=None)
def gamma(S):
    """S: sorted tuple of (p, a), distinct primes.  The full recursion (maximum over which tree comes last)."""
    if len(S) == 1:
        return single(*S[0])
    best = None
    for idx, (p, a) in enumerate(S):
        rest = S[:idx] + S[idx + 1:]
        G = gamma(rest)
        if G <= 0: continue
        L = 1
        for (_, c) in rest: L *= c + 1
        v = step(G, L, p, a)
        if best is None or v > best: best = v
    return Fr(-1) if best is None else best

def gamma_ordered(seq):
    """the trees in the given order; None as soon as a value is not positive."""
    G = single(*seq[0]); L = seq[0][1] + 1
    for (p, a) in seq[1:]:
        G = step(G, L, p, a)
        if G <= 0: return None
        L *= a + 1
    return G

def thm7_ways(f):
    """f: dict prime -> exponent.  The choices of q (None for n = m) with Gamma(m) > 0, with the value."""
    ways = []
    items = tuple(sorted(f.items()))
    if items:
        G = gamma(items)
        if G > 0: ways.append((None, G))
    for q in f:
        rest = tuple(sorted((p, a) for p, a in f.items() if p != q))
        if rest:
            G = gamma(rest)
            if G > 0: ways.append((q, G))
    return ways

def thm6_any(f):
    if c_rec(tuple(sorted(f.items()))) > 0: return True
    return any(c_rec(tuple(sorted((p, a) for p, a in f.items() if p != q))) > 0 for q in f)

def odd_primes(k):
    res = []; n = 3
    while len(res) < k:
        if all(n % d for d in range(3, int(n ** 0.5) + 1, 2)): res.append(n)
        n += 2
    return res

def part_small(limit):
    unc = []; only7 = []; n7 = 0
    for n in range(1, limit, 2):
        f = factor(n)
        t2, t3 = thm2(f), thm3(f); t6 = thm6_any(f); t7 = bool(thm7_ways(f)) if len(f) >= 1 else False
        if t7: n7 += 1
        if not (t2 or t3 or t6 or t7): unc.append(n)
        if t7 and not (t2 or t3 or t6): only7.append(n)
    print(f'odd n < {limit}: covered by none of Theorems 2, 3, 6, 7: {unc}; covered by Theorem 7 and by none of 2, 3, 6: {only7}; '
          f'covered by Theorem 7 at all: {n7}')
    for n in (118125, 165375, 675, 1575, 4725, 11025):
        f = factor(n)
        print(f'   {n} = {f}: Theorem 7 with (q, Gamma(m)): {[(q, str(G)) for q, G in thm7_ways(f)]}; Theorem 6: {thm6_any(f)}; Theorems 2, 3: {thm2(f)}, {thm3(f)}')
    for m in (4375, 6125, 225, 189, 441, 1225, 675, 175):
        print(f'   Gamma({m} = {factor(m)}) = {gamma(tuple(sorted(factor(m).items())))}')
    print('   single(3, a), a = 1..6:', [str(single(3, a)) for a in range(1, 7)], '; all > 7/24:', all(single(3, a) > Fr(7, 24) for a in range(1, 60)))
    print('   lam(p, a) < 1/(2^(p-1) - 1) for p in 3..47, a <= 60:',
          all(lam(p, a) < Fr(1, 2 ** (p - 1) - 1) for p in odd_primes(14) for a in range(1, 61)))

def part_cor8():
    ps = odd_primes(8)
    bad = 0; tested = 0; sharp = {}
    for i1 in range(len(ps)):
        for i2 in range(i1 + 1, len(ps)):
            for i3 in range(i2 + 1, len(ps)):
                p1, p2, p3 = ps[i1], ps[i2], ps[i3]
                if p3 > 13: continue
                for e1 in range(1, 16):
                    for e2 in range(1, 26):
                        for e3 in range(1, 8):
                            c1 = (e2 + 1) <= Fr(3, 8) * (2 ** (p3 - 1) - 1)
                            c2 = (e3 + 1) <= Fr(3, 8) * (2 ** (p2 - 1) - 1)
                            c3 = (e1 + 1) <= Fr(7, 32) * (2 ** (p3 - 1) - 1)
                            if not (c1 or c2 or c3): continue
                            tested += 1
                            f = {p1: e1, p2: e2, p3: e3}
                            ok = True
                            if c1 and not gamma(((p2, e2), (p3, e3))) > 0: ok = False       # q = p1
                            if c2 and not gamma(((p2, e2), (p3, e3))) > 0: ok = False       # q = p1
                            if c3 and not gamma(((p1, e1), (p3, e3))) > 0: ok = False       # q = p2
                            if not ok: bad += 1; print('Corollary 8 fails at', f)
    print(f'Corollary 8: {tested} triples (p1 < p2 < p3 <= 13, e1 <= 15, e2 <= 25, e3 <= 7) satisfying (i), (ii) or (iii): '
          f'Gamma > 0 for the m named in its proof in every case; exceptions: {bad}')
    # 3^a 5^b 7^c
    A = max(a for a in range(1, 100) if (a + 1) <= Fr(7, 32) * 63)
    B = max(b for b in range(1, 100) if (b + 1) <= Fr(3, 8) * 63)
    C = max(c for c in range(1, 100) if (c + 1) <= Fr(3, 8) * 15)
    print(f'for 3^a 5^b 7^c the three conditions read a <= {A}, b <= {B}, c <= {C}')
    unc = []
    for a in range(1, 20):
        for b in range(1, 30):
            for c in range(1, 9):
                f = {3: a, 5: b, 7: c}
                cov = thm2(f) or thm3(f) or bool(thm7_ways(f)) or thm6_any(f)
                if (a <= A or b <= B or c <= C) and not cov: print('NOT covered though the condition holds:', f)
                if not cov: unc.append((3 ** a * 5 ** b * 7 ** c, a, b, c))
    unc.sort()
    print(f'   3^a 5^b 7^c, a < 20, b < 30, c < 9, covered by none of Theorems 2, 3, 6, 7 (full Gamma): {len(unc)}; the least: {unc[:3]}')
    inside = [(n, a, b, c) for (n, a, b, c) in unc if not (a >= A + 1 and b >= B + 1 and c >= C + 1)]
    print(f'   of them outside the region a >= {A + 1}, b >= {B + 1}, c >= {C + 1}: {len(inside)}')
    cov_in_region = [(a, b, c) for a in range(A + 1, 20) for b in range(B + 1, 30) for c in range(C + 1, 9)
                     if (3 ** a * 5 ** b * 7 ** c, a, b, c) not in set(unc)]
    print(f'   in that region, covered all the same (the corollary is sufficient, not necessary): {len(cov_in_region)} {cov_in_region[:6]}')

def part_mono(seed):
    rng = random.Random(seed); ps = odd_primes(16); viol = 0; tested = 0; pos = 0
    for _ in range(40000):
        k = rng.randint(1, 5)
        idx = sorted(rng.sample(range(10), k))
        idx2 = sorted(min(15, i + rng.randint(0, 5)) for i in idx)
        if len(set(idx2)) < k: continue
        # idx2[j] >= idx[j] holds for the sorted lists
        if any(b < a for a, b in zip(idx, idx2)): continue
        e = [rng.choice([1, 1, 2, 2, 3, 4, 6, 9, 14]) for _ in range(k)]
        S = tuple((ps[i], x) for i, x in zip(idx, e)); S2 = tuple((ps[i], x) for i, x in zip(idx2, e))
        G, G2 = gamma(S), gamma(S2)
        tested += 1
        if G > 0:
            pos += 1
            if G2 < G: viol += 1; print('monotonicity fails', S, G, S2, G2)
        # the digit recursion as well (not needed for the bound), where its state space is small
        states = 1
        for x in e: states *= x + 1
        if states <= 2000:
            c1, c2 = c_rec(S), c_rec(S2)
            if c1 > 0 and c2 < c1: viol += 1; print('monotonicity of the digit recursion fails', S, c1, S2, c2)
    print(f'monotonicity: {tested} random pairs (same exponents in the same order, primes replaced by larger ones), Gamma > 0 for the smaller primes in {pos}: '
          f'Gamma (and c) with the larger primes never smaller; exceptions: {viol}')

def part_nstar():
    f = factor_big(NSTAR)
    print(f'N* = {NSTAR} = {f}; 3^6 5^11 7^6 11^2 13 = {3**6 * 5**11 * 7**6 * 11**2 * 13}')
    print(f'   Theorem 2: {thm2(f)}; Theorem 3: {thm3(f)}')
    items = tuple(sorted(f.items()))
    print(f'   Theorem 7, n = m: Gamma(N*) = {gamma(items)}')
    for q in f:
        rest = tuple(sorted((p, a) for p, a in f.items() if p != q))
        print(f'   Theorem 7, q = {q}: Gamma(N*/{q}^{f[q]}) = {gamma(rest)}  (best value over all orders; -1: no order reaches a positive value)')
    print(f'   Theorem 6, n = m: c(N*) = {c_rec(items)}')
    for q in f:
        rest = tuple(sorted((p, a) for p, a in f.items() if p != q))
        print(f'   Theorem 6, q = {q}: c = {c_rec(rest)}')
    cov = thm2(f) or thm3(f) or bool(thm7_ways(f)) or thm6_any(f)
    print(f'   N* covered by Theorem 2, 3, 6 or 7: {cov}')

def factor_big(n):
    f = {}
    for p in odd_primes(40):
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
    assert n == 1
    return f

def part_below(bound):
    """all (e_1, ..., e_k), e_j >= 1, on the first k odd primes, with product < bound.  For each: Theorem 2, Theorem 3, or the
    recursion along increasing primes for some q (None or one of the primes).  Where that fails: the full Gamma and Theorem 6."""
    ps = odd_primes(20)
    stats = {'vectors': 0, 'thm2': 0, 'thm3': 0, 'inc_order': 0, 'full_gamma_needed': 0, 'thm6_needed': 0, 'uncovered': []}
    t0 = time.time()
    # iterative depth-first search; a state: (k, prod, exps, vals) with vals[0] = running value for q = None (all trees so far),
    # vals[i] = running value with the i-th prime left out (i = 1..k); each value is (G, L) or None when not positive; G None, L 1 = empty box
    stack = [(0, 1, (), [('empty', 1)])]
    while stack:
        k, prod, exps, vals = stack.pop()
        p = ps[k]
        pe = p; e = 1
        while prod * pe < bound:
            # extend every running value by the tree (p, e); the new value "p left out" is the old q = None value
            new = []
            for v in vals:
                if v is None: new.append(None); continue
                G, L = v
                if G == 'empty': G2 = single(p, e)
                else: G2 = step(G, L, p, e)
                new.append((G2, L * (e + 1)) if G2 > 0 else None)
            new.append(vals[0])                       # q = p: the box of the earlier primes, unchanged
            exps2 = exps + (e,)
            stats['vectors'] += 1
            kk = k + 1
            if kk <= 2: stats['thm2'] += 1
            elif kk == 3 and sum(1 for x in exps2 if x == 1) >= 2: stats['thm3'] += 1
            elif any(v is not None and v[0] != 'empty' for v in new): stats['inc_order'] += 1
            else:
                f = {ps[j]: exps2[j] for j in range(kk)}
                if thm7_ways(f): stats['full_gamma_needed'] += 1
                elif thm6_any(f): stats['thm6_needed'] += 1
                else: stats['uncovered'].append((prod * pe, exps2))
            stack.append((kk, prod * pe, exps2, new))
            pe *= p; e += 1
    print(f'exponent vectors on initial segments of the odd primes with product < {bound}: {stats["vectors"]}')
    print(f'   covered by Theorem 2: {stats["thm2"]}; by Theorem 3: {stats["thm3"]}; by Theorem 7 with the trees in the order of increasing primes, '
          f'for some q: {stats["inc_order"]}; only by the full recursion (another order): {stats["full_gamma_needed"]}; only by Theorem 6: {stats["thm6_needed"]}')
    print(f'   covered by nothing: {len(stats["uncovered"])} {sorted(stats["uncovered"])[:5]}')
    print(f'   [{time.time() - t0:.0f} s]')

if __name__ == '__main__':
    part = sys.argv[1]
    if part == 'small': part_small(int(sys.argv[2]))
    elif part == 'cor8': part_cor8()
    elif part == 'mono': part_mono(int(sys.argv[2]))
    elif part == 'nstar': part_nstar()
    elif part == 'below': part_below(int(sys.argv[2]) if len(sys.argv) > 2 else NSTAR)
