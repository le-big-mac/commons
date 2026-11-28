/-
Erdős's bound for the problem of Littlewood and Offord, for nonzero real numbers and for nonzero complex numbers:
a signed sum `∑ ± a i` of `m` nonzero numbers takes any one value for at most `C(m, ⌊m/2⌋)` of the `2^m` choices of
signs.  (Statements fixed on 28 November 2026, before any Lean proof of them.  A signing is `ε : ι → Bool`, `true`
is `+`; `sg` is from `Pnq/SignDefs.lean`.)
-/
import Mathlib
import Pnq.SignDefs

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

namespace OffordAux

/-- two Booleans that agree with one proposition in the same way are equal -/
theorem bool_eq_of_iff_iff {p : Prop} {b b' : Bool} (h : (b = true ↔ p) ↔ (b' = true ↔ p)) :
    b = b' := by
  by_cases hp : p <;> cases b <;> cases b' <;> simp_all

/-- one term: if the signed term of `b'` is positive whenever that of `b` is, the term of `b` is at most that
of `b'` (the signed term `sg b * x` is positive exactly when `b = true ↔ 0 < x`, for `x ≠ 0`) -/
theorem term_le (x : ℝ) (b b' : Bool) (h : (b = true ↔ 0 < x) → (b' = true ↔ 0 < x)) :
    (sg b : ℝ) * x ≤ (sg b' : ℝ) * x := by
  by_cases hp : 0 < x
  · cases b <;> cases b' <;> simp [sg, hp] at h ⊢
    linarith
  · have hn : x ≤ 0 := not_lt.mp hp
    cases b <;> cases b' <;> simp [sg, hp] at h ⊢
    linarith

/-- one term, strictly: if the signed term of `b'` is positive and that of `b` is not, and `x ≠ 0`, the term of
`b` is less than that of `b'` -/
theorem term_lt (x : ℝ) (b b' : Bool) (hx : x ≠ 0) (h' : b' = true ↔ 0 < x)
    (h : ¬ (b = true ↔ 0 < x)) : (sg b : ℝ) * x < (sg b' : ℝ) * x := by
  rcases lt_or_gt_of_ne hx with hneg | hpos
  · have hn : ¬ 0 < x := not_lt.mpr hneg.le
    cases b <;> cases b' <;> simp [sg, hn] at h h' ⊢
    linarith
  · cases b <;> cases b' <;> simp [sg, hpos] at h h' ⊢

/-- a real-linear form `z ↦ z.re - t * z.im` that vanishes at none of finitely many nonzero complex numbers -/
theorem exists_real_form {κ : Type*} [Finite κ] (a : κ → ℂ) (ha : ∀ i, a i ≠ 0) :
    ∃ t : ℝ, ∀ i, (a i).re - t * (a i).im ≠ 0 := by
  -- `t` outside the finite set of the quotients `re / im`
  obtain ⟨t, ht⟩ := (Set.finite_range fun i => (a i).re / (a i).im).exists_notMem
  refine ⟨t, fun i h => ?_⟩
  by_cases him : (a i).im = 0
  · apply ha i
    apply Complex.ext
    · simpa [him] using h
    · simpa using him
  · apply ht
    refine ⟨i, ?_⟩
    field_simp
    linarith

end OffordAux

open Classical in
/-- **Erdős's bound, real numbers.**  For nonzero real numbers `a i` and any real `v`, the signings `ε` with
`∑ i, sg (ε i) * a i = v` number at most `C(m, ⌊m/2⌋)`, where `m` is the number of the `a i`. -/
theorem card_signedSum_eq_le_real (a : ι → ℝ) (ha : ∀ i, a i ≠ 0) (v : ℝ) :
    (Finset.univ.filter fun ε : ι → Bool => ∑ i, (sg (ε i) : ℝ) * a i = v).card ≤
      (Fintype.card ι).choose (Fintype.card ι / 2) := by
  -- `F`: the signings with the value `v`; `A ε`: the set of the elements whose signed term is positive
  set F := Finset.univ.filter fun ε : ι → Bool => ∑ i, (sg (ε i) : ℝ) * a i = v
  let A : (ι → Bool) → Finset ι := fun ε => Finset.univ.filter fun i => (ε i = true ↔ 0 < a i)
  have hmem : ∀ ε i, i ∈ A ε ↔ (ε i = true ↔ 0 < a i) := by
    intro ε i
    simp only [A, Finset.mem_filter, Finset.mem_univ, true_and]
  have hAinj : Function.Injective A := by
    intro ε ε' h
    funext i
    have hi : i ∈ A ε ↔ i ∈ A ε' := by rw [h]
    rw [hmem, hmem] at hi
    exact OffordAux.bool_eq_of_iff_iff hi
  -- the sets `A ε`, `ε ∈ F`, form an antichain: a proper inclusion makes the signed sum strictly larger
  have hanti : IsAntichain (· ⊆ ·) (SetLike.coe (F.image A)) := by
    intro s hs s' hs' hne hsub
    rw [Finset.mem_coe, Finset.mem_image] at hs hs'
    obtain ⟨ε, hε, rfl⟩ := hs
    obtain ⟨ε', hε', rfl⟩ := hs'
    have h1 : ∑ i, (sg (ε i) : ℝ) * a i = v := (Finset.mem_filter.mp hε).2
    have h2 : ∑ i, (sg (ε' i) : ℝ) * a i = v := (Finset.mem_filter.mp hε').2
    have hlt : ∑ i, (sg (ε i) : ℝ) * a i < ∑ i, (sg (ε' i) : ℝ) * a i := by
      apply Finset.sum_lt_sum
      · intro i _
        apply OffordAux.term_le
        intro hi
        exact (hmem ε' i).mp (hsub ((hmem ε i).mpr hi))
      · obtain ⟨i, hi', hi⟩ := Finset.exists_of_ssubset (Finset.ssubset_iff_subset_ne.mpr ⟨hsub, hne⟩)
        exact ⟨i, Finset.mem_univ i,
          OffordAux.term_lt (a i) (ε i) (ε' i) (ha i) ((hmem ε' i).mp hi') (fun h => hi ((hmem ε i).mpr h))⟩
    linarith
  -- Sperner's theorem
  calc F.card = (F.image A).card := (Finset.card_image_of_injective F hAinj).symm
    _ ≤ (Fintype.card ι).choose (Fintype.card ι / 2) := hanti.sperner

open Classical in
/-- **The same bound for nonzero complex numbers.** -/
theorem card_signedSum_eq_le_complex (a : ι → ℂ) (ha : ∀ i, a i ≠ 0) (v : ℂ) :
    (Finset.univ.filter fun ε : ι → Bool => ∑ i, (sg (ε i) : ℂ) * a i = v).card ≤
      (Fintype.card ι).choose (Fintype.card ι / 2) := by
  -- a real-linear form `z ↦ z.re - t * z.im` that vanishes at no `a i`; the real case for its values
  obtain ⟨t, ht⟩ := OffordAux.exists_real_form a ha
  refine le_trans (Finset.card_le_card ?_)
    (card_signedSum_eq_le_real (fun i => (a i).re - t * (a i).im) ht (v.re - t * v.im))
  intro ε hε
  simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε ⊢
  have hre := congrArg Complex.re hε
  have him := congrArg Complex.im hε
  simp only [Complex.re_sum, Complex.im_sum, Complex.mul_re, Complex.mul_im, Complex.intCast_re,
    Complex.intCast_im, zero_mul, sub_zero, add_zero] at hre him
  rw [← hre, ← him, Finset.mul_sum, ← Finset.sum_sub_distrib]
  apply Finset.sum_congr rfl
  intro i _
  ring

end Pnq
