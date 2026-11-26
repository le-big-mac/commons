import Pnq.Upset
/-!
Audit file 11: the role of `0 < s` in `least_size`.

`Φ_1 = X - 1` divides the mask exactly of the empty multiset.  So, for an up-set `D` (which does not contain `1`),
"`0 < s` and, for every divisor `d ≠ 1`, `Φ_d ∣ mask ↔ d ∈ D`" is the same as
"for every divisor `d` of `M` (`d = 1` included), `Φ_d ∣ mask ↔ d ∈ D`":
the set of `least_size` is the set of sizes of the multisets whose cyclotomic divisors, among the `Φ_d` with
`d ∣ M`, are exactly those with `d ∈ D`.
-/
open Finset Pnq Pnq.Upset

namespace Audit

theorem cyclotomic_one_dvd_iff {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    Polynomial.cyclotomic 1 ℤ ∣ maskW w ↔ ∑ a, w a = 0 := by
  rw [Polynomial.cyclotomic_one, ← Polynomial.C_1, Polynomial.dvd_iff_isRoot, Polynomial.IsRoot, maskW,
    Polynomial.eval_finsetSum]
  simp only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow, Polynomial.eval_X, one_pow,
    mul_one]
  exact_mod_cast Iff.rfl

theorem pattern_iff {M : ℕ} [NeZero M] {D : Finset ℕ} (hD : IsUpSet M D) (w : ZMod M → ℕ) :
    (0 < ∑ a, w a ∧ ∀ d, d ∣ M → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)) ↔
      ∀ d, d ∣ M → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D) := by
  have h1 : (1 : ℕ) ∉ D := fun h => (hD.1 1 h).2 rfl
  constructor
  · rintro ⟨hpos, h⟩ d hd
    by_cases hd1 : d = 1
    · subst hd1
      rw [cyclotomic_one_dvd_iff]
      exact ⟨fun h0 => absurd h0 hpos.ne', fun h => absurd h h1⟩
    · exact h d hd hd1
  · intro h
    refine ⟨?_, fun d hd _ => h d hd⟩
    have h2 := h 1 (one_dvd _)
    rw [cyclotomic_one_dvd_iff] at h2
    exact Nat.pos_of_ne_zero (fun h0 => h1 (h2.1 h0))

/-- `least_size` restated with the pattern over all divisors and without `0 < s` -/
theorem least_size_all_divisors {p q n m : ℕ} [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q) (D : Finset ℕ)
    (hD : IsUpSet (p ^ n * q ^ m) D) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q ^ m) → ℕ, ∑ a, w a = s ∧
        ∀ d, d ∣ p ^ n * q ^ m → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)}
      (∑ c ∈ corners (p ^ n * q ^ m) D, p ^ n * q ^ m / c) := by
  have h := least_size hpq D hD
  have e : {s | ∃ w : ZMod (p ^ n * q ^ m) → ℕ, ∑ a, w a = s ∧
        ∀ d, d ∣ p ^ n * q ^ m → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)} =
      {s | ∃ w : ZMod (p ^ n * q ^ m) → ℕ, ∑ a, w a = s ∧ 0 < s ∧
        ∀ d, d ∣ p ^ n * q ^ m → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ D)} := by
    ext s
    constructor
    · rintro ⟨w, rfl, hw⟩
      exact ⟨w, rfl, (pattern_iff hD w).2 hw⟩
    · rintro ⟨w, rfl, hpos, hw⟩
      exact ⟨w, rfl, (pattern_iff hD w).1 ⟨hpos, hw⟩⟩
  rw [e]
  exact h

end Audit

#print axioms Audit.least_size_all_divisors
