/-
The least-size theorem for `Z_{pⁿq}` on the larger group `Z_{pⁿq·r}`, `r` an odd prime (`r` may be `p` or `q`): among the
multisets on `ZMod (p^n * q * r)` whose cyclotomic divisors are a given pattern of divisors of `p^n * q` and no others, the
least number of elements is the one the theorem gives on `ZMod (p^n * q)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.)
-/
import Pnq.MinGroup
import Pnq.Lift

open Finset

namespace Pnq

namespace Lift

/-- **Unbalanced patterns, lifted.**  `r` an odd prime.  Among the multisets on `ZMod (p^n * q * r)` with `Φ_q ∤ A(X)`,
with `Φ_{p^ℓ} ∣ A(X)` exactly for the levels `ℓ ∈ Es`, with `Φ_{p^ℓ q} ∣ A(X)` exactly for the levels `ℓ ∈ Fs`, and with
no `Φ_d ∣ A(X)` for a divisor `d` of `p^n q r` that does not divide `p^n q`, the least size is `minU p q Es Fs`. -/
theorem minsize_unbalanced_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minU p q Es Fs) := by
  sorry

/-- **Balanced patterns with every `Φ_{p^ℓ q}`, lifted.** -/
theorem minsize_balanced_all_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ 0 < s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (q * p ^ Es.card) := by
  sorry

/-- **Balanced patterns with a first level `a0` at which `Φ_{p^a0 q} ∤ A(X)`, lifted.** -/
theorem minsize_balanced_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minB p q Es Fs a0) := by
  sorry

end Lift

end Pnq
