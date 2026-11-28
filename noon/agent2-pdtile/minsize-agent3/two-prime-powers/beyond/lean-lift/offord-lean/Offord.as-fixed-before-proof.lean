/-
Erdős's bound for the problem of Littlewood and Offord, for nonzero real numbers and for nonzero complex numbers:
a signed sum `∑ ± a i` of `m` nonzero numbers takes any one value for at most `C(m, ⌊m/2⌋)` of the `2^m` choices of
signs.  (Statements fixed on 28 November 2026, before any Lean proof of them.  A signing is `ε : ι → Bool`, `true`
is `+`; `sg` is from `Pnq/SignDefs.lean`.)
-/
import Mathlib
import Pnq.SignDefs

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

open Classical in
/-- **Erdős's bound, real numbers.**  For nonzero real numbers `a i` and any real `v`, the signings `ε` with
`∑ i, sg (ε i) * a i = v` number at most `C(m, ⌊m/2⌋)`, where `m` is the number of the `a i`. -/
theorem card_signedSum_eq_le_real (a : ι → ℝ) (ha : ∀ i, a i ≠ 0) (v : ℝ) :
    (Finset.univ.filter fun ε : ι → Bool => ∑ i, (sg (ε i) : ℝ) * a i = v).card ≤
      (Fintype.card ι).choose (Fintype.card ι / 2) := by
  sorry

open Classical in
/-- **The same bound for nonzero complex numbers.** -/
theorem card_signedSum_eq_le_complex (a : ι → ℂ) (ha : ∀ i, a i ≠ 0) (v : ℂ) :
    (Finset.univ.filter fun ε : ι → Bool => ∑ i, (sg (ε i) : ℂ) * a i = v).card ≤
      (Fintype.card ι).choose (Fintype.card ι / 2) := by
  sorry

end Pnq
