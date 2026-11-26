import Pnq.Upset
/-!
Audit file 7.
(a) The three theorems without the hypothesis `p ≠ q`: the project's proofs, copied word for word, with `hpq`
    deleted.  If these compile, the hypothesis is not needed and the statements hold for `p = q` too.
(b) The hypotheses of `lower_bound` can be met for every up-set (the theorem is not vacuous), and the bound is
    attained.
(c) Instances: `M = 1`, a prime power, `p = q`.
-/
open Finset Pnq Pnq.Upset

namespace Audit

variable {p q n m : ℕ} [Fact p.Prime] [Fact q.Prime]

/-! ### (a) without `p ≠ q` -/

theorem structure_iff' (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D)
    (w : ZMod (p ^ n * q ^ m) → ℕ) :
    (∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW w) ↔
      ∃ g : ℕ → ZMod (p ^ n * q ^ m) → ℕ,
        (∀ c ∈ corners (p ^ n * q ^ m) D, ∀ x, g c (x + (c : ZMod (p ^ n * q ^ m))) = g c x) ∧
        ∀ a, w a = ∑ c ∈ corners (p ^ n * q ^ m) D, g c a := by
  constructor
  · intro h
    exact Aux.rep_all D hD w
      (fun ξ hξ => (zeroAtW_iff_cyclotomic_dvd w _ (hD.1 _ hξ).1).2 (h _ hξ) ξ rfl)
  · rintro ⟨g, hg, hw⟩ d hd
    rw [← zeroAtW_iff_cyclotomic_dvd w d (hD.1 d hd).1]
    intro ξ hξ
    rw [Aux.hatW_sum _ g w hw ξ]
    refine Finset.sum_eq_zero fun c hc => ?_
    refine Aux.hatW_eq_zero_of_periodic (g c) _ ξ (hg c hc) ?_
    rw [Ne, Pqr.Bridge.mul_natCast_eq_zero_iff, hξ]
    exact fun hdc => Aux.corner_not_mem hc (hD.2 d hd c hdc (Aux.corner_dvd hc))

