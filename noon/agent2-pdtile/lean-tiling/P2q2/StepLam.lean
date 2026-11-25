/-
Step functions on `ZMod M` in Möbius coordinates and their Fourier coefficients (general `M`).
`stepFn M μ x = ∑_{d ∣ M, d ∣ x} μ d`; its transform at a frequency of order `e` is
`Lam M μ e = ∑_{e ∣ d ∣ M} μ d * (M / d)`.
-/
import Pqr.CM
import Pqr.Counting

open Finset

namespace P2q2

open Pqr

/-- the step function with Möbius coefficients `μ` -/
noncomputable def stepFn (M : ℕ) (μ : ℕ → ℝ) (x : ZMod M) : ℝ :=
  ∑ d ∈ M.divisors, if d ∣ x.val then μ d else 0

/-- its Fourier coefficient at the frequencies of order `e` -/
noncomputable def Lam (M : ℕ) (μ : ℕ → ℝ) (e : ℕ) : ℝ :=
  ∑ d ∈ M.divisors, if e ∣ d then μ d * ((M / d : ℕ) : ℝ) else 0

variable {M : ℕ} [NeZero M]

theorem stepFn_eq_sum_gcd (μ : ℕ → ℝ) (x : ZMod M) :
    stepFn M μ x = ∑ d ∈ (x.val.gcd M).divisors, μ d := by
  rw [stepFn, sum_divisors_ite]

/-- For `d ∣ M`, divisibility of the representative by `d` is invariant under negation. -/
theorem dvd_neg_val_iff {d : ℕ} (hd : d ∣ M) (x : ZMod M) : d ∣ (-x).val ↔ d ∣ x.val := by
  rw [ZMod.neg_val]
  split_ifs with h
  · subst h
    simp
  · exact Nat.dvd_sub_iff_right (ZMod.val_lt x).le hd

/-- A step function is even. -/
theorem stepFn_neg (μ : ℕ → ℝ) (x : ZMod M) : stepFn M μ (-x) = stepFn M μ x := by
  unfold stepFn
  refine Finset.sum_congr rfl fun d hd => ?_
  simp only [dvd_neg_val_iff (Nat.dvd_of_mem_divisors hd)]

omit [NeZero M] in
theorem stepFn_zero (μ : ℕ → ℝ) : stepFn M μ 0 = ∑ d ∈ M.divisors, μ d := by
  simp [stepFn]

theorem stepFn_nonneg (μ : ℕ → ℝ) (hpos : ∀ g ∈ M.divisors, 0 ≤ ∑ d ∈ g.divisors, μ d) (x : ZMod M) :
    0 ≤ stepFn M μ x := by
  rw [stepFn_eq_sum_gcd]
  exact hpos _ (gcd_mem_divisors M _)

/-- A weak tile has a weak complement that is a step function. -/
theorem exists_stepFn (A : Finset (ZMod M)) (f : ZMod M → ℝ) (h : WeakTiling A f) :
    ∃ μ : ℕ → ℝ, WeakTiling A (stepFn M μ) := by
  obtain ⟨μ, h1, h2, h3⟩ := countingCert_of_weakTiling A f h
  refine ⟨μ, stepFn_nonneg μ h1, (stepFn_zero μ).trans h2, fun v => ?_⟩
  rw [← h3 v, sum_mul_cnt]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [show v - a = -(a - v) from (neg_sub a v).symm, stepFn_neg, stepFn]

theorem ft_stepFn (μ : ℕ → ℝ) (ξ : ZMod M) : ft (stepFn M μ) ξ = ((Lam M μ (ord ξ) : ℝ) : ℂ) := by
  have h1 : ∀ w : ZMod M, ((stepFn M μ w : ℝ) : ℂ) * ZMod.stdAddChar (ξ * w)
      = ∑ d ∈ M.divisors, (μ d : ℂ) * (if d ∣ w.val then ZMod.stdAddChar (ξ * w) else 0) := by
    intro w
    rw [stepFn, Complex.ofReal_sum, Finset.sum_mul]
    refine Finset.sum_congr rfl fun d _ => ?_
    split_ifs <;> simp
  rw [ft]
  simp_rw [h1]
  rw [Finset.sum_comm, Lam, Complex.ofReal_sum]
  refine Finset.sum_congr rfl fun d hd => ?_
  rw [← Finset.mul_sum, Bridge.sum_char_multiples d (Nat.dvd_of_mem_divisors hd)]
  simp only [Bridge.mul_natCast_eq_zero_iff]
  split_ifs <;> simp

