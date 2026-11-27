/-
The statement on signs for every `n`: the slices modulo 3.  M (a signing that is bad at `3^i d`, `3 ∤ d`, is 3-bad at
`d`), S0′ (a signing that is 3-bad at `p^i d`, `p ≠ 3`, has equal sums in `F3` on the `p` classes of every group at
level `i` of `p`) and S1′ (step-down: if moreover the level `i` of `p` is not live, the signing is 3-bad at
`p^(i-1) d`).  S0′ and S1′ are S0 and S1 of `Pnq/SignSlice.lean` with `F3` for `ℂ` and `Bad3` for `BadAt`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenDefs
import Pnq.SignSlice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-- **M (reduce modulo 3).**  `3 ∤ d` (so `d ≥ 1`), `i` any exponent (`i = 0` allowed).  If the signing `ε` is bad at
`3^i * d` (`Φ_(3^i d)` divides the signed mask over `ℤ`), then `ε` is 3-bad at `d`. -/
theorem bad3_of_badAt (e : ι → ℕ) (ε : ι → Bool) (i : ℕ) {d : ℕ} (h3 : ¬ 3 ∣ d)
    (hbad : BadAt e ε (3 ^ i * d)) : Bad3 e ε d := by
  sorry

/-- **S0′ (flatness modulo 3).**  `p` prime, `p ≠ 3` (`p = 2` allowed), `i ≥ 1`, `p ∤ d` (so `d ≥ 1`), `3 ∤ d`, `η ∈ F3`
a root of unity of order `d`.  If the signing `ε` is 3-bad at `p^i * d`, then in every group at level `i` (the `p`
classes `c % p^(i-1) + t p^(i-1)`, `t < p`, modulo `p^i`) the signed sums
`classSum3 e ε η (p^i) r = ∑_{e k % p^i = r} sg (ε k) η^(e k)` of the `p` classes are equal. -/
theorem classSum3_eq_of_bad3 (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) {η : F3} (hη : IsPrimitiveRoot η d)
    (hbad : Bad3 e ε (p ^ i * d)) (c t t' : ℕ) (ht : t < p) (ht' : t' < p) :
    classSum3 e ε η (p ^ i) (c % p ^ (i - 1) + t * p ^ (i - 1)) =
      classSum3 e ε η (p ^ i) (c % p ^ (i - 1) + t' * p ^ (i - 1)) := by
  sorry

/-- **S1′ (step-down modulo 3).**  `p` prime, `p ≠ 3` (`p = 2` allowed), `i ≥ 1`, `p ∤ d` (so `d ≥ 1`), `3 ∤ d`.  If the
signing `ε` is 3-bad at `p^i * d` and the level `i` of `p` is not live, then `ε` is 3-bad at `p^(i-1) * d`. -/
theorem bad3_of_not_live (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) (hbad : Bad3 e ε (p ^ i * d))
    (hlive : live e p i = false) : Bad3 e ε (p ^ (i - 1) * d) := by
  sorry

end Pnq
