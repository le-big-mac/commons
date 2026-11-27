/-
The statement on signs for every `n`, with its exceptional pairs: the final statements.  A nonempty multiset `w` on
`ZMod n` that is not an exceptional pair can be split into two parts `u`, `v` so that no `Φ_d`, `d ∣ n`, divides
`maskW u - maskW v`; an exceptional pair cannot.  The first from B (`exists_not_badAt_of_three_le` of
`Pnq/EvenAll.lean`) for three or more elements, as `exists_signs_odd` of `Pnq/SignFinal.lean` was drawn from
`exists_not_badAt`, and by hand for one and two elements.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenAll
import Pnq.SignFinal

open Finset

namespace Pnq

/-- an exceptional pair: two marks whose difference has even additive order -/
def ExceptionalPair {n : ℕ} (w : ZMod n → ℕ) : Prop :=
  ∃ a b : ZMod n, w = Pi.single a 1 + Pi.single b 1 ∧ Even (addOrderOf (a - b))

/-- **The statement on signs for every `n`** (the first final statement of the plan).  The elements of a nonempty
multiset `w` on `ZMod n` that is not an exceptional pair can be split into two parts `u`, `v` so that no `Φ_d`,
`d ∣ n`, divides `maskW u - maskW v`. -/
theorem exists_signs_all (n : ℕ) [NeZero n] (w : ZMod n → ℕ) (hw : ∃ x, w x ≠ 0)
    (hpair : ¬ ExceptionalPair w) :
    ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  sorry

/-- **The exceptional pairs are exceptions** (the second final statement of the plan).  For an exceptional pair `w`,
every splitting `u + v = w` has `maskW u - maskW v` divisible by `Φ_d` for some `d ∣ n`. -/
theorem not_exists_signs_of_exceptionalPair (n : ℕ) [NeZero n] (w : ZMod n → ℕ) (hpair : ExceptionalPair w) :
    ¬ ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  sorry

end Pnq
