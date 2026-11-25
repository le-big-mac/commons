/-
The standard criterion for a tiling of `ZMod M` in terms of Fourier zeros: if `|A| · |B| = M` and every
divisor `d > 1` of `M` is a Fourier zero of `A` or of `B`, then `A ⊕ B = ZMod M`.
(Used to produce the tiling complement once (T1) and (T2) are known.)
-/
import Pqr.Main
import Pqr.SCBounds

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

/-- the transform of an indicator function is `hat` -/
theorem ft_indicator (B : Finset (ZMod M)) (ξ : ZMod M) :
    ft (fun w => if w ∈ B then (1 : ℝ) else 0) ξ = hat B ξ := by
  unfold ft hat
  have h : ∀ w : ZMod M, (((if w ∈ B then (1 : ℝ) else 0 : ℝ)) : ℂ) * ZMod.stdAddChar (ξ * w)
      = if w ∈ B then (ZMod.stdAddChar (ξ * w) : ℂ) else 0 := by
    intro w; split_ifs <;> simp
  simp only [h]
  rw [Finset.sum_ite_mem, Finset.univ_inter]

/-- under the hypotheses of the criterion, every `v` has exactly one representation, counted as a sum -/
theorem conv_indicator_eq_one (A B : Finset (ZMod M)) (hcard : A.card * B.card = M)
    (hz : ∀ d, d ∣ M → d ≠ 1 → ZeroAt A d ∨ ZeroAt B d) (v : ZMod M) :
    ∑ a ∈ A, (if v - a ∈ B then (1 : ℝ) else 0) = 1 := by
  have key : (fun v : ZMod M =>
      (∑ a ∈ A, (((if v - a ∈ B then (1 : ℝ) else 0 : ℝ)) : ℂ)) - 1) = 0 := by
    apply zmod_fourier_uniq
    intro ξ
    simp only [sub_mul, one_mul, Finset.sum_sub_distrib]
    rw [conv_ft A (fun w => if w ∈ B then (1 : ℝ) else 0) ξ, sum_stdAddChar_mul, ft_indicator]
    by_cases hξ : ξ = 0
    · subst hξ
      simp only [hat_zero, ite_true]
      have : ((A.card * B.card : ℕ) : ℂ) = (M : ℂ) := by rw [hcard]
      push_cast at this
      rw [this, sub_self]
    · simp only [hξ, ite_false, sub_zero]
      rcases hz (ord ξ) (ord_dvd ξ) (fun h => hξ ((ord_eq_one_iff ξ).mp h)) with h | h
      · rw [h ξ rfl, zero_mul]
      · rw [h ξ rfl, mul_zero]
  have h1 := congrFun key v
  simp only [Pi.zero_apply] at h1
  have h2 : ((∑ a ∈ A, (if v - a ∈ B then (1 : ℝ) else 0) : ℝ) : ℂ) = ((1 : ℝ) : ℂ) := by
    push_cast
    linear_combination h1
  exact_mod_cast h2

/-- **Tiling criterion.** If `|A| · |B| = M` and every divisor `d > 1` of `M` is a Fourier zero of `A` or
of `B`, then `A ⊕ B = ZMod M`. -/
theorem tiling_of_zeroAt (A B : Finset (ZMod M)) (hcard : A.card * B.card = M)
    (hz : ∀ d, d ∣ M → d ≠ 1 → ZeroAt A d ∨ ZeroAt B d) : IsTiling A B := by
  classical
  intro v
  have h := conv_indicator_eq_one A B hcard hz v
  rw [Finset.sum_boole] at h
  have hc : (A.filter (fun a => v - a ∈ B)).card = 1 := by exact_mod_cast h
  obtain ⟨a0, ha0⟩ := Finset.card_eq_one.mp hc
  have hm : a0 ∈ A.filter (fun a => v - a ∈ B) := by rw [ha0]; exact Finset.mem_singleton_self a0
  rw [Finset.mem_filter] at hm
  refine ⟨(a0, v - a0), ⟨hm.1, hm.2, by simp⟩, ?_⟩
  rintro ⟨a, b⟩ ⟨ha, hb, hab⟩
  simp only at ha hb hab
  have hb' : b = v - a := by rw [← hab]; abel
  have : a ∈ A.filter (fun a => v - a ∈ B) := by
    rw [Finset.mem_filter]; exact ⟨ha, by rw [← hb']; exact hb⟩
  rw [ha0, Finset.mem_singleton] at this
  subst this
  rw [hb']

end Pqr
