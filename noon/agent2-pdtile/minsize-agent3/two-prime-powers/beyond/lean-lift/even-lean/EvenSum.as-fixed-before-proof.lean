/-
The statement on signs for every `n`: the sum N1′, the sum N1 of `Pnq/SignSum.lean` without the prime 3.  It is about
`μ` only: the sum of `(1/2)^(μ t)` over a finite set of numbers `t > 1` prime to 6 is below `1/8`.  In the rational
numbers.  (The value of the sum over all such `t` is `0.11856…`.)
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignSum

open Finset

namespace Pnq

/-- **N1′ (the sum without the prime 3).**  For every finite set `T` of numbers `t > 1` divisible neither by 2 nor
by 3: `∑_{t ∈ T} (1/2)^(μ t) < 1/8`. -/
theorem sum_half_pow_mu_lt (T : Finset ℕ) (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ ¬ 3 ∣ t ∧ 1 < t) :
    ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t < 1 / 8 := by
  sorry

end Pnq
