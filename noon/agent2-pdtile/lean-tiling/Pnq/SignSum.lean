/-
The statement on signs for every odd `n`: the sum N1.  It is about `μ` only: the sum of `(1/2)^(μ t)` over a set of
odd numbers `t > 1` with `μ t ≤ m - 1`, together with the share `m.choose (m/2) / 2^m` of the signings bad at `1`, is
below `1`.  In the rational numbers.
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignDefs

open Finset

namespace Pnq

namespace SumAux

/-!
The route.  `a u` is the product of `1 + u / ((p - 1) / 2)` over the odd primes `p ≤ 2 * u + 1`.
* Counting (`card_le_a`, `card_filter_add_one_le`): a finite set of odd numbers `t > 1` has at most
  `a u - 1` elements with `μ t ≤ 2 * u` (an injection into the vectors of exponents).
* Layers (`layers`, `part_le_W`): the part of the sum with `μ t ≤ 2 * U` is at most
  `W U = ∑_{u=1}^{U} (a u - a (u - 1)) / 4^u`.
* The tail (`a_sq_le`, `a_le`, `tail`, `sum_le`): `a u ^ 2 ≤ 8 ^ u` by halving and a count of the
  odd primes, so `a u / 4^u ≤ (5/7)^u` (because `8 ≤ (20/7)^2`), and the whole sum is at most
  `W U₀ + (5/2) (5/7)^U₀` for every `U₀`.
* The numbers (`W_19`, `small_cases`, `central_le`), with `U₀ = 19`.
-/

/-- the odd primes below `B` -/
def oddPrimes (B : ℕ) : Finset ℕ := (Finset.range B).filter fun p => p.Prime ∧ p ≠ 2

/-- the product of `1 + u / ((p - 1) / 2)` over the odd primes `p < B` -/
def aB (B u : ℕ) : ℕ := ∏ p ∈ oddPrimes B, (1 + u / ((p - 1) / 2))

/-- the bound for the number of odd `t` with `μ t ≤ 2 * u` -/
def a (u : ℕ) : ℕ := aB (2 * u + 2) u

theorem mem_oddPrimes {B p : ℕ} : p ∈ oddPrimes B ↔ p < B ∧ p.Prime ∧ p ≠ 2 := by
  simp [oddPrimes]

theorem oddPrimes_mono {B B' : ℕ} (h : B ≤ B') : oddPrimes B ⊆ oddPrimes B' := by
  intro p hp
  rw [mem_oddPrimes] at hp ⊢
  exact ⟨lt_of_lt_of_le hp.1 h, hp.2⟩

/-- an odd prime is at least `3` and is `2 * k + 1` with `k = (p - 1) / 2 ≥ 1` -/
theorem oddPrime_half {p : ℕ} (hp : p.Prime) (h2 : p ≠ 2) :
    1 ≤ (p - 1) / 2 ∧ p = 2 * ((p - 1) / 2) + 1 := by
  have hodd : Odd p := hp.odd_of_ne_two h2
  have h1 : 2 ≤ p := hp.two_le
  obtain ⟨k, hk⟩ := hodd
  omega

/-- the product may be taken over the odd primes below any bound `B ≥ 2 * u + 2` -/
theorem aB_eq_a {B u : ℕ} (h : 2 * u + 2 ≤ B) : aB B u = a u := by
  unfold a aB
  symm
  apply Finset.prod_subset (oddPrimes_mono h)
  intro p hp hnp
  rw [mem_oddPrimes] at hp hnp
  have hge : 2 * u + 2 ≤ p := by
    by_contra hlt
    exact hnp ⟨by omega, hp.2⟩
  obtain ⟨h1, h2⟩ := oddPrime_half hp.2.1 hp.2.2
  have : u / ((p - 1) / 2) = 0 := Nat.div_eq_of_lt (by omega)
  rw [this, Nat.add_zero]

/-! ### `μ` of an odd number -/

theorem mu_even {t : ℕ} (ht : ¬ 2 ∣ t) : Even (μ t) := by
  unfold μ
  apply Finset.sup_induction
  · exact ⟨0, rfl⟩
  · intro a₁ h₁ a₂ h₂
    rcases le_total a₁ a₂ with h | h
    · rwa [sup_eq_right.2 h]
    · rwa [sup_eq_left.2 h]
  · intro p hp
    have hpp : p.Prime := Nat.prime_of_mem_primeFactors hp
    have hpt : p ∣ t := Nat.dvd_of_mem_primeFactors hp
    have h2 : p ≠ 2 := by
      rintro rfl
      exact ht hpt
    obtain ⟨_, h3⟩ := oddPrime_half hpp h2
    have : p - 1 = 2 * ((p - 1) / 2) := by omega
    rw [this, mul_assoc]
    exact even_two_mul _

