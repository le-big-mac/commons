import Pnq.SignFinal
import Pnq.LiftAll
/-! Audit: small facts, proved in Lean, about how the ten definitions and the fifteen statements are to be read;
instances that show that no hypothesis is contradictory; and the steps "the parts fit" that are one line.
Nothing here is used by anything else.  The fifteen theorems are `sorry` in this copy, so everything that uses one of
them depends on `sorryAx`; the reading lemmas of the first part use none of them (see the `#print axioms` at the end). -/
open Finset

namespace AuditSigns
open Pnq

/-! ### `sg`, `P`, `BadAt`, `classSum`: reading lemmas (none of them uses a statement of the skeleton) -/

example : sg true = 1 := rfl
example : sg false = -1 := rfl

section
variable {ι : Type*} [Fintype ι]

/-- the coefficient of `X^j` in the signed mask is the sum of the signs of the elements with exponent `j` -/
theorem P_coeff (e : ι → ℕ) (ε : ι → Bool) (j : ℕ) :
    (P e ε).coeff j = ∑ k, if e k = j then sg (ε k) else 0 := by
  unfold P
  rw [Polynomial.finsetSum_coeff]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [Polynomial.coeff_C_mul, Polynomial.coeff_X_pow]
  by_cases h : e k = j
  · subst h; simp
  · have h' : ¬ j = e k := fun hh => h hh.symm
    simp [h, h']

/-- the value of the signed mask at `1` is the sum of the signs -/
theorem P_eval_one (e : ι → ℕ) (ε : ι → Bool) : (P e ε).eval 1 = ∑ k, sg (ε k) := by
  unfold P
  rw [Polynomial.eval_finsetSum]
  simp

/-- the value of the signed mask at a complex number -/
theorem P_aeval (e : ι → ℕ) (ε : ι → Bool) (z : ℂ) :
    Polynomial.aeval z (P e ε) = ∑ k, (sg (ε k) : ℂ) * z ^ e k := by
  unfold P
  rw [map_sum]
  refine Finset.sum_congr rfl fun k _ => ?_
  simp

/-- the class sums modulo `M` of all classes add up to the value of the signed mask at `η` -/
theorem sum_classSum (e : ι → ℕ) (ε : ι → Bool) (η : ℂ) {M : ℕ} (hM : 0 < M) :
    ∑ r ∈ Finset.range M, classSum e ε η M r = Polynomial.aeval η (P e ε) := by
  rw [P_aeval]
  unfold classSum
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [Finset.sum_ite_eq]
  simp [Nat.mod_lt _ hM]

/-- a class `r ≥ M` holds nothing: its class sum is `0` -/
theorem classSum_of_le (e : ι → ℕ) (ε : ι → Bool) (η : ℂ) {M r : ℕ} (hM : 0 < M) (hr : M ≤ r) :
    classSum e ε η M r = 0 := by
  unfold classSum
  refine Finset.sum_eq_zero fun k _ => ?_
  have := Nat.mod_lt (e k) hM
  exact if_neg (by omega)

/-- `cyclotomic 0 ℤ = 1`: every signing is "bad at 0" -/
theorem badAt_zero (e : ι → ℕ) (ε : ι → Bool) : BadAt e ε 0 := by
  unfold BadAt
  rw [Polynomial.cyclotomic_zero]
  exact one_dvd _

/-- for an empty family the signed mask is `0` and the only signing is bad at every `d` -/
theorem badAt_of_isEmpty [IsEmpty ι] (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) : BadAt e ε d := by
  unfold BadAt P
  simp

/-- S4, first half, proved here directly (not from the skeleton): bad at `1` iff the signs add up to `0` -/
theorem badAt_one_iff' (e : ι → ℕ) (ε : ι → Bool) : BadAt e ε 1 ↔ ∑ k, sg (ε k) = 0 := by
  unfold BadAt
  have h1 : (Polynomial.X - 1 : Polynomial ℤ) = Polynomial.X - Polynomial.C 1 := by simp
  rw [Polynomial.cyclotomic_one, h1, Polynomial.dvd_iff_isRoot, Polynomial.IsRoot.def, P_eval_one]

/-- "bad at `d`" sees the exponents only modulo any multiple `n` of `d`: the `e k` need not be reduced -/
theorem badAt_mod (e : ι → ℕ) (ε : ι → Bool) {d n : ℕ} (hdn : d ∣ n) :
    BadAt (fun k => e k % n) ε d ↔ BadAt e ε d := by
  unfold BadAt
  have h1 : Polynomial.cyclotomic d ℤ ∣ (Polynomial.X ^ n - 1 : Polynomial ℤ) := by
    obtain ⟨c, hc⟩ := hdn
    rw [hc]
    exact (Polynomial.cyclotomic.dvd_X_pow_sub_one d ℤ).trans
      (pow_one_sub_dvd_pow_mul_sub_one Polynomial.X d c)
  have h2 : (Polynomial.X ^ n - 1 : Polynomial ℤ) ∣ P (fun k => e k % n) ε - P e ε := by
    unfold P
    rw [← Finset.sum_sub_distrib]
    refine Finset.dvd_sum fun k _ => ?_
    obtain ⟨g, hg⟩ := sub_one_dvd_pow_sub_one ((Polynomial.X : Polynomial ℤ) ^ n) (e k / n)
    have h3 : (Polynomial.X : Polynomial ℤ) ^ e k
        = Polynomial.X ^ (e k % n) * (Polynomial.X ^ n) ^ (e k / n) := by
      rw [← pow_mul, ← pow_add, Nat.mod_add_div]
    refine ⟨-(Polynomial.C (sg (ε k)) * Polynomial.X ^ (e k % n) * g), ?_⟩
    rw [h3]
    linear_combination (-(Polynomial.C (sg (ε k)) * Polynomial.X ^ (e k % n))) * hg
  exact dvd_iff_dvd_of_dvd_sub (h1.trans h2)

/-- a signing and its negative are bad at the same `d` -/
theorem badAt_not (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) : BadAt e (fun k => !ε k) d ↔ BadAt e ε d := by
  unfold BadAt
  have h : P e (fun k => !ε k) = -P e ε := by
    unfold P
    rw [← Finset.sum_neg_distrib]
    refine Finset.sum_congr rfl fun k _ => ?_
    rcases h : ε k with _ | _ <;> simp [sg, h]
  rw [h, dvd_neg]

/-! ### `live`, `rank`, `IsPivot` at the edges -/

/-- level `0` is never live for `p ≥ 2` (natural subtraction: `p ^ (0 - 1) = 1`), so `live e p i = true` implies `1 ≤ i` -/
theorem live_zero (e : ι → ℕ) {p : ℕ} (hp : 2 ≤ p) : live e p 0 = false := by
  cases hl : live e p 0
  · rfl
  · rw [live_iff] at hl
    obtain ⟨c, hc, h⟩ := hl
    obtain ⟨k, hk⟩ := h 1 (by omega)
    simp at hc hk
    omega

theorem one_le_of_live (e : ι → ℕ) {p i : ℕ} (hp : 2 ≤ p) (h : live e p i = true) : 1 ≤ i := by
  rcases Nat.eq_zero_or_pos i with rfl | hi
  · rw [live_zero e hp] at h
    exact absurd h (by decide)
  · exact hi

example (e : ι → ℕ) (p : ℕ) : rank e p 0 = 0 := by simp [rank]

/-- the rank does not exceed the level -/
theorem rank_le (e : ι → ℕ) (p i : ℕ) : rank e p i ≤ i := by
  unfold rank
  calc _ ≤ (Finset.Icc 1 i).card := Finset.card_filter_le _ _
    _ = i := by simp

/-- the empty set is a pivot set (for `p ≥ 1`), so the hypothesis `IsPivot` can always be supplied -/
theorem isPivot_empty (e : ι → ℕ) {p : ℕ} (hp : 0 < p) (i : ℕ) : IsPivot e p i ∅ := by
  refine ⟨fun k hk => absurd hk (Finset.notMem_empty k), fun c => ⟨0, hp, fun k hk => absurd hk (Finset.notMem_empty k)⟩⟩

/-- a subset of a pivot set is a pivot set -/
theorem isPivot_subset (e : ι → ℕ) {p i : ℕ} {J J' : Finset ι} (h : IsPivot e p i J) (hJ : J' ⊆ J) :
    IsPivot e p i J' := by
  refine ⟨fun k hk k' hk' => h.1 k (hJ hk) k' (hJ hk'), fun c => ?_⟩
  obtain ⟨t, ht, h2⟩ := h.2 c
  exact ⟨t, ht, fun k hk => h2 k (hJ hk)⟩

