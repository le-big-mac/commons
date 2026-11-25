/-
The Coven–Meyerowitz conditions relative to `M`, for subsets of `ZMod M`, in terms of Fourier zeros:
* `prod_minFac_dvd_card`: the product of `p` over the prime powers `p^a ∣ M` that are Fourier zeros of `A`
  divides `|A|`;
* `tiling_of_T1_T2`: (T1) and (T2) imply that `A` tiles `ZMod M` (Coven–Meyerowitz);
* `T1_of_no_orphan`: a weak tile all of whose Fourier zeros are exactly divisible by a prime power that is
  itself a Fourier zero satisfies (T1);
* `weak_tiling_tiles_prime_pow`: every weak tile of `ZMod (p^n)` is a tile.
-/
import Pqr.DigitSets

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

open Classical in
/-- the prime powers dividing `M` that are Fourier zeros of `A` (the set `S_A` of Coven and Meyerowitz) -/
noncomputable def SA (A : Finset (ZMod M)) : Finset ℕ := (primePowers M).filter (fun s => ZeroAt A s)

/-- (T1) relative to `M`: `|A| = ∏_{p^a ∈ S_A} p` -/
def T1 (A : Finset (ZMod M)) : Prop := A.card = ∏ s ∈ SA A, s.minFac

/-- (T2) relative to `M`: a divisor `d > 1` of `M` all of whose exact prime-power factors are in `S_A` is a
Fourier zero of `A` -/
def T2 (A : Finset (ZMod M)) : Prop :=
  ∀ d, d ∣ M → d ≠ 1 → (∀ s ∈ primePowers M, ExactDiv s d → ZeroAt A s) → ZeroAt A d

/-! Helper lemmas live in the namespace `Pqr.CM`, so that their names cannot clash with those of the
other files of the project. -/

namespace CM

theorem mem_SA (A : Finset (ZMod M)) (s : ℕ) : s ∈ SA A ↔ s ∈ primePowers M ∧ ZeroAt A s := by
  classical
  unfold SA
  exact Finset.mem_filter

theorem SA_subset (A : Finset (ZMod M)) : SA A ⊆ primePowers M := fun s hs => ((mem_SA A s).1 hs).1

/-! ### Splitting a residue class modulo `p^a` into `p` classes modulo `p^(a+1)` -/

/-- for `d ∣ M`: `w - k` is divisible by `d` iff the representative of `w` is congruent to `k` modulo `d` -/
theorem dvd_val_sub_natCast {d : ℕ} (hd : d ∣ M) (w : ZMod M) (k : ℕ) :
    d ∣ (w - (k : ZMod M)).val ↔ w.val ≡ k [MOD d] := by
  rw [← ZMod.natCast_eq_zero_iff, ZMod.natCast_val, ZMod.cast_sub hd, ZMod.cast_natCast hd, sub_eq_zero,
    ← ZMod.natCast_val, ZMod.natCast_eq_natCast_iff]

/-- `n ≡ t p^a (mod p^(a+1))` iff `p^a ∣ n` and the next digit of `n` in base `p` is `t` -/
theorem modEq_mul_pow_iff {p : ℕ} (hp : 0 < p) (a n t : ℕ) (ht : t < p) :
    n ≡ t * p ^ a [MOD p ^ (a + 1)] ↔ p ^ a ∣ n ∧ (n / p ^ a) % p = t := by
  have hpa : 0 < p ^ a := Nat.pow_pos hp
  constructor
  · intro h
    have h1 : p ^ a ∣ n := by
      have h2 : n ≡ t * p ^ a [MOD p ^ a] := h.of_dvd (pow_dvd_pow p (Nat.le_succ a))
      exact Nat.modEq_zero_iff_dvd.1 (h2.trans (Nat.modEq_zero_iff_dvd.2 (dvd_mul_left _ _)))
    refine ⟨h1, ?_⟩
    obtain ⟨m, rfl⟩ := h1
    rw [Nat.mul_div_cancel_left m hpa]
    have h3 : p ^ a * m ≡ p ^ a * t [MOD p ^ a * p] := by rwa [mul_comm t, pow_succ] at h
    have h4 : m ≡ t [MOD p] := Nat.ModEq.mul_left_cancel' hpa.ne' h3
    have h5 : m % p = t % p := h4
    rw [h5, Nat.mod_eq_of_lt ht]
  · rintro ⟨⟨m, rfl⟩, h2⟩
    rw [Nat.mul_div_cancel_left m hpa] at h2
    have h4 : m ≡ t [MOD p] := by
      have h5 : m % p = t % p := by rw [h2, Nat.mod_eq_of_lt ht]
      exact h5
    rw [mul_comm t, pow_succ]
    exact Nat.ModEq.mul_left' _ h4

