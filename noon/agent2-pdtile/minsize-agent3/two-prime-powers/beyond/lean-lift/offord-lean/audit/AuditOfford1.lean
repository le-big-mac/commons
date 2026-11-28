import Pnq.OffordBad
/-! Audit of the seven statements fixed on 28 November 2026: small checks that pin down the reading.
Nothing here proves any of the seven. -/
open Finset Pnq Polynomial

/-! ## the computable parts -/
#eval sg true
#eval sg false
#eval (List.range 14).map fun m => (m, m / 2, m.choose (m / 2))
#eval [0, 1, 3, 9, 15, 45, 105].map fun n => (n, (Nat.divisors n).card)

example : sg true = 1 := by decide
example : sg false = -1 := by decide
example : ((sg true : ℤ) : ℝ) = 1 := by simp [sg]
example : ((sg false : ℤ) : ℝ) = -1 := by simp [sg]
example : ((sg false : ℤ) : ℂ) = -1 := by simp [sg]

/-! natural-number division in the bound -/
example : (0 : ℕ).choose (0 / 2) = 1 := by decide
example : (1 : ℕ).choose (1 / 2) = 1 := by decide
example : (2 : ℕ).choose (2 / 2) = 2 := by decide
example : (5 : ℕ).choose (5 / 2) = 10 := by decide
example : (12 : ℕ).choose (12 / 2) = 924 := by decide

/-! divisors -/
example : (1 : ℕ).divisors.card = 1 := by decide
example : (45 : ℕ).divisors.card = 6 := by decide
example : (0 : ℕ).divisors.card = 0 := by decide
example : (2 : ℕ) ∣ 0 := by decide            -- so `¬ 2 ∣ n'` excludes `n' = 0`
example : ¬ (0 : ℕ) ∣ 2 ^ 3 := by decide      -- `d = 0` is no divisor of `2 ^ k`
example : ¬ (0 : ℕ) ∣ 2 ^ 3 * 45 := by decide

/-! ## `d = 0`: `Φ_0 = 1`, so every signing is bad at `0`; statement 3 needs `d ≠ 0` -/
example {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) : BadAt e ε 0 := by
  simp [BadAt]

/-! ## `m = 0`: the one (empty) signing has mask `0` and is bad at every `d` -/
example (e : Fin 0 → ℕ) (ε : Fin 0 → Bool) (d : ℕ) : BadAt e ε d := by
  simp [BadAt, P]

/-! ## concrete masks -/
-- exponents 0, 1 with signs + - : the mask is 1 - X, bad at 1
example : BadAt (ι := Fin 2) ![0, 1] ![true, false] 1 := by
  unfold BadAt P
  simp [sg, Fin.sum_univ_two, cyclotomic_one]
  exact ⟨-1, by ring⟩

-- exponents 0, 1 with signs + + : the mask is 1 + X, bad at 2 (a divisor of 2 ^ 1)
example : BadAt (ι := Fin 2) ![0, 1] ![true, true] 2 := by
  unfold BadAt P
  simp [sg, Fin.sum_univ_two, cyclotomic_two]
  exact ⟨1, by ring⟩

-- repeated exponents 3, 3 with signs + - : the mask is 0, bad at every d
example (d : ℕ) : BadAt (ι := Fin 2) ![3, 3] ![true, false] d := by
  unfold BadAt P
  simp [sg, Fin.sum_univ_two]

-- one element: the mask X ^ 5 is not bad at 1
example : ¬ BadAt (ι := Fin 1) ![5] ![true] 1 := by
  unfold BadAt P
  rw [cyclotomic_one, show (X - 1 : ℤ[X]) = X - C 1 by simp, dvd_iff_isRoot]
  simp [sg]

-- exponents 0, 1 with signs + + : the mask 1 + X is not bad at 1
example : ¬ BadAt (ι := Fin 2) ![0, 1] ![true, true] 1 := by
  unfold BadAt P
  rw [cyclotomic_one, show (X - 1 : ℤ[X]) = X - C 1 by simp, dvd_iff_isRoot]
  simp [sg, Fin.sum_univ_two]

/-! ## the signed sums of statements 1 and 2 -/
open Classical in
example : ![true, false] ∈
    (Finset.univ.filter fun ε : Fin 2 → Bool => ∑ i, (sg (ε i) : ℝ) * (![1, 1] : Fin 2 → ℝ) i = 0) := by
  simp [sg, Fin.sum_univ_two]

open Classical in
example : ![true, true] ∉
    (Finset.univ.filter fun ε : Fin 2 → Bool => ∑ i, (sg (ε i) : ℝ) * (![1, 1] : Fin 2 → ℝ) i = 0) := by
  simp [sg, Fin.sum_univ_two]

open Classical in
example : ![true, false] ∈
    (Finset.univ.filter fun ε : Fin 2 → Bool =>
      ∑ i, (sg (ε i) : ℂ) * (![Complex.I, Complex.I] : Fin 2 → ℂ) i = 0) := by
  simp [sg, Fin.sum_univ_two]

/-! ## what the statements rest on -/
#print axioms Pnq.card_exists_badAt_le
#print axioms Pnq.card_badAt_le_choose
#check @Pnq.card_exists_badAt_le
#print axioms Pnq.card_signedSum_eq_le_real
#print axioms Pnq.card_signedSum_eq_le_complex
#print axioms Pnq.not_badAt_one_of_odd
#print axioms Pnq.card_exists_badAt_two_pow_le
#print axioms Pnq.not_exists_badAt_two_pow_of_odd
#print axioms Pnq.card_exists_badAt_le_divisors