theorem le_mu {t p : ℕ} (hp : p ∈ t.primeFactors) : (p - 1) * t.factorization p ≤ μ t :=
  Finset.le_sup (f := fun p => (p - 1) * t.factorization p) hp

theorem two_le_mu {t : ℕ} (ht : ¬ 2 ∣ t) (h1 : 1 < t) : 2 ≤ μ t := by
  have hne : t ≠ 1 := by omega
  obtain ⟨p, hpp, hpt⟩ := Nat.exists_prime_and_dvd hne
  have h2 : p ≠ 2 := by
    rintro rfl
    exact ht hpt
  have hmem : p ∈ t.primeFactors := Nat.mem_primeFactors.2 ⟨hpp, hpt, by omega⟩
  have hle := le_mu hmem
  have hpos : 0 < t.factorization p := hpp.factorization_pos_of_dvd (by omega) hpt
  obtain ⟨h3, h4⟩ := oddPrime_half hpp h2
  have h5 : 2 ≤ p - 1 := by omega
  calc 2 = 2 * 1 := rfl
    _ ≤ (p - 1) * t.factorization p := Nat.mul_le_mul h5 hpos
    _ ≤ μ t := hle

/-- the exponent of an odd prime `p` in a `t` with `μ t ≤ 2 * u` is at most
`u / ((p - 1) / 2)` -/
theorem fact_le {t u p : ℕ} (hμ : μ t ≤ 2 * u) (hpp : p.Prime) (h2 : p ≠ 2) :
    t.factorization p ≤ u / ((p - 1) / 2) := by
  obtain ⟨h3, h4⟩ := oddPrime_half hpp h2
  rw [Nat.le_div_iff_mul_le (by omega)]
  by_cases hmem : p ∈ t.primeFactors
  · have hle := le_mu hmem
    have h5 : p - 1 = 2 * ((p - 1) / 2) := by omega
    rw [h5] at hle
    have h6 : 2 * (t.factorization p * ((p - 1) / 2)) ≤ 2 * u := by
      calc 2 * (t.factorization p * ((p - 1) / 2))
          = 2 * ((p - 1) / 2) * t.factorization p := by ring
        _ ≤ μ t := hle
        _ ≤ 2 * u := hμ
    omega
  · have : t.factorization p = 0 := by
      rw [← Finsupp.notMem_support_iff, Nat.support_factorization]
      exact hmem
    rw [this]
    simp

/-- an odd `t` with `μ t ≤ 2 * u` has no prime factor outside the odd primes below `2 * u + 2` -/
theorem fact_eq_zero {t u p : ℕ} (ht : ¬ 2 ∣ t) (hμ : μ t ≤ 2 * u)
    (hp : p ∉ oddPrimes (2 * u + 2)) : t.factorization p = 0 := by
  by_contra hne
  have hmem : p ∈ t.primeFactors := by
    rw [← Nat.support_factorization, Finsupp.mem_support_iff]
    exact hne
  have hpp : p.Prime := Nat.prime_of_mem_primeFactors hmem
  have hpt : p ∣ t := Nat.dvd_of_mem_primeFactors hmem
  have h2 : p ≠ 2 := by
    rintro rfl
    exact ht hpt
  have hge : 2 * u + 2 ≤ p := by
    by_contra hlt
    exact hp (mem_oddPrimes.2 ⟨by omega, hpp, h2⟩)
  have hle := le_mu hmem
  have hpos : 0 < t.factorization p := Nat.pos_of_ne_zero hne
  have h5 : 2 * u + 1 ≤ (p - 1) * t.factorization p :=
    calc 2 * u + 1 = (2 * u + 1) * 1 := (mul_one _).symm
      _ ≤ (p - 1) * t.factorization p := Nat.mul_le_mul (by omega) hpos
  omega

