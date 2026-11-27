"""Third pass: "On the clock of 36 hours "12, 18 and 36" is one of them: to balance at those three and at no other divisor takes 19 marks."
(a) exact: a marking of 19 marks (rings of 9, of 6 and of 4 marks) balances at 12, 18 and 36 and at no other divisor of 36; so do
    all 4 * 6 * 9 ways of placing the three rings.
(b) that nothing smaller will do: a solver's verdict, not a proof (scipy's milp, which is HiGHS and works in rounded numbers).
    The least number of marks is sought among markings that balance at 12, 18 and 36 (22 equations in whole numbers) and, for each
    of the divisors 2, 3, 4, 6, 9, have some coefficient of the remainder at least 1 or at most -1 (a 0/1 variable picks the
    coefficient and its sign).  The marking the solver returns is then tested in whole numbers.
(c) the same question for one divisor at a time is not needed; (b) is the whole pattern.
usage: check36.py"""
import itertools, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
M = 36
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
def pattern(marks):
    a = [0] * M
    for x in marks: a[x % M] += 1
    return tuple(d for d in divisors(M) if d > 1 and not any(rem(a, phi(d))))

print('(a) rings: 9 marks four hours apart, 6 marks six hours apart, 4 marks nine hours apart')
ring = lambda start, gap: [(start + gap * i) % M for i in range(M // gap)]
ex = ring(0, 4) + ring(1, 6) + ring(2, 9)
print('    ', sorted(ex), ':', len(ex), 'marks; balances exactly at', pattern(ex))
pats = {}
for s4, s6, s9 in itertools.product(range(4), range(6), range(9)):
    pats.setdefault(pattern(ring(s4, 4) + ring(s6, 6) + ring(s9, 9)), 0); pats[pattern(ring(s4, 4) + ring(s6, 6) + ring(s9, 9))] += 1
print('     all', 4 * 6 * 9, 'placings of the three rings, by where they balance:', pats)
print('     each ring alone:', pattern(ring(0, 4)), pattern(ring(0, 6)), pattern(ring(0, 9)))

print('(b) least number of marks that balance at 12, 18, 36 and at no other divisor of 36: solver')
R = {d: np.array([rem([1 if i == x else 0 for i in range(M)], phi(d)) for x in range(M)]).T for d in divisors(M) if d > 1}   # R[d] @ a = remainder
want, forbid = (12, 18, 36), (2, 3, 4, 6, 9)
BIG = 200; UB = 40
nb = sum(2 * R[d].shape[0] for d in forbid)                 # one 0/1 variable for each (divisor, coefficient, sign)
n = M + nb
c = np.concatenate([np.ones(M), np.zeros(nb)])
cons = []
A = np.zeros((sum(R[d].shape[0] for d in want), n)); r = 0
for d in want:
    k = R[d].shape[0]; A[r:r + k, :M] = R[d]; r += k
cons.append(LinearConstraint(A, 0, 0))
pos = M
for d in forbid:
    k = R[d].shape[0]; pick = np.zeros((1, n))
    for i in range(k):
        for sgn in (+1, -1):
            row = np.zeros((1, n)); row[0, :M] = sgn * R[d][i]; row[0, pos] = -BIG      # sgn * coefficient >= 1 - BIG * (1 - z)
            cons.append(LinearConstraint(row, 1 - BIG, np.inf)); pick[0, pos] = 1; pos += 1
    cons.append(LinearConstraint(pick, 1, np.inf))                                     # at least one picked
cons.append(LinearConstraint(c.reshape(1, -1), 1, UB))
res = milp(c, constraints=cons, integrality=np.ones(n), bounds=Bounds(np.zeros(n), np.concatenate([np.full(M, UB), np.ones(nb)])))
print('     solver status:', res.status, res.message)
a = np.rint(res.x[:M]).astype(int); marks = [x for x in range(M) for _ in range(a[x])]
print('     least number by the solver:', int(round(res.fun)), '; its marking', marks)
print('     that marking in whole numbers:', len(marks), 'marks; balances exactly at', pattern(marks))
print('     (the solver works in rounded numbers: its "nothing smaller" is a verdict, not a proof; the proof is the theorem of the working note on clocks of p^n q^m hours, which the page says is proved in Lean)')
