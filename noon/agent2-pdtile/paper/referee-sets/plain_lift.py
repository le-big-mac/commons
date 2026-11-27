"""A control for my test, and the lift of Kiss, Laba, Marshall and Somlai, Section 2.1 (after (2.2)): the copies of a go to
a, a + M, ..., a + (w - 1) M.  On Z_{N r} (multiplicities <= r, not all r) this is a set that reduces to the multiset and keeps
every divisor Phi_d, d | N.  How often does it also gain none?  Every multiset with multiplicities 0..r on Z_N, nonempty,
not all r; exact patterns (cyc.py)."""
import itertools
from cyc import pattern
for r, Ns in [(3, [1, 2, 3, 4, 5, 6, 7]), (5, [1, 2, 3, 4, 5])]:
    tot = keep = 0; first = None
    for N in Ns:
        for w in itertools.product(range(r + 1), repeat=N):
            mult = {x: m for x, m in enumerate(w) if m}
            if not mult or all(m == r for m in mult.values()): continue
            S = {x + N * u: 1 for x, m in mult.items() for u in range(m)}
            P0 = pattern(mult, N); P1 = pattern(S, N * r)
            assert P0 <= P1
            tot += 1; keep += (P0 == P1)
            if P0 != P1 and first is None: first = (N, dict(mult), sorted(S), sorted(P0), sorted(P1))
    print(f'r = {r}, N in {Ns}: {tot} multisets; the plain lift a, a+N, .. keeps the old divisors in all, and gains none in {keep}; '
          f'first that gains one: N = {first[0]}, multiset {first[1]} -> set {first[2]}: divisors {first[3]} -> {first[4]}')
