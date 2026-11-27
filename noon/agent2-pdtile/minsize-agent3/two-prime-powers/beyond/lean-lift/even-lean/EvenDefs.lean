/-
The statement on signs for every `n`: the definitions for the reduction modulo 3.

Setting as in `Pnq/SignDefs.lean`: `ι` a finite type (one point for each element of a multiset), `e : ι → ℕ` the
exponents, `ε : ι → Bool` a signing, `P e ε` the signed mask, `BadAt e ε d` (`Φ_d` divides the signed mask over `ℤ`).
New here: `F3` is the algebraic closure of `ZMod 3`; `val3 e ε ζ` is the signed mask evaluated at `ζ ∈ F3`; the signing
is 3-bad at `d` (`Bad3 e ε d`) if `val3 e ε ζ = 0` for EVERY `ζ ∈ F3` that is a primitive `d`-th root of unity
(every one, not one: `Φ_d` is reducible modulo 3); `bad3Set e d` is the set of these signings; `classSum3` is the
`classSum` of `SignDefs` in `F3`.
Remarks on the definition.  If `3 ∣ d` and `d ≠ 0`, `F3` has no primitive `d`-th root of unity and every signing is
3-bad at `d`; and `0 ∈ F3` is a "primitive `0`-th root" in Mathlib's sense, so `Bad3 e ε 0` says that the signs of the
elements with exponent `0` add up to `0` in `F3`.  The statements about `Bad3` therefore carry `¬ 3 ∣ d`, which also
gives `d ≠ 0`.
(Definitions fixed on 27 November 2026, before any Lean proof that uses them.  None of them can be evaluated.)
-/
import Pnq.SignDefs

open Finset

namespace Pnq

/-- the algebraic closure of the field with three elements -/
abbrev F3 : Type := AlgebraicClosure (ZMod 3)

section

variable {ι : Type*} [Fintype ι]

/-- the signed mask of the signing `ε` evaluated at `ζ ∈ F3`: `∑ k, sg (ε k) ζ ^ e k` -/
noncomputable def val3 (e : ι → ℕ) (ε : ι → Bool) (ζ : F3) : F3 :=
  ∑ k, (sg (ε k) : F3) * ζ ^ e k

/-- the signing `ε` is 3-bad at `d`: the signed mask vanishes at every primitive `d`-th root of unity of `F3`
(for `3 ∤ d`: `Φ_d` divides the signed mask modulo 3) -/
def Bad3 (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) : Prop :=
  ∀ ζ : F3, IsPrimitiveRoot ζ d → val3 e ε ζ = 0

open Classical in
/-- the set of the signings that are 3-bad at `d` -/
noncomputable def bad3Set (e : ι → ℕ) (d : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε => Bad3 e ε d

/-- the signed sum `∑ sg (ε k) η ^ e k` in `F3` over the elements `k` in the class `r` modulo `M` (that is,
`e k % M = r`): the `classSum` of `Pnq/SignDefs.lean` with `F3` for `ℂ` -/
noncomputable def classSum3 (e : ι → ℕ) (ε : ι → Bool) (η : F3) (M r : ℕ) : F3 :=
  ∑ k, if e k % M = r then (sg (ε k) : F3) * η ^ e k else 0

/-! Unfolding lemmas. -/

/-- membership in `bad3Set` (unfolding) -/
theorem mem_bad3Set (e : ι → ℕ) (d : ℕ) (ε : ι → Bool) : ε ∈ bad3Set e d ↔ Bad3 e ε d := by
  simp [bad3Set]

/-- `val3 e ε ζ` is the signed mask `P e ε ∈ ℤ[X]` evaluated at `ζ` (through the ring map `ℤ → F3`), as `aeval` -/
theorem val3_eq_aeval (e : ι → ℕ) (ε : ι → Bool) (ζ : F3) :
    val3 e ε ζ = Polynomial.aeval ζ (P e ε) := by
  simp [val3, P]

/-- `val3 e ε ζ` is the signed mask `P e ε ∈ ℤ[X]` evaluated at `ζ` through the ring map `ℤ → F3`, as `eval₂` -/
theorem val3_eq_eval₂ (e : ι → ℕ) (ε : ι → Bool) (ζ : F3) :
    val3 e ε ζ = (P e ε).eval₂ (Int.castRingHom F3) ζ := by
  rw [val3_eq_aeval, Polynomial.aeval_def,
    Subsingleton.elim (algebraMap ℤ F3) (Int.castRingHom F3)]

/-- `val3 e ε ζ` is the value at `ζ` of the image of the signed mask in `F3[X]` -/
theorem val3_eq_eval_map (e : ι → ℕ) (ε : ι → Bool) (ζ : F3) :
    val3 e ε ζ = ((P e ε).map (Int.castRingHom F3)).eval ζ := by
  simp [val3, P, Polynomial.eval_finsetSum, Polynomial.map_sum]

end

end Pnq
