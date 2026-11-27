/-
Lifting along the prime 2.  If `N = 2^k * (p^a * q^b)` with odd primes `p ≠ q`, a nonempty multiset on `ZMod N` can be lifted to
`ZMod (N * 2)` with the same number of elements and exactly the same cyclotomic divisors of its mask polynomial.  So the sizes of
the multisets with exactly a given pattern of divisors of `N` are the same on `ZMod N` and on `ZMod (N * 2)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  On paper: the lift is read off from a
signing, by the lemma on signs, of the elements in one class modulo `2^k`.)
-/
import Pnq.Lift
import Pnq.Sign

open Finset

namespace Pnq

namespace Lift

/-- **The lemma on lifts for the prime 2**, for `N` whose odd part is `p^a * q^b`. -/
theorem exists_lift_two {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q)
    (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b)) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  sorry

/-- **Sizes are the same, for the prime 2.** -/
theorem sizes_eq_two {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q)
    (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b)) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * 2 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  sorry

end Lift

end Pnq