/-- **Counting.** A finite set of odd numbers `t` with `μ t ≤ 2 * u` has at most `a u` elements. -/
theorem card_le_a (S : Finset ℕ) (u : ℕ) (hS : ∀ t ∈ S, ¬ 2 ∣ t ∧ μ t ≤ 2 * u) : S.card ≤ a u := by
  have hcard :
      ((oddPrimes (2 * u + 2)).pi fun p => Finset.range (1 + u / ((p - 1) / 2))).card = a u := by
    rw [Finset.card_pi]
    unfold a aB
    apply Finset.prod_congr rfl
    intro p _
    rw [Finset.card_range]
  rw [← hcard]
  apply Finset.card_le_card_of_injOn (fun t p _ => t.factorization p)
  · intro t ht
    have ht' := hS t (Finset.mem_coe.1 ht)
    rw [Finset.mem_coe, Finset.mem_pi]
    intro p hp
    rw [mem_oddPrimes] at hp
    rw [Finset.mem_range]
    have := fact_le ht'.2 hp.2.1 hp.2.2
    exact Nat.lt_of_le_of_lt this (by omega)
  · intro t₁ ht₁ t₂ ht₂ heq
    have h₁ := hS t₁ (Finset.mem_coe.1 ht₁)
    have h₂ := hS t₂ (Finset.mem_coe.1 ht₂)
    have hne₁ : t₁ ≠ 0 := by
      rintro rfl
      exact h₁.1 (dvd_zero 2)
    have hne₂ : t₂ ≠ 0 := by
      rintro rfl
      exact h₂.1 (dvd_zero 2)
    apply Nat.eq_of_factorization_eq hne₁ hne₂
    intro p
    by_cases hp : p ∈ oddPrimes (2 * u + 2)
    · exact congrFun (congrFun heq p) hp
    · rw [fact_eq_zero h₁.1 h₁.2 hp, fact_eq_zero h₂.1 h₂.2 hp]

theorem mu_one : μ 1 = 0 := by
  simp [μ]

/-- a finite set of odd numbers `t > 1` has at most `a u - 1` elements with `μ t ≤ 2 * u` -/
theorem card_filter_add_one_le (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t) (u : ℕ) :
    (T.filter fun t => μ t ≤ 2 * u).card + 1 ≤ a u := by
  have h1 : 1 ∉ T.filter fun t => μ t ≤ 2 * u := by
    intro h
    have := (hT 1 (Finset.mem_filter.1 h).1).2
    omega
  rw [← Finset.card_insert_of_notMem h1]
  apply card_le_a
  intro t ht
  rw [Finset.mem_insert, Finset.mem_filter] at ht
  rcases ht with rfl | ht
  · refine ⟨by decide, ?_⟩
    rw [mu_one]
    omega
  · exact ⟨(hT t ht.1).1, ht.2⟩

/-! ### Layers -/

/-- the sum of `(1/2)^(μ t)` over the `t ∈ T` with `μ t ≤ 2 * U` -/
def part (T : Finset ℕ) (U : ℕ) : ℚ := ∑ t ∈ T.filter (fun t => μ t ≤ 2 * U), (1 / 2 : ℚ) ^ μ t

/-- the number of `t ∈ T` with `μ t ≤ 2 * U` -/
def cnt (T : Finset ℕ) (U : ℕ) : ℕ := (T.filter fun t => μ t ≤ 2 * U).card

/-- the number of `t ∈ T` with `μ t = 2 * U` -/
def lay (T : Finset ℕ) (U : ℕ) : ℕ := (T.filter fun t => μ t = 2 * U).card

theorem filter_succ (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t) (U : ℕ) :
    T.filter (fun t => μ t ≤ 2 * (U + 1)) =
      T.filter (fun t => μ t ≤ 2 * U) ∪ T.filter (fun t => μ t = 2 * (U + 1)) := by
  rw [← Finset.filter_or]
  apply Finset.filter_congr
  intro t ht
  obtain ⟨k, hk⟩ := mu_even (hT t ht)
  omega

theorem disjoint_succ (T : Finset ℕ) (U : ℕ) :
    Disjoint (T.filter (fun t => μ t ≤ 2 * U)) (T.filter (fun t => μ t = 2 * (U + 1))) := by
  apply Finset.disjoint_filter.2
  intro t _ h1 h2
  omega

theorem cnt_succ (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t) (U : ℕ) :
    cnt T (U + 1) = cnt T U + lay T (U + 1) := by
  unfold cnt lay
  rw [filter_succ T hT U, Finset.card_union_of_disjoint (disjoint_succ T U)]

theorem part_succ (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t) (U : ℕ) :
    part T (U + 1) = part T U + (lay T (U + 1) : ℚ) / 4 ^ (U + 1) := by
  unfold part lay
  rw [filter_succ T hT U, Finset.sum_union (disjoint_succ T U)]
  congr 1
  have h : ∀ t ∈ T.filter (fun t => μ t = 2 * (U + 1)), (1 / 2 : ℚ) ^ μ t = 1 / 4 ^ (U + 1) := by
    intro t ht
    have e : (1 / 2 : ℚ) ^ 2 = 1 / 4 := by norm_num
    rw [(Finset.mem_filter.1 ht).2, pow_mul, e, one_div_pow]
  rw [Finset.sum_congr rfl h, Finset.sum_const, nsmul_eq_mul]
  ring