theorem lower_bound' (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D)
    (w : ZMod (p ^ n * q ^ m) → ℕ) (hdiv : ∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW w)
    (hcor : ∀ c ∈ corners (p ^ n * q ^ m) D, ¬ Polynomial.cyclotomic c ℤ ∣ maskW w) :
    ∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c ≤ ∑ a, w a := by
  obtain ⟨g, hg, hw⟩ := (structure_iff' D hD w).1 hdiv
  have key : ∀ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c ≤ ∑ a, g c a := by
    intro c hc
    have hcM := Aux.corner_dvd hc
    by_contra hlt
    have hzero : ∀ x, g c x = 0 := by
      intro x
      by_contra hx
      exact hlt (Aux.div_le_sum_of_periodic c hcM (g c) (hg c hc) x hx)
    apply hcor c hc
    rw [← zeroAtW_iff_cyclotomic_dvd w c hcM]
    intro ξ hξ
    rw [Aux.hatW_sum _ g w hw ξ]
    refine Finset.sum_eq_zero fun c' hc' => ?_
    by_cases hcc : c' = c
    · rw [hcc, hatW]
      refine Finset.sum_eq_zero fun a _ => ?_
      rw [hzero a, Nat.cast_zero, zero_mul]
    · refine Aux.hatW_eq_zero_of_periodic (g c') _ ξ (hg c' hc') ?_
      rw [Ne, Pqr.Bridge.mul_natCast_eq_zero_iff, hξ]
      exact fun hdvd => hcc ((Aux.mem_corners.1 hc).2 c' (Aux.mem_corners.1 hc').1 hdvd)
  calc ∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c
      ≤ ∑ c ∈ corners (p ^ n * q ^ m) D, ∑ a, g c a := Finset.sum_le_sum key
    _ = ∑ a, w a := by
        rw [Finset.sum_comm]
        exact Finset.sum_congr rfl fun a _ => (hw a).symm

theorem least_size' (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q ^ m) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
        ∀ d, d ∣ p ^ n * q ^ m → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)}
      (∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c) := by
  have hM : p ^ n * q ^ m ≠ 0 := NeZero.ne _
  have hpos : ∀ c ∈ corners (p ^ n * q ^ m) D, 0 < p ^ n * q ^ m / c := fun c hc =>
    Nat.div_pos (Nat.le_of_dvd (Nat.pos_of_ne_zero hM) (Aux.corner_dvd hc))
      (Nat.pos_of_dvd_of_pos (Aux.corner_dvd hc) (Nat.pos_of_ne_zero hM))
  constructor
  · refine ⟨fun a => ∑ c ∈ corners (p ^ n * q ^ m) D, if c ∣ a.val then 1 else 0, ?_, ?_, ?_⟩
    · rw [Finset.sum_comm]
      exact Finset.sum_congr rfl fun c hc => Aux.sum_dvd_val_one c (Aux.corner_dvd hc)
    · obtain ⟨c, hc, -⟩ := Aux.exists_corner D 1 (Aux.one_mem hM hD)
      exact Finset.sum_pos hpos ⟨c, hc⟩
    · intro d hd _
      rw [← zeroAtW_iff_cyclotomic_dvd _ d hd]
      constructor
      · intro hz
        by_contra hdD
        obtain ⟨c, hc, hdc⟩ := Aux.exists_corner D d
          (Finset.mem_sdiff.2 ⟨Nat.mem_divisors.2 ⟨hd, hM⟩, hdD⟩)
        have h1 := hz _ (Pqr.ord_natCast_div' hd)
        rw [Aux.hatW_multiples _ (fun c hc => Aux.corner_dvd hc), Pqr.ord_natCast_div' hd] at h1
        have h2 : (∑ c ∈ corners (p ^ n * q ^ m) D, if d ∣ c then p ^ n * q ^ m / c else 0) = 0 := by
          exact_mod_cast h1
        have h3 := (Finset.sum_eq_zero_iff.1 h2) c hc
        rw [ite_eq_left hdc] at h3
        exact (hpos c hc).ne' h3
      · intro hdD ξ hξ
        rw [Aux.hatW_multiples _ (fun c hc => Aux.corner_dvd hc), hξ, Finset.sum_eq_zero, Nat.cast_zero]
        intro c hc
        exact ite_eq_right fun hdc => Aux.corner_not_mem hc (hD.2 d hdD c hdc (Aux.corner_dvd hc))
  · rintro s ⟨w, rfl, hs, hw⟩
    refine lower_bound' D hD w (fun d hd => (hw d (hD.1 d hd).1 (hD.1 d hd).2).2 hd)
      (fun c hc hdiv => ?_)
    by_cases hc1 : c = 1
    · rw [hc1] at hdiv
      have hz := (zeroAtW_iff_cyclotomic_dvd w 1 (one_dvd _)).2 hdiv 0 ((Pqr.ord_eq_one_iff 0).2 rfl)
      rw [Aux.hatW_zero] at hz
      have h0 : ∑ a, w a = 0 := by exact_mod_cast hz
      exact hs.ne' h0
    · exact Aux.corner_not_mem hc ((hw c (Aux.corner_dvd hc) hc1).1 hdiv)

-- usable at p = q (here `ZMod (2^1 * 2^2)`, the group of order 8)
example (D : Finset ℕ) (hD : IsUpSet (2 ^ 1 * 2 ^ 2) D) :=
  least_size' (p := 2) (q := 2) (n := 1) (m := 2) D hD

/-! ### (b) `lower_bound` is not vacuous, and its bound is attained, for every up-set -/

/-- `Φ_1` divides the mask only of the empty multiset -/
theorem cyclotomic_one_dvd_iff {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    Polynomial.cyclotomic 1 ℤ ∣ maskW w ↔ ∑ a, w a = 0 := by
  rw [Polynomial.cyclotomic_one, ← Polynomial.C_1, Polynomial.dvd_iff_isRoot, Polynomial.IsRoot, maskW,
    Polynomial.eval_finsetSum]
  simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow, Polynomial.eval_X, one_pow,
    mul_one]
  exact_mod_cast Iff.rfl

theorem lower_bound_attained (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D) :
    ∃ w : ZMod (p ^ n * q ^ m) → ℕ,
      (∀ d ∈ D, Polynomial.cyclotomic d ℤ ∣ maskW w) ∧
      (∀ c ∈ corners (p ^ n * q ^ m) D, ¬ Polynomial.cyclotomic c ℤ ∣ maskW w) ∧
      ∑ a, w a = ∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c := by
  obtain ⟨w, hsum, hpos, hpat⟩ := (least_size hpq D hD).1
  refine ⟨w, fun d hd => (hpat d (hD.1 d hd).1 (hD.1 d hd).2).2 hd, fun c hc hdiv => ?_, hsum⟩
  by_cases hc1 : c = 1
  · rw [hc1, cyclotomic_one_dvd_iff, hsum] at hdiv
    exact hpos.ne' hdiv
  · exact Aux.corner_not_mem hc ((hpat c (Aux.corner_dvd hc) hc1).1 hdiv)

/-- the set of `least_size` is never empty, and never contains `0` -/
theorem least_size_set_nonempty (hpq : p ≠ q) (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D) :
    ({s | ∃ w : ZMod (p ^ n * q ^ m) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
        ∀ d, d ∣ p ^ n * q ^ m → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)}).Nonempty ∧
    0 < ∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c :=
  ⟨⟨_, (least_size hpq D hD).1⟩, by obtain ⟨w, hsum, hpos, -⟩ := (least_size hpq D hD).1; exact hpos⟩

/-- without `0 < s` the least element would be `0` for the largest up-set: the empty multiset has every `Φ_d`
as a divisor of its mask (which is `0`) -/
example {M : ℕ} [NeZero M] (d : ℕ) : Polynomial.cyclotomic d ℤ ∣ maskW (fun _ : ZMod M => 0) := by
  have : maskW (fun _ : ZMod M => 0) = 0 := by simp [maskW]
  rw [this]
  exact dvd_zero _

/-! ### (c) instances -/

-- M = 1 (n = m = 0): the only up-set is ∅, its corner is 1, the least size is 1
example : IsLeast {s | ∃ w : ZMod (2 ^ 0 * 3 ^ 0) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
    ∀ d, d ∣ 2 ^ 0 * 3 ^ 0 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ (∅ : Finset ℕ))} 1 := by
  have h := least_size (p := 2) (q := 3) (n := 0) (m := 0) (by norm_num) ∅ (by
    constructor <;> intro d hd <;> simp at hd)
  have e : (∑ c ∈ corners (2 ^ 0 * 3 ^ 0) (∅ : Finset ℕ), 2 ^ 0 * 3 ^ 0 / c) = 1 := by decide
  rwa [e] at h

