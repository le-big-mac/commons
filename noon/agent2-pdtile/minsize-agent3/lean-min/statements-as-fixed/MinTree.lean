/-
The least size of a multiset on `Z_{pⁿ} × Z_q` (a tree) with a given exact pattern.
(Statements fixed by agent3 / Yonder, 26 November 2026.)  Lower bounds: `Pnq/Tree.lean`, `Pnq/Sharp.lean`,
`Pnq/Balanced.lean`.  Constructions: `Pnq/BuildU.lean`, `Pnq/BuildB.lean`.
-/
import Pnq.BuildU
import Pnq.BuildB

open Finset

namespace Pnq

variable {p q : ℕ}

/-- **Least size, `Φ_q ∤ A`.** -/
theorem isLeast_unbalanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ t : Tree p q n, size t = s ∧ ¬ F t 0 ∧ eSet t = Es ∧ fSet t = Fs} (minU p q Es Fs) := by
  sorry

/-- **Least size, `Φ_q ∣ A`, every level in `F`** (among multisets that are not empty). -/
theorem isLeast_balanced_all (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ t : Tree p q n, size t = s ∧ 0 < s ∧ F t 0 ∧ eSet t = Es ∧ fSet t = Finset.Icc 1 n}
      (q * p ^ Es.card) := by
  sorry

/-- **Least size, `Φ_q ∣ A`, `a0` the first level missing from `F`.** -/
theorem isLeast_balanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ t : Tree p q n, size t = s ∧ F t 0 ∧ eSet t = Es ∧ fSet t = Fs} (minB p q Es Fs a0) := by
  sorry

end Pnq
