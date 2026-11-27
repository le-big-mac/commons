/-
The statement on signs for every `n`: the assembly.  A′ (for `n` prime to 3 and a family of at least three exponents
there is a signing that is 3-bad at no `d ∣ n`) and B (for every `n ≠ 0` and a family of at least three exponents
there is a signing that is bad at no `d ∣ n`).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenCount
import Pnq.EvenLadder
import Pnq.EvenSum
import Pnq.SignAll

open Finset

namespace Pnq

/-- **A′ (assembly, in elements, modulo 3).**  `3 ∤ n` (so `n ≥ 1`), `ι` finite with at least three points,
`e : ι → ℕ` any exponents.  There is a signing `ε` that is 3-bad at no divisor `d` of `n`. -/
theorem exists_not_bad3 (n : ℕ) (hn : ¬ 3 ∣ n) {ι : Type*} [Fintype ι] (hm : 3 ≤ Fintype.card ι)
    (e : ι → ℕ) : ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ Bad3 e ε d := by
  sorry

/-- **B (back to `ℤ`).**  `n ≠ 0`, `ι` finite with at least three points, `e : ι → ℕ` any exponents.  There is a
signing `ε` that is bad at no divisor `d` of `n`: no `Φ_d`, `d ∣ n`, divides `∑ k, sg (ε k) X ^ e k`. -/
theorem exists_not_badAt_of_three_le (n : ℕ) (hn : n ≠ 0) {ι : Type*} [Fintype ι]
    (hm : 3 ≤ Fintype.card ι) (e : ι → ℕ) : ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ BadAt e ε d := by
  sorry

end Pnq
