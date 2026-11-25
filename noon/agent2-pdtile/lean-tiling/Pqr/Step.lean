/-
Parts B and C: a step weak tiling complement gives the bounds.
-/
import Pqr.Defs

open Finset

set_option linter.unusedSectionVars false

namespace Pqr

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]

namespace Step

/-! ### Marginals of a real array, and how they sum -/

section Marginals

variable (A : X → Y → Z → ℝ)

/-- total mass of a real array -/
def rT : ℝ := ∑ i, ∑ j, ∑ k, A i j k
/-- the one-dimensional marginals -/
def rX (i : X) : ℝ := ∑ j, ∑ k, A i j k
def rY (j : Y) : ℝ := ∑ i, ∑ k, A i j k
def rZ (k : Z) : ℝ := ∑ i, ∑ j, A i j k
/-- the two-dimensional marginals -/
def rXY (i : X) (j : Y) : ℝ := ∑ k, A i j k
def rXZ (i : X) (k : Z) : ℝ := ∑ j, A i j k
def rYZ (j : Y) (k : Z) : ℝ := ∑ i, A i j k

theorem sum_rX : ∑ i, rX A i = rT A := rfl
theorem sum_rY : ∑ j, rY A j = rT A := by
  unfold rY rT; exact Finset.sum_comm
theorem sum_rZ : ∑ k, rZ A k = rT A := by
  unfold rZ rT
  rw [Finset.sum_comm]
  exact Finset.sum_congr rfl (fun i _ => Finset.sum_comm)
theorem sum_rXY_i (j : Y) : ∑ i, rXY A i j = rY A j := rfl
theorem sum_rXY_j (i : X) : ∑ j, rXY A i j = rX A i := rfl
theorem sum_rXZ_i (k : Z) : ∑ i, rXZ A i k = rZ A k := rfl
theorem sum_rXZ_k (i : X) : ∑ k, rXZ A i k = rX A i := by
  unfold rXZ rX; exact Finset.sum_comm
theorem sum_rYZ_j (k : Z) : ∑ j, rYZ A j k = rZ A k := by
  unfold rYZ rZ; exact Finset.sum_comm
theorem sum_rYZ_k (j : Y) : ∑ k, rYZ A j k = rY A j := by
  unfold rYZ rY; exact Finset.sum_comm
theorem sum_A_i (j : Y) (k : Z) : ∑ i, A i j k = rYZ A j k := rfl
theorem sum_A_j (i : X) (k : Z) : ∑ j, A i j k = rXZ A i k := rfl
theorem sum_A_k (i : X) (j : Y) : ∑ k, A i j k = rXY A i j := rfl

end Marginals

/-! ### Step 1: expansion of the tiling identity -/

