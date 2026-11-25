/-
Part D: the combinatorial argument.  From the bounds to the structure of the set.
(Lemmas 3–6 and Section 5 of `pqr-agent2.md`, for arrays on a product of three finite types.)
-/
import Pqr.Defs
import Pqr.Perm

open Finset

set_option linter.unusedSectionVars false
set_option linter.unusedVariables false

namespace Pqr

variable {X Y Z : Type*} [Fintype X] [Fintype Y] [Fintype Z]

/-! ### Additive matrices -/

/-- Normal form of an additive matrix of nonnegative integers: `a₀ + α i + β j` with `a₀, α, β ≥ 0` and
`min α = min β = 0`. -/
theorem normal_form [Nonempty X] [Nonempty Y] (N : X → Y → ℤ) (hadd : Add2 N)
    (hnn : ∀ i j, 0 ≤ N i j) :
    ∃ (a0 : ℤ) (α : X → ℤ) (β : Y → ℤ), 0 ≤ a0 ∧ (∀ i, 0 ≤ α i) ∧ (∀ j, 0 ≤ β j) ∧
      (∃ i, α i = 0) ∧ (∃ j, β j = 0) ∧ ∀ i j, N i j = a0 + α i + β j := by
  obtain ⟨j1⟩ := ‹Nonempty Y›
  obtain ⟨i0, -, hi0⟩ := Finset.exists_min_image (univ : Finset X) (fun i => N i j1) univ_nonempty
  obtain ⟨j0, -, hj0⟩ := Finset.exists_min_image (univ : Finset Y) (fun j => N i0 j) univ_nonempty
  refine ⟨N i0 j0, fun i => N i j0 - N i0 j0, fun j => N i0 j - N i0 j0, hnn _ _, ?_, ?_,
    ⟨i0, by simp⟩, ⟨j0, by simp⟩, ?_⟩
  · intro i
    have h1 := hadd i i0 j0 j1
    have h2 := hi0 i (mem_univ _)
    linarith
  · intro j
    have := hj0 j (mem_univ _)
    linarith
  · intro i j
    have := hadd i i0 j j0
    linarith

/-- Sum of a matrix in normal form along a row. -/
theorem row_sum_nf (a0 : ℤ) (α : X → ℤ) (β : Y → ℤ) (i : X) :
    ∑ j, (a0 + α i + β j) = Fintype.card Y * a0 + Fintype.card Y * α i + ∑ j, β j := by
  simp [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ]
  ring

/-- Sum of a matrix in normal form along a column. -/
theorem col_sum_nf (a0 : ℤ) (α : X → ℤ) (β : Y → ℤ) (j : Y) :
    ∑ i, (a0 + α i + β j) = Fintype.card X * a0 + ∑ i, α i + Fintype.card X * β j := by
  simp [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ]

/-- **Lemma 3** for a matrix: an additive matrix of nonnegative integers whose row sums are not all
equal and whose column sums are not all equal has total at least `|X| + |Y|`. -/
theorem lemma3_matrix [Nonempty X] [Nonempty Y] (N : X → Y → ℤ) (hadd : Add2 N)
    (hnn : ∀ i j, 0 ≤ N i j) (hrow : ¬ ∀ i i', ∑ j, N i j = ∑ j, N i' j)
    (hcol : ¬ ∀ j j', ∑ i, N i j = ∑ i, N i j') :
    (Fintype.card X : ℤ) + Fintype.card Y ≤ ∑ i, ∑ j, N i j := by
  obtain ⟨a0, α, β, ha0, hα, hβ, -, -, hN⟩ := normal_form N hadd hnn
  have hp : (0 : ℤ) ≤ Fintype.card X := by positivity
  have hq : (0 : ℤ) ≤ Fintype.card Y := by positivity
  -- some α is positive
  have hα1 : 1 ≤ ∑ i, α i := by
    by_contra hlt
    have hz : ∑ i, α i = 0 := le_antisymm (by linarith) (Finset.sum_nonneg (fun i _ => hα i))
    have hall : ∀ i, α i = 0 := fun i =>
      (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => hα i)).mp hz i (mem_univ _)
    apply hrow
    intro i i'
    simp only [hN, hall]
  have hβ1 : 1 ≤ ∑ j, β j := by
    by_contra hlt
    have hz : ∑ j, β j = 0 := le_antisymm (by linarith) (Finset.sum_nonneg (fun j _ => hβ j))
    have hall : ∀ j, β j = 0 := fun j =>
      (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hβ j)).mp hz j (mem_univ _)
    apply hcol
    intro j j'
    simp only [hN, hall]
  have htot : ∑ i, ∑ j, N i j
      = Fintype.card X * (Fintype.card Y * a0) + Fintype.card Y * ∑ i, α i
        + Fintype.card X * ∑ j, β j := by
    simp only [hN, row_sum_nf]
    simp [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Finset.mul_sum]
  rw [htot]
  nlinarith [mul_nonneg hp (mul_nonneg hq ha0)]

/-! ### Basic facts about 0/1 arrays -/

