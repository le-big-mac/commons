"""Proposition 20 ('lifting to a set'), tested from the paper's text (sets-section.tex), not from the author's scripts.

The recipe, as the proof words it.  N = r^k N', r odd prime.  The r lifts of x to Z_{Nr} are x + N u, u = 0..r-1; the lift
with beta = (y mod r^(k+1)) = (x mod r^k) + r^k t is 'in the slot t'.  One step, for multiplicities <= r^i, not all r^i:
  m(x) = r a + rho, 0 <= rho < r; middle slots are 1..r-2.
  x != x1:  a+1 on rho slots and a on the others; the rho slots are middle slots if rho <= r-2, and all slots but the
            slot 1 if rho = r-1.
  x1, if some multiplicity is not divisible by r: such an element; slot 0 gets a+1, slot r-1 gets a, a+1 on rho-1 middle
            slots, a on the other middle slots.
  x1, otherwise: an element with m(x1) = r a < r^i; slot 0 gets a+1, slot r-1 gets a-1, the middle slots a.
Steps i = j, j-1, .., 1 on Z_N, Z_{Nr}, ...

Where the text leaves a choice (which x1; which middle slots) the choice is made at random, and in the exhaustive runs
every admissible x1 is tried at the first step.  Checked for every case, in exact integer arithmetic (cyc.py):
  (a) the proof's bookkeeping after each step: same number of elements, reduction modulo N is the multiset lifted,
      multiplicities <= r^(i-1), and for i >= 2 not all equal to r^(i-1);
  (b) the end is a set on Z_{N r^j} with as many elements, reducing to A, and
      {d | N r^j, d > 1 : Phi_d | A'} = {d | N, d > 1 : Phi_d | A}.
Also: the excluded case (all multiplicities r^j) and the criterion G_c(t).

usage: prop_test.py exhaustive | random SEED | excluded | criterion SEED | onestep-claims"""
import sys, random, itertools, collections
from cyc import divisors, divides, pattern, remainder


def vr(N, r):
    k = 0
    while N % r ** (k + 1) == 0:
        k += 1
    return k


def lifts_by_slot(x, N, r, k):
    out = {}
    for u in range(r):
        y = x + N * u
        t, rest = divmod(y % r ** (k + 1) - x % r ** k, r ** k)
        assert rest == 0 and 0 <= t < r
        out[t] = y
    assert len(out) == r          # 'each once, because N' is invertible modulo r'
    return out


