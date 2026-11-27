/-
The statement on signs for every odd `n`: the slices.  S0 (a signing that is bad at `p^i d` has equal sums on the `p`
classes of every group at level `i` of `p`) and S1 (step-down: if moreover the level `i` of `p` is not live, the
signing is bad at `p^(i-1) d`).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignDefs
import Pnq.Lift2

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-- **S0 (flatness).**  `p` prime, `i ≥ 1`, `p ∤ d` (so `d ≥ 1`), `η` a complex root of unity of order `d`.  If the
signing `ε` is bad at `p^i * d`, then in every group at level `i` (the `p` classes `c % p^(i-1) + t p^(i-1)`, `t < p`,
modulo `p^i`) the signed sums `classSum e ε η (p^i) r = ∑_{e k % p^i = r} sg (ε k) η^(e k)` of the `p` classes are
equal. -/
theorem classSum_eq_of_badAt (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i)
    {d : ℕ} (hd : ¬ p ∣ d) {η : ℂ} (hη : IsPrimitiveRoot η d) (hbad : BadAt e ε (p ^ i * d))
    (c t t' : ℕ) (ht : t < p) (ht' : t' < p) :
    classSum e ε η (p ^ i) (c % p ^ (i - 1) + t * p ^ (i - 1)) =
      classSum e ε η (p ^ i) (c % p ^ (i - 1) + t' * p ^ (i - 1)) := by
  sorry

/-- **S1 (step-down).**  `p` prime, `i ≥ 1`, `p ∤ d` (so `d ≥ 1`).  If the signing `ε` is bad at `p^i * d` and the
level `i` of `p` is not live, then `ε` is bad at `p^(i-1) * d`. -/
theorem badAt_of_not_live (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i)
    {d : ℕ} (hd : ¬ p ∣ d) (hbad : BadAt e ε (p ^ i * d)) (hlive : live e p i = false) :
    BadAt e ε (p ^ (i - 1) * d) := by
  sorry

end Pnq
