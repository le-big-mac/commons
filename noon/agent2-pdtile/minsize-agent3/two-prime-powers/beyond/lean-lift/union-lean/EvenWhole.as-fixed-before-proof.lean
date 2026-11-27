/-
"Twice" for the whole of `Z_n` (Corollary U of the note of the evening of 27 November 2026).
`n'` odd, `k` any natural number, `n = 2^k * n'`.  For elements with exponents `e : ι → ℕ`, the signings whose signed
mask `P e ε = ∑ ± X^(e i)` is divisible by the cyclotomic polynomial `Φ_d` for SOME divisor `d` of `2^k * n'` number
at most twice those whose signed mask is divisible by `Φ_d` for some divisor `d` of `n'`.
(Statement fixed before any Lean proof of it.)
-/
import Pnq.EvenUnion
import Pnq.SignSlice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

open Classical in
/-- **Corollary U (the whole of `Z_n`).**  `n'` odd (so `n' ≥ 1`).  The number of signings that are bad at some
divisor of `2^k * n'` is at most twice the number of signings that are bad at some divisor of `n'`. -/
theorem card_exists_badAt_le (e : ι → ℕ) (k : ℕ) {n' : ℕ} (hn' : ¬ 2 ∣ n') :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k * n' ∧ BadAt e ε d).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ n' ∧ BadAt e ε d).card := by
  sorry

end Pnq