end

/-! ### `μ`, `lhsN1` -/

theorem mu_three : μ 3 = 2 := by
  simp [μ, Nat.Prime.primeFactors Nat.prime_three, Nat.Prime.factorization_self Nat.prime_three]

example : μ 0 = 0 := by simp [μ]
example : μ 1 = 0 := by simp [μ]

/-- for odd `m` the left side of N1 is the plain sum -/
theorem lhsN1_odd (m : ℕ) (hm : ¬ Even m) (T : Finset ℕ) : lhsN1 m T = ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t := by
  simp [lhsN1, hm]

/-- for even `m` it is the share of the level `1`, plus the sum, minus `1/16` exactly when `3 ∈ T` and `14 ≤ m` -/
theorem lhsN1_even (m : ℕ) (hm : Even m) (T : Finset ℕ) :
    lhsN1 m T = (m.choose (m / 2) : ℚ) / 2 ^ m + ∑ t ∈ T, (1 / 2 : ℚ) ^ μ t
      - (if 3 ∈ T ∧ 14 ≤ m then 1 / 16 else 0) := by
  simp [lhsN1, hm]

/-! ### No hypothesis is contradictory: each statement applied to data that satisfy its hypotheses -/

theorem bad3 : BadAt (ι := Fin 3) ![0, 1, 2] (fun _ => true) 3 := by
  refine ⟨1, ?_⟩
  simp [P, sg, Fin.sum_univ_three, Polynomial.cyclotomic_three]
  ring

