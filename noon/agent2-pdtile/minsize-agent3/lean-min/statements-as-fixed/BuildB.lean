/-
The constructions for the half with `Φ_q ∣ A`: for every pattern a tree with exactly that pattern and the
least size.  (Statements fixed by agent3 / Yonder, 26 November 2026.)
-/
import Pnq.Rule

open Finset

namespace Pnq

variable {p q : ℕ}

/-- **The construction, `Φ_q ∣ A`, every level in `F`.** For every set `Es` of levels in `1..n` there is a
balanced tree whose levels of `E` are exactly `Es`, whose levels `≥ 1` of `F` are all of `1..n`, and which has
`q · p^|Es|` elements. -/
theorem exists_balanced_all (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) :
    ∃ t : Tree p q n, F t 0 ∧ eSet t = Es ∧ fSet t = Finset.Icc 1 n ∧ size t = q * p ^ Es.card := by
  sorry

/-- **The construction, `Φ_q ∣ A`, some level missing from `F`.** Let `Es`, `Fs` be sets of levels in `1..n`
and `a0` the first level in `1..n` that is not in `Fs`.  There is a balanced tree whose levels of `E` are
exactly `Es`, whose levels `≥ 1` of `F` are exactly `Fs`, and which has `minB p q Es Fs a0` elements. -/
theorem exists_balanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    ∃ t : Tree p q n, F t 0 ∧ eSet t = Es ∧ fSet t = Fs ∧ size t = minB p q Es Fs a0 := by
  sorry

end Pnq
