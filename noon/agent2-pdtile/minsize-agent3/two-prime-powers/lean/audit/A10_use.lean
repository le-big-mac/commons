import Pnq.Upset
/-!
Audit file 10: the theorems applied to a group written as `ZMod 12`, `ZMod 8`, `ZMod 1` (not as
`ZMod (p ^ n * q ^ m)`): the numerals are equal by evaluation, so the statements can be used as they stand.
-/
open Pnq Pnq.Upset

example (D : Finset ℕ) (hD : IsUpSet 12 D) (w : ZMod 12 → ℕ) :
    (∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW (M := 2 ^ 2 * 3 ^ 1) w) ↔
      ∃ g : ℕ → ZMod 12 → ℕ,
        (∀ c ∈ corners 12 D, ∀ x, g c (x + (c : ZMod 12)) = g c x) ∧ ∀ a, w a = ∑ c ∈ corners 12 D, g c a :=
  structure_iff (p := 2) (q := 3) (n := 2) (m := 1) (by norm_num) D hD w

-- a prime power: 8 = 2^3 * 3^0
example (D : Finset ℕ) (hD : IsUpSet 8 D) (w : ZMod 8 → ℕ)
    (hdiv : ∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW (M := 2 ^ 3 * 3 ^ 0) w)
    (hcor : ∀ c ∈ corners 8 D, ¬ Polynomial.cyclotomic c ℤ ∣ maskW (M := 2 ^ 3 * 3 ^ 0) w) :
    ∑ c ∈ corners 8 D, 8 / c ≤ ∑ a : ZMod (2 ^ 3 * 3 ^ 0), w a :=
  lower_bound (p := 2) (q := 3) (n := 3) (m := 0) (by norm_num) D hD w hdiv hcor

-- the trivial group: 1 = 2^0 * 3^0
example (D : Finset ℕ) (hD : IsUpSet 1 D) :=
  least_size (p := 2) (q := 3) (n := 0) (m := 0) (by norm_num) D hD
