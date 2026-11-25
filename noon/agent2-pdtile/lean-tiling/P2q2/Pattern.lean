/-
`ZMod (p^2 * q^2)`: the Coven–Meyerowitz conditions in terms of the eight zeros, and the divisibility `k ∣ |A|`.
-/
import P2q2.LPDefs
import Pqr.CM

open Finset

namespace P2q2

open Pqr

variable (p q : ℕ) [Fact p.Prime] [Fact q.Prime]

/-! Helper lemmas live in the namespace `P2q2.Pattern`, so that their names cannot clash with those of the
other files of the project. -/

namespace Pattern

variable {p q}

/-! ### The divisors and the prime powers dividing `p^2 * q^2` -/

theorem M_ne_zero : p ^ 2 * q ^ 2 ≠ 0 :=
  Nat.mul_ne_zero (pow_ne_zero _ (Fact.out : p.Prime).ne_zero) (pow_ne_zero _ (Fact.out : q.Prime).ne_zero)

theorem coprime_pow (hpq : p ≠ q) (a b : ℕ) : Nat.Coprime (p ^ a) (q ^ b) :=
  Nat.Coprime.pow _ _ ((Nat.coprime_primes Fact.out Fact.out).2 hpq)

/-- the divisors of `p^2 * q^2` are the `p^l * q^m`, `l, m ≤ 2` -/
theorem dvd_M {d : ℕ} (hd : d ∣ p ^ 2 * q ^ 2) : ∃ l m, l ≤ 2 ∧ m ≤ 2 ∧ d = p ^ l * q ^ m := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  obtain ⟨d1, d2, h1, h2, hdd⟩ := Nat.dvd_mul.1 hd
  obtain ⟨l, hl, rfl⟩ := (Nat.dvd_prime_pow hp).1 h1
  obtain ⟨m, hm, rfl⟩ := (Nat.dvd_prime_pow hq).1 h2
  exact ⟨l, m, hl, hm, hdd.symm⟩

/-- the powers `p^l`, `1 ≤ l ≤ 2`, are prime powers dividing `p^2 * q^2` -/
theorem pow_left_mem {l : ℕ} (h1 : 1 ≤ l) (h2 : l ≤ 2) : p ^ l ∈ primePowers (p ^ 2 * q ^ 2) := by
  have hp : p.Prime := Fact.out
  rw [DigitSets.mem_primePowers_iff M_ne_zero]
  exact ⟨(pow_dvd_pow p h2).trans (dvd_mul_right _ _), (isPrimePow_nat_iff _).2 ⟨p, l, hp, h1, rfl⟩⟩

/-- the powers `q^m`, `1 ≤ m ≤ 2`, are prime powers dividing `p^2 * q^2` -/
theorem pow_right_mem {m : ℕ} (h1 : 1 ≤ m) (h2 : m ≤ 2) : q ^ m ∈ primePowers (p ^ 2 * q ^ 2) := by
  have hq : q.Prime := Fact.out
  rw [DigitSets.mem_primePowers_iff M_ne_zero]
  exact ⟨(pow_dvd_pow q h2).trans (dvd_mul_left _ _), (isPrimePow_nat_iff _).2 ⟨q, m, hq, h1, rfl⟩⟩

