/-
The statement on signs for every odd `n`: two counts.  S2 (a): a pivot set `J` for the level `i` of `p` bounds the number
of signings bad at `p^i d` by `2^(m - |J|)`.  S4: the signings bad at `1`.
The numbers of signings are cardinalities of the finite sets `badSet e d`; `m` is `Fintype.card ι`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignSlice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-- **S2 (a) (pivots).**  `p` prime, `i ≥ 1`, `p ∤ d`.  If `J` is a pivot set for the level `i` of `p`, the number of
signings bad at `p^i * d` is at most `2^(m - |J|)`: two such signings that agree outside `J` are equal. -/
theorem card_badSet_mul_two_pow_card_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i) {d : ℕ}
    (hd : ¬ p ∣ d) {J : Finset ι} (hJ : IsPivot e p i J) :
    (badSet e (p ^ i * d)).card * 2 ^ J.card ≤ 2 ^ Fintype.card ι := by
  sorry

/-- **S4, first half.**  A signing is bad at `1` exactly when its signs add up to `0`. -/
theorem badAt_one_iff (e : ι → ℕ) (ε : ι → Bool) : BadAt e ε 1 ↔ ∑ k, sg (ε k) = 0 := by
  sorry

/-- **S4, second half.**  The number of signings bad at `1` is `m.choose (m / 2)` if `m` is even and `0` if `m` is
odd. -/
theorem card_badSet_one (e : ι → ℕ) :
    (badSet e 1).card =
      if Even (Fintype.card ι) then (Fintype.card ι).choose (Fintype.card ι / 2) else 0 := by
  sorry

end Pnq
