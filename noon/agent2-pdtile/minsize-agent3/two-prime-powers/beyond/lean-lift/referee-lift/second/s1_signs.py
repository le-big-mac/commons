"""Lemma 17 of the paper (signs), implemented from the paper's text (subsection "The prime 2"), and tested with exact arithmetic.
n = p^a q^b, p != q odd primes, a, b >= 0 (for b = 0 the prime q is an auxiliary odd prime other than p).  B a nonempty multiset on Z_n.
The signs, as the paper's proof gives them:  fix an element x* of B, C_i = its class modulo p^i.  s(C_a) = 1 if C_a holds an odd number of
elements, 2 if even.  For i = a, ..., 1: of the p - 1 other classes modulo p^i inside C_{i-1}, those with an even number get s = 0, those
with an odd number get +1 and -1 in pairs, and one left over gets that one of +1, -1 which keeps s(C_{i-1}) away from 0 modulo q.
Checked for each signing: (i) s(Z_n) not 0 mod q; (ii) at each level i two classes mod p^i inside one class mod p^{i-1} with different s mod q;
and the conclusion: the signed mask is divisible by NO Phi_d, d | n, d = 1 included (integer remainders modulo Phi_d).
Every choice of x*, both preferences for the left-over class where both are allowed, random pairing.   usage: python -I -B s1_signs.py [small]"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift/second')
import itertools, random
import numpy as np
from cyc import divisors, tables
rnd = random.Random(1126)
def give(idxs, total, sg):
    """signs for the elements idxs with sum = total"""
    k = len(idxs); assert abs(total) <= k and (k - total) % 2 == 0
    order = idxs[:]; rnd.shuffle(order)
    e = 1 if total >= 0 else -1
    for j, ix in enumerate(order):
        sg[ix] = e if j < abs(total) else (1 if (j - abs(total)) % 2 == 0 else -1)
def paper_signs(B, p, a, q, istar, prefer):
    """B: list of integers in range(n); returns the list of signs and the dictionary {i: s(C_i)}"""
    sg = [0] * len(B); xs = B[istar]
    Ca = [j for j, x in enumerate(B) if (x - xs) % p ** a == 0]
    cur = 1 if len(Ca) % 2 else 2
    give(Ca, cur, sg); sC = {a: cur}
    for i in range(a, 0, -1):
        rest = {}
        for j, x in enumerate(B):
            if (x - xs) % p ** (i - 1) == 0 and (x - xs) % p ** i != 0: rest.setdefault(x % p ** i, []).append(j)
        assert len(rest) <= p - 1
        odd = [c for c in rest if len(rest[c]) % 2]; rnd.shuffle(odd)
        for c in rest:
            if len(rest[c]) % 2 == 0: give(rest[c], 0, sg)
        pairs = len(odd) // 2
        for h in range(pairs): give(rest[odd[2 * h]], 1, sg); give(rest[odd[2 * h + 1]], -1, sg)
        if len(odd) % 2:
            opts = [e for e in ((1, -1) if prefer > 0 else (-1, 1)) if (cur + e) % q]
            assert opts, 'both cur + 1 and cur - 1 divisible by q'
            give(rest[odd[-1]], opts[0], sg); cur += opts[0]
        assert cur % q
        sC[i - 1] = cur
    assert all(s in (1, -1) for s in sg)
    return sg, sC
def check(B, sg, n, p, a, q, istar, sC):
    xs = B[istar]
    tot = sum(sg); assert tot == sC[0] and tot % q != 0                                   # (i)
    for i in range(1, a + 1):                                                            # (ii): C_i against one of its siblings
        s = {}
        for x, e in zip(B, sg):
            if (x - xs) % p ** (i - 1) == 0: s[x % p ** i] = s.get(x % p ** i, 0) + e
        vals = [s.get((xs + t * p ** (i - 1)) % p ** i, 0) for t in range(p)]
        assert vals[0] == sC[i]
        assert any((v - vals[0]) % q for v in vals[1:]), ('(ii) fails', B, i)
    T = tables(n); idx = np.array(B); w = np.array(sg)
    for d, t in T.items():
        if not (t[idx] * w[:, None]).sum(axis=0).any(): return d
    return None
def run_all(B, n, p, a, q, stats, fails, all_stars=True):
    stars = range(len(B)) if all_stars else [rnd.randrange(len(B))]
    for istar in stars:
        for prefer in (1, -1):
            sg, sC = paper_signs(B, p, a, q, istar, prefer)
            bad = check(B, sg, n, p, a, q, istar, sC)
            stats['signings'] += 1
            if bad is not None: fails.append((n, p, a, q, B, istar, prefer, bad))
    T = tables(n); idx = np.array(B)
    stats['multisets'] += 1
    stats['all + is good'] += all(t[idx].sum(axis=0).any() for t in T.values())
def rand_multiset(n):
    r = rnd.random()
    if r < 0.35: return sorted(rnd.randrange(n) for _ in range(rnd.randint(1, 12)))
    if r < 0.5: return sorted(rnd.sample(range(n), rnd.randint(1, min(n, 40))))
    el = []
    for _ in range(rnd.randint(1, 4)):
        c = rnd.choice(divisors(n)); x0 = rnd.randrange(n); el += [(x0 + c * j) % n for j in range(n // c)]
    for _ in range(rnd.randint(0, 3)): el.append(rnd.randrange(n))
    return sorted(el)
def main():
    small = len(sys.argv) > 1
    tot = {'multisets': 0, 'signings': 0, 'all + is good': 0}; fails = []
    print('--- exhaustive: every nonempty multiset with at most S elements (and, where said, every nonempty subset); every x*; both preferences')
    EXH = [  # (p, a, q, b, S, all subsets?)
        (3, 0, 5, 0, 6, False), (5, 0, 3, 0, 6, False), (3, 1, 5, 0, 7, True), (3, 1, 7, 0, 5, True), (5, 1, 3, 0, 6, True), (7, 1, 3, 0, 5, True), (7, 1, 5, 0, 4, True),
        (3, 2, 5, 0, 5, True), (3, 2, 7, 0, 4, True), (3, 0, 5, 1, 6, True), (5, 0, 3, 1, 7, True), (3, 0, 5, 2, 3, False), (5, 0, 3, 2, 5, True),
        (3, 1, 5, 1, 5, True), (5, 1, 3, 1, 5, True), (3, 1, 7, 1, 4, False), (7, 1, 3, 1, 4, False), (3, 3, 5, 0, 3, False), (5, 2, 3, 0, 3, False),
        (3, 2, 5, 1, 3, False), (5, 1, 3, 2, 3, False), (3, 1, 5, 2, 3, False), (5, 2, 3, 1, 3, False), (5, 1, 7, 1, 3, False), (7, 1, 5, 1, 3, False), (3, 1, 11, 1, 3, False), (11, 1, 3, 1, 3, False),
    ]
    if small: EXH = EXH[:6]
    for p, a, q, b, S, subsets in EXH:
        n = p ** a * q ** b; st = dict.fromkeys(tot, 0)
        for s in range(1, S + 1):
            for B in itertools.combinations_with_replacement(range(n), s): run_all(list(B), n, p, a, q, st, fails)
        if subsets and n <= 15:
            for mask in range(1, 1 << n):
                B = [x for x in range(n) if mask >> x & 1]
                if len(B) > S: run_all(B, n, p, a, q, st, fails, all_stars=(n <= 9))
        for k in tot: tot[k] += st[k]
        print(f'n = {n} = {p}^{a}*{q}^{b} (tree prime {p}, modulus {q}), S = {S}{", and every larger subset" if subsets and n <= 15 else ""}: {st}', flush=True)
    print('--- random multisets (uniform, sets, sums of cosets with points added); a random x*; both preferences')
    RND = [(3, 2, 5, 1, 1500), (5, 1, 3, 2, 1500), (3, 2, 7, 1, 1200), (7, 1, 3, 2, 1200), (3, 1, 5, 2, 1200), (5, 2, 3, 1, 1200), (3, 3, 5, 1, 800), (5, 1, 3, 3, 800),
           (3, 2, 5, 2, 800), (5, 2, 3, 2, 800), (3, 4, 5, 0, 800), (3, 4, 7, 0, 600), (5, 3, 3, 0, 800), (7, 2, 3, 0, 800), (7, 2, 5, 0, 600), (3, 1, 7, 2, 800), (7, 2, 3, 1, 800),
           (5, 1, 7, 1, 1000), (7, 1, 5, 1, 1000), (11, 1, 13, 1, 600), (13, 1, 11, 1, 600), (3, 5, 5, 0, 500), (3, 0, 5, 3, 600), (5, 2, 7, 1, 500), (7, 1, 5, 2, 500),
           (3, 2, 5, 3, 300), (5, 3, 3, 2, 300), (3, 3, 7, 1, 400), (3, 0, 5, 0, 300), (5, 0, 7, 0, 300), (3, 2, 11, 1, 500), (11, 1, 3, 2, 500)]
    if small: RND = [(3, 2, 5, 1, 200), (5, 1, 3, 2, 200)]
    for p, a, q, b, Tn in RND:
        n = p ** a * q ** b; st = dict.fromkeys(tot, 0)
        for _ in range(Tn): run_all(rand_multiset(n), n, p, a, q, st, fails, all_stars=False)
        for k in tot: tot[k] += st[k]
        print(f'n = {n} = {p}^{a}*{q}^{b} (tree prime {p}, modulus {q}), {Tn} random: {st}', flush=True)
    print('TOTAL:', tot); print('FAILURES (a Phi_d dividing the signed mask):', len(fails), fails[:3])

if __name__ == '__main__': main()
