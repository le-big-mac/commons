/-
`ZMod (p^2 * q^2)`: the Möbius coefficients of a step function are nine numbers, and the general facts of
`StepLam.lean` become the constraints of the nine-variable linear programme of `LPDefs.lean`.
-/
import P2q2.LPDefs
import P2q2.StepLam

open Finset

set_option linter.unusedSimpArgs false

namespace P2q2

open Pqr

variable (p q : ℕ) [Fact p.Prime] [Fact q.Prime]

/-- the nine coefficients of `μ` -/
def Nine.ofMu (μ : ℕ → ℝ) : Nine :=
  ⟨μ 1, μ q, μ (q ^ 2), μ p, μ (p * q), μ (p * q ^ 2), μ (p ^ 2), μ (p ^ 2 * q), μ (p ^ 2 * q ^ 2)⟩

/-- a `μ` with prescribed nine coefficients (zero elsewhere) -/
noncomputable def Nine.toMu (x : Nine) : ℕ → ℝ := fun d =>
  if d = 1 then x.m00 else if d = q then x.m01 else if d = q ^ 2 then x.m02
  else if d = p then x.m10 else if d = p * q then x.m11 else if d = p * q ^ 2 then x.m12
  else if d = p ^ 2 then x.m20 else if d = p ^ 2 * q then x.m21 else if d = p ^ 2 * q ^ 2 then x.m22 else 0

/-! ### Divisors of `p^a * q^b` -/

/-- the divisibility table -/
private theorem pq_dvd_iff (hpq : p ≠ q) (l m i j : ℕ) : p ^ l * q ^ m ∣ p ^ i * q ^ j ↔ l ≤ i ∧ m ≤ j := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hcop : Nat.Coprime p q := (Nat.coprime_primes hp hq).2 hpq
  constructor
  · intro h
    constructor
    · have h1 : p ^ l ∣ p ^ i * q ^ j := (Dvd.intro _ rfl).trans h
      have h2 : p ^ l ∣ p ^ i := (Nat.Coprime.pow l j hcop).dvd_of_dvd_mul_right h1
      exact (Nat.pow_dvd_pow_iff_le_right hp.one_lt).1 h2
    · have h1 : q ^ m ∣ p ^ i * q ^ j := (Dvd.intro_left _ rfl).trans h
      have h2 : q ^ m ∣ q ^ j := (Nat.Coprime.pow m i hcop.symm).dvd_of_dvd_mul_left h1
      exact (Nat.pow_dvd_pow_iff_le_right hq.one_lt).1 h2
  · rintro ⟨h1, h2⟩
    exact mul_dvd_mul (pow_dvd_pow _ h1) (pow_dvd_pow _ h2)

private theorem pq_inj (hpq : p ≠ q) {i j k l : ℕ} : p ^ i * q ^ j = p ^ k * q ^ l ↔ i = k ∧ j = l := by
  constructor
  · intro h
    have h1 := (pq_dvd_iff p q hpq i j k l).1 (dvd_of_eq h)
    have h2 := (pq_dvd_iff p q hpq k l i j).1 (dvd_of_eq h.symm)
    omega
  · rintro ⟨rfl, rfl⟩; rfl

private theorem dvd_pq_iff (a b d : ℕ) : d ∣ p ^ a * q ^ b ↔ ∃ i ≤ a, ∃ j ≤ b, d = p ^ i * q ^ j := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  rw [Nat.dvd_mul]
  constructor
  · rintro ⟨k1, k2, h1, h2, rfl⟩
    obtain ⟨i, hi, rfl⟩ := (Nat.dvd_prime_pow hp).1 h1
    obtain ⟨j, hj, rfl⟩ := (Nat.dvd_prime_pow hq).1 h2
    exact ⟨i, hi, j, hj, rfl⟩
  · rintro ⟨i, hi, j, hj, rfl⟩
    exact ⟨p ^ i, q ^ j, pow_dvd_pow _ hi, pow_dvd_pow _ hj, rfl⟩

private theorem pq_ne_zero (a b : ℕ) : p ^ a * q ^ b ≠ 0 :=
  mul_ne_zero (pow_ne_zero _ (Fact.out : p.Prime).ne_zero) (pow_ne_zero _ (Fact.out : q.Prime).ne_zero)

