import Pnq.EvenFinal

/-! Audit of the even skeleton: do the fixed statements fit together, and can their hypotheses be met?
Everything here rests on the `sorry` statements of the skeleton where it uses them (that is the point: these are
derivations at the level of statements).  Scratch file of the audit; nothing else uses it. -/

open Pnq

namespace AuditFit

/-! ### L from T and S0′ (the derivation of `CheckEven.lean`, as a named theorem, then compared with the fixed L) -/

theorem fit_succ {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} (hd : ¬ 2 ∣ d) (h3 : ¬ 3 ∣ d) (j : ℕ)
    (hbad : Bad3 e ε (2 ^ (j + 1) * d)) :
    levelBad e (fun k => fun η : {η : F3 // IsPrimitiveRoot η d} => η.1 ^ e k) ε (j + 1) := by
  intro r hr
  funext η
  have h := classSum3_eq_of_bad3 e ε Nat.prime_two (by norm_num) (by omega : 1 ≤ j + 1) hd h3
    η.2 hbad r 0 1 (by norm_num) (by norm_num)
  rw [Nat.add_sub_cancel, Nat.mod_eq_of_lt hr, zero_mul, add_zero, one_mul] at h
  simp only [csum, classSum3] at h ⊢
  rw [Finset.sum_apply, Finset.sum_apply]
  convert h using 2 <;> split_ifs <;> simp [zsmul_eq_mul]

theorem fit_zero {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) {d : ℕ} :
    levelBad e (fun k => fun η : {η : F3 // IsPrimitiveRoot η d} => η.1 ^ e k) ε 0 ↔ Bad3 e ε d := by
  rw [levelBad_zero]
  constructor
  · intro h ζ hζ
    have := congrFun h ⟨ζ, hζ⟩
    simpa [val3, Finset.sum_apply, zsmul_eq_mul] using this
  · intro h
    funext η
    have := h η.1 η.2
    simpa [val3, Finset.sum_apply, zsmul_eq_mul] using this

open Classical in
theorem L_derived {ι : Type*} [Fintype ι] (e : ι → ℕ) {d : ℕ} (hd : ¬ 2 ∣ d) (h3 : ¬ 3 ∣ d) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ Bad3 e ε (2 ^ j * d)).card ≤
      2 * (bad3Set e d).card := by
  have hT := card_exists_levelBad_le e
    (fun k => fun η : {η : F3 // IsPrimitiveRoot η d} => η.1 ^ e k) K
  refine le_trans (Finset.card_le_card ?_) (le_trans hT ?_)
  · intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε ⊢
    obtain ⟨j, hj, hb⟩ := hε
    refine ⟨j, hj, ?_⟩
    cases j with
    | zero => exact (fit_zero e ε).mpr (by simpa using hb)
    | succ j => exact fit_succ e ε hd h3 j hb
  · refine Nat.mul_le_mul_left 2 (Finset.card_le_card ?_)
    intro ε hε
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hε
    exact (mem_bad3Set e d ε).mpr ((fit_zero e ε).mp hε)

/-- the derived theorem has the type of the fixed statement L (instances included) -/
example : type_of% @Pnq.card_exists_bad3_le := @L_derived

/-! ### B from A′ and M -/

theorem B_derived (n : ℕ) (hn : n ≠ 0) {ι : Type*} [Fintype ι] (hm : 3 ≤ Fintype.card ι) (e : ι → ℕ) :
    ∃ ε : ι → Bool, ∀ d, d ∣ n → ¬ BadAt e ε d := by
  obtain ⟨a, n3, hn3, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hn 3 (by norm_num)
  obtain ⟨ε, hε⟩ := exists_not_bad3 n3 hn3 hm e
  refine ⟨ε, fun d hd hbad => ?_⟩
  have hd0 : d ≠ 0 := fun h => hn (zero_dvd_iff.mp (h ▸ hd))
  obtain ⟨i, d', hd', rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hd0 3 (by norm_num)
  have h1 : d' ∣ 3 ^ a * n3 := (Dvd.intro_left _ rfl).trans hd
  have hco : Nat.Coprime d' (3 ^ a) :=
    Nat.Coprime.pow_right _ ((Nat.Prime.coprime_iff_not_dvd Nat.prime_three).2 hd').symm
  exact hε d' (hco.dvd_of_dvd_mul_left h1) (bad3_of_badAt e ε i hd' hbad)

example : type_of% @Pnq.exists_not_badAt_of_three_le := @B_derived

/-! ### the first final statement for three or more elements, from B (the proof of `exists_signs_odd` with B) -/

theorem final_of_three_le (n : ℕ) [NeZero n] (w : ZMod n → ℕ) (h3 : 3 ≤ ∑ x, w x) :
    ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  obtain ⟨ε, hε⟩ := exists_not_badAt_of_three_le n (NeZero.ne n)
    (ι := Σ x : ZMod n, Fin (w x)) (by simpa [Fintype.card_sigma] using h3) (fun k => k.1.val)
  refine ⟨fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card,
    fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card,
    fun x => ?_, fun d hd hdvd => hε d hd ?_⟩
  · change (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card
      + (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card = w x
    rw [FinalAux.card_true_add_card_false, Fintype.card_fin]
  · unfold BadAt
    rw [FinalAux.P_sigma]
    exact hdvd

/-! ### S2′ with the rank from S2′ with a pivot set and the finished `exists_isPivot` -/

theorem S2rank_derived {ι : Type*} [Fintype ι] (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3) {i : ℕ}
    (hi : 1 ≤ i) {d : ℕ} (hd : ¬ p ∣ d) (h3 : ¬ 3 ∣ d) (hlive : live e p i = true) :
    (bad3Set e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i) ≤ 2 ^ Fintype.card ι := by
  obtain ⟨J, hJ, hcard⟩ := exists_isPivot e hp hi hlive
  exact (Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by norm_num) hcard)).trans
    (card_bad3Set_mul_two_pow_card_le e hp hp3 hi hd h3 hJ)

example : type_of% @Pnq.card_bad3Set_mul_two_pow_rank_le := @S2rank_derived

/-! ### the step of A′: a signing 3-bad at `d` (prime to 3) with the level `v_p(d)` of a prime `p ≠ 3` of `d` not
live is 3-bad at `d / p`; from S1′ (the factor `2^j` of `d` stays in the "d" of S1′) -/

theorem step_down3 {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) {p : ℕ} (hp : p.Prime) (hp3 : p ≠ 3)
    {d : ℕ} (hd3 : ¬ 3 ∣ d) (hpd : p ∣ d) (hbad : Bad3 e ε d)
    (hlive : live e p (d.factorization p) = false) : Bad3 e ε (d / p) := by
  have hd0 : d ≠ 0 := fun h => hd3 (h ▸ dvd_zero 3)
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
  have h3'' : ¬ 3 ∣ d'' := fun h => hd3 (Dvd.dvd.mul_left h _)
  have h := bad3_of_not_live e ε hp hp3 hi1 hd'' h3'' hbad hlive
  have h2 : p ^ i * d'' / p = p ^ (i - 1) * d'' := by
    obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
    rw [pow_succ, Nat.add_sub_cancel, mul_assoc, mul_comm p d'', ← mul_assoc, Nat.mul_div_cancel _ hp.pos]
  rw [h2]
  exact h

/-! ### the count at `d = 1` in the form A′ uses it: from E1 (second half) -/

theorem three_mul_card_bad3Set_one_le {ι : Type*} [Fintype ι] (e : ι → ℕ) :
    3 * (bad3Set e 1).card ≤ 2 ^ Fintype.card ι + 2 := by
  have h := card_bad3Set_one e
  split_ifs at h <;> omega

/-! ### No hypothesis is contradictory: each statement applied to data that satisfy its hypotheses -/

/-- `Φ_3` divides `1 + X + X²` -/
theorem badAt3 : BadAt (ι := Fin 3) ![0, 1, 2] (fun _ => true) (3 ^ 1 * 1) := by
  refine ⟨1, ?_⟩
  simp [P, sg, Fin.sum_univ_three, Polynomial.cyclotomic_three]
  ring

-- M: i = 1, d = 1
example : Bad3 (ι := Fin 3) ![0, 1, 2] (fun _ => true) 1 :=
  bad3_of_badAt _ _ 1 (d := 1) (by norm_num) badAt3

/-- `1 + ζ = 0` at the primitive second root of unity `ζ = -1`: the signing `+ +` of `{0, 1}` is 3-bad at 2 -/
theorem bad3_two : Bad3 (ι := Fin 2) ![0, 1] ![true, true] (2 ^ 1 * 1) := by
  intro ζ hζ
  have h2 : ζ = -1 := by
    have : IsPrimitiveRoot ζ 2 := by simpa using hζ
    exact this.eq_neg_one_of_two_right
  subst h2
  simp [val3, sg, Fin.sum_univ_two]

-- S0′: p = 2, i = 1, d = 1, η = 1
example (c t t' : ℕ) (ht : t < 2) (ht' : t' < 2) :=
  classSum3_eq_of_bad3 (ι := Fin 2) ![0, 1] ![true, true] Nat.prime_two (by norm_num) (i := 1) le_rfl (d := 1)
    (by norm_num) (by norm_num) (η := 1) IsPrimitiveRoot.one bad3_two c t t' ht ht'

/-- the signing `+ -` of `{0, 0}` has the signed mask 0 and is 3-bad at every `d` -/
theorem bad3_all (d : ℕ) : Bad3 (ι := Fin 2) ![0, 0] ![true, false] d := by
  intro ζ _
  simp [val3, sg, Fin.sum_univ_two]

theorem notlive2 : live (ι := Fin 2) ![0, 0] 2 1 = false := by decide
theorem notlive5 : live (ι := Fin 2) ![0, 0] 5 1 = false := by decide

-- S1′: p = 2, i = 1, d = 1; and p = 5, i = 1, d = 4
example := bad3_of_not_live (ι := Fin 2) ![0, 0] ![true, false] Nat.prime_two (by norm_num) (i := 1) le_rfl (d := 1)
  (by norm_num) (by norm_num) (bad3_all _) notlive2
example := bad3_of_not_live (ι := Fin 2) ![0, 0] ![true, false] Nat.prime_five (by norm_num) (i := 1) le_rfl (d := 4)
  (by norm_num) (by norm_num) (bad3_all _) notlive5

/-- a one-element pivot set for the level 1 of 2: the element `0` of the family `{0, 1}` -/
theorem pivot2 : IsPivot (ι := Fin 2) ![0, 1] 2 1 {0} := by
  refine ⟨fun k hk k' hk' _ => ?_, fun c => ⟨1, by norm_num, fun k hk => ?_⟩⟩
  · rw [Finset.mem_singleton] at hk hk'
    rw [hk, hk']
  · rw [Finset.mem_singleton] at hk
    subst hk
    simp

-- S2′ with a pivot set: p = 2, i = 1, d = 5
example := card_bad3Set_mul_two_pow_card_le (ι := Fin 2) ![0, 1] Nat.prime_two (by norm_num) (i := 1) le_rfl (d := 5)
  (by norm_num) (by norm_num) pivot2

theorem live2 : live (ι := Fin 2) ![0, 1] 2 1 = true := by decide
theorem live5 : live (ι := Fin 5) ![0, 1, 2, 3, 4] 5 1 = true := by decide

-- S2′ with the rank: p = 2, i = 1, d = 7; p = 5, i = 1, d = 14
example := card_bad3Set_mul_two_pow_rank_le (ι := Fin 2) ![0, 1] Nat.prime_two (by norm_num) (i := 1) le_rfl (d := 7)
  (by norm_num) (by norm_num) live2
example := card_bad3Set_mul_two_pow_rank_le (ι := Fin 5) ![0, 1, 2, 3, 4] Nat.prime_five (by norm_num) (i := 1) le_rfl
  (d := 14) (by norm_num) (by norm_num) live5

-- E1, L, N1′, A′, B, the final statements
example := bad3_one_iff (ι := Fin 3) ![0, 1, 2] (fun _ => true)
example := card_bad3Set_one (ι := Fin 3) ![0, 1, 2]
example := card_exists_bad3_le (ι := Fin 3) ![0, 1, 2] (d := 35) (by norm_num) (by norm_num) 3
example := card_exists_levelBad_le (ι := Fin 3) ![0, 1, 2] ![(1 : ℤ), 1, 1] 2
example := sum_half_pow_mu_lt {5, 7, 35} (by decide)
example := exists_not_bad3 20 (by norm_num) (ι := Fin 3) (by simp) ![0, 1, 2]
example := exists_not_bad3 1 (by norm_num) (ι := Fin 3) (by simp) ![0, 0, 0]
example := exists_not_badAt_of_three_le 12 (by norm_num) (ι := Fin 3) (by simp) ![0, 1, 2]
example (w : ZMod 12 → ℕ) (hw : ∃ x, w x ≠ 0) (h : ¬ ExceptionalPair w) := exists_signs_all 12 w hw h
example (w : ZMod 1 → ℕ) (hw : ∃ x, w x ≠ 0) (h : ¬ ExceptionalPair w) := exists_signs_all 1 w hw h
example (w : ZMod 12 → ℕ) (h : ExceptionalPair w) := not_exists_signs_of_exceptionalPair 12 w h

/-! ### Without `p ≠ 3` the statement S0′ would be false: `p = 3`, `i = 1`, `d = 1`, one element -/

theorem S0_false_for_three :
    ¬ ∀ (c t t' : ℕ), t < 3 → t' < 3 →
      classSum3 (ι := Fin 1) ![0] ![true] 1 (3 ^ 1) (c % 3 ^ (1 - 1) + t * 3 ^ (1 - 1)) =
        classSum3 (ι := Fin 1) ![0] ![true] 1 (3 ^ 1) (c % 3 ^ (1 - 1) + t' * 3 ^ (1 - 1)) := by
  intro h
  have h1 := h 0 0 1 (by norm_num) (by norm_num)
  simp [classSum3, sg] at h1

/-- its hypothesis `Bad3 e ε (3 ^ 1 * 1)` holds for every signing (no primitive third root of unity in `F3`) -/
theorem hyp_for_three : Bad3 (ι := Fin 1) ![0] ![true] (3 ^ 1 * 1) := by
  intro ζ hζ
  exfalso
  have h3 : IsPrimitiveRoot ζ 3 := by simpa using hζ
  have hne : NeZero ((3 : ℕ) : F3) := h3.neZero'
  exact hne.out ((CharP.cast_eq_zero_iff F3 3 3).2 dvd_rfl)

/-! ### A′ and B fail for the empty family and for the pair `{0, 1}` on `n = 2` (so `3 ≤ card` cannot be dropped) -/

/-- two elements `0, 1`, `n = 2`: every signing is 3-bad at 1 or at 2 -/
theorem A_false_pair : ¬ ∃ ε : Fin 2 → Bool, ∀ d, d ∣ 2 → ¬ Bad3 (ι := Fin 2) ![0, 1] ε d := by
  rintro ⟨ε, h⟩
  have h1 := h 1 (by norm_num)
  have h2 := h 2 dvd_rfl
  rcases hε0 : ε 0 with _ | _ <;> rcases hε1 : ε 1 with _ | _
  · apply h2
    intro ζ hζ
    have hz : ζ = -1 := hζ.eq_neg_one_of_two_right
    subst hz
    simp [val3, sg, Fin.sum_univ_two, hε0, hε1]
  · apply h1
    intro ζ hζ
    rw [IsPrimitiveRoot.one_right_iff] at hζ
    subst hζ
    simp [val3, sg, Fin.sum_univ_two, hε0, hε1]
  · apply h1
    intro ζ hζ
    rw [IsPrimitiveRoot.one_right_iff] at hζ
    subst hζ
    simp [val3, sg, Fin.sum_univ_two, hε0, hε1]
  · apply h2
    intro ζ hζ
    have hz : ζ = -1 := hζ.eq_neg_one_of_two_right
    subst hz
    simp [val3, sg, Fin.sum_univ_two, hε0, hε1]

/-- the empty family, any `n` prime to 3: the one signing is 3-bad at 1 -/
theorem A_false_empty (n : ℕ) : ¬ ∃ ε : Fin 0 → Bool, ∀ d, d ∣ n → ¬ Bad3 (fun _ => 0 : Fin 0 → ℕ) ε d := by
  rintro ⟨ε, h⟩
  exact h 1 (one_dvd n) (fun ζ _ => by simp [val3])

end AuditFit

#print axioms AuditFit.L_derived
#print axioms AuditFit.B_derived
#print axioms AuditFit.final_of_three_le
#print axioms AuditFit.S2rank_derived
#print axioms AuditFit.step_down3
#print axioms AuditFit.three_mul_card_bad3Set_one_le
#print axioms AuditFit.bad3_two
#print axioms AuditFit.S0_false_for_three
#print axioms AuditFit.hyp_for_three
#print axioms AuditFit.A_false_pair
#print axioms AuditFit.A_false_empty
