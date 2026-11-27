import Pnq.SetAll
/-! Audit: small facts, proved in Lean, about how the five statements are to be read; the paper's wording of the proposition derived
from `exists_set_lift`; instances showing that no hypothesis is contradictory; one concrete fact in the auditor's own words derived
from `minsize_unbalanced_set`.  Nothing here is used by anything else.  The five theorems are `sorry` in this copy, so everything that
uses one of them depends on `sorryAx`; what is checked is that the statements fit together as the paper's wording needs. -/
open Finset

namespace AuditSets

/-! ### The types -/

example (N r j : ℕ) : N * r ^ j = N * (r ^ j) := rfl
example (p q n s : ℕ) : p ^ n * q * s = (p ^ n * q) * s := rfl
-- every `NeZero` and `Fact` argument is a proof of a proposition, so which instance Lean found cannot matter
example (n : ℕ) (h₁ h₂ : NeZero n) : h₁ = h₂ := rfl
example (r : ℕ) (h₁ h₂ : Fact r.Prime) : h₁ = h₂ := rfl
-- `0` divides none of the orders
example (N r j : ℕ) [NeZero N] [Fact r.Prime] : ¬ (0 ∣ N * r ^ j) := by
  intro h
  exact NeZero.ne (N * r ^ j) (Nat.eq_zero_of_zero_dvd h)
example (p q n s : ℕ) [Fact p.Prime] [Fact q.Prime] [NeZero s] : ¬ (0 ∣ p ^ n * q * s) := by
  intro h
  exact NeZero.ne (p ^ n * q * s) (Nat.eq_zero_of_zero_dvd h)
-- membership in a set written `{t | P t}` is `P`
example (P : ℕ → Prop) (a : ℕ) : a ∈ {t | P t} ↔ P a := Iff.rfl

/-! ### The reduction modulo `N` in `exists_set_lift` -/

/-- the map sends `y` to the residue of its representative modulo `N` -/
theorem val_castHom {N m : ℕ} [NeZero N] [NeZero m] (y : ZMod (N * m)) :
    (ZMod.castHom (Nat.dvd_mul_right N m) (ZMod N) y).val = y.val % N := by
  rw [ZMod.castHom_apply, ← ZMod.natCast_val, ZMod.val_natCast]

theorem castHom_eq_iff {N m : ℕ} [NeZero N] [NeZero m] (y : ZMod (N * m)) (x : ZMod N) :
    ZMod.castHom (Nat.dvd_mul_right N m) (ZMod N) y = x ↔ y.val % N = x.val := by
  rw [← val_castHom]
  exact ⟨fun h => by rw [h], fun h => ZMod.val_injective N h⟩

/-- the fibre counts add up to the number of elements of the set: "as many elements as `A`" is in the statement -/
theorem card_eq_sum_of_fibres {N m : ℕ} [NeZero N] (A : Finset (ZMod (N * m))) (w : ZMod N → ℕ)
    (h : ∀ x : ZMod N,
      (A.filter (fun y => ZMod.castHom (Nat.dvd_mul_right N m) (ZMod N) y = x)).card = w x) :
    A.card = ∑ x, w x := by
  rw [Finset.card_eq_sum_card_fiberwise (f := fun y => ZMod.castHom (Nat.dvd_mul_right N m) (ZMod N) y)
    (t := Finset.univ) (fun _ _ => Finset.mem_univ _)]
  exact Finset.sum_congr rfl fun x _ => h x

/-- the fibre count over `x` is the multiplicity of `x` in the reduction of the multiset `indW A` (the sum that defines
`Pnq.Lift.reduce`, with `r ^ j` in place of `r`) -/
theorem fibre_card_eq_sum {N m : ℕ} [NeZero N] [NeZero m] (A : Finset (ZMod (N * m))) (x : ZMod N) :
    (A.filter (fun y => ZMod.castHom (Nat.dvd_mul_right N m) (ZMod N) y = x)).card
      = ∑ y : ZMod (N * m), if ZMod.castHom (Nat.dvd_mul_right N m) (ZMod N) y = x then Pnq.indW A y else 0 := by
  rw [Finset.card_filter, ← Finset.sum_subset (Finset.subset_univ A)]
  · refine Finset.sum_congr rfl fun y hy => ?_
    have h1 : Pnq.indW A y = 1 := by simp [Pnq.indW, hy]
    rw [h1]
  · intro y _ hy
    have h0 : Pnq.indW A y = 0 := by simp [Pnq.indW, hy]
    rw [h0]
    split_ifs <;> rfl