theorem bad_all : ∀ d, BadAt (ι := Fin 2) ![0, 0] ![true, false] d := by
  intro d
  have h : P (ι := Fin 2) ![0, 0] ![true, false] = 0 := by
    simp [P, sg, Fin.sum_univ_two]
  unfold BadAt
  rw [h]
  exact dvd_zero _

theorem live3 : live (ι := Fin 3) ![0, 1, 2] 3 1 = true := by decide
theorem notlive : live (ι := Fin 2) ![0, 0] 3 1 = false := by decide
def e7 : Fin 7 → ℕ := ![0, 1, 2, 0, 1, 2, 0]
theorem live7 : live e7 3 1 = true := by decide
theorem rank7 : rank e7 3 1 = 1 := by decide

-- S0: p = 3, i = 1, d = 1, η = 1
example (c t t' : ℕ) (ht : t < 3) (ht' : t' < 3) :=
  classSum_eq_of_badAt (ι := Fin 3) ![0, 1, 2] (fun _ => true) Nat.prime_three (i := 1) le_rfl (d := 1) (by norm_num)
    (η := 1) IsPrimitiveRoot.one bad3 c t t' ht ht'
-- S1: bad at 3 = 3^1 * 1 and level 1 of 3 not live
example := badAt_of_not_live (ι := Fin 2) ![0, 0] ![true, false] Nat.prime_three (i := 1) le_rfl (d := 1) (by norm_num)
  (bad_all _) notlive
-- S2 (a): the empty pivot set
example := card_badSet_mul_two_pow_card_le (ι := Fin 3) ![0, 1, 2] Nat.prime_three (i := 1) le_rfl (d := 5) (by norm_num)
  (isPivot_empty _ (by norm_num) 1)
-- S4
example := badAt_one_iff (ι := Fin 3) ![0, 1, 2] (fun _ => true)
example := card_badSet_one (ι := Fin 3) ![0, 1, 2]
-- occupied classes, S2 (b), S2, S3
example := rank_lt_card_image (ι := Fin 3) ![0, 1, 2] Nat.prime_three 4
example := exists_isPivot (ι := Fin 3) ![0, 1, 2] Nat.prime_three (i := 1) le_rfl live3
example := card_badSet_mul_two_pow_rank_le (ι := Fin 3) ![0, 1, 2] Nat.prime_three (i := 1) le_rfl (d := 35)
  (by norm_num) live3
example := rank_lt_card (ι := Fin 3) ![0, 1, 2] Nat.prime_two 0
-- S5: seven elements, level 1 of 3 live, rank 1
example := card_badSet_three_pow_mul_le e7 (by simp) live7 rank7
-- N1: m = 3, T = {3}
example := lhsN1_lt_one 3 (by norm_num) {3} (by
  intro t ht
  rw [Finset.mem_singleton] at ht
  subst ht
  refine ⟨by norm_num, by norm_num, ?_⟩
  rw [mu_three])
-- A1 and the final statements: three odd primes, a power of 2, and both
example := exists_not_badAt 105 (by norm_num) (ι := Fin 3) ![0, 1, 2]
example := exists_not_badAt 1 (by norm_num) (ι := Fin 1) ![0]
example (w : ZMod 105 → ℕ) (hw : ∃ x, w x ≠ 0) := exists_signs_odd 105 (by norm_num) w hw
example (w : ZMod 1 → ℕ) (hw : ∃ x, w x ≠ 0) := exists_signs_odd 1 (by norm_num) w hw
example (w : ZMod 210 → ℕ) (hw : ∃ x, w x ≠ 0) := exists_lift_two_all w hw
example (w : ZMod 8 → ℕ) (hw : ∃ x, w x ≠ 0) := exists_lift_two_all w hw
example (w : ZMod 1 → ℕ) (hw : ∃ x, w x ≠ 0) := exists_lift_two_all w hw
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 315) := sizes_eq_two_all (N := 315) P hP
example (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ 16) := sizes_eq_two_all (N := 16) P hP