/-- **Splitting**: a class modulo `p^a` is the disjoint union of `p` classes modulo `p^(a+1)`. -/
theorem cnt_split (A : Finset (ZMod M)) {p : ℕ} (hp : 0 < p) (a : ℕ) (h : p ^ (a + 1) ∣ M)
    (v : ZMod M) :
    cnt A (p ^ a) v = ∑ t ∈ range p, cnt A (p ^ (a + 1)) (v + ((t * p ^ a : ℕ) : ZMod M)) := by
  classical
  unfold cnt
  rw [Finset.card_eq_sum_card_fiberwise (f := fun x : ZMod M => ((x - v).val / p ^ a) % p)
    (t := range p) (fun x _ => mem_coe.2 (mem_range.2 (Nat.mod_lt _ hp)))]
  refine Finset.sum_congr rfl fun t ht => ?_
  congr 1
  rw [Finset.filter_filter]
  refine Finset.filter_congr fun x _ => ?_
  rw [show x - (v + ((t * p ^ a : ℕ) : ZMod M)) = (x - v) - ((t * p ^ a : ℕ) : ZMod M) by ring,
    dvd_val_sub_natCast h, modEq_mul_pow_iff hp a _ t (mem_range.1 ht)]

/-! ### The power of `p` dividing the counts -/

/-- downward induction on `a`: `p^(number of zeros p^b with a < b ≤ n)` divides every count modulo `p^a` -/
theorem pow_card_dvd_cnt (A : Finset (ZMod M)) {p : ℕ} (hp : p.Prime) (n : ℕ) (hn : p ^ n ∣ M)
    [DecidablePred fun b : ℕ => ZeroAt A (p ^ b)] (a : ℕ) (ha : a ≤ n) :
    ∀ v : ZMod M, p ^ ((Ioc a n).filter (fun b => ZeroAt A (p ^ b))).card ∣ cnt A (p ^ a) v := by
  induction ha using Nat.decreasingInduction with
  | self => intro v; simp
  | of_succ k hk ih =>
    intro v
    have hk1 : p ^ (k + 1) ∣ M := (pow_dvd_pow p hk).trans hn
    have hI : Ioc k n = insert (k + 1) (Ioc (k + 1) n) := by
      ext b
      simp only [mem_Ioc, mem_insert]
      omega
    rw [hI, Finset.filter_insert]
    by_cases hz : ZeroAt A (p ^ (k + 1))
    · rw [ite_eq_left hz, Finset.card_insert_of_notMem (by simp), pow_succ, mul_comm,
        ← (zeroAt_prime_pow A p hp k hk1).1 hz v]
      exact Nat.mul_dvd_mul_left p (ih v)
    · rw [ite_eq_right hz, cnt_split A hp.pos k hk1 v]
      exact Finset.dvd_sum fun t _ => ih _

/-! ### Prime powers dividing `M`, sorted by their prime -/

