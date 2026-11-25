/-
Weak tiles of `ZMod (p^n * q)` with a common weak complement have a common tiling complement.
Uses Theorem A (`Pnq`) in the form (T1), (T2), "no orphan zero".
-/
import Pnq.Main

open Finset

namespace P2q2

open Pqr

/-- (S) for two sets with a common weak complement: a nonempty set having every common zero of `A₁` and `A₂`
has at least `|A₁|` elements. -/
theorem S_bound_two {M : ℕ} [NeZero M] (A₁ A₂ A' : Finset (ZMod M)) (g : ZMod M → ℝ)
    (h₁ : WeakTiling A₁ g) (h₂ : WeakTiling A₂ g) (hA' : A'.Nonempty)
    (hZ : ∀ d, d ∣ M → d ≠ 1 → ZeroAt A₁ d → ZeroAt A₂ d → ZeroAt A' d) : A₁.card ≤ A'.card := by
  have hA : A₁.Nonempty := nonempty_of_weakTiling A₁ g h₁
  have hApos : (0 : ℝ) < A₁.card := Nat.cast_pos.2 hA.card_pos
  have hsum := card_mul_sum A₁ g h₁
  set c : ℝ := (A'.card : ℝ) / A₁.card with hc
  -- all Fourier coefficients of `1_{A'} * g - c` vanish
  have key : ∀ ξ : ZMod M,
      ∑ v, ((∑ a ∈ A', (g (v - a) : ℂ)) - c) * ZMod.stdAddChar (ξ * v) = 0 := by
    intro ξ
    simp_rw [sub_mul]
    rw [Finset.sum_sub_distrib, conv_ft, ← Finset.mul_sum, sum_stdAddChar_mul]
    by_cases hξ : ξ = 0
    · subst hξ
      rw [ite_eq_left rfl, hat_zero, ft_zero, sub_eq_zero]
      have : (A'.card : ℝ) * ∑ w, g w = c * M := by
        rw [hc, ← hsum]
        field_simp
      exact_mod_cast this
    · rw [ite_eq_right hξ, mul_zero, sub_zero]
      have hprod₁ := hat_mul_ft A₁ g h₁ ξ
      have hprod₂ := hat_mul_ft A₂ g h₂ ξ
      rw [ite_eq_right hξ] at hprod₁ hprod₂
      by_cases hFz : ft g ξ = 0
      · rw [hFz, mul_zero]
      · have hAz₁ : hat A₁ ξ = 0 := (mul_eq_zero.1 hprod₁).resolve_right hFz
        have hAz₂ : hat A₂ ξ = 0 := (mul_eq_zero.1 hprod₂).resolve_right hFz
        have hZA' : ZeroAt A' (ord ξ) :=
          hZ _ (Pqr.ord_dvd ξ) (fun h1 => hξ ((ord_eq_one_iff ξ).1 h1))
            (zeroAt_of_hat_eq_zero A₁ ξ hAz₁) (zeroAt_of_hat_eq_zero A₂ ξ hAz₂)
        rw [hZA' ξ rfl, zero_mul]
  have hg := zmod_fourier_uniq (fun v => (∑ a ∈ A', (g (v - a) : ℂ)) - c) key
  obtain ⟨v, hv⟩ := hA'
  have hv0 := congrFun hg v
  simp only [Pi.zero_apply, sub_eq_zero] at hv0
  have hv1 : ∑ a ∈ A', g (v - a) = c := by exact_mod_cast hv0
  have hge : g (v - v) ≤ ∑ a ∈ A', g (v - a) :=
    Finset.single_le_sum (f := fun a => g (v - a)) (fun a _ => h₁.1 _) hv
  rw [sub_self, h₁.2.1, hv1, hc, le_div_iff₀ hApos, one_mul] at hge
  exact_mod_cast hge

/-- Two sets with a common weak complement have the same number of elements. -/
theorem card_eq_of_common_complement {M : ℕ} [NeZero M] (A₁ A₂ : Finset (ZMod M)) (g : ZMod M → ℝ)
    (h₁ : WeakTiling A₁ g) (h₂ : WeakTiling A₂ g) : A₁.card = A₂.card := by
  have e₁ := card_mul_sum A₁ g h₁
  have e₂ := card_mul_sum A₂ g h₂
  have hM : (M : ℝ) ≠ 0 := Nat.cast_ne_zero.2 (NeZero.ne M)
  have hs : (∑ w, g w) ≠ 0 := by
    intro h0
    rw [h0, mul_zero] at e₁
    exact hM e₁.symm
  have h : (A₁.card : ℝ) = A₂.card := mul_right_cancel₀ hs (e₁.trans e₂.symm)
  exact_mod_cast h

/-- a positive number divides itself exactly -/
theorem exactDiv_self {s : ℕ} (hs : 0 < s) : ExactDiv s s :=
  ⟨dvd_rfl, by rw [Nat.div_self hs]; exact Nat.coprime_one_right _⟩

variable (p q n : ℕ) [Fact p.Prime] [Fact q.Prime]

/-- the divisors `≠ 1` of `p^n * q` -/
theorem dvd_pnq_cases {d : ℕ} (hd : d ∣ p ^ n * q) (hd1 : d ≠ 1) :
    (∃ ℓ, 1 ≤ ℓ ∧ ℓ ≤ n ∧ d = p ^ ℓ) ∨ d = q ∨ (∃ ℓ, 1 ≤ ℓ ∧ ℓ ≤ n ∧ d = p ^ ℓ * q) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  obtain ⟨d1, d2, h1, h2, hdd⟩ := Nat.dvd_mul.1 hd
  obtain ⟨ℓ, hℓ, hd1'⟩ := (Nat.dvd_prime_pow hp).1 h1
  rcases (Nat.dvd_prime hq).1 h2 with h2' | h2'
  · have hdeq : d = p ^ ℓ := by rw [← hdd, hd1', h2', mul_one]
    have hℓ1 : 1 ≤ ℓ := by
      rcases Nat.eq_zero_or_pos ℓ with h | h
      · rw [h, pow_zero] at hdeq
        exact absurd hdeq hd1
      · exact h
    exact Or.inl ⟨ℓ, hℓ1, hℓ, hdeq⟩
  · rcases Nat.eq_zero_or_pos ℓ with h | h
    · exact Or.inr (Or.inl (by rw [← hdd, hd1', h2', h, pow_zero, one_mul]))
    · exact Or.inr (Or.inr ⟨ℓ, h, hℓ, by rw [← hdd, hd1', h2']⟩)

/-- Theorem A in the form of the two Coven–Meyerowitz conditions. -/
theorem T1_T2_of_weakTiling_pnq (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) (f : ZMod (p ^ n * q) → ℝ)
    (h : WeakTiling A f) : T1 A ∧ T2 A := by
  obtain ⟨γ, hγ⟩ := Pnq.exists_stepTiling_tree hpq A f h
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hc := Pnq.step_structure hp.two_le hq.two_le ((Nat.coprime_primes hp hq).mpr hpq)
    (Pnq.treeOf A) γ hγ
  refine ⟨?_, Pnq.T2_of_tree hpq A hc.2⟩
  show A.card = ∏ s ∈ SA A, s.minFac
  rw [← Pnq.size_treeOf A, hc.1]
  by_cases h0 : Pnq.F (Pnq.treeOf A) 0
  · rw [ite_eq_left h0, Pnq.prod_SA_of_F0 hpq A h0]
  · rw [ite_eq_right h0, mul_one, Pnq.prod_SA_of_not_F0 hpq A h0]

/-- A weak tile of `ZMod (p^n * q)` has no orphan zero. -/
theorem no_orphan_of_weakTiling_pnq (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q)))
    (f : ZMod (p ^ n * q) → ℝ) (h : WeakTiling A f) :
    ∀ d, d ∣ p ^ n * q → d ≠ 1 → ZeroAt A d → ∃ s ∈ SA A, ExactDiv s d := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hcop : Nat.Coprime p q := (Nat.coprime_primes hp hq).mpr hpq
  obtain ⟨γ, hγ⟩ := Pnq.exists_stepTiling_tree hpq A f h
  have hc := Pnq.step_structure hp.two_le hq.two_le hcop (Pnq.treeOf A) γ hγ
  intro d hd hd1 hz
  have hqmem : q ∈ primePowers (p ^ n * q) := (Pnq.mem_primePowers_pnq hpq q).2 (Or.inr rfl)
  rcases dvd_pnq_cases p q n hd hd1 with ⟨ℓ, h1, hn, rfl⟩ | rfl | ⟨ℓ, h1, hn, rfl⟩
  · exact ⟨_, (CM.mem_SA A _).2 ⟨(Pnq.mem_primePowers_pnq hpq _).2 (Or.inl ⟨ℓ, h1, hn, rfl⟩), hz⟩,
      exactDiv_self (Nat.pow_pos hp.pos)⟩
  · exact ⟨_, (CM.mem_SA A _).2 ⟨hqmem, hz⟩, exactDiv_self hq.pos⟩
  · have hcop' : Nat.Coprime (p ^ ℓ) q := Nat.Coprime.pow_left _ hcop
    by_cases hzq : ZeroAt A q
    · refine ⟨q, (CM.mem_SA A _).2 ⟨hqmem, hzq⟩, dvd_mul_left _ _, ?_⟩
      rw [Nat.mul_div_cancel _ hq.pos]
      exact hcop'.symm
    by_cases hzp : ZeroAt A (p ^ ℓ)
    · refine ⟨p ^ ℓ, (CM.mem_SA A _).2
        ⟨(Pnq.mem_primePowers_pnq hpq _).2 (Or.inl ⟨ℓ, h1, hn, rfl⟩), hzp⟩, dvd_mul_right _ _, ?_⟩
      rw [Nat.mul_div_cancel_left _ (Nat.pow_pos hp.pos)]
      exact hcop'
    exfalso
    obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
    have hF : Pnq.F (Pnq.treeOf A) (m + 1) := (Pnq.F_treeOf hpq A (m + 1) h1 hn).2 hz
    have hF0 : ¬ Pnq.F (Pnq.treeOf A) 0 := fun h0 => hzq ((Pnq.F_treeOf_zero A).1 h0)
    have hE : ¬ Pnq.E (Pnq.treeOf A) (m + 1) := fun hE => hzp ((Pnq.E_treeOf A (m + 1) h1 hn).1 hE)
    have h3 := Pnq.lemma3 hp.two_le hq.two_le hcop (Pnq.treeOf A) m hF0 hF hE
    have hsize := hc.1
    rw [ite_eq_right hF0, mul_one] at hsize
    rw [hsize] at h3
    have hpos : 0 < p ^ Pnq.e (Pnq.treeOf A) := Nat.pow_pos hp.pos
    have h4 : p ^ Pnq.e (Pnq.treeOf A) * (p + q) ≤ p ^ Pnq.e (Pnq.treeOf A) * 1 := by
      rw [mul_one]
      exact h3
    have h5 : p + q ≤ 1 := Nat.le_of_mul_le_mul_left h4 hpos
    have := hp.two_le
    omega

/-- for a set `S` of prime powers dividing `p^n * q`: `q ∈ S` iff `q` divides `∏_{s ∈ S} minFac s` -/
theorem q_mem_iff_dvd_prod (hpq : p ≠ q) (S : Finset ℕ) (hS : S ⊆ primePowers (p ^ n * q)) :
    q ∈ S ↔ q ∣ ∏ s ∈ S, s.minFac := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  constructor
  · intro h
    have h' := Finset.dvd_prod_of_mem (fun s => s.minFac) h
    rwa [hq.minFac_eq] at h'
  · intro h
    obtain ⟨s, hs, hdvd⟩ := Prime.exists_mem_finset_dvd hq.prime h
    rcases (Pnq.mem_primePowers_pnq hpq s).1 (hS hs) with ⟨ℓ, h1, -, rfl⟩ | rfl
    · rw [hp.pow_minFac (by omega)] at hdvd
      exact absurd ((Nat.prime_dvd_prime_iff_eq hq hp).1 hdvd).symm hpq
    · exact hs

/-- One inclusion of `SA_eq_of_common_complement_pnq`. -/
theorem SA_subset_of_common_complement_pnq (hpq : p ≠ q) (A₁ A₂ : Finset (ZMod (p ^ n * q)))
    (g : ZMod (p ^ n * q) → ℝ) (h₁ : WeakTiling A₁ g) (h₂ : WeakTiling A₂ g) : SA A₁ ⊆ SA A₂ := by
  classical
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hM : p ^ n * q ≠ 0 := NeZero.ne _
  have hT1₁ : A₁.card = ∏ s ∈ SA A₁, s.minFac := (T1_T2_of_weakTiling_pnq p q n hpq A₁ g h₁).1
  have hT1₂ : A₂.card = ∏ s ∈ SA A₂, s.minFac := (T1_T2_of_weakTiling_pnq p q n hpq A₂ g h₂).1
  have hcard : A₁.card = A₂.card := card_eq_of_common_complement A₁ A₂ g h₁ h₂
  have hS₁ := CM.SA_subset A₁
  have hS₂ := CM.SA_subset A₂
  -- `q` is in both or in neither
  have hqiff : q ∈ SA A₁ ↔ q ∈ SA A₂ := by
    rw [q_mem_iff_dvd_prod p q n hpq _ hS₁, q_mem_iff_dvd_prod p q n hpq _ hS₂, ← hT1₁, ← hT1₂, hcard]
  have hsub : SA A₁ ∩ SA A₂ ⊆ primePowers (p ^ n * q) := Finset.inter_subset_left.trans hS₁
  have hcardT := card_digitSet (M := p ^ n * q) (SA A₁ ∩ SA A₂) hsub
  have hTne : (digitSet (p ^ n * q) (SA A₁ ∩ SA A₂)).Nonempty := by
    rw [← Finset.card_pos, hcardT]
    exact Finset.prod_pos fun s _ => Nat.minFac_pos s
  -- every common zero of `A₁` and `A₂` is a zero of the digit set of `SA A₁ ∩ SA A₂`
  have hle : A₁.card ≤ ∏ s ∈ SA A₁ ∩ SA A₂, s.minFac := by
    rw [← hcardT]
    refine S_bound_two A₁ A₂ _ g h₁ h₂ hTne fun d hd hd1 hz₁ hz₂ => ?_
    rw [zeroAt_digitSet _ hsub d hd]
    obtain ⟨s₁, hs₁, he₁⟩ := no_orphan_of_weakTiling_pnq p q n hpq A₁ g h₁ d hd hd1 hz₁
    obtain ⟨s₂, hs₂, he₂⟩ := no_orphan_of_weakTiling_pnq p q n hpq A₂ g h₂ d hd hd1 hz₂
    by_cases h12 : s₁ ∈ SA A₂
    · exact ⟨s₁, Finset.mem_inter.2 ⟨hs₁, h12⟩, he₁⟩
    by_cases h21 : s₂ ∈ SA A₁
    · exact ⟨s₂, Finset.mem_inter.2 ⟨h21, hs₂⟩, he₂⟩
    exfalso
    have hd0 : d ≠ 0 := fun h0 => hM (zero_dvd_iff.1 (h0 ▸ hd))
    rcases (Pnq.mem_primePowers_pnq hpq s₁).1 (hS₁ hs₁) with ⟨ℓ₁, h1, -, rfl⟩ | rfl
    · rcases (Pnq.mem_primePowers_pnq hpq s₂).1 (hS₂ hs₂) with ⟨ℓ₂, h2, -, rfl⟩ | rfl
      · have e1 := (DigitSets.exactDiv_pow_iff hp (by omega) hd0).1 he₁
        have e2 := (DigitSets.exactDiv_pow_iff hp (by omega) hd0).1 he₂
        rw [← e1, e2] at h12
        exact h12 hs₂
      · exact h21 (hqiff.2 hs₂)
    · exact h12 (hqiff.1 hs₁)
  -- a strictly smaller set of prime powers has a strictly smaller product
  intro s hs
  by_contra hns
  have hsplit : (∏ s ∈ SA A₁ ∩ SA A₂, s.minFac) * ∏ s ∈ SA A₁ \ SA A₂, s.minFac
      = ∏ s ∈ SA A₁, s.minFac := Finset.prod_inter_mul_prod_sdiff _ _ _
  have hs1 : s ≠ 1 := ((DigitSets.mem_primePowers_iff hM).1 (hS₁ hs)).2.ne_one
  have h2 : 2 ≤ ∏ s ∈ SA A₁ \ SA A₂, s.minFac :=
    (Nat.minFac_prime hs1).two_le.trans
      (Nat.le_of_dvd (Finset.prod_pos fun s _ => Nat.minFac_pos s)
        (Finset.dvd_prod_of_mem _ (Finset.mem_sdiff.2 ⟨hs, hns⟩)))
  have hpos : 0 < ∏ s ∈ SA A₁ ∩ SA A₂, s.minFac := Finset.prod_pos fun s _ => Nat.minFac_pos s
  rw [hT1₁, ← hsplit] at hle
  nlinarith

/-- Two weak tiles of `ZMod (p^n * q)` with a common weak complement have the same prime-power zeros. -/
theorem SA_eq_of_common_complement_pnq (hpq : p ≠ q) (A₁ A₂ : Finset (ZMod (p ^ n * q)))
    (g : ZMod (p ^ n * q) → ℝ) (h₁ : WeakTiling A₁ g) (h₂ : WeakTiling A₂ g) : SA A₁ = SA A₂ :=
  Finset.Subset.antisymm (SA_subset_of_common_complement_pnq p q n hpq A₁ A₂ g h₁ h₂)
    (SA_subset_of_common_complement_pnq p q n hpq A₂ A₁ g h₂ h₁)

/-- A family of weak tiles of `ZMod (p^n * q)` with a common weak complement has a common tiling complement. -/
theorem exists_common_complement_pnq (hpq : p ≠ q) {ι : Type*} (A : ι → Finset (ZMod (p ^ n * q)))
    (g : ZMod (p ^ n * q) → ℝ) (h : ∀ c, WeakTiling (A c) g) :
    ∃ B : Finset (ZMod (p ^ n * q)), ∀ c, IsTiling (A c) B := by
  rcases isEmpty_or_nonempty ι with hι | ⟨⟨c₀⟩⟩
  · exact ⟨∅, fun c => isEmptyElim c⟩
  · refine ⟨digitSet (p ^ n * q) (primePowers (p ^ n * q) \ SA (A c₀)), fun c => ?_⟩
    have hT := T1_T2_of_weakTiling_pnq p q n hpq (A c) g (h c)
    rw [← SA_eq_of_common_complement_pnq p q n hpq (A c) (A c₀) g (h c) (h c₀)]
    exact tiling_of_T1_T2_digitSet (A c) hT.1 hT.2

end P2q2
