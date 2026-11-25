/-
A set that is invariant under translation by `h` has no Fourier mass at any order that does not divide `h`.
(agent3 / Yonder; used for Lemma 5 of the `p^2 q^2` theorem.)
-/
import Pqr.DigitSets
import Pqr.Bridge2

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

/-- If `a + h ∈ A` for every `a ∈ A`, then translation by `h` permutes `A`. -/
theorem image_add_eq_of_subset (A : Finset (ZMod M)) (h : ZMod M) (hA : ∀ a ∈ A, a + h ∈ A) :
    A.image (fun a => a + h) = A := by
  apply Finset.eq_of_subset_of_card_le
  · intro b hb
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.1 hb
    exact hA a ha
  · rw [Finset.card_image_of_injective _ (add_left_injective h)]

/-- **Periodic sets.** If `A + h = A` then `A` has a zero at every order `d` not dividing `h`. -/
theorem zeroAt_of_translate (A : Finset (ZMod M)) (h : ℕ) (hA : ∀ a ∈ A, a + (h : ZMod M) ∈ A)
    (d : ℕ) (hd : ¬ d ∣ h) : ZeroAt A d := by
  intro ξ hξ
  have himg := image_add_eq_of_subset A (h : ZMod M) hA
  have h1 : hat A ξ = ZMod.stdAddChar (ξ * (h : ZMod M)) * hat A ξ := by
    unfold hat
    conv_lhs => rw [← himg]
    rw [Finset.sum_image (fun x _ y _ hxy => add_left_injective _ hxy), Finset.mul_sum]
    refine Finset.sum_congr rfl fun a _ => ?_
    rw [mul_add, AddChar.map_add_eq_mul, mul_comm]
  have h2 : (ZMod.stdAddChar (ξ * (h : ZMod M)) : ℂ) ≠ 1 := by
    intro h3
    rw [DigitSets.stdAddChar_eq_one_iff, Bridge.mul_natCast_eq_zero_iff, hξ] at h3
    exact hd h3
  have h4 : (1 - (ZMod.stdAddChar (ξ * (h : ZMod M)) : ℂ)) * hat A ξ = 0 := by linear_combination h1
  exact (mul_eq_zero.1 h4).resolve_left (sub_ne_zero.2 (Ne.symm h2))

end Pqr
