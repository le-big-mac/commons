"""Second pass: the paragraph 'The prime 2' of the paper's subsection, tested from the paper's text.

Lemma 17 (signs), as its proof words the choice: n = P^a Q^b, B a nonempty multiset on Z_n.  Fix an element x* of B and let
C_i be its class modulo P^i.  C_a gets the value s = 1 if it holds an odd number of elements and 2 if an even number.
For i = a, a-1, .., 1: the rest of C_(i-1) is P - 1 classes modulo P^i; those holding an even number get s = 0; those
holding an odd number get +1 and -1 in pairs; one left over gets that one of +1, -1 which keeps s(C_(i-1)) away from 0
modulo Q.  (A class holding v elements is given the value s by (v + s)/2 signs + and the rest -; which elements get
which is left open by the text and is chosen at random here.)

The step along 2 of the paragraph: N = 2^k N', N' = P^a Q^b; every element of A has multiplicity 1 or 2, not every
element 2.  The two copies of a doubled element go to its two lifts.  Choose a class modulo 2^k that holds an element of
multiplicity 1; sign the elements of multiplicity 1 in it by Lemma 17 (their residues modulo N'); sign + goes low
(residue modulo 2^(k+1) below 2^k), sign - high.  Elements of multiplicity 1 in other classes: the paragraph does not
say; here they go low or high AT RANDOM (the claim to test is that anything will do).
Checked: the lift is a set with as many elements, it reduces to A, and its pattern among the divisors of 2N is
exactly that of A.  Exact integer arithmetic (../cyc.py).

usage: two.py signs | exhaustive | random SEED | claim1 | needs"""
import sys, os, itertools, random, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from cyc import divisors, pattern, remainder


