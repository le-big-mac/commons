/-
The least-size theorem for `Z_{pⁿq}` on every larger group `Z_{pⁿq·s}`, `s ≥ 1`: among the multisets on `ZMod (p^n * q * s)` whose
cyclotomic divisors are a given pattern of divisors of `p^n * q` and no others, the least number of elements is the one the theorem
gives on `ZMod (p^n * q)`.  Also, for any `N` and odd `s`: the sizes of the multisets with exactly a given pattern of divisors of
`N` are the same on `ZMod N` and on `ZMod (N * s)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  On paper: lift along the factors 2 of `s`
first, by the lemma on signs, then along its odd prime factors.)
-/
import Pnq.MinGroup
import Pnq.Lift
import Pnq.LiftMin
import Pnq.Lift2

open Finset

namespace Pnq

namespace Lift

namespace AllAux

/-- the numbers of elements of the nonempty multisets on `ZMod M` whose mask is divisible by `Φ_d`, for `d ∣ M`, `d ≠ 1`,
exactly when `d ∈ P` (the sets of the theorems `sizes_eq`, `sizes_eq_two`, `sizes_eq_odd`, `sizes_eq_mul`) -/
def sizes (M : ℕ) [NeZero M] (P : Finset ℕ) : Set ℕ :=
  {t | ∃ w : ZMod M → ℕ, ∑ x, w x = t ∧ 0 < t ∧
      ∀ d, d ∣ M → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)}

/-- equal moduli, equal sets of sizes -/
theorem sizes_congr {M M' : ℕ} [NeZero M] [NeZero M'] (h : M = M') (P : Finset ℕ) :
    sizes M P = sizes M' P := by
  subst h
  rfl

/-- the sizes on `ZMod (N * s)`, `s` odd, by induction on `s`: one odd prime factor of `s` at a time, by `sizes_eq` -/
theorem sizes_odd {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    ∀ (s : ℕ) [NeZero s], Odd s → sizes (N * s) P = sizes N P := by
  intro s
  induction s using Nat.strong_induction_on with
  | _ s ih =>
    intro _ hs
    by_cases h1 : s = 1
    · subst h1
      exact sizes_congr (mul_one N) P
    · obtain ⟨r, hr, s', rfl⟩ := Nat.exists_prime_and_dvd h1
      have hs'0 : s' ≠ 0 := by
        rintro rfl
        exact NeZero.ne (r * 0) (mul_zero r)
      have : NeZero s' := ⟨hs'0⟩
      have : Fact r.Prime := ⟨hr⟩
      have hr2 : r ≠ 2 := by
        rintro rfl
        exact Nat.not_even_iff_odd.2 (Nat.Odd.of_mul_left hs) even_two
      have hlt : s' < r * s' := lt_mul_of_one_lt_left (Nat.pos_of_ne_zero hs'0) hr.one_lt
      have e1 : sizes (N * (r * s')) P = sizes (N * s' * r) P := sizes_congr (by ring) P
      have e2 : sizes (N * s' * r) P = sizes (N * s') P :=
        sizes_eq (N := N * s') (r := r) hr2 P fun d hd => Dvd.dvd.mul_right (hP d hd) s'
      exact e1.trans (e2.trans (ih s' hlt (Nat.Odd.of_mul_right hs)))

/-- `p^n q 2^i` is `2^k` times a product of powers of two different odd primes (if `p` or `q` is `2`, one of the two
odd primes is a spare one with exponent `0`) -/
theorem exists_form (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q) (i : ℕ) :
    ∃ p' q' : ℕ, p'.Prime ∧ q'.Prime ∧ p' ≠ 2 ∧ q' ≠ 2 ∧ p' ≠ q' ∧
      ∃ k a b : ℕ, p ^ n * q * 2 ^ i = 2 ^ k * (p' ^ a * q' ^ b) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  by_cases hp2 : p = 2
  · subst hp2
    have hq2 : q ≠ 2 := fun h => hpq h.symm
    by_cases hq3 : q = 3
    · subst hq3
      exact ⟨5, 3, by norm_num, hq, by norm_num, hq2, by norm_num, n + i, 0, 1, by ring⟩
    · exact ⟨3, q, Nat.prime_three, hq, by norm_num, hq2, fun h => hq3 h.symm, n + i, 0, 1, by ring⟩
  · by_cases hq2 : q = 2
    · subst hq2
      by_cases hp3 : p = 3
      · subst hp3
        exact ⟨3, 5, hp, by norm_num, hp2, by norm_num, by norm_num, i + 1, n, 0, by ring⟩
      · exact ⟨p, 3, hp, Nat.prime_three, hp2, by norm_num, hp3, i + 1, n, 0, by ring⟩
    · exact ⟨p, q, hp, hq, hp2, hq2, hpq, i, n, 1, by ring⟩

/-- the sizes on `ZMod (p^n q 2^j)`, by induction on `j`, by `sizes_eq_two` -/
theorem sizes_two_pow (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q) (P : Finset ℕ)
    (hP : ∀ d ∈ P, d ∣ p ^ n * q) (j : ℕ) :
    sizes (p ^ n * q * 2 ^ j) P = sizes (p ^ n * q) P := by
  induction j with
  | zero => exact sizes_congr (by ring) P
  | succ i ih =>
    obtain ⟨p', q', hp', hq', hp'2, hq'2, hpq', k, a, b, hN⟩ := exists_form p q n hpq i
    have : Fact p'.Prime := ⟨hp'⟩
    have : Fact q'.Prime := ⟨hq'⟩
    have e1 : sizes (p ^ n * q * 2 ^ (i + 1)) P = sizes (p ^ n * q * 2 ^ i * 2) P := sizes_congr (by ring) P
    have e2 : sizes (p ^ n * q * 2 ^ i * 2) P = sizes (p ^ n * q * 2 ^ i) P :=
      sizes_eq_two (N := p ^ n * q * 2 ^ i) p' q' hp'2 hq'2 hpq' k a b hN P
        fun d hd => Dvd.dvd.mul_right (hP d hd) _
    exact e1.trans (e2.trans ih)

/-- a multiset with an element has a positive number of elements -/
theorem sum_pos_of_exists {M : ℕ} [NeZero M] {w : ZMod M → ℕ} (h : ∃ x, w x ≠ 0) : 0 < ∑ x, w x := by
  obtain ⟨x, hx⟩ := h
  exact lt_of_lt_of_le (Nat.pos_of_ne_zero hx)
    (Finset.single_le_sum (fun _ _ => Nat.zero_le _) (Finset.mem_univ x))

section UpDown

variable {M M' : ℕ} [NeZero M] [NeZero M']

/-- **Going up.**  If the sets of sizes on `ZMod M'` and on `ZMod M` are equal for every pattern of divisors of `M`, a
nonempty multiset on `ZMod M` has a companion on `ZMod M'` with the same number of elements, the same `Φ_d` for the
divisors `d ≠ 1` of `M`, and no `Φ_d` for a divisor `d` of `M'` that does not divide `M`.  (Take for the pattern the
set of the divisors `d` of `M` with `Φ_d` dividing the mask.) -/
theorem exists_up (hdvd : M ∣ M')
    (h : ∀ P : Finset ℕ, (∀ d ∈ P, d ∣ M) → sizes M' P = sizes M P)
    (w : ZMod M → ℕ) (hpos : 0 < ∑ x, w x) :
    ∃ w' : ZMod M' → ℕ, ∑ y, w' y = ∑ x, w x ∧
      (∀ d, d ∣ M → d ≠ 1 →
        (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ Polynomial.cyclotomic d ℤ ∣ maskW w')) ∧
      ∀ d, d ∣ M' → ¬ d ∣ M → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  classical
  let P : Finset ℕ := (Nat.divisors M).filter fun d => Polynomial.cyclotomic d ℤ ∣ maskW w
  have hP : ∀ d ∈ P, d ∣ M := fun d hd => Nat.dvd_of_mem_divisors (Finset.mem_filter.1 hd).1
  have hmem : ∀ d, d ∣ M → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P) := fun d hd =>
    ⟨fun hc => Finset.mem_filter.2 ⟨Nat.mem_divisors.2 ⟨hd, NeZero.ne M⟩, hc⟩,
      fun hc => (Finset.mem_filter.1 hc).2⟩
  have hin : (∑ x, w x) ∈ sizes M P := ⟨w, rfl, hpos, fun d hd _ => hmem d hd⟩
  rw [← h P hP] at hin
  obtain ⟨w', hs, -, hpat⟩ := hin
  refine ⟨w', hs, fun d hd hd1 => (hmem d hd).trans (hpat d (hd.trans hdvd) hd1).symm,
    fun d hd hnd hc => ?_⟩
  have hd1 : d ≠ 1 := by
    rintro rfl
    exact hnd (one_dvd M)
  exact hnd (hP d ((hpat d hd hd1).1 hc))

/-- **Going down.**  If the sets of sizes on `ZMod M'` and on `ZMod M` are equal for every pattern of divisors of `M`, a
nonempty multiset on `ZMod M'` with no `Φ_d` for a divisor `d` of `M'` that does not divide `M` has a companion on
`ZMod M` with the same number of elements and the same `Φ_d` for the divisors `d ≠ 1` of `M`. -/
theorem exists_down
    (h : ∀ P : Finset ℕ, (∀ d ∈ P, d ∣ M) → sizes M' P = sizes M P)
    (w' : ZMod M' → ℕ) (hpos : 0 < ∑ y, w' y)
    (hnew : ∀ d, d ∣ M' → ¬ d ∣ M → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w') :
    ∃ w : ZMod M → ℕ, ∑ x, w x = ∑ y, w' y ∧
      ∀ d, d ∣ M → d ≠ 1 →
        (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ Polynomial.cyclotomic d ℤ ∣ maskW w') := by
  classical
  let P : Finset ℕ := (Nat.divisors M).filter fun d => Polynomial.cyclotomic d ℤ ∣ maskW w'
  have hP : ∀ d ∈ P, d ∣ M := fun d hd => Nat.dvd_of_mem_divisors (Finset.mem_filter.1 hd).1
  have hmem : ∀ d, d ∣ M → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P) := fun d hd =>
    ⟨fun hc => Finset.mem_filter.2 ⟨Nat.mem_divisors.2 ⟨hd, NeZero.ne M⟩, hc⟩,
      fun hc => (Finset.mem_filter.1 hc).2⟩
  have hin : (∑ y, w' y) ∈ sizes M' P := by
    refine ⟨w', rfl, hpos, fun d hd _ => ?_⟩
    by_cases hdM : d ∣ M
    · exact hmem d hdM
    · exact iff_of_false (hnew d hd hdM) fun hc => hdM (hP d hc)
  rw [h P hP] at hin
  obtain ⟨w, hs, -, hpat⟩ := hin
  exact ⟨w, hs, fun d hd hd1 => (hpat d hd hd1).trans (hmem d hd).symm⟩

end UpDown

/-- `p^ℓ ≠ 1` for a level `ℓ` in `1..n` -/
theorem pow_ne_one {p n ℓ : ℕ} (hp : p.Prime) (hℓ : ℓ ∈ Finset.Icc 1 n) : p ^ ℓ ≠ 1 :=
  (Nat.one_lt_pow (Nat.one_le_iff_ne_zero.1 (Finset.mem_Icc.1 hℓ).1) hp.one_lt).ne'

/-- `p^ℓ q ≠ 1` -/
theorem pow_mul_q_ne_one {q : ℕ} (hq : q.Prime) (p ℓ : ℕ) : p ^ ℓ * q ≠ 1 := fun h =>
  hq.ne_one (Nat.dvd_one.1 (Dvd.intro_left (p ^ ℓ) h))

section Levels

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime] {M' : ℕ} [NeZero M']

/-- `Φ_q`, for two multisets with the same `Φ_d`, `d ∣ p^n q`, `d ≠ 1` -/
theorem dvd_q_iff {w : ZMod (p ^ n * q) → ℕ} {w' : ZMod M' → ℕ}
    (h : ∀ d, d ∣ p ^ n * q → d ≠ 1 →
      (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ Polynomial.cyclotomic d ℤ ∣ maskW w')) :
    Polynomial.cyclotomic q ℤ ∣ maskW w ↔ Polynomial.cyclotomic q ℤ ∣ maskW w' :=
  h q MinGroupAux.q_dvd (Fact.out : q.Prime).ne_one

/-- the levels `ℓ` with `Φ_{p^ℓ}`, for two multisets with the same `Φ_d`, `d ∣ p^n q`, `d ≠ 1` -/
theorem levelsE_iff {w : ZMod (p ^ n * q) → ℕ} {w' : ZMod M' → ℕ}
    (h : ∀ d, d ∣ p ^ n * q → d ≠ 1 →
      (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ Polynomial.cyclotomic d ℤ ∣ maskW w'))
    {Es : Finset ℕ} (hE : Es ⊆ Finset.Icc 1 n) :
    levelsEW w = Es ↔
      ∀ ℓ ∈ Finset.Icc 1 n, (Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w' ↔ ℓ ∈ Es) := by
  rw [Aux.levelsEW_eq_iff _ hE]
  refine forall₂_congr fun ℓ hℓ => ?_
  rw [h (p ^ ℓ) (MinGroupAux.pow_dvd (Finset.mem_Icc.1 hℓ).2) (pow_ne_one Fact.out hℓ)]

/-- the levels `ℓ` with `Φ_{p^ℓ q}`, for two multisets with the same `Φ_d`, `d ∣ p^n q`, `d ≠ 1` -/
theorem levelsF_iff {w : ZMod (p ^ n * q) → ℕ} {w' : ZMod M' → ℕ}
    (h : ∀ d, d ∣ p ^ n * q → d ≠ 1 →
      (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ Polynomial.cyclotomic d ℤ ∣ maskW w'))
    {Fs : Finset ℕ} (hF : Fs ⊆ Finset.Icc 1 n) :
    levelsFW w = Fs ↔
      ∀ ℓ ∈ Finset.Icc 1 n, (Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w' ↔ ℓ ∈ Fs) := by
  rw [Aux.levelsFW_eq_iff _ hF]
  refine forall₂_congr fun ℓ hℓ => ?_
  rw [h (p ^ ℓ * q) (MinGroupAux.pow_mul_q_dvd (Finset.mem_Icc.1 hℓ).2)
    (pow_mul_q_ne_one Fact.out p ℓ)]

/-- every level `ℓ` with `Φ_{p^ℓ q}`, for two multisets with the same `Φ_d`, `d ∣ p^n q`, `d ≠ 1` -/
theorem levelsF_all_iff {w : ZMod (p ^ n * q) → ℕ} {w' : ZMod M' → ℕ}
    (h : ∀ d, d ∣ p ^ n * q → d ≠ 1 →
      (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ Polynomial.cyclotomic d ℤ ∣ maskW w')) :
    levelsFW w = Finset.Icc 1 n ↔
      ∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w' := by
  rw [levelsF_iff h (Finset.Subset.refl _)]
  exact forall₂_congr fun ℓ hℓ => iff_true_right hℓ

end Levels

end AllAux

/-- **Sizes are the same on `ZMod (N * s)`, `s` odd, any `N`.** -/
theorem sizes_eq_odd {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (hs : Odd s) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  exact AllAux.sizes_odd P hP s hs

section All

variable (p q n s : ℕ) [Fact p.Prime] [Fact q.Prime] [NeZero s]

/-- **Sizes are the same on `ZMod (p^n * q * s)`, every `s ≥ 1`.** -/
theorem sizes_eq_mul (hpq : p ≠ q) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ p ^ n * q) :
    {t | ∃ w' : ZMod (p ^ n * q * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ p ^ n * q → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  obtain ⟨j, s', hs', rfl⟩ := Nat.exists_eq_two_pow_mul_odd (NeZero.ne s)
  have hs'0 : s' ≠ 0 := by
    rintro rfl
    exact NeZero.ne (2 ^ j * 0) (mul_zero _)
  have : NeZero s' := ⟨hs'0⟩
  have e1 : AllAux.sizes (p ^ n * q * (2 ^ j * s')) P = AllAux.sizes (p ^ n * q * 2 ^ j * s') P :=
    AllAux.sizes_congr (by ring) P
  have e2 : AllAux.sizes (p ^ n * q * 2 ^ j * s') P = AllAux.sizes (p ^ n * q * 2 ^ j) P :=
    AllAux.sizes_odd P (fun d hd => Dvd.dvd.mul_right (hP d hd) _) s' hs'
  exact e1.trans (e2.trans (AllAux.sizes_two_pow p q n hpq P hP j))

/-- **Unbalanced patterns on `ZMod (p^n * q * s)`.** -/
theorem minsize_unbalanced_mul (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {t | ∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minU p q Es Fs) := by
  have hold := minsize_unbalanced_zmod p q n hpq Es Fs hE hF
  have hsz := fun P hP => sizes_eq_mul p q n s hpq P hP
  constructor
  · obtain ⟨w, hs, h0, hEw, hFw⟩ := hold.1
    obtain ⟨w', hs', hsame, hnew⟩ := AllAux.exists_up (Nat.dvd_mul_right (p ^ n * q) s) hsz w
      (AllAux.sum_pos_of_exists (Aux.exists_ne_zero_of_not_dvd h0))
    exact ⟨w', hs'.trans hs, fun h => h0 ((AllAux.dvd_q_iff hsame).2 h),
      (AllAux.levelsE_iff hsame hE).1 hEw, (AllAux.levelsF_iff hsame hF).1 hFw, hnew⟩
  · rintro t ⟨w', hs, h0, hEw, hFw, hnew⟩
    obtain ⟨w, hs', hsame⟩ := AllAux.exists_down hsz w'
      (AllAux.sum_pos_of_exists (Aux.exists_ne_zero_of_not_dvd h0)) hnew
    exact hold.2 ⟨w, hs'.trans hs, fun h => h0 ((AllAux.dvd_q_iff hsame).1 h),
      (AllAux.levelsE_iff hsame hE).2 hEw, (AllAux.levelsF_iff hsame hF).2 hFw⟩

/-- **Balanced patterns with every `Φ_{p^ℓ q}`, on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_all_mul (hpq : p ≠ q)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {t | ∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t ∧ 0 < t ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (q * p ^ Es.card) := by
  have hold := minsize_balanced_all_zmod p q n hpq Es hE
  have hsz := fun P hP => sizes_eq_mul p q n s hpq P hP
  constructor
  · obtain ⟨w, hs, hpos, h0, hEw, hFw⟩ := hold.1
    obtain ⟨w', hs', hsame, hnew⟩ := AllAux.exists_up (Nat.dvd_mul_right (p ^ n * q) s) hsz w
      (lt_of_lt_of_eq hpos hs.symm)
    exact ⟨w', hs'.trans hs, hpos, (AllAux.dvd_q_iff hsame).1 h0,
      (AllAux.levelsE_iff hsame hE).1 hEw, (AllAux.levelsF_all_iff hsame).1 hFw, hnew⟩
  · rintro t ⟨w', hs, hpos, h0, hEw, hFw, hnew⟩
    obtain ⟨w, hs', hsame⟩ := AllAux.exists_down hsz w' (lt_of_lt_of_eq hpos hs.symm) hnew
    exact hold.2 ⟨w, hs'.trans hs, hpos, (AllAux.dvd_q_iff hsame).2 h0,
      (AllAux.levelsE_iff hsame hE).2 hEw, (AllAux.levelsF_all_iff hsame).2 hFw⟩

/-- **Balanced patterns with a first level `a0` at which `Φ_{p^a0 q} ∤ A(X)`, on `ZMod (p^n * q * s)`.** -/
theorem minsize_balanced_mul (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {t | ∃ w : ZMod (p ^ n * q * s) → ℕ, ∑ a, w a = t ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * s → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minB p q Es Fs a0) := by
  have hold := minsize_balanced_zmod p q n hpq Es Fs hE hF a0 ha1 han hlow hna
  have hsz := fun P hP => sizes_eq_mul p q n s hpq P hP
  constructor
  · obtain ⟨w, hs, h0, hEw, hFw⟩ := hold.1
    have hnd : ¬ Polynomial.cyclotomic (p ^ a0 * q) ℤ ∣ maskW w := fun h =>
      hna (((Aux.levelsFW_eq_iff w hF).1 hFw a0 (Finset.mem_Icc.2 ⟨ha1, han⟩)).1 h)
    obtain ⟨w', hs', hsame, hnew⟩ := AllAux.exists_up (Nat.dvd_mul_right (p ^ n * q) s) hsz w
      (AllAux.sum_pos_of_exists (Aux.exists_ne_zero_of_not_dvd hnd))
    exact ⟨w', hs'.trans hs, (AllAux.dvd_q_iff hsame).1 h0,
      (AllAux.levelsE_iff hsame hE).1 hEw, (AllAux.levelsF_iff hsame hF).1 hFw, hnew⟩
  · rintro t ⟨w', hs, h0, hEw, hFw, hnew⟩
    have hnd : ¬ Polynomial.cyclotomic (p ^ a0 * q) ℤ ∣ maskW w' := fun h =>
      hna ((hFw a0 (Finset.mem_Icc.2 ⟨ha1, han⟩)).1 h)
    obtain ⟨w, hs', hsame⟩ := AllAux.exists_down hsz w'
      (AllAux.sum_pos_of_exists (Aux.exists_ne_zero_of_not_dvd hnd)) hnew
    exact hold.2 ⟨w, hs'.trans hs, (AllAux.dvd_q_iff hsame).2 h0,
      (AllAux.levelsE_iff hsame hE).2 hEw, (AllAux.levelsF_iff hsame hF).2 hFw⟩

end All

end Lift

end Pnq
