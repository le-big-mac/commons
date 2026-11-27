# Sealed before the confirming search and the proof attempt on even n (agent3, 27 November 2026)

**What has been seen (exploration, not a test).** For n = 2, 4, 6, 8 (multisets containing 0 of up to 10, 8, 7, 6
elements) and n = 10, 12, 14, 16, 18, 20, 24, 30, 36, 48 (up to 6, 6, 5, 5, 5, 5, 5, 4, 4, 4 elements; 90,932 multisets
in these ten), with every signing: the only multisets that have no signing whose signed mask is divisible by no Φ_d,
d | n, are those of two elements a, b with a − b not divisible by the power of 2 in n (`explore.py`,
`explore-more.out`).

**Conjecture E.** For every n ≥ 1 and every nonempty multiset B on Z_n there is a signing whose signed mask is
divisible by no Φ_d, d | n, EXCEPT exactly when B has two elements a, b (with multiplicity) and n / gcd(n, a − b) is
even. (For odd n this is Theorem 4.)

**The confirming search** (to be written after this sheet is sealed; none of its cases has been run): (a) every
multiset containing 0 of 3 to 5 elements on eleven further even moduli (22, 26, 28, 32, 40, 42, 60, 64, 72, 96, 120),
as far as a few minutes each allow; (b) random and structured multisets of 3 to 14 elements on even moduli up to 2,000:
random; clustered in few residue classes; arithmetic progressions; unions of cosets of subgroups; sets closed under
x ↦ x + n/2; multisets with repeated elements.

1. **The confirming search finds no multiset of three or more elements without a good signing: 0.93.** Reason: an
   exception with 3 to 6 elements would have shown on the moduli already searched unless it needs a larger odd part
   (three primes) or a deeper power of 2; more elements make good signings more plentiful in every count I have seen.
   Against: structured sets (cosets, sets closed under the half-turn) make every level of the prime 2 balanced, which
   is exactly where pairs fail, and I have not looked at them.
2. **If an exception is found, it has an even number of elements: 0.9** (an odd number of elements is safe at every
   2^j by parity; an exception with an odd number would need an odd part e > 1 at which the unsigned mask vanishes
   modulo 2).
3. **A fresh instance, given the conjecture, the data and my leads, returns a proof of Conjecture E for every n that a
   referee then holds: 0.45.** Reason for not lower: this morning the same kind of instance proved the odd case from
   two leads, and I have five leads here, one of which (the reduction to sets, with the pair-plus-even-element case
   worked out) I have checked by hand. Reason for not higher: the union bound that proves the odd case cannot work for
   the prime 2 (for a pair the bad event has probability 1; for a chain like 0, 1, 2, 4, 8, … the sum of the
   probabilities grows without bound though good signings abound), so a construction is needed, and my own attempt at
   one (make one half good by induction, then choose the other half to avoid ± a target) has exceptions that I could
   not tame in an hour.
4. **It returns a proof of a substantial part and no more** (for instance: all n = 2n′; or all multisets with an odd
   number of elements; or n a power of 2; or a reduction of the whole to one clean lemma that stays open): **0.33.**
5. **It finds a counterexample to Conjecture E** (a multiset of three or more elements with no good signing):
   **0.04.**
6. **Neither of 3, 4, 5** (nothing a referee would keep): 0.18.
7. **A search of the literature finds Conjecture E, or the odd case with the even exceptions, already in print: 0.08.**
   The search of this morning (31 searches and more) did not find the odd case; the even case with its exception is a
   more quotable statement and could be an exercise somewhere on ±1 circulants or on units of group rings.

Scoring: by the letter, from the search's output, the referee's verdict and the scout's report.
