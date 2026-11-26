"""A trial of the lifting lemma as Pnq/Lift.lean states it (exists_lift), by brute force and by nothing from the proof.
For N and an odd prime r (which may divide N): does every nonempty multiset w on Z_N of a few elements have a multiset w'
on Z_{N r} that reduces to w modulo N and whose mask polynomial sum w'(y) X^y is divisible by no cyclotomic polynomial
Phi_d with d dividing N r and not N?   (Phi_d divides the mask exactly when the mask vanishes at exp(2 pi i / d).)
usage: python -I lift-try.py > lift-try.out"""
import cmath, itertools, math

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def lifts(w, N, r):
    """every multiset on Z_{N r} that reduces to the multiset w (a sorted tuple of residues modulo N, with repeats)"""
    seen = set()
    for ks in itertools.product(range(r), repeat=len(w)):
        m = tuple(sorted(x + N * k for x, k in zip(w, ks)))
        if m not in seen: seen.add(m); yield m

def bad(m, ds):
    """the d in ds with Phi_d dividing the mask of the multiset m"""
    return [d for d in ds if abs(sum(cmath.exp(2j * math.pi * y / d) for y in m)) < 1e-9]

if __name__ == '__main__':
    total = fails = 0
    for r in (3, 5, 2):
        for N in range(1, 9 if r == 3 else 7):
            new = [d for d in divisors(N * r) if N % d]
            tried = lacking = 0; first = None
            for size in range(1, 5 if r < 5 else 4):
                for w in itertools.combinations_with_replacement(range(N), size):
                    tried += 1
                    if not any(not bad(m, new) for m in lifts(w, N, r)):
                        lacking += 1; first = first or w
            if r != 2: total += tried; fails += lacking
            print('r = %d, N = %d (the new divisors of N r: %s): %d multisets of 1 to %d elements; without such a lift: %d%s' % (
                r, N, new, tried, 4 if r < 5 else 3, lacking, (' (the first: %s)' % (first,)) if first else ''))
    print('for the odd primes 3 and 5: %d multisets tried, %d without a lift (the lemma says none); the rows for r = 2 are outside the lemma' % (total, fails))