/-! ### What the statements would say without a hypothesis -/

-- A1 without `[Nonempty ι]` would be false: the empty family has no good signing
example : ¬ ∃ ε : Fin 0 → Bool, ∀ d, d ∣ 1 → ¬ BadAt (fun _ => 0 : Fin 0 → ℕ) ε d := by
  rintro ⟨ε, h⟩
  exact h 1 (dvd_refl 1) (badAt_of_isEmpty _ _ _)
-- A1 with `n = 0` would be false (`0 ∣ 0`, and every signing is bad at `0`); `¬ 2 ∣ n` excludes `n = 0`
example : (2 : ℕ) ∣ 0 := dvd_zero 2
example {ι : Type*} [Fintype ι] (e : ι → ℕ) : ¬ ∃ ε : ι → Bool, ∀ d, d ∣ 0 → ¬ BadAt e ε d := by
  rintro ⟨ε, h⟩
  exact h 0 (dvd_refl 0) (badAt_zero e ε)
-- in S0, S1, S2 the modulus `p ^ i * d` is never `0`: `¬ p ∣ d` gives `d ≠ 0`
example (p i d : ℕ) (hp : p.Prime) (hd : ¬ p ∣ d) : p ^ i * d ≠ 0 := by
  have hd0 : d ≠ 0 := by
    rintro rfl
    exact hd (dvd_zero p)
  exact Nat.mul_ne_zero (pow_ne_zero i hp.ne_zero) hd0
-- in S0 the root `η` has order `d ≥ 1`; for `d = 1` it is `1`
example (η : ℂ) (h : IsPrimitiveRoot η 1) : η = 1 := IsPrimitiveRoot.one_right_iff.1 h

/-! ### The parts fit: the one-line steps -/

section
variable {ι : Type*} [Fintype ι]

/-- S2 from S2 (a) and S2 (b) -/
theorem S2_of_S2a_S2b (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i) {d : ℕ}
    (hd : ¬ p ∣ d) (hlive : live e p i = true) :
    (badSet e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i) ≤ 2 ^ Fintype.card ι := by
  obtain ⟨J, hJ, hcard⟩ := exists_isPivot e hp hi hlive
  exact (Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by norm_num) hcard)).trans
    (card_badSet_mul_two_pow_card_le e hp hi hd hJ)

