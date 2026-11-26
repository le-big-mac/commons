/-
Multisets on `ZMod M`, given by their multiplicities `w : ZMod M → ℕ`: Fourier zeros, the mask polynomial,
and (for `M = p^n * q`) the tree of a multiset, with the bridge between the level conditions `E`, `F` of
`Pnq/Tree.lean` and the Fourier zeros.  This is `Pqr/ZeroDefs.lean`, `Pqr/Cyclotomic.lean` and
`Pnq/Group.lean` again with weights in place of a set.
(Definitions and statements fixed by agent3 / Yonder, 26 November 2026.)
-/
import Pnq.BalancedGroup
import Pqr.Cyclotomic

open Finset

namespace Pnq

section General

variable {M : ℕ} [NeZero M]

/-- the Fourier coefficient at `ξ` of the multiset with multiplicities `w` -/
noncomputable def hatW (w : ZMod M → ℕ) (ξ : ZMod M) : ℂ :=
  ∑ a : ZMod M, (w a : ℂ) * ZMod.stdAddChar (ξ * a)

/-- the multiset `w` has no Fourier mass at the frequencies of order `d` -/
def ZeroAtW (w : ZMod M → ℕ) (d : ℕ) : Prop := ∀ ξ : ZMod M, Pqr.ord ξ = d → hatW w ξ = 0

/-- the mask polynomial `∑ w(a) X^a` of a multiset of residues, with exponents in `[0, M)` -/
noncomputable def maskW (w : ZMod M → ℕ) : Polynomial ℤ :=
  ∑ a : ZMod M, Polynomial.C (w a : ℤ) * Polynomial.X ^ a.val

/-- the multiset of a set: multiplicity `1` on the set and `0` off it -/
def indW (A : Finset (ZMod M)) : ZMod M → ℕ := fun a => if a ∈ A then 1 else 0

/-- on a set, `ZeroAtW` is `Pqr.ZeroAt` -/
theorem zeroAtW_indW (A : Finset (ZMod M)) (d : ℕ) : ZeroAtW (indW A) d ↔ Pqr.ZeroAt A d := by
  sorry

/-- on a set, `maskW` is `Pqr.mask` -/
theorem maskW_indW (A : Finset (ZMod M)) : maskW (indW A) = Pqr.mask A := by
  sorry

/-- For `d ∣ M`: the multiset `w` has no Fourier mass at the frequencies of order `d` iff the cyclotomic
polynomial `Φ_d` divides its mask polynomial. -/
theorem zeroAtW_iff_cyclotomic_dvd (w : ZMod M → ℕ) (d : ℕ) (hd : d ∣ M) :
    ZeroAtW w d ↔ Polynomial.cyclotomic d ℤ ∣ maskW w := by
  sorry

end General

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

/-- The part of the multiset `w` in the residue class `r` modulo `p^d`, as a tree of depth `k`: the children
of a node are the classes of the next base-`p` digit, and a leaf holds the number of elements, with
multiplicity, in each class modulo `q`.  (Intended for `d + k = n` and `r < p^d`.) -/
def subW (w : ZMod (p ^ n * q) → ℕ) : (k : ℕ) → ℕ → ℕ → Tree p q k
  | 0, d, r => .leaf (fun j => ∑ a : ZMod (p ^ n * q),
      if a.val % p ^ d = r ∧ a.val % q = (j : ℕ) then w a else 0)
  | k + 1, d, r => .node (fun c => subW w k (d + 1) (r + (c : ℕ) * p ^ d))

/-- the tree of a multiset on `ZMod (p^n * q)` -/
def treeOfW (w : ZMod (p ^ n * q) → ℕ) : Tree p q n := subW w n 0 0

/-- on a set, `treeOfW` is `treeOf` -/
theorem treeOfW_indW (A : Finset (ZMod (p ^ n * q))) : treeOfW (indW A) = treeOf A := by
  sorry

/-- the size of the tree is the number of elements, with multiplicity -/
theorem size_treeOfW (w : ZMod (p ^ n * q) → ℕ) : size (treeOfW w) = ∑ a : ZMod (p ^ n * q), w a := by
  sorry

/-- level `ℓ` of `E`, `1 ≤ ℓ ≤ n`: no Fourier mass at order `p^ℓ` -/
theorem E_treeOfW (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    E (treeOfW w) ℓ ↔ ZeroAtW w (p ^ ℓ) := by
  sorry

/-- level `0` of `F`: no Fourier mass at order `q` -/
theorem F_treeOfW_zero (w : ZMod (p ^ n * q) → ℕ) : F (treeOfW w) 0 ↔ ZeroAtW w q := by
  sorry

/-- level `ℓ` of `F`, `1 ≤ ℓ ≤ n`: no Fourier mass at order `p^ℓ q` -/
theorem F_treeOfW (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    F (treeOfW w) ℓ ↔ ZeroAtW w (p ^ ℓ * q) := by
  sorry

/-- every tree is the tree of a multiset on `ZMod (p^n * q)` (the Chinese remainder theorem) -/
theorem treeOfW_surjective (hpq : p ≠ q) :
    Function.Surjective (treeOfW : (ZMod (p ^ n * q) → ℕ) → Tree p q n) := by
  sorry

end Pnq