/-- Step 1: the tiling sum against a step function, expanded in the marginals. -/
theorem expand [DecidableEq X] [DecidableEq Y] [DecidableEq Z]
    (A : X → Y → Z → ℝ) (γ : Bool → Bool → Bool → ℝ) (i : X) (j : Y) (k : Z) :
    ∑ i', ∑ j', ∑ k', A i' j' k' * γ (decide (i' = i)) (decide (j' = j)) (decide (k' = k))
      = γ false false false * rT A
        + (γ true false false - γ false false false) * rX A i
        + (γ false true false - γ false false false) * rY A j
        + (γ false false true - γ false false false) * rZ A k
        + (γ true true false - γ true false false - γ false true false + γ false false false)
            * rXY A i j
        + (γ true false true - γ true false false - γ false false true + γ false false false)
            * rXZ A i k
        + (γ false true true - γ false true false - γ false false true + γ false false false)
            * rYZ A j k
        + (γ true true true - γ true true false - γ true false true - γ false true true
            + γ true false false + γ false true false + γ false false true - γ false false false)
            * A i j k := by
  have hγ : ∀ i' j' k',
      A i' j' k' * γ (decide (i' = i)) (decide (j' = j)) (decide (k' = k))
      = γ false false false * A i' j' k'
        + (γ true false false - γ false false false) * (if i' = i then A i' j' k' else 0)
        + (γ false true false - γ false false false) * (if j' = j then A i' j' k' else 0)
        + (γ false false true - γ false false false) * (if k' = k then A i' j' k' else 0)
        + (γ true true false - γ true false false - γ false true false + γ false false false)
            * (if i' = i then (if j' = j then A i' j' k' else 0) else 0)
        + (γ true false true - γ true false false - γ false false true + γ false false false)
            * (if i' = i then (if k' = k then A i' j' k' else 0) else 0)
        + (γ false true true - γ false true false - γ false false true + γ false false false)
            * (if j' = j then (if k' = k then A i' j' k' else 0) else 0)
        + (γ true true true - γ true true false - γ true false true - γ false true true
            + γ true false false + γ false true false + γ false false true - γ false false false)
            * (if i' = i then (if j' = j then (if k' = k then A i' j' k' else 0) else 0)
                else 0) := by
    intro i' j' k'
    by_cases h1 : i' = i <;> by_cases h2 : j' = j <;> by_cases h3 : k' = k <;>
      simp [h1, h2, h3] <;> ring
  simp only [hγ, Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_ite_irrel,
    Finset.sum_const_zero, Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  rfl

/-- The identity (W). -/
def Weq (A : X → Y → Z → ℝ) (m0 mx my mz mxy mxz myz mxyz : ℝ) : Prop :=
  ∀ i j k, m0 * rT A + mx * rX A i + my * rY A j + mz * rZ A k + mxy * rXY A i j
    + mxz * rXZ A i k + myz * rYZ A j k + mxyz * A i j k = 1

/-! ### Step 2: summing (W) over coordinates -/

section Sums

variable {A : X → Y → Z → ℝ} {m0 mx my mz mxy mxz myz mxyz : ℝ} {p q r : ℝ}

/-- (W) summed over the third coordinate -/
theorem Weq.sumZ (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hr : (Fintype.card Z : ℝ) = r) (i : X) (j : Y) :
    (r * m0 + mz) * rT A + (r * mx + mxz) * rX A i + (r * my + myz) * rY A j
      + (r * mxy + mxyz) * rXY A i j = r := by
  subst hr
  have h := Finset.sum_congr (s₁ := (Finset.univ : Finset Z)) rfl (fun k _ => W i j k)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, mul_one, sum_rZ, sum_rXZ_k, sum_rYZ_k, sum_A_k A i j] at h
  linear_combination h

/-- (W) summed over the second coordinate -/
theorem Weq.sumY (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hq : (Fintype.card Y : ℝ) = q) (i : X) (k : Z) :
    (q * m0 + my) * rT A + (q * mx + mxy) * rX A i + (q * mz + myz) * rZ A k
      + (q * mxz + mxyz) * rXZ A i k = q := by
  subst hq
  have h := Finset.sum_congr (s₁ := (Finset.univ : Finset Y)) rfl (fun j _ => W i j k)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, mul_one, sum_rY, sum_rXY_j, sum_rYZ_j, sum_A_j A i k] at h
  linear_combination h

/-- (W) summed over the first coordinate -/
theorem Weq.sumX (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (j : Y) (k : Z) :
    (p * m0 + mx) * rT A + (p * my + mxy) * rY A j + (p * mz + mxz) * rZ A k
      + (p * myz + mxyz) * rYZ A j k = p := by
  subst hp
  have h := Finset.sum_congr (s₁ := (Finset.univ : Finset X)) rfl (fun i _ => W i j k)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, mul_one, sum_rX, sum_rXY_i, sum_rXZ_i, sum_A_i A j k] at h
  linear_combination h

/-- (W) summed over the second and third coordinates -/
theorem Weq.sumYZ (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hq : (Fintype.card Y : ℝ) = q) (hr : (Fintype.card Z : ℝ) = r) (i : X) :
    (q * r * m0 + q * mz + r * my + myz) * rT A
      + (q * r * mx + r * mxy + q * mxz + mxyz) * rX A i = q * r := by
  subst hq
  have h := Finset.sum_congr (s₁ := (Finset.univ : Finset Y)) rfl (fun j _ => W.sumZ hr i j)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, sum_rY, sum_rXY_j] at h
  linear_combination h

/-- (W) summed over the first and third coordinates -/
theorem Weq.sumXZ (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (hr : (Fintype.card Z : ℝ) = r) (j : Y) :
    (p * r * m0 + p * mz + r * mx + mxz) * rT A
      + (p * r * my + r * mxy + p * myz + mxyz) * rY A j = p * r := by
  subst hp
  have h := Finset.sum_congr (s₁ := (Finset.univ : Finset X)) rfl (fun i _ => W.sumZ hr i j)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, sum_rX, sum_rXY_i] at h
  linear_combination h

/-- (W) summed over the first and second coordinates -/
theorem Weq.sumXY (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (hq : (Fintype.card Y : ℝ) = q) (k : Z) :
    (p * q * m0 + p * my + q * mx + mxy) * rT A
      + (p * q * mz + q * mxz + p * myz + mxyz) * rZ A k = p * q := by
  subst hp
  have h := Finset.sum_congr (s₁ := (Finset.univ : Finset X)) rfl (fun i _ => W.sumY hq i k)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, sum_rX, sum_rXZ_i] at h
  linear_combination h

