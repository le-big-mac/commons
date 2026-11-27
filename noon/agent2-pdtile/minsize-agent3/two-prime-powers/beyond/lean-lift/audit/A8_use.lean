import Pnq.LiftMin
/-! Audit file: the theorems USED to obtain concrete facts stated by the auditor in plain terms.
If a statement said something other than intended, these derivations would not go through (or would need other inputs). -/
open Pnq Pnq.Lift
namespace AuditUse
instance : Fact (Nat.Prime 2) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 3) := ⟨by norm_num⟩

-- membership in a set written `{s | p s}` is `p`
example (p : ℕ → Prop) (a : ℕ) : a ∈ {s | p s} ↔ p a := Iff.rfl
example : 2 ^ 1 * 3 * 3 = 18 := rfl
example : minU 2 3 ∅ {1} = 5 := by decide
example : minB 2 3 {1} {2} 1 = 18 := by decide
example : minB 3 2 {1} {2} 1 = 18 := by decide

/-- On Z_18 (= ZMod (2^1 * 3 * 3)): a multiset whose mask is divisible by Φ_6 and by none of Φ_2, Φ_3, Φ_9, Φ_18 has at least
5 elements.  From `minsize_unbalanced_lift` with p = 2, q = 3, n = 1, r = 3, Es = ∅, Fs = {1}. -/
theorem use_18_lower (w : ZMod (2 ^ 1 * 3 * 3) → ℕ)
    (h2 : ¬ Polynomial.cyclotomic 2 ℤ ∣ maskW w) (h3 : ¬ Polynomial.cyclotomic 3 ℤ ∣ maskW w)
    (h6 : Polynomial.cyclotomic 6 ℤ ∣ maskW w)
    (h9 : ¬ Polynomial.cyclotomic 9 ℤ ∣ maskW w) (h18 : ¬ Polynomial.cyclotomic 18 ℤ ∣ maskW w) :
    5 ≤ ∑ a, w a := by
  have h := (minsize_unbalanced_lift 2 3 1 3 (by decide) (by decide) ∅ {1} (by simp) (by simp)).2
  have hv : minU 2 3 ∅ {1} = 5 := by decide
  rw [hv] at h
  refine h ⟨w, rfl, h3, ?_, ?_, ?_⟩
  · intro ℓ hℓ
    have h1 : ℓ = 1 := by
      have := Finset.mem_Icc.1 hℓ
      omega
    subst h1
    change Polynomial.cyclotomic 2 ℤ ∣ maskW w ↔ 1 ∈ (∅ : Finset ℕ)
    exact ⟨fun hd => absurd hd h2, fun hm => absurd hm (by simp)⟩
  · intro ℓ hℓ
    have h1 : ℓ = 1 := by
      have := Finset.mem_Icc.1 hℓ
      omega
    subst h1
    change Polynomial.cyclotomic 6 ℤ ∣ maskW w ↔ 1 ∈ ({1} : Finset ℕ)
    exact ⟨fun _ => Finset.mem_singleton_self 1, fun _ => h6⟩
  · intro d hd hnd
    have hle : d ≤ 18 := Nat.le_of_dvd (by norm_num) hd
    interval_cases d <;> first
      | exact absurd hd (by decide)
      | exact absurd (by decide) hnd
      | assumption

/-- and such a multiset with exactly 5 elements exists -/
theorem use_18_attained : ∃ w : ZMod (2 ^ 1 * 3 * 3) → ℕ, ∑ a, w a = 5 ∧
    ¬ Polynomial.cyclotomic 2 ℤ ∣ maskW w ∧ ¬ Polynomial.cyclotomic 3 ℤ ∣ maskW w ∧
    Polynomial.cyclotomic 6 ℤ ∣ maskW w ∧
    ¬ Polynomial.cyclotomic 9 ℤ ∣ maskW w ∧ ¬ Polynomial.cyclotomic 18 ℤ ∣ maskW w := by
  have h := (minsize_unbalanced_lift 2 3 1 3 (by decide) (by decide) ∅ {1} (by simp) (by simp)).1
  have hv : minU 2 3 ∅ {1} = 5 := by decide
  rw [hv] at h
  obtain ⟨w, hs, h3, hE, hF, hnew⟩ := h
  have hE1 : Polynomial.cyclotomic 2 ℤ ∣ maskW w ↔ 1 ∈ (∅ : Finset ℕ) := hE 1 (by simp)
  have hF1 : Polynomial.cyclotomic 6 ℤ ∣ maskW w ↔ 1 ∈ ({1} : Finset ℕ) := hF 1 (by simp)
  refine ⟨w, hs, fun hd => absurd (hE1.1 hd) (by simp), h3, hF1.2 (Finset.mem_singleton_self 1), ?_, ?_⟩
  · exact hnew 9 (by decide) (by decide)
  · exact hnew 18 (by decide) (by decide)

/-- `sizes_eq` used: on Z_18 and on Z_6 the same sizes occur for "Φ_2 and Φ_3 divide, Φ_6 does not (and on Z_18 neither Φ_9
nor Φ_18)".  Stated with the sets of the theorem; here only that the instance type-checks with P = {2, 3}. -/
example := sizes_eq (N := 6) (r := 3) (by decide) {2, 3} (by decide)

/-- `exists_lift` + `cyclotomic_dvd_reduce_iff` + `sum_reduce` used together: every nonempty multiset on Z_6 has, on Z_18, a
multiset with the same number of elements, the same answers for Φ_1, Φ_2, Φ_3, Φ_6, and neither Φ_9 nor Φ_18. -/
theorem use_lift (w : ZMod 6 → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (6 * 3) → ℕ, ∑ y, w' y = ∑ x, w x ∧
      (∀ d, d ∣ 6 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ Polynomial.cyclotomic d ℤ ∣ maskW w)) ∧
      ¬ Polynomial.cyclotomic 9 ℤ ∣ maskW w' ∧ ¬ Polynomial.cyclotomic 18 ℤ ∣ maskW w' := by
  obtain ⟨w', hred, hnew⟩ := exists_lift (N := 6) (r := 3) (by decide) w hw
  subst hred
  exact ⟨w', (sum_reduce w').symm, fun d hd => (cyclotomic_dvd_reduce_iff w' d hd).symm,
    hnew 9 (by decide) (by decide), hnew 18 (by decide) (by decide)⟩

end AuditUse
#print axioms AuditUse.use_18_lower
#print axioms AuditUse.use_18_attained
#print axioms AuditUse.use_lift