/-- the number of elements of the multiset of a set -/
theorem sum_indW {M : ℕ} [NeZero M] (A : Finset (ZMod M)) : ∑ a, Pnq.indW A a = A.card := by
  unfold Pnq.indW
  rw [Fintype.sum_ite_mem]
  simp

/-! ### `j = 0`, and the hypotheses `hle`, `hne` in the paper's words -/

-- for `j = 0` the two hypotheses of `exists_set_lift` contradict each other: the statement says nothing there
example {N r : ℕ} (w : ZMod N → ℕ) (hle : ∀ x, w x ≤ r ^ 0) (hne : ∃ x, w x ≠ 0 ∧ w x ≠ r ^ 0) : False := by
  obtain ⟨x, h0, h1⟩ := hne
  have h := hle x
  rw [pow_zero] at h h1
  omega

-- "nonempty, every multiplicity at most r^j, not every element of the multiset of multiplicity r^j" is `hle` and `hne`
theorem paper_hyp_iff {N r j : ℕ} (w : ZMod N → ℕ) :
    ((∀ x, w x ≤ r ^ j) ∧ ∃ x, w x ≠ 0 ∧ w x ≠ r ^ j) ↔
    ((∃ x, w x ≠ 0) ∧ (∀ x, w x ≤ r ^ j) ∧ ¬ ∀ x, w x ≠ 0 → w x = r ^ j) := by
  constructor
  · rintro ⟨hle, x, h0, h1⟩
    exact ⟨⟨x, h0⟩, hle, fun h => h1 (h x h0)⟩
  · rintro ⟨_, hle, hn⟩
    refine ⟨hle, ?_⟩
    by_contra hc
    exact hn fun x h0 => by
      by_contra h1
      exact hc ⟨x, h0, h1⟩

-- in `set_sizes_iff_mul`, `j = 0` leaves only `t = 0`, for which both sides are false
example (r t : ℕ) (ht : t < r ^ 0) : ¬ (0 < t) := by
  rw [pow_zero] at ht
  omega

-- the values of the rule are at least 1, so `hm` cannot hold with `j = 0` in the three least-size statements
theorem minU_pos (p q : ℕ) (hp : 0 < p) (Es Fs : Finset ℕ) : 0 < Pnq.minU p q Es Fs := by
  unfold Pnq.minU
  have h1 : 0 < p ^ Es.card := Nat.pow_pos hp
  have h2 : 0 < p ^ (Fs \ Es).card := Nat.pow_pos hp
  split_ifs
  · exact h1
  · exact Nat.mul_pos h1 (by omega)
theorem minB_pos (p q : ℕ) (hp : 0 < p) (hq : 0 < q) (Es Fs : Finset ℕ) (a0 : ℕ) : 0 < Pnq.minB p q Es Fs a0 := by
  unfold Pnq.minB
  have h1 : 0 < p ^ Es.card := Nat.pow_pos hp
  have h2 : 0 < p ^ (Pnq.gOf Es Fs a0).card := Nat.pow_pos hp
  exact Nat.mul_pos (Nat.mul_pos hq h1) (by omega)

/-! ### `d = 1`, the empty set -/

example : Polynomial.cyclotomic 0 ℤ = 1 := Polynomial.cyclotomic_zero ℤ
example : Polynomial.cyclotomic 1 ℤ = Polynomial.X - 1 := Polynomial.cyclotomic_one ℤ
theorem maskW_zero {M : ℕ} [NeZero M] : Pnq.maskW (fun _ : ZMod M => 0) = 0 := by
  simp [Pnq.maskW]
theorem indW_empty {M : ℕ} : Pnq.indW (∅ : Finset (ZMod M)) = fun _ => 0 := by
  funext a
  simp [Pnq.indW]
-- every `Φ_d` divides the mask of the empty set
example {M : ℕ} [NeZero M] (d : ℕ) : Polynomial.cyclotomic d ℤ ∣ Pnq.maskW (Pnq.indW (∅ : Finset (ZMod M))) := by
  rw [indW_empty, maskW_zero]; exact dvd_zero _
