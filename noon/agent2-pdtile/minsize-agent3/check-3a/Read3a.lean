import Pnq.MinGroup
/-! Scratch file of the reader of section 3a (26 November 2026).  Nothing here is part of the development. -/
open Finset

namespace Read3a

/-- The hypotheses on `a0` of the third statement. -/
def IsFirstMissing (n : ℕ) (Fs : Finset ℕ) (a0 : ℕ) : Prop :=
  1 ≤ a0 ∧ a0 ≤ n ∧ (∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) ∧ a0 ∉ Fs

/-- "The three cover every pattern once", the part about `a0`: if `Fs` is all of `1..n` no `a0` meets the
hypotheses of the third statement, and if it is not, exactly one does. -/
theorem cover (n : ℕ) (Fs : Finset ℕ) (hF : Fs ⊆ Finset.Icc 1 n) :
    (Fs = Finset.Icc 1 n ∧ ¬ ∃ a0, IsFirstMissing n Fs a0) ∨
    (Fs ≠ Finset.Icc 1 n ∧ ∃! a0, IsFirstMissing n Fs a0) := by
  by_cases h : Fs = Finset.Icc 1 n
  · left
    refine ⟨h, ?_⟩
    rintro ⟨a0, h1, h2, -, h4⟩
    exact h4 (h ▸ Finset.mem_Icc.2 ⟨h1, h2⟩)
  · right
    refine ⟨h, ?_⟩
    have hex : ∃ a, a ∈ Finset.Icc 1 n ∧ a ∉ Fs := by
      by_contra hno
      apply h
      apply Finset.Subset.antisymm hF
      intro a ha
      by_contra haF
      exact hno ⟨a, ha, haF⟩
    classical
    refine ⟨Nat.find hex, ⟨?_, ?_, ?_, ?_⟩, ?_⟩
    · exact (Finset.mem_Icc.1 (Nat.find_spec hex).1).1
    · exact (Finset.mem_Icc.1 (Nat.find_spec hex).1).2
    · intro ℓ h1 hlt
      by_contra hℓ
      have hn : ℓ ≤ n := le_trans (le_of_lt hlt) (Finset.mem_Icc.1 (Nat.find_spec hex).1).2
      exact Nat.find_min hex hlt ⟨Finset.mem_Icc.2 ⟨h1, hn⟩, hℓ⟩
    · exact (Nat.find_spec hex).2
    · rintro b ⟨hb1, hbn, hblow, hbF⟩
      have hle : Nat.find hex ≤ b := Nat.find_min' hex ⟨Finset.mem_Icc.2 ⟨hb1, hbn⟩, hbF⟩
      rcases Nat.lt_or_eq_of_le hle with hlt | heq
      · exact absurd (hblow _ (Finset.mem_Icc.1 (Nat.find_spec hex).1).1 hlt) (Nat.find_spec hex).2
      · exact heq.symm

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

/-- the empty multiset has mask polynomial `0` -/
theorem maskW_zero : Pnq.maskW (fun _ : ZMod (p ^ n * q) => 0) = 0 := by
  simp [Pnq.maskW]

/-- "The empty multiset has every Φ_d as a divisor, so it belongs to the second statement's pattern with E
every level" -/
theorem empty_pattern :
    Polynomial.cyclotomic q ℤ ∣ Pnq.maskW (fun _ : ZMod (p ^ n * q) => 0) ∧
    Pnq.levelsEW (fun _ : ZMod (p ^ n * q) => 0) = Finset.Icc 1 n ∧
    Pnq.levelsFW (fun _ : ZMod (p ^ n * q) => 0) = Finset.Icc 1 n := by
  refine ⟨?_, ?_, ?_⟩
  · rw [maskW_zero]; exact dvd_zero _
  · ext ℓ
    simp [Pnq.levelsEW, maskW_zero]
  · ext ℓ
    simp [Pnq.levelsFW, maskW_zero]

/-- a multiset with no element is the empty one -/
theorem eq_zero_of_sum (w : ZMod (p ^ n * q) → ℕ) (h : ∑ a, w a = 0) : w = fun _ => 0 := by
  funext a
  exact (Finset.sum_eq_zero_iff.1 h) a (Finset.mem_univ a)

/-- "in the other two the pattern itself shuts it out": first statement -/
theorem first_not_empty (w : ZMod (p ^ n * q) → ℕ) (h0 : ¬ Polynomial.cyclotomic q ℤ ∣ Pnq.maskW w) :
    0 < ∑ a, w a := by
  by_contra hs
  have hw := eq_zero_of_sum w (by omega)
  subst hw
  exact h0 (empty_pattern (p := p) (q := q) (n := n)).1

