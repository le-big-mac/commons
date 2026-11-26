/-
The least size of a multiset on `ZMod (p^n * q)` whose mask polynomial is divisible by exactly a given set of
the cyclotomic polynomials `Φ_d`, `d ∣ p^n q`, `d > 1`.
(Definitions and statements fixed by agent3 / Yonder, 26 November 2026.)

The divisors `d > 1` of `p^n q` are `p^ℓ` (`1 ≤ ℓ ≤ n`), `q`, and `p^ℓ q` (`1 ≤ ℓ ≤ n`).  A pattern is: the set
`Es` of levels `ℓ` with `Φ_{p^ℓ} ∣ A(X)`, the set `Fs` of levels `ℓ ≥ 1` with `Φ_{p^ℓ q} ∣ A(X)`, and whether
`Φ_q ∣ A(X)`.  The three theorems below cover every pattern.
-/
import Pnq.MinTree
import Pnq.Weighted

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ} ∣ A(X)` -/
noncomputable def levelsEW (w : ZMod (p ^ n * q) → ℕ) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w)

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ q} ∣ A(X)` -/
noncomputable def levelsFW (w : ZMod (p ^ n * q) → ℕ) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w)

/-- **Least size, `Φ_q ∤ A(X)`.** Among the multisets on `Z_{p^n q}` whose mask polynomial is not divisible
by `Φ_q`, is divisible by `Φ_{p^ℓ}` exactly for `ℓ ∈ Es` and by `Φ_{p^ℓ q}` (`ℓ ≥ 1`) exactly for `ℓ ∈ Fs`,
the least number of elements is `p^|Es|` if `Fs ⊆ Es`, and `p^|Es| (p^|Fs \ Es| + q)` otherwise. -/
theorem minsize_unbalanced_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Fs}
      (minU p q Es Fs) := by
  sorry

/-- **Least size, `Φ_q ∣ A(X)` and `Φ_{p^ℓ q} ∣ A(X)` for every `ℓ`.** Among the multisets that are not
empty, the least number of elements is `q p^|Es|`. -/
theorem minsize_balanced_all_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ 0 < s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Finset.Icc 1 n}
      (q * p ^ Es.card) := by
  sorry

/-- **Least size, `Φ_q ∣ A(X)`, and `a0` the first level in `1..n` with `Φ_{p^a0 q} ∤ A(X)`.** The least number
of elements is `q p^|Es| (p^k' + x)`, where `k'` is the number of levels beyond `a0` that are in `Fs` and not
in `Es`, and `x` is `0` or `1` by the four clauses of `xOf`. -/
theorem minsize_balanced_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Fs}
      (minB p q Es Fs a0) := by
  sorry

end Pnq
