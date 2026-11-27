import Pnq.Weighted
import Pnq.MinGroup
/-
Lifting.  For an odd prime `r`, a multiset on `ZMod N` can be lifted to `ZMod (N * r)` with the same number of elements and
exactly the same cyclotomic divisors of its mask polynomial: every `Φ_d` with `d ∣ N` divides the one mask exactly when it divides
the other, and no `Φ_d` with `d ∣ N * r`, `d ∤ N` divides the lifted one.  Reduction modulo `N` goes the other way.  So the sizes
of the multisets with exactly a given pattern of divisors of `N` are the same on `ZMod N` and on `ZMod (N * r)`.
(Definitions and statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  The lemma on lifts is
due to a fresh instance that read a note of mine; the proof on paper is by counting roots.)
-/

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

/-
The least-size theorem for `Z_{pⁿq}` on the larger group `Z_{pⁿq·r}`, `r` an odd prime (`r` may be `p` or `q`): among the
multisets on `ZMod (p^n * q * r)` whose cyclotomic divisors are a given pattern of divisors of `p^n * q` and no others, the
least number of elements is the one the theorem gives on `ZMod (p^n * q)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.)
-/

open Finset

namespace Pnq

namespace Lift

/-- **Unbalanced patterns, lifted.**  `r` an odd prime.  Among the multisets on `ZMod (p^n * q * r)` with `Φ_q ∤ A(X)`,
with `Φ_{p^ℓ} ∣ A(X)` exactly for the levels `ℓ ∈ Es`, with `Φ_{p^ℓ q} ∣ A(X)` exactly for the levels `ℓ ∈ Fs`, and with
no `Φ_d ∣ A(X)` for a divisor `d` of `p^n q r` that does not divide `p^n q`, the least size is `minU p q Es Fs`. -/
theorem minsize_unbalanced_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minU p q Es Fs) := by
  sorry

/-- **Balanced patterns with every `Φ_{p^ℓ q}`, lifted.** -/
theorem minsize_balanced_all_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ 0 < s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (q * p ^ Es.card) := by
  sorry

/-- **Balanced patterns with a first level `a0` at which `Φ_{p^a0 q} ∤ A(X)`, lifted.** -/
theorem minsize_balanced_lift (p q n r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] (hpq : p ≠ q) (hr : r ≠ 2)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q * r) → ℕ, ∑ a, w a = s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w ↔ ℓ ∈ Es) ∧
        (∀ ℓ ∈ Finset.Icc 1 n, Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w ↔ ℓ ∈ Fs) ∧
        ∀ d, d ∣ p ^ n * q * r → ¬ d ∣ p ^ n * q → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w}
      (minB p q Es Fs a0) := by
  sorry

end Lift

end Pnq

open Lean Meta Elab Command in
run_cmd do
  for n in [``Pnq.Lift.instNeZeroMul, ``Pnq.Lift.reduce,
      ``Pnq.Lift.sum_reduce, ``Pnq.Lift.cyclotomic_dvd_reduce_iff, ``Pnq.Lift.exists_lift, ``Pnq.Lift.sizes_eq,
      ``Pnq.Lift.minsize_unbalanced_lift, ``Pnq.Lift.minsize_balanced_all_lift, ``Pnq.Lift.minsize_balanced_lift] do
    let ci ← getConstInfo n
    IO.println s!"### {n} TYPE hash={ci.type.hash} levelParams={ci.levelParams}"
    IO.println (toString (repr ci.type))
    if let .defnInfo d := ci then
      IO.println s!"### {n} VALUE hash={d.value.hash}"
      IO.println (toString (repr d.value))
    if n == ``Pnq.Lift.instNeZeroMul then
      if let .thmInfo d := ci then
        IO.println s!"### {n} VALUE hash={d.value.hash}"
        IO.println (toString (repr d.value))
