/-
Assembly: weak tiling implies tiling in `ZMod p × ZMod q × ZMod r`.
-/
import Pqr.Defs
import Pqr.Comb
import Pqr.Step
import Pqr.Fourier

open Finset

set_option linter.unusedSectionVars false

namespace Pqr

/-- `A ⊕ B = G` -/
def IsTiling {G : Type*} [AddCommGroup G] (A B : Finset G) : Prop :=
  ∀ v : G, ∃! ab : G × G, ab.1 ∈ A ∧ ab.2 ∈ B ∧ ab.1 + ab.2 = v

/-- If a homomorphism restricted to `A` is a bijection onto its codomain, then `A` and the kernel tile. -/
theorem tile_of_transversal {G Q : Type*} [AddCommGroup G] [AddCommGroup Q] [Fintype G]
    [DecidableEq Q] (π : G →+ Q) (A : Finset G) (h : ∀ c : Q, ∃! a, a ∈ A ∧ π a = c) :
    ∃ B : Finset G, IsTiling A B := by
  refine ⟨univ.filter (fun b => π b = 0), fun v => ?_⟩
  obtain ⟨a, ⟨haA, hav⟩, hau⟩ := h (π v)
  refine ⟨(a, v - a), ⟨haA, by simp [hav], by simp⟩, ?_⟩
  rintro ⟨a', b'⟩ ⟨ha', hb', hab⟩
  simp only [mem_filter, mem_univ, true_and] at hb'
  have h1 : π a' = π v := by rw [← hab]; simp [hb']
  have h2 : a' = a := hau a' ⟨ha', h1⟩
  subst h2
  have : b' = v - a' := by rw [← hab]; abel
  simp [this]

/-- zero/one integers that sum to one: exactly one of them is one -/
theorem existsUnique_of_sum_one {ι : Type*} [Fintype ι] [DecidableEq ι] (g : ι → ℤ)
    (h01 : ∀ x, g x = 0 ∨ g x = 1) (h : ∑ x, g x = 1) : ∃! x, g x = 1 := by
  have hnn : ∀ x, 0 ≤ g x := fun x => by rcases h01 x with h | h <;> simp [h]
  have hex : ∃ x, g x = 1 := by
    by_contra hcon
    push Not at hcon
    have : ∑ x, g x = 0 := Finset.sum_eq_zero (fun x _ => (h01 x).resolve_right (hcon x))
    omega
  obtain ⟨x, hx⟩ := hex
  refine ⟨x, hx, fun y hy => ?_⟩
  by_contra hne
  have h1 : g x + g y ≤ ∑ z, g z := by
    rw [← Finset.add_sum_erase univ g (mem_univ x)]
    have : g y ≤ ∑ z ∈ univ.erase x, g z :=
      Finset.single_le_sum (f := g) (fun z _ => hnn z) (Finset.mem_erase.mpr ⟨hne, mem_univ y⟩)
    linarith
  omega

section main

variable (p q r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime]

theorem ind_zero_one (A : Finset (ZMod p × ZMod q × ZMod r)) (i : ZMod p) (j : ZMod q)
    (k : ZMod r) : ind p q r A i j k = 0 ∨ ind p q r A i j k = 1 := by
  unfold ind; split_ifs <;> simp

theorem ind_eq_one_iff (A : Finset (ZMod p × ZMod q × ZMod r)) (i : ZMod p) (j : ZMod q)
    (k : ZMod r) : ind p q r A i j k = 1 ↔ (i, j, k) ∈ A := by
  unfold ind; split_ifs with h <;> simp [h]

