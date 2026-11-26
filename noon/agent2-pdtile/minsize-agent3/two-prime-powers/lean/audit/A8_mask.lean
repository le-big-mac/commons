import Pnq.Upset
/-!
Audit file 8: what `maskW` and `Polynomial.cyclotomic` are, so that the translation into a program is pinned down.
-/
open Finset Pnq

namespace Audit

/-- the coefficient of `X^k` in the mask of `w` is `w (k mod M)` for `k < M` and `0` for `k ≥ M` -/
theorem coeff_maskW {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (k : ℕ) :
    (maskW w).coeff k = if k < M then (w (k : ZMod M) : ℤ) else 0 := by
  rw [maskW, Polynomial.finsetSum_coeff]
  simp only [Polynomial.coeff_C_mul, Polynomial.coeff_X_pow]
  split_ifs with hk
  · rw [Finset.sum_eq_single (k : ZMod M)]
    · simp [ZMod.val_natCast, Nat.mod_eq_of_lt hk]
    · intro b _ hb
      have : k ≠ b.val := fun h => hb (by rw [h, ZMod.natCast_zmod_val])
      simp [this]
    · simp
  · apply Finset.sum_eq_zero
    intro a _
    have : k ≠ a.val := fun h => hk (h ▸ ZMod.val_lt a)
    simp [this]

/-- the mask evaluated at `1` is the number of elements -/
theorem eval_one_maskW {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    (maskW w).eval 1 = ((∑ a, w a : ℕ) : ℤ) := by
  rw [maskW, Polynomial.eval_finsetSum]
  simp

/-- the mask is `0` only for the empty multiset -/
theorem maskW_eq_zero_iff {M : ℕ} [NeZero M] (w : ZMod M → ℕ) : maskW w = 0 ↔ ∀ a, w a = 0 := by
  constructor
  · intro h a
    have h1 := coeff_maskW w a.val
    rw [h, Polynomial.coeff_zero, if_pos (ZMod.val_lt a), ZMod.natCast_zmod_val] at h1
    exact_mod_cast h1.symm
  · intro h
    ext k
    rw [coeff_maskW, Polynomial.coeff_zero]
    split_ifs <;> simp [h]

end Audit

-- Mathlib's cyclotomic polynomials: the facts that characterise them
#check @Polynomial.prod_cyclotomic_eq_X_pow_sub_one   -- ∏ over the divisors of n of Φ_i = X^n - 1
#check @Polynomial.cyclotomic_zero                    -- Φ_0 = 1 (never reached: d ∣ M and M ≠ 0)
#check @Polynomial.cyclotomic_one                     -- Φ_1 = X - 1
#check @Polynomial.cyclotomic_two                     -- Φ_2 = X + 1
#check @Polynomial.cyclotomic.monic
#check @Polynomial.cyclotomic.irreducible
#check @Polynomial.natDegree_cyclotomic
#check @ZMod.val_lt
#check @ZMod.natCast_self
#check @ZMod.val_natCast
#print axioms Audit.coeff_maskW
