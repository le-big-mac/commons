/-
The statement on signs for every odd `n`: two counts.  S2 (a): a pivot set `J` for the level `i` of `p` bounds the number
of signings bad at `p^i d` by `2^(m - |J|)`.  S4: the signings bad at `1`.
The numbers of signings are cardinalities of the finite sets `badSet e d`; `m` is `Fintype.card ι`.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignSlice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

namespace CountAux

/-- the sign determines the Boolean -/
theorem sg_injective : Function.Injective sg := by
  intro a b h
  cases a <;> cases b <;> simp [sg] at h ⊢

/-- the value of the signed mask at `1` is the sum of the signs -/
theorem eval_one_P (e : ι → ℕ) (ε : ι → Bool) : (P e ε).eval 1 = ∑ k, sg (ε k) := by
  simp [P, Polynomial.eval_finsetSum]

/-- the sum of the signs is twice the number of `true` less the number of elements -/
theorem sum_sg (ε : ι → Bool) :
    ∑ k, sg (ε k) = 2 * ((univ.filter fun k => ε k = true).card : ℤ) - (Fintype.card ι : ℤ) := by
  have h : ∀ k, sg (ε k) = 2 * (if ε k = true then (1 : ℤ) else 0) - 1 := by
    intro k
    cases ε k <;> simp [sg]
  rw [Finset.sum_congr rfl fun k _ => h k, Finset.sum_sub_distrib, ← Finset.mul_sum,
    Finset.sum_boole]
  simp

/-- bad at `1` means that `1` is a root of the signed mask (`Φ_1 = X - 1`): the signs add up to
`0` -/
theorem badAt_one (e : ι → ℕ) (ε : ι → Bool) : BadAt e ε 1 ↔ ∑ k, sg (ε k) = 0 := by
  unfold BadAt
  have hX : (Polynomial.X - 1 : Polynomial ℤ) = Polynomial.X - Polynomial.C 1 := by simp
  rw [Polynomial.cyclotomic_one, hX, Polynomial.dvd_iff_isRoot, Polynomial.IsRoot.def, eval_one_P]

/-- a signing is bad at `1` exactly when half of its signs are `true` -/
theorem mem_badSet_one_iff (e : ι → ℕ) (ε : ι → Bool) :
    ε ∈ badSet e 1 ↔ 2 * (univ.filter fun k => ε k = true).card = Fintype.card ι := by
  rw [mem_badSet, badAt_one, sum_sg]
  omega

