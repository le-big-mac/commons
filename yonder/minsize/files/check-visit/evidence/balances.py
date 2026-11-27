"""Exact test of every balance the open text states.
"Balance at d" (d steps to a full turn; the mark at hour x puts a weight x/d of a turn on) is: sum over marks of exp(2 pi i x/d) = 0,
which holds exactly when the cyclotomic polynomial Phi_d divides A(X) = sum of X^x over the marks (with repeats).  Tested here in
whole numbers (polynomial remainder by Phi_d), not in rounded numbers; the centre of gravity is printed beside it as a float.
usage: balances.py"""
import itertools, math, cmath
from collections import Counter

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def polymul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b): r[i + j] += x * y
    return r

def polydivexact(a, b):          # a / b for monic-or-unit-leading b, whole numbers, exact
    a = a[:]; q = [0] * (len(a) - len(b) + 1)
    for i in range(len(a) - len(b), -1, -1):
        c = a[i + len(b) - 1] // b[-1]; q[i] = c
        for j, y in enumerate(b): a[i + j] -= c * y
    assert not any(a), 'not exact'
    return q

_phi = {}
def phi(n):                      # cyclotomic polynomial, coefficients low to high
    if n in _phi: return _phi[n]
    p = [-1] + [0] * (n - 1) + [1]             # X^n - 1
    for d in divisors(n):
        if d < n: p = polydivexact(p, phi(d))
    _phi[n] = p; return p

def rem(a, b):                   # remainder of a by monic b, whole numbers
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

def pattern(marks, M, with1=False):
    return tuple(d for d in divisors(M) if (d > 1 or with1) and balances_at(marks, M, d))

def cog(marks, d):
    z = sum(cmath.exp(2j * math.pi * x / d) for x in marks) / len(marks)
    return abs(z)

def show(name, marks, M):
    print(f'{name}: marks {list(marks)} on the clock of {M} hours')
    for d in divisors(M):
        b = balances_at(marks, M, d)
        spots = Counter(x % d for x in marks)
        print(f'   d = {d:2d} ({d} steps to a turn): exact {"BALANCES" if b else "does not balance"};  distance of centre of gravity from centre {cog(marks, d):.6f};  weights by spot {dict(sorted(spots.items()))}')
        assert b == (cog(marks, d) < 1e-9)
    print('   balances exactly at (1 left out):', pattern(marks, M))

print('phi(12) =', phi(12), ' phi(6) =', phi(6), ' phi(4) =', phi(4), ' phi(3) =', phi(3), ' phi(2) =', phi(2))
print()
print('==== A. The balances stated in "The question" and "The answer" (12 hours) ====')
show('the pair', (0, 6), 12)
show('the triangle', (1, 5, 9), 12)
show('the five marks', (0, 6, 1, 5, 9), 12)
show('"3 alone"', (0, 1, 2), 12)
assert pattern((0, 6), 12) == (4, 12)
assert pattern((1, 5, 9), 12) == (3, 6, 12)
assert pattern((0, 6, 1, 5, 9), 12) == (12,)
assert pattern((0, 1, 2), 12) == (3,)
print()
print('nothing balances at 1 (any non-empty marking): d = 1 tested for every multiset of 1..5 marks on 12 hours below')

print()
print('==== B. Every multiset of 1 to 5 marks on the clock of 12 hours: least number of marks for each pattern reached ====')
M = 12
least = {}; count = {}; example = {}
any1 = 0
for n in range(1, 6):
    for ms in itertools.combinations_with_replacement(range(M), n):
        if balances_at(ms, M, 1): any1 += 1
        pat = pattern(ms, M)
        count[(n, pat)] = count.get((n, pat), 0) + 1
        if pat not in least: least[pat] = n; example[pat] = ms
print('multisets that balance at 1:', any1)
for pat in sorted(least, key=lambda p: (least[p], p)):
    print(f'   pattern {pat if pat else "(nowhere)"}: least number {least[pat]}, e.g. {example[pat]}')
print()
for want in [(12,), (4, 12), (3,)]:
    print(f'pattern {want}: least number of marks = {least[want]};  number of multisets of each size 1..5 with exactly this pattern:',
          [count.get((n, want), 0) for n in range(1, 6)])
assert least[(12,)] == 5 and least[(4, 12)] == 2 and least[(3,)] == 3
print('so: "12 alone" takes five marks and no fewer; "4 and 12" two; "3 alone" three  -- as the open text says')

print()
print('==== C. The sentence of "In short" read literally: "balance in one way and in no other ... no four marks can" ====')
for n in range(1, 6):
    one = {pat: c for (k, pat), c in count.items() if k == n and len(pat) == 1}
    sets_one = Counter()
    for ms in itertools.combinations(range(M), n):
        pat = pattern(ms, M)
        if len(pat) == 1: sets_one[pat] += 1
    print(f'   {n} marks: markings (repeats allowed) that balance at exactly one divisor: {sum(one.values())}  by divisor {dict(sorted(one.items()))};  of them without repeats: {sum(sets_one.values())} {dict(sorted(sets_one.items()))}')
ex4 = [ms for ms in itertools.combinations(range(M), 4) if len(pattern(ms, M)) == 1][:3]
print('   examples of four marks at different hours that balance at exactly one divisor:', [(ms, pattern(ms, M)) for ms in ex4])
print('   two marks 0 and 2:', pattern((0, 2), 12), '  two marks 0 and 1:', pattern((0, 1), 12), '  three marks 0, 1, 2:', pattern((0, 1, 2), 12))

print()
print('==== D. The clock of 36 hours ====')
show('the five marks', (0, 6, 1, 5, 9), 36)
assert pattern((0, 6, 1, 5, 9), 36) == (12,)
M = 36; fewest = None; n12 = Counter()
for n in range(1, 5):
    for ms in itertools.combinations_with_replacement(range(M), n):
        if pattern(ms, M) == (12,): n12[n] += 1
print('multisets of 1, 2, 3, 4 marks on 36 hours that balance at 12 and at no other divisor of 36:', [n12[n] for n in range(1, 5)])
assert sum(n12.values()) == 0
print('so no four marks (and no fewer) do, as the open text says')

print()
print('==== E. The walk: how many times it goes round, and which numbers of steps there are ====')
print('divisors of 12 other than 1:', [d for d in divisors(12) if d > 1])
for d in (12, 6, 4, 3, 2):
    print(f'   {d} steps to a turn: a step is 1/{d} of a turn = {12 // d} hour-lengths of the clock; counting 0..11 and back to 0 goes round {12 // d} time(s)')
print('hour 6 at a quarter turn an hour:', 6 / 4, 'turns')

print()
print('==== F. Two things said in the folds that the open text leans on ====')
show('18 hours, five different hours', (0, 1, 2, 4, 10), 18)
show('6 hours, pair and triangle', (0, 3, 0, 2, 4), 6)
