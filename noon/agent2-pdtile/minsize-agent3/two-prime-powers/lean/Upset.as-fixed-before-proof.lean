/-
Two prime powers: the patterns that are up-sets.  For `M = p^n * q^m` and an up-set `D` of the divisors of `M`,
a multiset on `ZMod M` whose mask polynomial is divisible by `Φ_d` for every `d ∈ D` is a sum of functions
periodic under the subgroups `c · ZMod M`, `c` a corner of `D` (a maximal divisor of `M` not in `D`); and the
least size of a multiset whose cyclotomic divisors are exactly `D` is the sum of `M / c` over the corners.
(Definitions and statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.
The proof on paper is a fresh instance's, on top of Proposition 6.3 of Kiss, Łaba, Marshall and Somlai.)
-/
import Pnq.Weighted

open Finset

namespace Pnq

namespace Upset

/-- `D` is an up-set of the divisors of `M` that does not contain `1`: every element of `D` is a divisor of `M`
other than `1`, and with `d` it contains every multiple of `d` that divides `M`. -/
def IsUpSet (M : ℕ) (D : Finset ℕ) : Prop :=
  (∀ d ∈ D, d ∣ M ∧ d ≠ 1) ∧ ∀ d ∈ D, ∀ e, d ∣ e → e ∣ M → e ∈ D

/-- the corners of `D`: the maximal divisors of `M` that are not in `D` (maximal for divisibility) -/
def corners (M : ℕ) (D : Finset ℕ) : Finset ℕ :=
  (M.divisors \ D).filter (fun c => ∀ e ∈ M.divisors \ D, c ∣ e → e = c)

variable {p q n m : ℕ} [Fact p.Prime] [Fact q.Prime]

instance instNeZeroPowMulPow : NeZero (p ^ n * q ^ m) :=
  ⟨Nat.mul_ne_zero (pow_ne_zero _ (Fact.out : p.Prime).ne_zero) (pow_ne_zero _ (Fact.out : q.Prime).ne_zero)⟩

/-- **The structure theorem.** For an up-set `D`, the mask polynomial of `w` is divisible by `Φ_d` for every
`d ∈ D` if and only if `w` is a sum, over the corners `c` of `D`, of functions `g c` with values in `ℕ` that are
periodic under adding `c` (that is, constant on the cosets of the subgroup `c · ZMod M`, so each `g c` is a sum
of such cosets). -/
theorem structure_iff (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D)
    (w : ZMod (p ^ n * q ^ m) → ℕ) :
    (∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW w) ↔
      ∃ g : ℕ → ZMod (p ^ n * q ^ m) → ℕ,
        (∀ c ∈ corners (p ^ n * q ^ m) D, ∀ x, g c (x + (c : ZMod (p ^ n * q ^ m))) = g c x) ∧
        ∀ a, w a = ∑ c ∈ corners (p ^ n * q ^ m) D, g c a := by
  sorry

/-- **The lower bound.** If the mask polynomial of `w` is divisible by `Φ_d` for every `d` of the up-set `D` and
by `Φ_c` for no corner `c` of `D`, then `w` has at least `∑ M / c` elements, the sum over the corners. -/
theorem lower_bound (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D)
    (w : ZMod (p ^ n * q ^ m) → ℕ) (hdiv : ∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW w)
    (hcor : ∀ c ∈ corners (p ^ n * q ^ m) D, ¬ Polynomial.cyclotomic c ℤ ∣ maskW w) :
    ∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c ≤ ∑ a, w a := by
  sorry

/-- **Least size for an up-set pattern.** Among the multisets on `ZMod (p^n * q^m)` that are not empty and whose
mask polynomial is divisible by `Φ_d`, for `d ∣ p^n q^m`, `d ≠ 1`, exactly when `d ∈ D`, the least number of
elements is the sum of `M / c` over the corners of `D`. -/
theorem least_size (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q ^ m) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
        ∀ d, d ∣ p ^ n * q ^ m → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)}
      (∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c) := by
  sorry

end Upset

end Pnq
