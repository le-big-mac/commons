import Pnq.EvenWhole

/-! Audit of the evening of 27 November (statements U and Corollary U): reading lemmas.  What is proved here WITHOUT
the two `sorry` statements is marked "free"; what is derived FROM them is marked "from U" / "from W" and shows how
the statements can be used.  Scratch file of the audit; nothing else uses it. -/

open Pnq Finset

namespace AuditUnion

/-! ### U: boundary cases (free) -/

/-- `κ` empty: no signing is in either set -/
theorem no_system {ι : Type*} [Fintype ι] {V : Type*} [AddCommGroup V] (pos : ι → ℕ) (val : PEmpty → ι → V)
    (K : ℕ) (ε : ι → Bool) : ¬ ∃ c, ∃ j, j ≤ K ∧ levelBad pos (val c) ε j := by
  rintro ⟨c, _⟩
  exact c.elim

/-- `ι` empty: every level is bad -/
theorem no_element {V : Type*} [AddCommGroup V] (pos : PEmpty → ℕ) (val : PEmpty → V) (ε : PEmpty → Bool)
    (j : ℕ) : levelBad pos val ε j := by
  cases j with
  | zero => simp [levelBad]
  | succ j =>
    intro r _
    simp [csum]

/-- all values `0`: every level is bad -/
theorem all_zero {ι : Type*} [Fintype ι] {V : Type*} [AddCommGroup V] (pos : ι → ℕ) (ε : ι → Bool) (j : ℕ) :
    levelBad pos (fun _ => (0 : V)) ε j := by
  cases j with
  | zero => simp [levelBad]
  | succ j =>
    intro r _
    simp [csum]

/-! ### U: one group `V` for all `c` against a group `V c` for each `c` -/

/-- (free) class sums go through an additive map -/
theorem csum_map {ι : Type*} [Fintype ι] {V W : Type*} [AddCommGroup V] [AddCommGroup W] (f : V →+ W)
    (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (M r : ℕ) :
    csum pos (fun k => f (val k)) ε M r = f (csum pos val ε M r) := by
  unfold csum
  rw [map_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  split_ifs
  · rw [map_zsmul]
  · rw [map_zero]

/-- (free) "level `j` is bad" is the same for the values and for their images under an injective additive map -/
theorem levelBad_map {ι : Type*} [Fintype ι] {V W : Type*} [AddCommGroup V] [AddCommGroup W] (f : V →+ W)
    (hf : Function.Injective f) (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (j : ℕ) :
    levelBad pos (fun k => f (val k)) ε j ↔ levelBad pos val ε j := by
  cases j with
  | zero =>
    rw [levelBad_zero, levelBad_zero]
    have h : ∑ k, sg (ε k) • f (val k) = f (∑ k, sg (ε k) • val k) := by
      rw [map_sum]
      exact Finset.sum_congr rfl fun k _ => (map_zsmul f _ _).symm
    rw [h]
    exact map_eq_zero_iff f hf
  | succ j =>
    rw [levelBad_succ, levelBad_succ]
    refine forall_congr' fun r => forall_congr' fun _ => ?_
    rw [csum_map, csum_map]
    exact hf.eq_iff

open Classical in
/-- (from U) the note's form, a group `V c` for each `c`: take the product of the groups -/
theorem U_family {ι : Type*} [Fintype ι] {κ : Type*} {V : κ → Type*} [∀ c, AddCommGroup (V c)]
    (pos : ι → ℕ) (val : ∀ c, ι → V c) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ c, ∃ j, j ≤ K ∧ levelBad pos (val c) ε j).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => ∃ c, levelBad pos (val c) ε 0).card := by
  have h := card_exists_exists_levelBad_le (V := ∀ c, V c) pos
    (fun c k => AddMonoidHom.single V c (val c k)) K
  have e1 : ∀ (ε : ι → Bool) (c : κ) (j : ℕ),
      levelBad pos (fun k => AddMonoidHom.single V c (val c k)) ε j ↔ levelBad pos (val c) ε j :=
    fun ε c j => levelBad_map _ (Pi.single_injective c) pos (val c) ε j
  simp only [e1] at h
  exact h

open Classical in
/-- (from U) T, one system, is U for `κ = Unit` -/
theorem T_of_U {ι : Type*} [Fintype ι] {V : Type*} [AddCommGroup V] (pos : ι → ℕ) (val : ι → V) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ levelBad pos val ε j).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => levelBad pos val ε 0).card := by
  have h := card_exists_exists_levelBad_le (κ := Unit) pos (fun _ => val) K
  simp only [exists_const] at h
  exact h

