/-
Weak tiling implies tiling in Z_p × Z_q × Z_r  (≅ Z_{pqr}),  p, q, r distinct primes.

Definitions shared by all files.  Arrays are functions `a : X → Y → Z → ℤ` on a product of three finite
types (the indicator of a set when the values are 0 and 1).
-/
import Mathlib

open Finset

namespace Pqr

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]

/-- number of points (with multiplicity) whose first coordinate is `i` -/
def N1 (a : X → Y → Z → ℤ) (i : X) : ℤ := ∑ j, ∑ k, a i j k

/-- number of points whose first two coordinates are `i`, `j` -/
def N2 (a : X → Y → Z → ℤ) (i : X) (j : Y) : ℤ := ∑ k, a i j k

/-- total mass -/
def total (a : X → Y → Z → ℤ) : ℤ := ∑ i, ∑ j, ∑ k, a i j k

/-- `Φ_{p_x} ∣ A` in coordinates: the counts along the first coordinate are constant -/
def F1 (a : X → Y → Z → ℤ) : Prop := ∀ i i', N1 a i = N1 a i'

/-- a matrix is additive (of the form `u i + w j`): all mixed second differences vanish -/
def Add2 (N : X → Y → ℤ) : Prop := ∀ i i' j j', N i j + N i' j' = N i j' + N i' j

/-- `Φ_{p_x p_y} ∣ A` in coordinates: the two-dimensional counts are additive -/
def F2 (a : X → Y → Z → ℤ) : Prop := Add2 (N2 a)

/-- `Φ_{p_x p_y p_z} ∣ A` in coordinates: all mixed third differences vanish -/
def F3 (a : X → Y → Z → ℤ) : Prop :=
  ∀ i i' j j' k k', a i j k + a i' j' k + a i' j k' + a i j' k'
    = a i' j k + a i j' k + a i j k' + a i' j' k'

/-! The seven conditions for an array, by permuting coordinates. -/
def Fx (a : X → Y → Z → ℤ) : Prop := F1 a
def Fy (a : X → Y → Z → ℤ) : Prop := F1 (fun j i k => a i j k)
def Fz (a : X → Y → Z → ℤ) : Prop := F1 (fun k i j => a i j k)
def Fxy (a : X → Y → Z → ℤ) : Prop := F2 a
def Fxz (a : X → Y → Z → ℤ) : Prop := F2 (fun i k j => a i j k)
def Fyz (a : X → Y → Z → ℤ) : Prop := F2 (fun j k i => a i j k)

/-- The only consequences of weak tiling that the combinatorial argument uses: upper bounds on the
size of the set in terms of which of the seven conditions fail. -/
structure Bounds (a : X → Y → Z → ℤ) : Prop where
  b0 : ¬ Fx a → ¬ Fy a → ¬ Fz a → ¬ Fxy a → ¬ Fxz a → ¬ Fyz a → ¬ F3 a → total a ≤ 1
  bx : ¬ Fy a → ¬ Fz a → ¬ Fyz a → total a ≤ Fintype.card X
  by' : ¬ Fx a → ¬ Fz a → ¬ Fxz a → total a ≤ Fintype.card Y
  bz : ¬ Fx a → ¬ Fy a → ¬ Fxy a → total a ≤ Fintype.card Z
  bxy : ¬ Fz a → total a ≤ Fintype.card X * Fintype.card Y
  bxz : ¬ Fy a → total a ≤ Fintype.card X * Fintype.card Z
  byz : ¬ Fx a → total a ≤ Fintype.card Y * Fintype.card Z
  cxy : ¬ Fxy a → ¬ Fz a → ¬ F3 a → total a ≤ max (Fintype.card X) (Fintype.card Y)
  cxz : ¬ Fxz a → ¬ Fy a → ¬ F3 a → total a ≤ max (Fintype.card X) (Fintype.card Z)
  cyz : ¬ Fyz a → ¬ Fx a → ¬ F3 a → total a ≤ max (Fintype.card Y) (Fintype.card Z)

/-- A weak tiling complement that is a step function: its value at `v - a` depends only on which
coordinates of `v` and `a` agree (`true` = agree). -/
def StepTiling [DecidableEq X] [DecidableEq Y] [DecidableEq Z]
    (a : X → Y → Z → ℤ) (γ : Bool → Bool → Bool → ℝ) : Prop :=
  (∀ b1 b2 b3, 0 ≤ γ b1 b2 b3) ∧ γ true true true = 1 ∧
  ∀ i j k, ∑ i', ∑ j', ∑ k',
    (a i' j' k' : ℝ) * γ (decide (i' = i)) (decide (j' = j)) (decide (k' = k)) = 1

/-- The conclusion in coordinates: for some set of coordinates, projecting the set to them is a
bijection.  (Then the coordinate subgroup of the remaining coordinates is a tiling complement.) -/
def Structured (a : X → Y → Z → ℤ) : Prop :=
  total a = 1 ∨ (∀ i, N1 a i = 1) ∨ (∀ j, N1 (fun j i k => a i j k) j = 1)
    ∨ (∀ k, N1 (fun k i j => a i j k) k = 1)
    ∨ (∀ i j, N2 a i j = 1) ∨ (∀ i k, N2 (fun i k j => a i j k) i k = 1)
    ∨ (∀ j k, N2 (fun j k i => a i j k) j k = 1) ∨ (∀ i j k, a i j k = 1)

end Pqr