/-- the prime powers dividing `M` with prime `p` are the `p^b`, `1 ≤ b ≤ v_p(M)` -/
theorem filter_minFac_primePowers {p : ℕ} (hp : p.Prime) :
    (primePowers M).filter (fun s => s.minFac = p)
      = (Ioc 0 (M.factorization p)).image (fun b => p ^ b) := by
  have hM : M ≠ 0 := NeZero.ne M
  ext s
  simp only [primePowers, mem_filter, mem_image, mem_Ioc, Nat.mem_divisors]
  constructor
  · rintro ⟨⟨⟨hsM, -⟩, hpp⟩, hmin⟩
    obtain ⟨q, k, hq, hk, rfl⟩ := (isPrimePow_nat_iff s).1 hpp
    rw [hq.pow_minFac hk.ne'] at hmin
    subst hmin
    exact ⟨k, ⟨hk, (hq.pow_dvd_iff_le_factorization hM).1 hsM⟩, rfl⟩
  · rintro ⟨b, ⟨hb0, hbn⟩, rfl⟩
    exact ⟨⟨⟨(hp.pow_dvd_iff_le_factorization hM).2 hbn, hM⟩,
      (isPrimePow_nat_iff _).2 ⟨p, b, hp, hb0, rfl⟩⟩, hp.pow_minFac hb0.ne'⟩

omit [NeZero M] in
/-- the exponent of `p` in `∏_{s ∈ S} minFac s` is the number of `s ∈ S` that are powers of `p` -/
theorem factorization_prod_minFac (S : Finset ℕ) (hS : S ⊆ primePowers M) (p : ℕ) :
    (∏ s ∈ S, s.minFac).factorization p = (S.filter (fun s => s.minFac = p)).card := by
  rw [Nat.factorization_prod (fun s _ => (Nat.minFac_pos s).ne'), Finset.sum_apply', Finset.card_filter]
  refine Finset.sum_congr rfl fun s hs => ?_
  have hs1 : s ≠ 1 := by
    have h := hS hs
    rw [primePowers, mem_filter] at h
    exact h.2.ne_one
  rw [(Nat.minFac_prime hs1).factorization, Finsupp.single_apply]

/-- `∏_{p^a ∣ M} p = M` -/
theorem prod_minFac_primePowers : ∏ s ∈ primePowers M, s.minFac = M := by
  have hM : M ≠ 0 := NeZero.ne M
  refine Nat.eq_of_factorization_eq (Finset.prod_ne_zero_iff.2 fun s _ => (Nat.minFac_pos s).ne') hM
    fun p => ?_
  by_cases hp : p.Prime
  · rw [factorization_prod_minFac _ (Finset.Subset.refl _) p, filter_minFac_primePowers hp,
      Finset.card_image_of_injective _ (Nat.pow_right_injective hp.two_le), Nat.card_Ioc, Nat.sub_zero]
  · rw [Nat.factorization_eq_zero_of_not_prime _ hp, Nat.factorization_eq_zero_of_not_prime _ hp]

end CM

theorem prod_minFac_dvd_card (A : Finset (ZMod M)) : (∏ s ∈ SA A, s.minFac) ∣ A.card := by
  classical
  rcases Nat.eq_zero_or_pos A.card with h0 | hpos
  · rw [h0]
    exact dvd_zero _
  have hne : (∏ s ∈ SA A, s.minFac) ≠ 0 :=
    Finset.prod_ne_zero_iff.2 fun s _ => (Nat.minFac_pos s).ne'
  rw [← Nat.factorization_prime_le_iff_dvd hne hpos.ne']
  intro p hp
  rw [CM.factorization_prod_minFac _ (CM.SA_subset A) p, ← hp.pow_dvd_iff_le_factorization hpos.ne']
  have h1 : (SA A).filter (fun s => s.minFac = p)
      = ((Ioc 0 (M.factorization p)).filter (fun b => ZeroAt A (p ^ b))).image (fun b => p ^ b) := by
    rw [SA, Finset.filter_comm, CM.filter_minFac_primePowers hp, Finset.filter_image]
  rw [h1, Finset.card_image_of_injective _ (Nat.pow_right_injective hp.two_le)]
  have h2 := CM.pow_card_dvd_cnt A hp (M.factorization p) (Nat.ordProj_dvd M p) 0 (Nat.zero_le _) 0
  rwa [pow_zero, cnt_one] at h2

/-- **Coven–Meyerowitz**, with the complement named: if `A` satisfies (T1) and (T2) then `A` tiles `ZMod M`
with the digit set of the prime powers of `M` that are not zeros of `A`. -/
theorem tiling_of_T1_T2_digitSet (A : Finset (ZMod M)) (h1 : T1 A) (h2 : T2 A) :
    IsTiling A (digitSet M (primePowers M \ SA A)) := by
  classical
  have hSA : SA A ⊆ primePowers M := CM.SA_subset A
  have hsub : primePowers M \ SA A ⊆ primePowers M := Finset.sdiff_subset
  have h1' : A.card = ∏ s ∈ SA A, s.minFac := h1
  refine tiling_of_zeroAt _ _ ?_ ?_
  · rw [h1', card_digitSet _ hsub, mul_comm, Finset.prod_sdiff hSA, CM.prod_minFac_primePowers]
  · intro d hd hd1
    by_cases hex : ∃ s ∈ primePowers M \ SA A, ExactDiv s d
    · exact Or.inr ((zeroAt_digitSet _ hsub d hd).2 hex)
    · refine Or.inl (h2 d hd hd1 fun s hs hsd => ?_)
      by_contra hns
      exact hex ⟨s, Finset.mem_sdiff.2 ⟨hs, fun hmem => hns ((CM.mem_SA A s).1 hmem).2⟩, hsd⟩

/-- **Coven–Meyerowitz**: (T1) and (T2) imply tiling. -/
theorem tiling_of_T1_T2 (A : Finset (ZMod M)) (h1 : T1 A) (h2 : T2 A) :
    ∃ B : Finset (ZMod M), IsTiling A B :=
  ⟨_, tiling_of_T1_T2_digitSet A h1 h2⟩

/-- A weak tile without "orphan" zeros satisfies (T1). -/
theorem T1_of_no_orphan (A : Finset (ZMod M)) (f : ZMod M → ℝ) (h : WeakTiling A f)
    (hno : ∀ d, d ∣ M → d ≠ 1 → ZeroAt A d → ∃ s ∈ SA A, ExactDiv s d) : T1 A := by
  have hSA : SA A ⊆ primePowers M := CM.SA_subset A
  have hA : A.Nonempty := nonempty_of_weakTiling A f h
  have hcard := card_digitSet (M := M) (SA A) hSA
  have hpos : 0 < ∏ s ∈ SA A, s.minFac := Finset.prod_pos fun s _ => Nat.minFac_pos s
  have hA' : (digitSet M (SA A)).Nonempty := by
    rw [← Finset.card_pos, hcard]
    exact hpos
  have hle : A.card ≤ ∏ s ∈ SA A, s.minFac := by
    rw [← hcard]
    exact S_bound A _ f h hA' fun d hd hd1 hz => (zeroAt_digitSet _ hSA d hd).2 (hno d hd hd1 hz)
  exact le_antisymm hle (Nat.le_of_dvd hA.card_pos (prod_minFac_dvd_card A))

/-- **Weak tiles of a cyclic group of prime-power order are tiles.** -/
theorem weak_tiling_tiles_prime_pow (p : ℕ) [Fact p.Prime] (n : ℕ) (A : Finset (ZMod (p ^ n)))
    (f : ZMod (p ^ n) → ℝ) (h : WeakTiling A f) : ∃ B : Finset (ZMod (p ^ n)), IsTiling A B := by
  have hp : p.Prime := Fact.out
  have : NeZero (p ^ n) := ⟨pow_ne_zero n hp.ne_zero⟩
  -- every divisor `d ≠ 1` of `p ^ n` is a prime power dividing `p ^ n`, and divides itself exactly
  have key : ∀ d, d ∣ p ^ n → d ≠ 1 → d ∈ primePowers (p ^ n) ∧ ExactDiv d d := by
    intro d hd hd1
    obtain ⟨k, -, rfl⟩ := (Nat.dvd_prime_pow hp).1 hd
    have hk0 : k ≠ 0 := by
      rintro rfl
      exact hd1 (pow_zero p)
    refine ⟨?_, dvd_rfl, ?_⟩
    · rw [primePowers, Finset.mem_filter, Nat.mem_divisors]
      exact ⟨⟨hd, NeZero.ne _⟩, (isPrimePow_nat_iff _).2 ⟨p, k, hp, Nat.pos_of_ne_zero hk0, rfl⟩⟩
    · rw [Nat.div_self (Nat.pow_pos hp.pos)]
      exact Nat.coprime_one_right _
  refine tiling_of_T1_T2 A (T1_of_no_orphan A f h fun d hd hd1 hz => ?_) fun d hd hd1 hall => ?_
  · exact ⟨d, (CM.mem_SA A d).2 ⟨(key d hd hd1).1, hz⟩, (key d hd hd1).2⟩
  · exact hall d (key d hd hd1).1 (key d hd hd1).2

end Pqr