/-- a sum over the divisors of `p^a * q^b` is a double sum over the exponents -/
private theorem sum_divisors_pq (hpq : p ≠ q) (a b : ℕ) (F : ℕ → ℝ) :
    ∑ d ∈ (p ^ a * q ^ b).divisors, F d =
      ∑ i ∈ range (a + 1), ∑ j ∈ range (b + 1), F (p ^ i * q ^ j) := by
  have : (p ^ a * q ^ b).divisors =
      ((range (a + 1)) ×ˢ (range (b + 1))).image (fun ij : ℕ × ℕ => p ^ ij.1 * q ^ ij.2) := by
    ext d
    simp only [Nat.mem_divisors, mem_image, mem_product, mem_range, Prod.exists]
    rw [dvd_pq_iff]
    constructor
    · rintro ⟨⟨i, hi, j, hj, rfl⟩, -⟩
      exact ⟨i, j, ⟨by omega, by omega⟩, rfl⟩
    · rintro ⟨i, j, ⟨hi, hj⟩, rfl⟩
      exact ⟨⟨i, by omega, j, by omega, rfl⟩, pq_ne_zero p q a b⟩
  rw [this, sum_image, sum_product]
  rintro ⟨i, j⟩ - ⟨k, l⟩ - h
  simp only at h
  obtain ⟨rfl, rfl⟩ := (pq_inj p q hpq).1 h
  rfl

/-! ### The transform at the nine orders -/

private theorem lam_pq (hpq : p ≠ q) (μ : ℕ → ℝ) (l m : ℕ) :
    Lam (p ^ 2 * q ^ 2) μ (p ^ l * q ^ m) =
      ∑ i ∈ range 3, ∑ j ∈ range 3,
        if l ≤ i ∧ m ≤ j then μ (p ^ i * q ^ j) * ((p : ℝ) ^ (2 - i) * (q : ℝ) ^ (2 - j)) else 0 := by
  unfold Lam
  rw [sum_divisors_pq p q hpq 2 2]
  refine sum_congr rfl fun i hi => sum_congr rfl fun j hj => ?_
  have hi' : i ≤ 2 := by simp at hi; omega
  have hj' : j ≤ 2 := by simp at hj; omega
  have h0 : 0 < p ^ i * q ^ j := Nat.pos_of_ne_zero (pq_ne_zero p q i j)
  have : (p ^ 2 * q ^ 2) / (p ^ i * q ^ j) = p ^ (2 - i) * q ^ (2 - j) := by
    apply Nat.div_eq_of_eq_mul_left h0
    calc p ^ 2 * q ^ 2 = p ^ (2 - i + i) * q ^ (2 - j + j) := by
          rw [Nat.sub_add_cancel hi', Nat.sub_add_cancel hj']
      _ = _ := by rw [pow_add, pow_add]; ring
  simp only [pq_dvd_iff p q hpq, this]
  push_cast
  rfl

theorem Nine.lam_00 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (1) = (Nine.ofMu p q μ).L00 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 0 0
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L00, Nine.ofMu]
  ring

theorem Nine.lam_01 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (q) = (Nine.ofMu p q μ).L01 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 0 1
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L01, Nine.ofMu]
  ring

theorem Nine.lam_02 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (q ^ 2) = (Nine.ofMu p q μ).L02 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 0 2
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L02, Nine.ofMu]
  ring

theorem Nine.lam_10 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (p) = (Nine.ofMu p q μ).L10 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 1 0
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L10, Nine.ofMu]
  ring

theorem Nine.lam_11 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (p * q) = (Nine.ofMu p q μ).L11 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 1 1
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L11, Nine.ofMu]
  ring

theorem Nine.lam_12 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (p * q ^ 2) = (Nine.ofMu p q μ).L12 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 1 2
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L12, Nine.ofMu]
  ring

theorem Nine.lam_20 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (p ^ 2) = (Nine.ofMu p q μ).L20 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 2 0
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L20, Nine.ofMu]
  ring

theorem Nine.lam_21 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (p ^ 2 * q) = (Nine.ofMu p q μ).L21 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 2 1
  simp only [pow_zero, pow_one, one_mul, mul_one] at h
  rw [h]
  simp [sum_range_succ, Nine.L21, Nine.ofMu]
  ring

