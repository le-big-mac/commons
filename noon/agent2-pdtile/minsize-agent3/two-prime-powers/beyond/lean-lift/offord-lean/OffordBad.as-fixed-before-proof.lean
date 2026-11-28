/-
The first statements about SHARES of bad signings: at one divisor, on moduli that are powers of 2, and on every
modulus with the number of divisors of its odd part.  (Statements fixed on 28 November 2026, before any Lean proof of
them.  `P`, `BadAt` are from `Pnq/SignDefs.lean`; "twice" for the whole of `Z_n` is `card_exists_badAt_le` of
`Pnq/EvenWhole.lean`; Erdős's bound is in `Pnq/Offord.lean`.)
-/
import Mathlib
import Pnq.Offord
import Pnq.EvenWhole

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

open Classical in
/-- **One divisor.**  For `d ≠ 0`, the signings that are bad at `d` number at most `C(m, ⌊m/2⌋)`, where `m` is the
number of elements. -/
theorem card_badAt_le_choose (e : ι → ℕ) {d : ℕ} (hd : d ≠ 0) :
    (Finset.univ.filter fun ε : ι → Bool => BadAt e ε d).card ≤
      (Fintype.card ι).choose (Fintype.card ι / 2) := by
  sorry

/-- **An odd number of elements is never bad at 1.** -/
theorem not_badAt_one_of_odd (e : ι → ℕ) (hm : Odd (Fintype.card ι)) (ε : ι → Bool) :
    ¬ BadAt e ε 1 := by
  sorry

open Classical in
/-- **Moduli that are powers of 2.**  The signings that are bad at some divisor of `2^k` number at most
`2 * C(m, ⌊m/2⌋)`. -/
theorem card_exists_badAt_two_pow_le (e : ι → ℕ) (k : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d).card ≤
      2 * (Fintype.card ι).choose (Fintype.card ι / 2) := by
  sorry

/-- **Moduli that are powers of 2, an odd number of elements: every signing is good.** -/
theorem not_exists_badAt_two_pow_of_odd (e : ι → ℕ) (k : ℕ) (hm : Odd (Fintype.card ι)) (ε : ι → Bool) :
    ¬ ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d := by
  sorry

open Classical in
/-- **Every modulus, with the number of divisors of its odd part.**  `n'` odd.  The signings that are bad at some
divisor of `2^k * n'` number at most `2 * (d(n') * C(m, ⌊m/2⌋))`, where `d(n')` is the number of divisors of `n'`. -/
theorem card_exists_badAt_le_divisors (e : ι → ℕ) (k : ℕ) {n' : ℕ} (hn' : ¬ 2 ∣ n') :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k * n' ∧ BadAt e ε d).card ≤
      2 * (n'.divisors.card * (Fintype.card ι).choose (Fintype.card ι / 2)) := by
  sorry

end Pnq
