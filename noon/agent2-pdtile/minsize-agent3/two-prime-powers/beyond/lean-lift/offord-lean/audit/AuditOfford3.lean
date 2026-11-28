import Pnq.OffordBad
/-! Audit, third file: the bound of statement 5 is attained for two elements (exponents 0, 1, k = 1): each of the
four signings is bad at 1 or at 2, and `2 * C(2, 1) = 4`.  (A fact about one small case; none of the seven.) -/
open Finset Pnq Polynomial

theorem Audit.all_bad (ε : Fin 2 → Bool) : ∃ d, d ∣ 2 ^ 1 ∧ BadAt ![0, 1] ε d := by
  have hP : P ![0, 1] ε = C (sg (ε 0)) + C (sg (ε 1)) * X := by
    simp [P, Fin.sum_univ_two]
  cases h0 : ε 0 <;> cases h1 : ε 1
  · -- signs - - : the mask -1 - X is divisible by Φ_2 = X + 1
    refine ⟨2, by norm_num, ?_⟩
    unfold BadAt
    rw [hP, h0, h1, cyclotomic_two]
    exact ⟨-1, by simp [sg]; try ring⟩
  · -- signs - + : the mask -1 + X is divisible by Φ_1 = X - 1
    refine ⟨1, by norm_num, ?_⟩
    unfold BadAt
    rw [hP, h0, h1, cyclotomic_one]
    exact ⟨1, by simp [sg]; try ring⟩
  · -- signs + - : the mask 1 - X
    refine ⟨1, by norm_num, ?_⟩
    unfold BadAt
    rw [hP, h0, h1, cyclotomic_one]
    exact ⟨-1, by simp [sg]; try ring⟩
  · -- signs + + : the mask 1 + X
    refine ⟨2, by norm_num, ?_⟩
    unfold BadAt
    rw [hP, h0, h1, cyclotomic_two]
    exact ⟨1, by simp [sg]; try ring⟩

open Classical in
theorem Audit.card_eq : (Finset.univ.filter fun ε : Fin 2 → Bool => ∃ d, d ∣ 2 ^ 1 ∧ BadAt ![0, 1] ε d).card
    = 2 * (Fintype.card (Fin 2)).choose (Fintype.card (Fin 2) / 2) := by
  rw [Finset.filter_true_of_mem (fun ε _ => Audit.all_bad ε)]
  simp

#print axioms Audit.card_eq
