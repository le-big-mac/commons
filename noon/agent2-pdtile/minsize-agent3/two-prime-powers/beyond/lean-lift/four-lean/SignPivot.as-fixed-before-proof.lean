/-
The statement on signs for every odd `n`: pivot sets and ranks.  The number of occupied classes modulo `p^j` is at least
`(p - 1) rank + 1`; a live level has a pivot set with `(p - 1) rank` elements (S2 (b)); so a live level `i` of `p` costs a
factor `2^((p-1) rank)` (S2); and ranks are small (S3).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignCount

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-- **The number of occupied classes** (the plan's `N_j ≥ 1 + (p - 1) rank p j`, in S2 (b) and S3).  For a nonempty
`ι` and a prime `p`, the number of classes modulo `p^j` that are occupied is at least `(p - 1) * rank e p j + 1`. -/
theorem rank_lt_card_image [Nonempty ι] (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (j : ℕ) :
    (p - 1) * rank e p j + 1 ≤ (Finset.univ.image fun k => e k % p ^ j).card := by
  sorry

/-- **S2 (b) (a large pivot set).**  `p` prime, `i ≥ 1`.  If the level `i` of `p` is live, there is a pivot set for
that level with at least `(p - 1) * rank e p i` elements. -/
theorem exists_isPivot (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i)
    (hlive : live e p i = true) :
    ∃ J : Finset ι, IsPivot e p i J ∧ (p - 1) * rank e p i ≤ J.card := by
  sorry

/-- **S2 (what a live level costs).**  `p` prime, `i ≥ 1`, `p ∤ d`, the level `i` of `p` live.  Then
`#{ε bad at p^i * d} * 2^((p - 1) * rank e p i) ≤ 2^m`. -/
theorem card_badSet_mul_two_pow_rank_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i) {d : ℕ}
    (hd : ¬ p ∣ d) (hlive : live e p i = true) :
    (badSet e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i) ≤ 2 ^ Fintype.card ι := by
  sorry

/-- **S3 (ranks are small).**  For a nonempty `ι`, every prime `p` and every `i`: `(p - 1) * rank e p i + 1 ≤ m`. -/
theorem rank_lt_card [Nonempty ι] (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (i : ℕ) :
    (p - 1) * rank e p i + 1 ≤ Fintype.card ι := by
  sorry

end Pnq
