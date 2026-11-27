/-
The statement on signs for every `n`: the sum N1′, the sum N1 of `Pnq/SignSum.lean` without the prime 3.  It is about
`μ` only: the sum of `(1/2)^(μ t)` over a finite set of numbers `t > 1` prime to 6 is below `1/8`.  In the rational
numbers.  (The value of the sum over all such `t` is `0.11856…`.)
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignSum

open Finset

namespace Pnq

namespace Sum3Aux

/-!
The route: that of `SumAux` in `Pnq/SignSum.lean`, with the prime 3 left out of the count.
`b u` is the product of `1 + u / ((p - 1) / 2)` over the primes `p` with `5 ≤ p ≤ 2 * u + 1`.
* Counting (`card_le_b`, `card_filter_add_one_le`): a finite set of numbers `t > 1` prime to 6 has at
  most `b u - 1` elements with `μ t ≤ 2 * u`.
* Layers (`layers`, `part_le_W6`): the part of the sum with `μ t ≤ 2 * U` is at most
  `W6 U = ∑_{u=1}^{U} (b u - b (u - 1)) / 4^u`.
* The tail (`tail`, `sum_le`): each layer beyond `U₀` has at most `SumAux.a u` elements (the count of
  this morning, for all odd `t`), and `SumAux.a_le : a u / 4^u ≤ (5/7)^u`, so the whole sum is at
  most `W6 U₀ + (5/2) (5/7)^U₀` for every `U₀`.
* The numbers (`b_1`, …, `b_19`, `W6_19`), with `U₀ = 19`.
-/

/-- the primes `p ≥ 5` below `B`: the odd primes below `B` other than `3` -/
def primes5 (B : ℕ) : Finset ℕ := (SumAux.oddPrimes B).filter fun p => p ≠ 3

/-- the product of `1 + u / ((p - 1) / 2)` over the primes `p` with `5 ≤ p < B` -/
def bB (B u : ℕ) : ℕ := ∏ p ∈ primes5 B, (1 + u / ((p - 1) / 2))

/-- the bound for the number of `t` prime to 6 with `μ t ≤ 2 * u` -/
def b (u : ℕ) : ℕ := bB (2 * u + 2) u

theorem mem_primes5 {B p : ℕ} : p ∈ primes5 B ↔ p ∈ SumAux.oddPrimes B ∧ p ≠ 3 := by
  simp [primes5]

theorem primes5_mono {B B' : ℕ} (h : B ≤ B') : primes5 B ⊆ primes5 B' := by
  intro p hp
  rw [mem_primes5] at hp ⊢
  exact ⟨SumAux.oddPrimes_mono h hp.1, hp.2⟩

/-- the product may be taken over the primes `≥ 5` below any bound `B ≥ 2 * u + 2` -/
theorem bB_eq_b {B u : ℕ} (h : 2 * u + 2 ≤ B) : bB B u = b u := by
  unfold b bB
  symm
  apply Finset.prod_subset (primes5_mono h)
  intro p hp hnp
  rw [mem_primes5, SumAux.mem_oddPrimes] at hp hnp
  have hge : 2 * u + 2 ≤ p := by
    by_contra hlt
    exact hnp ⟨⟨by omega, hp.1.2⟩, hp.2⟩
  obtain ⟨h1, h2⟩ := SumAux.oddPrime_half hp.1.2.1 hp.1.2.2
  have : u / ((p - 1) / 2) = 0 := Nat.div_eq_of_lt (by omega)
  rw [this, Nat.add_zero]

/-! ### Counting -/

/-- a `t` prime to 6 with `μ t ≤ 2 * u` has no prime factor outside the primes `≥ 5` below
`2 * u + 2` -/
theorem fact_eq_zero {t u p : ℕ} (ht : ¬ 2 ∣ t) (ht3 : ¬ 3 ∣ t) (hμ : μ t ≤ 2 * u)
    (hp : p ∉ primes5 (2 * u + 2)) : t.factorization p = 0 := by
  by_cases h3 : p = 3
  · rw [h3]
    exact Nat.factorization_eq_zero_of_not_dvd ht3
  · exact SumAux.fact_eq_zero ht hμ fun h => hp (mem_primes5.2 ⟨h, h3⟩)

/-- **Counting.** A finite set of numbers `t` prime to 6 with `μ t ≤ 2 * u` has at most `b u`
elements. -/
theorem card_le_b (S : Finset ℕ) (u : ℕ) (hS : ∀ t ∈ S, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ μ t ≤ 2 * u) :
    S.card ≤ b u := by
  have hcard :
      ((primes5 (2 * u + 2)).pi fun p => Finset.range (1 + u / ((p - 1) / 2))).card = b u := by
    rw [Finset.card_pi]
    unfold b bB
    apply Finset.prod_congr rfl
    intro p _
    rw [Finset.card_range]
  rw [← hcard]
  apply Finset.card_le_card_of_injOn (fun t p _ => t.factorization p)
  · intro t ht
    have ht' := hS t (Finset.mem_coe.1 ht)
    rw [Finset.mem_coe, Finset.mem_pi]
    intro p hp
    rw [mem_primes5, SumAux.mem_oddPrimes] at hp
    rw [Finset.mem_range]
    have := SumAux.fact_le ht'.2.2 hp.1.2.1 hp.1.2.2
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
    by_cases hp : p ∈ primes5 (2 * u + 2)
    · exact congrFun (congrFun heq p) hp
    · rw [fact_eq_zero h₁.1 h₁.2.1 h₁.2.2 hp, fact_eq_zero h₂.1 h₂.2.1 h₂.2.2 hp]

