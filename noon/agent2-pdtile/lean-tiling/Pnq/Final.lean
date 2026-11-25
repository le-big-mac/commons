/-
From (T1) and (T2) on the tree of `A ⊆ ZMod (p^n * q)` to a tiling complement, through the bridge of
`Pnq/Group.lean` and the Coven–Meyerowitz theorem of `Pqr/CM.lean`.
-/
import Pnq.Group
import Pqr.CM

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

/-! ### The prime powers dividing `p^n * q` -/

/-- a positive power of `p` is not `q` -/
theorem pow_ne_of_ne (hpq : p ≠ q) {ℓ : ℕ} (h1 : 1 ≤ ℓ) : p ^ ℓ ≠ q := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  intro h
  have hdvd : p ∣ q := by
    rw [← h]
    exact dvd_pow_self p (by omega)
  exact hpq ((Nat.prime_dvd_prime_iff_eq hp hq).1 hdvd)

/-- the prime powers dividing `p^n * q` are the `p^ℓ`, `1 ≤ ℓ ≤ n`, and `q` -/
theorem mem_primePowers_pnq (hpq : p ≠ q) (s : ℕ) :
    s ∈ Pqr.primePowers (p ^ n * q) ↔ (∃ ℓ, 1 ≤ ℓ ∧ ℓ ≤ n ∧ s = p ^ ℓ) ∨ s = q := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hM : p ^ n * q ≠ 0 := Nat.mul_ne_zero (pow_ne_zero _ hp.ne_zero) hq.ne_zero
  rw [Pqr.DigitSets.mem_primePowers_iff hM]
  constructor
  · rintro ⟨hdvd, hpp⟩
    obtain ⟨r, k, hr, hk, hs⟩ := (isPrimePow_nat_iff s).1 hpp
    rw [← hs] at hdvd
    have hrdvd : r ∣ p ^ n * q := (dvd_pow_self r hk.ne').trans hdvd
    rcases (Nat.Prime.dvd_mul hr).1 hrdvd with h | h
    · -- `r = p`
      have hrp : r = p := (Nat.prime_dvd_prime_iff_eq hr hp).1 (hr.dvd_of_dvd_pow h)
      rw [hrp] at hdvd hs
      left
      refine ⟨k, hk, ?_, hs.symm⟩
      have hcop : Nat.Coprime (p ^ k) q := Nat.Coprime.pow_left _ ((Nat.coprime_primes hp hq).2 hpq)
      exact (Nat.pow_dvd_pow_iff_le_right hp.one_lt).1 (hcop.dvd_of_dvd_mul_right hdvd)
    · -- `r = q`
      have hrq : r = q := (Nat.prime_dvd_prime_iff_eq hr hq).1 h
      rw [hrq] at hdvd hs
      right
      have hcop : Nat.Coprime (q ^ k) (p ^ n) :=
        Nat.Coprime.pow _ _ ((Nat.coprime_primes hq hp).2 (Ne.symm hpq))
      have h1 : q ^ k ∣ q ^ 1 := by
        rw [pow_one]
        exact hcop.dvd_of_dvd_mul_left hdvd
      have hk1 : k ≤ 1 := (Nat.pow_dvd_pow_iff_le_right hq.one_lt).1 h1
      have hk' : k = 1 := by omega
      rw [← hs, hk', pow_one]
  · rintro (⟨ℓ, h1, hn, rfl⟩ | rfl)
    · exact ⟨(pow_dvd_pow p hn).trans (dvd_mul_right _ _),
        (isPrimePow_nat_iff _).2 ⟨p, ℓ, hp, h1, rfl⟩⟩
    · exact ⟨dvd_mul_left _ _, hq.isPrimePow⟩

/-! ### The set `S_A` and (T1) -/

/-- the prime powers dividing `p^n * q` that are Fourier zeros of `A`, in terms of the tree of `A` -/
theorem mem_SA_pnq (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) (s : ℕ) :
    s ∈ Pqr.SA A ↔ (∃ ℓ ∈ eSet (treeOf A), s = p ^ ℓ) ∨ (s = q ∧ F (treeOf A) 0) := by
  rw [Pqr.CM.mem_SA, mem_primePowers_pnq hpq]
  constructor
  · rintro ⟨⟨ℓ, h1, hn, hs⟩ | hs, hz⟩
    · rw [hs] at hz
      exact Or.inl ⟨ℓ, (mem_eSet _ _).2 ⟨h1, hn, (E_treeOf A ℓ h1 hn).2 hz⟩, hs⟩
    · rw [hs] at hz
      exact Or.inr ⟨hs, (F_treeOf_zero A).2 hz⟩
  · rintro (⟨ℓ, hℓ, hs⟩ | ⟨hs, h0⟩)
    · obtain ⟨h1, hn, hE⟩ := (mem_eSet _ _).1 hℓ
      rw [hs]
      exact ⟨Or.inl ⟨ℓ, h1, hn, rfl⟩, (E_treeOf A ℓ h1 hn).1 hE⟩
    · rw [hs]
      exact ⟨Or.inr rfl, (F_treeOf_zero A).1 h0⟩

/-- `∏ minFac` over the powers `p^ℓ`, `ℓ ∈ S`, of `p` (all `ℓ ≥ 1`) is `p ^ |S|` -/
theorem prod_minFac_image_pow (S : Finset ℕ) (hS : ∀ ℓ ∈ S, 1 ≤ ℓ) :
    ∏ s ∈ S.image (fun ℓ => p ^ ℓ), s.minFac = p ^ S.card := by
  classical
  have hp : p.Prime := Fact.out
  rw [Finset.prod_image (fun a _ b _ h => Nat.pow_right_injective hp.two_le h),
    Finset.prod_congr rfl (fun ℓ hℓ => hp.pow_minFac (Nat.one_le_iff_ne_zero.1 (hS ℓ hℓ))),
    Finset.prod_const]

/-- `q` is not one of the powers `p^ℓ`, `ℓ ∈ eSet` -/
theorem q_notMem_image (hpq : p ≠ q) {m : ℕ} (t : Tree p q m) :
    q ∉ (eSet t).image (fun ℓ => p ^ ℓ) := by
  classical
  intro h
  obtain ⟨ℓ, hℓ, h⟩ := Finset.mem_image.1 h
  exact pow_ne_of_ne hpq ((mem_eSet _ _).1 hℓ).1 h

/-- the right-hand side of (T1) when `Φ_q ∣ A` -/
theorem prod_SA_of_F0 (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) (h0 : F (treeOf A) 0) :
    ∏ s ∈ Pqr.SA A, s.minFac = p ^ e (treeOf A) * q := by
  classical
  have hq : q.Prime := Fact.out
  have hSA : Pqr.SA A = insert q ((eSet (treeOf A)).image (fun ℓ => p ^ ℓ)) := by
    ext s
    rw [mem_SA_pnq hpq, Finset.mem_insert, Finset.mem_image]
    constructor
    · rintro (⟨ℓ, hℓ, hs⟩ | ⟨hs, -⟩)
      · exact Or.inr ⟨ℓ, hℓ, hs.symm⟩
      · exact Or.inl hs
    · rintro (hs | ⟨ℓ, hℓ, hs⟩)
      · exact Or.inr ⟨hs, h0⟩
      · exact Or.inl ⟨ℓ, hℓ, hs.symm⟩
  rw [hSA, Finset.prod_insert (q_notMem_image hpq _),
    prod_minFac_image_pow _ (fun ℓ hℓ => ((mem_eSet _ _).1 hℓ).1), hq.minFac_eq, mul_comm]
  rfl

/-- the right-hand side of (T1) when `Φ_q ∤ A` -/
theorem prod_SA_of_not_F0 (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) (h0 : ¬ F (treeOf A) 0) :
    ∏ s ∈ Pqr.SA A, s.minFac = p ^ e (treeOf A) := by
  classical
  have hSA : Pqr.SA A = (eSet (treeOf A)).image (fun ℓ => p ^ ℓ) := by
    ext s
    rw [mem_SA_pnq hpq, Finset.mem_image]
    constructor
    · rintro (⟨ℓ, hℓ, hs⟩ | ⟨-, h⟩)
      · exact ⟨ℓ, hℓ, hs.symm⟩
      · exact absurd h h0
    · rintro ⟨ℓ, hℓ, hs⟩
      exact Or.inl ⟨ℓ, hℓ, hs.symm⟩
  rw [hSA, prod_minFac_image_pow _ (fun ℓ hℓ => ((mem_eSet _ _).1 hℓ).1)]
  rfl

/-! ### (T2) -/

/-- (T2) for `A` from (T2) for its tree -/
theorem T2_of_tree (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q)))
    (hT2 : F (treeOf A) 0 → ∀ ℓ, E (treeOf A) (ℓ + 1) → F (treeOf A) (ℓ + 1)) : Pqr.T2 A := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  intro d hd hd1 hall
  obtain ⟨d1, d2, h1, h2, hdd⟩ := Nat.dvd_mul.1 hd
  obtain ⟨ℓ, hℓ, hd1'⟩ := (Nat.dvd_prime_pow hp).1 h1
  have hqmem : q ∈ Pqr.primePowers (p ^ n * q) := (mem_primePowers_pnq hpq q).2 (Or.inr rfl)
  have hpmem : 1 ≤ ℓ → p ^ ℓ ∈ Pqr.primePowers (p ^ n * q) := fun hℓ1 =>
    (mem_primePowers_pnq hpq _).2 (Or.inl ⟨ℓ, hℓ1, hℓ, rfl⟩)
  have hcop : Nat.Coprime (p ^ ℓ) q := Nat.Coprime.pow_left _ ((Nat.coprime_primes hp hq).2 hpq)
  have hself : ∀ s : ℕ, 0 < s → Pqr.ExactDiv s s := fun s hs =>
    ⟨dvd_rfl, by rw [Nat.div_self hs]; exact Nat.coprime_one_right _⟩
  rcases (Nat.dvd_prime hq).1 h2 with h2' | h2'
  · -- `d = p^ℓ`, `ℓ ≥ 1`
    have hdeq : d = p ^ ℓ := by rw [← hdd, hd1', h2', mul_one]
    have hℓ1 : 1 ≤ ℓ := by
      rcases Nat.eq_zero_or_pos ℓ with h | h
      · rw [h, pow_zero] at hdeq
        exact absurd hdeq hd1
      · exact h
    rw [hdeq] at hall ⊢
    exact hall _ (hpmem hℓ1) (hself _ (Nat.pow_pos hp.pos))
  · rcases Nat.eq_zero_or_pos ℓ with h | h
    · -- `d = q`
      have hdeq : d = q := by rw [← hdd, hd1', h2', h, pow_zero, one_mul]
      rw [hdeq] at hall ⊢
      exact hall q hqmem (hself q hq.pos)
    · -- `d = p^ℓ * q`, `ℓ ≥ 1`
      have hdeq : d = p ^ ℓ * q := by rw [← hdd, hd1', h2']
      rw [hdeq] at hall ⊢
      have hzp : Pqr.ZeroAt A (p ^ ℓ) := by
        refine hall _ (hpmem h) ⟨dvd_mul_right _ _, ?_⟩
        rw [Nat.mul_div_cancel_left _ (Nat.pow_pos hp.pos)]
        exact hcop
      have hzq : Pqr.ZeroAt A q := by
        refine hall q hqmem ⟨dvd_mul_left _ _, ?_⟩
        rw [Nat.mul_div_cancel _ hq.pos]
        exact hcop.symm
      obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
      exact (F_treeOf hpq A (m + 1) h hℓ).1
        (hT2 ((F_treeOf_zero A).2 hzq) m ((E_treeOf A (m + 1) h hℓ).2 hzp))

/-! ### The theorem -/

open Classical in
/-- **(ii)** If the tree of `A` satisfies (T1) and (T2) in the form delivered by `Pnq.counting`, then `A` tiles. -/
theorem tiling_of_tree_T1_T2 (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q)))
    (hT1 : size (treeOf A) = p ^ e (treeOf A) * (if F (treeOf A) 0 then q else 1))
    (hT2 : F (treeOf A) 0 → ∀ ℓ, E (treeOf A) (ℓ + 1) → F (treeOf A) (ℓ + 1)) :
    ∃ B : Finset (ZMod (p ^ n * q)), Pqr.IsTiling A B := by
  refine Pqr.tiling_of_T1_T2 A ?_ (T2_of_tree hpq A hT2)
  show A.card = ∏ s ∈ Pqr.SA A, s.minFac
  rw [← size_treeOf A, hT1]
  by_cases h0 : F (treeOf A) 0
  · rw [ite_eq_left h0, prod_SA_of_F0 hpq A h0]
  · rw [ite_eq_right h0, mul_one, prod_SA_of_not_F0 hpq A h0]

end Pnq
