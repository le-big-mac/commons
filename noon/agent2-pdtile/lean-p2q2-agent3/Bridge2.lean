/-
The bridge from Fourier zeros to residue-class counts, for an order `p^(a+1) q^(b+1)` (both primes to a positive
power): the instance needed for `ZMod (p^2 q^2)`.  (agent3 / Yonder; modelled on `zeroAt_prime_pow_mul` in `Bridge.lean`.)
-/
import Pqr.Bridge

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

namespace Bridge

/-- `[e ∣ p^(a+1) q^(b+1)] - [e ∣ p^a q^(b+1)] - [e ∣ p^(a+1) q^b] + [e ∣ p^a q^b] = [e = p^(a+1) q^(b+1)]` -/
theorem indicator_prime_pow_mul_pow {p q : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) (a b e : ℕ) :
    (if e ∣ p ^ (a + 1) * q ^ (b + 1) then (1 : ℤ) else 0) + (if e ∣ p ^ a * q ^ (b + 1) then -1 else 0)
        + (if e ∣ p ^ (a + 1) * q ^ b then -1 else 0) + (if e ∣ p ^ a * q ^ b then 1 else 0)
      = if e = p ^ (a + 1) * q ^ (b + 1) then 1 else 0 := by
  have hcop : Nat.Coprime q p := (Nat.coprime_primes hq hp).2 (Ne.symm hpq)
  have h43 : e ∣ p ^ a * q ^ b → e ∣ p ^ (a + 1) * q ^ b := fun h =>
    h.trans (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ a)) _)
  have h42 : e ∣ p ^ a * q ^ b → e ∣ p ^ a * q ^ (b + 1) := fun h =>
    h.trans (Nat.mul_dvd_mul_left _ (pow_dvd_pow q (Nat.le_succ b)))
  have h31 : e ∣ p ^ (a + 1) * q ^ b → e ∣ p ^ (a + 1) * q ^ (b + 1) := fun h =>
    h.trans (Nat.mul_dvd_mul_left _ (pow_dvd_pow q (Nat.le_succ b)))
  have h21 : e ∣ p ^ a * q ^ (b + 1) → e ∣ p ^ (a + 1) * q ^ (b + 1) := fun h =>
    h.trans (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ a)) _)
  have h234 : e ∣ p ^ a * q ^ (b + 1) → e ∣ p ^ (a + 1) * q ^ b → e ∣ p ^ a * q ^ b := by
    intro h2 h3
    obtain ⟨e₁, e₂, he₁, he₂, rfl⟩ := Nat.dvd_mul.1 h2
    have hc : Nat.Coprime e₂ (p ^ (a + 1)) :=
      Nat.Coprime.coprime_dvd_left he₂ (Nat.Coprime.pow _ _ hcop)
    have h4 : e₂ ∣ q ^ b := hc.dvd_of_dvd_mul_left ((dvd_mul_left e₂ e₁).trans h3)
    exact Nat.mul_dvd_mul he₁ h4
  have hE1 : e = p ^ (a + 1) * q ^ (b + 1) → e ∣ p ^ (a + 1) * q ^ (b + 1) := fun h => h ▸ dvd_rfl
  have hE2 : e = p ^ (a + 1) * q ^ (b + 1) → ¬ e ∣ p ^ a * q ^ (b + 1) := by
    rintro rfl h
    exact not_prime_pow_succ_dvd hp a (Nat.dvd_of_mul_dvd_mul_right (pow_pos hq.pos _) h)
  have hE3 : e = p ^ (a + 1) * q ^ (b + 1) → ¬ e ∣ p ^ (a + 1) * q ^ b := by
    rintro rfl h
    exact not_prime_pow_succ_dvd hq b (Nat.dvd_of_mul_dvd_mul_left (pow_pos hp.pos _) h)
  have hmain : e ∣ p ^ (a + 1) * q ^ (b + 1) → ¬ e ∣ p ^ a * q ^ (b + 1) → ¬ e ∣ p ^ (a + 1) * q ^ b
      → e = p ^ (a + 1) * q ^ (b + 1) := by
    intro h1 h2 h3
    obtain ⟨e₁, e₂, he₁, he₂, rfl⟩ := Nat.dvd_mul.1 h1
    rcases (dvd_prime_pow_succ_iff hp a e₁).1 he₁ with h | rfl
    · exact absurd (Nat.mul_dvd_mul h he₂) h2
    · rcases (dvd_prime_pow_succ_iff hq b e₂).1 he₂ with h | rfl
      · exact absurd (Nat.mul_dvd_mul_left _ h) h3
      · rfl
  by_cases hE : e = p ^ (a + 1) * q ^ (b + 1)
  · rw [ite_eq_left (hE1 hE), ite_eq_right (hE2 hE), ite_eq_right (hE3 hE), ite_eq_right (fun h => hE3 hE (h43 h)),
      ite_eq_left hE]
    norm_num
  · by_cases P2 : e ∣ p ^ a * q ^ (b + 1) <;> by_cases P3 : e ∣ p ^ (a + 1) * q ^ b
    · rw [ite_eq_left (h21 P2), ite_eq_left P2, ite_eq_left P3, ite_eq_left (h234 P2 P3), ite_eq_right hE]
      norm_num
    · rw [ite_eq_left (h21 P2), ite_eq_left P2, ite_eq_right P3, ite_eq_right (fun h => P3 (h43 h)), ite_eq_right hE]
      norm_num
    · rw [ite_eq_left (h31 P3), ite_eq_right P2, ite_eq_left P3, ite_eq_right (fun h => P2 (h42 h)), ite_eq_right hE]
      norm_num
    · rw [ite_eq_right (fun h => hE (hmain h P2 P3)), ite_eq_right P2, ite_eq_right P3,
        ite_eq_right (fun h => P3 (h43 h)), ite_eq_right hE]
      norm_num