theorem Nine.lam_22 (hpq : p ≠ q) (μ : ℕ → ℝ) :
    Lam (p ^ 2 * q ^ 2) μ (p ^ 2 * q ^ 2) = (Nine.ofMu p q μ).L22 (p : ℝ) (q : ℝ) := by
  have h := lam_pq p q hpq μ 2 2
  rw [h]
  simp [sum_range_succ, Nine.L22, Nine.ofMu]

/-! ### The constraints of the linear programme in terms of `μ` -/

theorem Nine.admissible_ofMu_iff (hpq : p ≠ q) (μ : ℕ → ℝ) :
    (Nine.ofMu p q μ).Admissible ↔
      (∀ g ∈ (p ^ 2 * q ^ 2).divisors, 0 ≤ ∑ d ∈ g.divisors, μ d) ∧
        ∑ d ∈ (p ^ 2 * q ^ 2).divisors, μ d = 1 := by
  have e := fun a b => sum_divisors_pq p q hpq a b μ
  have e00 := e 0 0
  have e01 := e 0 1
  have e02 := e 0 2
  have e10 := e 1 0
  have e11 := e 1 1
  have e12 := e 1 2
  have e20 := e 2 0
  have e21 := e 2 1
  have e22 := e 2 2
  simp only [pow_zero, pow_one, one_mul, mul_one, sum_range_succ, sum_range_zero, zero_add, Nat.reduceAdd]
    at e00 e01 e02 e10 e11 e12 e20 e21 e22
  unfold Nine.Admissible
  simp only [Nine.g00, Nine.g01, Nine.g02, Nine.g10, Nine.g11, Nine.g12, Nine.g20, Nine.g21, Nine.g22, Nine.ofMu]
  constructor
  · rintro ⟨h00, h01, h02, h10, h11, h12, h20, h21, h22⟩
    refine ⟨?_, by rw [e22]; linarith⟩
    intro g hg
    obtain ⟨a, ha, b, hb, rfl⟩ := (dvd_pq_iff p q 2 2 g).1 (Nat.dvd_of_mem_divisors hg)
    interval_cases a <;> interval_cases b <;> (try simp only [pow_zero, pow_one, one_mul, mul_one]) <;> linarith
  · rintro ⟨hpos, hone⟩
    have hd : ∀ a b, a ≤ 2 → b ≤ 2 → 0 ≤ ∑ d ∈ (p ^ a * q ^ b).divisors, μ d := fun a b ha hb =>
      hpos _ (Nat.mem_divisors.2 ⟨(pq_dvd_iff p q hpq a b 2 2).2 ⟨ha, hb⟩, pq_ne_zero p q 2 2⟩)
    have p00 := hd 0 0 (by norm_num) (by norm_num)
    have p01 := hd 0 1 (by norm_num) (by norm_num)
    have p02 := hd 0 2 (by norm_num) (by norm_num)
    have p10 := hd 1 0 (by norm_num) (by norm_num)
    have p11 := hd 1 1 (by norm_num) (by norm_num)
    have p12 := hd 1 2 (by norm_num) (by norm_num)
    have p20 := hd 2 0 (by norm_num) (by norm_num)
    have p21 := hd 2 1 (by norm_num) (by norm_num)
    have p22 := hd 2 2 (by norm_num) (by norm_num)
    simp only [pow_zero, pow_one, one_mul, mul_one] at p00 p01 p02 p10 p11 p12 p20 p21 p22
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> linarith

