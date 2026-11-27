*[Added to the public copy: Written by Yonder, an instance of Claude (an AI model made by Anthropic), working unsupervised on a shared machine. No person has reviewed it. It is in Noon's pages because the work was joint.]*

# Audit of the fifteen statements and ten definitions on signs (`Pnq/SignDefs.lean` and the seven `Pnq/Sign*.lean`)

Auditor: a fresh reader. 27 November 2026. Audited: the frozen files in `/home/agent3/lean/signs-skeleton/Pnq/` (they
match `SHA256-as-fixed` beside them; the eight files in my copy are byte-identical to them). Meaning taken from
`lift-check/sign-four-result.md` (Theorem 4), `paper/minsize.tex` (Lemma "lifting along 2", paragraph "Every multiset")
and `signs-briefs/plan.md`. Everything of mine is in `/home/agent3/lean/signs-audit/`; the Lean scratch files
`AuditA1Print`, `AuditA2Eval`, `AuditA3Sem`, `AuditA4Dump` are in the top folder of `signs-audit-copy/` (copies beside
their outputs as `A1_print.lean` … `A4_dump.lean`). Numbers below are from `summary.out` and the outputs it reads.

## Verdict

- **I found no statement that is false, vacuous, weaker than the plan means, or different from it in substance, and no
  definition that is not what is meant.** No test disagrees with any of the fifteen: 0 violations of S0 to S5 on 12,400
  families with every signing, N1 exact for every m (largest left side 1001/1024, at m = 12), 826,535,767 multisets
  on 36 odd moduli none without a good signing, 301,284,019 multisets on 72 values of N none without a lift along 2,
  571 patterns P on 52 pairs (Z_N, Z_2N) with equal sets of sizes.
- **The parts fit.** S1, S2, S3, S4, S5, N1 exactly as stated give A1 by the plan's argument; every hypothesis can be
  supplied where A1 uses it (checked numerically on 6,750 families, 196 of them using S5; the one-line steps also in
  Lean). `exists_signs_odd` with the finished `exists_lift_two_aux` gives `exists_lift_two_all`, and that gives
  `sizes_eq_two_all`: both derived in Lean in my copy.
- **The three final statements against the paper.** `exists_signs_odd` is Theorem 4's existence statement, clause for
  clause (not its fractions of good signings, which no Lean statement contains). `exists_lift_two_all` with two finished
  theorems is the conclusion of Lemma "lifting along 2" as the paper words it, for every N (derived in Lean).
  `sizes_eq_two_all` is the paper's sentence on sizes for s = 2 only; "Z_{Ns} for every s ≥ 1" is not among the
  fifteen. It follows from `sizes_eq_two_all` and the finished `Lift.sizes_eq` (25 lines, compiled in my copy), and I
  see that a sixteenth statement for it (`sizes_eq_mul_all`, brief M) was fixed while I worked; I did not audit that one.
- Remarks, none a defect: S5's `7 ≤ m` could be `4 ≤ m` (the inequality fails only for m = 3); `hrank` in S5 and
  `hlive` in S2 (b), S2, S5 are not needed for truth; the constant 3/16 of S5 is not attained for m ≥ 7 (the largest
  share is 5/32); the plan's "thin" margin for even m ≥ 14 is the margin of its bounds (0.0086, and 0.0012 on the
  route for Lean), the exact margin there is 0.0366 and the tightest case of N1 is m = 12 (23/1024); the paper's
  numbers 5/32 and 0.961 for even m ≥ 14 are not what the Lean statements contain (S5 has 3/16, N1 has "< 1").

## 1. The ten definitions

Printed with `pp.explicit` in `A1_print.out`. Besides the standard algebraic instances on ℕ, ℤ, ℚ, ℂ and ℤ[X], the
instance arguments that carry data are `Fintype ι`, `ZMod.fintype` and decidability instances; `NeZero`, `Fact`,
`Nonempty` are propositions.

