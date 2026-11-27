/-
"Twice" for several systems of values at once (Theorem U of the note of the evening of 27 November 2026).
`ι` a finite type, each `k : ι` with a position `pos k : ℕ`; `κ` any type of indices, and for each `c : κ` a system of
values `val c : ι → V` in an additive commutative group `V` (any group, any values, `0` allowed).  The positions are
the same for every `c`.  The signings for which some level `0, …, K` is bad for the values of SOME `c` number at most
twice those for which level `0` is bad for the values of some `c`.
For a single `c` this is `card_exists_levelBad_le` of `Pnq/EvenTwice.lean`.
(Statement fixed before any Lean proof of it.)
-/
import Pnq.EvenTwice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι] {V : Type*} [AddCommGroup V]

open Classical in
/-- **U (several systems of values).**  For every `K`, the number of signings `ε` such that level `j` is bad for the
values `val c`, for some index `c` and some `j ≤ K`, is at most twice the number of signings such that level `0` is
bad for the values `val c` for some index `c`. -/
theorem card_exists_exists_levelBad_le {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ c, ∃ j, j ≤ K ∧ levelBad pos (val c) ε j).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => ∃ c, levelBad pos (val c) ε 0).card := by
  sorry

end Pnq