/-- "in the other two the pattern itself shuts it out": third statement -/
theorem third_not_empty (w : ZMod (p ^ n * q) → ℕ) (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hna : a0 ∉ Pnq.levelsFW w) : 0 < ∑ a, w a := by
  by_contra hs
  have hw := eq_zero_of_sum w (by omega)
  subst hw
  rw [(empty_pattern (p := p) (q := q) (n := n)).2.2] at hna
  exact hna (Finset.mem_Icc.2 ⟨ha1, han⟩)

/-- Item 2 of "In short" for multisets on the group, in terms of the cyclotomic polynomials: not a named
theorem of the eleven files; here from the tree bound of section 2a and the new bridge. -/
theorem item2_from_bridge (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ)
    (h0 : ¬ Polynomial.cyclotomic q ℤ ∣ Pnq.maskW w) :
    p ^ (Pnq.levelsEW w ∪ Pnq.levelsFW w).card ≤ ∑ a, w a := by
  have hp : p.Prime := Fact.out
  have h := Pnq.pow_card_union_le_size (q := q) hp.two_le (Pnq.treeOfW w)
    (fun h => h0 ((Pnq.MinGroupAux.F_treeOfW_zero_iff w).1 h))
  rwa [Pnq.MinGroupAux.eSet_treeOfW, Pnq.MinGroupAux.fSet_treeOfW hpq, Pnq.size_treeOfW] at h

/-- The same from the first of the three statements alone. -/
theorem item2_from_first (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ)
    (h0 : ¬ Polynomial.cyclotomic q ℤ ∣ Pnq.maskW w) :
    p ^ (Pnq.levelsEW w ∪ Pnq.levelsFW w).card ≤ ∑ a, w a := by
  have hp : p.Prime := Fact.out
  have hE : Pnq.levelsEW w ⊆ Finset.Icc 1 n := by
    classical
    exact Finset.filter_subset _ _
  have hF : Pnq.levelsFW w ⊆ Finset.Icc 1 n := by
    classical
    exact Finset.filter_subset _ _
  have h := (Pnq.minsize_unbalanced_zmod p q n hpq (Pnq.levelsEW w) (Pnq.levelsFW w) hE hF).2
    ⟨w, rfl, h0, rfl, rfl⟩
  refine le_trans ?_ h
  have hcard : (Pnq.levelsEW w ∪ Pnq.levelsFW w).card
      = (Pnq.levelsEW w).card + (Pnq.levelsFW w \ Pnq.levelsEW w).card := by
    rw [← Finset.union_sdiff_self_eq_union, Finset.card_union_of_disjoint Finset.disjoint_sdiff]
  unfold Pnq.minU
  split_ifs with hsub
  · rw [Finset.union_eq_left.2 hsub]
  · rw [hcard, pow_add]
    exact Nat.mul_le_mul_left _ (Nat.le_add_right _ _)

/-- An instance, to see that a statement is not empty of content: in `Z_54` (`p = 3`, `q = 2`, `n = 3`)
the least multiset with `Φ_2 ∤ A`, no `Φ_{3^ℓ}` dividing and `Φ_{3^ℓ·2} ∣ A` exactly for `ℓ = 1` has 5 elements. -/
example : IsLeast {s | ∃ w : ZMod (3 ^ 3 * 2) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic 2 ℤ ∣ Pnq.maskW w ∧
    Pnq.levelsEW (p := 3) (q := 2) (n := 3) w = ∅ ∧ Pnq.levelsFW (p := 3) (q := 2) (n := 3) w = {1}} 5 := by
  have : Fact (Nat.Prime 3) := ⟨by norm_num⟩
  have : Fact (Nat.Prime 2) := ⟨by norm_num⟩
  have h := Pnq.minsize_unbalanced_zmod 3 2 3 (by norm_num) ∅ {1} (by simp) (by simp)
  have hv : Pnq.minU 3 2 ∅ {1} = 5 := by decide
  rw [hv] at h
  exact h

end Read3a

#print axioms Read3a.cover
#print axioms Read3a.empty_pattern
#print axioms Read3a.first_not_empty
#print axioms Read3a.third_not_empty
#print axioms Read3a.item2_from_bridge
#print axioms Read3a.item2_from_first
