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

/-! Helper lemmas live in the namespace `Pnq.WeightedAux`, so that their names cannot clash with those of
the other files of the project.  They are the lemmas of `Pqr/Bridge.lean`, `Pqr/SCBounds.lean`,
`Pqr/Cyclotomic.lean` and `Pnq/Group.lean` again, with a weight `w a` in place of membership `a ∈ A`. -/

namespace WeightedAux

/-- on a set, `hatW` is `Pqr.hat` -/
theorem hatW_indW (A : Finset (ZMod M)) (ξ : ZMod M) : hatW (indW A) ξ = Pqr.hat A ξ := by
  rw [hatW, Pqr.hat, ← Fintype.sum_ite_mem A]
  refine Finset.sum_congr rfl fun a _ => ?_
  simp only [indW]
  split_ifs <;> simp

/-- The Fourier coefficient of `w` at `ξ` is the value of the mask polynomial at `ψ ξ`. -/
theorem hatW_eq_aeval_maskW (w : ZMod M → ℕ) (ξ : ZMod M) :
    hatW w ξ = Polynomial.aeval (ZMod.stdAddChar ξ : ℂ) (maskW w) := by
  rw [hatW, maskW, map_sum]
  refine Finset.sum_congr rfl fun a _ => ?_
  have h : Polynomial.aeval (ZMod.stdAddChar ξ : ℂ) (Polynomial.C (w a : ℤ) * Polynomial.X ^ a.val)
      = (w a : ℂ) * (ZMod.stdAddChar ξ : ℂ) ^ a.val := by
    simp
  rw [h, ← AddChar.map_nsmul_eq_pow, nsmul_eq_mul, ZMod.natCast_zmod_val, mul_comm a]

/-- Galois: the Fourier zeros of a multiset are a union of classes of frequencies of equal order. -/
theorem zeroAtW_of_hatW_eq_zero (w : ZMod M → ℕ) (ξ : ZMod M) (h : hatW w ξ = 0) :
    ZeroAtW w (Pqr.ord ξ) := by
  intro ξ' hξ'
  have hM : M ≠ 0 := NeZero.ne M
  obtain ⟨u, hu⟩ := Pqr.exists_unit_mul_of_ord_eq ξ ξ' hξ'
  have hk : ((u : ZMod M).val).Coprime M := ZMod.val_coe_unit_coprime u
  have h' : ∑ a : ZMod M, (((w a : ℤ)) : ℂ) * ZMod.stdAddChar (ξ * a) = 0 := by
    simpa [hatW] using h
  have hgal := Pqr.galois_sum Finset.univ M hM (fun a => (w a : ℤ))
    (fun a => ZMod.stdAddChar (ξ * a))
    (fun a _ => by
      rw [← AddChar.map_nsmul_eq_pow, nsmul_eq_mul, ZMod.natCast_self, zero_mul,
        AddChar.map_zero_eq_one])
    _ hk h'
  rw [hatW, ← hgal]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [← AddChar.map_nsmul_eq_pow, nsmul_eq_mul, ZMod.natCast_zmod_val, hu, mul_assoc]
  simp

/-- the number of elements of the multiset `w`, with multiplicity, congruent to `v` modulo `d`
(meaningful for `d ∣ M`) -/
def cntW (w : ZMod M → ℕ) (d : ℕ) (v : ZMod M) : ℕ :=
  ∑ a : ZMod M, if d ∣ (a - v).val then w a else 0

/-- the transform of a count function -/
theorem sum_cntW_mul_char (w : ZMod M → ℕ) (j : ℕ) (hj : j ∣ M) (ξ : ZMod M) :
    ∑ v : ZMod M, (cntW w j v : ℂ) * ZMod.stdAddChar (ξ * v)
      = hatW w ξ * (if Pqr.ord ξ ∣ j then ((M / j : ℕ) : ℂ) else 0) := by
  have h1 : ∀ v : ZMod M, (cntW w j v : ℂ) * ZMod.stdAddChar (ξ * v)
      = ∑ a : ZMod M, (w a : ℂ) * (if j ∣ (a - v).val then ZMod.stdAddChar (ξ * v) else 0) := by
    intro v
    rw [cntW, Nat.cast_sum, Finset.sum_mul]
    refine Finset.sum_congr rfl fun a _ => ?_
    split_ifs <;> simp
  simp_rw [h1]
  rw [Finset.sum_comm, hatW, Finset.sum_mul]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [← Finset.mul_sum, mul_assoc]
  congr 1
  rw [← Equiv.sum_comp (Equiv.subLeft a)]
  have h2 : ∀ t : ZMod M,
      (if j ∣ (a - (Equiv.subLeft a) t).val then ZMod.stdAddChar (ξ * (Equiv.subLeft a) t) else 0)
        = ZMod.stdAddChar (ξ * a) * (if j ∣ t.val then ZMod.stdAddChar (-ξ * t) else 0) := by
    intro t
    rw [Equiv.subLeft_apply, sub_sub_cancel]
    split_ifs
    · rw [← AddChar.map_add_eq_mul]
      congr 1
      ring
    · rw [mul_zero]
  simp_rw [h2]
  rw [← Finset.mul_sum, Pqr.Bridge.sum_char_multiples j hj]
  simp only [neg_mul, neg_eq_zero, Pqr.Bridge.mul_natCast_eq_zero_iff]