theorem eval_one_maskW {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    (Pnq.maskW w).eval 1 = ((∑ a, w a : ℕ) : ℤ) := by
  unfold Pnq.maskW
  rw [← Polynomial.coe_evalRingHom, map_sum]
  simp
/-- `Φ_1` divides the mask only of the empty multiset -/
theorem cyclotomic_one_dvd_iff {M : ℕ} [NeZero M] (w : ZMod M → ℕ) :
    Polynomial.cyclotomic 1 ℤ ∣ Pnq.maskW w ↔ ∑ a, w a = 0 := by
  have h1 : (Polynomial.X - 1 : Polynomial ℤ) = Polynomial.X - Polynomial.C 1 := by simp
  rw [Polynomial.cyclotomic_one, h1, Polynomial.dvd_iff_isRoot, Polynomial.IsRoot.def, eval_one_maskW]
  exact_mod_cast Iff.rfl
/-- so the clause `d = 1` of `exists_set_lift` adds nothing to the fibre counts: it says "the set is empty iff the multiset is" -/
theorem clause_one_of_fibres {N m : ℕ} [NeZero N] [NeZero m] (A : Finset (ZMod (N * m))) (w : ZMod N → ℕ)
    (h : ∀ x : ZMod N,
      (A.filter (fun y => ZMod.castHom (Nat.dvd_mul_right N m) (ZMod N) y = x)).card = w x) :
    (Polynomial.cyclotomic 1 ℤ ∣ Pnq.maskW (Pnq.indW A) ↔ 1 ∣ N ∧ Polynomial.cyclotomic 1 ℤ ∣ Pnq.maskW w) := by
  rw [cyclotomic_one_dvd_iff, cyclotomic_one_dvd_iff, sum_indW, card_eq_sum_of_fibres A w h]
  exact ⟨fun h0 => ⟨one_dvd N, h0⟩, fun h0 => h0.2⟩

/-! ### The paper's Proposition "lifting to a set", as worded, from `exists_set_lift` -/

/-- `r` an odd prime, `N ≥ 1`, a multiset on `Z_N` with every multiplicity at most `r^j` and not every element of it of multiplicity
`r^j` (so it is nonempty): there is a set on `Z_{N r^j}` with as many elements, whose reduction modulo `N` is the multiset (the
number of elements of the set with residue `x` is the multiplicity of `x`), such that for every `d ∣ N r^j`: `Φ_d` divides the mask
of the set iff `d ∣ N` and `Φ_d` divides the mask of the multiset. -/
theorem paper_setlift {N r : ℕ} [NeZero N] [Fact r.Prime] (hr : r ≠ 2) (j : ℕ)
    (w : ZMod N → ℕ) (hle : ∀ x, w x ≤ r ^ j) (hnot : ¬ ∀ x, w x ≠ 0 → w x = r ^ j) :
    ∃ A : Finset (ZMod (N * r ^ j)),
      A.card = ∑ x, w x ∧
      (∀ x : ZMod N, (A.filter (fun y => y.val % N = x.val)).card = w x) ∧
      ∀ d, d ∣ N * r ^ j →
        (Polynomial.cyclotomic d ℤ ∣ Pnq.maskW (Pnq.indW A) ↔ d ∣ N ∧ Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w) := by
  have hne : ∃ x, w x ≠ 0 ∧ w x ≠ r ^ j := by
    by_contra hc
    exact hnot fun x h0 => by
      by_contra h1
      exact hc ⟨x, h0, h1⟩
  obtain ⟨A, hfib, hdiv⟩ := Pnq.Lift.exists_set_lift hr j w hle hne
  refine ⟨A, card_eq_sum_of_fibres A w hfib, fun x => ?_, hdiv⟩
  rw [← hfib x]
  congr 1
  exact Finset.filter_congr fun y _ => (castHom_eq_iff y x).symm

/-- the same in the form "same old divisors, no new divisor" -/
theorem paper_setlift' {N r : ℕ} [NeZero N] [Fact r.Prime] (hr : r ≠ 2) (j : ℕ)
    (w : ZMod N → ℕ) (hle : ∀ x, w x ≤ r ^ j) (hne : ∃ x, w x ≠ 0 ∧ w x ≠ r ^ j) :
    ∃ A : Finset (ZMod (N * r ^ j)), A.card = ∑ x, w x ∧
      (∀ d, d ∣ N → (Polynomial.cyclotomic d ℤ ∣ Pnq.maskW (Pnq.indW A) ↔ Polynomial.cyclotomic d ℤ ∣ Pnq.maskW w)) ∧
      ∀ d, d ∣ N * r ^ j → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ Pnq.maskW (Pnq.indW A) := by
  obtain ⟨A, hfib, hdiv⟩ := Pnq.Lift.exists_set_lift hr j w hle hne
  refine ⟨A, card_eq_sum_of_fibres A w hfib, fun d hd => ?_, fun d hd hnd hc => hnd ((hdiv d hd).1 hc).1⟩
  rw [hdiv d (Dvd.dvd.mul_right hd _)]
  exact ⟨fun h => h.2, fun h => ⟨hd, h⟩⟩

/-! ### The statements can be used: no hypothesis is contradictory -/

instance : Fact (Nat.Prime 2) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 3) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 5) := ⟨by norm_num⟩
instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩

