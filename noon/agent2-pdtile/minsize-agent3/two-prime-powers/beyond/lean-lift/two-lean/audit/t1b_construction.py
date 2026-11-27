# The signing in the paper's proof of Lemma "signs", carried out and checked, on multisets far larger than brute force reaches.
# (This tests the paper's proof, hence the truth of `exists_signs` for these n; it is not a reading of the Lean statement.)
# n = p^a q^b, p != q odd primes.  Fix an element x* of B; C_i = its class modulo p^i.  s(C_a) = 1 if C_a holds an odd number
# of elements, 2 if even.  For i = a, ..., 1: each of the other p - 1 classes modulo p^i inside C_{i-1} gets s = 0 if it holds
# an even number; those with an odd number get +1 and -1 in pairs, and a left-over one gets the one of +1, -1 that keeps
# s(C_{i-1}) away from 0 modulo q.  Within a class the signs are dealt in any way that gives the class its value s.
# Then no Phi_d, d | n (d = 1 included), may divide the signed mask: checked with exact integer arithmetic (core.Grp).
import sys, random, time
from core import Grp, pattern_slow


def sign_class(elems_idx, target):
    """signs for the elements (indices) of one class with sum `target` (|target| <= count, same parity)"""
    nu = len(elems_idx)
    assert abs(target) <= nu and (nu - target) % 2 == 0
    plus = (nu + target) // 2
    return {i: (1 if k < plus else -1) for k, i in enumerate(elems_idx)}


def paper_signs(B, p, a, q, b, rng):
    n = p ** a * q ** b
    idx = list(range(len(B)))
    rng.shuffle(idx)                       # "in any way": the order inside a class is random
    star = B[idx[0]]
    signs = {}
    # C_a
    Ca = [i for i in idx if (B[i] - star) % p ** a == 0]
    sC = 1 if len(Ca) % 2 == 1 else 2
    signs.update(sign_class(Ca, sC))
    for i in range(a, 0, -1):
        # the other p - 1 classes modulo p^i inside C_{i-1}
        others = {}
        for j in idx:
            if (B[j] - star) % p ** (i - 1) == 0 and (B[j] - star) % p ** i != 0:
                others.setdefault((B[j] - star) % p ** i, []).append(j)
        odd = [c for c in sorted(others) if len(others[c]) % 2 == 1]
        even = [c for c in sorted(others) if len(others[c]) % 2 == 0]
        for c in even:
            signs.update(sign_class(others[c], 0))
        rng.shuffle(odd)
        while len(odd) >= 2:
            c1, c2 = odd.pop(), odd.pop()
            signs.update(sign_class(others[c1], 1))
            signs.update(sign_class(others[c2], -1))
        if odd:
            c = odd.pop()
            t = 1 if (sC + 1) % q != 0 else -1
            assert (sC + t) % q != 0
            signs.update(sign_class(others[c], t))
            sC += t
        assert sC % q != 0
    assert len(signs) == len(B)
    return [signs[i] for i in range(len(B))]


def random_multiset(n, rng, G):
    kind = rng.randrange(4)
    if kind == 0:
        return [rng.randrange(n) for _ in range(rng.randint(1, 60))]
    if kind == 1:   # unions of cosets of subgroups: many Phi_d divide the unsigned mask
        B = []
        for _ in range(rng.randint(1, 4)):
            d = rng.choice(G.divs)
            t = rng.randrange(n)
            B += [(t + j * (n // d)) % n for j in range(d)]
        return B
    if kind == 2:   # the whole group, several times, plus a few
        return list(range(n)) * rng.randint(1, 2) + [rng.randrange(n) for _ in range(rng.randint(0, 3))]
    # few distinct elements with high multiplicity
    pts = [rng.randrange(n) for _ in range(rng.randint(1, 4))]
    return [rng.choice(pts) for _ in range(rng.randint(1, 40))]


if __name__ == '__main__':
    rng = random.Random(2026112601)
    cases = [(3, 0, 5, 0), (3, 1, 5, 0), (3, 0, 5, 1), (3, 1, 5, 1), (5, 1, 3, 1), (3, 2, 5, 1), (5, 1, 3, 2), (3, 1, 5, 2),
             (5, 2, 3, 1), (3, 3, 5, 1), (5, 1, 3, 3), (3, 2, 5, 2), (5, 2, 3, 2), (3, 4, 5, 0), (3, 0, 5, 3), (3, 5, 7, 0),
             (3, 1, 7, 1), (7, 1, 3, 1), (3, 2, 7, 1), (7, 2, 3, 1), (3, 1, 7, 2), (5, 1, 7, 1), (7, 1, 5, 1), (5, 2, 7, 1),
             (7, 1, 5, 2), (3, 3, 7, 1), (7, 1, 3, 3), (3, 1, 11, 1), (11, 1, 3, 2), (3, 2, 11, 1), (5, 1, 11, 1), (11, 1, 13, 1),
             (13, 1, 3, 1), (3, 3, 5, 2), (5, 2, 3, 3), (3, 4, 5, 1), (5, 1, 3, 4), (3, 6, 5, 0), (5, 3, 3, 1), (7, 2, 5, 1)]
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    total = bad = nontrivial = 0
    t0 = time.time()
    for (p, a, q, b) in cases:
        n = p ** a * q ** b
        G = Grp(n)
        cb = cn = 0
        for r in range(reps):
            B = random_multiset(n, rng, G)
            sg = paper_signs(B, p, a, q, b, rng)
            pat = G.pattern(B, sg)
            if r < 3:
                assert pat == pattern_slow(B, n, sg)      # the table method against long division, on the signed mask
            if pat:
                cb += 1
                print(f"   FAILURE n={n} B={B} signs={sg} divisors={sorted(pat)}")
            if G.pattern(B):
                cn += 1
        total += reps; bad += cb; nontrivial += cn
        print(f"n = {p}^{a} * {q}^{b} = {n:5d}: {reps} multisets, all-plus mask had a divisor in {cn}, the paper's signing failed in {cb}",
              flush=True)
    print(f"TOTAL: {len(cases)} moduli, {total} multisets (sizes up to 2n + 3), all-plus fails in {nontrivial}, "
          f"the paper's signing fails in {bad}  [{time.time() - t0:.0f}s]")
