/-
An arithmetic fact used for one exceptional zero pattern: for distinct primes `p`, `q` the number
`p²q²(pq − 1) / (p²(q − 1) + q²(p − 1))` is not an integer.
-/
import Mathlib

namespace P2q2

/-- `D = (a+1)² b + (b+1)² a` is coprime to `a + 1` when `a + 1` and `b + 1` are coprime. -/
private lemma coprime_D_left (a b : ℕ) (hcop : Nat.Coprime (a + 1) (b + 1)) :
    Nat.Coprime ((a + 1) ^ 2 * b + (b + 1) ^ 2 * a) (a + 1) := by
  have hrw : (a + 1) ^ 2 * b + (b + 1) ^ 2 * a = (b + 1) ^ 2 * a + (a + 1) * ((a + 1) * b) := by
    ring
  rw [hrw, Nat.coprime_add_mul_left_left]
  have ha : Nat.Coprime a (a + 1) := by simp
  exact Nat.Coprime.mul_left (hcop.symm.pow_left 2) ha

/-- The natural-number form of the statement, with `p = a + 1`, `q = b + 1`:
`n · D = (a+1)² (b+1)² · T` is impossible, where `D = (a+1)² b + (b+1)² a` and `T = a b + a + b`,
because `D` is coprime to `(a+1)² (b+1)²`, hence divides `T`, while `D - T = a b (a + b + 3) > 0`. -/
private lemma no_card_nat (a b n : ℕ) (ha : 1 ≤ a) (hb : 1 ≤ b)
    (hcop : Nat.Coprime (a + 1) (b + 1))
    (h : n * ((a + 1) ^ 2 * b + (b + 1) ^ 2 * a)
      = (a + 1) ^ 2 * (b + 1) ^ 2 * (a * b + a + b)) : False := by
  have h1 : Nat.Coprime ((a + 1) ^ 2 * b + (b + 1) ^ 2 * a) (a + 1) := coprime_D_left a b hcop
  have h2 : Nat.Coprime ((a + 1) ^ 2 * b + (b + 1) ^ 2 * a) (b + 1) := by
    have := coprime_D_left b a hcop.symm
    rwa [add_comm] at this
  have h3 : Nat.Coprime ((a + 1) ^ 2 * b + (b + 1) ^ 2 * a) ((a + 1) ^ 2 * (b + 1) ^ 2) :=
    Nat.Coprime.mul_right (h1.pow_right 2) (h2.pow_right 2)
  have hdvd : (a + 1) ^ 2 * b + (b + 1) ^ 2 * a ∣ (a + 1) ^ 2 * (b + 1) ^ 2 * (a * b + a + b) :=
    ⟨n, by rw [← h, mul_comm]⟩
  have hdvdT : (a + 1) ^ 2 * b + (b + 1) ^ 2 * a ∣ a * b + a + b := h3.dvd_of_dvd_mul_left hdvd
  have hTpos : 0 < a * b + a + b := by omega
  have hle : (a + 1) ^ 2 * b + (b + 1) ^ 2 * a ≤ a * b + a + b := Nat.le_of_dvd hTpos hdvdT
  have hab : 0 < a * b := Nat.mul_pos ha hb
  have hgt : a * b + a + b < (a + 1) ^ 2 * b + (b + 1) ^ 2 * a := by
    have hexp : (a + 1) ^ 2 * b + (b + 1) ^ 2 * a = a * b + a + b + a * b * (a + b + 3) := by
      ring
    have : 0 < a * b * (a + b + 3) := Nat.mul_pos hab (by omega)
    omega
  omega

theorem no_card (p q n : ℕ) (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q)
    (h : (n : ℝ) * ((p : ℝ) ^ 2 * ((q : ℝ) - 1) + (q : ℝ) ^ 2 * ((p : ℝ) - 1))
      = (p : ℝ) ^ 2 * (q : ℝ) ^ 2 * ((p : ℝ) * (q : ℝ) - 1)) : False := by
  have hcop : Nat.Coprime p q := (Nat.coprime_primes hp hq).2 hpq
  obtain ⟨a, rfl⟩ : ∃ a, p = a + 1 := ⟨p - 1, by have := hp.pos; omega⟩
  obtain ⟨b, rfl⟩ : ∃ b, q = b + 1 := ⟨q - 1, by have := hq.pos; omega⟩
  have ha : 1 ≤ a := by have := hp.two_le; omega
  have hb : 1 ≤ b := by have := hq.two_le; omega
  refine no_card_nat a b n ha hb hcop ?_
  have hR : ((n * ((a + 1) ^ 2 * b + (b + 1) ^ 2 * a) : ℕ) : ℝ)
      = (((a + 1) ^ 2 * (b + 1) ^ 2 * (a * b + a + b) : ℕ) : ℝ) := by
    push_cast at h ⊢
    linear_combination h
  exact_mod_cast hR

end P2q2
