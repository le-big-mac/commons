"""Referee's test of the sentence 'Consequence for lifting along 2' of small-multisets.md, from the proof of Lemma 18
(lifting along 2) of minsize.tex:  N = 2^k N' (N' odd), A a nonempty multiset on Z_N, c a class modulo 2^k that holds an
element of A, B = the residues modulo N' of the elements of A in that class.  For EVERY signing of B that is good on
Z_N' (first element +, and also its negative): lift the elements of the class with sign + low (y mod 2^(k+1) < 2^k), those
with sign - high, all other elements low.  Claim: for every divisor d of 2N:  Phi_d | A'  iff  d | N and Phi_d | A.
Also counted: signings of B that are NOT good, and for how many of them the lift gains a divisor (it gains one only if
the sums over the other classes vanish too; the count shows that the test can fail).
usage: ref_lift2.py SEED COUNT"""
import sys, random
from reflib import *
rng = random.Random(int(sys.argv[1])); count = int(sys.argv[2])
tot = dict(multisets=0, classes=0, good=0, bad=0, bad_and_claim_fails=0)
for _ in range(count):
    N1 = rng.choice([1, 3, 9, 15, 21, 27, 45, 63, 75, 105]); k = rng.randint(0, 3); N = 2 ** k * N1
    m = rng.randint(1, 8); fN = factor(N)
    if N > 1 and rng.random() < 0.6:
        A = []
        while len(A) < m:
            q = rng.choice(list(fN)); c0 = rng.randrange(N)
            if len(A) + q <= m and rng.random() < 0.85: A += [(c0 + (N // q) * j) % N for j in range(q)]
            else: A.append(rng.choice(A) if A and rng.random() < 0.4 else rng.randrange(N))
    else:
        A = [rng.randrange(N) for _ in range(m)]
    divA = set(bad_levels(N, A, [1] * len(A)))            # d | N with Phi_d | A
    tot['multisets'] += 1
    for c in sorted(set(x % 2 ** k for x in A)):
        idx = [j for j, x in enumerate(A) if x % 2 ** k == c]
        B = [A[j] % N1 for j in idx]
        g = good_all(N1, B)
        sg = sign_matrix(len(B))
        tot['classes'] += 1
        for row, gv in zip(sg, g):
            for flip in (1, -1):
                signs = {j: int(v) * flip for j, v in zip(idx, row)}
                Ap = []
                for j, x in enumerate(A):
                    lifts = [x, x + N]
                    low = [y for y in lifts if y % 2 ** (k + 1) < 2 ** k]
                    high = [y for y in lifts if y % 2 ** (k + 1) >= 2 ** k]
                    assert len(low) == 1 and len(high) == 1
                    Ap.append(high[0] if signs.get(j, 1) < 0 else low[0])
                divAp = set(bad_levels(2 * N, Ap, [1] * len(Ap)))
                claim = (divAp == divA)                   # divA has only divisors of N
                if gv:
                    tot['good'] += 1
                    assert claim, ('lifting along 2 fails for a good signing', N, A, c, B, list(row), flip, sorted(divAp), sorted(divA))
                else:
                    tot['bad'] += 1; tot['bad_and_claim_fails'] += (not claim)
print(f'lifting along 2 from a good signing of one class: {tot["multisets"]} multisets of 1..8 elements on Z_N, N = 2^k N\', k = 0..3, '
      f'N\' in 1, 3, 9, 15, 21, 27, 45, 63, 75, 105; {tot["classes"]} classes; good signings (both global signs) {tot["good"]}: '
      f'the lift has exactly the divisors of A in every case; signings that are not good {tot["bad"]}, the lift gains a divisor for {tot["bad_and_claim_fails"]} of them')
