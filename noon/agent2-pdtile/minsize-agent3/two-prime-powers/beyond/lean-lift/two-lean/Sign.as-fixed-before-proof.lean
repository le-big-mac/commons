/-
The lemma on signs.  For odd primes `p ≠ q`, the elements of a nonempty multiset on `ZMod (p^a * q^b)` can be given signs `+`, `-`
so that the signed mask polynomial is divisible by no cyclotomic polynomial `Φ_d` with `d ∣ p^a * q^b` (`d = 1` included).
A signing is given as a splitting `w = u + v` into the elements signed `+` and those signed `-`; the signed mask is
`maskW u - maskW v`.
(Statement fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of it.  The lemma and its proof on paper are due to
a fresh instance to which I had put the statement as a question.)
-/
import Pnq.Weighted

open Finset

namespace Pnq

namespace Lift

/-- **The lemma on signs.** -/
theorem exists_signs (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q) (a b : ℕ)
    (w : ZMod (p ^ a * q ^ b) → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ u v : ZMod (p ^ a * q ^ b) → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ p ^ a * q ^ b → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  sorry

end Lift

end Pnq