/-- The bridge for multisets, for a family of divisors indexed by an arbitrary type. -/
theorem zeroAtW_iff_cntW_aux {ι : Type*} (w : ZMod M → ℕ) (d : ℕ) (s : Finset ι) (J : ι → ℕ)
    (c : ι → ℤ) (hS : ∀ i ∈ s, J i ∣ M)
    (hc : ∀ e, e ∣ M → (∑ i ∈ s, if e ∣ J i then c i else 0) = if e = d then 1 else 0) :
    ZeroAtW w d ↔ ∀ v : ZMod M, ∑ i ∈ s, c i * (J i : ℤ) * (cntW w (J i) v : ℤ) = 0 := by
  have hM : (M : ℂ) ≠ 0 := Nat.cast_ne_zero.2 (NeZero.ne M)
  have key : ∀ ξ : ZMod M,
      ∑ v : ZMod M, ((∑ i ∈ s, c i * (J i : ℤ) * (cntW w (J i) v : ℤ) : ℤ) : ℂ)
          * ZMod.stdAddChar (ξ * v)
        = hatW w ξ * M * (if Pqr.ord ξ = d then 1 else 0) := by
    intro ξ
    calc ∑ v : ZMod M, ((∑ i ∈ s, c i * (J i : ℤ) * (cntW w (J i) v : ℤ) : ℤ) : ℂ)
          * ZMod.stdAddChar (ξ * v)
        = ∑ i ∈ s, (c i : ℂ) * ((J i : ℂ)
            * ∑ v : ZMod M, (cntW w (J i) v : ℂ) * ZMod.stdAddChar (ξ * v)) := by
          push_cast
          simp_rw [Finset.sum_mul, Finset.mul_sum]
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun v _ => by ring
      _ = ∑ i ∈ s, hatW w ξ * M * (((if Pqr.ord ξ ∣ J i then c i else 0 : ℤ)) : ℂ) := by
          refine Finset.sum_congr rfl fun i hi => ?_
          rw [sum_cntW_mul_char w (J i) (hS i hi) ξ]
          have hJ : (J i : ℂ) * ((M / J i : ℕ) : ℂ) = M := by
            rw [← Nat.cast_mul, Nat.mul_div_cancel' (hS i hi)]
          split_ifs
          · linear_combination (c i : ℂ) * hatW w ξ * hJ
          · simp
      _ = hatW w ξ * M * (if Pqr.ord ξ = d then 1 else 0) := by
          rw [← Finset.mul_sum, ← Int.cast_sum, hc _ (Pqr.ord_dvd ξ)]
          split_ifs <;> simp
  constructor
  · intro hz v
    have h0 := Pqr.Bridge.fourier_uniq_zmod
      (fun v => ((∑ i ∈ s, c i * (J i : ℤ) * (cntW w (J i) v : ℤ) : ℤ) : ℂ)) (fun ξ => by
        rw [key]
        split_ifs with h
        · rw [hz ξ h]; simp
        · simp)
    have h1 : ((∑ i ∈ s, c i * (J i : ℤ) * (cntW w (J i) v : ℤ) : ℤ) : ℂ) = 0 := congrFun h0 v
    exact_mod_cast h1
  · intro hg ξ hξ
    have h1 := key ξ
    simp only [hg, Int.cast_zero, zero_mul, Finset.sum_const_zero, hξ, ite_true, mul_one] at h1
    exact (mul_eq_zero.1 h1.symm).resolve_right hM

/-- every element is congruent to `v` modulo 1 -/
theorem cntW_one (w : ZMod M → ℕ) (v : ZMod M) : cntW w 1 v = ∑ a : ZMod M, w a := by
  simp [cntW]

/-- order a prime power: the count of a class mod `p^(ℓ+1)` is `1/p` of the count of its class mod `p^ℓ` -/
theorem zeroAtW_prime_pow (w : ZMod M → ℕ) (p : ℕ) (hp : p.Prime) (ℓ : ℕ)
    (h : p ^ (ℓ + 1) ∣ M) :
    ZeroAtW w (p ^ (ℓ + 1)) ↔ ∀ v : ZMod M, p * cntW w (p ^ (ℓ + 1)) v = cntW w (p ^ ℓ) v := by
  have hℓ : p ^ ℓ ∣ M := (pow_dvd_pow p (Nat.le_succ ℓ)).trans h
  have hpl : (p : ℤ) ^ ℓ ≠ 0 := pow_ne_zero _ (Nat.cast_ne_zero.2 hp.ne_zero)
  have key : ∀ X W : ℕ,
      ((1 : ℤ) * ((p ^ (ℓ + 1) : ℕ) : ℤ) * (X : ℤ) + (-1) * ((p ^ ℓ : ℕ) : ℤ) * (W : ℤ) = 0)
        ↔ p * X = W := by
    intro X W
    push_cast
    constructor
    · intro h1
      have h2 : (p : ℤ) ^ ℓ * ((p : ℤ) * X - W) = 0 := by linear_combination h1
      have h3 : (p : ℤ) * X = W := by
        have := (mul_eq_zero.1 h2).resolve_left hpl
        linarith
      exact_mod_cast h3
    · intro h1
      have h2 : (p : ℤ) * X = W := by exact_mod_cast h1
      linear_combination (p : ℤ) ^ ℓ * h2
  rw [zeroAtW_iff_cntW_aux w (p ^ (ℓ + 1)) (Finset.univ : Finset (Fin 2)) ![p ^ (ℓ + 1), p ^ ℓ]
    ![1, -1] ?_ ?_]
  · refine forall_congr' fun v => ?_
    rw [Fin.sum_univ_two]
    exact key _ _
  · intro i _
    fin_cases i
    · exact h
    · exact hℓ
  · intro e _
    rw [Fin.sum_univ_two]
    exact Pqr.Bridge.indicator_prime_pow hp ℓ e

/-- order a prime power times another prime: the `p × q` arrays of counts are additive -/
theorem zeroAtW_prime_pow_mul (w : ZMod M → ℕ) (p q : ℕ) (hp : p.Prime) (hq : q.Prime)
    (hpq : p ≠ q) (ℓ : ℕ) (h : p ^ (ℓ + 1) * q ∣ M) :
    ZeroAtW w (p ^ (ℓ + 1) * q) ↔ ∀ v : ZMod M,
      p * q * cntW w (p ^ (ℓ + 1) * q) v + cntW w (p ^ ℓ) v
        = q * cntW w (p ^ ℓ * q) v + p * cntW w (p ^ (ℓ + 1)) v := by
  have h1 : p ^ ℓ * q ∣ M := (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ ℓ)) q).trans h
  have h2 : p ^ (ℓ + 1) ∣ M := (dvd_mul_right _ q).trans h
  have h3 : p ^ ℓ ∣ M := (dvd_mul_right _ q).trans h1
  have hpl : (p : ℤ) ^ ℓ ≠ 0 := pow_ne_zero _ (Nat.cast_ne_zero.2 hp.ne_zero)
  have key : ∀ X Y Z W : ℕ,
      ((1 : ℤ) * ((p ^ (ℓ + 1) * q : ℕ) : ℤ) * (X : ℤ) + (-1) * ((p ^ ℓ * q : ℕ) : ℤ) * (Y : ℤ)
          + (-1) * ((p ^ (ℓ + 1) : ℕ) : ℤ) * (Z : ℤ) + 1 * ((p ^ ℓ : ℕ) : ℤ) * (W : ℤ) = 0)
        ↔ p * q * X + W = q * Y + p * Z := by
    intro X Y Z W
    push_cast
    constructor
    · intro h4
      have h5 : (p : ℤ) ^ ℓ * ((p : ℤ) * q * X + W - (q * Y + p * Z)) = 0 := by
        linear_combination h4
      have h6 : (p : ℤ) * q * X + W = q * Y + p * Z := by
        have := (mul_eq_zero.1 h5).resolve_left hpl
        linarith
      exact_mod_cast h6
    · intro h4
      have h5 : (p : ℤ) * q * X + W = q * Y + p * Z := by exact_mod_cast h4
      linear_combination (p : ℤ) ^ ℓ * h5
  rw [zeroAtW_iff_cntW_aux w (p ^ (ℓ + 1) * q) (Finset.univ : Finset (Fin 4))
    ![p ^ (ℓ + 1) * q, p ^ ℓ * q, p ^ (ℓ + 1), p ^ ℓ] ![1, -1, -1, 1] ?_ ?_]
  · refine forall_congr' fun v => ?_
    rw [Fin.sum_univ_four]
    exact key _ _ _ _
  · intro i _
    fin_cases i
    · exact h
    · exact h1
    · exact h2
    · exact h3
  · intro e _
    rw [Fin.sum_univ_four]
    exact Pqr.Bridge.indicator_prime_pow_mul hp hq hpq ℓ e