example (w : ZMod 6 → ℕ) (hle : ∀ x, w x ≤ 3 ^ 2) (hne : ∃ x, w x ≠ 0 ∧ w x ≠ 3 ^ 2) :=
  Pnq.Lift.exists_set_lift (N := 6) (r := 3) (by decide) 2 w hle hne
example (w : ZMod 1 → ℕ) (hle : ∀ x, w x ≤ 7 ^ 1) (hne : ∃ x, w x ≠ 0 ∧ w x ≠ 7 ^ 1) :=
  Pnq.Lift.exists_set_lift (N := 1) (r := 7) (by decide) 1 w hle hne
-- a concrete multiset for which both hypotheses hold: 0 twice on Z_6, with r^j = 9
example :=
  Pnq.Lift.exists_set_lift (N := 6) (r := 3) (by decide) 2 (fun x => if x = 0 then 2 else 0)
    (fun x => by split_ifs <;> norm_num) ⟨0, by norm_num, by norm_num⟩
-- r = q, r = p, p = 2, q = 2, n = 0, s with further factors (even, multiples of p, q, another prime): all allowed
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 2 ^ 1 * 3) (t : ℕ) (ht : t < 3 ^ 2) :=
  Pnq.Lift.set_sizes_iff_mul 2 3 1 18 3 2 (by decide) (by decide) (by decide) P hP t ht
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 3 ^ 2 * 2) (t : ℕ) (ht : t < 3 ^ 1) :=
  Pnq.Lift.set_sizes_iff_mul 3 2 2 30 3 1 (by decide) (by decide) (by decide) P hP t ht
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 5 ^ 0 * 2) (t : ℕ) (ht : t < 7 ^ 1) :=
  Pnq.Lift.set_sizes_iff_mul 5 2 0 7 7 1 (by decide) (by decide) (by decide) P hP t ht
example := Pnq.Lift.minsize_unbalanced_set 3 2 0 45 3 2 (by decide) (by decide) (by decide) ∅ ∅ (by decide) (by decide)
  (by decide)
example := Pnq.Lift.minsize_unbalanced_set 2 3 1 9 3 2 (by decide) (by decide) (by decide) ∅ {1} (by decide) (by decide)
  (by decide)
example := Pnq.Lift.minsize_balanced_all_set 2 3 1 50 5 2 (by decide) (by decide) (by decide) {1} (by decide) (by decide)
example := Pnq.Lift.minsize_balanced_all_set 3 5 0 7 7 1 (by decide) (by decide) (by decide) ∅ (by decide) (by decide)
example := Pnq.Lift.minsize_balanced_set 2 3 2 25 5 2 (by decide) (by decide) (by decide) {1} {2} (by decide) (by decide) 1
  (by decide) (by decide) (by decide) (by decide) (by decide)
-- the third statement has no instance for n = 0, as before
example (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ 0) : False := by omega

/-! ### One concrete fact, in the auditor's words, from `minsize_unbalanced_set` -/

open Pnq Pnq.Lift

example : 2 ^ 1 * 3 * 9 = 54 := rfl
example : minU 2 3 ∅ {1} = 5 := by decide

/-- On Z_54 (= ZMod (2^1 * 3 * 9)): a SET whose mask is divisible by Φ_6 and by none of Φ_2, Φ_3, Φ_9, Φ_18, Φ_27, Φ_54 has at
least 5 elements.  From `minsize_unbalanced_set` with p = 2, q = 3, n = 1, s = 9, r = 3, j = 2, Es = ∅, Fs = {1}. -/
theorem use_54_lower (A : Finset (ZMod (2 ^ 1 * 3 * 9)))
    (h2 : ¬ Polynomial.cyclotomic 2 ℤ ∣ maskW (indW A)) (h3 : ¬ Polynomial.cyclotomic 3 ℤ ∣ maskW (indW A))
    (h6 : Polynomial.cyclotomic 6 ℤ ∣ maskW (indW A))
    (h9 : ¬ Polynomial.cyclotomic 9 ℤ ∣ maskW (indW A)) (h18 : ¬ Polynomial.cyclotomic 18 ℤ ∣ maskW (indW A))
    (h27 : ¬ Polynomial.cyclotomic 27 ℤ ∣ maskW (indW A)) (h54 : ¬ Polynomial.cyclotomic 54 ℤ ∣ maskW (indW A)) :
    5 ≤ A.card := by
  have h := (minsize_unbalanced_set 2 3 1 9 3 2 (by decide) (by decide) (by decide) ∅ {1} (by simp) (by simp)
    (by decide)).2
  have hv : minU 2 3 ∅ {1} = 5 := by decide
  rw [hv] at h
  refine h ⟨A, rfl, h3, ?_, ?_, ?_⟩
  · intro ℓ hℓ
    have h1 : ℓ = 1 := by
      have := Finset.mem_Icc.1 hℓ
      omega
    subst h1
    change Polynomial.cyclotomic 2 ℤ ∣ maskW (indW A) ↔ 1 ∈ (∅ : Finset ℕ)
    exact ⟨fun hd => absurd hd h2, fun hm => absurd hm (by simp)⟩
  · intro ℓ hℓ
    have h1 : ℓ = 1 := by
      have := Finset.mem_Icc.1 hℓ
      omega
    subst h1
    change Polynomial.cyclotomic 6 ℤ ∣ maskW (indW A) ↔ 1 ∈ ({1} : Finset ℕ)
    exact ⟨fun _ => Finset.mem_singleton_self 1, fun _ => h6⟩
  · intro d hd hnd
    have hle : d ≤ 54 := Nat.le_of_dvd (by norm_num) hd
    interval_cases d <;> first
      | exact absurd hd (by decide)
      | exact absurd (by decide) hnd
      | assumption

