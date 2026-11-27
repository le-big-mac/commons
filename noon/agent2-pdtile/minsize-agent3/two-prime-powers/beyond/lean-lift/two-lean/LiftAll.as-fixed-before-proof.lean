/-
The least-size theorem for `Z_{pⁿq}` on every larger group `Z_{pⁿq·s}`, `s ≥ 1`: among the multisets on `ZMod (p^n * q * s)` whose
cyclotomic divisors are a given pattern of divisors of `p^n * q` and no others, the least number of elements is the one the theorem
gives on `ZMod (p^n * q)`.  Also, for any `N` and odd `s`: the sizes of the multisets with exactly a given pattern of divisors of
`N` are the same on `ZMod N` and on `ZMod (N * s)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  On paper: lift along the factors 2 of `s`
first, by the lemma on signs, then along its odd prime factors.)
-/
import Pnq.MinGroup
import Pnq.Lift
import Pnq.LiftMin
import Pnq.Lift2

open Finset

namespace Pnq

namespace Lift

/-- **Sizes are the same on `ZMod (N * s)`, `s` odd, any `N`.** -/
theorem sizes_eq_odd {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (hs : Odd s) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  sorry

section All

variable (p q n s : ℕ) [Fact p.Prime] [Fact q.Prime] [NeZero s]

/-- **Sizes are the same on `ZMod (p^n * q * s)`, every `s ≥ 1`.** -/
theorem sizes_eq_mul (hpq : p ≠ q) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ p ^ n * q) :
    {t | ∃ w' : ZMod (p ^ n * q * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  sorry

/-- **Unbalanced patterns on `ZMod (p^n * q * s)`.** -/
theorem minsize_unbalanced_mul (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {t | ∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minU p q Es Fs) := by
  sorry

/-- **Balanced patterns with every `Φ_{p^ℓ q}`, on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_all_mul (hpq : p ≠ q)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {t | ∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t ∧ 0 < t ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (q * p ^ Es.card) := by
  sorry

/-- **Balanced patterns with a first level `a0` at which `Φ_{p^a0 q} ∤ A(X)`, on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_mul (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {t | ∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minB p q Es Fs a0) := by
  sorry

end All

end Lift

end Pnq
