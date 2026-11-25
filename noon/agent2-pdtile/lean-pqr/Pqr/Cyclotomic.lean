/-
`ZeroAt A d` is the classical condition "the cyclotomic polynomial `Φ_d` divides the mask polynomial of `A`".
-/
import Pqr.SCBounds

open Finset Polynomial

namespace Pqr

variable {M : ℕ} [NeZero M]

/-- the mask polynomial `A(X) = ∑_{a ∈ A} X^a` of a set of residues, with exponents in `[0, M)` -/
noncomputable def mask (A : Finset (ZMod M)) : ℤ[X] := ∑ a ∈ A, X ^ a.val

/-- The Fourier coefficient of `A` at `ξ` is the value of the mask polynomial at `ψ ξ`. -/
theorem hat_eq_aeval_mask (A : Finset (ZMod M)) (ξ : ZMod M) :
    hat A ξ = aeval (ZMod.stdAddChar ξ : ℂ) (mask A) := by
  rw [hat, mask, map_sum]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [map_pow, aeval_X, ← AddChar.map_nsmul_eq_pow, nsmul_eq_mul, ZMod.natCast_zmod_val, mul_comm]

/-- `ψ 1 = exp (2πi / M)` is a primitive `M`-th root of unity. -/
theorem isPrimitiveRoot_stdAddChar_one :
    IsPrimitiveRoot (ZMod.stdAddChar (1 : ZMod M) : ℂ) M := by
  have h := Complex.isPrimitiveRoot_exp M (NeZero.ne M)
  have h1 : (ZMod.stdAddChar (1 : ZMod M) : ℂ) = Complex.exp (2 * Real.pi * Complex.I / M) := by
    have h2 := ZMod.stdAddChar_coe (N := M) 1
    simpa using h2
  rwa [h1]

/-- For `d ∣ M`, `ψ (M / d)` is a primitive `d`-th root of unity. -/
theorem isPrimitiveRoot_stdAddChar_div {d : ℕ} (hd : d ∣ M) :
    IsPrimitiveRoot (ZMod.stdAddChar ((M / d : ℕ) : ZMod M) : ℂ) d := by
  have hM : M ≠ 0 := NeZero.ne M
  have hMd : M / d ≠ 0 := by
    intro h0
    have h1 := Nat.div_mul_cancel hd
    rw [h0, zero_mul] at h1
    exact hM h1.symm
  have h2 := (isPrimitiveRoot_stdAddChar_one (M := M)).pow_of_dvd hMd (Nat.div_dvd_of_dvd hd)
  rw [Nat.div_div_self hd hM, ← AddChar.map_nsmul_eq_pow, nsmul_eq_mul, mul_one] at h2
  exact h2

/-- the element `M / d` of `ZMod M` has order `d` when `d ∣ M` -/
theorem ord_natCast_div' {d : ℕ} (hd : d ∣ M) : ord ((M / d : ℕ) : ZMod M) = d := by
  have hM : M ≠ 0 := NeZero.ne M
  rw [ord, ZMod.val_natCast, ← Nat.gcd_rec, Nat.gcd_eq_right (Nat.div_dvd_of_dvd hd),
    Nat.div_div_self hd hM]

/-- For `d ∣ M`: the indicator of `A` has no Fourier mass at the frequencies of order `d` iff `Φ_d` divides the
mask polynomial of `A`. -/
theorem zeroAt_iff_cyclotomic_dvd (A : Finset (ZMod M)) (d : ℕ) (hd : d ∣ M) :
    ZeroAt A d ↔ cyclotomic d ℤ ∣ mask A := by
  have hM : M ≠ 0 := NeZero.ne M
  have hdpos : 0 < d := Nat.pos_of_dvd_of_pos hd (Nat.pos_of_ne_zero hM)
  have hprim := isPrimitiveRoot_stdAddChar_div (M := M) hd
  have hord := ord_natCast_div' (M := M) hd
  have hcyc := cyclotomic_eq_minpoly hprim hdpos
  have hint : IsIntegral ℤ (ZMod.stdAddChar ((M / d : ℕ) : ZMod M) : ℂ) := hprim.isIntegral hdpos
  rw [hcyc]
  constructor
  · intro h
    have h0 := h _ hord
    rw [hat_eq_aeval_mask] at h0
    exact minpoly.isIntegrallyClosed_dvd hint h0
  · rintro ⟨Q, hQ⟩
    have h0 : hat A ((M / d : ℕ) : ZMod M) = 0 := by
      rw [hat_eq_aeval_mask, hQ, map_mul, minpoly.aeval, zero_mul]
    have h1 := zeroAt_of_hat_eq_zero A _ h0
    rwa [hord] at h1

end Pqr