end WeightedAux

/-- on a set, `ZeroAtW` is `Pqr.ZeroAt` -/
theorem zeroAtW_indW (A : Finset (ZMod M)) (d : ℕ) : ZeroAtW (indW A) d ↔ Pqr.ZeroAt A d := by
  unfold ZeroAtW Pqr.ZeroAt
  simp only [WeightedAux.hatW_indW]

/-- on a set, `maskW` is `Pqr.mask` -/
theorem maskW_indW (A : Finset (ZMod M)) : maskW (indW A) = Pqr.mask A := by
  rw [maskW, Pqr.mask, ← Fintype.sum_ite_mem A]
  refine Finset.sum_congr rfl fun a _ => ?_
  simp only [indW]
  split_ifs <;> simp

/-- For `d ∣ M`: the multiset `w` has no Fourier mass at the frequencies of order `d` iff the cyclotomic
polynomial `Φ_d` divides its mask polynomial. -/
theorem zeroAtW_iff_cyclotomic_dvd (w : ZMod M → ℕ) (d : ℕ) (hd : d ∣ M) :
    ZeroAtW w d ↔ Polynomial.cyclotomic d ℤ ∣ maskW w := by
  have hM : M ≠ 0 := NeZero.ne M
  have hdpos : 0 < d := Nat.pos_of_dvd_of_pos hd (Nat.pos_of_ne_zero hM)
  have hprim := Pqr.isPrimitiveRoot_stdAddChar_div (M := M) hd
  have hord := Pqr.ord_natCast_div' (M := M) hd
  have hcyc := Polynomial.cyclotomic_eq_minpoly hprim hdpos
  have hint : IsIntegral ℤ (ZMod.stdAddChar ((M / d : ℕ) : ZMod M) : ℂ) := hprim.isIntegral hdpos
  rw [hcyc]
  constructor
  · intro h
    have h0 := h _ hord
    rw [WeightedAux.hatW_eq_aeval_maskW] at h0
    exact minpoly.isIntegrallyClosed_dvd hint h0
  · rintro ⟨Q, hQ⟩
    have h0 : hatW w ((M / d : ℕ) : ZMod M) = 0 := by
      rw [WeightedAux.hatW_eq_aeval_maskW, hQ, map_mul, minpoly.aeval, zero_mul]
    have h1 := WeightedAux.zeroAtW_of_hatW_eq_zero w _ h0
    rwa [hord] at h1

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

