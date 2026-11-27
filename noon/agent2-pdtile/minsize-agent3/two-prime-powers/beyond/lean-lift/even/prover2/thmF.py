# Theorem F: n = 2^k * 3^a.  Construction of a 3-good signing of the residues modulo 2^k (proof of Lemma F),
# and exact check that it is (1) 3-good on Z_{2^k}, (2) good on Z_n.
import sys, itertools, random
sys.path.insert(0, '/home/agent3/lean/lift-check/even/prover2')
from lib2 import *

def v2(x, cap):
    if x == 0: return cap
    v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v

def sum0mod3(idx):
    # signs for the elements idx (len >= 2, or 0) with sum of signs = 0 mod 3
    r = len(idx); assert r != 1
    t = (-r) % 3            # number of minus signs: r - 2t = r + t = 0 mod 3
    return {i: (-1 if j < t else 1) for j, i in enumerate(idx)}

def sumnot0mod3(idx):
    r = len(idx); assert r >= 1
    t = 0 if r % 3 else 1
    return {i: (-1 if j < t else 1) for j, i in enumerate(idx)}

def exceptional(el, K):
    # el: list of (index, residue mod 2^K)
    return len(el) == 2 and el[0][1] != el[1][1]

def sign3(el, K):
    # el: list of (index, u), u in Z_{2^K}; returns dict index -> sign, 3-good on Z_{2^K}; None for an exceptional pair
    if exceptional(el, K): return None
    if K == 0:
        return sumnot0mod3([i for i, _ in el])
    E = [(i, u // 2) for i, u in el if u % 2 == 0]
    D = [(i, (u - 1) // 2) for i, u in el if u % 2 == 1]
    if not D: return sign3(E, K - 1)
    if not E: return sign3(D, K - 1)
    if len(E) == 1 or len(D) == 1:
        A, C = (E, D) if len(D) == 1 else (D, E)
        assert len(A) >= 2
        out = sum0mod3([i for i, _ in A]); out[C[0][0]] = 1
        return out
    exE, exD = exceptional(E, K - 1), exceptional(D, K - 1)
    if exE and exD:
        vE = v2(E[0][1] - E[1][1], K - 1); vD = v2(D[0][1] - D[1][1], K - 1)
        if vD >= vE:
            return {E[0][0]: 1, E[1][0]: -1, D[0][0]: 1, D[1][0]: 1}
        return {E[0][0]: 1, E[1][0]: 1, D[0][0]: 1, D[1][0]: -1}
    A, C = (E, D) if not exE else (D, E)
    out = sign3(A, K - 1)
    out.update(sum0mod3([i for i, _ in C]))
    return out

def check(B, n, stats):
    K, odd = two_part(n)
    q = 1 << K
    el = [(i, x % q) for i, x in enumerate(B)]
    sg = sign3(el, K)
    exc = (len(B) == 2 and (B[0] - B[1]) % q != 0)
    if sg is None:
        assert exc; stats['exc'] += 1
        # confirm: no good signing
        assert not good(B, [1, 1], n) and not good(B, [1, -1], n)
        return
    assert not exc
    signs = [sg[i] for i in range(len(B))]
    Bq = [x % q for x in B]
    for d in divisors(q):
        assert not is_bad3(Bq, signs, q, d), ('not 3-good', B, n, signs, d)
    assert good(B, signs, n), ('not good', B, n, signs)
    stats['ok'] += 1

if __name__ == '__main__':
    mode = sys.argv[1]
    stats = {'ok': 0, 'exc': 0}
    if mode == 'exhaust':
        for n, mmax in [(2, 9), (4, 8), (8, 6), (16, 5), (6, 8), (12, 6), (18, 6), (24, 5), (36, 5), (48, 4), (54, 5), (72, 4), (108, 4), (162, 4), (144, 3), (96, 4)]:
            st = {'ok': 0, 'exc': 0}
            for m in range(1, mmax + 1):
                for B in multisets_with_zero(n, m):
                    check(B, n, st)
            print('n', n, 'all multisets with 0 up to', mmax, 'elements:', st, flush=True)
    if mode == 'subsets':
        for n in [8, 12, 16]:
            st = {'ok': 0, 'exc': 0}
            for mask in range(1, 1 << n):
                B = [x for x in range(n) if mask >> x & 1]
                if n > 16 and len(B) > 12: continue
                check(B, n, st)
            print('n', n, 'nonempty subsets:', st, flush=True)
    if mode == 'random':
        random.seed(5)
        for n in [32, 64, 96, 192, 288, 432, 486, 648, 864, 1296, 1458, 2592]:
            st = {'ok': 0, 'exc': 0}
            K, odd = two_part(n)
            for t in range(400):
                kind = t % 5
                m = random.randint(2, 40)
                if kind == 0: B = [random.randrange(n) for _ in range(m)]
                elif kind == 1:   # closed under x -> x + n/2
                    h = [random.randrange(n // 2) for _ in range(max(1, m // 2))]; B = h + [x + n // 2 for x in h]
                elif kind == 2:   # union of cosets of a subgroup
                    g = random.choice([d for d in divisors(n) if 1 < d <= 12]); st_ = n // g
                    B = []
                    for _ in range(random.randint(1, 4)):
                        o = random.randrange(st_); B += [o + i * st_ for i in range(g)]
                elif kind == 3:   # all three classes modulo 3 of even size, m even
                    B = []
                    for c in range(3):
                        B += [3 * random.randrange(n // 3) + c for _ in range(2 * random.randint(1, 4))]
                else:             # few residues modulo 2^K, many modulo the odd part
                    us = [random.randrange(1 << K) for _ in range(2)]
                    B = []
                    for _ in range(m):
                        u = random.choice(us); w = random.randrange(odd)
                        x = next(x for x in range(u, n, 1 << K) if x % odd == w) if odd > 1 else u
                        B.append(x)
                check(B, n, st)
            print('n', n, 'random and structured:', st, flush=True)