/-- the partial sums `∑_{u=1}^{U} (a u - a (u-1)) / 4^u` -/
def W (U : ℕ) : ℚ := ∑ u ∈ Finset.range U, ((a (u + 1) : ℚ) - a u) / 4 ^ (u + 1)

theorem W_succ (U : ℕ) : W (U + 1) = W U + ((a (U + 1) : ℚ) - a U) / 4 ^ (U + 1) :=
  Finset.sum_range_succ _ _

theorem a_zero : a 0 = 1 := by
  unfold a aB
  apply Finset.prod_eq_one
  intro p _
  rw [Nat.zero_div, Nat.add_zero]

theorem gap_nonneg (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t) (U : ℕ) :
    (0 : ℚ) ≤ ((a U : ℚ) - 1 - cnt T U) / 4 ^ U := by
  have hc := card_filter_add_one_le T hT U
  have h1 : ((cnt T U + 1 : ℕ) : ℚ) ≤ (a U : ℚ) := by
    unfold cnt
    exact_mod_cast hc
  push_cast at h1
  apply div_nonneg
  · linarith
  · positivity

/-- **Layers**, in the form that survives induction. -/
theorem layers (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t) (U : ℕ) :
    part T U + ((a U : ℚ) - 1 - cnt T U) / 4 ^ U ≤ W U := by
  induction U with
  | zero =>
    have hempty : T.filter (fun t => μ t ≤ 2 * 0) = ∅ := by
      apply Finset.filter_false_of_mem
      intro t ht
      have := two_le_mu (hT t ht).1 (hT t ht).2
      omega
    unfold part cnt W
    rw [hempty, a_zero]
    simp
  | succ U ih =>
    have hT' : ∀ t ∈ T, ¬ 2 ∣ t := fun t ht => (hT t ht).1
    have hd := gap_nonneg T hT U
    have key : part T (U + 1) + ((a (U + 1) : ℚ) - 1 - cnt T (U + 1)) / 4 ^ (U + 1) =
        part T U + (((a U : ℚ) - 1 - cnt T U) / 4 ^ U) / 4
          + ((a (U + 1) : ℚ) - a U) / 4 ^ (U + 1) := by
      rw [part_succ T hT' U, cnt_succ T hT' U, pow_succ]
      push_cast
      field_simp
      ring
    rw [key, W_succ]
    linarith

theorem part_le_W (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t) (U : ℕ) : part T U ≤ W U := by
  have h := layers T hT U
  have hd := gap_nonneg T hT U
  linarith

/-! ### The number of odd primes -/

theorem oddPrimes_succ_of_not {B : ℕ} (h : ¬ (B.Prime ∧ B ≠ 2)) :
    oddPrimes (B + 1) = oddPrimes B := by
  unfold oddPrimes
  rw [Finset.range_add_one, Finset.filter_insert]
  simp only [h, ↓reduceIte]

theorem card_oddPrimes_succ_le (B : ℕ) : (oddPrimes (B + 1)).card ≤ (oddPrimes B).card + 1 := by
  unfold oddPrimes
  rw [Finset.range_add_one, Finset.filter_insert]
  split_ifs
  · exact Finset.card_insert_le _ _
  · omega

theorem not_oddPrime_of_two_dvd {B : ℕ} (h : 2 ∣ B) : ¬ (B.Prime ∧ B ≠ 2) := by
  rintro ⟨hp, h2⟩
  exact h2 ((Nat.prime_dvd_prime_iff_eq Nat.prime_two hp).1 h).symm

theorem not_oddPrime_of_three_dvd {B : ℕ} (h : 3 ∣ B) (h3 : B ≠ 3) : ¬ (B.Prime ∧ B ≠ 2) := by
  rintro ⟨hp, _⟩
  exact h3 ((Nat.prime_dvd_prime_iff_eq Nat.prime_three hp).1 h).symm

theorem card_oddPrimes_six : (oddPrimes 6).card ≤ 2 := by decide