/-- the prime powers dividing `p^2 * q^2` are `p`, `p^2`, `q`, `q^2` -/
theorem mem_primePowers (hpq : p ≠ q) (s : ℕ) :
    s ∈ primePowers (p ^ 2 * q ^ 2) ↔ s = p ∨ s = p ^ 2 ∨ s = q ∨ s = q ^ 2 := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  constructor
  · intro hs
    obtain ⟨hdvd, hpp⟩ := (DigitSets.mem_primePowers_iff M_ne_zero).1 hs
    obtain ⟨r, k, hr, hk, hs⟩ := (isPrimePow_nat_iff s).1 hpp
    rw [← hs] at hdvd
    have hrdvd : r ∣ p ^ 2 * q ^ 2 := (dvd_pow_self r hk.ne').trans hdvd
    rcases (Nat.Prime.dvd_mul hr).1 hrdvd with h | h
    · have hrp : r = p := (Nat.prime_dvd_prime_iff_eq hr hp).1 (hr.dvd_of_dvd_pow h)
      rw [hrp] at hdvd hs
      have hk2 : k ≤ 2 :=
        (Nat.pow_dvd_pow_iff_le_right hp.one_lt).1 ((coprime_pow hpq k 2).dvd_of_dvd_mul_right hdvd)
      have hk' : k = 1 ∨ k = 2 := by omega
      rcases hk' with rfl | rfl
      · exact Or.inl (by rw [← hs, pow_one])
      · exact Or.inr (Or.inl hs.symm)
    · have hrq : r = q := (Nat.prime_dvd_prime_iff_eq hr hq).1 (hr.dvd_of_dvd_pow h)
      rw [hrq] at hdvd hs
      have hk2 : k ≤ 2 :=
        (Nat.pow_dvd_pow_iff_le_right hq.one_lt).1 ((coprime_pow hpq 2 k).symm.dvd_of_dvd_mul_left hdvd)
      have hk' : k = 1 ∨ k = 2 := by omega
      rcases hk' with rfl | rfl
      · exact Or.inr (Or.inr (Or.inl (by rw [← hs, pow_one])))
      · exact Or.inr (Or.inr (Or.inr hs.symm))
  · rintro (rfl | rfl | rfl | rfl)
    · simpa using pow_left_mem (p := s) (q := q) (l := 1) le_rfl one_le_two
    · exact pow_left_mem one_le_two le_rfl
    · simpa using pow_right_mem (p := p) (q := s) (m := 1) le_rfl one_le_two
    · exact pow_right_mem one_le_two le_rfl

/-! ### Exact divisibility -/

theorem exactDiv_self {s : ℕ} (hs : 0 < s) : ExactDiv s s :=
  ⟨dvd_rfl, by rw [Nat.div_self hs]; exact Nat.coprime_one_right _⟩

theorem exactDiv_left (hpq : p ≠ q) (l m : ℕ) : ExactDiv (p ^ l) (p ^ l * q ^ m) := by
  have hp : p.Prime := Fact.out
  refine ⟨dvd_mul_right _ _, ?_⟩
  rw [Nat.mul_div_cancel_left _ (Nat.pow_pos hp.pos)]
  exact coprime_pow hpq l m

theorem exactDiv_right (hpq : p ≠ q) (l m : ℕ) : ExactDiv (q ^ m) (p ^ l * q ^ m) := by
  have hq : q.Prime := Fact.out
  refine ⟨dvd_mul_left _ _, ?_⟩
  rw [Nat.mul_div_cancel _ (Nat.pow_pos hq.pos)]
  exact (coprime_pow hpq l m).symm

/-! ### The pattern, indexed by the exponents -/

/-- `PatA` for the zeros of `A`, uniformly in the exponents `1 ≤ l, m ≤ 2` -/
theorem patA_cases (A : Finset (ZMod (p ^ 2 * q ^ 2)))
    (hpat : PatA (ZeroAt A q) (ZeroAt A (q ^ 2)) (ZeroAt A p) (ZeroAt A (p * q)) (ZeroAt A (p * q ^ 2))
      (ZeroAt A (p ^ 2)) (ZeroAt A (p ^ 2 * q)) (ZeroAt A (p ^ 2 * q ^ 2))) :
    (∀ l m, 1 ≤ l → l ≤ 2 → 1 ≤ m → m ≤ 2 →
      ZeroAt A (p ^ l * q ^ m) → ZeroAt A (p ^ l) ∨ ZeroAt A (q ^ m)) ∧
    (∀ l m, 1 ≤ l → l ≤ 2 → 1 ≤ m → m ≤ 2 →
      ZeroAt A (p ^ l) → ZeroAt A (q ^ m) → ZeroAt A (p ^ l * q ^ m)) := by
  obtain ⟨h1, h2, h3, h4, h5, h6, h7, h8⟩ := hpat
  constructor
  · intro l m hl1 hl2 hm1 hm2
    interval_cases l <;> interval_cases m <;> (try simp only [pow_one]) <;> assumption
  · intro l m hl1 hl2 hm1 hm2
    interval_cases l <;> interval_cases m <;> (try simp only [pow_one]) <;> assumption

/-! ### The product over `S_A` -/

theorem primePowers_eq (hpq : p ≠ q) : primePowers (p ^ 2 * q ^ 2) = {p, p ^ 2, q, q ^ 2} := by
  ext s
  rw [mem_primePowers hpq]
  simp

theorem ne_sq_self : p ≠ p ^ 2 := by
  have hp : p.Prime := Fact.out
  intro h
  have h2 : p ^ 1 = p ^ 2 := by rw [pow_one]; exact h
  have := Nat.pow_right_injective hp.two_le h2
  omega

theorem ne_sq_of_ne (hpq : p ≠ q) : p ≠ q ^ 2 := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  intro h
  have hdvd : q ∣ p := by
    rw [h]
    exact dvd_pow_self q two_ne_zero
  exact hpq ((Nat.prime_dvd_prime_iff_eq hq hp).1 hdvd).symm

omit [Fact p.Prime] [Fact q.Prime] in
theorem sq_ne_sq (hpq : p ≠ q) : p ^ 2 ≠ q ^ 2 := fun h =>
  hpq (Nat.pow_left_injective two_ne_zero h)

open Classical in
/-- the right-hand side of (T1) in terms of the four prime-power zeros -/
theorem prod_SA (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) :
    ∏ s ∈ SA A, s.minFac = (if ZeroAt A p then p else 1) * (if ZeroAt A (p ^ 2) then p else 1) *
      (if ZeroAt A q then q else 1) * (if ZeroAt A (q ^ 2) then q else 1) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hn1 : p ∉ ({p ^ 2, q, q ^ 2} : Finset ℕ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton, not_or]
    exact ⟨ne_sq_self, hpq, ne_sq_of_ne hpq⟩
  have hn2 : p ^ 2 ∉ ({q, q ^ 2} : Finset ℕ) := by
    simp only [Finset.mem_insert, Finset.mem_singleton, not_or]
    exact ⟨(ne_sq_of_ne (Ne.symm hpq)).symm, sq_ne_sq hpq⟩
  have hn3 : q ∉ ({q ^ 2} : Finset ℕ) := by
    simp only [Finset.mem_singleton]
    exact ne_sq_self
  rw [SA, Finset.prod_filter, primePowers_eq hpq, Finset.prod_insert hn1, Finset.prod_insert hn2,
    Finset.prod_insert hn3, Finset.prod_singleton, hp.minFac_eq, hq.minFac_eq,
    hp.pow_minFac two_ne_zero, hq.pow_minFac two_ne_zero]
  ring

end Pattern

/-- A weak tile whose zero pattern satisfies (T2) and has no orphan tiles. -/
theorem tiling_of_patA (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (f : ZMod (p ^ 2 * q ^ 2) → ℝ)
    (h : WeakTiling A f)
    (hpat : PatA (ZeroAt A q) (ZeroAt A (q ^ 2)) (ZeroAt A p) (ZeroAt A (p * q)) (ZeroAt A (p * q ^ 2))
      (ZeroAt A (p ^ 2)) (ZeroAt A (p ^ 2 * q)) (ZeroAt A (p ^ 2 * q ^ 2))) :
    ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  obtain ⟨horph, hT2⟩ := Pattern.patA_cases A hpat
  refine tiling_of_T1_T2 A (T1_of_no_orphan A f h fun d hd hd1 hz => ?_) fun d hd hd1 hall => ?_
  · -- no orphan: every zero is exactly divisible by a prime-power zero
    obtain ⟨l, m, hl, hm, rfl⟩ := Pattern.dvd_M hd
    rcases Nat.eq_zero_or_pos l with rfl | hl0
    · rcases Nat.eq_zero_or_pos m with rfl | hm0
      · exact absurd (by rw [pow_zero, pow_zero, mul_one]) hd1
      · rw [pow_zero, one_mul] at hz ⊢
        exact ⟨q ^ m, (CM.mem_SA A _).2 ⟨Pattern.pow_right_mem hm0 hm, hz⟩,
          Pattern.exactDiv_self (Nat.pow_pos hq.pos)⟩
    · rcases Nat.eq_zero_or_pos m with rfl | hm0
      · rw [pow_zero, mul_one] at hz ⊢
        exact ⟨p ^ l, (CM.mem_SA A _).2 ⟨Pattern.pow_left_mem hl0 hl, hz⟩,
          Pattern.exactDiv_self (Nat.pow_pos hp.pos)⟩
      · rcases horph l m hl0 hl hm0 hm hz with hz' | hz'
        · exact ⟨p ^ l, (CM.mem_SA A _).2 ⟨Pattern.pow_left_mem hl0 hl, hz'⟩,
            Pattern.exactDiv_left hpq l m⟩
        · exact ⟨q ^ m, (CM.mem_SA A _).2 ⟨Pattern.pow_right_mem hm0 hm, hz'⟩,
            Pattern.exactDiv_right hpq l m⟩
  · -- (T2)
    obtain ⟨l, m, hl, hm, rfl⟩ := Pattern.dvd_M hd
    rcases Nat.eq_zero_or_pos l with rfl | hl0
    · rcases Nat.eq_zero_or_pos m with rfl | hm0
      · exact absurd (by rw [pow_zero, pow_zero, mul_one]) hd1
      · rw [pow_zero, one_mul] at hall ⊢
        exact hall _ (Pattern.pow_right_mem hm0 hm) (Pattern.exactDiv_self (Nat.pow_pos hq.pos))
    · rcases Nat.eq_zero_or_pos m with rfl | hm0
      · rw [pow_zero, mul_one] at hall ⊢
        exact hall _ (Pattern.pow_left_mem hl0 hl) (Pattern.exactDiv_self (Nat.pow_pos hp.pos))
      · exact hT2 l m hl0 hl hm0 hm
          (hall _ (Pattern.pow_left_mem hl0 hl) (Pattern.exactDiv_left hpq l m))
          (hall _ (Pattern.pow_right_mem hm0 hm) (Pattern.exactDiv_right hpq l m))

/-- `k = p^{#p-power zeros} q^{#q-power zeros}` is at most `|A|` (it divides it). -/
theorem kfac_le_card (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (hA : A.Nonempty) :
    kfac (ZeroAt A p) p * kfac (ZeroAt A (p ^ 2)) p * kfac (ZeroAt A q) q * kfac (ZeroAt A (q ^ 2)) q
      ≤ (A.card : ℝ) := by
  classical
  have hdvd := prod_minFac_dvd_card A
  rw [Pattern.prod_SA hpq A] at hdvd
  have hle := Nat.le_of_dvd hA.card_pos hdvd
  have hcast : ∀ (z : Prop) (r : ℕ), kfac z (r : ℝ) = ((if z then r else 1 : ℕ) : ℝ) := by
    intro z r
    by_cases hz : z
    · rw [kfac_pos z _ hz, ite_eq_left hz]
    · rw [kfac_neg z _ hz, ite_eq_right hz, Nat.cast_one]
  rw [hcast, hcast, hcast, hcast]
  exact_mod_cast hle

end P2q2
