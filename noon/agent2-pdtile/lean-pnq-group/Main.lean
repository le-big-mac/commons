/-
Weak tiling implies tiling in `ZMod (p^n * q)`: the assembly.

* `exists_stepTiling_tree` (agent2, `StepOf.lean`): a weak complement gives a step complement on the tree of `A`;
* the three bounds from a step complement on the tree (agent3) — here a hypothesis until that file exists;
* `counting` (agent3, `Tree.lean`): the bounds give (T1) and (T2) on the tree;
* `tiling_of_tree_T1_T2` (agent2, `Final.lean`): (T1) and (T2) on the tree give a tiling complement, through the
  bridge of `Group.lean` and the Coven–Meyerowitz theorem of `Pqr/CM.lean`.
-/
import Pnq.Final
import Pnq.StepOf

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

/-- the three upper bounds that `Pnq.counting` takes as hypotheses -/
def ThreeBounds {n : ℕ} (t : Tree p q n) : Prop :=
  (size t ≤ p ^ e t * q) ∧
  (¬ F t 0 → (∀ ℓ, F t (ℓ + 1) → E t (ℓ + 1)) → size t ≤ p ^ e t) ∧
  (F t 0 → ∀ a, E t (a + 1) → ¬ F t (a + 1) →
    (∀ ℓ, a < ℓ → (E t (ℓ + 1) ↔ F t (ℓ + 1))) → size t * min p q ≤ p ^ e t * q)

/-- Weak tiling implies tiling in `ZMod (p^n * q)`, **given** that a step complement on a tree implies the
three bounds. -/
theorem weak_tiling_tiles_pnq_of_bounds (hpq : p ≠ q)
    (hb : ∀ (t : Tree p q n) (γ : ℕ → Bool → ℝ), 0 < size t → StepTiling γ t → ThreeBounds t)
    (A : Finset (ZMod (p ^ n * q))) (f : ZMod (p ^ n * q) → ℝ) (h : Pqr.WeakTiling A f) :
    ∃ B : Finset (ZMod (p ^ n * q)), Pqr.IsTiling A B := by
  obtain ⟨γ, hγ⟩ := exists_stepTiling_tree hpq A f h
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hpos : 0 < size (treeOf A) := by
    rw [size_treeOf]
    exact Finset.card_pos.mpr (Pqr.nonempty_of_weakTiling A f h)
  obtain ⟨U1, U2, L2⟩ := hb (treeOf A) γ hpos hγ
  have hc := counting hp.two_le hq.two_le ((Nat.coprime_primes hp hq).mpr hpq) (treeOf A) hpos U1 U2 L2
  exact tiling_of_tree_T1_T2 hpq A hc.1 hc.2

end Pnq