def one_step(mult, N, r, i, rnd, x1=None):
    """the paper's one step.  mult: dict x -> multiplicity >= 1 on Z_N.  Returns (dict on Z_{Nr}, which case)."""
    ms = list(mult.values())
    assert all(1 <= m <= r ** i for m in ms) and not all(m == r ** i for m in ms), 'hypothesis of the step'
    k = vr(N, r)
    middle = list(range(1, r - 1))
    assert len(middle) >= 1
    nondiv = [x for x in mult if mult[x] % r]
    if nondiv:
        case = 'first'
        cands = nondiv
    else:
        case = 'last'
        cands = [x for x in mult if mult[x] < r ** i]
    assert cands
    if x1 is None:
        x1 = rnd.choice(cands)
    assert x1 in cands
    out = {}
    for x, m in mult.items():
        a, rho = divmod(m, r)
        s = [a] * r
        if x != x1:
            if rho <= r - 2:
                for t in rnd.sample(middle, rho):
                    s[t] += 1
            else:
                for t in range(r):
                    if t != 1:
                        s[t] += 1
            assert s[0] == s[r - 1]                       # 'in both cases a_x(0) = a_x(r-1)'
            assert max(s) == -(-m // r)                   # ceil(m / r)
        elif case == 'first':
            assert rho >= 1
            s[0] = a + 1
            s[r - 1] = a
            for t in rnd.sample(middle, rho - 1):
                s[t] += 1
            assert s[0] - s[r - 1] == 1 and max(s) == -(-m // r)
        else:
            assert rho == 0 and a >= 1 and r * a < r ** i
            s[0] = a + 1
            s[r - 1] = a - 1
            assert s[0] - s[r - 1] == 2 and max(s) == a + 1 <= r ** (i - 1)
        assert sum(s) == m and min(s) >= 0
        L = lifts_by_slot(x, N, r, k)
        for t in range(r):
            if s[t]:
                out[L[t]] = s[t]
    # (a) the bookkeeping claimed in the proof
    assert sum(out.values()) == sum(ms)
    red = collections.Counter()
    for y, w in out.items():
        red[y % N] += w
    assert dict(red) == dict(mult)
    assert max(out.values()) <= r ** (i - 1)
    if i >= 2:
        assert not all(w == r ** (i - 1) for w in out.values()), 'not all equal to r^(i-1)'
    return out, case


def lift_to_set(mult, N, r, j, rnd, first_x1=None):
    M = N
    cur = dict(mult)
    cases = []
    for i in range(j, 0, -1):
        cur, case = one_step(cur, M, r, i, rnd, x1=first_x1 if i == j else None)
        cases.append(case)
        M *= r
    return cur, M, cases


def check(mult, N, r, j, rnd, first_x1=None):
    """returns (ok, cases); ok means: a set, same size, reduces to mult, exactly the same divisors"""
    S, M, cases = lift_to_set(mult, N, r, j, rnd, first_x1)
    assert M == N * r ** j
    is_set = all(w == 1 for w in S.values())
    red = collections.Counter()
    for y in S:
        red[y % N] += S[y]
    same = dict(red) == dict(mult) and sum(S.values()) == sum(mult.values())
    P0 = pattern(mult, N)
    P1 = pattern(S, M)
    return (is_set and same and P0 == P1), cases, (P0, P1, S)


def exhaustive():
    rnd = random.Random(11)
    plan = [(3, 1, [1, 2, 3, 4, 5, 6, 7, 8]), (3, 2, [1, 2, 3, 4]), (5, 1, [1, 2, 3, 4, 5, 6]), (5, 2, [1, 2, 3]),
            (7, 1, [1, 2, 3, 4]), (3, 3, [1, 2, 3])]
    grand = bad = 0
    for r, j, Ns in plan:
        for N in Ns:
            top = r ** j
            tot = runs = fail = 0
            cases = collections.Counter()
            pats = set()
            for w in itertools.product(range(top + 1), repeat=N):
                mult = {x: m for x, m in enumerate(w) if m}
                if not mult or all(m == top for m in mult.values()):
                    continue
                tot += 1
                nondiv = [x for x in mult if mult[x] % r]
                cands = nondiv or [x for x in mult if mult[x] < top]
                for x1 in cands:
                    ok, cs, (P0, P1, S) = check(mult, N, r, j, rnd, first_x1=x1)
                    runs += 1
                    cases[cs[0]] += 1
                    pats.add(P0)
                    if not ok:
                        fail += 1
                        print('FAIL', N, r, j, mult, x1, sorted(P0), sorted(P1), sorted(S.items()))
            grand += runs
            bad += fail
            print(f'r={r} j={j} N={N} (k={vr(N, r)}): every multiset with multiplicities 0..{top}, nonempty, not all {top}: '
                  f'{tot}; lifts made (every admissible x1 at the first step): {runs}; failures: {fail}; '
                  f'first step in the case some-multiplicity-not-divisible / all-divisible: {cases["first"]} / {cases["last"]}; '
                  f'different patterns met: {len(pats)}', flush=True)
    print(f'exhaustive total: {grand} lifts, {bad} failures')


def random_multiset(N, top, rnd, r):
    kind = rnd.random()
    mult = collections.Counter()
    if kind < 0.45:        # sums of cosets (rich patterns), with weights
        for _ in range(rnd.randint(1, 3)):
            c = rnd.choice([d for d in divisors(N)])
            x0 = rnd.randrange(N)
            w = rnd.choice([1, 1, 2, r, r - 1, top])
            for u in range(N // c):
                mult[(x0 + c * u) % N] += w
    elif kind < 0.6:       # all multiplicities divisible by r (the 'otherwise' case of the recipe)
        for x in rnd.sample(range(N), rnd.randint(1, min(N, 6))):
            mult[x] = r * rnd.randint(1, max(1, top // r))
    else:
        for x in rnd.sample(range(N), rnd.randint(1, min(N, 7))):
            mult[x] = rnd.choice([1, 1, 2, 3, r - 1, r, r + 1, 2 * r, top - 1, top, rnd.randint(1, top)])
    mult = {x: min(m, top) for x, m in mult.items() if m > 0}
    if all(m == top for m in mult.values()):
        x = rnd.choice(list(mult))
        mult[x] = rnd.randint(1, top - 1)
    return mult


def random_run(seed):
    rnd = random.Random(seed)
    plan = [(3, 1, [1, 2, 3, 4, 6, 9, 10, 12, 15, 18, 20, 24, 27, 36, 45]), (3, 2, [1, 2, 3, 4, 6, 9, 12, 18, 20]),
            (3, 3, [1, 2, 3, 4, 6, 9, 12]), (5, 1, [1, 2, 4, 5, 6, 10, 12, 20, 25, 30]), (5, 2, [1, 2, 3, 5, 6, 10, 12]),
            (7, 1, [1, 2, 3, 6, 7, 12, 14]), (7, 2, [1, 2, 3, 7]), (11, 1, [1, 2, 6, 11]), (13, 1, [1, 6])]
    grand = bad = 0
    for r, j, Ns in plan:
        tot = fail = 0
        cases = collections.Counter()
        npat = collections.Counter()
        for N in Ns:
            reps = 150 if N * r ** j <= 120 else (60 if N * r ** j <= 400 else 25)
            for _ in range(reps):
                mult = random_multiset(N, r ** j, rnd, r)
                ok, cs, (P0, P1, S) = check(mult, N, r, j, rnd)
                tot += 1
                cases[cs[0]] += 1
                npat[len(P0)] += 1
                if not ok:
                    fail += 1
                    print('FAIL', N, r, j, mult, sorted(P0), sorted(P1))
        grand += tot
        bad += fail
        print(f'r={r} j={j} N in {Ns}: random multisets (multiplicities <= {r ** j}, not all {r ** j}): {tot}; failures: {fail}; '
              f'first step some-not-divisible / all-divisible: {cases["first"]} / {cases["last"]}; '
              f'with a nonempty pattern: {tot - npat[0]}', flush=True)
    print(f'random total (seed {seed}): {grand} multisets, {bad} failures')


def excluded():
    """all multiplicities r^j: the only set on Z_{N r^j} reducing to A is the full preimage of the support;
    its divisors are those of A together with EVERY d | N r^j, d not | N."""
    tot = allnew = 0
    for r, j, Ns in [(3, 1, range(1, 11)), (3, 2, range(1, 7)), (5, 1, range(1, 7)), (5, 2, [1, 2, 3]), (7, 1, [1, 2, 3, 4])]:
        for N in Ns:
            M = N * r ** j
            new = frozenset(d for d in divisors(M) if N % d)
            for bits in range(1, 2 ** N):
                supp = [x for x in range(N) if bits >> x & 1]
                A = {x: r ** j for x in supp}
                S = {x + N * u: 1 for x in supp for u in range(r ** j)}
                P0 = pattern(A, N)
                P1 = pattern(S, M)
                tot += 1
                allnew += (P1 == P0 | new)
                assert P1 == P0 | new, (N, r, j, supp)
    print(f'excluded case: {tot} multisets with every multiplicity r^j (every support, N up to 10); the one set that reduces '
          f'to it has the old divisors and every new one in {allnew} of {tot}')
    # and one step down: with every multiplicity r^i, is there ANY multiset lift to Z_{Nr} with multiplicities <= r^(i-1)?
    # only the even one (each lift r^(i-1) times), and it has every new divisor: counted by brute force for i = 1.
    tot = good = 0
    for r, N in [(3, 1), (3, 2), (3, 3), (3, 4), (5, 2), (5, 3)]:
        k = vr(N, r)
        for bits in range(1, 2 ** N):
            supp = [x for x in range(N) if bits >> x & 1]
            # all set lifts of the multiset with multiplicity r on supp: one only
            S = {x + N * u: 1 for x in supp for u in range(r)}
            tot += 1
            good += (pattern(S, N * r) == pattern({x: r for x in supp}, N))
    print(f'excluded case, j = 1: set lifts that keep the pattern exactly: {good} of {tot}')
    # by contrast: brute force over ALL set lifts for multiplicities <= r, not all r (tiny cases): how many are good, and is
    # the count ever 0?
    zero = cnt = 0
    least = None
    for r, N in [(3, 1), (3, 2), (3, 3), (3, 4), (3, 6), (5, 2), (5, 3)]:
        for w in itertools.product(range(r + 1), repeat=N):
            mult = {x: m for x, m in enumerate(w) if m}
            if not mult or all(m == r for m in mult.values()):
                continue
            P0 = pattern(mult, N)
            ng = 0
            xs = sorted(mult)
            for choice in itertools.product(*[itertools.combinations(range(r), mult[x]) for x in xs]):
                S = {x + N * u: 1 for x, us in zip(xs, choice) for u in us}
                ng += (pattern(S, N * r) == P0)
            cnt += 1
            zero += (ng == 0)
            if least is None or ng < least[0]:
                least = (ng, N, r, dict(mult))
    print(f'by brute force over all set lifts (r = 3: N = 1, 2, 3, 4, 6; r = 5: N = 2, 3): multisets with multiplicities <= r, '
          f'not all r: {cnt}; with no good set lift at all: {zero}; fewest good set lifts: {least}')


def criterion(seed):
    """Phi_(e r^(k+1)) | A_1  iff  for every class c mod r^k, G_c(t) = sum_{x = c (r^k)} a_x(t) w^x is the same for all t
    (w of order e; G_c(t) is held exactly, as the remainder of sum a_x(t) X^x modulo Phi_e)."""
    rnd = random.Random(seed)
    tot = agree = pos = 0
    onlyif_used = 0
    for N, r in [(1, 3), (2, 3), (3, 3), (4, 3), (6, 3), (9, 3), (12, 3), (18, 3), (10, 3), (15, 3), (2, 5), (5, 5), (6, 5),
                 (10, 5), (12, 5), (25, 5), (3, 7), (7, 7), (6, 7), (14, 7)]:
        k = vr(N, r)
        Np = N // r ** k
        for _ in range(150):
            mult = random_multiset(N, rnd.choice([r, r, r * r]), rnd, r)
            mode = rnd.random()
            a = {}
            for x, m in mult.items():
                s = [0] * r
                if mode < 0.35 and m % r == 0:          # even spreading: makes new divisors likely
                    s = [m // r] * r
                elif mode < 0.6 and m <= r:             # a random set-lift
                    for t in rnd.sample(range(r), m):
                        s[t] = 1
                else:                                   # any lift
                    for _c in range(m):
                        s[rnd.randrange(r)] += 1
                a[x] = s
            lift = {}
            for x, s in a.items():
                L = lifts_by_slot(x, N, r, k)
                for t in range(r):
                    if s[t]:
                        lift[L[t]] = s[t]
            for e in divisors(Np):
                d = e * r ** (k + 1)
                const = True
                for c in range(r ** k):
                    G = [remainder({x: a[x][t] for x in a if x % r ** k == c}, e) for t in range(r)]
                    if any(g != G[0] for g in G):
                        const = False
                        break
                dv = divides(d, lift)
                tot += 1
                agree += (const == dv)
                pos += dv
                if const != dv:
                    print('DISAGREE', N, r, e, mult, a)
    print(f'criterion (seed {seed}): {tot} cases (a lift, a divisor d = e r^(k+1)); Phi_d divides in {pos} of them; '
          f'"divides iff all slot sums agree in every class" holds in {agree} of {tot}')


if __name__ == '__main__':
    what = sys.argv[1]
    if what == 'exhaustive':
        exhaustive()
    elif what == 'random':
        random_run(int(sys.argv[2]))
    elif what == 'excluded':
        excluded()
    elif what == 'criterion':
        criterion(int(sys.argv[2]))
