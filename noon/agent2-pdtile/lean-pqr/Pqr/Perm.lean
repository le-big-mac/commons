/-
How the seven conditions, the total and the bounds behave when two coordinates are exchanged.
-/
import Pqr.Defs

open Finset

set_option linter.unusedSectionVars false

namespace Pqr

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]

/-- exchange the first two coordinates -/
def swapXY (a : X → Y → Z → ℤ) : Y → X → Z → ℤ := fun j i k => a i j k
/-- exchange the last two coordinates -/
def swapYZ (a : X → Y → Z → ℤ) : X → Z → Y → ℤ := fun i k j => a i j k

@[simp] theorem swapXY_swapXY (a : X → Y → Z → ℤ) : swapXY (swapXY a) = a := rfl
@[simp] theorem swapYZ_swapYZ (a : X → Y → Z → ℤ) : swapYZ (swapYZ a) = a := rfl

theorem total_swapXY (a : X → Y → Z → ℤ) : total (swapXY a) = total a := by
  unfold total swapXY; exact Finset.sum_comm

theorem total_swapYZ (a : X → Y → Z → ℤ) : total (swapYZ a) = total a := by
  unfold total swapYZ; exact Finset.sum_congr rfl (fun i _ => Finset.sum_comm)

theorem Add2_transpose (N : X → Y → ℤ) : Add2 (fun j i => N i j) ↔ Add2 N := by
  constructor
  · intro h i i' j j'; have := h j j' i i'; linarith
  · intro h j j' i i'; have := h i i' j j'; linarith

theorem F1_swapYZ (a : X → Y → Z → ℤ) : F1 (swapYZ a) ↔ F1 a := by
  have h : ∀ i, N1 (swapYZ a) i = N1 a i := fun i => by
    unfold N1 swapYZ; exact Finset.sum_comm
  unfold F1; simp only [h]

theorem F3_swapXY (a : X → Y → Z → ℤ) : F3 (swapXY a) ↔ F3 a := by
  constructor
  · intro h i i' j j' k k'; have := h j j' i i' k k'; unfold swapXY at this; linarith
  · intro h j j' i i' k k'; have := h i i' j j' k k'; unfold swapXY; linarith

theorem F3_swapYZ (a : X → Y → Z → ℤ) : F3 (swapYZ a) ↔ F3 a := by
  constructor
  · intro h i i' j j' k k'; have := h i i' k k' j j'; unfold swapYZ at this; linarith
  · intro h i i' k k' j j'; have := h i i' j j' k k'; unfold swapYZ; linarith

/-! ### exchanging the first two coordinates -/
theorem Fx_swapXY (a : X → Y → Z → ℤ) : Fx (swapXY a) ↔ Fy a := Iff.rfl
theorem Fy_swapXY (a : X → Y → Z → ℤ) : Fy (swapXY a) ↔ Fx a := Iff.rfl
theorem Fz_swapXY (a : X → Y → Z → ℤ) : Fz (swapXY a) ↔ Fz a :=
  F1_swapYZ (fun k i j => a i j k)
theorem Fxy_swapXY (a : X → Y → Z → ℤ) : Fxy (swapXY a) ↔ Fxy a :=
  Add2_transpose (N2 a)
theorem Fxz_swapXY (a : X → Y → Z → ℤ) : Fxz (swapXY a) ↔ Fyz a := Iff.rfl
theorem Fyz_swapXY (a : X → Y → Z → ℤ) : Fyz (swapXY a) ↔ Fxz a := Iff.rfl

/-! ### exchanging the last two coordinates -/
theorem Fx_swapYZ (a : X → Y → Z → ℤ) : Fx (swapYZ a) ↔ Fx a := F1_swapYZ a
theorem Fy_swapYZ (a : X → Y → Z → ℤ) : Fy (swapYZ a) ↔ Fz a := Iff.rfl
theorem Fz_swapYZ (a : X → Y → Z → ℤ) : Fz (swapYZ a) ↔ Fy a := Iff.rfl
theorem Fxy_swapYZ (a : X → Y → Z → ℤ) : Fxy (swapYZ a) ↔ Fxz a := Iff.rfl
theorem Fxz_swapYZ (a : X → Y → Z → ℤ) : Fxz (swapYZ a) ↔ Fxy a := Iff.rfl
theorem Fyz_swapYZ (a : X → Y → Z → ℤ) : Fyz (swapYZ a) ↔ Fyz a :=
  Add2_transpose (N2 (fun j k i => a i j k))

