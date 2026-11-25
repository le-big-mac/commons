/-
Step weak tiling complements on the tree (definitions proposed by agent3 on the board, 09:16 UTC; transcribed
by agent2 so that both sides can be proved against one text).

`γ d b` is the value of the complement at a difference that vanishes in exactly the lowest `d` base-`p` digits
(`d = n`: in all of them) and whose layer coordinate is zero (`b = true`) or not (`b = false`).
-/
import Pnq.Tree

open Finset

namespace Pnq

variable {p q : ℕ}

/-- The tiling identity, by recursion on the tree.  `d` is the depth of the current node and `ext w` is the
contribution of the elements outside the current subtree to the sum at a point of layer `w` inside it. -/
def Tiles (γ : ℕ → Bool → ℝ) : {k : ℕ} → ℕ → Tree p q k → (Fin q → ℝ) → Prop
  | _, d, .leaf f, ext =>
      ∀ w, ext w + γ d true * (f w : ℝ) + γ d false * ((∑ j, (f j : ℝ)) - f w) = 1
  | _, d, .node ch, ext =>
      ∀ c, Tiles γ (d + 1) (ch c)
        (fun w => ext w + ∑ c' ∈ univ.erase c,
          (γ d true * (lay (ch c') w : ℝ) + γ d false * ((size (ch c') : ℝ) - lay (ch c') w)))

/-- `γ` is a step weak tiling complement of the set stored in the tree `t` of depth `n`. -/
def StepTiling (γ : ℕ → Bool → ℝ) {n : ℕ} (t : Tree p q n) : Prop :=
  (∀ d b, 0 ≤ γ d b) ∧ γ n true = 1 ∧ Tiles γ 0 t (fun _ => 0)

end Pnq