/-- a finite set of numbers `t > 1` prime to 6 has at most `b u - 1` elements with `μ t ≤ 2 * u` -/
theorem card_filter_add_one_le (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) (u : ℕ) :
    (T.filter fun t => μ t ≤ 2 * u).card + 1 ≤ b u := by
  have h1 : 1 ∉ T.filter fun t => μ t ≤ 2 * u := by
    intro h
    have := (hT 1 (Finset.mem_filter.1 h).1).2.2
    omega
  rw [← Finset.card_insert_of_notMem h1]
  apply card_le_b
  intro t ht
  rw [Finset.mem_insert, Finset.mem_filter] at ht
  rcases ht with rfl | ht
  · refine ⟨by decide, by decide, ?_⟩
    rw [SumAux.mu_one]
    omega
  · exact ⟨(hT t ht.1).1, (hT t ht.1).2.1, ht.2⟩

/-! ### Layers -/

/-- the partial sums `∑_{u=1}^{U} (b u - b (u-1)) / 4^u` -/
def W6 (U : ℕ) : ℚ := ∑ u ∈ Finset.range U, ((b (u + 1) : ℚ) - b u) / 4 ^ (u + 1)

theorem W6_succ (U : ℕ) : W6 (U + 1) = W6 U + ((b (U + 1) : ℚ) - b U) / 4 ^ (U + 1) :=
  Finset.sum_range_succ _ _

theorem b_zero : b 0 = 1 := by
  unfold b bB
  apply Finset.prod_eq_one
  intro p _
  rw [Nat.zero_div, Nat.add_zero]

/-- the hypothesis on `T`, weakened to the one of `SumAux` -/
theorem odd_of_prime_to_six {T : Finset ℕ} (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) :
    ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t :=
  fun t ht => ⟨(hT t ht).1, (hT t ht).2.2⟩

theorem gap_nonneg (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) (U : ℕ) :
    (0 : ℚ) ≤ ((b U : ℚ) - 1 - SumAux.cnt T U) / 4 ^ U := by
  have hc := card_filter_add_one_le T hT U
  have h1 : ((SumAux.cnt T U + 1 : ℕ) : ℚ) ≤ (b U : ℚ) := by
    unfold SumAux.cnt
    exact_mod_cast hc
  push_cast at h1
  apply div_nonneg
  · linarith
  · positivity

/-- **Layers**, in the form that survives induction. -/
theorem layers (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) (U : ℕ) :
    SumAux.part T U + ((b U : ℚ) - 1 - SumAux.cnt T U) / 4 ^ U ≤ W6 U := by
  induction U with
  | zero =>
    have hempty : T.filter (fun t => μ t ≤ 2 * 0) = ∅ := by
      apply Finset.filter_false_of_mem
      intro t ht
      have := SumAux.two_le_mu (hT t ht).1 (hT t ht).2.2
      omega
    unfold SumAux.part SumAux.cnt W6
    rw [hempty, b_zero]
    simp
  | succ U ih =>
    have hT' : ∀ t ∈ T, ¬ 2 ∣ t := fun t ht => (hT t ht).1
    have hd := gap_nonneg T hT U
    have key : SumAux.part T (U + 1) + ((b (U + 1) : ℚ) - 1 - SumAux.cnt T (U + 1)) / 4 ^ (U + 1) =
        SumAux.part T U + (((b U : ℚ) - 1 - SumAux.cnt T U) / 4 ^ U) / 4
          + ((b (U + 1) : ℚ) - b U) / 4 ^ (U + 1) := by
      rw [SumAux.part_succ T hT' U, SumAux.cnt_succ T hT' U, pow_succ]
      push_cast
      field_simp
      ring
    rw [key, W6_succ]
    linarith

theorem part_le_W6 (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) (U : ℕ) :
    SumAux.part T U ≤ W6 U := by
  have h := layers T hT U
  have hd := gap_nonneg T hT U
  linarith

/-! ### The tail -/