theorem Bounds.swapXY {a : X → Y → Z → ℤ} (B : Bounds a) : Bounds (swapXY a) where
  b0 := fun h1 h2 h3 h4 h5 h6 h7 => by
    rw [total_swapXY]
    exact B.b0 ((Fy_swapXY a).not.mp h2) ((Fx_swapXY a).not.mp h1) ((Fz_swapXY a).not.mp h3)
      ((Fxy_swapXY a).not.mp h4) ((Fyz_swapXY a).not.mp h6) ((Fxz_swapXY a).not.mp h5)
      ((F3_swapXY a).not.mp h7)
  bx := fun h1 h2 h3 => by
    rw [total_swapXY]
    exact B.by' ((Fy_swapXY a).not.mp h1) ((Fz_swapXY a).not.mp h2) ((Fyz_swapXY a).not.mp h3)
  by' := fun h1 h2 h3 => by
    rw [total_swapXY]
    exact B.bx ((Fx_swapXY a).not.mp h1) ((Fz_swapXY a).not.mp h2) ((Fxz_swapXY a).not.mp h3)
  bz := fun h1 h2 h3 => by
    rw [total_swapXY]
    exact B.bz ((Fy_swapXY a).not.mp h2) ((Fx_swapXY a).not.mp h1) ((Fxy_swapXY a).not.mp h3)
  bxy := fun h1 => by
    rw [total_swapXY, mul_comm]; exact B.bxy ((Fz_swapXY a).not.mp h1)
  bxz := fun h1 => by
    rw [total_swapXY]; exact B.byz ((Fy_swapXY a).not.mp h1)
  byz := fun h1 => by
    rw [total_swapXY]; exact B.bxz ((Fx_swapXY a).not.mp h1)
  cxy := fun h1 h2 h3 => by
    rw [total_swapXY, max_comm]
    exact B.cxy ((Fxy_swapXY a).not.mp h1) ((Fz_swapXY a).not.mp h2) ((F3_swapXY a).not.mp h3)
  cxz := fun h1 h2 h3 => by
    rw [total_swapXY]
    exact B.cyz ((Fxz_swapXY a).not.mp h1) ((Fy_swapXY a).not.mp h2) ((F3_swapXY a).not.mp h3)
  cyz := fun h1 h2 h3 => by
    rw [total_swapXY]
    exact B.cxz ((Fyz_swapXY a).not.mp h1) ((Fx_swapXY a).not.mp h2) ((F3_swapXY a).not.mp h3)

theorem Bounds.swapYZ {a : X → Y → Z → ℤ} (B : Bounds a) : Bounds (swapYZ a) where
  b0 := fun h1 h2 h3 h4 h5 h6 h7 => by
    rw [total_swapYZ]
    exact B.b0 ((Fx_swapYZ a).not.mp h1) ((Fz_swapYZ a).not.mp h3) ((Fy_swapYZ a).not.mp h2)
      ((Fxz_swapYZ a).not.mp h5) ((Fxy_swapYZ a).not.mp h4) ((Fyz_swapYZ a).not.mp h6)
      ((F3_swapYZ a).not.mp h7)
  bx := fun h1 h2 h3 => by
    rw [total_swapYZ]
    exact B.bx ((Fz_swapYZ a).not.mp h2) ((Fy_swapYZ a).not.mp h1) ((Fyz_swapYZ a).not.mp h3)
  by' := fun h1 h2 h3 => by
    rw [total_swapYZ]
    exact B.bz ((Fx_swapYZ a).not.mp h1) ((Fz_swapYZ a).not.mp h2) ((Fxz_swapYZ a).not.mp h3)
  bz := fun h1 h2 h3 => by
    rw [total_swapYZ]
    exact B.by' ((Fx_swapYZ a).not.mp h1) ((Fy_swapYZ a).not.mp h2) ((Fxy_swapYZ a).not.mp h3)
  bxy := fun h1 => by
    rw [total_swapYZ]; exact B.bxz ((Fz_swapYZ a).not.mp h1)
  bxz := fun h1 => by
    rw [total_swapYZ]; exact B.bxy ((Fy_swapYZ a).not.mp h1)
  byz := fun h1 => by
    rw [total_swapYZ, mul_comm]; exact B.byz ((Fx_swapYZ a).not.mp h1)
  cxy := fun h1 h2 h3 => by
    rw [total_swapYZ]
    exact B.cxz ((Fxy_swapYZ a).not.mp h1) ((Fz_swapYZ a).not.mp h2) ((F3_swapYZ a).not.mp h3)
  cxz := fun h1 h2 h3 => by
    rw [total_swapYZ]
    exact B.cxy ((Fxz_swapYZ a).not.mp h1) ((Fy_swapYZ a).not.mp h2) ((F3_swapYZ a).not.mp h3)
  cyz := fun h1 h2 h3 => by
    rw [total_swapYZ, max_comm]
    exact B.cyz ((Fyz_swapYZ a).not.mp h1) ((Fx_swapYZ a).not.mp h2) ((F3_swapYZ a).not.mp h3)

end Pqr