end Bridge

/-- order `p^(a+1) q^(b+1)`: in every class modulo `p^a q^b`, the `p × q` array of counts is additive -/
theorem zeroAt_prime_pow_mul_pow (A : Finset (ZMod M)) (p q : ℕ) (hp : p.Prime) (hq : q.Prime)
    (hpq : p ≠ q) (a b : ℕ) (h : p ^ (a + 1) * q ^ (b + 1) ∣ M) :
    ZeroAt A (p ^ (a + 1) * q ^ (b + 1)) ↔ ∀ v : ZMod M,
      p * q * cnt A (p ^ (a + 1) * q ^ (b + 1)) v + cnt A (p ^ a * q ^ b) v
        = q * cnt A (p ^ a * q ^ (b + 1)) v + p * cnt A (p ^ (a + 1) * q ^ b) v := by
  have h1 : p ^ a * q ^ (b + 1) ∣ M := (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ a)) _).trans h
  have h2 : p ^ (a + 1) * q ^ b ∣ M := (Nat.mul_dvd_mul_left _ (pow_dvd_pow q (Nat.le_succ b))).trans h
  have h3 : p ^ a * q ^ b ∣ M := (Nat.mul_dvd_mul_left _ (pow_dvd_pow q (Nat.le_succ b))).trans h1
  have hpa : (p : ℤ) ^ a * (q : ℤ) ^ b ≠ 0 :=
    mul_ne_zero (pow_ne_zero _ (Nat.cast_ne_zero.2 hp.ne_zero)) (pow_ne_zero _ (Nat.cast_ne_zero.2 hq.ne_zero))
  have key : ∀ X Y Z W : ℕ,
      ((1 : ℤ) * ((p ^ (a + 1) * q ^ (b + 1) : ℕ) : ℤ) * (X : ℤ) + (-1) * ((p ^ a * q ^ (b + 1) : ℕ) : ℤ) * (Y : ℤ)
          + (-1) * ((p ^ (a + 1) * q ^ b : ℕ) : ℤ) * (Z : ℤ) + 1 * ((p ^ a * q ^ b : ℕ) : ℤ) * (W : ℤ) = 0)
        ↔ p * q * X + W = q * Y + p * Z := by
    intro X Y Z W
    push_cast
    constructor
    · intro h4
      have h5 : (p : ℤ) ^ a * (q : ℤ) ^ b * ((p : ℤ) * q * X + W - (q * Y + p * Z)) = 0 := by
        linear_combination h4
      have h6 : (p : ℤ) * q * X + W = q * Y + p * Z := by
        have := (mul_eq_zero.1 h5).resolve_left hpa
        linarith
      exact_mod_cast h6
    · intro h4
      have h5 : (p : ℤ) * q * X + W = q * Y + p * Z := by exact_mod_cast h4
      linear_combination (p : ℤ) ^ a * (q : ℤ) ^ b * h5
  rw [Bridge.zeroAt_iff_cnt_aux A (p ^ (a + 1) * q ^ (b + 1)) (Finset.univ : Finset (Fin 4))
    ![p ^ (a + 1) * q ^ (b + 1), p ^ a * q ^ (b + 1), p ^ (a + 1) * q ^ b, p ^ a * q ^ b] ![1, -1, -1, 1] ?_ ?_]
  · refine forall_congr' fun v => ?_
    rw [Fin.sum_univ_four]
    exact key _ _ _ _
  · intro i _
    fin_cases i
    · exact h
    · exact h1
    · exact h2
    · exact h3
  · intro e _
    rw [Fin.sum_univ_four]
    exact Bridge.indicator_prime_pow_mul_pow hp hq hpq a b e

end Pqr