-- M = 12, D = {4, 12}: corner 6, least size 2
example : IsLeast {s | ∃ w : ZMod (2 ^ 2 * 3 ^ 1) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
    ∀ d, d ∣ 2 ^ 2 * 3 ^ 1 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ ({4, 12} : Finset ℕ))} 2 := by
  have hB : (∀ d ∈ ({4, 12} : Finset ℕ), d ∣ 2 ^ 2 * 3 ^ 1 ∧ d ≠ 1) ∧
      ∀ d ∈ ({4, 12} : Finset ℕ), ∀ e ∈ (2 ^ 2 * 3 ^ 1).divisors, d ∣ e → e ∈ ({4, 12} : Finset ℕ) := by
    decide
  have hD : IsUpSet (2 ^ 2 * 3 ^ 1) {4, 12} :=
    ⟨hB.1, fun d hd e hde heM => hB.2 d hd e (Nat.mem_divisors.2 ⟨heM, by norm_num⟩) hde⟩
  have h := least_size (p := 2) (q := 3) (n := 2) (m := 1) (by norm_num) {4, 12} hD
  have e : (∑ c ∈ corners (2 ^ 2 * 3 ^ 1) ({4, 12} : Finset ℕ), 2 ^ 2 * 3 ^ 1 / c) = 2 := by decide
  rwa [e] at h

end Audit

#print axioms Audit.structure_iff'
#print axioms Audit.lower_bound'
#print axioms Audit.least_size'
#print axioms Audit.lower_bound_attained
