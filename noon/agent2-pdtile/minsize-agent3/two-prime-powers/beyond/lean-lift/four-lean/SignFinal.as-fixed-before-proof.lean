/-
The statement on signs for every odd `n`, and the lifting along the prime 2 for every `N`: the final statements.
The statement on signs for multisets on `ZMod n`, `n` odd (`Lift.exists_signs` of `Pnq/Sign.lean` with `p^a * q^b`
replaced by an odd `n`), the lemma on lifts for the prime 2 for every `N`, and the equality of the sets of sizes on
`ZMod (N * 2)` and on `ZMod N`.  All three from A1 (`exists_not_badAt` of `Pnq/SignAll.lean`).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignAll
import Pnq.Lift2

open Finset

namespace Pnq

/-- **The statement on signs for every odd `n`** (the first final statement of the plan).  The elements of a nonempty
multiset `w` on `ZMod n`, `n` odd, can be split into two parts `u`, `v` so that no `Φ_d`, `d ∣ n`, divides
`maskW u - maskW v`. -/
theorem exists_signs_odd (n : ℕ) [NeZero n] (hn : ¬ 2 ∣ n) (w : ZMod n → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  sorry

/-- **The lemma on lifts for the prime 2, for every `N`** (the second final statement of the plan).  A nonempty
multiset `w` on `ZMod N` is the reduction of a multiset `w'` on `ZMod (N * 2)` whose mask is divisible by no `Φ_d`
with `d ∣ N * 2`, `d ∤ N`. -/
theorem exists_lift_two_all {N : ℕ} [NeZero N] (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, Lift.reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  sorry

/-- **Sizes are the same, for the prime 2, for every `N`** (`Lift.sizes_eq_two` of `Pnq/Lift2.lean` without its
hypotheses on the odd part of `N`).  For a set `P` of divisors of `N`, the sizes of the nonempty multisets on
`ZMod (N * 2)` whose mask is divisible by `Φ_d`, `d ∣ N * 2`, `d ≠ 1`, exactly for `d ∈ P` are the sizes of the
nonempty multisets on `ZMod N` whose mask is divisible by `Φ_d`, `d ∣ N`, `d ≠ 1`, exactly for `d ∈ P`. -/
theorem sizes_eq_two_all {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * 2 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  sorry

end Pnq
