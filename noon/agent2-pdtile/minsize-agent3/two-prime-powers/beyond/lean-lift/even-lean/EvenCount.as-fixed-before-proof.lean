/-
The statement on signs for every `n`: the counts modulo 3.  S2′ (a pivot set `J` for the level `i` of a prime `p ≠ 3`
bounds the number of signings 3-bad at `p^i d` by `2^(m - |J|)`; a live level `i` of `p` costs a factor
`2^((p-1) rank)`) and E1 (the signings 3-bad at `1`: the sum of the signs is divisible by 3; their number is
`(2^m + 2)/3` for even `m` and `(2^m - 2)/3` for odd `m`).
The numbers of signings are cardinalities of the finite sets `bad3Set e d`; `m` is `Fintype.card ι`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenSlice
import Pnq.SignPivot

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-- **S2′, with a pivot set.**  `p` prime, `p ≠ 3` (`p = 2` allowed), `i ≥ 1`, `p ∤ d`, `3 ∤ d`.  If `J` is a pivot set
for the level `i` of `p`, the number of signings 3-bad at `p^i * d` is at most `2^(m - |J|)`. -/
theorem card_bad3Set_mul_two_pow_card_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) {J : Finset ι} (hJ : IsPivot e p i J) :
    (bad3Set e (p ^ i * d)).card * 2 ^ J.card ≤ 2 ^ Fintype.card ι := by
  sorry

/-- **S2′, with the rank (what a live level costs modulo 3).**  `p` prime, `p ≠ 3`, `i ≥ 1`, `p ∤ d`, `3 ∤ d`, the
level `i` of `p` live.  Then `#{ε 3-bad at p^i * d} * 2^((p - 1) * rank e p i) ≤ 2^m`. -/
theorem card_bad3Set_mul_two_pow_rank_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) (hlive : live e p i = true) :
    (bad3Set e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i) ≤ 2 ^ Fintype.card ι := by
  sorry

/-- **E1, first half.**  A signing is 3-bad at `1` exactly when the integer sum of its signs is divisible by 3. -/
theorem bad3_one_iff (e : ι → ℕ) (ε : ι → Bool) : Bad3 e ε 1 ↔ (3 : ℤ) ∣ ∑ k, sg (ε k) := by
  sorry

/-- **E1, second half.**  Three times the number of signings 3-bad at `1` is `2^m + 2` if `m` is even and `2^m - 2`
if `m` is odd (written without subtraction). -/
theorem card_bad3Set_one (e : ι → ℕ) :
    3 * (bad3Set e 1).card + (if Even (Fintype.card ι) then 0 else 2) =
      2 ^ Fintype.card ι + (if Even (Fintype.card ι) then 2 else 0) := by
  sorry

end Pnq