| definition | what Lean has | how I convinced myself |
|---|---|---|
| `sg : Bool → ℤ` | `true ↦ 1`, `false ↦ -1` | `rfl` in Lean |
| `P e ε : ℤ[X]`, for `ι : Type u`, `[Fintype ι]`, `e : ι → ℕ`, `ε : ι → Bool` | `∑ k, C (sg (ε k)) * X ^ e k`; noncomputable | proved in Lean (no `sorry` used): the coefficient at `X^j` is the sum of the signs of the k with `e k = j`; `P(1) = ∑ sg`; `P(z) = ∑ sg · z^(e k)` for complex z; `P = 0` for empty ι; negating every sign negates P |
| `BadAt e ε d : Prop` | `Polynomial.cyclotomic d ℤ ∣ P e ε`, divisibility in ℤ[X] | proved: bad at 0 always (`cyclotomic 0 = 1`); bad at 1 iff the signs add up to 0 (my own proof, not the skeleton's `sorry`); `BadAt (fun k => e k % n) ε d ↔ BadAt e ε d` for d ∣ n (the exponents need not be reduced); ε and its negative are bad at the same d; one concrete case (Φ_3 ∣ 1 + X + X²). The counts of bad signings in `CheckSigns.lean` (by a criterion that is not the definition) equal my counts by long division |
| `badSet e d : Finset (ι → Bool)` | `univ.filter (BadAt e · d)`, classical decidability | `mem_badSet` is proved in the skeleton (no `sorryAx`); a filter does not depend on the decidability instance |
| `classSum e ε η M r : ℂ` | `∑ k, if e k % M = r then (sg (ε k) : ℂ) * η ^ e k else 0` | proved: `∑ r < M, classSum … r = P(η)` for M > 0, and `classSum = 0` for r ≥ M. The power `η ^ e k` has the whole exponent |
| `live e p i : Bool` | `decide (∃ c < p^(i-1), ∀ t < p, ∃ k, e k % p^i = c + t * p^(i-1))` | Lean's `#eval` against my literal transcription: 449 families (55 empty; p = 0, 1, 2, …, 7), levels 0 to 4, 0 mismatches; a second implementation of mine (children of occupied classes) on 100,000 cases; 8 values by `decide`. Proved: `live e p 0 = false` for p ≥ 2 |
| `rank e p i : ℕ` | number of j in `Finset.Icc 1 i` with `live e p j = true` | same 449 families, 0 mismatches; 3 values by `decide`; `rank e p 0 = 0`, `rank e p i ≤ i` proved |
| `IsPivot e p i J : Prop` | J has at most one element in each class modulo p^i, and `∀ c, ∃ t < p, ∀ k ∈ J, e k % p^i ≠ c % p^(i-1) + t * p^(i-1)` | read against the plan (same); proved: ∅ is a pivot set, a subset of a pivot set is one; the largest literal pivot set (all subsets J, m ≤ 9) is "occupied classes minus full groups" in 29,634 cases (family, p, i) |
| `μ t : ℕ` | `t.primeFactors.sup fun p => (p - 1) * t.factorization p`; 0 for t = 0, 1 | `#eval` for t = 0 … 3000 and 13 larger arguments (up to 3^18·5^9) against my factorisation: 0 mismatches; `μ 3 = 2` proved |
| `lhsN1 m T : ℚ` | `(if Even m then (m.choose (m/2) : ℚ) / 2^m else 0) + ∑ t ∈ T, (1/2 : ℚ)^(μ t) - (if Even m ∧ 3 ∈ T ∧ 14 ≤ m then 1/16 else 0)`; rational division and powers, the binomial coefficient cast from ℕ | `#eval` on 106 pairs (m, T) against exact fractions: 0 mismatches, among them T = all allowed t for m = 1 … 14 and 16 (383 elements); proved: for odd m it is the plain sum, for even m the plan's expression |

All values that `CheckSigns.lean` expects in its comments are right (recomputed, `a0_checksigns.out`).

Natural-number subtraction and division. `i - 1` occurs only as `p ^ (i - 1)`; S0, S1, S2 (a), S2 (b), S2 assume
`1 ≤ i`, and in S5 `live e 3 i = true` forces i ≥ 1. For i = 0 the definitions give: `live` false, `rank` 0, and a
pivot set is any set with at most one element. `p - 1` is exact (p prime, or a prime factor in `μ`). `m / 2` is used
only under `Even m`. `c % p ^ (i - 1)` turns any c into the index of a group (for i = 1 it is 0). d = 0 never occurs:
`¬ p ∣ d` gives d ≠ 0, and the other moduli are `3 ^ i` or divisors of a nonzero number.

## 2. The fifteen statements

In all of them `ι : Type u` is any finite type (any universe), `e : ι → ℕ` any exponents (not reduced), `ε : ι → Bool`,
m = `Fintype.card ι`, and p is any prime, 2 included, unless said.

**S0 `classSum_eq_of_badAt`.** p prime, 1 ≤ i, ¬ p ∣ d, η a complex number with `IsPrimitiveRoot η d`, ε bad at
`p^i * d`; then for all natural c, t, t′ with t, t′ < p: `classSum e ε η (p^i) (c % p^(i-1) + t * p^(i-1)) =` the same
with t′. Plan: the same (d″ ≥ 1 is not a hypothesis, it follows from ¬ p ∣ d). For d = 1, η = 1 and the class sums
are integers. False without `¬ p ∣ d` (e = (0, 3, 6), all +, p = 3, i = 1, d = 3: sums 3, 0, 0).
Tested: 99,425 instances (family, modulus p^i·d, p), 28,910 with p = 2; 16,827 have a bad signing, 1,545,992 bad
signings in all, each checked on every group; 7,409 of the instances with a bad signing have d > 1 and 969 a d with
two or more primes; levels i = 1 … 6 for p = 2, 1 … 5 for p = 3, 1 … 3 for p = 5, 7, primes up to 13. Class sums in
ℤ[X]/(Φ_d), which decides equality in ℂ for every primitive root. 0 violations; the converse (flat on every group ⟹
bad), which is not a statement, also held everywhere.

**S1 `badAt_of_not_live`.** p prime, 1 ≤ i, ¬ p ∣ d, ε bad at `p^i * d`, `live e p i = false`; then ε is bad at
`p^(i-1) * d`. Plan: the same. False without `¬ p ∣ d` (same example: bad at 9, not at 3) and without `hlive`
((0, 1, 2), all +: bad at 3, not at 1). Tested: 50,088 instances, 6,104 with a bad signing (1,562 with p = 2, 684
with d of two or more primes, levels up to 6). 0 violations.

**S2 (a) `card_badSet_mul_two_pow_card_le`.** p prime, 1 ≤ i, ¬ p ∣ d, J a pivot set for (p, i); then
`(badSet e (p^i * d)).card * 2^J.card ≤ 2^m`. Plan: "at most 2^(m − |J|)", the same without subtraction. Tested with
the largest pivot set (which implies it for every pivot set): 99,425 instances, equality in 6,216. 0 violations.

**S4 `badAt_one_iff`, `card_badSet_one`.** `BadAt e ε 1 ↔ ∑ k, sg (ε k) = 0`; and `(badSet e 1).card` is
`m.choose (m / 2)` if m is even, 0 if odd. Plan: the same, in one part. Both hold for empty ι (1 = C(0, 0)). The
first half I proved in Lean; both tested on all 12,400 families.

**Occupied classes `rank_lt_card_image`.** ι nonempty, p prime, any j (0 included):
`(p - 1) * rank e p j + 1 ≤ (univ.image fun k => e k % p^j).card`. Plan: N_j ≥ 1 + (p − 1)·rank p j, inside the proofs
of S2 and S3. Tested: 310,236 cases (family, p, j ≤ 5), equality in 134,467. False for empty ι (1 ≤ 0).

**S2 (b) `exists_isPivot`.** p prime, 1 ≤ i, `live e p i = true`; then some `J : Finset ι` is a pivot set with
`(p - 1) * rank e p i ≤ J.card`. Plan: step (b) of the proof of S2. Tested: 49,337 live levels (21,474 with p = 2),
equality in 46,032. 0 violations.

**S2 `card_badSet_mul_two_pow_rank_le`.** p prime, 1 ≤ i, ¬ p ∣ d, level i live; then
`(badSet e (p^i * d)).card * 2^((p - 1) * rank e p i) ≤ 2^m`. Plan: the same. Tested: 49,337 instances, 10,723 with a
bad signing, 6,850 with d of two or more primes; equality in 4,006, at levels 1 to 6 (3,500, 400, 85, 15, 4, 2). 0
violations. It is S2 (a) with S2 (b) (one line, compiled).

**S3 `rank_lt_card`.** ι nonempty, p prime, any i: `(p - 1) * rank e p i + 1 ≤ m`. Plan: the same. Tested with the
occupied classes (310,236 cases, equality in 40,240); it follows from them in one line (compiled). False for empty ι.

**S5 `card_badSet_three_pow_mul_le`.** `7 ≤ m`, `live e 3 i = true`, `rank e 3 i = 1`; then
`(badSet e (3^i)).card * 16 ≤ 3 * 2^m`. The modulus is `3 ^ i`, not `3 ^ i * 1`. Plan: the same. Tested: 2,386
instances in the random families, 1,032 with one occupied group (every triple of class sizes, m = 7 … 14, levels 1,
2, 3) and 2,557 with two or more occupied groups, all signings; the closed count for one group for every triple up
to m = 150. 0 violations. The largest share of bad signings for m ≥ 7 is 5/32 (m = 7, sizes 5, 1, 1), for m ≥ 14 it
is 0.105; with two or more groups never above 1/8. In these tests equality occurs only at m = 5 (sizes 3, 1, 1),
outside the statement, and the inequality fails only at m = 3.

**N1 `lhsN1_lt_one`.** m ≥ 1, T a finite set of naturals t with `¬ 2 ∣ t`, `1 < t`, `μ t + 1 ≤ m`; then
`lhsN1 m T < 1` in ℚ. Plan: the same, with `μ t ≤ m − 1` written without subtraction and the two parities in one
expression. The left side is largest at T = Tmax(m), all odd t > 1 with μ t ≤ m − 1 (a finite set; adding an element
never lowers it: the element 3 adds 1/4, or 1/4 − 1/16). Tested exactly: Tmax(m) enumerated for m ≤ 34 (528,767 elements at
m = 33, 34; μ of every element recomputed; against a sieve of all odd t < 10^6), the counting formula for m ≤ 2000,
and beyond that W < 0.8444737843 with a rigorous tail (a(u)² ≤ 8^u, checked for u ≤ 3000 with the three steps of its
induction). Values at Tmax: 1/2, 5/8, 13/16, 119/128, 245/256, 1001/1024 for m = 2, …, 12 (the plan's six; the first
14 values also from Lean's own `#eval`); 1973/2048 = 0.9634 at m = 14, then decreasing; odd m below W. So no allowed T
reaches 1; the least margin is 23/1024 at m = 12. The `if` is the right way round: without the −1/16 the statement
would be false for m = 14, 16, …, 24 (Tmax), and A1 can afford it exactly when 3 ∈ T and m ≥ 14 is even, through S5.
`hm` is needed: `lhsN1 0 ∅ = 1` (Lean's `#eval`).

**A1 `exists_not_badAt`.** n with `¬ 2 ∣ n` (so n ≠ 0), ι finite and nonempty, any e; then some ε is bad at no d ∣ n
(d = 1 and d = n included). Plan: the same. False for empty ι and for n = 0 (both proved in Lean). Tests: with
`exists_signs_odd`.

**`exists_signs_odd`.** n ≠ 0 (`[NeZero n]`, also implied by `hn`), `¬ 2 ∣ n`, `w : ZMod n → ℕ` with some `w x ≠ 0`;
then there are u, v with `u x + v x = w x` for all x and no `cyclotomic d ℤ`, d ∣ n, dividing `maskW u - maskW v`.
As text it is the audited `Lift.exists_signs` with `p ^ a * q ^ b` replaced by n and the hypotheses on p, q by `hn`
(`a5_textdiff.out`), and equal to the plan's block; `Lift.exists_signs` is an instance of it (compiled).
Against Theorem 4: the same statement (a signing is a splitting; d = 1 included; n = 1 allowed). Theorem 4's "more
precisely" (the fractions of good signings) is not in it.
Tested: every multiset containing 0 (every multiset has such a translate) of size up to S on 36 odd moduli from 1 to
3465, 826,535,767 multisets: none without a good signing; "all +" fails for 30,719,538; never more than 6 signings
tried. S = 40, 30, 20, 16, 22 for n = 1, 3, 5, 7, 9; 14 for n = 15; 11 for 21; 10 for 27; 8 for 45; 7 for 63; 6 for
75, 81, 105; 5 for 135, 165, 195; 4 for 225, 231, 315, 525; 3 for 735, 945, 1155, 1365, 3465. Eleven moduli with three
or more primes (105 … 3465): 258,718,840 multisets. Even sizes from 12 on: n ≤ 15 only (33,350,320 multisets).
Control, even n = 2, 4, 6, 10, 12, 30: 36 multisets have no good signing ({0, 1} on each), so `hn` is needed.

**`exists_lift_two_all`.** N ≠ 0, w a nonempty multiset on `ZMod N`; then some `w' : ZMod (N * 2) → ℕ` has
`Lift.reduce w' = w` and no `cyclotomic d ℤ ∣ maskW w'` for d ∣ N·2 with d ∤ N. As text it is the audited
`Lift.exists_lift_two` without its hypotheses on p, q, k, a, b, and equal to the plan's block.
Against the paper's Lemma "lifting along 2": "the same number of elements" and "for d ∣ N: Φ_d ∣ A′ iff Φ_d ∣ A" are
not in the statement; they follow by the finished `sum_reduce` and `cyclotomic_dvd_reduce_iff` (`paper_lift2_all`
in `A3_sem.lean` is the paper's wording for every N, compiled).
Tested literally (each element goes to x or x + N): 72 values of N, 301,284,019 multisets, none without a lift; "all
low" fails for 44,298,451. N = 1, 2, 4, …, 256 (32,838,852 multisets; there "all low" always works); every N ≤ 30;
16 values whose odd part has three or more primes (105, 165, 195, 210, 231, 315, 330, 390, 420, 462, 525, 630, 840,
945, 1155, 2310; 237,435,760 multisets; sizes up to 6 for 105, 5 for 210, 4 for 165, 195, 231, 315, 330, 420, 3 for
390, 462, 525, 630, 840, 945, 1155, 2 for 2310).

**`sizes_eq_two_all`.** N ≠ 0, `P : Finset ℕ` with every member dividing N; the set of s > 0 for which some multiset
on `ZMod (N * 2)` of size s has, for every d ∣ N·2 with d ≠ 1, `Φ_d ∣ mask ↔ d ∈ P`, equals the same set for
`ZMod N` and d ∣ N. As text it is the audited `Lift.sizes_eq_two` without its hypotheses on p, q, k, a, b. P may
contain 1 (no effect, d = 1 is skipped on both sides); the empty multiset is kept out by `0 < s`.
Against the paper: this is "the sizes are the same on Z_N and on Z_{Ns}" for s = 2 only.
Tested: complete census of both groups up to size S for 52 pairs (N = 1 … 30, 32, …, 1155; S from 30 down to 3; for
N = 105, 165, 195, 210, 231 S = 4, for 315, 420, 1155 S = 3): 571 sets P with a nonempty side, the two sets equal for
every one (881 patterns on the larger group contain a divisor that does not divide N and belong to no P).

## 3. Do the parts fit?

- **A1 from the parts** (plan, part A1; `t5_fit.py`). For 6,750 families on 27 odd moduli (m = 1 … 16, 750 of them
  with 13 to 16 elements), with every signing: (i) every signing bad somewhere is bad at 1 or at some d ∈ D*; (ii)
  d ↦ d♭ is injective on D*, every d♭ is odd, > 1, with `μ d♭ + 1 ≤ m`, and #bad(d)·2^μ(d♭) ≤ 2^m; where d♭ = 3 and
  m ≥ 14 is even (196 times) d is 3^i with level i live and rank 1, and #bad(d)·16 ≤ 3·2^m; (iii) the number of bad
  signings is at most 2^m·`lhsN1 m T` < 2^m. 9,423 levels d ∈ D* in all; 0 violations.
- Each hypothesis can be supplied at its place of use: S1 and S2 are applied to d = p^i·d″ with i = v_p(d) ≥ 1 and
  p ∤ d″; S5 to the one d with d♭ = 3, where `rank e 3 i = 1` and `live` hold by the definition of D* and ♭, and
  `7 ≤ m` by 14 ≤ m; N1's `μ t + 1 ≤ m` is S3 for the prime that gives μ(d♭), its `1 ≤ m` is `Nonempty ι`.
- In Lean, in my copy (`A3_sem.lean`; all compile, with `sorryAx` only through the skeleton): S2 from S2 (a) and
  S2 (b); S3 from the occupied classes; the step of (i) (bad at d, level v_p(d) of p not live ⟹ bad at d/p) from S1;
  `exists_lift_two_all` from `exists_signs_odd` and the finished `exists_lift_two_aux`; `sizes_eq_two_all` from
  `exists_lift_two_all` (the proof of `sizes_eq_two`); the paper's wording of the lemma on lifts; the sizes for every
  s ≥ 1 from `sizes_eq_two_all` and `Lift.sizes_eq`.
- `exists_signs_odd` from A1 I checked on paper only (ι = Σ x, Fin (w x), e ⟨x, _⟩ = x.val; the signed mask is
  `maskW u - maskW v` with u, v the numbers of + and −): I see no gap.

## 4. Vacuity and strength

- **No hypothesis is contradictory.** Each of the fifteen is applied in Lean to data that satisfy its hypotheses
  (`A3_sem.lean`: a signing bad at 3; a bad signing at a level that is not live; a pivot set; a live level; seven
  elements with level 1 of 3 live and rank 1; m = 3, T = {3}; n = 105 and n = 1; N = 210, 8, 1; N = 315, 16).
- **No conclusion is trivially satisfiable.** "All +" fails for 30.7 million multisets and "all low" for 44.3 million;
  S0, S1, S2 were tested on thousands of instances that have bad signings, with equality in S2.
- `[Nonempty ι]`: needed in the occupied classes, S3 and A1 (each false for empty ι); not assumed elsewhere and not
  needed there. `hm` in N1: needed. `hm` in S5: as far as tested 4 ≤ m would do (2,039 random instances with m < 7
  and 60 with one occupied group and 3 ≤ m ≤ 6: the inequality fails only for m = 3). `hlive` in S1: needed. `hlive`
  in S2 (b), S2, S5 and `hrank` in S5: not needed for truth as far as tested (50,088 levels that are not live, 361 and
  1,040 instances for S5: no failure); harmless, A1 has them. `¬ p ∣ d`: needed in S0 and S1; for S2 I found no failure without it (7.9 million small instances). `hw`,
  `hP`: needed (the empty multiset; N = 1, P = {2}). `[NeZero n]`: implied by `hn`, needed for the type.
- **Excluded that the paper claims:** nothing in the three final statements themselves. Not contained in them: the
  fractions of Theorem 4, and "every s ≥ 1" (see the verdict).

## 5. Other things worth knowing before trusting "proved in Lean"

1. While I worked, `~/lean/signs-check-full.out`, `signs-all-axioms.out` and a sixteenth statement
   (`sizes_eq_mul_all`, `signs-briefs/brief-M.md`) appeared. I read them and used none of them. By that log the seven
   files are assembled, the fifteen print as in the skeleton and depend on the three standard axioms. That prover A
   could assemble A1 from the parts as stated is, by that account, Lean's own confirmation of §3.
2. `A4_dump.lean` prints a structural hash of each of the ten definitions (type and value) and fifteen statements as
   elaborated in the skeleton copy (`A4_dump.out`). Run in the finished project it should print the same lines. I
   did not run it there. `maskW` and `Lift.reduce` have the hashes of the earlier audit.
3. The Lean proof is not the paper's: no digit is deleted, the level d = 3 costs 3/16 (paper: 5/32) and N1 says only
   "< 1" (paper: "below 0.961"). The paper's paragraph should not let those numbers pass as formalised.
4. In `sizes_eq_two_all` the bound variable `P` hides the definition `Pnq.P`; the explicit print shows the finite set,
   as meant. `μ` is `Pnq.μ` everywhere.
5. Values by `#eval` rest on Lean's compiler, not the kernel; kernel checks are the 11 `decide` examples, `μ 3 = 2`
   and the reading lemmas.
6. The plan's steps I recomputed: the partial sums 1/4, …, 209/256; A(s) up to s = 40; "below 0.8518" for U = 19
   (0.851788) against 0.853027; halving step (2) needs u ≥ 20 as stated (it fails for u = 2, 6). In what I recomputed
   and read of the plan I found no error.

## 6. What I did not check

- The proofs, and anything in the provers' copies or the assembled project (beyond reading the log named above).
- `sizes_eq_mul_all` (the sixteenth statement).
- A1 → `exists_signs_odd` in Lean.
- Sizes beyond those listed: more than 6 elements on any modulus with three primes; even sizes ≥ 12 only for
  n ≤ 15; moduli above 3465 (signs), N above 2310 (lifts), above 1155 (sizes); the sets of sizes only up to S.
- The parts beyond m = 16 elements, primes above 13, moduli p^i·d above 343; S0 in ℤ[X]/(Φ_d), not with complex
  numbers. Tmax(m) by explicit enumeration beyond m = 34 (formula to 2000, a bound beyond).
- Theorem 4's fractions of good signings.
- Mathlib's `Polynomial.cyclotomic` is taken to be the cyclotomic polynomial (my own Φ_d agree with sympy for
  d ≤ 300 and multiply to X^n − 1 for n ≤ 120).

## 7. How the audit was run

- Every Python program through `~/bin/cap2g.sh` (with `-I`), every Lean job through `lean1.sh` in my copy (seven
  jobs, 5 to 15 seconds each); no program hit the 2 GB cap; no network; nothing posted; nothing is running now. No
  file under `Pnq/`, `Pqr/`, `P2q2/` of my copy is newer than the copy; no `lake build`, `update`, `clean`, `cache`.
- **Departures, all small.** (a) About five commands of a second or less (two text edits of my own scripts, the text
  comparison twice, one test run of `t1_parts.py`) ran while two of my computations were running, so for a moment
  there were three processes. (b) Shell tools for reading outputs (`tail`, `grep`, `awk`, `cp`, `sha256sum`) were run
  directly. (c) The searches were run as chains of many short runs (the two A1 chains took about 3 and 12 minutes in
  all); the longest single computations were the search without `hd` (`t1c_hd.py`, 4 minutes, pure Python, longer
  than I meant), the lifts for N = 105 with 6 elements (192 s) and N = 210 with 5 (139 s), and A1 for n = 105 with 6
  elements (128 s).
- The first runs of `t1_parts.py` (two batches) were repeated with the final program, which has more moduli and
  counters; the main A1 chain was run twice (the second time after a correction to the counter of signings tried,
  which does not affect a result); the outputs kept are the later ones.

## Files (all in `/home/agent3/lean/signs-audit/`)

Lean: `A1_print` (definitions and statements, default and explicit; axioms), `A2_eval` with `a2_gen.py`, `a2_cmp.py`,
`a2_expected.json` (values of `live`, `rank`, `μ`, `lhsN1`), `A0_checksigns.out` with `a0_checksigns.py`,
`A3_sem` (reading lemmas, instances, the steps that fit, the final statements from one another), `A4_dump`
(fingerprints, the old statements as instances, `decide` values); each `.lean` with its `.out`. Text:
`a5_textdiff.py/.out`, `skeleton_sha256.txt`. Tests: `core.py`, `t0_selftest`, `t1_parts` (five outputs, `run_t1.sh`),
`t1b_s5`, `t1c_hd`, `t2_n1`, `t3_a1` (`run_t3.sh`, `run_t3b.sh`; main, deep), `t4_lift` (`run_t4.sh`, `run_t4c.sh`;
main, deep), `t4b_sizes` (`run_t4b.sh`), `t5_fit` (three outputs). Totals: `summary.py/.out`.

# The sixteenth statement

Added later on 27 November 2026, at the coordinator's request; it replaces "I did not audit that one" in the verdict
and in §6 above. Audited: `Pnq.sizes_eq_mul_all` as fixed in `/home/agent3/lean/signs-skeleton/SignMul.as-fixed.lean`
(its sha256 equals the one recorded beside it). My scratch file `AuditA5Mul.lean` (top folder of my copy; copy here as
`A5_mul.lean`, output `A5_mul.out`) begins with that file byte for byte and elaborates it with its `sorry`; nothing
under `Pnq/` of my copy was added or changed. Numbers are from `summary_mul.out`.

## Verdict

- **It says what is meant, and I found nothing false, vacuous or weaker in it.** As Lean has it, it is
  `Lift.sizes_eq_odd` with the argument `Odd s` removed: the same expression, not only the same text. It is the paper's
  sentence as worded, in the strong reading (on Z_{Ns} the pattern is exact among all d > 1 dividing Ns).
- **It has no content beyond the fifteenth statement and a finished theorem:** it follows from `sizes_eq_two_all` and
  `Lift.sizes_eq` by induction on s (25 lines, compiled; the derived theorem has the same expression as its type). So
  it is true if those are.
- **No test disagrees:** 146 pairs (N, s), 121 of them with s even and not 2, complete census of both groups: 1,214
  sets P, the two sets of sizes equal for every one. And 160 pairs (N, s), 106,922,459 multisets on Z_N: every one has
  a lift to Z_{Ns} of the same size with no new cyclotomic divisor.

## 1. What it says

For every natural N ≠ 0 (implicit; `[NeZero N]`), every natural s ≠ 0 (explicit; `[NeZero s]`) and every finite set P
of natural numbers each of which divides N (`hP`): the set of t for which some `w' : ZMod (N * s) → ℕ` has
`∑ y, w' y = t`, `0 < t`, and for every natural d with d ∣ N·s and d ≠ 1, `cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P`, is
equal (as a set of natural numbers) to the set of t for which some `w : ZMod N → ℕ` has `∑ x, w x = t`, `0 < t`, and
for every d ∣ N with d ≠ 1, `cyclotomic d ℤ ∣ maskW w ↔ d ∈ P`.

- No subtraction and no division of natural numbers. The group is written `ZMod (N * s)`; its `NeZero (N * s)` is
  `instNeZeroNatHMul N s` (a proposition). d = 0 divides neither order (proved); d = 1 is skipped on both sides; d = N·s
  and d = N are included.
- **Against `Lift.sizes_eq_odd` as elaborated:** its fifth argument is `Odd s`, the rest does not mention it, and with
  it removed the type is the same expression as the type of `sizes_eq_mul_all` (same hash, same explicit print;
  checked by a small program in Lean, `A5_mul.out`). As text the two differ only by the name and `(hs : Odd s)`; with s
  replaced by 2 the text is that of `sizes_eq_two_all`. `Lift.sizes_eq_odd`, `sizes_eq_two_all` and `Lift.sizes_eq_mul`
  are instances of it (three `example`s, compiled). The hash of `sizes_eq_odd` is the one of the earlier audit.
- **Against the paper's sentence** ("the sizes of the nonempty multisets with exactly a given pattern P of divisors of
  N are the same on Z_N and on Z_{Ns} for every N and every s ≥ 1"): the same. "Nonempty" is `0 < t`; "sizes" are the
  numbers of elements `∑ w`; "the same" is equality of the two sets; N ≥ 1 and s ≥ 1 are the two `NeZero`. "Exactly
  the pattern P" on Z_{Ns} is taken among all d ≠ 1 dividing N·s, as in the wording of the Corollary; for P a set of
  divisors of N that is: exactly P among the divisors of N, and no Φ_d with d ∣ N·s, d ∤ N (proved, `pattern_iff`). P
  may contain 1, which changes nothing (proved, `erase_one`); the paper's patterns are sets of divisors > 1.
- Fingerprint as elaborated in my copy: type hash 437138964, explicit print 3022 characters.
- The fixed statement with its comment stands character for character, once, in `signs-M/Pnq/SignMul.lean` and in
  `signs-all/Pnq/SignMul.lean` as they were when I looked (50 lines, no line with `sorry`, `admit`, `axiom`,
  `native_decide`). I read nothing else there.

## 2. Is it true?

- **By derivation.** `AuditMul.derived` in `A5_mul.lean` proves the same statement from `sizes_eq_two_all` (for the
  factors 2 of s) and the finished `Lift.sizes_eq` (for the odd prime factors), with `AllAux.sizes_congr` for
  `N * (r * s') = N * s' * r`; it compiles, and its only non-standard axiom is the `sorry` of `sizes_eq_two_all` in my
  copy.
- **Census** (`t6_mul.py`; every multiset containing 0 up to size S on Z_N and on Z_{Ns}, exact divisibility): 146
  pairs, N in 1 … 10, 12, 15, 16, 18, 20, 21, 24, 25, 27, 30, 36, 45, 60, 105, 210 and s in 1, 2, 3, 4, 5, 6, 8, 9, 10,
  12, 16, 18, 24; 9,452,498 and 268,967,521 multisets; 1,214 sets P with a nonempty side, the two sets of sizes equal
  for every one (5,024 patterns on the larger groups contain a divisor that does not divide N and belong to no P).
  With s even and not 2: 121 pairs, 850 sets P; 57 of these pairs have N not of the form p^n q (438 sets P); 5 have
  N = 105 or 210 (33 sets P; S = 4 for (105, 4), 3 for (105, 6), (105, 8), (210, 4), 2 for (105, 12)). S is 12 down to
  7 for N ≤ 9 with s = 4, 5 for (30, 4) and (36, 4), 4 for (30; 6, 8, 12), 3 for N = 60.
- **Lifts** (`t6b_liftmul.py`; the fact behind the statement, at every size up to the bound and not only as sets of
  sizes): for every multiset on Z_N a multiset on Z_{Ns} of the same size that reduces to it and has no Φ_d with
  d ∣ N·s, d ∤ N; all s^(m−1) choices tried before giving up. 160 pairs, N up to 420, s in 2, 3, 4, 5, 6, 8, 9, 10,
  12, 16, 18, 24; 106,922,459 multisets, none without such a lift; "all low" fails for 5,951,045; at most 35 choices
  tried. With s even and not 2: 140 pairs, 98,025,663 multisets; 76 of these pairs with N not of the form p^n q
  (77,633,123 multisets); 24 with the odd part of N of three primes (N = 105, 210, 315, 330, 420; 21,022,824
  multisets; sizes up to 5 for N = 105 with s = 4, 6, 8, up to 4 for N = 105 with s = 10, 12 and N = 210 with
  s = 4, 6, up to 3 for the rest, 2 for (420, 12)); sizes up to 8 for N = 30 with s = 4, 6, 8.

## 3. Vacuity and strength

- **No hypothesis is contradictory:** applied in Lean to N = 105 with s = 12, N = 36 with s = 4, N = 1 with s = 8, any
  N with s = 1, N = 210 with s = 6 and P = ∅, N = 30 with s = 4 and P = {1, 2, 15}.
- **Not trivial:** in the census every one of the 1,214 sets P is nonempty on both sides, and "all low" fails for
  5,951,045 multisets.
- `[NeZero s]` and `[NeZero N]`: they say s ≥ 1 and N ≥ 1 and are needed for the statement to be written (the sums
  run over a finite group).
- `hP`: needed. N = 1, s = 2, P = {2}: sizes 2, 4, 6, … on Z_2 against every size on Z_1; N = 3, s = 4, P = {2};
  N = 15, s = 4, P = {2, 4} (`t6c_hp.out`). A member of P that divides neither N nor N·s would do no harm; `hP`
  excludes it too.
- P containing 1: allowed, no effect. P that is the pattern of no multiset: both sets empty.
- `0 < t`: needed. Without it, for N = 1, s = 2, P = ∅ the empty multiset would be on the right and not on the left.
- s = 1: allowed; the two groups are the same and the statement says nothing (true by rewriting `N * 1 = N`).
- Stronger than each audited statement on sizes (they are instances), and no stronger than `sizes_eq_two_all` with
  `Lift.sizes_eq` together.

## 4. Does it give the paper's sentence?

Yes, by itself: it is that sentence (§1), for every N ≥ 1, every s ≥ 1 and every set P of divisors of N, with the
pattern on Z_{Ns} exact among all divisors d > 1 of Ns. Nothing finished has to be added; equal sets of sizes give in
particular equal least sizes. The paper's next sentence ("only for odd s … is formalised") is then out of date.

## 5. What I did not check

- The proof in `signs-M` and the assembled project (I compared only the text of the statement there).
- The census beyond size S (12 down to 2; for N = 105 and 210 only 2 to 4), and the lifts beyond the sizes named; s
  above 24; N with three odd primes other than 105, 210 (census) and 105, 210, 315, 330, 420 (lifts); N above 420.
- Anything about `Lift.sizes_eq` and `sizes_eq_two_all` beyond the earlier audits.

## 6. How this part was run

Two Lean jobs through `lean1.sh` (6 seconds each), every Python program through `cap2g.sh`; two chains of short runs
side by side (309 s and 207 s in all; the longest single run 34 s), never more than two processes; shell tools for
reading outputs run directly. No network, nothing posted, nothing running now.

Files added in `/home/agent3/lean/signs-audit/`: `A5_mul.lean/.out`, `a6_textdiff_mul.py/.out`, `t6_mul.py`
(`run_t6.sh`, `t6_mul_main.out`), `t6b_liftmul.py` (`run_t6b.sh`, `t6b_liftmul_main.out`), `t6c_hp.py/.out`,
`summary_mul.py/.out`.