/-- The transform of a step complement vanishes at the orders that are not zeros of the set. -/
theorem lam_eq_zero_of_not_zeroAt (A : Finset (ZMod M)) (μ : ℕ → ℝ) (h : WeakTiling A (stepFn M μ))
    (e : ℕ) (he : e ∣ M) (he1 : e ≠ 1) (hz : ¬ ZeroAt A e) : Lam M μ e = 0 := by
  by_contra hne
  apply hz
  have hord : ord ((M / e : ℕ) : ZMod M) = e := DigitSets.ord_natCast_div he
  have hξ : ((M / e : ℕ) : ZMod M) ≠ 0 := fun h0 =>
    he1 (by rw [← hord]; exact (ord_eq_one_iff _).2 h0)
  have hprod := hat_mul_ft A _ h ((M / e : ℕ) : ZMod M)
  rw [ite_eq_right hξ, ft_stepFn, hord] at hprod
  rcases mul_eq_zero.1 hprod with h0 | h0
  · have hZ := zeroAt_of_hat_eq_zero A _ h0
    rwa [hord] at hZ
  · exact absurd (Complex.ofReal_eq_zero.1 h0) hne

theorem card_mul_lam_one (A : Finset (ZMod M)) (μ : ℕ → ℝ) (h : WeakTiling A (stepFn M μ)) :
    (A.card : ℝ) * Lam M μ 1 = M := by
  have h0 := hat_mul_ft A _ h 0
  rw [hat_zero, ft_stepFn, ite_eq_left rfl, (ord_eq_one_iff (0 : ZMod M)).2 rfl] at h0
  exact_mod_cast h0

/-- A nonnegative normalised step function whose transform vanishes wherever the transform of `A` does not,
and whose mass is at most `M / |A|`, is a weak tiling complement of `A`. -/
theorem weakTiling_stepFn_of_lam (A : Finset (ZMod M)) (hA : A.Nonempty) (μ : ℕ → ℝ)
    (hpos : ∀ g ∈ M.divisors, 0 ≤ ∑ d ∈ g.divisors, μ d) (hone : ∑ d ∈ M.divisors, μ d = 1)
    (hz : ∀ e, e ∣ M → e ≠ 1 → ¬ ZeroAt A e → Lam M μ e = 0)
    (hle : (A.card : ℝ) * Lam M μ 1 ≤ M) : WeakTiling A (stepFn M μ) := by
  have hM : (0 : ℝ) < M := Nat.cast_pos.2 (Nat.pos_of_ne_zero (NeZero.ne M))
  have hf0 : ∀ x, 0 ≤ stepFn M μ x := stepFn_nonneg μ hpos
  have hf1 : stepFn M μ 0 = 1 := (stepFn_zero μ).trans hone
  set K : ℝ := (A.card : ℝ) * Lam M μ 1 / M with hK
  -- all Fourier coefficients of `1_A * f - K` vanish
  have key : ∀ ξ : ZMod M,
      ∑ v, ((∑ a ∈ A, (stepFn M μ (v - a) : ℂ)) - K) * ZMod.stdAddChar (ξ * v) = 0 := by
    intro ξ
    simp_rw [sub_mul]
    rw [Finset.sum_sub_distrib, conv_ft, ← Finset.mul_sum, sum_stdAddChar_mul, ft_stepFn]
    by_cases hξ : ξ = 0
    · subst hξ
      rw [ite_eq_left rfl, hat_zero, (ord_eq_one_iff (0 : ZMod M)).2 rfl, sub_eq_zero]
      have : (A.card : ℝ) * Lam M μ 1 = K * M := by
        rw [hK]
        field_simp
      exact_mod_cast this
    · rw [ite_eq_right hξ, mul_zero, sub_zero]
      by_cases hZ : ZeroAt A (ord ξ)
      · rw [hZ ξ rfl, zero_mul]
      · rw [hz _ (ord_dvd ξ) (fun h1 => hξ ((ord_eq_one_iff ξ).1 h1)) hZ, Complex.ofReal_zero,
          mul_zero]
  have hg := zmod_fourier_uniq (fun v => (∑ a ∈ A, (stepFn M μ (v - a) : ℂ)) - K) key
  have hc : ∀ v, ∑ a ∈ A, stepFn M μ (v - a) = K := by
    intro v
    have hv0 := congrFun hg v
    simp only [Pi.zero_apply, sub_eq_zero] at hv0
    exact_mod_cast hv0
  have hK1 : K ≤ 1 := by
    rw [hK, div_le_one hM]
    exact hle
  obtain ⟨a, ha⟩ := hA
  have hge : stepFn M μ (a - a) ≤ ∑ b ∈ A, stepFn M μ (a - b) :=
    Finset.single_le_sum (f := fun b => stepFn M μ (a - b)) (fun b _ => hf0 _) ha
  rw [sub_self, hf1, hc a] at hge
  have hKeq : K = 1 := le_antisymm hK1 hge
  exact ⟨hf0, hf1, fun v => by rw [hc v, hKeq]⟩

end P2q2
