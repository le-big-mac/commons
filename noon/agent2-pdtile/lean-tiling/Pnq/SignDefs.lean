/-
The statement on signs for every odd `n`: definitions.

Setting.  `ι` is a finite type (the elements of a multiset, one point for each element), `e : ι → ℕ` gives their
exponents, a signing is `ε : ι → Bool` (`true` is `+`, `false` is `-`).  The signed mask is
`P e ε = ∑ k, sg (ε k) X ^ e k`; the signing is bad at `d` if `Φ_d` divides it.  For a prime `p` and a level `i ≥ 1`,
a class is a residue modulo `p^i`, it is occupied if some `e k` lies in it; the group of `c < p^(i-1)` is the `p`
classes `c + t p^(i-1)`, `t < p`; the level `i` is live if some group is full (all its `p` classes occupied).
`rank e p i` counts the live levels `1, …, i`, and `μ t` is the largest `(p - 1) v_p(t)` over the primes `p ∣ t`.
(Definitions fixed on 27 November 2026, before any Lean proof that uses them.  `live`, `rank`, `μ`, `lhsN1` can be
evaluated; the polynomial `P`, and so `BadAt` and `badSet`, cannot.)
-/
import Mathlib

open Finset

namespace Pnq

/-- the sign of a Boolean: `true` is `1`, `false` is `-1` -/
def sg (b : Bool) : ℤ := if b then 1 else -1

section

variable {ι : Type*} [Fintype ι]

/-- the signed mask `∑ k, sg (ε k) X ^ e k` of the signing `ε` of the elements with exponents `e` -/
noncomputable def P (e : ι → ℕ) (ε : ι → Bool) : Polynomial ℤ :=
  ∑ k, Polynomial.C (sg (ε k)) * Polynomial.X ^ e k

/-- the signing `ε` is bad at `d`: the cyclotomic polynomial `Φ_d` divides the signed mask -/
def BadAt (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) : Prop :=
  Polynomial.cyclotomic d ℤ ∣ P e ε

open Classical in
/-- the set of the signings that are bad at `d` -/
noncomputable def badSet (e : ι → ℕ) (d : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε => BadAt e ε d

/-- the signed sum `∑ sg (ε k) η ^ e k` over the elements `k` in the class `r` modulo `M` (that is, `e k % M = r`);
the plan's `s r`, with `M = p^i` and `η` a root of unity of order prime to `p` -/
noncomputable def classSum (e : ι → ℕ) (ε : ι → Bool) (η : ℂ) (M r : ℕ) : ℂ :=
  ∑ k, if e k % M = r then (sg (ε k) : ℂ) * η ^ e k else 0

/-- level `i` of `p` is live for `e`: there is `c < p^(i-1)` such that each of the `p` classes `c + t p^(i-1)`,
`t < p`, modulo `p^i` is occupied (holds `e k` for some `k`).  A Boolean, so that it can be evaluated. -/
def live (e : ι → ℕ) (p i : ℕ) : Bool :=
  decide (∃ c, c < p ^ (i - 1) ∧ ∀ t, t < p → ∃ k, e k % p ^ i = c + t * p ^ (i - 1))

/-- the number of live levels `j` of `p` with `1 ≤ j ≤ i` -/
def rank (e : ι → ℕ) (p i : ℕ) : ℕ :=
  ((Finset.Icc 1 i).filter fun j => live e p j = true).card

/-- `J` is a pivot set for the level `i` of `p`: its elements lie in pairwise different classes modulo `p^i`, and
every group at level `i` (the `p` classes `c % p^(i-1) + t p^(i-1)`, `t < p`) has a class that holds no element
of `J` -/
def IsPivot (e : ι → ℕ) (p i : ℕ) (J : Finset ι) : Prop :=
  (∀ k ∈ J, ∀ k' ∈ J, e k % p ^ i = e k' % p ^ i → k = k') ∧
    ∀ c, ∃ t, t < p ∧ ∀ k ∈ J, e k % p ^ i ≠ c % p ^ (i - 1) + t * p ^ (i - 1)

end

/-- `μ t`: the largest `(p - 1) * v_p(t)` over the primes `p` dividing `t` (`0` for `t = 0, 1`) -/
def μ (t : ℕ) : ℕ :=
  t.primeFactors.sup fun p => (p - 1) * t.factorization p

/-- the left side of the inequality N1 for `m` elements and a set `T` of odd numbers:
`∑_{t ∈ T} (1/2)^(μ t)`, to which, if `m` is even, `m.choose (m/2) / 2^m` is added, and from which, if moreover
`3 ∈ T` and `14 ≤ m`, `1/16` is taken away -/
def lhsN1 (m : ℕ) (T : Finset ℕ) : ℚ :=
  (if Even m then (m.choose (m / 2) : ℚ) / 2 ^ m else 0) + ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t
    - (if Even m ∧ 3 ∈ T ∧ 14 ≤ m then 1 / 16 else 0)

/-! Unfolding lemmas. -/

section

variable {ι : Type*} [Fintype ι]

/-- membership in `badSet` (unfolding) -/
theorem mem_badSet (e : ι → ℕ) (d : ℕ) (ε : ι → Bool) : ε ∈ badSet e d ↔ BadAt e ε d := by
  simp [badSet]

/-- `live` as a proposition (unfolding) -/
theorem live_iff (e : ι → ℕ) (p i : ℕ) :
    live e p i = true ↔
      ∃ c, c < p ^ (i - 1) ∧ ∀ t, t < p → ∃ k, e k % p ^ i = c + t * p ^ (i - 1) := by
  simp [live]

end

end Pnq
