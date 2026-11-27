/-
Sets on larger groups.  If `s` is divisible by `r^j`, `r` an odd prime, then for every size `t < r^j` a SET of `t` elements on
`ZMod (p^n * q * s)` with exactly a given pattern of divisors of `p^n * q` exists exactly when a multiset of `t` elements with that
pattern exists on `ZMod (p^n * q)`.  So when the least size that the theorem gives is below `r^j`, it is also the least size of a set
on `ZMod (p^n * q * s)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  On paper: lift a multiset along the factors
2 of `s`, then along `r^j` to a set, then along the other odd prime factors; a lift of a set is a set.)
-/
import Pnq.LiftAll
import Pnq.SetLift

open Finset

namespace Pnq

namespace Lift

section Sets

variable (p q n s r j : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] [NeZero s]

/-- **Sizes below `r^j`: sets on `ZMod (p^n * q * s)` against multisets on `ZMod (p^n * q)`.** -/
theorem set_sizes_iff_mul (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ p ^ n * q)
    (t : ℕ) (ht : t < r ^ j) :
    (∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW (indW A) ↔ d ∈ P)) ↔
    (∃ w : ZMod (p ^ n * q) → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)) := by
  sorry

/-- **Unbalanced patterns, sets on `ZMod (p^n * q * s)`.** -/
theorem minsize_unbalanced_set (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (hm : minU p q Es Fs < r ^ j) :
    IsLeast {t | ∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW (indW A) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW (indW A)}
      (minU p q Es Fs) := by
  sorry

/-- **Balanced patterns with every `Φ_{p^ℓ q}`, sets on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_all_set (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hm : q * p ^ Es.card < r ^ j) :
    IsLeast {t | ∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ 0 < t ∧ Polynomial.cyclotomic q ℤ ∣ maskW (indW A) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW (indW A)) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW (indW A)}
      (q * p ^ Es.card) := by
  sorry

/-- **Balanced patterns with a first level `a0` at which `Φ_{p^a0 q} ∤ A(X)`, sets on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_set (hpq : p ≠ q) (hr : r ≠ 2) (hs : r ^ j ∣ s)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) (hm : minB p q Es Fs a0 < r ^ j) :
    IsLeast {t | ∃ A : Finset (ZMod (p ^ n * q * s)), A.card = t ∧ Polynomial.cyclotomic q ℤ ∣ maskW (indW A) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW (indW A) ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW (indW A)}
      (minB p q Es Fs a0) := by
  sorry

end Sets

end Lift

end Pnq
