/-
The rule for the least size of a multiset with a given exact pattern: definitions only.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any proof that uses them was written.)

`Es` and `Fs` are sets of levels in `1..n`: `Es` the levels `ℓ` with `Φ_{p^ℓ} ∣ A`, `Fs` the levels `ℓ ≥ 1` with
`Φ_{p^ℓ q} ∣ A`.  Whether `Φ_q ∣ A` (level `0` of `F` in the notes) is said separately, in words.
-/
import Pnq.Balanced

open Finset

namespace Pnq

/-- the levels beyond `a0` that are in `Fs` and not in `Es` -/
def gOf (Es Fs : Finset ℕ) (a0 : ℕ) : Finset ℕ := (Fs \ Es).filter (fun ℓ => a0 < ℓ)

/-- The summand `x` of the rule for the half with `Φ_q ∣ A`, where `a0` is the first level in `1..n` missing
from `Fs`: `x = 0` if one of four clauses holds, and `x = 1` otherwise.  The clauses: (1) no level beyond `a0`
is in `Fs` and not in `Es`; (2) some level before `a0` is in `Es`; (3) `a0 ∈ Es` and `p ≥ 3`; (4) `a0 ∈ Es`,
`p = 2`, and some level of `Es \ Fs` lies strictly between `a0` and every level beyond `a0` that is in `Fs`
and not in `Es`. -/
def xOf (p : ℕ) (Es Fs : Finset ℕ) (a0 : ℕ) : ℕ :=
  if gOf Es Fs a0 = ∅ ∨ (∃ ℓ ∈ Es, ℓ < a0) ∨ (a0 ∈ Es ∧ 3 ≤ p) ∨
      (a0 ∈ Es ∧ p = 2 ∧ ∃ b ∈ Es \ Fs, a0 < b ∧ ∀ g ∈ gOf Es Fs a0, b < g) then 0 else 1

/-- the least size when `Φ_q ∤ A` -/
def minU (p q : ℕ) (Es Fs : Finset ℕ) : ℕ :=
  if Fs ⊆ Es then p ^ Es.card else p ^ Es.card * (p ^ (Fs \ Es).card + q)

/-- the least size when `Φ_q ∣ A` and `a0` is the first level in `1..n` missing from `Fs` -/
def minB (p q : ℕ) (Es Fs : Finset ℕ) (a0 : ℕ) : ℕ :=
  q * p ^ Es.card * (p ^ (gOf Es Fs a0).card + xOf p Es Fs a0)

end Pnq
