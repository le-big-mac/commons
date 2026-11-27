"""The paper's Lemma (lifting), tested as the proof builds it.  N = r^k N', r an odd prime, M = N r.
(a) the r lifts of x have residues modulo r^(k+1) equal to (x mod r^k) + r^k t, t = 0..r-1, each once  [every x, every case];
(b) lift every element to its lift with t = 0 except ONE copy of one element x0, which goes to its lift with t = 1:
    for every divisor d of M (d = 1 included):  Phi_d | A'  iff  d | N and Phi_d | A.   Tried for EVERY choice of x0 in the support.
(c) controls: the plain lift (all t = 0); the paper's bad example; r = 2 with the same recipe.
Multisets: all multisets up to a size for small N; random ones (half uniform, half sums of cosets with a few points added) otherwise.
usage: python -I t2_lemma.py"""
import sys; sys.path.insert(0, '/home/agent3/paper/referee-lift')
import itertools, random
from cyc import divisors, pattern
rnd = random.Random(20261126)
def split(N, r):
    k = 0
    while N % r == 0: N //= r; k += 1
    return k, N
def lift_maps(N, r):
    """L[t][x] = the lift of x with residue (x mod r^k) + r^k t modulo r^(k+1); checks (a)"""
    k, N1 = split(N, r); M = N * r; R = r ** (k + 1)
    L = [[None] * N for _ in range(r)]
    for x in range(N):
        betas = sorted((x + j * N) % R for j in range(r))
        assert betas == [(x % r ** k) + r ** k * t for t in range(r)], (N, r, x, betas)      # claim (a)
        for j in range(r):
            y = x + j * N; t = ((y % R) - (x % r ** k)) // r ** k
            L[t][x] = y
    return L
def check(A, N, r, L, stats, need_all_x0=True):
    """A: sorted list of elements of range(N) (with repeats).  Returns list of failing x0."""
    M = N * r
    PA = pattern(A, N, with_one=True)
    want = frozenset(d for d in divisors(M) if N % d == 0 and d in PA)
    bad = []
    for x0 in sorted(set(A)):
        A2 = [L[0][x] for x in A]; A2[A.index(x0)] = L[1][x0]
        assert sorted(y % N for y in A2) == sorted(A)                 # it is a lift, same number of elements
        if pattern(A2, M, with_one=True) != want: bad.append(x0)
        stats['lifts tried'] += 1
    plain = pattern([L[0][x] for x in A], M, with_one=True)
    stats['plain lift keeps the pattern'] += (plain == want)
    stats['multisets'] += 1
    stats['with a nonempty pattern'] += bool(want)
    return bad