/-- from a multiple `n ≥ 6` of `6` on, only `n + 1` and `n + 5` can be prime among the next six
numbers -/
theorem card_oddPrimes_step (n : ℕ) (h6 : 6 ∣ n) (hn : 6 ≤ n) :
    (oddPrimes (n + 2)).card ≤ (oddPrimes n).card + 1 ∧
    (oddPrimes (n + 4)).card ≤ (oddPrimes n).card + 1 ∧
    (oddPrimes (n + 6)).card ≤ (oddPrimes n).card + 2 := by
  have e1 : (oddPrimes (n + 1)).card = (oddPrimes n).card :=
    congrArg Finset.card (oddPrimes_succ_of_not (B := n) (not_oddPrime_of_two_dvd (by omega)))
  have e2 : (oddPrimes (n + 2)).card ≤ (oddPrimes (n + 1)).card + 1 :=
    card_oddPrimes_succ_le (n + 1)
  have e3 : (oddPrimes (n + 3)).card = (oddPrimes (n + 2)).card :=
    congrArg Finset.card (oddPrimes_succ_of_not (B := n + 2) (not_oddPrime_of_two_dvd (by omega)))
  have e4 : (oddPrimes (n + 4)).card = (oddPrimes (n + 3)).card :=
    congrArg Finset.card
      (oddPrimes_succ_of_not (B := n + 3) (not_oddPrime_of_three_dvd (by omega) (by omega)))
  have e5 : (oddPrimes (n + 5)).card = (oddPrimes (n + 4)).card :=
    congrArg Finset.card (oddPrimes_succ_of_not (B := n + 4) (not_oddPrime_of_two_dvd (by omega)))
  have e6 : (oddPrimes (n + 6)).card ≤ (oddPrimes (n + 5)).card + 1 :=
    card_oddPrimes_succ_le (n + 5)
  omega

theorem card_oddPrimes_six_mul (k : ℕ) : (oddPrimes (6 * k + 6)).card ≤ 2 * k + 2 := by
  induction k with
  | zero => exact card_oddPrimes_six
  | succ k ih =>
    have h := (card_oddPrimes_step (6 * k + 6) (by omega) (by omega)).2.2
    have e : 6 * (k + 1) + 6 = 6 * k + 6 + 6 := by ring
    rw [e]
    omega

/-- the number `π` of odd primes `≤ 2 * u + 1` satisfies `2 * π ≤ 3 * (u - u / 2)` for `u ≥ 20` -/
theorem pi_bound (u : ℕ) (hu : 20 ≤ u) : 2 * (oddPrimes (2 * u + 2)).card ≤ 3 * (u - u / 2) := by
  obtain ⟨k, hk⟩ : ∃ k, 2 * u + 2 = 6 * k + 6 ∨ 2 * u + 2 = 6 * k + 6 + 2 ∨
      2 * u + 2 = 6 * k + 6 + 4 := ⟨(2 * u + 2) / 6 - 1, by omega⟩
  have h0 := card_oddPrimes_six_mul k
  have hs := card_oddPrimes_step (6 * k + 6) (by omega) (by omega)
  rcases hk with hk | hk | hk
  · rw [hk]
    omega
  · rw [hk]
    omega
  · rw [hk]
    omega

/-! ### Halving -/

theorem halving (u k : ℕ) (hk : 1 ≤ k) : 1 + u / k ≤ 2 * (1 + u / 2 / k) := by
  have h1 : u / 2 < (u / 2 / k + 1) * k := Nat.lt_mul_of_div_lt (Nat.lt_succ_self _) hk
  have h2 : u < (2 * (u / 2 / k + 1)) * k := by
    have e : (2 * (u / 2 / k + 1)) * k = 2 * ((u / 2 / k + 1) * k) := by ring
    omega
  have h3 : u / k < 2 * (u / 2 / k + 1) := (Nat.div_lt_iff_lt_mul hk).2 h2
  omega

theorem a_le_two_pow_mul (u : ℕ) : a u ≤ 2 ^ (oddPrimes (2 * u + 2)).card * a (u / 2) := by
  rw [← aB_eq_a (B := 2 * u + 2) (u := u / 2) (by omega)]
  unfold a aB
  rw [← Finset.prod_const, ← Finset.prod_mul_distrib]
  apply Finset.prod_le_prod
  intro p hp
  rw [mem_oddPrimes] at hp
  exact halving u _ (oddPrime_half hp.2.1 hp.2.2).1

/-! ### Evaluation for `u < 20` -/

theorem oddPrimes_forty : oddPrimes 40 = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37].toFinset := by
  decide

/-- `a u` for `u < 20`, as a product over a list -/
def aL (u : ℕ) : ℕ :=
  ([3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37].map fun p => 1 + u / ((p - 1) / 2)).prod

theorem a_eq_aL {u : ℕ} (h : u < 20) : a u = aL u := by
  rw [← aB_eq_a (B := 40) (by omega)]
  unfold aB aL
  rw [oddPrimes_forty, List.prod_toFinset _ (by decide)]