namespace WeightedAux

open GroupAux

/-! ### On a set -/

theorem subW_indW (A : Finset (ZMod (p ^ n * q))) (k : ℕ) :
    ∀ d r : ℕ, subW (indW A) k d r = sub A k d r := by
  induction k with
  | zero =>
    intro d r
    change Tree.leaf _ = Tree.leaf _
    congr 1
    funext j
    rw [Finset.card_filter, ← Fintype.sum_ite_mem A]
    refine Finset.sum_congr rfl fun a _ => ?_
    simp only [indW]
    split_ifs <;> rfl
  | succ k ih =>
    intro d r
    change Tree.node _ = Tree.node _
    congr 1
    funext c
    exact ih _ _

/-! ### Counts of residue classes, with multiplicity -/

/-- splitting a weighted sum according to the value of a function with values in `[0, m)` -/
theorem sum_ite_fin {α : Type*} [Fintype α] (w : α → ℕ) (P : α → Prop) [DecidablePred P] (f : α → ℕ)
    (m : ℕ) (hf : ∀ a, f a < m) :
    ∑ c : Fin m, ∑ a : α, (if P a ∧ f a = (c : ℕ) then w a else 0)
      = ∑ a : α, if P a then w a else 0 := by
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [Fin.sum_univ_eq_sum_range (fun c => if P a ∧ f a = c then w a else 0) m]
  by_cases hP : P a
  · simp only [hP, true_and]
    rw [Finset.sum_ite_eq]
    simp [hf a]
  · simp [hP]

/-- `N(d, r)`: the number of elements of `w`, with multiplicity, in the class `r` mod `p^d` -/
def cntPW (w : ZMod (p ^ n * q) → ℕ) (d r : ℕ) : ℕ :=
  ∑ a : ZMod (p ^ n * q), if a.val % p ^ d = r then w a else 0

/-- `L(d, r, j)`: the number of elements of `w`, with multiplicity, in the class `r` mod `p^d` and the
class `j` mod `q` -/
def cntPQW (w : ZMod (p ^ n * q) → ℕ) (d r j : ℕ) : ℕ :=
  ∑ a : ZMod (p ^ n * q), if a.val % p ^ d = r ∧ a.val % q = j then w a else 0

theorem cntPQW_succ (w : ZMod (p ^ n * q) → ℕ) (d r j : ℕ) (hr : r < p ^ d) :
    ∑ c : Fin p, cntPQW w (d + 1) (r + (c : ℕ) * p ^ d) j = cntPQW w d r j := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  unfold cntPQW
  rw [← sum_ite_fin w (fun a => a.val % p ^ d = r ∧ a.val % q = j)
    (fun a => a.val / p ^ d % p) p (fun a => Nat.mod_lt _ hp)]
  refine Finset.sum_congr rfl fun c _ => Finset.sum_congr rfl fun a _ => ?_
  refine if_congr ?_ rfl rfl
  rw [mod_pow_succ_eq_iff hr]
  tauto

theorem cntPW_succ (w : ZMod (p ^ n * q) → ℕ) (d r : ℕ) (hr : r < p ^ d) :
    ∑ c : Fin p, cntPW w (d + 1) (r + (c : ℕ) * p ^ d) = cntPW w d r := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  unfold cntPW
  rw [← sum_ite_fin w (fun a => a.val % p ^ d = r)
    (fun a => a.val / p ^ d % p) p (fun a => Nat.mod_lt _ hp)]
  refine Finset.sum_congr rfl fun c _ => Finset.sum_congr rfl fun a _ => ?_
  refine if_congr ?_ rfl rfl
  rw [mod_pow_succ_eq_iff hr]

theorem cntPQW_sum (w : ZMod (p ^ n * q) → ℕ) (d r : ℕ) :
    ∑ j : Fin q, cntPQW w d r j = cntPW w d r := by
  have hq : 0 < q := (Fact.out : q.Prime).pos
  unfold cntPQW cntPW
  exact sum_ite_fin w (fun a => a.val % p ^ d = r) (fun a => a.val % q) q
    (fun a => Nat.mod_lt _ hq)

