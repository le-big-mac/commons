/-
The statement on signs for every `n`: the counts modulo 3.  S2′ (a pivot set `J` for the level `i` of a prime `p ≠ 3`
bounds the number of signings 3-bad at `p^i d` by `2^(m - |J|)`; a live level `i` of `p` costs a factor
`2^((p-1) rank)`) and E1 (the signings 3-bad at `1`: the sum of the signs is divisible by 3; their number is
`(2^m + 2)/3` for even `m` and `(2^m - 2)/3` for odd `m`).
The numbers of signings are cardinalities of the finite sets `bad3Set e d`; `m` is `Fintype.card ι`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenSlice
import Pnq.SignPivot

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

namespace Count3Aux

/-- `2 ≠ 0` in `F3` (characteristic 3) -/
theorem two_ne_zero : (2 : F3) ≠ 0 := by
  intro h
  have h2 : ((2 : ℕ) : F3) = 0 := by exact_mod_cast h
  have h3 := (CharP.cast_eq_zero_iff F3 3 2).mp h2
  omega

/-- the sign, read in `F3`, determines the Boolean (`1 ≠ -1` in `F3`) -/
theorem sg_cast_injective {a b : Bool} (h : (sg a : F3) = (sg b : F3)) : a = b := by
  cases a <;> cases b
  · rfl
  · exfalso
    have h' : ((-1 : ℤ) : F3) = ((1 : ℤ) : F3) := h
    rw [Int.cast_neg, Int.cast_one] at h'
    exact two_ne_zero (by linear_combination -h')
  · exfalso
    have h' : ((1 : ℤ) : F3) = ((-1 : ℤ) : F3) := h
    rw [Int.cast_neg, Int.cast_one] at h'
    exact two_ne_zero (by linear_combination h')
  · rfl

/-- `F3` has a primitive `d`-th root of unity for every `d` that `3` does not divide -/
theorem exists_isPrimitiveRoot {d : ℕ} (h3 : ¬ 3 ∣ d) : ∃ η : F3, IsPrimitiveRoot η d := by
  have : NeZero ((d : ℕ) : F3) := NeZero.of_not_dvd F3 h3
  exact HasEnoughRootsOfUnity.exists_isPrimitiveRoot F3 d

/-- **The claim of S2′.**  Two signings that are 3-bad at `p^i * d` and agree outside a pivot set `J` for the level
`i` of `p` are equal. -/
theorem eq_of_bad3_of_agree (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ} (hi : 1 ≤ i)
    {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) {J : Finset ι} (hJ : IsPivot e p i J) {ε ε' : ι → Bool}
    (hε : Bad3 e ε (p ^ i * d)) (hε' : Bad3 e ε' (p ^ i * d)) (hag : ∀ k, k ∉ J → ε k = ε' k) :
    ε = ε' := by
  have hd0 : d ≠ 0 := by
    rintro rfl
    exact hd (dvd_zero p)
  obtain ⟨η, hη⟩ : ∃ η : F3, IsPrimitiveRoot η d := exists_isPrimitiveRoot h3
  have hη0 : η ≠ 0 := hη.ne_zero hd0
  funext k
  by_cases hk : k ∈ J
  swap
  · exact hag k hk
  -- the class `r` of `k` modulo `p^i`, written as `r % p^(i-1) + (r / p^(i-1)) * p^(i-1)`
  have hpow : p ^ i = p ^ (i - 1) * p := by
    rw [← pow_succ, Nat.sub_add_cancel hi]
  have hMpos : 0 < p ^ i := pow_pos hp.pos _
  obtain ⟨r, hr⟩ : ∃ r, r = e k % p ^ i := ⟨_, rfl⟩
  have hrlt : r < p ^ (i - 1) * p := by
    rw [hr, ← hpow]
    exact Nat.mod_lt _ hMpos
  have htk : r / p ^ (i - 1) < p := Nat.div_lt_of_lt_mul hrlt
  have hrdec : r % p ^ (i - 1) + r / p ^ (i - 1) * p ^ (i - 1) = r := by
    rw [mul_comm]
    exact Nat.mod_add_div r (p ^ (i - 1))
  -- a class of the same group that holds no element of `J`
  obtain ⟨t, ht, hfree⟩ := hJ.2 r
  have h0 : classSum3 e ε η (p ^ i) (r % p ^ (i - 1) + t * p ^ (i - 1)) =
      classSum3 e ε' η (p ^ i) (r % p ^ (i - 1) + t * p ^ (i - 1)) := by
    unfold classSum3
    refine Finset.sum_congr rfl fun k' _ => ?_
    by_cases hk' : e k' % p ^ i = r % p ^ (i - 1) + t * p ^ (i - 1)
    · have hnot : k' ∉ J := fun hmem => hfree k' hmem hk'
      rw [hag k' hnot]
    · rw [ite_eq_right hk', ite_eq_right hk']
  -- flatness modulo 3 (S0′) for both signings
  have h1 := classSum3_eq_of_bad3 e ε hp hp3 hi hd h3 hη hε r (r / p ^ (i - 1)) t htk ht
  have h2 := classSum3_eq_of_bad3 e ε' hp hp3 hi hd h3 hη hε' r (r / p ^ (i - 1)) t htk ht
  rw [hrdec] at h1 h2
  have h3' : classSum3 e ε η (p ^ i) r = classSum3 e ε' η (p ^ i) r := by
    rw [h1, h2, h0]
  -- in the class `r` the two signings differ at most at `k`
  have h4 : classSum3 e ε η (p ^ i) r - classSum3 e ε' η (p ^ i) r =
      ((sg (ε k) : F3) - (sg (ε' k) : F3)) * η ^ e k := by
    unfold classSum3
    rw [← Finset.sum_sub_distrib, Finset.sum_eq_single k]
    · rw [ite_eq_left hr.symm, ite_eq_left hr.symm, sub_mul]
    · intro k' _ hne
      by_cases hk' : e k' % p ^ i = r
      · have hnot : k' ∉ J := fun hmem => hne (hJ.1 k' hmem k hk (hk'.trans hr))
        rw [hag k' hnot, sub_self]
      · rw [ite_eq_right hk', ite_eq_right hk', sub_self]
    · intro h
      exact absurd (Finset.mem_univ k) h
  have h5 : ((sg (ε k) : F3) - (sg (ε' k) : F3)) * η ^ e k = 0 := by
    rw [← h4, h3', sub_self]
  have h6 : (sg (ε k) : F3) = (sg (ε' k) : F3) := by
    rcases mul_eq_zero.mp h5 with h | h
    · exact sub_eq_zero.mp h
    · exact absurd h (pow_ne_zero _ hη0)
  exact sg_cast_injective h6

/-- the value at `1` of the signed mask in `F3` is the sum of the signs -/
theorem val3_one (e : ι → ℕ) (ε : ι → Bool) : val3 e ε 1 = ((∑ k, sg (ε k) : ℤ) : F3) := by
  unfold val3
  rw [Int.cast_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [one_pow, mul_one]

/-- 3-bad at `1` means that the signed mask vanishes at `1` (the only primitive first root of unity) -/
theorem bad3_one (e : ι → ℕ) (ε : ι → Bool) : Bad3 e ε 1 ↔ val3 e ε 1 = 0 := by
  constructor
  · intro h
    exact h 1 IsPrimitiveRoot.one
  · intro h ζ hζ
    rw [IsPrimitiveRoot.one_right_iff] at hζ
    rw [hζ]
    exact h

/-- the number of signings of `m` elements whose signs add up to `r` modulo 3 -/
def cnt (m : ℕ) (r : ZMod 3) : ℕ :=
  (univ.filter fun ε : Fin m → Bool => ((∑ k, sg (ε k) : ℤ) : ZMod 3) = r).card

/-- no element: the empty sum is `0` -/
theorem cnt_zero (r : ZMod 3) : cnt 0 r = if r = 0 then 1 else 0 := by
  unfold cnt
  rw [Finset.card_filter, Finset.univ_unique, Finset.sum_singleton, Finset.univ_eq_empty,
    Finset.sum_empty, Int.cast_zero]
  by_cases hr : r = 0
  · rw [ite_eq_left hr, ite_eq_left hr.symm]
  · rw [ite_eq_right hr, ite_eq_right (Ne.symm hr)]

/-- split off the first sign: it is `+` (the others add up to `r - 1`) or `-` (they add up to `r + 1`) -/
theorem cnt_succ (m : ℕ) (r : ZMod 3) : cnt (m + 1) r = cnt m (r - 1) + cnt m (r + 1) := by
  unfold cnt
  rw [Finset.card_filter, Finset.card_filter, Finset.card_filter,
    ← (Fin.consEquiv fun _ : Fin (m + 1) => Bool).sum_comp, Fintype.sum_prod_type, Fintype.sum_bool]
  congr 1
  · refine Finset.sum_congr rfl fun δ _ => ?_
    have hiff : (((∑ k, sg ((Fin.consEquiv fun _ : Fin (m + 1) => Bool) (true, δ) k) : ℤ) : ZMod 3) = r) ↔
        (((∑ k, sg (δ k) : ℤ) : ZMod 3) = r - 1) := by
      rw [Fin.consEquiv_apply, Fin.sum_univ_succ]
      simp only [Fin.cons_zero, Fin.cons_succ]
      have h1 : sg true = 1 := rfl
      rw [h1, Int.cast_add, Int.cast_one, eq_sub_iff_add_eq']
    rw [if_congr hiff rfl rfl]
  · refine Finset.sum_congr rfl fun δ _ => ?_
    have hiff : (((∑ k, sg ((Fin.consEquiv fun _ : Fin (m + 1) => Bool) (false, δ) k) : ℤ) : ZMod 3) = r) ↔
        (((∑ k, sg (δ k) : ℤ) : ZMod 3) = r + 1) := by
      rw [Fin.consEquiv_apply, Fin.sum_univ_succ]
      simp only [Fin.cons_zero, Fin.cons_succ]
      have h1 : sg false = -1 := rfl
      rw [h1, Int.cast_add, Int.cast_neg, Int.cast_one, neg_add_eq_iff_eq_add, add_comm]
    rw [if_congr hiff rfl rfl]

/-- the three counts: `3 * cnt m r = 2^m + (-1)^m * 2` for `r = 0` and `2^m - (-1)^m` for `r ≠ 0` -/
theorem three_mul_cnt (m : ℕ) :
    ∀ r : ZMod 3, 3 * (cnt m r : ℤ) = 2 ^ m + (-1) ^ m * (if r = 0 then 2 else -1) := by
  induction m with
  | zero =>
    intro r
    rw [cnt_zero]
    by_cases hr : r = 0
    · rw [ite_eq_left hr, ite_eq_left hr]
      norm_num
    · rw [ite_eq_right hr, ite_eq_right hr]
      norm_num
  | succ m ih =>
    intro r
    have hf : (if r - 1 = 0 then (2 : ℤ) else -1) + (if r + 1 = 0 then (2 : ℤ) else -1) =
        -(if r = 0 then (2 : ℤ) else -1) := by
      revert r
      decide
    rw [cnt_succ, Nat.cast_add, mul_add, ih, ih, pow_succ, pow_succ]
    linear_combination ((-1 : ℤ) ^ m) * hf

/-- the number of signings of `ι` whose signs add up to a multiple of 3 is `cnt m 0` -/
theorem card_filter_dvd [DecidableEq ι] :
    (univ.filter fun ε : ι → Bool => (3 : ℤ) ∣ ∑ k, sg (ε k)).card = cnt (Fintype.card ι) 0 := by
  unfold cnt
  refine Finset.card_equiv ((Fintype.equivFin ι).arrowCongr (Equiv.refl Bool)) fun ε => ?_
  rw [Finset.mem_filter, Finset.mem_filter, ZMod.intCast_zmod_eq_zero_iff_dvd]
  have hsum : ∑ k, sg (((Fintype.equivFin ι).arrowCongr (Equiv.refl Bool)) ε k) = ∑ k, sg (ε k) :=
    Equiv.sum_comp (Fintype.equivFin ι).symm fun k => sg (ε k)
  rw [hsum]
  simp

end Count3Aux

/-- **S2′, with a pivot set.**  `p` prime, `p ≠ 3` (`p = 2` allowed), `i ≥ 1`, `p ∤ d`, `3 ∤ d`.  If `J` is a pivot set
for the level `i` of `p`, the number of signings 3-bad at `p^i * d` is at most `2^(m - |J|)`. -/
theorem card_bad3Set_mul_two_pow_card_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) {J : Finset ι} (hJ : IsPivot e p i J) :
    (bad3Set e (p ^ i * d)).card * 2 ^ J.card ≤ 2 ^ Fintype.card ι := by
  classical
  -- (3-bad signing, signing of `J`) ↦ the signing that agrees with the first outside `J` and with
  -- the second on `J`; by the claim this is injective
  have hcard : ((bad3Set e (p ^ i * d)) ×ˢ (univ : Finset (J → Bool))).card ≤
      (univ : Finset (ι → Bool)).card := by
    refine Finset.card_le_card_of_injOn
      (fun x : (ι → Bool) × (J → Bool) => fun k => if h : k ∈ J then x.2 ⟨k, h⟩ else x.1 k) ?_ ?_
    · intro x _
      exact Finset.mem_coe.mpr (Finset.mem_univ _)
    · rintro ⟨ε, δ⟩ hx ⟨ε', δ'⟩ hx' heq
      rw [Finset.mem_coe, Finset.mem_product, mem_bad3Set] at hx hx'
      have hfun : ∀ k, (if h : k ∈ J then δ ⟨k, h⟩ else ε k) =
          (if h : k ∈ J then δ' ⟨k, h⟩ else ε' k) := fun k => congrFun heq k
      have hδ : δ = δ' := by
        funext ⟨k, hk⟩
        have h := hfun k
        rw [dite_eq_left hk, dite_eq_left hk] at h
        exact h
      have hε : ε = ε' := by
        refine Count3Aux.eq_of_bad3_of_agree e hp hp3 hi hd h3 hJ hx.1 hx'.1 fun k hk => ?_
        have h := hfun k
        rw [dite_eq_right hk, dite_eq_right hk] at h
        exact h
      rw [hδ, hε]
  rw [Finset.card_product, Finset.card_univ, Finset.card_univ, Fintype.card_fun, Fintype.card_fun,
    Fintype.card_bool, Fintype.card_coe] at hcard
  exact hcard

/-- **S2′, with the rank (what a live level costs modulo 3).**  `p` prime, `p ≠ 3`, `i ≥ 1`, `p ∤ d`, `3 ∤ d`, the
level `i` of `p` live.  Then `#{ε 3-bad at p^i * d} * 2^((p - 1) * rank e p i) ≤ 2^m`. -/
theorem card_bad3Set_mul_two_pow_rank_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) (hlive : live e p i = true) :
    (bad3Set e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i) ≤ 2 ^ Fintype.card ι := by
  obtain ⟨J, hJ, hcard⟩ := exists_isPivot e hp hi hlive
  calc (bad3Set e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i)
      ≤ (bad3Set e (p ^ i * d)).card * 2 ^ J.card :=
        Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by norm_num) hcard)
    _ ≤ 2 ^ Fintype.card ι := card_bad3Set_mul_two_pow_card_le e hp hp3 hi hd h3 hJ

/-- **E1, first half.**  A signing is 3-bad at `1` exactly when the integer sum of its signs is divisible by 3. -/
theorem bad3_one_iff (e : ι → ℕ) (ε : ι → Bool) : Bad3 e ε 1 ↔ (3 : ℤ) ∣ ∑ k, sg (ε k) := by
  rw [Count3Aux.bad3_one, Count3Aux.val3_one, CharP.intCast_eq_zero_iff F3 3]
  rfl

/-- **E1, second half.**  Three times the number of signings 3-bad at `1` is `2^m + 2` if `m` is even and `2^m - 2`
if `m` is odd (written without subtraction). -/
theorem card_bad3Set_one (e : ι → ℕ) :
    3 * (bad3Set e 1).card + (if Even (Fintype.card ι) then 0 else 2) =
      2 ^ Fintype.card ι + (if Even (Fintype.card ι) then 2 else 0) := by
  classical
  have hset : bad3Set e 1 = univ.filter fun ε : ι → Bool => (3 : ℤ) ∣ ∑ k, sg (ε k) := by
    ext ε
    rw [mem_bad3Set, bad3_one_iff, Finset.mem_filter]
    simp
  have h := Count3Aux.three_mul_cnt (Fintype.card ι) 0
  rw [← Count3Aux.card_filter_dvd, ← hset, ite_eq_left rfl] at h
  by_cases hm : Even (Fintype.card ι)
  · rw [ite_eq_left hm, ite_eq_left hm]
    rw [hm.neg_one_pow] at h
    have h' : (3 : ℤ) * ((bad3Set e 1).card : ℤ) + 0 = ((2 ^ Fintype.card ι + 2 : ℕ) : ℤ) := by
      push_cast
      linear_combination h
    exact_mod_cast h'
  · rw [ite_eq_right hm, ite_eq_right hm]
    rw [(Nat.not_even_iff_odd.mp hm).neg_one_pow] at h
    have h' : (3 : ℤ) * ((bad3Set e 1).card : ℤ) + 2 = ((2 ^ Fintype.card ι + 0 : ℕ) : ℤ) := by
      push_cast
      linear_combination h
    exact_mod_cast h'

end Pnq