/-- and such a set with exactly 5 elements exists -/
theorem use_54_attained : ∃ A : Finset (ZMod (2 ^ 1 * 3 * 9)), A.card = 5 ∧
    ¬ Polynomial.cyclotomic 2 ℤ ∣ maskW (indW A) ∧ ¬ Polynomial.cyclotomic 3 ℤ ∣ maskW (indW A) ∧
    Polynomial.cyclotomic 6 ℤ ∣ maskW (indW A) ∧
    ¬ Polynomial.cyclotomic 9 ℤ ∣ maskW (indW A) ∧ ¬ Polynomial.cyclotomic 18 ℤ ∣ maskW (indW A) ∧
    ¬ Polynomial.cyclotomic 27 ℤ ∣ maskW (indW A) ∧ ¬ Polynomial.cyclotomic 54 ℤ ∣ maskW (indW A) := by
  have h := (minsize_unbalanced_set 2 3 1 9 3 2 (by decide) (by decide) (by decide) ∅ {1} (by simp) (by simp)
    (by decide)).1
  have hv : minU 2 3 ∅ {1} = 5 := by decide
  rw [hv] at h
  obtain ⟨A, hs, h3, hE, hF, hnew⟩ := h
  have hE1 : Polynomial.cyclotomic 2 ℤ ∣ maskW (indW A) ↔ 1 ∈ (∅ : Finset ℕ) := hE 1 (by simp)
  have hF1 : Polynomial.cyclotomic 6 ℤ ∣ maskW (indW A) ↔ 1 ∈ ({1} : Finset ℕ) := hF 1 (by simp)
  exact ⟨A, hs, fun hd => absurd (hE1.1 hd) (by simp), h3, hF1.2 (Finset.mem_singleton_self 1),
    hnew 9 (by decide) (by decide), hnew 18 (by decide) (by decide), hnew 27 (by decide) (by decide),
    hnew 54 (by decide) (by decide)⟩

/-- a set is a multiset: the sizes of sets with a pattern are among the sizes of multisets with it (the easy half of
`set_sizes_iff_mul`, on the big group; no hypothesis on `t`) -/
theorem set_is_multiset {M : ℕ} [NeZero M] (P : Finset ℕ) (t : ℕ)
    (h : ∃ A : Finset (ZMod M), A.card = t ∧ 0 < t ∧
        ∀ d, d ∣ M → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW (indW A) ↔ d ∈ P)) :
    ∃ w : ZMod M → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ M → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P) := by
  obtain ⟨A, hc, ht, hp⟩ := h
  exact ⟨indW A, (sum_indW A).trans hc, ht, hp⟩

end AuditSets

#print axioms AuditSets.val_castHom
#print axioms AuditSets.card_eq_sum_of_fibres
#print axioms AuditSets.fibre_card_eq_sum
#print axioms AuditSets.cyclotomic_one_dvd_iff
#print axioms AuditSets.clause_one_of_fibres
#print axioms AuditSets.paper_hyp_iff
#print axioms AuditSets.minU_pos
#print axioms AuditSets.minB_pos
#print axioms AuditSets.set_is_multiset
#print axioms AuditSets.paper_setlift
#print axioms AuditSets.paper_setlift'
#print axioms AuditSets.use_54_lower
#print axioms AuditSets.use_54_attained