theorem lay_subW_aux (w : ZMod (p ^ n * q) → ℕ) (k : ℕ) :
    ∀ d r : ℕ, r < p ^ d → ∀ j : Fin q, lay (subW w k d r) j = cntPQW w d r j := by
  induction k with
  | zero => intro d r _ j; rfl
  | succ k ih =>
    intro d r hr j
    rw [← cntPQW_succ w d r j hr]
    change ∑ c : Fin p, lay (subW w k (d + 1) (r + (c : ℕ) * p ^ d)) j = _
    exact Finset.sum_congr rfl fun c _ => ih (d + 1) _ (add_mul_pow_lt hr c.isLt) j

theorem size_subW_aux (w : ZMod (p ^ n * q) → ℕ) (k d r : ℕ) (hr : r < p ^ d) :
    size (subW w k d r) = cntPW w d r := by
  unfold size
  rw [← cntPQW_sum]
  exact Finset.sum_congr rfl fun j _ => lay_subW_aux w k d r hr j

/-- layer counts of a subtree -/
theorem lay_subW (w : ZMod (p ^ n * q) → ℕ) (k d r : ℕ) (hr : r < p ^ d) (j : Fin q) :
    lay (subW w k d r) j
      = ∑ a : ZMod (p ^ n * q), if a.val % p ^ d = r ∧ a.val % q = (j : ℕ) then w a else 0 :=
  lay_subW_aux w k d r hr j

/-- size of a subtree -/
theorem size_subW (w : ZMod (p ^ n * q) → ℕ) (k d r : ℕ) (hr : r < p ^ d) :
    size (subW w k d r) = ∑ a : ZMod (p ^ n * q), if a.val % p ^ d = r then w a else 0 :=
  size_subW_aux w k d r hr

