/-
The lifting for every `N` and every `s`: the sets of sizes on `ZMod (N * s)` and on `ZMod N` are the same.
`Lift.sizes_eq_odd` of `Pnq/LiftAll.lean` without its hypothesis that `s` is odd; from it and `sizes_eq_two_all` of
`Pnq/SignFinal.lean`.
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignFinal
import Pnq.LiftAll

open Finset

namespace Pnq

/-- **Sizes are the same on `ZMod (N * s)`, every `N`, every `s ≥ 1`.**  For a set `P` of divisors of `N`, the sizes of
the nonempty multisets on `ZMod (N * s)` whose mask is divisible by `Φ_d`, `d ∣ N * s`, `d ≠ 1`, exactly for `d ∈ P` are
the sizes of the nonempty multisets on `ZMod N` whose mask is divisible by `Φ_d`, `d ∣ N`, `d ≠ 1`, exactly for
`d ∈ P`. -/
theorem sizes_eq_mul_all {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  sorry

end Pnq
