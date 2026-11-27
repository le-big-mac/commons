/-
The statement on signs for every odd `n`: S5, the first live level of the prime `3`, counted more exactly.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignPivot

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-- **S5 (the first live level of the prime 3).**  If `m ≥ 7`, the level `i` of the prime `3` is live and
`rank e 3 i = 1`, then `#{ε bad at 3^i} * 16 ≤ 3 * 2^m`. -/
theorem card_badSet_three_pow_mul_le (e : ι → ℕ) (hm : 7 ≤ Fintype.card ι) {i : ℕ}
    (hlive : live e 3 i = true) (hrank : rank e 3 i = 1) :
    (badSet e (3 ^ i)).card * 16 ≤ 3 * 2 ^ Fintype.card ι := by
  sorry

end Pnq