/-- the meaning of `E` for a subtree: equal counts in the `p` classes below each class `r'` at depth `e` -/
theorem E_subW (w : ZMod (p ^ n * q) → ℕ) (m : ℕ) :
    ∀ k d r e : ℕ, m < k → r < p ^ d → e = d + m →
      (E (subW w k d r) (m + 1) ↔ ∀ r', r' < p ^ e → r' % p ^ d = r → ∀ c c' : Fin p,
        cntPW w (e + 1) (r' + (c : ℕ) * p ^ e) = cntPW w (e + 1) (r' + (c' : ℕ) * p ^ e)) := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  induction m with
  | zero =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    obtain rfl : e = d := by omega
    change (∀ c c' : Fin p, size (subW w k (e + 1) (r + (c : ℕ) * p ^ e))
      = size (subW w k (e + 1) (r + (c' : ℕ) * p ^ e))) ↔ _
    have hs : ∀ c : Fin p, size (subW w k (e + 1) (r + (c : ℕ) * p ^ e))
        = cntPW w (e + 1) (r + (c : ℕ) * p ^ e) :=
      fun c => size_subW_aux w k (e + 1) _ (add_mul_pow_lt hr c.isLt)
    simp only [hs]
    constructor
    · intro h r' hr' hmod c c'
      rw [Nat.mod_eq_of_lt hr'] at hmod
      subst hmod
      exact h c c'
    · intro h c c'
      exact h r hr (Nat.mod_eq_of_lt hr) c c'
  | succ m ih =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    change (∀ c : Fin p, E (subW w k (d + 1) (r + (c : ℕ) * p ^ d)) (m + 1)) ↔ _
    refine Iff.trans (forall_congr' fun c =>
      ih k (d + 1) _ e (by omega) (add_mul_pow_lt hr c.isLt) (by omega)) ?_
    exact forall_digit_iff hp hr _

/-- the meaning of `F` for a subtree: additive `p × q` arrays below each class `r'` at depth `e` -/
theorem F_subW (w : ZMod (p ^ n * q) → ℕ) (m : ℕ) :
    ∀ k d r e : ℕ, m < k → r < p ^ d → e = d + m →
      (F (subW w k d r) (m + 1) ↔ ∀ r', r' < p ^ e → r' % p ^ d = r →
        ∀ (c c' : Fin p) (j j' : Fin q),
          cntPQW w (e + 1) (r' + (c : ℕ) * p ^ e) j + cntPQW w (e + 1) (r' + (c' : ℕ) * p ^ e) j'
            = cntPQW w (e + 1) (r' + (c : ℕ) * p ^ e) j'
              + cntPQW w (e + 1) (r' + (c' : ℕ) * p ^ e) j) := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  induction m with
  | zero =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    obtain rfl : e = d := by omega
    change (∀ (c c' : Fin p) (j j' : Fin q),
      lay (subW w k (e + 1) (r + (c : ℕ) * p ^ e)) j + lay (subW w k (e + 1) (r + (c' : ℕ) * p ^ e)) j'
        = lay (subW w k (e + 1) (r + (c : ℕ) * p ^ e)) j'
          + lay (subW w k (e + 1) (r + (c' : ℕ) * p ^ e)) j) ↔ _
    have hs : ∀ (c : Fin p) (j : Fin q), lay (subW w k (e + 1) (r + (c : ℕ) * p ^ e)) j
        = cntPQW w (e + 1) (r + (c : ℕ) * p ^ e) j :=
      fun c j => lay_subW_aux w k (e + 1) _ (add_mul_pow_lt hr c.isLt) j
    simp only [hs]
    constructor
    · intro h r' hr' hmod c c' j j'
      rw [Nat.mod_eq_of_lt hr'] at hmod
      subst hmod
      exact h c c' j j'
    · intro h c c' j j'
      exact h r hr (Nat.mod_eq_of_lt hr) c c' j j'
  | succ m ih =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    change (∀ c : Fin p, F (subW w k (d + 1) (r + (c : ℕ) * p ^ d)) (m + 1)) ↔ _
    refine Iff.trans (forall_congr' fun c =>
      ih k (d + 1) _ e (by omega) (add_mul_pow_lt hr c.isLt) (by omega)) ?_
    exact forall_digit_iff hp hr _

/-! ### Counts `cntW` in terms of residues of representatives -/

theorem cntW_pow (w : ZMod (p ^ n * q) → ℕ) {d : ℕ} (hd : d ≤ n) (v : ZMod (p ^ n * q)) :
    cntW w (p ^ d) v = cntPW w d (v.val % p ^ d) := by
  unfold cntW cntPW
  exact Finset.sum_congr rfl fun a _ => if_congr
    (dvd_val_sub_iff ((pow_dvd_pow p hd).mul_right q) a v) rfl rfl

theorem cntW_pow_mul (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ) {d : ℕ} (hd : d ≤ n)
    (v : ZMod (p ^ n * q)) :
    cntW w (p ^ d * q) v = cntPQW w d (v.val % p ^ d) (v.val % q) := by
  have hcop : Nat.Coprime (p ^ d) q :=
    Nat.Coprime.pow_left d ((Nat.coprime_primes Fact.out Fact.out).2 hpq)
  unfold cntW cntPQW
  refine Finset.sum_congr rfl fun a _ => if_congr ?_ rfl rfl
  rw [dvd_val_sub_iff (Nat.mul_dvd_mul_right (pow_dvd_pow p hd) q) a v]
  exact (Nat.modEq_and_modEq_iff_modEq_mul hcop).symm

theorem cntW_q (w : ZMod (p ^ n * q) → ℕ) (v : ZMod (p ^ n * q)) :
    cntW w q v = ∑ a : ZMod (p ^ n * q), if a.val % q = v.val % q then w a else 0 := by
  unfold cntW
  exact Finset.sum_congr rfl fun a _ => if_congr
    (dvd_val_sub_iff (dvd_mul_left q _) a v) rfl rfl

/-! ### Every tree is the tree of a multiset -/

/-- the entry of the leaf reached by the base-`p` digits of `x`, lowest digit first -/
def entry (hp : 0 < p) : {k : ℕ} → Tree p q k → ℕ → Fin q → ℕ
  | _, .leaf f, _ => f
  | _, .node ch, x => entry hp (ch ⟨x % p, Nat.mod_lt _ hp⟩) (x / p)

/-- Chinese remainder theorem: a sum over the elements with given residues mod `p^n` and mod `q` has
exactly one term. -/
theorem sum_ite_crt (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ) (r j : ℕ) (a₀ : ZMod (p ^ n * q))
    (h₁ : a₀.val % p ^ n = r) (h₂ : a₀.val % q = j) :
    ∑ a : ZMod (p ^ n * q), (if a.val % p ^ n = r ∧ a.val % q = j then w a else 0) = w a₀ := by
  have hcop : Nat.Coprime (p ^ n) q :=
    Nat.Coprime.pow_left n ((Nat.coprime_primes Fact.out Fact.out).2 hpq)
  rw [Finset.sum_eq_single a₀]
  · rw [ite_eq_left ⟨h₁, h₂⟩]
  · intro b _ hb
    refine ite_eq_right fun hb' => hb ?_
    have hmod : b.val ≡ a₀.val [MOD p ^ n * q] :=
      (Nat.modEq_and_modEq_iff_modEq_mul hcop).1 ⟨hb'.1.trans h₁.symm, hb'.2.trans h₂.symm⟩
    exact ZMod.val_injective _ (hmod.eq_of_lt_of_lt (ZMod.val_lt b) (ZMod.val_lt a₀))
  · intro h
    exact absurd (Finset.mem_univ a₀) h

/-- if `w`, on the class `r` mod `p^d`, is read off the tree `s` by the remaining digits, then the part of
`w` in that class is `s` -/
theorem subW_eq (hpq : p ≠ q) (hp0 : 0 < p) (w : ZMod (p ^ n * q) → ℕ) (k : ℕ) :
    ∀ (d r : ℕ) (s : Tree p q k), d + k = n → r < p ^ d →
      (∀ a : ZMod (p ^ n * q), a.val % p ^ d = r → ∀ j : Fin q, a.val % q = (j : ℕ) →
        w a = entry hp0 s (a.val / p ^ d) j) → subW w k d r = s := by
  induction k with
  | zero =>
    intro d r s hd hr h
    have hdn : d = n := by omega
    cases s with
    | leaf f =>
      change Tree.leaf _ = Tree.leaf f
      congr 1
      funext j
      obtain ⟨a₀, h₁, h₂⟩ := exists_val_mod_pow_q hpq (le_of_eq hdn) r (j : ℕ) hr j.isLt
      have h3 := h a₀ h₁ j h₂
      subst hdn
      rw [sum_ite_crt hpq w r j a₀ h₁ h₂, h3]
      rfl
  | succ k ih =>
    intro d r s hd hr h
    cases s with
    | node ch =>
      change Tree.node _ = Tree.node ch
      congr 1
      funext c
      refine ih (d + 1) _ (ch c) (by omega) (add_mul_pow_lt hr c.isLt) ?_
      intro a ha j hj
      obtain ⟨ha1, ha2⟩ := (mod_pow_succ_eq_iff hr).1 ha
      rw [h a ha1 j hj]
      change entry hp0 (ch ⟨a.val / p ^ d % p, Nat.mod_lt _ hp0⟩) (a.val / p ^ d / p) j = _
      have hc : (⟨a.val / p ^ d % p, Nat.mod_lt _ hp0⟩ : Fin p) = c := Fin.ext ha2
      rw [hc, Nat.div_div_eq_div_mul, pow_succ]

end WeightedAux

/-- on a set, `treeOfW` is `treeOf` -/
theorem treeOfW_indW (A : Finset (ZMod (p ^ n * q))) : treeOfW (indW A) = treeOf A := by
  exact WeightedAux.subW_indW A n 0 0

/-- the size of the tree is the number of elements, with multiplicity -/
theorem size_treeOfW (w : ZMod (p ^ n * q) → ℕ) : size (treeOfW w) = ∑ a : ZMod (p ^ n * q), w a := by
  rw [treeOfW, WeightedAux.size_subW w n 0 0 (by simp)]
  simp [Nat.mod_one]

/-- level `ℓ` of `E`, `1 ≤ ℓ ≤ n`: no Fourier mass at order `p^ℓ` -/
theorem E_treeOfW (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    E (treeOfW w) ℓ ↔ ZeroAtW w (p ^ ℓ) := by
  obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
  have hp : p.Prime := Fact.out
  have hm : m ≤ n := by omega
  rw [WeightedAux.zeroAtW_prime_pow w p hp m ((pow_dvd_pow p hn).mul_right q), treeOfW,
    WeightedAux.E_subW w m n 0 0 m (by omega) (by simp) (by simp)]
  simp only [WeightedAux.cntW_pow w hn, WeightedAux.cntW_pow w hm]
  constructor
  · intro h v
    have hr' : v.val % p ^ m < p ^ m := Nat.mod_lt _ (pow_pos hp.pos m)
    rw [← WeightedAux.cntPW_succ w m _ hr', Nat.mod_pow_succ, mul_comm (p ^ m),
      Finset.sum_congr rfl (fun c' _ => h _ hr' (Nat.mod_one _) c'
        ⟨v.val / p ^ m % p, Nat.mod_lt _ hp.pos⟩)]
    simp
  · intro h r' hr' _ c c'
    have key : ∀ c : Fin p,
        p * WeightedAux.cntPW w (m + 1) (r' + (c : ℕ) * p ^ m) = WeightedAux.cntPW w m r' := by
      intro c
      obtain ⟨v, hv⟩ := GroupAux.exists_val_mod_pow (q := q) hn (r' + (c : ℕ) * p ^ m)
        (GroupAux.add_mul_pow_lt hr' c.isLt)
      have hv' : v.val % p ^ m = r' := by
        rw [← Nat.mod_mod_of_dvd v.val (pow_dvd_pow p (Nat.le_succ m)), hv,
          GroupAux.add_mul_pow_mod hr']
      have h2 := h v
      rwa [hv, hv'] at h2
    exact Nat.eq_of_mul_eq_mul_left hp.pos ((key c).trans (key c').symm)

/-- level `0` of `F`: no Fourier mass at order `q` -/
theorem F_treeOfW_zero (w : ZMod (p ^ n * q) → ℕ) : F (treeOfW w) 0 ↔ ZeroAtW w q := by
  have hq : q.Prime := Fact.out
  have h := WeightedAux.zeroAtW_prime_pow w q hq 0
    (by rw [zero_add, pow_one]; exact dvd_mul_left q _)
  simp only [zero_add, pow_one, pow_zero, WeightedAux.cntW_one, WeightedAux.cntW_q] at h
  rw [h, F_zero, treeOfW]
  have hl : ∀ j : Fin q, lay (subW w n 0 0) j
      = ∑ a : ZMod (p ^ n * q), if a.val % q = (j : ℕ) then w a else 0 := by
    intro j
    rw [WeightedAux.lay_subW w n 0 0 (by simp) j]
    simp [Nat.mod_one]
  have hsum : ∑ j : Fin q, (∑ a : ZMod (p ^ n * q), if a.val % q = (j : ℕ) then w a else 0)
      = ∑ a : ZMod (p ^ n * q), w a := by
    have h3 := WeightedAux.sum_ite_fin w (fun _ => True) (fun a => a.val % q) q
      (fun a => Nat.mod_lt _ hq.pos)
    simpa using h3
  simp only [hl]
  constructor
  · intro h2 v
    rw [← hsum, Finset.sum_congr rfl (fun j' _ => h2 j' ⟨v.val % q, Nat.mod_lt _ hq.pos⟩)]
    simp
  · intro h2 j j'
    have key : ∀ j : Fin q,
        q * (∑ a : ZMod (p ^ n * q), if a.val % q = (j : ℕ) then w a else 0)
          = ∑ a : ZMod (p ^ n * q), w a := by
      intro j
      obtain ⟨v, hv⟩ := GroupAux.exists_val_mod_q (p := p) (n := n) (j : ℕ) j.isLt
      have h3 := h2 v
      rwa [hv] at h3
    exact Nat.eq_of_mul_eq_mul_left hq.pos ((key j).trans (key j').symm)

/-- level `ℓ` of `F`, `1 ≤ ℓ ≤ n`: no Fourier mass at order `p^ℓ q` -/
theorem F_treeOfW (hpq : p ≠ q) (w : ZMod (p ^ n * q) → ℕ) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    F (treeOfW w) ℓ ↔ ZeroAtW w (p ^ ℓ * q) := by
  obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hm : m ≤ n := by omega
  rw [WeightedAux.zeroAtW_prime_pow_mul w p q hp hq hpq m
      (Nat.mul_dvd_mul_right (pow_dvd_pow p hn) q),
    treeOfW, WeightedAux.F_subW w m n 0 0 m (by omega) (by simp) (by simp)]
  simp only [WeightedAux.cntW_pow w hn, WeightedAux.cntW_pow w hm, WeightedAux.cntW_pow_mul hpq w hn,
    WeightedAux.cntW_pow_mul hpq w hm]
  -- for one class `r'` mod `p^m`: additivity of the array of the `p × q` classes inside it
  have key : ∀ r', r' < p ^ m →
      ((∀ (c c' : Fin p) (j j' : Fin q),
          WeightedAux.cntPQW w (m + 1) (r' + (c : ℕ) * p ^ m) j
              + WeightedAux.cntPQW w (m + 1) (r' + (c' : ℕ) * p ^ m) j'
            = WeightedAux.cntPQW w (m + 1) (r' + (c : ℕ) * p ^ m) j'
              + WeightedAux.cntPQW w (m + 1) (r' + (c' : ℕ) * p ^ m) j) ↔
        ∀ (c : Fin p) (j : Fin q),
          p * q * WeightedAux.cntPQW w (m + 1) (r' + (c : ℕ) * p ^ m) j + WeightedAux.cntPW w m r'
            = q * WeightedAux.cntPQW w m r' j
              + p * WeightedAux.cntPW w (m + 1) (r' + (c : ℕ) * p ^ m)) := by
    intro r' hr'
    have h2 := GroupAux.additive_iff hp.pos hq.pos
      (fun (c : Fin p) (j : Fin q) => WeightedAux.cntPQW w (m + 1) (r' + (c : ℕ) * p ^ m) j)
    simp only [WeightedAux.cntPQW_sum, WeightedAux.cntPW_succ w m r' hr',
      WeightedAux.cntPQW_succ w m r' _ hr'] at h2
    exact h2
  constructor
  · intro h v
    have hr' : v.val % p ^ m < p ^ m := Nat.mod_lt _ (pow_pos hp.pos m)
    have h2 := (key _ hr').1 (h _ hr' (Nat.mod_one _)) ⟨v.val / p ^ m % p, Nat.mod_lt _ hp.pos⟩
      ⟨v.val % q, Nat.mod_lt _ hq.pos⟩
    rw [Nat.mod_pow_succ, mul_comm (p ^ m)]
    exact h2
  · intro h r' hr' _
    rw [key r' hr']
    intro c j
    obtain ⟨v, hv1, hv2⟩ := GroupAux.exists_val_mod_pow_q hpq hn (r' + (c : ℕ) * p ^ m) (j : ℕ)
      (GroupAux.add_mul_pow_lt hr' c.isLt) j.isLt
    have hv' : v.val % p ^ m = r' := by
      rw [← Nat.mod_mod_of_dvd v.val (pow_dvd_pow p (Nat.le_succ m)), hv1,
        GroupAux.add_mul_pow_mod hr']
    have h2 := h v
    rwa [hv1, hv2, hv'] at h2

/-- every tree is the tree of a multiset on `ZMod (p^n * q)` (the Chinese remainder theorem) -/
theorem treeOfW_surjective (hpq : p ≠ q) :
    Function.Surjective (treeOfW : (ZMod (p ^ n * q) → ℕ) → Tree p q n) := by
  intro t
  have hp : 0 < p := (Fact.out : p.Prime).pos
  have hq : 0 < q := (Fact.out : q.Prime).pos
  refine ⟨fun a => WeightedAux.entry hp t a.val ⟨a.val % q, Nat.mod_lt _ hq⟩, ?_⟩
  refine WeightedAux.subW_eq hpq hp _ n 0 0 t (by omega) (by simp) ?_
  intro a _ j hj
  simp only [pow_zero, Nat.div_one]
  congr 1
  exact Fin.ext hj

end Pnq