theorem a_1 : a 1 = 2 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_2 : a 2 = 6 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_3 : a 3 = 16 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_4 : a 4 = 30 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_5 : a 5 = 72 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_6 : a 6 = 336 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_7 : a 7 = 384 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_8 : a 8 = 1080 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_9 : a 9 = 3200 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_10 : a 10 = 6336 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_11 : a 11 = 13824 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_12 : a 12 = 32760 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_13 : a 13 = 35280 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_14 : a 14 = 86400 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_15 : a 15 = 294912 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_16 : a 16 = 528768 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_17 : a 17 = 559872 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_18 : a 18 = 3064320 := by rw [a_eq_aL (by norm_num)]; rfl
theorem a_19 : a 19 = 3225600 := by rw [a_eq_aL (by norm_num)]; rfl

/-! ### `a u ^ 2 ≤ 8 ^ u` -/

theorem a_sq_le (u : ℕ) : a u ^ 2 ≤ 8 ^ u := by
  induction u using Nat.strong_induction_on with
  | _ u ih =>
    rcases lt_or_ge u 20 with h | h
    · interval_cases u <;>
        simp only [a_zero, a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9, a_10, a_11, a_12, a_13,
          a_14, a_15, a_16, a_17, a_18, a_19] <;> norm_num
    · have h1 := a_le_two_pow_mul u
      have h2 := ih (u / 2) (by omega)
      have h3 := pi_bound u h
      calc a u ^ 2 ≤ (2 ^ (oddPrimes (2 * u + 2)).card * a (u / 2)) ^ 2 := Nat.pow_le_pow_left h1 2
        _ = (2 ^ 2) ^ (oddPrimes (2 * u + 2)).card * a (u / 2) ^ 2 := by
          rw [mul_pow, pow_right_comm]
        _ ≤ (2 ^ 2) ^ (oddPrimes (2 * u + 2)).card * (2 ^ 3) ^ (u / 2) :=
          Nat.mul_le_mul_left _ h2
        _ = 2 ^ (2 * (oddPrimes (2 * u + 2)).card + 3 * (u / 2)) := by
          rw [← pow_mul, ← pow_mul, ← pow_add]
        _ ≤ 2 ^ (3 * u) := Nat.pow_le_pow_right (by norm_num) (by omega)
        _ = 8 ^ u := by
          rw [pow_mul]
          norm_num

theorem a_le (u : ℕ) : (a u : ℚ) / 4 ^ u ≤ (5 / 7) ^ u := by
  have h1 : (a u : ℚ) ^ 2 ≤ 8 ^ u := by exact_mod_cast a_sq_le u
  have h2 : (8 : ℚ) ^ u ≤ ((20 / 7) ^ u) ^ 2 := by
    rw [← pow_mul, mul_comm, pow_mul]
    apply pow_le_pow_left₀ (by norm_num)
    norm_num
  have h3 : (a u : ℚ) ≤ (20 / 7) ^ u :=
    (sq_le_sq₀ (by positivity) (by positivity)).1 (h1.trans h2)
  rw [div_le_iff₀ (by positivity), ← mul_pow]
  norm_num
  exact h3

/-! ### The tail -/

