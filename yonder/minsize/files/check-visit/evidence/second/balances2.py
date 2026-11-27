"""Second pass: exact tests of what the changed open text states.
"Balance at d" is tested in whole numbers: the cyclotomic polynomial Phi_d divides the sum of X^x over the marks (with repeats).
usage: balances2.py"""
import itertools
from collections import Counter

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]
def polydivexact(a, b):
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1] // b[-1]; q[i] = c
        for j, y in enumerate(b): a[i + j] -= c * y
    assert not any(a)
    return q
_phi = {}
def phi(n):
    if n in _phi: return _phi[n]
    p = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n):
        if d < n: p = polydivexact(p, phi(d))
    _phi[n] = p; return p
def rem(a, b):
    a = a[:]
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1]
        if c:
            for j, y in enumerate(b): a[i + j] -= c * y
    return a[:len(b) - 1]
def balances_at(marks, M, d):
    a = [0] * M
    for x in marks: a[x % M] += 1
    return not any(rem(a, phi(d)))
def pattern(marks, M):
    return tuple(d for d in divisors(M) if d > 1 and balances_at(marks, M, d))

print('==== A. "On a clock of 12 hours there are five such ways" ====')
print('numbers of steps to a full turn on 12 hours (divisors of 12 but 1):', [d for d in divisors(12) if d > 1])

print('\n==== B. "12 alone" on 12 hours: 2 + 3 = 5, "a pair and a triangle" ====')
M = 12; five = []
for n in range(1, 6):
    for ms in itertools.combinations_with_replacement(range(M), n):
        if pattern(ms, M) == (12,):
            five.append(ms)
print('markings of 1 to 5 marks that balance at 12 alone:', len(five), '; their sizes:', sorted(set(len(m) for m in five)))
def pair_and_triangle(ms, M):
    c = Counter(ms)
    for a in range(M // 2):                       # a pair of opposite marks a, a + M/2
        for t in range(M // 3):                   # a triangle t, t + M/3, t + 2M/3
            want = Counter([a, a + M // 2]) + Counter([t, t + M // 3, t + 2 * M // 3])
            if want == c: return (a, a + M // 2), (t, t + M // 3, t + 2 * M // 3)
    return None
print('of them, a pair of opposite marks with a triangle of evenly spaced marks:', sum(1 for m in five if pair_and_triangle(m, M)), 'of', len(five))
print('the page\'s marking:', pair_and_triangle((0, 1, 5, 6, 9), 12))
print('the first formula for "12 alone" (no power of 2 in the pattern, e = 0; one short power, 4, k = 1): 2^0 * (2^1 + 3) =', 2 ** 0 * (2 ** 1 + 3))

print('\n==== C. The clock of 6 hours: "five marks that balance at 6 and at no other divisor always mark one hour twice" ====')
M = 6; by = {}
for n in range(1, 8):
    for ms in itertools.combinations_with_replacement(range(M), n):
        if pattern(ms, M) == (6,): by.setdefault(n, []).append(ms)
print('markings of 1 to 7 marks on 6 hours that balance at 6 and at no other divisor, by number of marks:', {n: len(v) for n, v in sorted(by.items())})
least = min(by)
print('least number of marks:', least)
mult = Counter()
for ms in by[5]:
    c = Counter(ms); mult[tuple(sorted(c.values(), reverse=True))] += 1
print('the five-mark ones, by how often each marked hour is marked:', dict(mult))
print('every one of them marks exactly one hour twice and no hour more often:', all(sorted(Counter(m).values(), reverse=True) == [2, 1, 1, 1] for m in by[5]))
print('every one of them is a pair of opposite marks with a triangle:', all(pair_and_triangle(m, 6) for m in by[5]))
sets6 = [s for n in range(1, 7) for s in itertools.combinations(range(6), n) if pattern(s, 6) == (6,)]
print('markings of any number of marks at different hours on 6 hours that balance at 6 and at no other divisor:', len(sets6))

print('\n==== D. The clock of 18 hours: "the marks 0, 1, 2, 4 and 10 do it" ====')
m18 = (0, 1, 2, 4, 10)
print('0, 1, 2, 4, 10 on 18 hours balance exactly at:', pattern(m18, 18), '; all at different hours:', len(set(m18)) == 5)
few = Counter()
for n in range(1, 5):
    for ms in itertools.combinations_with_replacement(range(18), n):
        if pattern(ms, 18) == (6,): few[n] += 1
print('markings of 1, 2, 3, 4 marks on 18 hours (repeats allowed) that balance at 6 and at no other divisor of 18:', [few[n] for n in range(1, 5)])
print('wound back onto 6 hours the five marks are', sorted(x % 6 for x in m18), 'with pattern', pattern([x % 6 for x in m18], 6))
print('18 = 6 * 3: the factor is', 18 // 6, '; the least number is 5; so the factor is not greater than the least number (the full account says so)')

print('\n==== E. The clock of 36 hours: "12, 18 and 36" is a pattern in which every multiple of a chosen divisor is chosen too ====')
def upset(D, M): return all((m in D) for d in D for m in divisors(M) if m % d == 0)
print('"12, 18 and 36":', upset({12, 18, 36}, 36), ';  "12 alone":', upset({12}, 36), ' (36 is a multiple of 12 and is missing)')
D = {12, 18, 36}; non = [d for d in divisors(36) if d not in D]; corners = [c for c in non if not any(x != c and x % c == 0 for x in non)]
print('largest divisors of 36 not in the pattern:', corners, '; rings of', [36 // c for c in corners], 'marks; together', sum(36 // c for c in corners), '(the full account says 9, 6 and 4: 19)')
print('the five marks on 36 hours balance exactly at:', pattern((0, 6, 1, 5, 9), 36))

print('\n==== F. "Why ask?": two sets tile the 12-hour clock exactly when their sizes multiply to 12 and at every divisor but 1 one of them balances ====')
M = 12; divs = [d for d in divisors(M) if d > 1]
pat = {}
subsets = {n: list(itertools.combinations(range(M), n)) for n in range(1, M + 1)}
for n in subsets:
    for s in subsets[n]: pat[s] = set(pattern(s, M))
tested = agree = tilings = 0
for a in (1, 2, 3, 4, 6, 12):
    b = M // a
    for A in subsets[a]:
        for B in subsets[b]:
            tile = len({(x + y) % M for x in A for y in B}) == M
            crit = all((d in pat[A]) or (d in pat[B]) for d in divs)
            tested += 1; agree += (tile == crit); tilings += tile
print(f'pairs of sets whose sizes multiply to 12: {tested}; of them tilings: {tilings}; the two tests agree on: {agree}')
# pairs whose sizes do not multiply to 12 cannot tile (each hour covered exactly once needs 12 sums)
print('the pair 0 and 6 with the turns 0..5:', len({(x + y) % 12 for x in (0, 6) for y in range(6)}) == 12, '; 0 and 6 balance at', sorted(pat[(0, 6)]), '; the turns 0..5 balance at', sorted(pat[(0, 1, 2, 3, 4, 5)]))