/-- the layers beyond `U₀`, each bounded by the count `SumAux.a` of all odd numbers -/
theorem tail (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) (U₀ n : ℕ) :
    SumAux.part T (U₀ + n) ≤ W6 U₀ + 5 / 2 * (5 / 7) ^ U₀ - 5 / 2 * (5 / 7) ^ (U₀ + n) := by
  induction n with
  | zero =>
    have := part_le_W6 T hT U₀
    rw [Nat.add_zero]
    linarith
  | succ n ih =>
    have hT' : ∀ t ∈ T, ¬ 2 ∣ t := fun t ht => (hT t ht).1
    have hT2 := odd_of_prime_to_six hT
    rw [← add_assoc, SumAux.part_succ T hT' (U₀ + n)]
    have h1 : (SumAux.lay T (U₀ + n + 1) : ℚ) / 4 ^ (U₀ + n + 1) ≤ (5 / 7) ^ (U₀ + n + 1) := by
      have hl : SumAux.lay T (U₀ + n + 1) ≤ SumAux.a (U₀ + n + 1) := by
        have h3 := SumAux.card_filter_add_one_le T hT2 (U₀ + n + 1)
        have h4 : SumAux.lay T (U₀ + n + 1) ≤
            (T.filter fun t => μ t ≤ 2 * (U₀ + n + 1)).card := by
          apply Finset.card_le_card
          intro t ht
          rw [Finset.mem_filter] at ht ⊢
          exact ⟨ht.1, ht.2.le⟩
        omega
      calc (SumAux.lay T (U₀ + n + 1) : ℚ) / 4 ^ (U₀ + n + 1)
          ≤ (SumAux.a (U₀ + n + 1) : ℚ) / 4 ^ (U₀ + n + 1) := by
            apply div_le_div_of_nonneg_right _ (by positivity)
            exact_mod_cast hl
        _ ≤ (5 / 7) ^ (U₀ + n + 1) := SumAux.a_le _
    have h2 : (5 / 7 : ℚ) ^ (U₀ + n + 1) =
        5 / 2 * (5 / 7) ^ (U₀ + n) - 5 / 2 * (5 / 7) ^ (U₀ + n + 1) := by
      rw [pow_succ]
      ring
    linarith

/-- the bound for the whole sum, with the layers up to `U₀` counted exactly -/
theorem sum_le (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) (U₀ : ℕ) :
    ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t ≤ W6 U₀ + 5 / 2 * (5 / 7) ^ U₀ := by
  have h := tail T hT U₀ (T.sup μ)
  have hall : T.filter (fun t => μ t ≤ 2 * (U₀ + T.sup μ)) = T := by
    apply Finset.filter_true_of_mem
    intro t ht
    have : μ t ≤ T.sup μ := Finset.le_sup ht
    omega
  unfold SumAux.part at h
  rw [hall] at h
  have hpos : (0 : ℚ) ≤ 5 / 2 * (5 / 7) ^ (U₀ + T.sup μ) := by positivity
  linarith

/-! ### Evaluation for `u < 20` -/

theorem primes5_forty : primes5 40 = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37].toFinset := by
  unfold primes5
  rw [SumAux.oddPrimes_forty]
  decide

/-- `b u` for `u < 20`, as a product over a list -/
def bL (u : ℕ) : ℕ :=
  ([5, 7, 11, 13, 17, 19, 23, 29, 31, 37].map fun p => 1 + u / ((p - 1) / 2)).prod

theorem b_eq_bL {u : ℕ} (h : u < 20) : b u = bL u := by
  rw [← bB_eq_b (B := 40) (by omega)]
  unfold bB bL
  rw [primes5_forty, List.prod_toFinset _ (by decide)]

theorem b_1 : b 1 = 1 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_2 : b 2 = 2 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_3 : b 3 = 4 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_4 : b 4 = 6 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_5 : b 5 = 12 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_6 : b 6 = 48 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_7 : b 7 = 48 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_8 : b 8 = 120 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_9 : b 9 = 320 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_10 : b 10 = 576 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_11 : b 11 = 1152 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_12 : b 12 = 2520 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_13 : b 13 = 2520 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_14 : b 14 = 5760 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_15 : b 15 = 18432 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_16 : b 16 = 31104 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_17 : b 17 = 31104 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_18 : b 18 = 161280 := by rw [b_eq_bL (by norm_num)]; rfl
theorem b_19 : b 19 = 161280 := by rw [b_eq_bL (by norm_num)]; rfl

/-! ### The numbers -/

/-- the layers up to `u = 19`, exactly -/
theorem W6_19_eq : W6 19 = 63653689 / 536870912 := by
  norm_num [W6, Finset.sum_range_succ, b_zero, b_1, b_2, b_3, b_4, b_5, b_6, b_7, b_8, b_9, b_10,
    b_11, b_12, b_13, b_14, b_15, b_16, b_17, b_18, b_19]

/-- the layers up to `u = 19` and the tail beyond them -/
theorem W6_19 : W6 19 + 5 / 2 * (5 / 7) ^ 19 < 1 / 8 := by
  rw [W6_19_eq]
  norm_num

end Sum3Aux

/-- **N1′ (the sum without the prime 3).**  For every finite set `T` of numbers `t > 1` divisible neither by 2 nor
by 3: `∑_{t ∈ T} (1/2)^(μ t) < 1/8`. -/
theorem sum_half_pow_mu_lt (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) :
    ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t < 1 / 8 := by
  exact lt_of_le_of_lt (Sum3Aux.sum_le T hT 19) Sum3Aux.W6_19

end Pnq