theorem tail (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t) (U₀ n : ℕ) :
    part T (U₀ + n) ≤ W U₀ + 5 / 2 * (5 / 7) ^ U₀ - 5 / 2 * (5 / 7) ^ (U₀ + n) := by
  induction n with
  | zero =>
    have := part_le_W T hT U₀
    rw [Nat.add_zero]
    linarith
  | succ n ih =>
    have hT' : ∀ t ∈ T, ¬ 2 ∣ t := fun t ht => (hT t ht).1
    rw [← add_assoc, part_succ T hT' (U₀ + n)]
    have h1 : (lay T (U₀ + n + 1) : ℚ) / 4 ^ (U₀ + n + 1) ≤ (5 / 7) ^ (U₀ + n + 1) := by
      have hl : lay T (U₀ + n + 1) ≤ a (U₀ + n + 1) := by
        have h3 := card_filter_add_one_le T hT (U₀ + n + 1)
        have h4 : lay T (U₀ + n + 1) ≤ (T.filter fun t => μ t ≤ 2 * (U₀ + n + 1)).card := by
          apply Finset.card_le_card
          intro t ht
          rw [Finset.mem_filter] at ht ⊢
          exact ⟨ht.1, ht.2.le⟩
        omega
      calc (lay T (U₀ + n + 1) : ℚ) / 4 ^ (U₀ + n + 1)
          ≤ (a (U₀ + n + 1) : ℚ) / 4 ^ (U₀ + n + 1) := by
            apply div_le_div_of_nonneg_right _ (by positivity)
            exact_mod_cast hl
        _ ≤ (5 / 7) ^ (U₀ + n + 1) := a_le _
    have h2 : (5 / 7 : ℚ) ^ (U₀ + n + 1) =
        5 / 2 * (5 / 7) ^ (U₀ + n) - 5 / 2 * (5 / 7) ^ (U₀ + n + 1) := by
      rw [pow_succ]
      ring
    linarith

/-- the bound for the whole sum, with the layers up to `U₀` counted exactly -/
theorem sum_le (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t) (U₀ : ℕ) :
    ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t ≤ W U₀ + 5 / 2 * (5 / 7) ^ U₀ := by
  have h := tail T hT U₀ (T.sup μ)
  have hall : T.filter (fun t => μ t ≤ 2 * (U₀ + T.sup μ)) = T := by
    apply Finset.filter_true_of_mem
    intro t ht
    have : μ t ≤ T.sup μ := Finset.le_sup ht
    omega
  unfold part at h
  rw [hall] at h
  have hpos : (0 : ℚ) ≤ 5 / 2 * (5 / 7) ^ (U₀ + T.sup μ) := by positivity
  linarith

/-- the bound for a sum all of whose terms have `μ t ≤ 2 * U` -/
theorem sum_le_W (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t) (U : ℕ)
    (hU : ∀ t ∈ T, μ t ≤ 2 * U) : ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t ≤ W U := by
  have h := part_le_W T hT U
  unfold part at h
  rwa [Finset.filter_true_of_mem hU] at h

/-! ### The numbers -/

theorem W_0 : W 0 = 0 := by
  unfold W
  rw [Finset.sum_range_zero]

theorem W_1 : W 1 = 1 / 4 := by
  norm_num [W, Finset.sum_range_succ, a_zero, a_1]

theorem W_2 : W 2 = 1 / 2 := by
  norm_num [W, Finset.sum_range_succ, a_zero, a_1, a_2]

theorem W_3 : W 3 = 21 / 32 := by
  norm_num [W, Finset.sum_range_succ, a_zero, a_1, a_2, a_3]

theorem W_4 : W 4 = 91 / 128 := by
  norm_num [W, Finset.sum_range_succ, a_zero, a_1, a_2, a_3, a_4]

theorem W_5 : W 5 = 385 / 512 := by
  norm_num [W, Finset.sum_range_succ, a_zero, a_1, a_2, a_3, a_4, a_5]

/-- the layers up to `u = 19` and the tail beyond them -/
theorem W_19 : W 19 + 5 / 2 * (5 / 7) ^ 19 < 1 + 1 / 16 - 429 / 2048 := by
  norm_num [W, Finset.sum_range_succ, a_zero, a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9, a_10,
    a_11, a_12, a_13, a_14, a_15, a_16, a_17, a_18, a_19]

/-- the six cases of an even `m ≤ 12` -/
theorem small_cases (m : ℕ) (h : m = 2 ∨ m = 4 ∨ m = 6 ∨ m = 8 ∨ m = 10 ∨ m = 12) :
    (m.choose (m / 2) : ℚ) / 2 ^ m + W ((m - 2) / 2) < 1 := by
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl
  · rw [show Nat.choose 2 (2 / 2) = 2 by decide, show (2 - 2) / 2 = 0 by norm_num, W_0]
    norm_num
  · rw [show Nat.choose 4 (4 / 2) = 6 by decide, show (4 - 2) / 2 = 1 by norm_num, W_1]
    norm_num
  · rw [show Nat.choose 6 (6 / 2) = 20 by decide, show (6 - 2) / 2 = 2 by norm_num, W_2]
    norm_num
  · rw [show Nat.choose 8 (8 / 2) = 70 by decide, show (8 - 2) / 2 = 3 by norm_num, W_3]
    norm_num
  · rw [show Nat.choose 10 (10 / 2) = 252 by decide, show (10 - 2) / 2 = 4 by norm_num, W_4]
    norm_num
  · rw [show Nat.choose 12 (12 / 2) = 924 by decide, show (12 - 2) / 2 = 5 by norm_num, W_5]
    norm_num

/-- the share `(2k choose k) / 4^k` is at most `429/2048` from `k = 7` on -/
theorem central_le (k : ℕ) (hk : 7 ≤ k) : ((2 * k).choose k : ℚ) / 2 ^ (2 * k) ≤ 429 / 2048 := by
  induction k, hk using Nat.le_induction with
  | base =>
    rw [show Nat.choose (2 * 7) 7 = 3432 by decide]
    norm_num
  | succ k hk ih =>
    have h := Nat.succ_mul_centralBinom_succ k
    rw [Nat.centralBinom_eq_two_mul_choose, Nat.centralBinom_eq_two_mul_choose] at h
    have h' : ((k : ℚ) + 1) * ((2 * (k + 1)).choose (k + 1) : ℚ) =
        2 * (2 * k + 1) * ((2 * k).choose k : ℚ) := by exact_mod_cast h
    have hq : (0 : ℚ) < 2 ^ (2 * k) := by positivity
    have e : (2 : ℚ) ^ (2 * (k + 1)) = 4 * 2 ^ (2 * k) := by
      rw [mul_add, pow_add]
      norm_num
      ring
    rw [div_le_iff₀ (by positivity)] at ih ⊢
    rw [e]
    have hk0 : (0 : ℚ) ≤ k := Nat.cast_nonneg k
    have h5 : ((k : ℚ) + 1) * ((2 * (k + 1)).choose (k + 1) : ℚ) ≤
        ((k : ℚ) + 1) * (429 / 2048 * (4 * 2 ^ (2 * k))) := by
      rw [h']
      nlinarith [mul_le_mul_of_nonneg_left ih (by positivity : (0 : ℚ) ≤ 2 * (2 * k + 1)),
        mul_nonneg hk0 hq.le]
    exact le_of_mul_le_mul_left h5 (by positivity)

theorem mu_three : μ 3 = 2 := by
  simp [μ, Nat.Prime.primeFactors Nat.prime_three, Nat.Prime.factorization_self Nat.prime_three]

end SumAux

/-- **N1 (the sum).**  For `m ≥ 1` and every finite set `T` of odd numbers `t > 1` with `μ t ≤ m - 1`: if `m` is odd,
`∑_{t ∈ T} (1/2)^(μ t) < 1`; if `m` is even,
`m.choose (m/2) / 2^m + ∑_{t ∈ T} (1/2)^(μ t) - (if 3 ∈ T ∧ 14 ≤ m then 1/16 else 0) < 1`.
(`lhsN1 m T` is the left side in both cases.) -/
theorem lhsN1_lt_one (m : ℕ) (hm : 1 ≤ m) (T : Finset ℕ)
    (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t ∧ μ t + 1 ≤ m) : lhsN1 m T < 1 := by
  have hT' : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t := fun t ht => ⟨(hT t ht).1, (hT t ht).2.1⟩
  have hsum := SumAux.sum_le T hT' 19
  have hnum := SumAux.W_19
  unfold lhsN1
  by_cases hev : Even m
  · rw [ite_eq_left hev]
    obtain ⟨k, hk⟩ := id hev
    rcases lt_or_ge m 14 with h14 | h14
    · -- even `m ≤ 12`: no tail
      have hno : ¬ (Even m ∧ 3 ∈ T ∧ 14 ≤ m) := fun h => by omega
      rw [ite_eq_right hno, sub_zero]
      have hW : ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t ≤ SumAux.W ((m - 2) / 2) := by
        apply SumAux.sum_le_W T hT'
        intro t ht
        obtain ⟨j, hj⟩ := SumAux.mu_even (hT t ht).1
        have := (hT t ht).2.2
        omega
      have hs := SumAux.small_cases m (by omega)
      linarith
    · -- even `m ≥ 14`
      have hc : (m.choose (m / 2) : ℚ) / 2 ^ m ≤ 429 / 2048 := by
        have h := SumAux.central_le k (by omega)
        have e1 : m / 2 = k := by omega
        have e2 : m = 2 * k := by omega
        rw [e1, e2]
        exact h
      by_cases h3 : 3 ∈ T
      · rw [ite_eq_left (⟨hev, h3, h14⟩ : Even m ∧ 3 ∈ T ∧ 14 ≤ m)]
        linarith
      · have hno : ¬ (Even m ∧ 3 ∈ T ∧ 14 ≤ m) := fun h => h3 h.2.1
        rw [ite_eq_right hno, sub_zero]
        have hT3 : ∀ t ∈ insert 3 T, ¬ 2 ∣ t ∧ 1 < t := by
          intro t ht
          rw [Finset.mem_insert] at ht
          rcases ht with rfl | ht
          · exact ⟨by decide, by norm_num⟩
          · exact hT' t ht
        have hsum3 := SumAux.sum_le (insert 3 T) hT3 19
        have e : (1 / 2 : ℚ) ^ 2 = 1 / 4 := by norm_num
        rw [Finset.sum_insert h3, SumAux.mu_three, e] at hsum3
        linarith
  · -- odd `m`
    have hno : ¬ (Even m ∧ 3 ∈ T ∧ 14 ≤ m) := fun h => hev h.1
    rw [ite_eq_right hev, ite_eq_right hno]
    linarith

end Pnq