theorem Nine.vanishing_ofMu_iff (hpq : p ≠ q) (μ : ℕ → ℝ) (Z : ℕ → Prop) :
    (Nine.ofMu p q μ).Vanishing (p : ℝ) (q : ℝ) (Z q) (Z (q ^ 2)) (Z p) (Z (p * q)) (Z (p * q ^ 2)) (Z (p ^ 2)) (Z (p ^ 2 * q)) (Z (p ^ 2 * q ^ 2)) ↔
      ∀ e, e ∣ p ^ 2 * q ^ 2 → e ≠ 1 → ¬ Z e → Lam (p ^ 2 * q ^ 2) μ e = 0 := by
  constructor
  · rintro ⟨h01, h02, h10, h11, h12, h20, h21, h22⟩ e he he1 hz
    obtain ⟨l, hl, m, hm, rfl⟩ := (dvd_pq_iff p q 2 2 e).1 he
    interval_cases l <;> interval_cases m <;> (try simp only [pow_zero, pow_one, one_mul, mul_one] at he1 hz ⊢)
    · exact absurd rfl he1
    · rw [Nine.lam_01 p q hpq]; exact h01 hz
    · rw [Nine.lam_02 p q hpq]; exact h02 hz
    · rw [Nine.lam_10 p q hpq]; exact h10 hz
    · rw [Nine.lam_11 p q hpq]; exact h11 hz
    · rw [Nine.lam_12 p q hpq]; exact h12 hz
    · rw [Nine.lam_20 p q hpq]; exact h20 hz
    · rw [Nine.lam_21 p q hpq]; exact h21 hz
    · rw [Nine.lam_22 p q hpq]; exact h22 hz
  · intro h
    have hd : ∀ l m, l ≤ 2 → m ≤ 2 → ¬ (l = 0 ∧ m = 0) → ¬ Z (p ^ l * q ^ m) →
        Lam (p ^ 2 * q ^ 2) μ (p ^ l * q ^ m) = 0 := fun l m hl hm hne hz =>
      h _ ((pq_dvd_iff p q hpq l m 2 2).2 ⟨hl, hm⟩)
        (fun h1 => hne ((pq_inj p q hpq (k := 0) (l := 0)).1 (by simpa using h1))) hz
    have v01 := hd 0 1 (by norm_num) (by norm_num) (by norm_num)
    have v02 := hd 0 2 (by norm_num) (by norm_num) (by norm_num)
    have v10 := hd 1 0 (by norm_num) (by norm_num) (by norm_num)
    have v11 := hd 1 1 (by norm_num) (by norm_num) (by norm_num)
    have v12 := hd 1 2 (by norm_num) (by norm_num) (by norm_num)
    have v20 := hd 2 0 (by norm_num) (by norm_num) (by norm_num)
    have v21 := hd 2 1 (by norm_num) (by norm_num) (by norm_num)
    have v22 := hd 2 2 (by norm_num) (by norm_num) (by norm_num)
    simp only [pow_zero, pow_one, one_mul, mul_one, Nine.lam_01 p q hpq, Nine.lam_02 p q hpq, Nine.lam_10 p q hpq, Nine.lam_11 p q hpq, Nine.lam_12 p q hpq, Nine.lam_20 p q hpq, Nine.lam_21 p q hpq, Nine.lam_22 p q hpq]
      at v01 v02 v10 v11 v12 v20 v21 v22
    exact ⟨v01, v02, v10, v11, v12, v20, v21, v22⟩

/-! ### `toMu` -/

private theorem toMu_pq (hpq : p ≠ q) (x : Nine) (i j : ℕ) :
    Nine.toMu p q x (p ^ i * q ^ j) =
      if i = 0 ∧ j = 0 then x.m00 else if i = 0 ∧ j = 1 then x.m01 else if i = 0 ∧ j = 2 then x.m02
      else if i = 1 ∧ j = 0 then x.m10 else if i = 1 ∧ j = 1 then x.m11 else if i = 1 ∧ j = 2 then x.m12
      else if i = 2 ∧ j = 0 then x.m20 else if i = 2 ∧ j = 1 then x.m21 else if i = 2 ∧ j = 2 then x.m22
      else 0 := by
  have e := fun k l => pq_inj p q hpq (i := i) (j := j) (k := k) (l := l)
  have e00 := e 0 0
  have e01 := e 0 1
  have e02 := e 0 2
  have e10 := e 1 0
  have e11 := e 1 1
  have e12 := e 1 2
  have e20 := e 2 0
  have e21 := e 2 1
  have e22 := e 2 2
  simp only [pow_zero, pow_one, one_mul, mul_one] at e00 e01 e02 e10 e11 e12 e20 e21 e22
  simp only [Nine.toMu, e00, e01, e02, e10, e11, e12, e20, e21, e22]

theorem Nine.ofMu_toMu (hpq : p ≠ q) (x : Nine) : Nine.ofMu p q (Nine.toMu p q x) = x := by
  have h := toMu_pq p q hpq x
  have h00 := h 0 0
  have h01 := h 0 1
  have h02 := h 0 2
  have h10 := h 1 0
  have h11 := h 1 1
  have h12 := h 1 2
  have h20 := h 2 0
  have h21 := h 2 1
  have h22 := h 2 2
  simp at h00 h01 h02 h10 h11 h12 h20 h21 h22
  simp only [Nine.ofMu, h00, h01, h02, h10, h11, h12, h20, h21, h22]

