/-
The lifting for every `N` and every `s`: the sets of sizes on `ZMod (N * s)` and on `ZMod N` are the same.
`Lift.sizes_eq_odd` of `Pnq/LiftAll.lean` without its hypothesis that `s` is odd; from it and `sizes_eq_two_all` of
`Pnq/SignFinal.lean`.
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignFinal
import Pnq.LiftAll

open Finset

namespace Pnq

namespace MulAux

/-- the sizes on `ZMod (N * 2^j)`, any `N`, by induction on `j`, by `sizes_eq_two_all` -/
theorem sizes_two_pow {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) (j : ℕ) :
    Lift.AllAux.sizes (N * 2 ^ j) P = Lift.AllAux.sizes N P := by
  induction j with
  | zero => exact Lift.AllAux.sizes_congr (by ring) P
  | succ i ih =>
    have e1 : Lift.AllAux.sizes (N * 2 ^ (i + 1)) P = Lift.AllAux.sizes (N * 2 ^ i * 2) P :=
      Lift.AllAux.sizes_congr (by ring) P
    have e2 : Lift.AllAux.sizes (N * 2 ^ i * 2) P = Lift.AllAux.sizes (N * 2 ^ i) P :=
      sizes_eq_two_all (N := N * 2 ^ i) P fun d hd => Dvd.dvd.mul_right (hP d hd) _
    exact e1.trans (e2.trans ih)

end MulAux

/-- **Sizes are the same on `ZMod (N * s)`, every `N`, every `s ≥ 1`.**  For a set `P` of divisors of `N`, the sizes of
the nonempty multisets on `ZMod (N * s)` whose mask is divisible by `Φ_d`, `d ∣ N * s`, `d ≠ 1`, exactly for `d ∈ P` are
the sizes of the nonempty multisets on `ZMod N` whose mask is divisible by `Φ_d`, `d ∣ N`, `d ≠ 1`, exactly for
`d ∈ P`. -/
theorem sizes_eq_mul_all {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  obtain ⟨j, s', hs', rfl⟩ := Nat.exists_eq_two_pow_mul_odd (NeZero.ne s)
  have hs'0 : s' ≠ 0 := by
    rintro rfl
    exact NeZero.ne (2 ^ j * 0) (mul_zero _)
  have : NeZero s' := ⟨hs'0⟩
  have e1 : Lift.AllAux.sizes (N * (2 ^ j * s')) P = Lift.AllAux.sizes (N * 2 ^ j * s') P :=
    Lift.AllAux.sizes_congr (by ring) P
  have e2 : Lift.AllAux.sizes (N * 2 ^ j * s') P = Lift.AllAux.sizes (N * 2 ^ j) P :=
    Lift.AllAux.sizes_odd P (fun d hd => Dvd.dvd.mul_right (hP d hd) _) s' hs'
  exact e1.trans (e2.trans (MulAux.sizes_two_pow P hP j))

end Pnq