/-- Step 2 (a): (W) summed over everything -/
theorem Weq.lam0 (W : Weq A m0 mx my mz mxy mxz myz mxyz) (hp : (Fintype.card X : ℝ) = p)
    (hq : (Fintype.card Y : ℝ) = q) (hr : (Fintype.card Z : ℝ) = r) :
    (p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz + mxyz)
      * rT A = p * q * r := by
  subst hp
  have h := Finset.sum_congr (s₁ := (Finset.univ : Finset X)) rfl (fun i _ => W.sumYZ hq hr i)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, sum_rX] at h
  linear_combination h

/-- Step 2 (b) -/
theorem Weq.lamX (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hq : (Fintype.card Y : ℝ) = q) (hr : (Fintype.card Z : ℝ) = r) (i i' : X) :
    (q * r * mx + r * mxy + q * mxz + mxyz) * (rX A i - rX A i') = 0 := by
  linear_combination W.sumYZ hq hr i - W.sumYZ hq hr i'

theorem Weq.lamY (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (hr : (Fintype.card Z : ℝ) = r) (j j' : Y) :
    (p * r * my + r * mxy + p * myz + mxyz) * (rY A j - rY A j') = 0 := by
  linear_combination W.sumXZ hp hr j - W.sumXZ hp hr j'

theorem Weq.lamZ (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (hq : (Fintype.card Y : ℝ) = q) (k k' : Z) :
    (p * q * mz + q * mxz + p * myz + mxyz) * (rZ A k - rZ A k') = 0 := by
  linear_combination W.sumXY hp hq k - W.sumXY hp hq k'

/-- Step 2 (c) -/
theorem Weq.lamXY (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hr : (Fintype.card Z : ℝ) = r) (i i' : X) (j j' : Y) :
    (r * mxy + mxyz) * (rXY A i j + rXY A i' j' - rXY A i j' - rXY A i' j) = 0 := by
  linear_combination W.sumZ hr i j + W.sumZ hr i' j' - W.sumZ hr i j' - W.sumZ hr i' j

theorem Weq.lamXZ (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hq : (Fintype.card Y : ℝ) = q) (i i' : X) (k k' : Z) :
    (q * mxz + mxyz) * (rXZ A i k + rXZ A i' k' - rXZ A i k' - rXZ A i' k) = 0 := by
  linear_combination W.sumY hq i k + W.sumY hq i' k' - W.sumY hq i k' - W.sumY hq i' k

theorem Weq.lamYZ (W : Weq A m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (j j' : Y) (k k' : Z) :
    (p * myz + mxyz) * (rYZ A j k + rYZ A j' k' - rYZ A j k' - rYZ A j' k) = 0 := by
  linear_combination W.sumX hp j k + W.sumX hp j' k' - W.sumX hp j k' - W.sumX hp j' k

/-- Step 2 (d) -/
theorem Weq.lamXYZ (W : Weq A m0 mx my mz mxy mxz myz mxyz) (i i' : X) (j j' : Y) (k k' : Z) :
    mxyz * (A i j k + A i' j' k + A i' j k' + A i j' k'
      - (A i' j k + A i j' k + A i j k' + A i' j' k')) = 0 := by
  linear_combination W i j k + W i' j' k + W i' j k' + W i j' k'
    - W i' j k - W i j' k - W i j k' - W i' j' k'

end Sums

/-! ### Step 3: the arithmetic, over the reals -/

section Arith

variable {p q r n m0 mx my mz mxy mxz myz mxyz : ℝ}

theorem le_of_mul {L n c K : ℝ} (hK : 0 < K) (hc : 0 ≤ c) (hL : K ≤ L) (h : L * n = K * c) :
    n ≤ c := by
  by_contra hn
  rw [not_le] at hn
  have hn0 : 0 < n := lt_of_le_of_lt hc hn
  have h1 : K * n ≤ L * n := mul_le_mul_of_nonneg_right hL hn0.le
  have h2 : K * c < K * n := mul_lt_mul_of_pos_left hn hK
  linarith

/-- identity (I0): if all seven `Λ` vanish then `n = 1` -/
theorem arith_b0 (hp : 1 ≤ p) (hq : 1 ≤ q) (hr : 1 ≤ r)
    (h1 : m0 + mx + my + mz + mxy + mxz + myz + mxyz = 1)
    (hn : (p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz) * n = p * q * r)
    (hx : q * r * mx + r * mxy + q * mxz + mxyz = 0)
    (hy : p * r * my + r * mxy + p * myz + mxyz = 0)
    (hz : p * q * mz + q * mxz + p * myz + mxyz = 0)
    (hxy : r * mxy + mxyz = 0) (hxz : q * mxz + mxyz = 0) (hyz : p * myz + mxyz = 0)
    (hxyz : mxyz = 0) : n ≤ 1 := by
  have hL : p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz = p * q * r := by
    linear_combination (p * q * r) * h1 - (p - 1) * hx - (q - 1) * hy - (r - 1) * hz
      - (p - 1) * (q - 1) * hxy - (p - 1) * (r - 1) * hxz - (q - 1) * (r - 1) * hyz
      - (p - 1) * (q - 1) * (r - 1) * hxyz
  have hp0 : 0 < p := by linarith
  have hq0 : 0 < q := by linarith
  have hr0 : 0 < r := by linarith
  exact le_of_mul (mul_pos (mul_pos hp0 hq0) hr0) zero_le_one hL.ge (by linear_combination hn)

/-- identity (Ix) -/
theorem arith_bx (hp : 1 ≤ p) (hq : 1 ≤ q) (hr : 1 ≤ r)
    (h1 : m0 + mx + my + mz + mxy + mxz + myz + mxyz = 1)
    (hftt : 0 ≤ m0 + my + mz + myz)
    (hn : (p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz) * n = p * q * r)
    (hy : p * r * my + r * mxy + p * myz + mxyz = 0)
    (hz : p * q * mz + q * mxz + p * myz + mxyz = 0)
    (hyz : p * myz + mxyz = 0) : n ≤ p := by
  have hL : p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz = q * r * (1 + (p - 1) * (m0 + my + mz + myz)) := by
    linear_combination (q * r) * h1 - (q - 1) * hy - (r - 1) * hz - (q - 1) * (r - 1) * hyz
  have hq0 : 0 < q := by linarith
  have hr0 : 0 < r := by linarith
  have hqr : 0 < q * r := mul_pos hq0 hr0
  have h2 : 0 ≤ (p - 1) * (m0 + my + mz + myz) := mul_nonneg (by linarith) hftt
  have hK : q * r ≤ p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz
      + p * myz + mxyz := by
    rw [hL]
    exact le_mul_of_one_le_right hqr.le (by linarith)
  exact le_of_mul hqr (by linarith) hK (by linear_combination hn)

/-- identity (Ixy) -/
theorem arith_bxy (hp : 1 ≤ p) (hq : 1 ≤ q) (hr : 1 ≤ r)
    (h1 : m0 + mx + my + mz + mxy + mxz + myz + mxyz = 1)
    (hftt : 0 ≤ m0 + my + mz + myz) (htft : 0 ≤ m0 + mx + mz + mxz) (hfft : 0 ≤ m0 + mz)
    (hn : (p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz) * n = p * q * r)
    (hz : p * q * mz + q * mxz + p * myz + mxyz = 0) : n ≤ p * q := by
  have hL : p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz = r * (1 + (p - 1) * (m0 + my + mz + myz) + (q - 1) * (m0 + mx + mz + mxz)
        + (p - 1) * (q - 1) * (m0 + mz)) := by
    linear_combination r * h1 - (r - 1) * hz
  have hp0 : 0 < p := by linarith
  have hq0 : 0 < q := by linarith
  have hr0 : 0 < r := by linarith
  have h2 : 0 ≤ (p - 1) * (m0 + my + mz + myz) := mul_nonneg (by linarith) hftt
  have h3 : 0 ≤ (q - 1) * (m0 + mx + mz + mxz) := mul_nonneg (by linarith) htft
  have h4 : 0 ≤ (p - 1) * (q - 1) * (m0 + mz) :=
    mul_nonneg (mul_nonneg (by linarith) (by linarith)) hfft
  have hK : r ≤ p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz
      + p * myz + mxyz := by
    rw [hL]
    exact le_mul_of_one_le_right hr0.le (by linarith)
  exact le_of_mul hr0 (mul_pos hp0 hq0).le hK (by linear_combination hn)

/-- identity (Cxy), in the case `p ≤ q` -/
theorem arith_cxy (hp : 1 ≤ p) (hq : 1 ≤ q) (hr : 1 ≤ r) (hpq : p ≤ q)
    (h1 : m0 + mx + my + mz + mxy + mxz + myz + mxyz = 1)
    (htft : 0 ≤ m0 + mx + mz + mxz) (hfft : 0 ≤ m0 + mz)
    (hn : (p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz) * n = p * q * r)
    (hz : p * q * mz + q * mxz + p * myz + mxyz = 0)
    (hxy : r * mxy + mxyz = 0) (hxyz : mxyz = 0) : n ≤ q := by
  have hL : p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz = r * (p + (q - p) * (m0 + mx + mz + mxz) + (p * q - q) * (m0 + mz)) := by
    linear_combination (r * p) * h1 - (r - 1) * hz - (p - 1) * hxy - (p - 1) * (r - 1) * hxyz
  have hp0 : 0 < p := by linarith
  have hq0 : 0 < q := by linarith
  have hr0 : 0 < r := by linarith
  have h2 : 0 ≤ (q - p) * (m0 + mx + mz + mxz) := mul_nonneg (by linarith) htft
  have h3 : 0 ≤ (p * q - q) * (m0 + mz) := by
    have : 0 ≤ q * (p - 1) := mul_nonneg hq0.le (by linarith)
    exact mul_nonneg (by linarith) hfft
  have hK : r * p ≤ p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz
      + p * myz + mxyz := by
    rw [hL]
    exact mul_le_mul_of_nonneg_left (by linarith) hr0.le
  exact le_of_mul (mul_pos hr0 hp0) hq0.le hK (by linear_combination hn)

end Arith

/-! ### Back to the integer array -/

section Cast

variable (a : X → Y → Z → ℤ)

theorem rT_cast : rT (fun i j k => (a i j k : ℝ)) = (total a : ℝ) := by
  unfold rT total; push_cast; rfl
theorem rX_cast (i : X) : rX (fun i j k => (a i j k : ℝ)) i = (N1 a i : ℝ) := by
  unfold rX N1; push_cast; rfl
theorem rY_cast (j : Y) :
    rY (fun i j k => (a i j k : ℝ)) j = (N1 (fun j i k => a i j k) j : ℝ) := by
  unfold rY N1; push_cast; rfl
theorem rZ_cast (k : Z) :
    rZ (fun i j k => (a i j k : ℝ)) k = (N1 (fun k i j => a i j k) k : ℝ) := by
  unfold rZ N1; push_cast; rfl
theorem rXY_cast (i : X) (j : Y) : rXY (fun i j k => (a i j k : ℝ)) i j = (N2 a i j : ℝ) := by
  unfold rXY N2; push_cast; rfl
theorem rXZ_cast (i : X) (k : Z) :
    rXZ (fun i j k => (a i j k : ℝ)) i k = (N2 (fun i k j => a i j k) i k : ℝ) := by
  unfold rXZ N2; push_cast; rfl
theorem rYZ_cast (j : Y) (k : Z) :
    rYZ (fun i j k => (a i j k : ℝ)) j k = (N2 (fun j k i => a i j k) j k : ℝ) := by
  unfold rYZ N2; push_cast; rfl

end Cast

/-! ### Step 2, concluded: the dichotomies for the integer array -/

section Dichotomy

variable {a : X → Y → Z → ℤ} {m0 mx my mz mxy mxz myz mxyz : ℝ} {p q r : ℝ}

theorem F1_of_mul {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z] {b : X → Y → Z → ℤ}
    {L : ℝ} (hL : L ≠ 0) (h : ∀ i i', L * ((N1 b i : ℝ) - (N1 b i' : ℝ)) = 0) : F1 b := by
  intro i i'
  have h' : (N1 b i : ℝ) - (N1 b i' : ℝ) = 0 := (mul_eq_zero.mp (h i i')).resolve_left hL
  have h'' : (N1 b i : ℝ) = (N1 b i' : ℝ) := by linarith
  exact_mod_cast h''

theorem F2_of_mul {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z] {b : X → Y → Z → ℤ}
    {L : ℝ} (hL : L ≠ 0)
    (h : ∀ i i' j j', L * ((N2 b i j : ℝ) + (N2 b i' j' : ℝ) - (N2 b i j' : ℝ)
      - (N2 b i' j : ℝ)) = 0) : F2 b := by
  intro i i' j j'
  have h' : (N2 b i j : ℝ) + (N2 b i' j' : ℝ) - (N2 b i j' : ℝ) - (N2 b i' j : ℝ) = 0 :=
    (mul_eq_zero.mp (h i i' j j')).resolve_left hL
  have h'' : ((N2 b i j + N2 b i' j' : ℤ) : ℝ) = ((N2 b i j' + N2 b i' j : ℤ) : ℝ) := by
    push_cast; linarith
  exact_mod_cast h''

theorem zero_of_not_Fx (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (hq : (Fintype.card Y : ℝ) = q) (hr : (Fintype.card Z : ℝ) = r) (hF : ¬ Fx a) :
    q * r * mx + r * mxy + q * mxz + mxyz = 0 := by
  by_contra hL
  refine hF (F1_of_mul hL fun i i' => ?_)
  have h := W.lamX hq hr i i'
  rwa [rX_cast, rX_cast] at h

theorem zero_of_not_Fy (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (hr : (Fintype.card Z : ℝ) = r) (hF : ¬ Fy a) :
    p * r * my + r * mxy + p * myz + mxyz = 0 := by
  by_contra hL
  refine hF (F1_of_mul hL fun j j' => ?_)
  have h := W.lamY hp hr j j'
  rwa [rY_cast, rY_cast] at h

theorem zero_of_not_Fz (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (hq : (Fintype.card Y : ℝ) = q) (hF : ¬ Fz a) :
    p * q * mz + q * mxz + p * myz + mxyz = 0 := by
  by_contra hL
  refine hF (F1_of_mul hL fun k k' => ?_)
  have h := W.lamZ hp hq k k'
  rwa [rZ_cast, rZ_cast] at h

theorem zero_of_not_Fxy (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (hr : (Fintype.card Z : ℝ) = r) (hF : ¬ Fxy a) : r * mxy + mxyz = 0 := by
  by_contra hL
  refine hF (F2_of_mul hL fun i i' j j' => ?_)
  have h := W.lamXY hr i i' j j'
  rwa [rXY_cast, rXY_cast, rXY_cast, rXY_cast] at h

theorem zero_of_not_Fxz (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (hq : (Fintype.card Y : ℝ) = q) (hF : ¬ Fxz a) : q * mxz + mxyz = 0 := by
  by_contra hL
  refine hF (F2_of_mul hL fun i i' k k' => ?_)
  have h := W.lamXZ hq i i' k k'
  rwa [rXZ_cast, rXZ_cast, rXZ_cast, rXZ_cast] at h

theorem zero_of_not_Fyz (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (hp : (Fintype.card X : ℝ) = p) (hF : ¬ Fyz a) : p * myz + mxyz = 0 := by
  by_contra hL
  refine hF (F2_of_mul hL fun j j' k k' => ?_)
  have h := W.lamYZ hp j j' k k'
  rwa [rYZ_cast, rYZ_cast, rYZ_cast, rYZ_cast] at h

theorem zero_of_not_F3 (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (hF : ¬ F3 a) : mxyz = 0 := by
  by_contra hL
  refine hF fun i i' j j' k k' => ?_
  have h := (mul_eq_zero.mp (W.lamXYZ i i' j j' k k')).resolve_left hL
  have h' : ((a i j k + a i' j' k + a i' j k' + a i j' k' : ℤ) : ℝ)
      = ((a i' j k + a i j' k + a i j k' + a i' j' k' : ℤ) : ℝ) := by
    push_cast; linarith
  exact_mod_cast h'

end Dichotomy

/-! ### Assembly -/

/-- an array of total mass zero satisfies all the bounds (used when one of the types is empty) -/
theorem bounds_of_total_zero (a : X → Y → Z → ℤ) (h0 : total a = 0) : Bounds a where
  b0 := fun _ _ _ _ _ _ _ => by rw [h0]; exact zero_le_one
  bx := fun _ _ _ => by rw [h0]; positivity
  by' := fun _ _ _ => by rw [h0]; positivity
  bz := fun _ _ _ => by rw [h0]; positivity
  bxy := fun _ => by rw [h0]; positivity
  bxz := fun _ => by rw [h0]; positivity
  byz := fun _ => by rw [h0]; positivity
  cxy := fun _ _ _ => by rw [h0]; positivity
  cxz := fun _ _ _ => by rw [h0]; positivity
  cyz := fun _ _ _ => by rw [h0]; positivity

/-- Steps 2 and 3: the identity (W), with the coefficients coming from a nonnegative step function
with value `1` at the origin, gives the bounds. -/
theorem bounds_of_Weq [Nonempty X] [Nonempty Y] [Nonempty Z] (a : X → Y → Z → ℤ)
    {m0 mx my mz mxy mxz myz mxyz : ℝ}
    (W : Weq (fun i j k => (a i j k : ℝ)) m0 mx my mz mxy mxz myz mxyz)
    (h1 : m0 + mx + my + mz + mxy + mxz + myz + mxyz = 1)
    (htff : 0 ≤ m0 + mx) (hftf : 0 ≤ m0 + my) (hfft : 0 ≤ m0 + mz)
    (httf : 0 ≤ m0 + mx + my + mxy) (htft : 0 ≤ m0 + mx + mz + mxz)
    (hftt : 0 ≤ m0 + my + mz + myz) : Bounds a := by
  obtain ⟨p, hp⟩ : ∃ p : ℝ, (Fintype.card X : ℝ) = p := ⟨_, rfl⟩
  obtain ⟨q, hq⟩ : ∃ q : ℝ, (Fintype.card Y : ℝ) = q := ⟨_, rfl⟩
  obtain ⟨r, hr⟩ : ∃ r : ℝ, (Fintype.card Z : ℝ) = r := ⟨_, rfl⟩
  obtain ⟨n, hn'⟩ : ∃ n : ℝ, (total a : ℝ) = n := ⟨_, rfl⟩
  have hp1 : 1 ≤ p := by rw [← hp]; exact_mod_cast Fintype.card_pos (α := X)
  have hq1 : 1 ≤ q := by rw [← hq]; exact_mod_cast Fintype.card_pos (α := Y)
  have hr1 : 1 ≤ r := by rw [← hr]; exact_mod_cast Fintype.card_pos (α := Z)
  have hn : (p * q * r * m0 + q * r * mx + p * r * my + p * q * mz + r * mxy + q * mxz + p * myz
      + mxyz) * n = p * q * r := by
    have h := W.lam0 hp hq hr
    rwa [rT_cast, hn'] at h
  have ex := zero_of_not_Fx W hq hr
  have ey := zero_of_not_Fy W hp hr
  have ez := zero_of_not_Fz W hp hq
  have exy := zero_of_not_Fxy W hr
  have exz := zero_of_not_Fxz W hq
  have eyz := zero_of_not_Fyz W hp
  have e3 := zero_of_not_F3 W
  have key : ∀ c : ℤ, n ≤ (c : ℝ) → total a ≤ c := fun c h => by
    rw [← hn'] at h; exact_mod_cast h
  have hpZ : (((Fintype.card X : ℕ) : ℤ) : ℝ) = p := by rw [← hp]; norm_cast
  have hqZ : (((Fintype.card Y : ℕ) : ℤ) : ℝ) = q := by rw [← hq]; norm_cast
  have hrZ : (((Fintype.card Z : ℕ) : ℤ) : ℝ) = r := by rw [← hr]; norm_cast
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- b0
    intro fx fy fz fxy fxz fyz f3
    refine key 1 ?_
    rw [Int.cast_one]
    exact arith_b0 hp1 hq1 hr1 h1 hn (ex fx) (ey fy) (ez fz) (exy fxy) (exz fxz) (eyz fyz) (e3 f3)
  · -- bx
    intro fy fz fyz
    refine key _ ?_
    rw [hpZ]
    exact arith_bx hp1 hq1 hr1 h1 hftt hn (ey fy) (ez fz) (eyz fyz)
  · -- by
    intro fx fz fxz
    refine key _ ?_
    rw [hqZ]
    exact arith_bx (p := q) (q := p) (r := r) (mx := my) (my := mx) (mz := mz) (mxy := mxy)
      (mxz := myz) (myz := mxz) (n := n) (m0 := m0) (mxyz := mxyz) hq1 hp1 hr1 (by linarith [h1])
      (by linarith [htft]) (by linear_combination hn) (by linear_combination ex fx)
      (by linear_combination ez fz) (by linear_combination exz fxz)
  · -- bz
    intro fx fy fxy
    refine key _ ?_
    rw [hrZ]
    exact arith_bx (p := r) (q := q) (r := p) (mx := mz) (my := my) (mz := mx) (mxy := myz)
      (mxz := mxz) (myz := mxy) (n := n) (m0 := m0) (mxyz := mxyz) hr1 hq1 hp1 (by linarith [h1])
      (by linarith [httf]) (by linear_combination hn) (by linear_combination ey fy)
      (by linear_combination ex fx) (by linear_combination exy fxy)
  · -- bxy
    intro fz
    refine key _ ?_
    rw [Int.cast_mul, hpZ, hqZ]
    exact arith_bxy hp1 hq1 hr1 h1 hftt htft hfft hn (ez fz)
  · -- bxz
    intro fy
    refine key _ ?_
    rw [Int.cast_mul, hpZ, hrZ]
    exact arith_bxy (p := p) (q := r) (r := q) (mx := mx) (my := mz) (mz := my) (mxy := mxz)
      (mxz := mxy) (myz := myz) (n := n) (m0 := m0) (mxyz := mxyz) hp1 hr1 hq1 (by linarith [h1])
      (by linarith [hftt]) (by linarith [httf]) (by linarith [hftf]) (by linear_combination hn)
      (by linear_combination ey fy)
  · -- byz
    intro fx
    refine key _ ?_
    rw [Int.cast_mul, hqZ, hrZ]
    exact arith_bxy (p := q) (q := r) (r := p) (mx := my) (my := mz) (mz := mx) (mxy := myz)
      (mxz := mxy) (myz := mxz) (n := n) (m0 := m0) (mxyz := mxyz) hq1 hr1 hp1 (by linarith [h1])
      (by linarith [htft]) (by linarith [httf]) (by linarith [htff]) (by linear_combination hn)
      (by linear_combination ex fx)
  · -- cxy
    intro fxy fz f3
    refine key _ ?_
    rw [Int.cast_natCast, Nat.cast_max, hp, hq]
    rcases le_total p q with hpq | hpq
    · refine le_max_of_le_right ?_
      exact arith_cxy hp1 hq1 hr1 hpq h1 htft hfft hn (ez fz) (exy fxy) (e3 f3)
    · refine le_max_of_le_left ?_
      exact arith_cxy (p := q) (q := p) (r := r) (mx := my) (my := mx) (mz := mz) (mxy := mxy)
        (mxz := myz) (myz := mxz) (n := n) (m0 := m0) (mxyz := mxyz) hq1 hp1 hr1 hpq
        (by linarith [h1]) (by linarith [hftt]) (by linarith [hfft]) (by linear_combination hn)
        (by linear_combination ez fz) (by linear_combination exy fxy) (e3 f3)
  · -- cxz
    intro fxz fy f3
    refine key _ ?_
    rw [Int.cast_natCast, Nat.cast_max, hp, hr]
    rcases le_total p r with hpq | hpq
    · refine le_max_of_le_right ?_
      exact arith_cxy (p := p) (q := r) (r := q) (mx := mx) (my := mz) (mz := my) (mxy := mxz)
        (mxz := mxy) (myz := myz) (n := n) (m0 := m0) (mxyz := mxyz) hp1 hr1 hq1 hpq
        (by linarith [h1]) (by linarith [httf]) (by linarith [hftf]) (by linear_combination hn)
        (by linear_combination ey fy) (by linear_combination exz fxz) (e3 f3)
    · refine le_max_of_le_left ?_
      exact arith_cxy (p := r) (q := p) (r := q) (mx := mz) (my := mx) (mz := my) (mxy := mxz)
        (mxz := myz) (myz := mxy) (n := n) (m0 := m0) (mxyz := mxyz) hr1 hp1 hq1 hpq
        (by linarith [h1]) (by linarith [hftt]) (by linarith [hftf]) (by linear_combination hn)
        (by linear_combination ey fy) (by linear_combination exz fxz) (e3 f3)
  · -- cyz
    intro fyz fx f3
    refine key _ ?_
    rw [Int.cast_natCast, Nat.cast_max, hq, hr]
    rcases le_total q r with hpq | hpq
    · refine le_max_of_le_right ?_
      exact arith_cxy (p := q) (q := r) (r := p) (mx := my) (my := mz) (mz := mx) (mxy := myz)
        (mxz := mxy) (myz := mxz) (n := n) (m0 := m0) (mxyz := mxyz) hq1 hr1 hp1 hpq
        (by linarith [h1]) (by linarith [httf]) (by linarith [htff]) (by linear_combination hn)
        (by linear_combination ex fx) (by linear_combination eyz fyz) (e3 f3)
    · refine le_max_of_le_left ?_
      exact arith_cxy (p := r) (q := q) (r := p) (mx := mz) (my := my) (mz := mx) (mxy := myz)
        (mxz := mxz) (myz := mxy) (n := n) (m0 := m0) (mxyz := mxyz) hr1 hq1 hp1 hpq
        (by linarith [h1]) (by linarith [htft]) (by linarith [htff]) (by linear_combination hn)
        (by linear_combination ex fx) (by linear_combination eyz fyz) (e3 f3)

end Step

variable [DecidableEq X] [DecidableEq Y] [DecidableEq Z]

open Step in
theorem bounds_of_stepTiling (a : X → Y → Z → ℤ) (γ : Bool → Bool → Bool → ℝ)
    (h : StepTiling a γ) : Bounds a := by
  obtain ⟨hpos, h1, hsum⟩ := h
  rcases isEmpty_or_nonempty X with hX | hX
  · exact bounds_of_total_zero a (by simp [total])
  rcases isEmpty_or_nonempty Y with hY | hY
  · exact bounds_of_total_zero a (by simp [total])
  rcases isEmpty_or_nonempty Z with hZ | hZ
  · exact bounds_of_total_zero a (by simp [total])
  have W : Weq (fun i j k => (a i j k : ℝ)) (γ false false false)
      (γ true false false - γ false false false)
      (γ false true false - γ false false false)
      (γ false false true - γ false false false)
      (γ true true false - γ true false false - γ false true false + γ false false false)
      (γ true false true - γ true false false - γ false false true + γ false false false)
      (γ false true true - γ false true false - γ false false true + γ false false false)
      (γ true true true - γ true true false - γ true false true - γ false true true
        + γ true false false + γ false true false + γ false false true - γ false false false) :=
    fun i j k => (expand (fun i j k => (a i j k : ℝ)) γ i j k).symm.trans (hsum i j k)
  refine bounds_of_Weq a W ?_ ?_ ?_ ?_ ?_ ?_ ?_
  · rw [← h1]; ring
  · have := hpos true false false; linarith
  · have := hpos false true false; linarith
  · have := hpos false false true; linarith
  · have := hpos true true false; linarith
  · have := hpos true false true; linarith
  · have := hpos false true true; linarith

end Pqr
