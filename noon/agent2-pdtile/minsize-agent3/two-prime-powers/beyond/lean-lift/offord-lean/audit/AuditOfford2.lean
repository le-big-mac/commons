import Pnq.OffordBad
/-! Audit, second file: the statements at particular arguments (they are `sorry` in this copy: this shows only
their form and how they apply), and the instances that the print hides. -/
open Finset Pnq Polynomial

/-! ## the statements at particular arguments -/
-- with the ordinary `univ` of `Fin 4 → Bool`, `exact h` fails (the statement's `univ` is built on the classical
-- `DecidableEq ι`); `convert h` closes it
open Classical in
example (v : ℝ) :
    (Finset.univ.filter fun ε : Fin 4 → Bool => ∑ i, (sg (ε i) : ℝ) * (1 : ℝ) = v).card ≤ 6 := by
  have h := card_signedSum_eq_le_real (ι := Fin 4) (fun _ => (1 : ℝ)) (by simp) v
  rw [Fintype.card_fin] at h
  convert h
  decide

open Classical in
example (v : ℂ) :
    (Finset.univ.filter fun ε : Fin 3 → Bool => ∑ i, (sg (ε i) : ℂ) * Complex.I = v).card ≤ 3 := by
  have h := card_signedSum_eq_le_complex (ι := Fin 3) (fun _ => Complex.I) (by simp) v
  rw [Fintype.card_fin] at h
  convert h
  decide

open Classical in
example (e : Fin 5 → ℕ) :
    (Finset.univ.filter fun ε : Fin 5 → Bool => BadAt e ε 7).card ≤ 10 := by
  have h := card_badAt_le_choose e (d := 7) (by decide)
  rw [Fintype.card_fin] at h
  convert h
  decide

open Classical in
example (e : Fin 4 → ℕ) (k : ℕ) :
    (Finset.univ.filter fun ε : Fin 4 → Bool => ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d).card ≤ 12 := by
  have h := card_exists_badAt_two_pow_le e k
  rw [Fintype.card_fin] at h
  convert h
  decide

open Classical in
example (e : Fin 4 → ℕ) (k : ℕ) :
    (Finset.univ.filter fun ε : Fin 4 → Bool => ∃ d, d ∣ 2 ^ k * 45 ∧ BadAt e ε d).card ≤ 72 := by
  have h := card_exists_badAt_le_divisors e k (n' := 45) (by decide)
  rw [Fintype.card_fin] at h
  convert h
  decide

example (e : Fin 3 → ℕ) (ε : Fin 3 → Bool) : ¬ BadAt e ε 1 :=
  not_badAt_one_of_odd e (by decide) ε

example (e : Fin 3 → ℕ) (ε : Fin 3 → Bool) (k : ℕ) : ¬ ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d :=
  not_exists_badAt_two_pow_of_odd e k (by decide) ε

-- the statements hold for a type in any universe and need no `DecidableEq ι`
example {ι : Type 3} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) (h : Odd (Fintype.card ι)) : ¬ BadAt e ε 1 :=
  not_badAt_one_of_odd e h ε

/-! ## hypotheses that cannot be dropped -/
-- statement 3 without `d ≠ 0` would be false: one element, both signings bad at 0, bound 1
open Classical in
example : (Finset.univ.filter fun ε : Fin 1 → Bool => BadAt (fun _ => 0) ε 0).card = 2 := by
  simp [BadAt]

-- statements 1 without `a i ≠ 0` would be false: one number 0, both signings give 0, bound 1
open Classical in
example : (Finset.univ.filter fun ε : Fin 1 → Bool =>
    ∑ i, (sg (ε i) : ℝ) * (![0] : Fin 1 → ℝ) i = 0).card = 2 := by
  simp

-- m = 0: the count of statement 3 is 1 (not 0), and the bound is 1
open Classical in
example (d : ℕ) : (Finset.univ.filter fun ε : Fin 0 → Bool => BadAt (fun _ => 0) ε d).card = 1 := by
  simp [BadAt, P]

-- statement 7 with n' = 0 (excluded by `¬ 2 ∣ n'`) would be false: every d divides 0, so d = 0 counts
example {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) (k : ℕ) : ∃ d, d ∣ 2 ^ k * 0 ∧ BadAt e ε d :=
  ⟨0, by simp, by simp [BadAt]⟩

/-! ## the instances that the print hides -/
set_option pp.explicit true in
set_option pp.notation false in
#check @Pnq.card_badAt_le_choose
set_option pp.explicit true in
set_option pp.notation false in
#check @Pnq.card_signedSum_eq_le_real
set_option pp.explicit true in
set_option pp.notation false in
#check @Pnq.not_badAt_one_of_odd
#print axioms Pnq.card_exists_badAt_le