def random_multiset(N):
    if rnd.random() < 0.5: return sorted(rnd.randrange(N) for _ in range(rnd.randint(1, 10)))
    el = []
    for _ in range(rnd.randint(1, 3)):
        c = rnd.choice(divisors(N)); x0 = rnd.randrange(N); el += [(x0 + c * j) % N for j in range(N // c)]
    for _ in range(rnd.randint(0, 2)): el.append(rnd.randrange(N))
    return sorted(el)
tot = dict.fromkeys(['multisets', 'lifts tried', 'plain lift keeps the pattern', 'with a nonempty pattern'], 0); failures = []
print('--- exhaustive: every multiset on Z_N with at most S elements, r odd')
for N, r, S in [(1, 3, 6), (1, 5, 6), (2, 3, 7), (3, 3, 7), (4, 3, 6), (6, 3, 5), (9, 3, 5), (12, 3, 4), (18, 3, 4), (2, 5, 7), (5, 5, 5), (6, 5, 5), (10, 5, 4),
                (15, 5, 4), (4, 7, 6), (7, 7, 4), (6, 7, 5), (12, 5, 4), (27, 3, 3), (36, 3, 3), (15, 3, 4), (45, 3, 3), (25, 5, 3), (3, 11, 6), (6, 13, 4)]:
    L = lift_maps(N, r); st = dict.fromkeys(tot, 0)
    for s in range(1, S + 1):
        for A in itertools.combinations_with_replacement(range(N), s):
            bad = check(list(A), N, r, L, st)
            if bad: failures.append((N, r, A, bad))
    for key in tot: tot[key] += st[key]
    print(f'N = {N}, r = {r} (k = {split(N, r)[0]}), M = {N * r}, S = {S}: {st}', flush=True)
print('--- random multisets, larger groups, r odd')
for N, r, T in [(12, 3, 3000), (36, 3, 3000), (54, 3, 2000), (108, 3, 1500), (20, 5, 3000), (100, 5, 1500), (45, 5, 2000), (75, 3, 2000), (75, 5, 1500), (60, 7, 1500),
                (30, 3, 3000), (30, 5, 3000), (72, 3, 2000), (24, 11, 1500), (98, 7, 1000), (225, 3, 800), (225, 5, 600), (210, 3, 600), (81, 3, 1500), (125, 5, 600)]:
    L = lift_maps(N, r); st = dict.fromkeys(tot, 0)
    for _ in range(T):
        A = random_multiset(N); bad = check(A, N, r, L, st)
        if bad: failures.append((N, r, A, bad))
    for key in tot: tot[key] += st[key]
    print(f'N = {N}, r = {r} (k = {split(N, r)[0]}), M = {N * r}, {T} random: {st}', flush=True)
print('TOTAL, r odd:', tot); print('FAILURES of the lemma, r odd:', len(failures), failures[:5])
print("--- the paper's example after the proof: N = 2, r = 3, A = {0, 0, 1}")
print('   least representatives 0, 0, 1 with one 0 raised by N = 2: {0, 2, 1}; pattern in Z_6:', sorted(pattern([0, 2, 1], 6)), ' (3 does not divide N = 2: a new divisor)')
print('   least representatives with the 1 raised by 2 instead: {0, 0, 3}; pattern in Z_6:', sorted(pattern([0, 0, 3], 6)))
L = lift_maps(2, 3)
for x0 in (0, 1):
    A = [0, 0, 1]; A2 = [L[0][x] for x in A]; A2[A.index(x0)] = L[1][x0]
    print(f'   the proof\'s lift with x0 = {x0}: {sorted(A2)}; pattern in Z_6: {sorted(pattern(A2, 6))}; pattern of A in Z_2: {sorted(pattern(A, 2))}')
print('--- control: the same recipe with r = 2 (the proof does not cover it)')
ctl = dict.fromkeys(tot, 0); bad2 = []
for N, S in [(1, 6), (2, 6), (3, 6), (4, 5), (6, 5), (9, 4), (12, 4), (15, 4)]:
    k, N1 = split(N, 2); M = 2 * N; R = 2 ** (k + 1)
    Lr = [[None] * N for _ in range(2)]
    for x in range(N):
        for j in range(2):
            y = x + j * N; Lr[((y % R) - (x % 2 ** k)) // 2 ** k][x] = y
    for s in range(1, S + 1):
        for A in itertools.combinations_with_replacement(range(N), s):
            A = list(A); PA = pattern(A, N, with_one=True); want = frozenset(d for d in divisors(M) if N % d == 0 and d in PA)
            ctl['multisets'] += 1; worked = 0
            for x0 in sorted(set(A)):
                A2 = [Lr[0][x] for x in A]; A2[A.index(x0)] = Lr[1][x0]; ctl['lifts tried'] += 1
                worked += pattern(A2, M, with_one=True) == want
            if worked == 0:
                # does SOME lift work?
                some = any(pattern([Lr[t][x] for x, t in zip(A, ts)], M, with_one=True) == want for ts in itertools.product((0, 1), repeat=len(A)))
                bad2.append((N, A, some))
print(f'   r = 2, exhaustive small cases: {ctl["multisets"]} multisets; the recipe fails for every choice of x0 in {len(bad2)} of them;')
print('   first few (N, A, does some other lift keep the pattern?):', bad2[:6])
print('   of those, with NO lift at all keeping the pattern:', sum(1 for b in bad2 if not b[2]))
