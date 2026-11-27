/-
The statement on signs for every odd `n`: A1, the theorem in elements.  For an odd `n` and a nonempty finite family of
exponents there is a signing that is bad at no `d ∣ n`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignSlice
import Pnq.SignCount
import Pnq.SignPivot
import Pnq.SignThree
import Pnq.SignSum

open Finset

namespace Pnq

/-- **A1 (the theorem, in elements).**  `n` odd, `ι` finite and nonempty, `e : ι → ℕ` any exponents.  There is a
signing `ε` that is bad at no divisor `d` of `n`: no `Φ_d`, `d ∣ n`, divides `∑ k, sg (ε k) X ^ e k`. -/
theorem exists_not_badAt (n : ℕ) (hn : ¬ 2 ∣ n) {ι : Type*} [Fintype ι] [Nonempty ι] (e : ι → ℕ) :
    ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ BadAt e ε d := by
  sorry

end Pnq