/-- (from U) the systems that Corollary U needs fit: indices the natural numbers, values in `ℂ` -/
example {ι : Type*} [Fintype ι] (e : ι → ℕ) (η : ℕ → ℂ) (k : ℕ) :=
  card_exists_exists_levelBad_le e (fun (c : {d : ℕ // d ∣ 15}) (i : ι) => η c.1 ^ e i) k

/-! ### Corollary U: boundary cases -/

/-- (free) `d = 0` is not among the divisors when `n'` is odd -/
theorem divisor_ne_zero (k n' d : ℕ) (hn' : ¬ 2 ∣ n') (h : d ∣ 2 ^ k * n') : d ≠ 0 := by
  rintro rfl
  have h0 : 2 ^ k * n' = 0 := Nat.eq_zero_of_zero_dvd h
  rcases Nat.mul_eq_zero.mp h0 with h1 | h1
  · exact absurd h1 (by positivity)
  · exact hn' (h1 ▸ dvd_zero 2)

/-- (free) at `d = 0` every signing is bad (`Φ_0 = 1` in Mathlib) -/
theorem badAt_zero {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) : BadAt e ε 0 := by
  unfold BadAt
  rw [Polynomial.cyclotomic_zero]
  exact one_dvd _

/-- (free) no element: the one signing is bad at every `d` -/
theorem badAt_empty (e : PEmpty → ℕ) (ε : PEmpty → Bool) (d : ℕ) : BadAt e ε d := by
  unfold BadAt P
  simp

/-- (free) bad at `1` is "the signs add up to `0`" -/
theorem badAt_one_iff {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) :
    BadAt e ε 1 ↔ ∑ k, sg (ε k) = 0 := by
  unfold BadAt P
  rw [Polynomial.cyclotomic_one,
    show (Polynomial.X - 1 : Polynomial ℤ) = Polynomial.X - Polynomial.C 1 by simp, Polynomial.dvd_iff_isRoot]
  rw [Polynomial.IsRoot.def, ← Polynomial.coe_evalRingHom, map_sum]
  simp

open Classical in
/-- (from W) the statement without the hypothesis "`n'` odd": it follows from the statement for the odd part of `n'`
(and for `n' = 0` both sets are the same) -/
theorem whole_any {ι : Type*} [Fintype ι] (e : ι → ℕ) (k n' : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k * n' ∧ BadAt e ε d).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ n' ∧ BadAt e ε d).card := by
  rcases Nat.eq_zero_or_pos n' with rfl | hpos
  · simp only [mul_zero]
    omega
  · obtain ⟨a, m, hm, rfl⟩ := Nat.exists_eq_two_pow_mul_odd hpos.ne'
    have hodd : ¬ 2 ∣ m := fun h2 => (Nat.not_even_iff_odd.mpr hm) (even_iff_two_dvd.mpr h2)
    have h := card_exists_badAt_le e (k + a) hodd
    rw [← mul_assoc, ← pow_add]
    refine h.trans (Nat.mul_le_mul_left 2 (Finset.card_le_card ?_))
    intro ε hε
    rw [Finset.mem_filter] at hε ⊢
    obtain ⟨hu, d, hd, hb⟩ := hε
    exact ⟨hu, d, Dvd.dvd.mul_left hd _, hb⟩

end AuditUnion

#print axioms AuditUnion.no_system
#print axioms AuditUnion.no_element
#print axioms AuditUnion.all_zero
#print axioms AuditUnion.levelBad_map
#print axioms AuditUnion.U_family
#print axioms AuditUnion.T_of_U
#print axioms AuditUnion.divisor_ne_zero
#print axioms AuditUnion.badAt_zero
#print axioms AuditUnion.badAt_empty
#print axioms AuditUnion.badAt_one_iff
#print axioms AuditUnion.whole_any