def factor(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def give(idx, s, sign, rnd):
    """the class idx (a list of positions) gets the value s: (v + s)/2 signs +, the rest -"""
    v = len(idx)
    assert abs(s) <= v and (v - s) % 2 == 0
    idx = list(idx)
    rnd.shuffle(idx)
    plus = (v + s) // 2
    for t, i in enumerate(idx):
        sign[i] = 1 if t < plus else -1


def signs17(B, P, a, Q, rnd, star=None):
    """B: list of residues modulo n = P^a Q^b (repeats allowed).  Returns the list of signs, in the order of B."""
    assert B and P != Q and P % 2 == 1 and Q % 2 == 1
    if star is None:
        star = rnd.randrange(len(B))
    xs = B[star]
    sign = [0] * len(B)
    Ca = [i for i in range(len(B)) if (B[i] - xs) % P ** a == 0]
    s = 1 if len(Ca) % 2 else 2
    give(Ca, s, sign, rnd)
    for i in range(a, 0, -1):
        rest = collections.defaultdict(list)
        for t in range(len(B)):
            if (B[t] - xs) % P ** (i - 1) == 0 and (B[t] - xs) % P ** i != 0:
                rest[B[t] % P ** i].append(t)
        assert len(rest) <= P - 1
        odd = []
        for cls, idx in sorted(rest.items()):
            if len(idx) % 2 == 0:
                give(idx, 0, sign, rnd)
            else:
                odd.append(idx)
        for t in range(0, len(odd) - 1, 2):
            give(odd[t], 1, sign, rnd)
            give(odd[t + 1], -1, sign, rnd)
        if len(odd) % 2:
            v = 1 if (s + 1) % Q != 0 else -1
            assert (s + v) % Q != 0
            give(odd[-1], v, sign, rnd)
            s += v
        assert s % Q != 0
    assert all(sign) and sum(sign) == s
    return sign


def roles(Np):
    """the ways to write N' = P^a Q^b with odd primes P != Q (a, b >= 0) that the lemma allows"""
    f = factor(Np)
    assert all(p % 2 for p in f) and len(f) <= 2, 'odd part not of the form p^a q^b'
    if len(f) == 0:
        return [(3, 0, 5), (5, 0, 3)]
    if len(f) == 1:
        p = next(iter(f))
        others = [q for q in (3, 5, 7) if q != p]
        return [(p, f[p], others[0]), (others[0], 0, p), (p, f[p], others[1])]
    (p, a), (q, b) = sorted(f.items())
    return [(p, a, q), (q, b, p)]


def step_two(mult, N, rnd, cls=None, role=None):
    """the paragraph's step.  mult: dict x -> 1 or 2, not all 2.  Returns a dict on Z_{2N}."""
    assert all(m in (1, 2) for m in mult.values()) and not all(m == 2 for m in mult.values())
    k = 0
    while N % 2 ** (k + 1) == 0:
        k += 1
    Np = N // 2 ** k
    P, a, Q = role if role else rnd.choice(roles(Np))
    def low_high(x):
        ys = (x, x + N)
        lo = [y for y in ys if y % 2 ** (k + 1) < 2 ** k]
        hi = [y for y in ys if y % 2 ** (k + 1) >= 2 ** k]
        assert len(lo) == 1 and len(hi) == 1
        return lo[0], hi[0]
    singles = [x for x in sorted(mult) if mult[x] == 1]
    classes = sorted(set(x % 2 ** k for x in singles))
    if cls is None:
        cls = rnd.choice(classes)
    assert cls in classes
    inc = [x for x in singles if x % 2 ** k == cls]
    sg = signs17([x % Np for x in inc], P, a, Q, rnd)
    out = {}
    for x, m in mult.items():
        lo, hi = low_high(x)
        if m == 2:
            out[lo] = 1
            out[hi] = 1
    for x, s in zip(inc, sg):
        lo, hi = low_high(x)
        out[lo if s == 1 else hi] = 1
    for x in singles:
        if x % 2 ** k != cls:
            lo, hi = low_high(x)
            out[rnd.choice((lo, hi))] = 1
    return out


def good(mult, N, lift):
    red = collections.Counter()
    for y, w in lift.items():
        red[y % N] += w
    return (all(w == 1 for w in lift.values()) and dict(red) == dict(mult)
            and pattern(lift, 2 * N) == pattern(mult, N))


def test_signs():
    rnd = random.Random(4)
    tot = bad = 0
    for n in [1, 3, 5, 7, 9, 15, 21, 25, 27, 35, 45, 49, 63, 75, 81, 189, 99, 135, 147, 175, 225]:
        f = factor(n)
        for P, a, Q in roles(n):
            for _ in range(120):
                size = rnd.randint(1, min(3 * n, 14))
                kind = rnd.random()
                if kind < 0.4:
                    B = [rnd.randrange(n) for _ in range(size)]
                elif kind < 0.7:           # sums of cosets: masks with many cyclotomic divisors before signing
                    B = []
                    for _c in range(rnd.randint(1, 2)):
                        c = rnd.choice(divisors(n)); x0 = rnd.randrange(n)
                        B += [(x0 + c * u) % n for u in range(n // c)]
                    B = B[:40]
                else:                      # few residues, many repeats
                    base = [rnd.randrange(n) for _ in range(rnd.randint(1, 3))]
                    B = [rnd.choice(base) for _ in range(size)]
                sg = signs17(B, P, a, Q, rnd)
                S = collections.Counter()
                for x, s in zip(B, sg):
                    S[x] += s
                tot += 1
                if any(not any(remainder(S, d)) for d in divisors(n)):
                    bad += 1
                    print('SIGNS FAIL', n, P, a, Q, B, sg)
    print(f'Lemma 17, my choice of signs from its proof: {tot} multisets on 21 moduli p^a q^b up to 225, every allowed choice '
          f'of the roles of the primes; the signed mask is divisible by some Phi_d, d | n (d = 1 included), in {bad}')


def exhaustive():
    rnd = random.Random(6)
    grand = bad = 0
    for N in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        k = 0
        while N % 2 ** (k + 1) == 0:
            k += 1
        tot = runs = fail = 0
        for w in itertools.product(range(3), repeat=N):
            mult = {x: m for x, m in enumerate(w) if m}
            if not mult or all(m == 2 for m in mult.values()):
                continue
            tot += 1
            classes = sorted(set(x % 2 ** k for x in mult if mult[x] == 1))
            for cls in classes:
                for role in roles(N // 2 ** k):
                    lift = step_two(mult, N, rnd, cls=cls, role=role)
                    runs += 1
                    if not good(mult, N, lift):
                        fail += 1
                        print('FAIL', N, mult, cls, role, sorted(lift))
        grand += runs
        bad += fail
        print(f'N={N} (k={k}, odd part {N // 2 ** k}): every multiset with multiplicities 0, 1, 2, nonempty, not every element 2: {tot}; '
              f'lifts (every admissible class, every allowed choice of the roles of the primes): {runs}; failures: {fail}', flush=True)
    print(f'exhaustive total: {grand} lifts, {bad} failures')


def random_run(seed):
    rnd = random.Random(seed)
    grand = bad = 0
    nonempty = 0
    for N in [14, 15, 18, 20, 21, 24, 25, 27, 28, 30, 36, 40, 42, 45, 48, 50, 54, 60, 63, 72, 75, 90, 98, 100, 108, 126, 150]:
        tot = fail = 0
        for _ in range(120 if N <= 60 else 50):
            mult = collections.Counter()
            if rnd.random() < 0.6:
                for _c in range(rnd.randint(1, 3)):
                    c = rnd.choice(divisors(N)); x0 = rnd.randrange(N)
                    for u in range(N // c):
                        mult[(x0 + c * u) % N] += 1
            else:
                for x in rnd.sample(range(N), rnd.randint(1, min(N, 9))):
                    mult[x] = rnd.choice((1, 1, 2))
            mult = {x: min(m, 2) for x, m in mult.items()}
            if all(m == 2 for m in mult.values()):
                mult[rnd.choice(list(mult))] = 1
            lift = step_two(mult, N, rnd)
            tot += 1
            nonempty += bool(pattern(mult, N))
            if not good(mult, N, lift):
                fail += 1
                print('FAIL', N, mult, sorted(lift))
        grand += tot
        bad += fail
    print(f'random (seed {seed}): {grand} multisets with multiplicities 1 and 2, not every element 2, on 27 groups Z_N, N from 14 to 150, '
          f'odd part p^a q^b ({nonempty} with a nonempty pattern); the step along 2 gave a set with exactly the pattern in {grand - bad}; failures: {bad}')


def claim1():
    A = {0: 4, 1: 2}
    print('Z_2, 0 four times and 1 twice: pattern (d > 1):', sorted(pattern(A, 2)), '; Phi_1 divides:', not any(remainder(A, 1)))
    gains = collections.Counter()
    n = 0
    for z in itertools.combinations([0, 2, 4, 6], 4):
        for o in itertools.combinations([1, 3, 5, 7], 2):
            S = {y: 1 for y in z + o}
            P = pattern(S, 8)
            n += 1
            gains[tuple(sorted(P))] += 1
            print('  set', sorted(S), 'on Z_8: divisors', sorted(P))
    print(f'  {n} set lifts; divisors gained, by number of lifts: {dict(gains)}; lifts that gain none: {gains.get((), 0)}')
    # how common is it?  every multiset with multiplicities <= 4, not every element 4, on Z_N, N = 1, 2, 3: all set lifts to Z_{4N}
    for N in (1, 2, 3):
        tot = none = 0
        ex = []
        for w in itertools.product(range(5), repeat=N):
            mult = {x: m for x, m in enumerate(w) if m}
            if not mult or all(m == 4 for m in mult.values()):
                continue
            P0 = pattern(mult, N)
            xs = sorted(mult)
            ok = False
            for choice in itertools.product(*[itertools.combinations(range(4), mult[x]) for x in xs]):
                S = {x + N * u: 1 for x, us in zip(xs, choice) for u in us}
                if pattern(S, 4 * N) == P0:
                    ok = True
                    break
            tot += 1
            if not ok:
                none += 1
                ex.append(dict(mult))
        print(f'  Z_{N} -> Z_{4 * N}: multisets with multiplicities <= 4, not every element 4: {tot}; with NO set lift that keeps the pattern exactly: {none}'
              + (f', e.g. {ex[:4]}' if ex else ''))


def needs():
    """what the step needs and what it does not: (i) 'not every element 2' (ii) every multiplicity <= 2 is needed for ANY set
    lift along 2 (trivial) (iii) all set lifts by brute force for tiny N: is there always a good one under the hypothesis?"""
    tot = bad = 0
    for N in [1, 2, 3, 4, 5, 6, 9, 10]:
        for bits in range(1, 2 ** N):
            supp = [x for x in range(N) if bits >> x & 1]
            A = {x: 2 for x in supp}
            S = {y: 1 for x in supp for y in (x, x + N)}
            tot += 1
            bad += (pattern(S, 2 * N) != pattern(A, N))
    print(f'every element doubled (every support, N in 1, 2, 3, 4, 5, 6, 9, 10): {tot} multisets; the one set that reduces to it gains a divisor in {bad}')
    tot = zero = 0
    for N in [1, 2, 3, 4, 5, 6, 7, 8]:
        for w in itertools.product(range(3), repeat=N):
            mult = {x: m for x, m in enumerate(w) if m}
            if not mult or all(m == 2 for m in mult.values()):
                continue
            P0 = pattern(mult, N)
            xs = sorted(mult)
            ng = 0
            for choice in itertools.product(*[itertools.combinations(range(2), mult[x]) for x in xs]):
                S = {x + N * u: 1 for x, us in zip(xs, choice) for u in us}
                ng += (pattern(S, 2 * N) == P0)
            tot += 1
            zero += (ng == 0)
    print(f'by brute force over all set lifts, N = 1..8: multisets with multiplicities 1, 2, not every element 2: {tot}; with no good set lift: {zero}')


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'signs': test_signs()
    elif what == 'exhaustive': exhaustive()
    elif what == 'random': random_run(int(sys.argv[2]))
    elif what == 'claim1': claim1()
    elif what == 'needs': needs()
