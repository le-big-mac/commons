/-
The statement on signs for every odd `n`: the sum N1.  It is about `μ` only: the sum of `(1/2)^(μ t)` over a set of
odd numbers `t > 1` with `μ t ≤ m - 1`, together with the share `m.choose (m/2) / 2^m` of the signings bad at `1`, is
below `1`.  In the rational numbers.
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignDefs

open Finset

namespace Pnq

/-- **N1 (the sum).**  For `m ≥ 1` and every finite set `T` of odd numbers `t > 1` with `μ t ≤ m - 1`: if `m` is odd,
`∑_{t ∈ T} (1/2)^(μ t) < 1`; if `m` is even,
`m.choose (m/2) / 2^m + ∑_{t ∈ T} (1/2)^(μ t) - (if 3 ∈ T ∧ 14 ≤ m then 1/16 else 0) < 1`.
(`lhsN1 m T` is the left side in both cases.) -/
theorem lhsN1_lt_one (m : ℕ) (hm : 1 ≤ m) (T : Finset ℕ)
    (hT : ∀ t ∈ T, ¬ 2 ∣ t ∧ 1 < t ∧ μ t + 1 ≤ m) : lhsN1 m T < 1 := by
  sorry

end Pnq