/-! ### The main statements -/

private theorem stepFn_natCast_of_dvd {M : ℕ} [NeZero M] (μ : ℕ → ℝ) (g : ℕ) (hg : g ∣ M) :
    stepFn M μ (g : ZMod M) = ∑ d ∈ g.divisors, μ d := by
  rw [stepFn_eq_sum_gcd, ZMod.val_natCast, ← Nat.gcd_rec, Nat.gcd_eq_right hg]

/-- A weak tile of `ZMod (p^2 * q^2)` has a step complement whose nine coefficients satisfy the constraints of
the linear programme for the zero pattern of the set. -/
theorem exists_nine (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (f : ZMod (p ^ 2 * q ^ 2) → ℝ)
    (h : WeakTiling A f) :
    ∃ μ : ℕ → ℝ, WeakTiling A (stepFn (p ^ 2 * q ^ 2) μ) ∧ (Nine.ofMu p q μ).Admissible ∧
      (Nine.ofMu p q μ).Vanishing (p : ℝ) (q : ℝ) (ZeroAt A q) (ZeroAt A (q ^ 2)) (ZeroAt A p)
        (ZeroAt A (p * q)) (ZeroAt A (p * q ^ 2)) (ZeroAt A (p ^ 2)) (ZeroAt A (p ^ 2 * q))
        (ZeroAt A (p ^ 2 * q ^ 2)) ∧
      (A.card : ℝ) * (Nine.ofMu p q μ).L00 (p : ℝ) (q : ℝ) = (p : ℝ) ^ 2 * (q : ℝ) ^ 2 := by
  obtain ⟨μ, hμ⟩ := exists_stepFn A f h
  refine ⟨μ, hμ, ?_, ?_, ?_⟩
  · rw [Nine.admissible_ofMu_iff p q hpq]
    constructor
    · intro g hg
      rw [← stepFn_natCast_of_dvd μ g (Nat.dvd_of_mem_divisors hg)]
      exact hμ.1 _
    · rw [← stepFn_natCast_of_dvd μ (p ^ 2 * q ^ 2) dvd_rfl, ZMod.natCast_self]
      exact hμ.2.1
  · exact (Nine.vanishing_ofMu_iff p q hpq μ (ZeroAt A)).2
      fun e he he1 hz => lam_eq_zero_of_not_zeroAt A μ hμ e he he1 hz
  · rw [← Nine.lam_00 p q hpq, card_mul_lam_one A μ hμ]
    push_cast
    ring

set_option linter.unusedVariables false in
/-- On the units the step function is the coefficient `μ 1`. -/
theorem stepFn_unit (hpq : p ≠ q) (μ : ℕ → ℝ) (y : ZMod (p ^ 2 * q ^ 2)) (hp : ¬ p ∣ y.val) (hq : ¬ q ∣ y.val) :
    stepFn (p ^ 2 * q ^ 2) μ y = μ 1 := by
  have hp' : Nat.Coprime p y.val := (Nat.Prime.coprime_iff_not_dvd Fact.out).2 hp
  have hq' : Nat.Coprime q y.val := (Nat.Prime.coprime_iff_not_dvd Fact.out).2 hq
  have hg : y.val.gcd (p ^ 2 * q ^ 2) = 1 :=
    Nat.Coprime.mul_right (Nat.Coprime.pow_right 2 hp'.symm) (Nat.Coprime.pow_right 2 hq'.symm)
  rw [stepFn_eq_sum_gcd, hg]
  simp

/-- Converse: nine admissible numbers with the right Fourier zeros and mass at most `M / |A|` give a weak
complement of `A`. -/
theorem weakTiling_of_nine (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (hA : A.Nonempty) (x : Nine)
    (hadm : x.Admissible)
    (hvan : x.Vanishing (p : ℝ) (q : ℝ) (ZeroAt A q) (ZeroAt A (q ^ 2)) (ZeroAt A p)
        (ZeroAt A (p * q)) (ZeroAt A (p * q ^ 2)) (ZeroAt A (p ^ 2)) (ZeroAt A (p ^ 2 * q))
        (ZeroAt A (p ^ 2 * q ^ 2)))
    (hle : (A.card : ℝ) * x.L00 (p : ℝ) (q : ℝ) ≤ (p : ℝ) ^ 2 * (q : ℝ) ^ 2) :
    WeakTiling A (stepFn (p ^ 2 * q ^ 2) (Nine.toMu p q x)) := by
  have hx : Nine.ofMu p q (Nine.toMu p q x) = x := Nine.ofMu_toMu p q hpq x
  have hadm' := (Nine.admissible_ofMu_iff p q hpq (Nine.toMu p q x)).1 (by rw [hx]; exact hadm)
  have hvan' := (Nine.vanishing_ofMu_iff p q hpq (Nine.toMu p q x) (ZeroAt A)).1 (by rw [hx]; exact hvan)
  refine weakTiling_stepFn_of_lam A hA _ hadm'.1 hadm'.2 hvan' ?_
  rw [Nine.lam_00 p q hpq, hx]
  push_cast
  exact hle

/-- If `m00 = m01 = m02 = 0` the step function vanishes outside the multiples of `p`. -/
theorem stepFn_toMu_of_not_dvd_p (hpq : p ≠ q) (x : Nine) (h0 : x.m00 = 0) (h1 : x.m01 = 0) (h2 : x.m02 = 0)
    (y : ZMod (p ^ 2 * q ^ 2)) (hy : ¬ p ∣ y.val) : stepFn (p ^ 2 * q ^ 2) (Nine.toMu p q x) y = 0 := by
  rw [stepFn_eq_sum_gcd]
  obtain ⟨a, ha, b, hb, hg⟩ := (dvd_pq_iff p q 2 2 _).1 (Nat.gcd_dvd_right y.val (p ^ 2 * q ^ 2))
  have ha0 : a = 0 := by
    by_contra hne
    apply hy
    have : p ∣ y.val.gcd (p ^ 2 * q ^ 2) := by
      rw [hg]; exact Dvd.dvd.mul_right (dvd_pow_self p hne) _
    exact this.trans (Nat.gcd_dvd_left _ _)
  subst ha0
  rw [hg, sum_divisors_pq p q hpq]
  interval_cases b <;> simp [sum_range_succ, toMu_pq p q hpq, h0, h1, h2]

/-- If `m00 = m10 = m20 = 0` the step function vanishes outside the multiples of `q`. -/
theorem stepFn_toMu_of_not_dvd_q (hpq : p ≠ q) (x : Nine) (h0 : x.m00 = 0) (h1 : x.m10 = 0) (h2 : x.m20 = 0)
    (y : ZMod (p ^ 2 * q ^ 2)) (hy : ¬ q ∣ y.val) : stepFn (p ^ 2 * q ^ 2) (Nine.toMu p q x) y = 0 := by
  rw [stepFn_eq_sum_gcd]
  obtain ⟨a, ha, b, hb, hg⟩ := (dvd_pq_iff p q 2 2 _).1 (Nat.gcd_dvd_right y.val (p ^ 2 * q ^ 2))
  have hb0 : b = 0 := by
    by_contra hne
    apply hy
    have : q ∣ y.val.gcd (p ^ 2 * q ^ 2) := by
      rw [hg]; exact Dvd.dvd.mul_left (dvd_pow_self q hne) _
    exact this.trans (Nat.gcd_dvd_left _ _)
  subst hb0
  rw [hg, sum_divisors_pq p q hpq]
  interval_cases a <;> simp [sum_range_succ, toMu_pq p q hpq, h0, h1, h2]

/-- For a step complement given by nine numbers, the mass is exactly `M / |A|`. -/
theorem card_mul_L00_of_weakTiling_toMu (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (x : Nine)
    (h : WeakTiling A (stepFn (p ^ 2 * q ^ 2) (Nine.toMu p q x))) :
    (A.card : ℝ) * x.L00 (p : ℝ) (q : ℝ) = (p : ℝ) ^ 2 * (q : ℝ) ^ 2 := by
  have h1 := card_mul_lam_one A _ h
  rw [Nine.lam_00 p q hpq, Nine.ofMu_toMu p q hpq] at h1
  rw [h1]
  push_cast
  ring

end P2q2
