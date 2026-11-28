/-
The first statements about SHARES of bad signings: at one divisor, on moduli that are powers of 2, and on every
modulus with the number of divisors of its odd part.  (Statements fixed on 28 November 2026, before any Lean proof of
them.  `P`, `BadAt` are from `Pnq/SignDefs.lean`; "twice" for the whole of `Z_n` is `card_exists_badAt_le` of
`Pnq/EvenWhole.lean`; Erdős's bound is in `Pnq/Offord.lean`.)
(Corrected on 28 November 2026, after the proofs: "the first statements about SHARES" above is wrong.  The shared
library has had counts of the signings that are bad at ONE divisor since 27 November: `card_badSet_one`,
`card_badSet_mul_two_pow_rank_le`, `card_badSet_three_pow_mul_le`.  The statements below are the first that bound by
a number how many signings are bad at SOME divisor of the modulus, and the first bound at one divisor that holds
for every multiset and every `d ≥ 1`.  Only this comment was changed; the statements and the proofs are as checked.)
-/
import Mathlib
import Pnq.Offord
import Pnq.EvenWhole

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

/-! Lemmas for the proofs of the five statements below, in the namespace `Pnq.OffordBadAux`. -/

namespace OffordBadAux

/-- a signing that is bad at `d ≠ 0` has signed sum `0` of the values `(eta d) ^ e k`, where `eta d`
is the root of unity of order `d` of `Pnq.WholeAux` -/
theorem sum_eq_zero_of_badAt (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (hd : d ≠ 0) (hbad : BadAt e ε d) :
    ∑ k, (sg (ε k) : ℂ) * WholeAux.eta d ^ e k = 0 := by
  have h1 := SliceAux.aeval_eq_zero_of_badAt e ε (Nat.pos_of_ne_zero hd) hbad
    (WholeAux.eta_isPrimitiveRoot hd)
  rw [← h1]
  unfold P
  rw [map_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [map_mul, Polynomial.aeval_C, map_pow, Polynomial.aeval_X, eq_intCast]

/-- the value of the signed mask at `1` is the sum of the signs -/
theorem eval_one_P (e : ι → ℕ) (ε : ι → Bool) : (P e ε).eval 1 = ∑ k, sg (ε k) := by
  unfold P
  rw [Polynomial.eval_finsetSum]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow, Polynomial.eval_X, one_pow,
    mul_one]

/-- a sign is `1` modulo 2 -/
theorem sg_cast_zmod_two (b : Bool) : ((sg b : ℤ) : ZMod 2) = 1 := by
  cases b
  · unfold sg
    rw [ite_eq_right (by simp), Int.cast_neg, Int.cast_one]
    decide
  · unfold sg
    rw [ite_eq_left rfl, Int.cast_one]

/-- the sum of an odd number of signs is not `0` -/
theorem sum_sg_ne_zero (hm : Odd (Fintype.card ι)) (ε : ι → Bool) : ∑ k, sg (ε k) ≠ 0 := by
  intro h
  have h2 : ((∑ k, sg (ε k) : ℤ) : ZMod 2) = (Fintype.card ι : ZMod 2) := by
    rw [Int.cast_sum, Finset.sum_congr rfl fun k _ => sg_cast_zmod_two (ε k), Finset.sum_const,
      Finset.card_univ, nsmul_eq_mul, mul_one]
  rw [h, Int.cast_zero] at h2
  have h3 : (Fintype.card ι : ZMod 2) = 1 := (ZMod.natCast_eq_one_iff_odd).mpr hm
  rw [h3] at h2
  exact zero_ne_one h2

open Classical in
/-- the signings that are bad at some divisor of `1` are those bad at `1` -/
theorem filter_dvd_one (e : ι → ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 1 ∧ BadAt e ε d) =
      Finset.univ.filter fun ε : ι → Bool => BadAt e ε 1 := by
  ext ε
  simp only [Finset.mem_filter, Finset.mem_univ, true_and, Nat.dvd_one]
  constructor
  · rintro ⟨d, rfl, hb⟩
    exact hb
  · intro hb
    exact ⟨1, rfl, hb⟩

open Classical in
/-- "twice" for a power of 2: the signings that are bad at some divisor of `2 ^ k` number at most
twice those that are bad at `1` -/
theorem card_two_pow_le (e : ι → ℕ) (k : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => BadAt e ε 1).card := by
  have h := card_exists_badAt_le e k (n' := 1) (by norm_num)
  rw [mul_one, filter_dvd_one] at h
  exact h

open Classical in
/-- if some signing is bad at some divisor of `2 ^ k`, then some signing is bad at `1` -/
theorem exists_badAt_one_of_two_pow (e : ι → ℕ) (k : ℕ) (ε : ι → Bool)
    (hε : ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d) : ∃ ε' : ι → Bool, BadAt e ε' 1 := by
  have h := card_two_pow_le e k
  have hpos : 0 < (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d).card :=
    Finset.card_pos.mpr ⟨ε, Finset.mem_filter.mpr ⟨Finset.mem_univ ε, hε⟩⟩
  have hpos1 : 0 < (Finset.univ.filter fun ε : ι → Bool => BadAt e ε 1).card := by
    by_contra h0
    rw [Nat.not_lt, Nat.le_zero] at h0
    rw [h0, mul_zero] at h
    exact absurd hpos (Nat.not_lt.mpr h)
  obtain ⟨ε', hε'⟩ := Finset.card_pos.mp hpos1
  exact ⟨ε', (Finset.mem_filter.mp hε').2⟩

open Classical in
/-- the signings that are bad at some divisor of `n' ≠ 0` number at most the sum, over the divisors
`d` of `n'`, of the numbers of the signings that are bad at `d` -/
theorem card_exists_dvd_le_sum (e : ι → ℕ) {n' : ℕ} (hn0 : n' ≠ 0) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ n' ∧ BadAt e ε d).card ≤
      ∑ d ∈ n'.divisors, (Finset.univ.filter fun ε : ι → Bool => BadAt e ε d).card := by
  refine le_trans (Finset.card_le_card ?_) Finset.card_biUnion_le
  intro ε hε
  simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_biUnion,
    Nat.mem_divisors] at hε ⊢
  obtain ⟨d, hd, hb⟩ := hε
  exact ⟨d, ⟨hd, hn0⟩, hb⟩

end OffordBadAux

open Classical in
/-- **One divisor.**  For `d ≠ 0`, the signings that are bad at `d` number at most `C(m, ⌊m/2⌋)`, where `m` is the
number of elements. -/
theorem card_badAt_le_choose (e : ι → ℕ) {d : ℕ} (hd : d ≠ 0) :
    (Finset.univ.filter fun ε : ι → Bool => BadAt e ε d).card ≤
      (Fintype.card ι).choose (Fintype.card ι / 2) := by
  refine le_trans (Finset.card_le_card ?_)
    (card_signedSum_eq_le_complex (fun k => WholeAux.eta d ^ e k)
      (fun k => pow_ne_zero _ ((WholeAux.eta_isPrimitiveRoot hd).ne_zero hd)) 0)
  intro ε hε
  simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε ⊢
  exact OffordBadAux.sum_eq_zero_of_badAt e ε hd hε

/-- **An odd number of elements is never bad at 1.** -/
theorem not_badAt_one_of_odd (e : ι → ℕ) (hm : Odd (Fintype.card ι)) (ε : ι → Bool) :
    ¬ BadAt e ε 1 := by
  intro h
  unfold BadAt at h
  rw [Polynomial.cyclotomic_one] at h
  obtain ⟨Q, hQ⟩ := h
  have h1 : (P e ε).eval 1 = 0 := by
    rw [hQ, Polynomial.eval_mul, Polynomial.eval_sub, Polynomial.eval_X, Polynomial.eval_one,
      sub_self, zero_mul]
  rw [OffordBadAux.eval_one_P] at h1
  exact OffordBadAux.sum_sg_ne_zero hm ε h1

open Classical in
/-- **Moduli that are powers of 2.**  The signings that are bad at some divisor of `2^k` number at most
`2 * C(m, ⌊m/2⌋)`. -/
theorem card_exists_badAt_two_pow_le (e : ι → ℕ) (k : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d).card ≤
      2 * (Fintype.card ι).choose (Fintype.card ι / 2) := by
  exact (OffordBadAux.card_two_pow_le e k).trans
    (Nat.mul_le_mul_left 2 (card_badAt_le_choose e one_ne_zero))

/-- **Moduli that are powers of 2, an odd number of elements: every signing is good.** -/
theorem not_exists_badAt_two_pow_of_odd (e : ι → ℕ) (k : ℕ) (hm : Odd (Fintype.card ι)) (ε : ι → Bool) :
    ¬ ∃ d, d ∣ 2 ^ k ∧ BadAt e ε d := by
  intro hε
  obtain ⟨ε', hε'⟩ := OffordBadAux.exists_badAt_one_of_two_pow e k ε hε
  exact not_badAt_one_of_odd e hm ε' hε'

open Classical in
/-- **Every modulus, with the number of divisors of its odd part.**  `n'` odd.  The signings that are bad at some
divisor of `2^k * n'` number at most `2 * (d(n') * C(m, ⌊m/2⌋))`, where `d(n')` is the number of divisors of `n'`. -/
theorem card_exists_badAt_le_divisors (e : ι → ℕ) (k : ℕ) {n' : ℕ} (hn' : ¬ 2 ∣ n') :
    (Finset.univ.filter fun ε : ι → Bool => ∃ d, d ∣ 2 ^ k * n' ∧ BadAt e ε d).card ≤
      2 * (n'.divisors.card * (Fintype.card ι).choose (Fintype.card ι / 2)) := by
  have hn0 : n' ≠ 0 := fun h => hn' (h ▸ dvd_zero 2)
  refine (card_exists_badAt_le e k hn').trans (Nat.mul_le_mul_left 2 ?_)
  refine (OffordBadAux.card_exists_dvd_le_sum e hn0).trans ?_
  refine (Finset.sum_le_card_nsmul _ _ _ fun d hd => ?_).trans (le_of_eq (smul_eq_mul _ _))
  exact card_badAt_le_choose e (Nat.pos_of_mem_divisors hd).ne'

end Pnq