/-- **Weak tiling implies tiling in `Z_p × Z_q × Z_r`**, for distinct primes `p`, `q`, `r`:
if `A` has a weak tiling complement (`f ≥ 0`, `f 0 = 1`, `∑ a ∈ A, f (v - a) = 1` for all `v`),
then `A ⊕ B` is the whole group for some set `B`. -/
theorem weak_tiling_tiles (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (A : Finset (ZMod p × ZMod q × ZMod r)) (f : ZMod p × ZMod q × ZMod r → ℝ)
    (h : WeakTiling A f) : ∃ B : Finset (ZMod p × ZMod q × ZMod r), IsTiling A B := by
  obtain ⟨γ, hγ⟩ := exists_stepTiling p q r hpq hpr hqr A f h
  have hB : Bounds (ind p q r A) := bounds_of_stepTiling _ γ hγ
  have h01 := ind_zero_one p q r A
  have hmem := ind_eq_one_iff p q r A
  have hne : A.Nonempty := by
    by_contra hE
    rw [Finset.not_nonempty_iff_eq_empty] at hE
    have := h.2.2 0
    rw [hE] at this
    simp at this
  have hpos : 0 < total (ind p q r A) := by
    obtain ⟨⟨i, j, k⟩, hv⟩ := hne
    have h1 : ind p q r A i j k ≤ N2 (ind p q r A) i j :=
      Finset.single_le_sum (f := fun k' => ind p q r A i j k')
        (fun k' _ => a_nonneg _ h01 i j k') (mem_univ k)
    have h2 : N2 (ind p q r A) i j ≤ N1 (ind p q r A) i :=
      Finset.single_le_sum (f := fun j' => N2 (ind p q r A) i j')
        (fun j' _ => N2_nonneg _ h01 i j') (mem_univ j)
    have h3 : N1 (ind p q r A) i ≤ total (ind p q r A) :=
      Finset.single_le_sum (f := fun i' => N1 (ind p q r A) i')
        (fun i' _ => N1_nonneg _ h01 i') (mem_univ i)
    have h4 : ind p q r A i j k = 1 := (hmem i j k).mpr hv
    linarith
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hr : r.Prime := Fact.out
  have hS : Structured (ind p q r A) :=
    structured_of_bounds (ind p q r A) h01 hpos
      (by rw [ZMod.card]; exact hp.two_le) (by rw [ZMod.card]; exact hq.two_le)
      (by rw [ZMod.card]; exact hr.two_le)
      (by rw [ZMod.card, ZMod.card]; exact (Nat.coprime_primes hp hq).mpr hpq)
      (by rw [ZMod.card, ZMod.card]; exact (Nat.coprime_primes hp hr).mpr hpr)
      (by rw [ZMod.card, ZMod.card]; exact (Nat.coprime_primes hq hr).mpr hqr) hB
  rcases hS with h0 | hx | hy | hz | hxy | hxz | hyz | hall
  · -- one point: the complement is everything
    apply tile_of_transversal (0 : ZMod p × ZMod q × ZMod r →+ Unit) A
    intro c
    have hsum : ∑ v : ZMod p × ZMod q × ZMod r, ind p q r A v.1 v.2.1 v.2.2 = 1 := by
      rw [Fintype.sum_prod_type]
      simp only [Fintype.sum_prod_type]
      exact h0
    obtain ⟨v, hv, hu⟩ := existsUnique_of_sum_one _ (fun v => h01 v.1 v.2.1 v.2.2) hsum
    refine ⟨v, ⟨(hmem _ _ _).mp hv, rfl⟩, fun w hw => hu w ((hmem _ _ _).mpr hw.1)⟩
  · -- one point in each class of the first coordinate
    apply tile_of_transversal (AddMonoidHom.fst (ZMod p) (ZMod q × ZMod r)) A
    intro i
    have hsum : ∑ w : ZMod q × ZMod r, ind p q r A i w.1 w.2 = 1 := by
      rw [Fintype.sum_prod_type]; exact hx i
    obtain ⟨w, hw, hu⟩ := existsUnique_of_sum_one _ (fun w => h01 i w.1 w.2) hsum
    refine ⟨(i, w), ⟨(hmem _ _ _).mp hw, rfl⟩, ?_⟩
    rintro ⟨i', w'⟩ ⟨hmemA, hi⟩
    simp only [AddMonoidHom.coe_fst] at hi
    subst hi
    rw [hu w' ((hmem _ _ _).mpr hmemA)]
  · -- one point in each class of the second coordinate
    apply tile_of_transversal ((AddMonoidHom.fst (ZMod q) (ZMod r)).comp
      (AddMonoidHom.snd (ZMod p) (ZMod q × ZMod r))) A
    intro j
    have hsum : ∑ w : ZMod p × ZMod r, ind p q r A w.1 j w.2 = 1 := by
      rw [Fintype.sum_prod_type]; exact hy j
    obtain ⟨w, hw, hu⟩ := existsUnique_of_sum_one _ (fun w => h01 w.1 j w.2) hsum
    refine ⟨(w.1, j, w.2), ⟨(hmem _ _ _).mp hw, rfl⟩, ?_⟩
    rintro ⟨i', j', k'⟩ ⟨hmemA, hj⟩
    simp only [AddMonoidHom.coe_comp, AddMonoidHom.coe_fst, AddMonoidHom.coe_snd,
      Function.comp_apply] at hj
    subst hj
    have := hu (i', k') ((hmem _ _ _).mpr hmemA)
    rw [← this]
  · -- one point in each class of the third coordinate
    apply tile_of_transversal ((AddMonoidHom.snd (ZMod q) (ZMod r)).comp
      (AddMonoidHom.snd (ZMod p) (ZMod q × ZMod r))) A
    intro k
    have hsum : ∑ w : ZMod p × ZMod q, ind p q r A w.1 w.2 k = 1 := by
      rw [Fintype.sum_prod_type]; exact hz k
    obtain ⟨w, hw, hu⟩ := existsUnique_of_sum_one _ (fun w => h01 w.1 w.2 k) hsum
    refine ⟨(w.1, w.2, k), ⟨(hmem _ _ _).mp hw, rfl⟩, ?_⟩
    rintro ⟨i', j', k'⟩ ⟨hmemA, hk⟩
    simp only [AddMonoidHom.coe_comp, AddMonoidHom.coe_snd, Function.comp_apply] at hk
    subst hk
    have := hu (i', j') ((hmem _ _ _).mpr hmemA)
    rw [← this]
  · -- one point for each value of the first two coordinates
    apply tile_of_transversal ((AddMonoidHom.fst (ZMod p) (ZMod q × ZMod r)).prod
      ((AddMonoidHom.fst (ZMod q) (ZMod r)).comp (AddMonoidHom.snd (ZMod p) (ZMod q × ZMod r)))) A
    rintro ⟨i, j⟩
    obtain ⟨k, hk, hu⟩ := existsUnique_of_sum_one _ (fun k => h01 i j k) (hxy i j)
    refine ⟨(i, j, k), ⟨(hmem _ _ _).mp hk, rfl⟩, ?_⟩
    rintro ⟨i', j', k'⟩ ⟨hmemA, hij⟩
    simp only [AddMonoidHom.prod_apply, AddMonoidHom.coe_comp, AddMonoidHom.coe_fst,
      AddMonoidHom.coe_snd, Function.comp_apply, Prod.mk.injEq] at hij
    obtain ⟨rfl, rfl⟩ := hij
    rw [hu k' ((hmem _ _ _).mpr hmemA)]
  · -- one point for each value of the first and third coordinates
    apply tile_of_transversal ((AddMonoidHom.fst (ZMod p) (ZMod q × ZMod r)).prod
      ((AddMonoidHom.snd (ZMod q) (ZMod r)).comp (AddMonoidHom.snd (ZMod p) (ZMod q × ZMod r)))) A
    rintro ⟨i, k⟩
    obtain ⟨j, hj, hu⟩ := existsUnique_of_sum_one _ (fun j => h01 i j k) (hxz i k)
    refine ⟨(i, j, k), ⟨(hmem _ _ _).mp hj, rfl⟩, ?_⟩
    rintro ⟨i', j', k'⟩ ⟨hmemA, hik⟩
    simp only [AddMonoidHom.prod_apply, AddMonoidHom.coe_comp, AddMonoidHom.coe_fst,
      AddMonoidHom.coe_snd, Function.comp_apply, Prod.mk.injEq] at hik
    obtain ⟨rfl, rfl⟩ := hik
    rw [hu j' ((hmem _ _ _).mpr hmemA)]
  · -- one point for each value of the last two coordinates
    apply tile_of_transversal (AddMonoidHom.snd (ZMod p) (ZMod q × ZMod r)) A
    rintro ⟨j, k⟩
    obtain ⟨i, hi, hu⟩ := existsUnique_of_sum_one _ (fun i => h01 i j k) (hyz j k)
    refine ⟨(i, j, k), ⟨(hmem _ _ _).mp hi, rfl⟩, ?_⟩
    rintro ⟨i', j', k'⟩ ⟨hmemA, hjk⟩
    simp only [AddMonoidHom.coe_snd, Prod.mk.injEq] at hjk
    obtain ⟨rfl, rfl⟩ := hjk
    rw [hu i' ((hmem _ _ _).mpr hmemA)]
  · -- everything: the complement is a point
    apply tile_of_transversal (AddMonoidHom.id (ZMod p × ZMod q × ZMod r)) A
    rintro ⟨i, j, k⟩
    exact ⟨(i, j, k), ⟨(hmem _ _ _).mp (hall i j k), rfl⟩, fun w hw => hw.2⟩

end main

end Pqr
