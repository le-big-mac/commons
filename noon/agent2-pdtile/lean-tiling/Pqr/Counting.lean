/-
Weak tiling in a cyclic group `ZMod M`, in counting form: a set `A` has a weak tiling complement iff some
real combination of its residue-class counts is identically 1 (with two sign conditions on the coefficients).
No characters, no cyclotomic polynomials in the statement.
-/
import Pqr.Fourier

open Finset

namespace Pqr

/-- number of elements of `A` congruent to `v` modulo `d` (meaningful for `d ∣ M`) -/
def cnt {M : ℕ} (A : Finset (ZMod M)) (d : ℕ) (v : ZMod M) : ℕ :=
  (A.filter (fun a => d ∣ (a - v).val)).card

/-- A counting certificate of weak tiling: coefficients `μ d`, `d ∣ M`, such that
(i) `∑_{d ∣ g} μ d ≥ 0` for every `g ∣ M`, (ii) `∑_{d ∣ M} μ d = 1`, and
(iii) `∑_{d ∣ M} μ d * #{a ∈ A : a ≡ v mod d} = 1` for every `v`. -/
def CountingCert {M : ℕ} (A : Finset (ZMod M)) (μ : ℕ → ℝ) : Prop :=
  (∀ g ∈ M.divisors, 0 ≤ ∑ d ∈ g.divisors, μ d) ∧ ∑ d ∈ M.divisors, μ d = 1 ∧
  ∀ v : ZMod M, ∑ d ∈ M.divisors, μ d * (cnt A d v : ℝ) = 1

/-! ### Divisor sums -/

/-- The divisors of `M` that divide `n` are the divisors of `gcd n M`. -/
theorem divisors_filter_dvd (M : ℕ) [NeZero M] (n : ℕ) :
    M.divisors.filter (fun d => d ∣ n) = (n.gcd M).divisors := by
  ext d
  have hM : M ≠ 0 := NeZero.ne M
  simp only [mem_filter, Nat.mem_divisors, Nat.dvd_gcd_iff, ne_eq, Nat.gcd_eq_zero_iff, hM,
    and_false, not_false_eq_true, and_true]
  exact and_comm

/-- A sum over the divisors of `M` dividing `n` is a sum over the divisors of `gcd n M`. -/
theorem sum_divisors_ite (M : ℕ) [NeZero M] (μ : ℕ → ℝ) (n : ℕ) :
    ∑ d ∈ M.divisors, (if d ∣ n then μ d else 0) = ∑ d ∈ (n.gcd M).divisors, μ d := by
  rw [← Finset.sum_filter, divisors_filter_dvd]

theorem gcd_mem_divisors (M : ℕ) [NeZero M] (n : ℕ) : n.gcd M ∈ M.divisors :=
  Nat.mem_divisors.2 ⟨Nat.gcd_dvd_right _ _, NeZero.ne M⟩

/-- The counting combination, with the two summations exchanged. -/
theorem sum_mul_cnt {M : ℕ} (A : Finset (ZMod M)) (μ : ℕ → ℝ) (v : ZMod M) :
    ∑ d ∈ M.divisors, μ d * (cnt A d v : ℝ)
      = ∑ a ∈ A, ∑ d ∈ M.divisors, (if d ∣ (a - v).val then μ d else 0) := by
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun d _ => ?_
  rw [cnt, Finset.card_filter, Nat.cast_sum, Finset.mul_sum]
  refine Finset.sum_congr rfl fun a _ => ?_
  split_ifs <;> simp

/-- Möbius inversion: every function on the positive integers is a divisor sum. -/
theorem exists_divisor_sum (F : ℕ → ℝ) : ∃ μ : ℕ → ℝ, ∀ n > 0, ∑ d ∈ n.divisors, μ d = F n :=
  ⟨_, ArithmeticFunction.sum_eq_iff_sum_mul_moebius_eq.2 fun _ _ => rfl⟩

/-! ### Averaging over the unit group -/

/-- Dilation by a unit preserves weak tiling complements. -/
theorem weakTiling_unit_mul {M : ℕ} [NeZero M] (A : Finset (ZMod M)) (f : ZMod M → ℝ)
    (h : WeakTiling A f) (u : (ZMod M)ˣ) : WeakTiling A (fun v => f (u * v)) := by
  have hk : (Fintype.card (ZMod M)).Coprime (u : ZMod M).val := by
    rw [ZMod.card]
    exact (ZMod.val_coe_unit_coprime u).symm
  have h1 := weakTiling_nsmul A f h _ hk
  simpa only [nsmul_eq_mul, ZMod.natCast_zmod_val] using h1

/-- the average of `f` over the dilations by units -/
noncomputable def avg {M : ℕ} [NeZero M] (f : ZMod M → ℝ) (v : ZMod M) : ℝ :=
  (∑ u : (ZMod M)ˣ, f (u * v)) / Fintype.card (ZMod M)ˣ

theorem weakTiling_avg_units {M : ℕ} [NeZero M] (A : Finset (ZMod M)) (f : ZMod M → ℝ)
    (h : WeakTiling A f) : WeakTiling A (avg f) :=
  weakTiling_avg A (fun (u : (ZMod M)ˣ) v => f (u * v)) (weakTiling_unit_mul A f h)

/-- The average is invariant under dilations by units. -/
theorem avg_unit_mul {M : ℕ} [NeZero M] (f : ZMod M → ℝ) (u : (ZMod M)ˣ) (v : ZMod M) :
    avg f (u * v) = avg f v := by
  unfold avg
  congr 1
  rw [← Equiv.sum_comp (Equiv.mulRight u) (fun w : (ZMod M)ˣ => f (w * v))]
  refine Finset.sum_congr rfl fun w _ => ?_
  simp [mul_assoc]

