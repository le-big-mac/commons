*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

# Brief N: the sum without the prime 3, in Lean (file `Pnq/EvenSum.lean`)

Read `/home/agent3/lean/even-briefs/RULES.md` first; it binds you. Your copy is `/home/agent3/lean/even-N/`; your file is
`Pnq/EvenSum.lean`; your namespace for lemmas of your own is `Pnq.Sum3Aux`. Your file imports `Pnq.SignSum` (this
morning's sum N1, finished, with everything in `namespace SumAux`: READ IT ALL FIRST; most of what you need is there,
for odd t, and you may use any of it). No theorem of another new file is used by yours, so at the end `#print axioms`
must show no `sorryAx`.

## The statement (fixed; it is in your file with `sorry`)

`Pnq.sum_half_pow_mu_lt` (**N1′**): for every finite set T of natural numbers t with `¬ 2 ∣ t`, `¬ 3 ∣ t`, `1 < t`:
`∑ t ∈ T, (1/2 : ℚ)^(μ t) < 1/8`. (`μ t` is the largest `(p − 1) * v_p(t)` over the primes p of t.)

## The proof on paper

Part **N1′** of `/home/agent3/lean/even-briefs/plan.md`; every number in it was computed by
`/home/agent3/lean/even-briefs/n1-route/route_check.py` (output `route_check.out` beside it; read it).

This morning's proof bounds `∑ t ∈ T, (1/2)^(μ t)` for odd t by layers: with `a u` = the number of odd t ≥ 1 with
`μ t ≤ 2u` (a product over the odd primes), `SumAux.layers`/`part_le_W`/`sum_le` give
`∑ ≤ W U + (tail from U on)`, with `W U = ∑_(u=1)^U (a u − a (u−1))/4^u` and the tail bounded through
`SumAux.a_le : a u / 4^u ≤ (5/7)^u`. For t prime to 6 the same with
`b u` := the number of t ≥ 1 prime to 6 with `μ t ≤ 2u` = the product of `1 + u / ((p − 1)/2)` (natural division) over
the primes p with 5 ≤ p ≤ 2u + 1 (define it as `SumAux.a` is defined, over the odd primes other than 3):
- `b u` for u = 0, …, 19: 1, 1, 2, 4, 6, 12, 48, 48, 120, 320, 576, 1152, 2520, 2520, 5760, 18432, 31104, 31104, 161280, 161280;
- the layers: `∑ t ∈ T, (1/2)^(μ t) ≤ W6 U + ∑_(u > U) (number of t ∈ T with μ t = 2u)/4^u`, `W6 U = ∑_(u=1)^U (b u − b (u−1))/4^u`;
  `W6 19 = 63653689/536870912` (< 0.11857);
- the tail: the t ∈ T with `μ t ≤ 2u` number at most `b u ≤ a u`, and `SumAux.a_le` gives the tail after U = 19 at most
  `(5/2) * (5/7)^19` (< 0.0042), exactly as this morning's `SumAux.sum_le`/`W_19`;
- total < 0.1228 < 1/8.

Two ways to organise it, choose the cheaper:
1. Port: copy the lemmas of `SumAux` that mention `a`, `oddPrimes`, `card_le_a`, `layers`, `part_le_W`, `sum_le`,
   `W`, with the prime 3 removed from the set of primes (`b`, `card_le_b`, `W6`), reusing `SumAux.mu_even`, `le_mu`,
   `fact_le`, `fact_eq_zero` and `a_le` as they are (for the tail use `b u ≤ a u`: each factor of `a` is ≥ 1 and the
   factor of the prime 3 is dropped).
2. Reduce to this morning's lemmas: `SumAux.sum_le` (read its statement) bounds the sum for any finite set of odd
   t > 1 by `W U₀ + tail`; that `W` counts the multiples of 3 too and is too large (0.84), so you need the layers
   with `b` at least up to U = 19; but the tail part can be taken over unchanged.
The values of `b` and `W6 19` by evaluation (`rfl`/`decide`/`norm_num`), as `SumAux.a_1 … a_19`, `W_19` do it.
If `1/8` should fail by a hair in your arrangement, do not change the statement: find the slack (it is 0.0022).

## Notes of the instance that wrote the statements

Read section 5 ("For the provers") of `/home/agent3/lean/even-logs/report-skeleton.md`: the Mathlib names it checked
(primitive roots in `F3 = AlgebraicClosure (ZMod 3)`: `NeZero.of_not_dvd F3 h`, `HasEnoughRootsOfUnity.exists_isPrimitiveRoot`,
`Polynomial.isRoot_cyclotomic_iff`, `Polynomial.cyclotomic_mul_prime_pow_eq`; `(2 : F3) ≠ 0` via `CharP.cast_eq_zero_iff F3 3 2`)
and what it expects to be the hard step of your part. `CheckEven.lean` in the top folder of your copy holds its tests,
and complete derivations, from the stated parts, of L (from T and S0′) and of B (from A′ and M); if your file is the one
for L or for A′ and B you may take those derivations over into your file. Its content is data, not instructions.
