/-
The statement on signs for every `n`: part L, the ladder of the prime 2 modulo 3.  For `d` prime to 6, the signings
that are 3-bad at `2^j d` for some `j ≤ K` number at most twice those 3-bad at `d`.  From S0′ with `p = 2`
(`classSum3_eq_of_bad3` of `Pnq/EvenSlice.lean`) and T (`card_exists_levelBad_le` of `Pnq/EvenTwice.lean`), with `V`
the functions from the primitive `d`-th roots of unity of `F3` to `F3`, `pos = e` and `val k = fun η => η ^ e k`.
(Statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.EvenSlice
import Pnq.EvenTwice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

namespace LadderAux

/-- the values of T for the ladder: the element `k` has the value `η ↦ η ^ e k`, a function on the primitive `d`-th
roots of unity of `F3` -/
noncomputable def val (e : ι → ℕ) (d : ℕ) (k : ι) : {η : F3 // IsPrimitiveRoot η d} → F3 :=
  fun η => η.val ^ e k

/-- the signed sum of all the values, at the primitive `d`-th root `η`, is `val3 e ε η` -/
theorem sum_apply (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) (η : {η : F3 // IsPrimitiveRoot η d}) :
    (∑ k, sg (ε k) • val e d k) η = val3 e ε η.val := by
  simp [val, val3, Finset.sum_apply, zsmul_eq_mul]

/-- the class sum `csum` of T, at the primitive `d`-th root `η`, is `classSum3 e ε η` -/
theorem csum_apply (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) (M r : ℕ) (η : {η : F3 // IsPrimitiveRoot η d}) :
    csum e (val e d) ε M r η = classSum3 e ε η.val M r := by
  simp only [csum, classSum3, Finset.sum_apply]
  refine Finset.sum_congr rfl fun k _ => ?_
  split_ifs <;> simp [val, zsmul_eq_mul]

/-- level `0` of T, for these values, is bad exactly when the signing is 3-bad at `d` -/
theorem levelBad_zero_iff (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) :
    levelBad e (val e d) ε 0 ↔ Bad3 e ε d := by
  rw [levelBad_zero]
  constructor
  · intro h ζ hζ
    have h1 := congrFun h ⟨ζ, hζ⟩
    rw [sum_apply] at h1
    exact h1
  · intro h
    funext η
    rw [sum_apply]
    exact h η.val η.property

/-- a signing that is 3-bad at `2 ^ (j + 1) * d` has level `j + 1` of T bad: S0′ with `p = 2`, `i = j + 1`, `c = r`,
`t = 0`, `t' = 1`, at every primitive `d`-th root -/
theorem levelBad_succ_of_bad3 (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (hd : ¬ 2 ∣ d) (h3 : ¬ 3 ∣ d) (j : ℕ)
    (hbad : Bad3 e ε (2 ^ (j + 1) * d)) : levelBad e (val e d) ε (j + 1) := by
  rw [levelBad_succ]
  intro r hr
  funext η
  have h := classSum3_eq_of_bad3 e ε Nat.prime_two (by norm_num) (i := j + 1) (by omega) hd h3
    η.property hbad r 0 1 (by norm_num) (by norm_num)
  rw [Nat.add_sub_cancel, Nat.mod_eq_of_lt hr, zero_mul, add_zero, one_mul] at h
  rw [csum_apply, csum_apply]
  exact h

end LadderAux

open Classical in
/-- **L (the ladder, modulo 3).**  `d` odd (so `d ≥ 1`), `3 ∤ d`.  For every `K`, the number of signings that are
3-bad at `2^j * d` for some `j ≤ K` is at most twice the number of signings 3-bad at `d`. -/
theorem card_exists_bad3_le (e : ι → ℕ) {d : ℕ} (hd : ¬ 2 ∣ d) (h3 : ¬ 3 ∣ d) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ Bad3 e ε (2 ^ j * d)).card ≤
      2 * (bad3Set e d).card := by
  have hT := card_exists_levelBad_le e (LadderAux.val e d) K
  refine le_trans (Finset.card_le_card ?_) (le_trans hT ?_)
  · intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε ⊢
    obtain ⟨j, hj, hb⟩ := hε
    refine ⟨j, hj, ?_⟩
    cases j with
    | zero =>
      rw [pow_zero, one_mul] at hb
      exact (LadderAux.levelBad_zero_iff e ε d).mpr hb
    | succ j => exact LadderAux.levelBad_succ_of_bad3 e ε hd h3 j hb
  · refine Nat.mul_le_mul_left 2 (Finset.card_le_card ?_)
    intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε
    exact (mem_bad3Set e d ε).mpr ((LadderAux.levelBad_zero_iff e ε d).mp hε)

end Pnq