theorem avg_neg {M : ℕ} [NeZero M] (f : ZMod M → ℝ) (v : ZMod M) : avg f (-v) = avg f v := by
  simpa using avg_unit_mul f (-1) v

/-- Every element of `ZMod M` is a unit multiple of the gcd of its representative with `M`.
(This is the proof of Mathlib's `ZMod.eq_unit_mul_divisor`, keeping track of the divisor.) -/
theorem eq_unit_mul_gcd {M : ℕ} [NeZero M] (a : ZMod M) :
    ∃ u : (ZMod M)ˣ, a = u * ((a.val.gcd M : ℕ) : ZMod M) := by
  have hM : M ≠ 0 := NeZero.ne M
  have hd : a.val.gcd M ≠ 0 := Nat.gcd_ne_zero_right hM
  obtain ⟨a₀, ha₀⟩ := a.val.gcd_dvd_left M
  obtain ⟨M₀, hM₀⟩ := a.val.gcd_dvd_right M
  -- `a₀` is coprime to `M₀`
  have hcop : Nat.Coprime a₀ M₀ := by
    have h := Nat.gcd_mul_left (a.val.gcd M) a₀ M₀
    rw [← ha₀, ← hM₀] at h
    exact Nat.eq_of_mul_eq_mul_left (Nat.pos_of_ne_zero hd) (by rw [← h, mul_one])
  -- lift the unit `a₀` modulo `M₀` to a unit modulo `M`
  have hdvd : M₀ ∣ M := ⟨a.val.gcd M, by rw [mul_comm]; exact hM₀⟩
  obtain ⟨u, hu⟩ := ZMod.unitsMap_surjective hdvd (ZMod.unitOfCoprime a₀ hcop)
  have hu' : (((u : ZMod M).val : ℕ) : ZMod M₀) = (a₀ : ZMod M₀) := by
    have h := congrArg (fun w : (ZMod M₀)ˣ => (w : ZMod M₀)) hu
    simp only [ZMod.unitsMap_val, ZMod.coe_unitOfCoprime] at h
    rw [ZMod.natCast_val]
    exact h
  have hmod : (u : ZMod M).val ≡ a₀ [MOD M₀] := (ZMod.natCast_eq_natCast_iff _ _ _).1 hu'
  have hmod' : a.val.gcd M * (u : ZMod M).val ≡ a.val.gcd M * a₀ [MOD a.val.gcd M * M₀] :=
    Nat.ModEq.mul_left' _ hmod
  rw [← hM₀, ← ha₀] at hmod'
  have h := (ZMod.natCast_eq_natCast_iff _ _ _).2 hmod'
  rw [ZMod.natCast_zmod_val, Nat.cast_mul, ZMod.natCast_zmod_val] at h
  exact ⟨u, h.symm.trans (mul_comm _ _)⟩

/-- The average depends only on the gcd with `M`. -/
theorem avg_eq_gcd {M : ℕ} [NeZero M] (f : ZMod M → ℝ) (x : ZMod M) :
    avg f x = avg f ((x.val.gcd M : ℕ) : ZMod M) := by
  obtain ⟨u, hu⟩ := eq_unit_mul_gcd x
  conv_lhs => rw [hu]
  exact avg_unit_mul f u _

/-! ### The main theorem -/

theorem countingCert_of_weakTiling {M : ℕ} [NeZero M] (A : Finset (ZMod M)) (f : ZMod M → ℝ)
    (h : WeakTiling A f) : ∃ μ : ℕ → ℝ, CountingCert A μ := by
  have hbar := weakTiling_avg_units A f h
  obtain ⟨μ, hμ⟩ := exists_divisor_sum (fun e => avg f (e : ZMod M))
  have hM : 0 < M := Nat.pos_of_ne_zero (NeZero.ne M)
  refine ⟨μ, fun g hg => ?_, ?_, fun v => ?_⟩
  · rw [hμ g (Nat.pos_of_mem_divisors hg)]
    exact hbar.1 _
  · rw [hμ M hM, ZMod.natCast_self]
    exact hbar.2.1
  · rw [sum_mul_cnt, ← hbar.2.2 v]
    refine Finset.sum_congr rfl fun a _ => ?_
    rw [sum_divisors_ite, hμ _ (Nat.gcd_pos_of_pos_right _ hM), ← avg_eq_gcd, ← neg_sub, avg_neg]

theorem weakTiling_of_countingCert {M : ℕ} [NeZero M] (A : Finset (ZMod M)) (μ : ℕ → ℝ)
    (h : CountingCert A μ) : ∃ f : ZMod M → ℝ, WeakTiling A f := by
  obtain ⟨h1, h2, h3⟩ := h
  refine ⟨fun x => ∑ d ∈ M.divisors, (if d ∣ (-x).val then μ d else 0), fun x => ?_, ?_, fun v => ?_⟩
  · beta_reduce
    rw [sum_divisors_ite]
    exact h1 _ (gcd_mem_divisors M _)
  · simpa using h2
  · rw [← h3 v, sum_mul_cnt]
    simp only [neg_sub]

theorem weakTiling_iff_countingCert (M : ℕ) [NeZero M] (A : Finset (ZMod M)) :
    (∃ f : ZMod M → ℝ, WeakTiling A f) ↔ ∃ μ : ℕ → ℝ, CountingCert A μ :=
  ⟨fun ⟨f, hf⟩ => countingCert_of_weakTiling A f hf,
    fun ⟨μ, hμ⟩ => weakTiling_of_countingCert A μ hμ⟩

end Pqr
