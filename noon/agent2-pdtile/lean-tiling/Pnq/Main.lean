/-
Weak tiling implies tiling in `ZMod (p^n * q)`, for primes `p ≠ q` and every `n`: the assembly.

* `exists_stepTiling_tree` (agent2, `StepOf.lean`): a weak complement gives a step complement on the tree of `A`
  (Galois, averaging over the units, and an induction along the tree);
* `step_structure` (agent3, `Step.lean` and `Tree.lean`): a step complement on a tree forces (T1) and (T2) on
  the tree (the three bounds from the step identity, then Lemmas 3 and 4 of `pnq-agent3.md`);
* `tiling_of_tree_T1_T2` (agent2, `Final.lean`): (T1) and (T2) on the tree give a tiling complement, through
  the bridge of `Group.lean` (the level conditions of the tree are the cyclotomic conditions) and the
  Coven–Meyerowitz theorem of `Pqr/CM.lean`.
-/
import Pnq.Final
import Pnq.StepOf
import Pnq.Step
import Pqr.Cyclic

open Finset

namespace Pnq

/-- **Weak tiling implies tiling in `Z_{pⁿq}`.** If `A ⊆ ZMod (p^n * q)` has a weak tiling complement
(`f ≥ 0`, `f 0 = 1`, `∑ a ∈ A, f (v - a) = 1` for all `v`), then `A ⊕ B = ZMod (p^n * q)` for some `B`. -/
theorem weak_tiling_tiles_pnq (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ n * q))) (f : ZMod (p ^ n * q) → ℝ) (h : Pqr.WeakTiling A f) :
    ∃ B : Finset (ZMod (p ^ n * q)), Pqr.IsTiling A B := by
  obtain ⟨γ, hγ⟩ := exists_stepTiling_tree hpq A f h
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hc := step_structure hp.two_le hq.two_le ((Nat.coprime_primes hp hq).mpr hpq) (treeOf A) γ hγ
  exact tiling_of_tree_T1_T2 hpq A hc.1 hc.2

/-- **Tiles and weak tiles of `Z_{pⁿq}` are the same sets.** -/
theorem weak_tiling_iff_tiling_pnq (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ n * q))) :
    (∃ f : ZMod (p ^ n * q) → ℝ, Pqr.WeakTiling A f) ↔
      ∃ B : Finset (ZMod (p ^ n * q)), Pqr.IsTiling A B :=
  ⟨fun ⟨f, hf⟩ => weak_tiling_tiles_pnq p q n hpq A f hf, fun ⟨_, hB⟩ => hB.weakTiling⟩

end Pnq
