/-
The construction for the half with `Φ_q ∤ A`: for every pattern a tree with exactly that pattern and the
least size.  (Statement fixed by agent3 / Yonder, 26 November 2026.)
-/
import Pnq.Rule

open Finset

namespace Pnq

variable {p q : ℕ}

/-- **The construction, `Φ_q ∤ A`.** For all sets `Es`, `Fs` of levels in `1..n` there is a tree (a multiset
on `Z_{pⁿ} × Z_q`) that is not balanced, whose levels of `E` are exactly `Es`, whose levels `≥ 1` of `F` are
exactly `Fs`, and which has `minU p q Es Fs` elements. -/
theorem exists_unbalanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    ∃ t : Tree p q n, ¬ F t 0 ∧ eSet t = Es ∧ fSet t = Fs ∧ size t = minU p q Es Fs := by
  sorry

end Pnq
