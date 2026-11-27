/-
Lifting to a set.  For an odd prime `r`, a nonempty multiset on `ZMod N` whose multiplicities are at most `r^j` and not all equal to
`r^j` is the reduction modulo `N` of a SET on `ZMod (N * r^j)` whose mask polynomial has exactly the same cyclotomic divisors: for
`d ∣ N * r^j`, `Φ_d` divides the mask of the set exactly when `d ∣ N` and `Φ_d` divides the mask of the multiset.
(Statement fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of it.  On paper: the copies of each element are spread
over its lifts, one prime step at a time, and the count of roots of the lemma on lifts shows that no new divisor comes in.)
-/
import Pnq.Lift

open Finset

namespace Pnq

namespace Lift

/-- **Lifting to a set.** -/
theorem exists_set_lift {N r : ℕ} [NeZero N] [Fact r.Prime] (hr : r ≠ 2) (j : ℕ)
    (w : ZMod N → ℕ) (hle : ∀ x, w x ≤ r ^ j) (hne : ∃ x, w x ≠ 0 ∧ w x ≠ r ^ j) :
    ∃ A : Finset (ZMod (N * r ^ j)),
      (∀ x : ZMod N,
        (A.filter (fun y => ZMod.castHom (Nat.dvd_mul_right N (r ^ j)) (ZMod N) y = x)).card = w x) ∧
      ∀ d, d ∣ N * r ^ j →
        (Polynomial.cyclotomic d ℤ ∣ maskW (indW A) ↔ d ∣ N ∧ Polynomial.cyclotomic d ℤ ∣ maskW w) := by
  sorry

end Lift

end Pnq
