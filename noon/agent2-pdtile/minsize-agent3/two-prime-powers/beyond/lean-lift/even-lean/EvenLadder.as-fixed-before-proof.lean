/-
The statement on signs for every `n`: part L, the ladder of the prime 2 modulo 3.  For `d` prime to 6, the signings
that are 3-bad at `2^j d` for some `j ≤ K` number at most twice those 3-bad at `d`.  From S0′ with `p = 2`
(`classSum3_eq_of_bad3` of `Pnq/EvenSlice.lean`) and T (`card_exists_levelBad_le` of `Pnq/EvenTwice.lean`), with `V`
the functions from the primitive `d`-th roots of unity of `F3` to `F3`, `pos = e` and `val k = fun η => η ^ e k`.
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.EvenSlice
import Pnq.EvenTwice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

open Classical in
/-- **L (the ladder, modulo 3).**  `d` odd (so `d ≥ 1`), `3 ∤ d`.  For every `K`, the number of signings that are
3-bad at `2^j * d` for some `j ≤ K` is at most twice the number of signings 3-bad at `d`. -/
theorem card_exists_bad3_le (e : ι → ℕ) {d : ℕ} (hd : ¬ 2 ∣ d) (h3 : ¬ 3 ∣ d) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ Bad3 e ε (2 ^ j * d)).card ≤
      2 * (bad3Set e d).card := by
  sorry

end Pnq
