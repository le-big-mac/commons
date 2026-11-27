/-
The statement on signs for every `n`: part T, "the levels of the prime 2 together cost at most twice level 0".
Pure combinatorics, no polynomials.  `ι` a finite type, each `k : ι` with a position `pos k : ℕ` and a value `val k`
in an additive commutative group `V` (any group, any values, `0` allowed); a signing is `ε : ι → Bool`.
`csum pos val ε M r` is the signed sum of the values over the class `r` modulo `M`.  Level `0` is bad if the signed
sum of all values is `0`; level `j + 1` is bad if for every `r < 2^j` the two classes `r` and `r + 2^j` modulo
`2^(j+1)` (the two halves of the class `r` modulo `2^j`) have equal signed sums.
(Theorem T′ of the proof on paper; statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignDefs

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι] {V : Type*} [AddCommGroup V]

/-- the signed sum `∑ sg (ε k) • val k` over the elements `k` whose position lies in the class `r` modulo `M`
(that is, `pos k % M = r`) -/
def csum (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (M r : ℕ) : V :=
  ∑ k, if pos k % M = r then sg (ε k) • val k else 0

/-- level `j` is bad for the signing `ε`.  Level `0`: the signed sum of all the values is `0`.  Level `j + 1`: for
every `r < 2^j`, the classes `r` and `r + 2^j` modulo `2^(j+1)` have the same signed sum. -/
def levelBad (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) : ℕ → Prop
  | 0 => ∑ k, sg (ε k) • val k = 0
  | j + 1 => ∀ r, r < 2 ^ j →
      csum pos val ε (2 ^ (j + 1)) r = csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j)

/-- `levelBad` at level `0` (unfolding) -/
theorem levelBad_zero (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) :
    levelBad pos val ε 0 ↔ ∑ k, sg (ε k) • val k = 0 :=
  Iff.rfl

/-- `levelBad` at level `j + 1` (unfolding) -/
theorem levelBad_succ (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (j : ℕ) :
    levelBad pos val ε (j + 1) ↔ ∀ r, r < 2 ^ j →
      csum pos val ε (2 ^ (j + 1)) r = csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j) :=
  Iff.rfl

open Classical in
/-- **T (twice level 0).**  For every `K`, the number of signings for which some level `j ≤ K` is bad is at most
twice the number of signings for which level `0` is bad. -/
theorem card_exists_levelBad_le (pos : ι → ℕ) (val : ι → V) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ levelBad pos val ε j).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => levelBad pos val ε 0).card := by
  sorry

end Pnq