/-- **The claim of S2 (a).**  Two signings that are bad at `p^i * d` and agree outside a pivot set
`J` for the level `i` of `p` are equal. -/
theorem eq_of_badAt_of_agree (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i) {d : ℕ}
    (hd : ¬ p ∣ d) {J : Finset ι} (hJ : IsPivot e p i J) {ε ε' : ι → Bool}
    (hε : BadAt e ε (p ^ i * d)) (hε' : BadAt e ε' (p ^ i * d)) (hag : ∀ k, k ∉ J → ε k = ε' k) :
    ε = ε' := by
  have hd0 : d ≠ 0 := by
    rintro rfl
    exact hd (dvd_zero p)
  obtain ⟨η, hη⟩ : ∃ η : ℂ, IsPrimitiveRoot η d := ⟨_, Complex.isPrimitiveRoot_exp d hd0⟩
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
  have h0 : classSum e ε η (p ^ i) (r % p ^ (i - 1) + t * p ^ (i - 1)) =
      classSum e ε' η (p ^ i) (r % p ^ (i - 1) + t * p ^ (i - 1)) := by
    unfold classSum
    refine Finset.sum_congr rfl fun k' _ => ?_
    by_cases hk' : e k' % p ^ i = r % p ^ (i - 1) + t * p ^ (i - 1)
    · have hnot : k' ∉ J := fun hmem => hfree k' hmem hk'
      rw [hag k' hnot]
    · rw [ite_eq_right hk', ite_eq_right hk']
  -- flatness (S0) for both signings
  have h1 := classSum_eq_of_badAt e ε hp hi hd hη hε r (r / p ^ (i - 1)) t htk ht
  have h2 := classSum_eq_of_badAt e ε' hp hi hd hη hε' r (r / p ^ (i - 1)) t htk ht
  rw [hrdec] at h1 h2
  have h3 : classSum e ε η (p ^ i) r = classSum e ε' η (p ^ i) r := by
    rw [h1, h2, h0]
  -- in the class `r` the two signings differ at most at `k`
  have h4 : classSum e ε η (p ^ i) r - classSum e ε' η (p ^ i) r =
      ((sg (ε k) : ℂ) - (sg (ε' k) : ℂ)) * η ^ e k := by
    unfold classSum
    rw [← Finset.sum_sub_distrib, Finset.sum_eq_single k]
    · rw [ite_eq_left hr.symm, ite_eq_left hr.symm, sub_mul]
    · intro k' _ hne
      by_cases hk' : e k' % p ^ i = r
      · have hnot : k' ∉ J := fun hmem => hne (hJ.1 k' hmem k hk (hk'.trans hr))
        rw [hag k' hnot, sub_self]
      · rw [ite_eq_right hk', ite_eq_right hk', sub_self]
    · intro h
      exact absurd (Finset.mem_univ k) h
  have h5 : ((sg (ε k) : ℂ) - (sg (ε' k) : ℂ)) * η ^ e k = 0 := by
    rw [← h4, h3, sub_self]
  have h6 : (sg (ε k) : ℂ) = (sg (ε' k) : ℂ) := by
    rcases mul_eq_zero.mp h5 with h | h
    · exact sub_eq_zero.mp h
    · exact absurd h (pow_ne_zero _ hη0)
  exact sg_injective (Int.cast_injective h6)

end CountAux

/-- **S2 (a) (pivots).**  `p` prime, `i ≥ 1`, `p ∤ d`.  If `J` is a pivot set for the level `i` of `p`, the number of
signings bad at `p^i * d` is at most `2^(m - |J|)`: two such signings that agree outside `J` are equal. -/
theorem card_badSet_mul_two_pow_card_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i) {d : ℕ}
    (hd : ¬ p ∣ d) {J : Finset ι} (hJ : IsPivot e p i J) :
    (badSet e (p ^ i * d)).card * 2 ^ J.card ≤ 2 ^ Fintype.card ι := by
  classical
  -- (bad signing, signing of `J`) ↦ the signing that agrees with the first outside `J` and with
  -- the second on `J`; by the claim this is injective
  have hcard : ((badSet e (p ^ i * d)) ×ˢ (univ : Finset (J → Bool))).card ≤
      (univ : Finset (ι → Bool)).card := by
    refine Finset.card_le_card_of_injOn
      (fun x : (ι → Bool) × (J → Bool) => fun k => if h : k ∈ J then x.2 ⟨k, h⟩ else x.1 k) ?_ ?_
    · intro x _
      exact Finset.mem_coe.mpr (Finset.mem_univ _)
    · rintro ⟨ε, δ⟩ hx ⟨ε', δ'⟩ hx' heq
      rw [Finset.mem_coe, Finset.mem_product, mem_badSet] at hx hx'
      have hfun : ∀ k, (if h : k ∈ J then δ ⟨k, h⟩ else ε k) =
          (if h : k ∈ J then δ' ⟨k, h⟩ else ε' k) := fun k => congrFun heq k
      have hδ : δ = δ' := by
        funext ⟨k, hk⟩
        have h := hfun k
        rw [dite_eq_left hk, dite_eq_left hk] at h
        exact h
      have hε : ε = ε' := by
        refine CountAux.eq_of_badAt_of_agree e hp hi hd hJ hx.1 hx'.1 fun k hk => ?_
        have h := hfun k
        rw [dite_eq_right hk, dite_eq_right hk] at h
        exact h
      rw [hδ, hε]
  rw [Finset.card_product, Finset.card_univ, Finset.card_univ, Fintype.card_fun, Fintype.card_fun,
    Fintype.card_bool, Fintype.card_coe] at hcard
  exact hcard

/-- **S4, first half.**  A signing is bad at `1` exactly when its signs add up to `0`. -/
theorem badAt_one_iff (e : ι → ℕ) (ε : ι → Bool) : BadAt e ε 1 ↔ ∑ k, sg (ε k) = 0 := by
  exact CountAux.badAt_one e ε

/-- **S4, second half.**  The number of signings bad at `1` is `m.choose (m / 2)` if `m` is even and `0` if `m` is
odd. -/
theorem card_badSet_one (e : ι → ℕ) :
    (badSet e 1).card =
      if Even (Fintype.card ι) then (Fintype.card ι).choose (Fintype.card ι / 2) else 0 := by
  classical
  split_ifs with hm
  · -- `m` even: the bad signings correspond to the subsets with `m / 2` elements
    have hch : (Fintype.card ι).choose (Fintype.card ι / 2) =
        (powersetCard (Fintype.card ι / 2) (univ : Finset ι)).card := by
      rw [Finset.card_powersetCard, Finset.card_univ]
    rw [hch]
    refine Finset.card_bij' (fun ε _ => univ.filter fun k => ε k = true)
      (fun s _ => fun k => decide (k ∈ s)) ?_ ?_ ?_ ?_
    · intro ε hε
      rw [CountAux.mem_badSet_one_iff] at hε
      rw [Finset.mem_powersetCard]
      exact ⟨Finset.subset_univ _, by omega⟩
    · intro s hs
      rw [Finset.mem_powersetCard] at hs
      rw [CountAux.mem_badSet_one_iff]
      have hfs : (univ.filter fun k => decide (k ∈ s) = true) = s := by
        ext k
        simp
      rw [hfs, hs.2]
      obtain ⟨c, hc⟩ := hm
      omega
    · intro ε _
      funext k
      simp
    · intro s _
      ext k
      simp
  · -- `m` odd: no signing has sum `0`
    rw [Finset.card_eq_zero, Finset.eq_empty_iff_forall_notMem]
    intro ε hε
    rw [CountAux.mem_badSet_one_iff] at hε
    exact hm ⟨(univ.filter fun k => ε k = true).card, by omega⟩

end Pnq
