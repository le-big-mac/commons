/-
Lifting.  For an odd prime `r`, a multiset on `ZMod N` can be lifted to `ZMod (N * r)` with the same number of elements and
exactly the same cyclotomic divisors of its mask polynomial: every `Φ_d` with `d ∣ N` divides the one mask exactly when it divides
the other, and no `Φ_d` with `d ∣ N * r`, `d ∤ N` divides the lifted one.  Reduction modulo `N` goes the other way.  So the sizes
of the multisets with exactly a given pattern of divisors of `N` are the same on `ZMod N` and on `ZMod (N * r)`.
(Definitions and statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  The lemma on lifts is
due to a fresh instance that read a note of mine; the proof on paper is by counting roots.)
-/
import Pnq.Weighted

open Finset

namespace Pnq

namespace Lift

variable {N r : ℕ} [NeZero N] [Fact r.Prime]

instance instNeZeroMul : NeZero (N * r) :=
  ⟨Nat.mul_ne_zero (NeZero.ne N) (Fact.out : r.Prime).ne_zero⟩

/-- Reduction modulo `N` of a multiset on `ZMod (N * r)`: the multiplicity of `x` is the number of elements, counted with
multiplicity, whose residue modulo `N` is `x`. -/
def reduce (w' : ZMod (N * r) → ℕ) : ZMod N → ℕ :=
  fun x => ∑ y : ZMod (N * r), if ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y = x then w' y else 0

/-- reduction keeps the number of elements -/
theorem sum_reduce (w' : ZMod (N * r) → ℕ) : ∑ x, reduce w' x = ∑ y, w' y := by
  sorry

/-- for `d ∣ N`, `Φ_d` divides the mask of the reduced multiset exactly when it divides the mask of the multiset -/
theorem cyclotomic_dvd_reduce_iff (w' : ZMod (N * r) → ℕ) (d : ℕ) (hd : d ∣ N) :
    Polynomial.cyclotomic d ℤ ∣ maskW (reduce w') ↔ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  sorry

/-- **The lemma on lifts.** If `r` is odd, a nonempty multiset on `ZMod N` is the reduction of a multiset on `ZMod (N * r)`
whose mask is divisible by no `Φ_d` with `d ∣ N * r`, `d ∤ N`. -/
theorem exists_lift (hr : r ≠ 2) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * r) → ℕ, reduce w' = w ∧
      ∀ d, d ∣ N * r → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  sorry

/-- **Sizes are the same.** If `r` is odd and `P` is a set of divisors of `N`, the numbers of elements of the nonempty
multisets on `ZMod (N * r)` whose mask is divisible by `Φ_d`, for `d ∣ N * r`, `d ≠ 1`, exactly when `d ∈ P`, are the numbers
of elements of the nonempty multisets on `ZMod N` whose mask is divisible by `Φ_d`, for `d ∣ N`, `d ≠ 1`, exactly when
`d ∈ P`. -/
theorem sizes_eq (hr : r ≠ 2) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * r) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * r → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  sorry

end Lift

end Pnq