theorem a_nonneg (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (i : X) (j : Y)
    (k : Z) : 0 ≤ a i j k := by
  rcases h01 i j k with h | h <;> simp [h]

theorem a_le_one (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (i : X) (j : Y)
    (k : Z) : a i j k ≤ 1 := by
  rcases h01 i j k with h | h <;> simp [h]

theorem N2_nonneg (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (i : X) (j : Y) :
    0 ≤ N2 a i j :=
  Finset.sum_nonneg (fun k _ => a_nonneg a h01 i j k)

theorem N2_le (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (i : X) (j : Y) :
    N2 a i j ≤ Fintype.card Z := by
  calc N2 a i j ≤ ∑ _k : Z, (1 : ℤ) := Finset.sum_le_sum (fun k _ => a_le_one a h01 i j k)
    _ = Fintype.card Z := by simp

theorem N1_nonneg (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (i : X) :
    0 ≤ N1 a i :=
  Finset.sum_nonneg (fun j _ => N2_nonneg a h01 i j)

theorem N1_le (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (i : X) :
    N1 a i ≤ Fintype.card Y * Fintype.card Z := by
  calc N1 a i ≤ ∑ _j : Y, (Fintype.card Z : ℤ) := Finset.sum_le_sum (fun j _ => N2_le a h01 i j)
    _ = Fintype.card Y * Fintype.card Z := by simp

/-- if the counts along the first coordinate are constant, each is `total / |X|` -/
theorem Fx_mul (a : X → Y → Z → ℤ) (hF : Fx a) (i : X) :
    (Fintype.card X : ℤ) * N1 a i = total a := by
  have : total a = ∑ _i' : X, N1 a i := Finset.sum_congr rfl (fun i' _ => hF i' i)
  rw [this]; simp

theorem Fy_mul (a : X → Y → Z → ℤ) (hF : Fy a) (j : Y) :
    (Fintype.card Y : ℤ) * N1 (fun j i k => a i j k) j = total a := by
  have := Fx_mul (swapXY a) hF j
  rw [total_swapXY] at this
  exact this

theorem Fz_mul (a : X → Y → Z → ℤ) (hF : Fz a) (k : Z) :
    (Fintype.card Z : ℤ) * N1 (fun k i j => a i j k) k = total a := by
  have := Fx_mul (swapXY (swapYZ a)) hF k
  rw [total_swapXY, total_swapYZ] at this
  exact this

/-! ### The counting lemmas -/

/-- **Lemma 3**: if the `xy`-counts are additive and neither the `x`-counts nor the `y`-counts are
constant, the set has at least `|X| + |Y|` elements. -/
theorem lemma3 [Nonempty X] [Nonempty Y] (a : X → Y → Z → ℤ)
    (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (hxy : Fxy a) (hx : ¬ Fx a) (hy : ¬ Fy a) :
    (Fintype.card X : ℤ) + Fintype.card Y ≤ total a :=
  lemma3_matrix (N2 a) hxy (N2_nonneg a h01) hx hy

/-- **Lemma 4(c)**: if all third mixed differences vanish and some slice is empty, the `xy`-counts
are additive. -/
theorem lemma4c (a : X → Y → Z → ℤ) (hF3 : F3 a) (k0 : Z) (hk0 : ∀ i j, a i j k0 = 0) : Fxy a := by
  intro i i' j j'
  unfold N2
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro k _
  have := hF3 i i' j j' k k0
  simp only [hk0] at this
  linarith

/-- **Lemma 5** (in the form used): if all third mixed differences vanish, every `x`-count is `|Y|`
and every `y`-count is `|X|`, then every `xy`-count is 1. -/
theorem lemma5 [Nonempty Z] (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1)
    (hF3 : F3 a) (hrow : ∀ i, N1 a i = Fintype.card Y)
    (hcol : ∀ j, N1 (fun j i k => a i j k) j = Fintype.card X)
    (hcop : Nat.Coprime (Fintype.card Z) (Fintype.card X * Fintype.card Y))
    (hZ : 2 ≤ Fintype.card Z) : ∀ i j, N2 a i j = 1 := by
  obtain ⟨k0⟩ := ‹Nonempty Z›
  have hdvd : ∀ i i' j j',
      (Fintype.card Z : ℤ) ∣ N2 a i j + N2 a i' j' - N2 a i j' - N2 a i' j := by
    intro i i' j j'
    have : N2 a i j + N2 a i' j' - N2 a i j' - N2 a i' j
        = ∑ _k : Z, (a i j k0 + a i' j' k0 - a i j' k0 - a i' j k0) := by
      unfold N2
      rw [← Finset.sum_add_distrib, ← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro k _
      have := hF3 i i' j j' k k0
      linarith
    rw [this, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    exact dvd_mul_right _ _
  intro i j
  have e1 : ∀ i', ∑ j', N2 a i' j' = N1 a i' := fun _ => rfl
  have e2 : ∀ j', ∑ i', N2 a i' j' = N1 (fun j i k => a i j k) j' := fun _ => rfl
  have etot : ∑ i', N1 a i' = (Fintype.card X : ℤ) * Fintype.card Y := by
    simp [hrow]
  have hsum : ∑ i', ∑ j', (N2 a i j + N2 a i' j' - N2 a i j' - N2 a i' j)
      = (Fintype.card X : ℤ) * Fintype.card Y * (N2 a i j - 1) := by
    have h1 : ∀ i', ∑ j', (N2 a i j + N2 a i' j' - N2 a i j' - N2 a i' j)
        = Fintype.card Y * N2 a i j + N1 a i' - N1 a i - Fintype.card Y * N2 a i' j := by
      intro i'
      simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
        nsmul_eq_mul, e1]
    simp only [h1, Finset.sum_sub_distrib, Finset.sum_add_distrib, Finset.sum_const,
      Finset.card_univ, nsmul_eq_mul, ← Finset.mul_sum, e2, hrow, hcol]
    ring
  have h2 : (Fintype.card Z : ℤ) ∣ (N2 a i j - 1) * ((Fintype.card X : ℤ) * Fintype.card Y) := by
    rw [mul_comm, ← hsum]
    exact Finset.dvd_sum (fun i' _ => Finset.dvd_sum (fun j' _ => hdvd i i' j j'))
  have hcop' : IsCoprime (Fintype.card Z : ℤ) ((Fintype.card X : ℤ) * Fintype.card Y) := by
    have := Nat.isCoprime_iff_coprime.mpr hcop
    simpa using this
  have h3 : (Fintype.card Z : ℤ) ∣ N2 a i j - 1 := hcop'.dvd_of_dvd_mul_right h2
  have h4 := N2_nonneg a h01 i j
  have h5 := N2_le a h01 i j
  have hZ' : (2 : ℤ) ≤ Fintype.card Z := by exact_mod_cast hZ
  have h6 : N2 a i j - 1 = 0 :=
    Int.eq_zero_of_abs_lt_dvd h3 (abs_lt.mpr ⟨by linarith, by linarith⟩)
  linarith

/-- **Lemma 6(a)**: if the `xy`-counts and the `yz`-counts are additive and the `y`-counts are not
constant, then the `x`-counts and the `z`-counts are constant. -/
theorem lemma6a [Nonempty X] [Nonempty Y] [Nonempty Z] (a : X → Y → Z → ℤ)
    (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (hxy : Fxy a) (hyz : Fyz a) (hy : ¬ Fy a)
    (hcop : Nat.Coprime (Fintype.card X) (Fintype.card Z)) : Fx a ∧ Fz a := by
  obtain ⟨a0, α, β, ha0, hα, hβ, ⟨i1, hi1⟩, ⟨j1, hj1⟩, hN⟩ :=
    normal_form (N2 a) hxy (N2_nonneg a h01)
  have h01' : ∀ (j : Y) (k : Z) (i : X), (fun j k i => a i j k) j k i = 0
      ∨ (fun j k i => a i j k) j k i = 1 := fun j k i => h01 i j k
  obtain ⟨b0, α', β', hb0, hα', hβ', ⟨j2, hj2⟩, ⟨k2, hk2⟩, hN'⟩ :=
    normal_form (N2 (fun j k i => a i j k)) hyz (N2_nonneg _ h01')
  have hp0 : (0 : ℤ) < Fintype.card X := by exact_mod_cast Fintype.card_pos
  have hr0 : (0 : ℤ) < Fintype.card Z := by exact_mod_cast Fintype.card_pos
  -- the y-counts computed from the two normal forms
  have hNy1 : ∀ j, N1 (fun j i k => a i j k) j
      = Fintype.card X * a0 + ∑ i, α i + Fintype.card X * β j := by
    intro j
    have : N1 (fun j i k => a i j k) j = ∑ i, N2 a i j := rfl
    rw [this]; simp only [hN]; exact col_sum_nf a0 α β j
  have hNy2 : ∀ j, N1 (fun j i k => a i j k) j
      = Fintype.card Z * b0 + Fintype.card Z * α' j + ∑ k, β' k := by
    intro j
    have : N1 (fun j i k => a i j k) j = ∑ k, N2 (fun j k i => a i j k) j k := by
      unfold N1 N2; exact Finset.sum_comm
    rw [this]; simp only [hN']; exact row_sum_nf b0 α' β' j
  -- p β j = r α' j
  have key : ∀ j j', (Fintype.card X : ℤ) * β j - Fintype.card Z * α' j
      = Fintype.card X * β j' - Fintype.card Z * α' j' := by
    intro j j'
    have h1 := hNy1 j; have h2 := hNy2 j; have h3 := hNy1 j'; have h4 := hNy2 j'
    linarith
  have hc : ∀ j, (Fintype.card X : ℤ) * β j = Fintype.card Z * α' j := by
    intro j
    have h1 := key j j1
    have h2 := key j j2
    rw [hj1] at h1; rw [hj2] at h2
    nlinarith [mul_nonneg hr0.le (hα' j1), mul_nonneg hp0.le (hβ j2)]
  -- some β is positive
  obtain ⟨js, hjs⟩ : ∃ j, β j ≠ 0 := by
    by_contra hcon
    push Not at hcon
    apply hy
    intro j j'
    rw [hNy1, hNy1, hcon j, hcon j']
  have hβs : 1 ≤ β js := by have := hβ js; omega
  have hdvd : (Fintype.card Z : ℤ) ∣ β js := by
    have h1 : (Fintype.card Z : ℤ) ∣ β js * Fintype.card X := ⟨α' js, by rw [mul_comm]; exact hc js⟩
    have hcop' : IsCoprime (Fintype.card Z : ℤ) (Fintype.card X : ℤ) :=
      Nat.isCoprime_iff_coprime.mpr hcop.symm
    exact hcop'.dvd_of_dvd_mul_right h1
  have hβr : (Fintype.card Z : ℤ) ≤ β js := Int.le_of_dvd (by linarith) hdvd
  have hsmall : ∀ i, a0 + α i ≤ 0 := by
    intro i
    have h1 := N2_le a h01 i js
    rw [hN] at h1
    linarith
  have hα0 : ∀ i, α i = 0 := fun i => by have := hsmall i; have := hα i; linarith
  have hα'p : (Fintype.card X : ℤ) ≤ α' js := by
    have h1 := hc js
    by_contra hlt
    push Not at hlt
    nlinarith
  have hsmall' : ∀ k, b0 + β' k ≤ 0 := by
    intro k
    have h1 := N2_le (fun j k i => a i j k) h01' js k
    rw [hN'] at h1
    linarith
  have hβ'0 : ∀ k, β' k = 0 := fun k => by have := hsmall' k; have := hβ' k; linarith
  constructor
  · intro i i'
    have e : ∀ i, N1 a i = ∑ j, N2 a i j := fun _ => rfl
    rw [e, e]; simp only [hN, hα0]
  · intro k k'
    have e : ∀ k, N1 (fun k i j => a i j k) k = ∑ j, N2 (fun j k i => a i j k) j k := by
      intro k; unfold N1 N2; exact Finset.sum_comm
    rw [e, e]; simp only [hN', hβ'0]

/-- (I6) An additive matrix of zeros and ones depends on one index only. -/
theorem add2_zero_one {Y Z : Type*} (S : Y → Z → ℤ) (h01 : ∀ j k, S j k = 0 ∨ S j k = 1)
    (hadd : Add2 S) : (∀ j j' k, S j k = S j' k) ∨ (∀ j k k', S j k = S j k') := by
  by_contra hcon
  push Not at hcon
  obtain ⟨⟨j, j', k, h1⟩, ⟨j2, k2, k2', h2⟩⟩ := hcon
  have e1 := hadd j j' k k2
  have e2 := hadd j j' k k2'
  have e3 := hadd j2 j k2 k2'
  have v1 := h01 j k; have v2 := h01 j' k; have v3 := h01 j k2; have v4 := h01 j' k2
  have v5 := h01 j k2'; have v6 := h01 j' k2'; have v7 := h01 j2 k2; have v8 := h01 j2 k2'
  omega

/-- **Lemma 6(b)**: if the `x`-counts are constant, the `yz`-counts additive and all third mixed
differences vanish, then the `y`-counts or the `z`-counts are constant. -/
theorem lemma6b [Nonempty X] [Nonempty Y] [Nonempty Z] (a : X → Y → Z → ℤ)
    (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (hx : Fx a) (hyz : Fyz a) (hF3 : F3 a)
    (hcop : Nat.Coprime (Fintype.card Y) (Fintype.card Z)) : Fy a ∨ Fz a := by
  have hp0 : (0 : ℤ) < Fintype.card X := by exact_mod_cast Fintype.card_pos
  -- every slice is additive
  have hslice : ∀ i, Add2 (fun j k => a i j k) := by
    intro i j j' k k'
    have hsum : ∑ _i' : X, (a i j k + a i j' k' - a i j k' - a i j' k) = 0 := by
      have h := hyz j j' k k'
      simp only [N2] at h
      have : ∑ _i' : X, (a i j k + a i j' k' - a i j k' - a i j' k)
          = ∑ i' : X, (a i' j k + a i' j' k' - a i' j k' - a i' j' k) := by
        apply Finset.sum_congr rfl
        intro i' _
        have := hF3 i i' j j' k k'
        linarith
      rw [this, Finset.sum_sub_distrib, Finset.sum_sub_distrib, Finset.sum_add_distrib]
      linarith
    rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul] at hsum
    have := (mul_eq_zero.mp hsum).resolve_left hp0.ne'
    show a i j k + a i j' k' = a i j k' + a i j' k
    linarith
  have hdich : ∀ i, (∀ j j' k, a i j k = a i j' k) ∨ (∀ j k k', a i j k = a i j k') :=
    fun i => add2_zero_one (fun j k => a i j k) (fun j k => h01 i j k) (hslice i)
  by_cases hA : ∀ i, ∀ j j' k, a i j k = a i j' k
  · left
    intro j j'
    unfold N1
    exact Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun k _ => hA i j j' k))
  by_cases hB : ∀ i, ∀ j k k', a i j k = a i j k'
  · right
    intro k k'
    unfold N1
    exact Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => hB i j k k'))
  exfalso
  push Not at hA hB
  obtain ⟨i1, hi1⟩ := hA
  obtain ⟨i2, hi2⟩ := hB
  have hz1 : ∀ j k k', a i1 j k = a i1 j k' :=
    (hdich i1).resolve_left (by push Not; exact hi1)
  have hy2 : ∀ j j' k, a i2 j k = a i2 j' k :=
    (hdich i2).resolve_right (by push Not; exact hi2)
  obtain ⟨j0⟩ := ‹Nonempty Y›
  obtain ⟨k0⟩ := ‹Nonempty Z›
  have hs1 : N1 a i1 = Fintype.card Z * ∑ j, a i1 j k0 := by
    unfold N1
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro j _
    rw [Finset.sum_congr rfl (fun k _ => hz1 j k k0)]
    simp
  have hs2 : N1 a i2 = Fintype.card Y * ∑ k, a i2 j0 k := by
    unfold N1
    rw [Finset.sum_comm, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro k _
    rw [Finset.sum_congr rfl (fun j _ => hy2 j j0 k)]
    simp
  have hs : N1 a i1 = N1 a i2 := hx i1 i2
  have hd1 : (Fintype.card Z : ℤ) ∣ N1 a i1 := ⟨_, hs1⟩
  have hd2 : (Fintype.card Y : ℤ) ∣ N1 a i1 := by rw [hs]; exact ⟨_, hs2⟩
  have hcop' : IsCoprime (Fintype.card Y : ℤ) (Fintype.card Z : ℤ) :=
    Nat.isCoprime_iff_coprime.mpr hcop
  have hd : (Fintype.card Y : ℤ) * Fintype.card Z ∣ N1 a i1 := hcop'.mul_dvd hd2 hd1
  have h0 := N1_nonneg a h01 i1
  have hle := N1_le a h01 i1
  rcases eq_or_lt_of_le h0 with hzero | hpos
  · have hall : ∀ j k, a i1 j k = 0 := by
      intro j k
      have h1 : ∑ j, N2 a i1 j = 0 := hzero.symm
      have h2 := (Finset.sum_eq_zero_iff_of_nonneg
        (fun j _ => N2_nonneg a h01 i1 j)).mp h1 j (mem_univ _)
      exact (Finset.sum_eq_zero_iff_of_nonneg
        (fun k _ => a_nonneg a h01 i1 j k)).mp h2 k (mem_univ _)
    obtain ⟨j, j', k, hne⟩ := hi1
    exact hne (by rw [hall, hall])
  · have hge : (Fintype.card Y : ℤ) * Fintype.card Z ≤ N1 a i1 := Int.le_of_dvd hpos hd
    have heq : N1 a i1 = Fintype.card Y * Fintype.card Z := le_antisymm hle hge
    have hall : ∀ j k, a i1 j k = 1 := by
      intro j k
      have h1 : ∑ j, ∑ k, (1 - a i1 j k) = 0 := by
        have e : ∑ j, ∑ k, a i1 j k = N1 a i1 := rfl
        simp only [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, e, heq]
        ring
      have h2 := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => Finset.sum_nonneg
        (fun k _ => by have := a_le_one a h01 i1 j k; linarith))).mp h1 j (mem_univ _)
      have h3 := (Finset.sum_eq_zero_iff_of_nonneg
        (fun k _ => by have := a_le_one a h01 i1 j k; linarith)).mp h2 k (mem_univ _)
      linarith
    obtain ⟨j, j', k, hne⟩ := hi1
    exact hne (by rw [hall, hall])

/-! ### Small facts used in the case analysis -/

theorem total_le (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) :
    total a ≤ Fintype.card X * (Fintype.card Y * Fintype.card Z) := by
  calc total a ≤ ∑ _i : X, ((Fintype.card Y : ℤ) * Fintype.card Z) :=
        Finset.sum_le_sum (fun i _ => N1_le a h01 i)
    _ = Fintype.card X * (Fintype.card Y * Fintype.card Z) := by simp

theorem all_one_of_total (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1)
    (h : total a = Fintype.card X * (Fintype.card Y * Fintype.card Z)) : ∀ i j k, a i j k = 1 := by
  intro i j k
  have h1 : ∑ i, ∑ j, ∑ k, (1 - a i j k) = 0 := by
    have e : ∑ i, ∑ j, ∑ k, a i j k = total a := rfl
    simp only [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, e, h]
    ring
  have nn : ∀ i j k, 0 ≤ 1 - a i j k := fun i j k => by have := a_le_one a h01 i j k; linarith
  have h2 := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => Finset.sum_nonneg
    (fun j _ => Finset.sum_nonneg (fun k _ => nn i j k)))).mp h1 i (mem_univ _)
  have h3 := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => Finset.sum_nonneg
    (fun k _ => nn i j k))).mp h2 j (mem_univ _)
  have h4 := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => nn i j k)).mp h3 k (mem_univ _)
  linarith

/-- nonnegative integers indexed by `X` with sum less than `|X|`: one of them is zero -/
theorem exists_zero_of_sum_lt (c : X → ℤ) (hc : ∀ i, 0 ≤ c i) (h : ∑ i, c i < Fintype.card X) :
    ∃ i, c i = 0 := by
  by_contra hcon
  push Not at hcon
  have h1 : ∀ i, 1 ≤ c i := fun i => by have := hc i; have := hcon i; omega
  have : (Fintype.card X : ℤ) ≤ ∑ i, c i := by
    calc (Fintype.card X : ℤ) = ∑ _i : X, (1 : ℤ) := by simp
      _ ≤ ∑ i, c i := Finset.sum_le_sum (fun i _ => h1 i)
  linarith

/-- if the set has fewer elements than `|X|`, some slice along the first coordinate is empty -/
theorem exists_empty_slice (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1)
    (h : total a < Fintype.card X) : ∃ i, ∀ j k, a i j k = 0 := by
  obtain ⟨i, hi⟩ := exists_zero_of_sum_lt (N1 a) (N1_nonneg a h01) h
  refine ⟨i, fun j k => ?_⟩
  have h2 := (Finset.sum_eq_zero_iff_of_nonneg
    (fun j _ => N2_nonneg a h01 i j)).mp hi j (mem_univ _)
  exact (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => a_nonneg a h01 i j k)).mp h2 k (mem_univ _)

theorem card_ne_of_coprime {m n : ℕ} (hm : 2 ≤ m) (h : Nat.Coprime m n) : m ≠ n := by
  rintro rfl
  have := Nat.coprime_self m |>.mp h
  omega

/-! ### The four cases of Section 5 -/

/-- `|E| = 3` -/
theorem case3 [Nonempty X] [Nonempty Y] [Nonempty Z] (a : X → Y → Z → ℤ)
    (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (hpos : 0 < total a)
    (cxy : Nat.Coprime (Fintype.card X) (Fintype.card Y))
    (cxz : Nat.Coprime (Fintype.card X) (Fintype.card Z))
    (cyz : Nat.Coprime (Fintype.card Y) (Fintype.card Z))
    (hx : Fx a) (hy : Fy a) (hz : Fz a) : ∀ i j k, a i j k = 1 := by
  obtain ⟨i0⟩ := ‹Nonempty X›
  obtain ⟨j0⟩ := ‹Nonempty Y›
  obtain ⟨k0⟩ := ‹Nonempty Z›
  have hdx : (Fintype.card X : ℤ) ∣ total a := ⟨N1 a i0, (Fx_mul a hx i0).symm⟩
  have hdy : (Fintype.card Y : ℤ) ∣ total a := ⟨_, (Fy_mul a hy j0).symm⟩
  have hdz : (Fintype.card Z : ℤ) ∣ total a := ⟨_, (Fz_mul a hz k0).symm⟩
  have c1 : IsCoprime (Fintype.card Y : ℤ) (Fintype.card Z : ℤ) := Nat.isCoprime_iff_coprime.mpr cyz
  have c2 : IsCoprime (Fintype.card X : ℤ) (Fintype.card Y : ℤ) := Nat.isCoprime_iff_coprime.mpr cxy
  have c3 : IsCoprime (Fintype.card X : ℤ) (Fintype.card Z : ℤ) := Nat.isCoprime_iff_coprime.mpr cxz
  have hd1 : (Fintype.card Y : ℤ) * Fintype.card Z ∣ total a := c1.mul_dvd hdy hdz
  have hd : (Fintype.card X : ℤ) * (Fintype.card Y * Fintype.card Z) ∣ total a :=
    (c2.mul_right c3).mul_dvd hdx hd1
  exact all_one_of_total a h01 (le_antisymm (total_le a h01) (Int.le_of_dvd hpos hd))

/-- `E = {x, y}` -/
theorem case2 [Nonempty X] [Nonempty Y] [Nonempty Z] (a : X → Y → Z → ℤ)
    (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (hpos : 0 < total a)
    (hX : 2 ≤ Fintype.card X) (hY : 2 ≤ Fintype.card Y) (hZ : 2 ≤ Fintype.card Z)
    (cxy : Nat.Coprime (Fintype.card X) (Fintype.card Y))
    (cxz : Nat.Coprime (Fintype.card X) (Fintype.card Z))
    (cyz : Nat.Coprime (Fintype.card Y) (Fintype.card Z))
    (B : Bounds a) (hx : Fx a) (hy : Fy a) (hz : ¬ Fz a) : ∀ i j, N2 a i j = 1 := by
  obtain ⟨i0⟩ := ‹Nonempty X›
  obtain ⟨j0⟩ := ‹Nonempty Y›
  have hX' : (2 : ℤ) ≤ Fintype.card X := by exact_mod_cast hX
  have hY' : (2 : ℤ) ≤ Fintype.card Y := by exact_mod_cast hY
  have hn_le := B.bxy hz
  have hdx : (Fintype.card X : ℤ) ∣ total a := ⟨N1 a i0, (Fx_mul a hx i0).symm⟩
  have hdy : (Fintype.card Y : ℤ) ∣ total a := ⟨_, (Fy_mul a hy j0).symm⟩
  have hd : (Fintype.card X : ℤ) * Fintype.card Y ∣ total a :=
    (Nat.isCoprime_iff_coprime.mpr cxy).mul_dvd hdx hdy
  have hn : total a = Fintype.card X * Fintype.card Y :=
    le_antisymm hn_le (Int.le_of_dvd hpos hd)
  have hrow : ∀ i, N1 a i = Fintype.card Y := by
    intro i
    have := Fx_mul a hx i
    rw [hn] at this
    exact mul_left_cancel₀ (by linarith : (Fintype.card X : ℤ) ≠ 0) this
  have hcol : ∀ j, N1 (fun j i k => a i j k) j = Fintype.card X := by
    intro j
    have := Fy_mul a hy j
    rw [hn, mul_comm (Fintype.card X : ℤ)] at this
    exact mul_left_cancel₀ (by linarith : (Fintype.card Y : ℤ) ≠ 0) this
  by_cases h3 : F3 a
  · exact lemma5 a h01 h3 hrow hcol (Nat.Coprime.mul_right cxz.symm cyz.symm) hZ
  · have hxy : Fxy a := by
      by_contra hxy
      have h := B.cxy hxy hz h3
      rw [Nat.cast_max] at h
      rcases le_max_iff.mp h with h | h <;> nlinarith
    intro i j
    have e1 : ∀ i', ∑ j', N2 a i' j' = N1 a i' := fun _ => rfl
    have e2 : ∀ j', ∑ i', N2 a i' j' = N1 (fun j i k => a i j k) j' := fun _ => rfl
    have hsum : ∑ i', ∑ j', (N2 a i j + N2 a i' j') = ∑ i', ∑ j', (N2 a i j' + N2 a i' j) :=
      Finset.sum_congr rfl (fun i' _ => Finset.sum_congr rfl (fun j' _ => hxy i i' j j'))
    simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul, e1,
      hrow] at hsum
    rw [← Finset.mul_sum, e2, hcol] at hsum
    have h5 : (Fintype.card X : ℤ) * Fintype.card Y * (N2 a i j - 1) = 0 := by linarith
    rcases mul_eq_zero.mp h5 with h | h
    · exfalso
      have : (0 : ℤ) < Fintype.card X * Fintype.card Y := by positivity
      linarith
    · linarith

/-- `E = {x}` -/
theorem case1 [Nonempty X] [Nonempty Y] [Nonempty Z] (a : X → Y → Z → ℤ)
    (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (hpos : 0 < total a)
    (hX : 2 ≤ Fintype.card X) (hY : 2 ≤ Fintype.card Y) (hZ : 2 ≤ Fintype.card Z)
    (cxy : Nat.Coprime (Fintype.card X) (Fintype.card Y))
    (cxz : Nat.Coprime (Fintype.card X) (Fintype.card Z))
    (cyz : Nat.Coprime (Fintype.card Y) (Fintype.card Z))
    (B : Bounds a) (hx : Fx a) (hy : ¬ Fy a) (hz : ¬ Fz a) : ∀ i, N1 a i = 1 := by
  obtain ⟨i0⟩ := ‹Nonempty X›
  have hX' : (2 : ℤ) ≤ Fintype.card X := by exact_mod_cast hX
  have hY' : (2 : ℤ) ≤ Fintype.card Y := by exact_mod_cast hY
  have hZ' : (2 : ℤ) ≤ Fintype.card Z := by exact_mod_cast hZ
  have hdx : (Fintype.card X : ℤ) ∣ total a := ⟨N1 a i0, (Fx_mul a hx i0).symm⟩
  have hge : (Fintype.card X : ℤ) ≤ total a := Int.le_of_dvd hpos hdx
  have key : total a = Fintype.card X := by
    apply le_antisymm _ hge
    by_cases hyz : Fyz a
    · have nxy : ¬ Fxy a := fun hxy => hz (lemma6a a h01 hxy hyz hy cxz).2
      have nxz : ¬ Fxz a := by
        intro hxz
        have := lemma6a (swapYZ a) (fun i k j => h01 i j k) hxz ((Fyz_swapYZ a).mpr hyz) hz cxy
        exact hy this.2
      have n3 : ¬ F3 a := fun h3 => (lemma6b a h01 hx hyz h3 cyz).elim hy hz
      have h1 := B.cxy nxy hz n3
      have h2 := B.cxz nxz hy n3
      rw [Nat.cast_max] at h1 h2
      by_contra hgt
      push Not at hgt
      have h1' : total a ≤ Fintype.card Y := by
        rcases le_max_iff.mp h1 with h | h
        · exfalso; linarith
        · exact h
      have h3 := lemma3 (swapYZ (swapXY a)) (fun j k i => h01 i j k) hyz
        (fun h => hy ((Fx_swapXY a).mp ((Fx_swapYZ (swapXY a)).mp h)))
        (fun h => hz ((Fz_swapXY a).mp h))
      rw [total_swapYZ, total_swapXY] at h3
      linarith
    · exact B.bx hy hz hyz
  intro i
  have := Fx_mul a hx i
  rw [key] at this
  exact mul_left_cancel₀ (by linarith : (Fintype.card X : ℤ) ≠ 0) (by rw [this, mul_one])

/-- `E = ∅` -/
theorem case0 [Nonempty X] [Nonempty Y] [Nonempty Z] (a : X → Y → Z → ℤ)
    (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1) (hpos : 0 < total a)
    (hX : 2 ≤ Fintype.card X) (hY : 2 ≤ Fintype.card Y) (hZ : 2 ≤ Fintype.card Z)
    (cxy : Nat.Coprime (Fintype.card X) (Fintype.card Y))
    (cxz : Nat.Coprime (Fintype.card X) (Fintype.card Z))
    (cyz : Nat.Coprime (Fintype.card Y) (Fintype.card Z))
    (B : Bounds a) (hx : ¬ Fx a) (hy : ¬ Fy a) (hz : ¬ Fz a) : total a = 1 := by
  have hX' : (2 : ℤ) ≤ Fintype.card X := by exact_mod_cast hX
  have hY' : (2 : ℤ) ≤ Fintype.card Y := by exact_mod_cast hY
  have hZ' : (2 : ℤ) ≤ Fintype.card Z := by exact_mod_cast hZ
  have h_xy_yz : ¬ (Fxy a ∧ Fyz a) := fun ⟨h1, h2⟩ => hx (lemma6a a h01 h1 h2 hy cxz).1
  have h_xy_xz : ¬ (Fxy a ∧ Fxz a) := by
    rintro ⟨h1, h2⟩
    have := lemma6a (swapXY a) (fun j i k => h01 i j k) ((Fxy_swapXY a).mpr h1) h2 hx cyz
    exact hy this.1
  have h_xz_yz : ¬ (Fxz a ∧ Fyz a) := by
    rintro ⟨h1, h2⟩
    have := lemma6a (swapYZ a) (fun i k j => h01 i j k) h1 ((Fyz_swapYZ a).mpr h2) hz cxy
    exact hx ((Fx_swapYZ a).mp this.1)
  by_cases hxy : Fxy a
  · exfalso
    have hyz : ¬ Fyz a := fun h => h_xy_yz ⟨hxy, h⟩
    have h1 := B.bx hy hz hyz
    have h2 := lemma3 a h01 hxy hx hy
    linarith
  by_cases hxz : Fxz a
  · exfalso
    have hyz : ¬ Fyz a := fun h => h_xz_yz ⟨hxz, h⟩
    have h1 := B.bx hy hz hyz
    have h2 := lemma3 (swapYZ a) (fun i k j => h01 i j k) hxz
      (fun h => hx ((Fx_swapYZ a).mp h)) hz
    rw [total_swapYZ] at h2
    linarith
  by_cases hyz : Fyz a
  · exfalso
    have h1 := B.by' hx hz hxz
    have h2 := lemma3 (swapYZ (swapXY a)) (fun j k i => h01 i j k) hyz
      (fun h => hy ((Fx_swapXY a).mp ((Fx_swapYZ (swapXY a)).mp h)))
      (fun h => hz ((Fz_swapXY a).mp h))
    rw [total_swapYZ, total_swapXY] at h2
    linarith
  by_cases h3 : F3 a
  · exfalso
    rcases lt_or_gt_of_ne (card_ne_of_coprime hX cxz) with hlt | hgt
    · -- |X| < |Z|: an empty slice along z
      have h1 := B.bx hy hz hyz
      have hlt' : total a < Fintype.card Z := by
        have : (Fintype.card X : ℤ) < Fintype.card Z := by exact_mod_cast hlt
        linarith
      have hlt'' : total (swapXY (swapYZ a)) < Fintype.card Z := by
        rw [total_swapXY, total_swapYZ]; exact hlt'
      obtain ⟨k0, hk0⟩ := exists_empty_slice (swapXY (swapYZ a)) (fun k i j => h01 i j k) hlt''
      exact hxy (lemma4c a h3 k0 (fun i j => hk0 i j))
    · -- |Z| < |X|: an empty slice along x
      have h1 := B.bz hx hy hxy
      have hlt' : total a < Fintype.card X := by
        have : (Fintype.card Z : ℤ) < Fintype.card X := by exact_mod_cast hgt
        linarith
      obtain ⟨i0, hi0⟩ := exists_empty_slice a h01 hlt'
      exact hyz (lemma4c (swapYZ (swapXY a))
        ((F3_swapYZ (swapXY a)).mpr ((F3_swapXY a).mpr h3)) i0 (fun j k => hi0 j k))
  · have := B.b0 hx hy hz hxy hxz hyz h3
    omega

/-! ### The theorem -/

/-- **Section 5.** A 0/1 array on a product of three finite sets of pairwise coprime sizes `≥ 2`
that satisfies the bounds is structured: for some set of coordinates, the projection of the set
to those coordinates is a bijection. -/
theorem structured_of_bounds (a : X → Y → Z → ℤ) (h01 : ∀ i j k, a i j k = 0 ∨ a i j k = 1)
    (hpos : 0 < total a)
    (hX : 2 ≤ Fintype.card X) (hY : 2 ≤ Fintype.card Y) (hZ : 2 ≤ Fintype.card Z)
    (cxy : Nat.Coprime (Fintype.card X) (Fintype.card Y))
    (cxz : Nat.Coprime (Fintype.card X) (Fintype.card Z))
    (cyz : Nat.Coprime (Fintype.card Y) (Fintype.card Z))
    (B : Bounds a) : Structured a := by
  have : Nonempty X := Fintype.card_pos_iff.mp (by omega)
  have : Nonempty Y := Fintype.card_pos_iff.mp (by omega)
  have : Nonempty Z := Fintype.card_pos_iff.mp (by omega)
  unfold Structured
  by_cases hx : Fx a <;> by_cases hy : Fy a <;> by_cases hz : Fz a
  · -- x, y, z
    exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr
      (case3 a h01 hpos cxy cxz cyz hx hy hz)))))))
  · -- x, y
    exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl
      (case2 a h01 hpos hX hY hZ cxy cxz cyz B hx hy hz)))))
  · -- x, z
    have := case2 (swapYZ a) (fun i k j => h01 i j k) (by rw [total_swapYZ]; exact hpos)
      hX hZ hY cxz cxy cyz.symm B.swapYZ ((Fx_swapYZ a).mpr hx) hz hy
    exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl this)))))
  · -- x
    exact Or.inr (Or.inl (case1 a h01 hpos hX hY hZ cxy cxz cyz B hx hy hz))
  · -- y, z
    have := case2 (swapYZ (swapXY a)) (fun j k i => h01 i j k)
      (by rw [total_swapYZ, total_swapXY]; exact hpos)
      hY hZ hX cyz cxy.symm cxz.symm B.swapXY.swapYZ
      ((Fx_swapYZ (swapXY a)).mpr hy) ((Fz_swapXY a).mpr hz) hx
    exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl this))))))
  · -- y
    have := case1 (swapXY a) (fun j i k => h01 i j k) (by rw [total_swapXY]; exact hpos)
      hY hX hZ cxy.symm cyz cxz B.swapXY hy hx (fun h => hz ((Fz_swapXY a).mp h))
    exact Or.inr (Or.inr (Or.inl this))
  · -- z
    have := case1 (swapXY (swapYZ a)) (fun k i j => h01 i j k)
      (by rw [total_swapXY, total_swapYZ]; exact hpos)
      hZ hX hY cxz.symm cyz.symm cxy B.swapYZ.swapXY hz
      (fun h => hx ((Fx_swapYZ a).mp h)) (fun h => hy ((Fz_swapXY (swapYZ a)).mp h))
    exact Or.inr (Or.inr (Or.inr (Or.inl this)))
  · -- none
    exact Or.inl (case0 a h01 hpos hX hY hZ cxy cxz cyz B hx hy hz)

end Pqr