/-- S3 from "occupied classes" -/
theorem S3_of_occupied [Nonempty ι] (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (i : ℕ) :
    (p - 1) * rank e p i + 1 ≤ Fintype.card ι :=
  (rank_lt_card_image e hp i).trans (Finset.card_image_le.trans (by simp))

/-- the step of A1 (i): a signing bad at `d = p^i d''` with level `i` of `p` not live is bad at `d / p` -/
theorem step_down (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) {d : ℕ} (hd0 : d ≠ 0) (hpd : p ∣ d)
    (hbad : BadAt e ε d) (hlive : live e p (d.factorization p) = false) : BadAt e ε (d / p) := by
  obtain ⟨i, d'', hd'', rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hd0 p hp.ne_one
  have hi : (p ^ i * d'').factorization p = i := by
    have hd''0 : d'' ≠ 0 := by
      rintro rfl
      exact hd'' (dvd_zero p)
    rw [Nat.factorization_mul (pow_ne_zero i hp.ne_zero) hd''0]
    simp [hp.factorization_pow, Nat.factorization_eq_zero_of_not_dvd hd'']
  rw [hi] at hlive
  have hi1 : 1 ≤ i := by
    rcases Nat.eq_zero_or_pos i with rfl | h
    · simp at hpd
      exact absurd hpd hd''
    · exact h
  have h := badAt_of_not_live e ε hp hi1 hd'' hbad hlive
  have h2 : p ^ i * d'' / p = p ^ (i - 1) * d'' := by
    obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
    rw [pow_succ, Nat.add_sub_cancel, mul_assoc, mul_comm p d'', ← mul_assoc, Nat.mul_div_cancel _ hp.pos]
  rw [h2]
  exact h

end

/-! ### The final statements from one another -/

/-- `exists_lift_two_all` from `exists_signs_odd` and the finished `exists_lift_two_aux` -/
theorem lift_of_signs {N : ℕ} [NeZero N] (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, Lift.reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  obtain ⟨k, N', hN', hN⟩ := Nat.exists_eq_two_pow_mul_odd (NeZero.ne N)
  have h2 : ¬ 2 ∣ N' := by
    rw [← even_iff_two_dvd]
    exact Nat.not_even_iff_odd.2 hN'
  have : NeZero N' := ⟨by
    rintro rfl
    exact h2 (dvd_zero 2)⟩
  exact Lift.TwoAux.exists_lift_two_aux k N' hN h2 (fun B hB => exists_signs_odd N' h2 B hB) w hw

/-- `sizes_eq_two_all` from `exists_lift_two_all` and the finished lemmas on `reduce` (the proof of `sizes_eq_two`) -/
theorem sizes_of_lift {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * 2 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  ext s
  simp only [Set.mem_ofPred_eq]
  constructor
  · rintro ⟨w', hs, hpos, hpat⟩
    refine ⟨Lift.reduce w', (Lift.sum_reduce w').trans hs, hpos, fun d hd hd1 => ?_⟩
    rw [Lift.cyclotomic_dvd_reduce_iff w' d hd]
    exact hpat d (Dvd.dvd.mul_right hd 2) hd1
  · rintro ⟨w, hs, hpos, hpat⟩
    have hw : ∃ x, w x ≠ 0 := Lift.Aux.exists_ne_zero_of_sum_pos w (hs ▸ hpos)
    obtain ⟨w', hred, hnew⟩ := exists_lift_two_all w hw
    subst hred
    refine ⟨w', (Lift.sum_reduce w').symm.trans hs, hpos, fun d hd hd1 => ?_⟩
    by_cases hdN : d ∣ N
    · rw [← Lift.cyclotomic_dvd_reduce_iff w' d hdN]
      exact hpat d hdN hd1
    · exact iff_of_false (hnew d hd hdN) fun h => hdN (hP d h)

/-- the paper's Lemma "lifting along 2" as worded (same number of elements, reduction, and for every `d ∣ 2N`:
`Φ_d ∣ A'` iff `d ∣ N` and `Φ_d ∣ A`), for EVERY `N`, from `exists_lift_two_all` and two finished theorems -/
theorem paper_lift2_all {N : ℕ} [NeZero N] (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = ∑ x, w x ∧ Lift.reduce w' = w ∧
      ∀ d, d ∣ N * 2 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔
        (d ∣ N ∧ Polynomial.cyclotomic d ℤ ∣ maskW w)) := by
  obtain ⟨w', hred, hnew⟩ := exists_lift_two_all w hw
  subst hred
  refine ⟨w', (Lift.sum_reduce w').symm, rfl, fun d hd => ⟨fun h => ?_, fun h => ?_⟩⟩
  · have hdN : d ∣ N := by
      by_contra hc
      exact hnew d hd hc h
    exact ⟨hdN, (Lift.cyclotomic_dvd_reduce_iff w' d hdN).2 h⟩
  · exact (Lift.cyclotomic_dvd_reduce_iff w' d h.1).1 h.2

/-- the paper's sentence "the sizes are the same on `Z_N` and on `Z_{Ns}` for every `N` and every `s ≥ 1`": from
`sizes_eq_two_all` (the factors 2) and the finished `Lift.sizes_eq` (the odd prime factors), by induction on `s` -/
theorem sizes_all {N : ℕ} [NeZero N] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    ∀ (s : ℕ) [NeZero s], Lift.AllAux.sizes (N * s) P = Lift.AllAux.sizes N P := by
  intro s
  induction s using Nat.strong_induction_on with
  | _ s ih =>
    intro _
    by_cases h1 : s = 1
    · subst h1
      exact Lift.AllAux.sizes_congr (mul_one N) P
    · obtain ⟨r, hr, s', rfl⟩ := Nat.exists_prime_and_dvd h1
      have hs'0 : s' ≠ 0 := by
        rintro rfl
        exact NeZero.ne (r * 0) (mul_zero r)
      have : NeZero s' := ⟨hs'0⟩
      have : Fact r.Prime := ⟨hr⟩
      have hlt : s' < r * s' := lt_mul_of_one_lt_left (Nat.pos_of_ne_zero hs'0) hr.one_lt
      have e1 : Lift.AllAux.sizes (N * (r * s')) P = Lift.AllAux.sizes (N * s' * r) P :=
        Lift.AllAux.sizes_congr (by ring) P
      have e2 : Lift.AllAux.sizes (N * s' * r) P = Lift.AllAux.sizes (N * s') P := by
        by_cases hr2 : r = 2
        · subst hr2
          exact sizes_eq_two_all (N := N * s') P fun d hd => Dvd.dvd.mul_right (hP d hd) s'
        · exact Lift.sizes_eq (N := N * s') (r := r) hr2 P fun d hd => Dvd.dvd.mul_right (hP d hd) s'
      exact e1.trans (e2.trans (ih s' hlt))

/-- the same with the sets written out: "the sizes are the same on `ZMod (N * s)` and on `ZMod N` for every `N` and
every `s ≥ 1`", as a consequence of `sizes_eq_two_all` and finished theorems -/
theorem sizes_all_text {N : ℕ} [NeZero N] (s : ℕ) [NeZero s] (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {t | ∃ w' : ZMod (N * s) → ℕ, ∑ y, w' y = t ∧ 0 < t ∧
        ∀ d, d ∣ N * s → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {t | ∃ w : ZMod N → ℕ, ∑ x, w x = t ∧ 0 < t ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} :=
  sizes_all P hP s

end AuditSigns

#print axioms AuditSigns.P_coeff
#print axioms AuditSigns.P_eval_one
#print axioms AuditSigns.P_aeval
#print axioms AuditSigns.sum_classSum
#print axioms AuditSigns.classSum_of_le
#print axioms AuditSigns.badAt_zero
#print axioms AuditSigns.badAt_of_isEmpty
#print axioms AuditSigns.badAt_one_iff'
#print axioms AuditSigns.badAt_mod
#print axioms AuditSigns.badAt_not
#print axioms AuditSigns.live_zero
#print axioms AuditSigns.rank_le
#print axioms AuditSigns.isPivot_empty
#print axioms AuditSigns.isPivot_subset
#print axioms AuditSigns.mu_three
#print axioms AuditSigns.lhsN1_odd
#print axioms AuditSigns.lhsN1_even
#print axioms AuditSigns.bad3
#print axioms AuditSigns.live7
#print axioms AuditSigns.rank7
#print axioms AuditSigns.S2_of_S2a_S2b
#print axioms AuditSigns.S3_of_occupied
#print axioms AuditSigns.step_down
#print axioms AuditSigns.lift_of_signs
#print axioms AuditSigns.sizes_of_lift
#print axioms AuditSigns.paper_lift2_all
#print axioms AuditSigns.sizes_all
#print axioms AuditSigns.sizes_all_text
