import Pnq.Rule
import Pnq.BalancedGroup
import Pqr.Cyclotomic
section SkBuildU
/-
The construction for the half with `Φ_q ∤ A`: for every pattern a tree with exactly that pattern and the
least size.  (Statement fixed by agent3 / Yonder, 26 November 2026.)
-/

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
end SkBuildU
section SkBuildB
/-
The constructions for the half with `Φ_q ∣ A`: for every pattern a tree with exactly that pattern and the
least size.  (Statements fixed by agent3 / Yonder, 26 November 2026.)
-/

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
end SkBuildB
section SkMinTree
/-
The least size of a multiset on `Z_{pⁿ} × Z_q` (a tree) with a given exact pattern.
(Statements fixed by agent3 / Yonder, 26 November 2026.)  Lower bounds: `Pnq/Tree.lean`, `Pnq/Sharp.lean`,
`Pnq/Balanced.lean`.  Constructions: `Pnq/BuildU.lean`, `Pnq/BuildB.lean`.
-/

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
end SkMinTree
section SkWeighted
/-
Multisets on `ZMod M`, given by their multiplicities `w : ZMod M → ℕ`: Fourier zeros, the mask polynomial,
and (for `M = p^n * q`) the tree of a multiset, with the bridge between the level conditions `E`, `F` of
`Pnq/Tree.lean` and the Fourier zeros.  This is `Pqr/ZeroDefs.lean`, `Pqr/Cyclotomic.lean` and
`Pnq/Group.lean` again with weights in place of a set.
(Definitions and statements fixed by agent3 / Yonder, 26 November 2026.)
-/

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
end SkWeighted
section SkMinGroup
/-
The least size of a multiset on `ZMod (p^n * q)` whose mask polynomial is divisible by exactly a given set of
the cyclotomic polynomials `Φ_d`, `d ∣ p^n q`, `d > 1`.
(Definitions and statements fixed by agent3 / Yonder, 26 November 2026.)

The divisors `d > 1` of `p^n q` are `p^ℓ` (`1 ≤ ℓ ≤ n`), `q`, and `p^ℓ q` (`1 ≤ ℓ ≤ n`).  A pattern is: the set
`Es` of levels `ℓ` with `Φ_{p^ℓ} ∣ A(X)`, the set `Fs` of levels `ℓ ≥ 1` with `Φ_{p^ℓ q} ∣ A(X)`, and whether
`Φ_q ∣ A(X)`.  The three theorems below cover every pattern.
-/

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ} ∣ A(X)` -/
noncomputable def levelsEW (w : ZMod (p ^ n * q) → ℕ) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Polynomial.cyclotomic (p ^ ℓ) ℤ ∣ maskW w)

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ q} ∣ A(X)` -/
noncomputable def levelsFW (w : ZMod (p ^ n * q) → ℕ) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Polynomial.cyclotomic (p ^ ℓ * q) ℤ ∣ maskW w)

/-- **Least size, `Φ_q ∤ A(X)`.** Among the multisets on `Z_{p^n q}` whose mask polynomial is not divisible
by `Φ_q`, is divisible by `Φ_{p^ℓ}` exactly for `ℓ ∈ Es` and by `Φ_{p^ℓ q}` (`ℓ ≥ 1`) exactly for `ℓ ∈ Fs`,
the least number of elements is `p^|Es|` if `Fs ⊆ Es`, and `p^|Es| (p^|Fs \ Es| + q)` otherwise. -/
theorem minsize_unbalanced_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ ¬ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Fs}
      (minU p q Es Fs) := by
  sorry

/-- **Least size, `Φ_q ∣ A(X)` and `Φ_{p^ℓ q} ∣ A(X)` for every `ℓ`.** Among the multisets that are not
empty, the least number of elements is `q p^|Es|`. -/
theorem minsize_balanced_all_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ 0 < s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Finset.Icc 1 n}
      (q * p ^ Es.card) := by
  sorry

/-- **Least size, `Φ_q ∣ A(X)`, and `a0` the first level in `1..n` with `Φ_{p^a0 q} ∤ A(X)`.** The least number
of elements is `q p^|Es| (p^k' + x)`, where `k'` is the number of levels beyond `a0` that are in `Fs` and not
in `Es`, and `x` is `0` or `1` by the four clauses of `xOf`. -/
theorem minsize_balanced_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (Es Fs : Finset ℕ) (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0)
    (han : a0 ≤ n) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    IsLeast {s | ∃ w : ZMod (p ^ n * q) → ℕ, ∑ a, w a = s ∧ Polynomial.cyclotomic q ℤ ∣ maskW w ∧
        levelsEW w = Es ∧ levelsFW w = Fs}
      (minB p q Es Fs a0) := by
  sorry

end Pnq
end SkMinGroup
open Pnq
-- the fixed definitions, as Lean has them
#print Pnq.gOf
#print Pnq.xOf
#print Pnq.minU
#print Pnq.minB
#print Pnq.hatW
#print Pnq.ZeroAtW
#print Pnq.maskW
#print Pnq.indW
#print Pnq.subW
#print Pnq.treeOfW
#print Pnq.levelsEW
#print Pnq.levelsFW
-- the fixed statements, as Lean has them
#check @Pnq.exists_unbalanced
#check @Pnq.exists_balanced_all
#check @Pnq.exists_balanced
#check @Pnq.isLeast_unbalanced
#check @Pnq.isLeast_balanced_all
#check @Pnq.isLeast_balanced
#check @Pnq.zeroAtW_indW
#check @Pnq.maskW_indW
#check @Pnq.zeroAtW_iff_cyclotomic_dvd
#check @Pnq.treeOfW_indW
#check @Pnq.size_treeOfW
#check @Pnq.E_treeOfW
#check @Pnq.F_treeOfW_zero
#check @Pnq.F_treeOfW
#check @Pnq.treeOfW_surjective
#check @Pnq.minsize_unbalanced_zmod
#check @Pnq.minsize_balanced_all_zmod
#check @Pnq.minsize_balanced_zmod
