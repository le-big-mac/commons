/-
The statement on signs for every `n`, with its exceptional pairs: the final statements.  A nonempty multiset `w` on
`ZMod n` that is not an exceptional pair can be split into two parts `u`, `v` so that no `Φ_d`, `d ∣ n`, divides
`maskW u - maskW v`; an exceptional pair cannot.  The first from B (`exists_not_badAt_of_three_le` of
`Pnq/EvenAll.lean`) for three or more elements, as `exists_signs_odd` of `Pnq/SignFinal.lean` was drawn from
`exists_not_badAt`, and by hand for one and two elements.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.EvenAll
import Pnq.SignFinal

open Finset

namespace Pnq

/-! Helper lemmas live in the namespace `Pnq.Final3Aux`, so that their names cannot clash with those of the other
files of the project. -/

namespace Final3Aux

open Polynomial

section

variable {n : ℕ} [NeZero n]

/-- the mask of the sum of two multisets -/
theorem maskW_add (u v : ZMod n → ℕ) : maskW (u + v) = maskW u + maskW v := by
  simp [maskW, Finset.sum_add_distrib, add_mul]

/-- the mask of one mark -/
theorem maskW_single (a : ZMod n) : maskW (Pi.single a 1) = X ^ a.val := by
  simp [maskW, Pi.single_apply]

/-- the mask of the empty multiset -/
theorem maskW_zero : maskW (0 : ZMod n → ℕ) = 0 := by
  simp [maskW]

/-- the value at a complex number of the difference of two masks -/
theorem aeval_sub (u v : ZMod n → ℕ) (z : ℂ) :
    aeval z (maskW u - maskW v) = ∑ x : ZMod n, ((u x : ℂ) - (v x : ℂ)) * z ^ x.val := by
  rw [map_sub, Lift.Aux.aeval_maskW, Lift.Aux.aeval_maskW, ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun x _ => (sub_mul _ _ _).symm

/-- if `Φ_d` divides a polynomial over `ℤ`, the polynomial vanishes at every primitive `d`-th root of unity -/
theorem aeval_eq_zero_of_cyclotomic_dvd (Q : ℤ[X]) {d : ℕ} (hd : 0 < d) (h : cyclotomic d ℤ ∣ Q) {z : ℂ}
    (hz : IsPrimitiveRoot z d) : aeval z Q = 0 := by
  obtain ⟨R, hR⟩ := h
  have h0 : aeval z (cyclotomic d ℤ) = 0 := by
    have h1 : IsRoot (cyclotomic d ℂ) z := hz.isRoot_cyclotomic hd
    rw [← map_cyclotomic d (algebraMap ℤ ℂ), IsRoot.def, eval_map_algebraMap] at h1
    exact h1
  rw [hR, map_mul, h0, zero_mul]

/-- for `z` with `z ^ n = 1`, the power `z ^ x.val` of a residue `x` modulo `n` is multiplicative in `x` -/
theorem pow_val_add {z : ℂ} (hz : z ^ n = 1) (x y : ZMod n) :
    z ^ (x + y).val = z ^ x.val * z ^ y.val := by
  rw [ZMod.val_add, ← pow_add, ← pow_eq_pow_mod _ hz]

/-- `n` divides `k * g.val` exactly when `k • g = 0` in `ZMod n` -/
theorem dvd_mul_val_iff (g : ZMod n) (k : ℕ) : n ∣ k * g.val ↔ k • g = 0 := by
  rw [← ZMod.natCast_eq_zero_iff, Nat.cast_mul, ZMod.natCast_zmod_val, nsmul_eq_mul]

/-- for `z` with `z ^ n = 1` and `k • g = 0` in `ZMod n`: `z ^ (k * g.val) = 1` -/
theorem pow_mul_val_eq_one {z : ℂ} (hz : z ^ n = 1) (g : ZMod n) {k : ℕ} (hk : k • g = 0) :
    z ^ (k * g.val) = 1 := by
  obtain ⟨c, hc⟩ := (dvd_mul_val_iff g k).2 hk
  rw [hc, pow_mul, hz, one_pow]

/-- one element taken out of a nonempty multiset -/
theorem exists_single_add (w : ZMod n → ℕ) {a : ZMod n} (ha : w a ≠ 0) :
    ∃ w' : ZMod n → ℕ, w = Pi.single a 1 + w' ∧ ∑ x, w x = ∑ x, w' x + 1 := by
  have h1 : w = Pi.single a 1 + fun x => w x - (Pi.single a 1 : ZMod n → ℕ) x := by
    funext x
    by_cases hx : x = a
    · subst hx
      simp only [Pi.add_apply, Pi.single_eq_same]
      omega
    · simp [hx]
  refine ⟨fun x => w x - (Pi.single a 1 : ZMod n → ℕ) x, h1, ?_⟩
  conv_lhs => rw [h1]
  simp [Finset.sum_add_distrib, add_comm]

/-- a nonempty multiset with fewer than three elements is one mark or two marks -/
theorem eq_single_or_pair (w : ZMod n → ℕ) (hw : ∃ x, w x ≠ 0) (h : ¬ 3 ≤ ∑ x, w x) :
    (∃ a, w = Pi.single a 1) ∨ ∃ a b, w = Pi.single a 1 + Pi.single b 1 := by
  obtain ⟨a, ha⟩ := hw
  obtain ⟨w', hw', hs'⟩ := exists_single_add w ha
  by_cases hw'0 : ∀ x, w' x = 0
  · left
    refine ⟨a, ?_⟩
    rw [hw']
    funext x
    simp [hw'0 x]
  · right
    obtain ⟨b, hb⟩ := not_forall.1 hw'0
    obtain ⟨w'', hw'', hs''⟩ := exists_single_add w' hb
    have h0 : ∑ x, w'' x = 0 := by omega
    have hz : ∀ x, w'' x = 0 := fun x => (Finset.sum_eq_zero_iff.1 h0) x (Finset.mem_univ x)
    refine ⟨a, b, ?_⟩
    rw [hw', hw'']
    funext x
    simp [hz x]

/-- a primitive `d`-th root of unity in `ℂ` for a divisor `d` of `n`, with `ζ ^ n = 1` and `ζ ≠ 0` -/
theorem exists_root_of_dvd {d : ℕ} (hd : d ∣ n) :
    0 < d ∧ ∃ ζ : ℂ, IsPrimitiveRoot ζ d ∧ ζ ^ n = 1 ∧ ζ ≠ 0 := by
  have hd0 : d ≠ 0 := fun h => NeZero.ne n (zero_dvd_iff.mp (h ▸ hd))
  have hζ := Complex.isPrimitiveRoot_exp d hd0
  refine ⟨Nat.pos_of_ne_zero hd0, _, hζ, ?_, hζ.ne_zero hd0⟩
  obtain ⟨c, rfl⟩ := hd
  rw [pow_mul, hζ.pow_eq_one, one_pow]

/-- one mark: no `Φ_d`, `d ∣ n`, divides `X ^ a` -/
theorem not_dvd_single (a : ZMod n) (d : ℕ) (hd : d ∣ n) :
    ¬ cyclotomic d ℤ ∣ maskW (Pi.single a 1) - maskW (0 : ZMod n → ℕ) := by
  intro hdvd
  obtain ⟨hd0, ζ, hζ, -, hζ0⟩ := exists_root_of_dvd hd
  have h0 := aeval_eq_zero_of_cyclotomic_dvd _ hd0 hdvd hζ
  rw [maskW_single, maskW_zero, sub_zero, map_pow, aeval_X] at h0
  exact pow_ne_zero _ hζ0 h0

/-- two marks `a`, `b` with `a - b` of odd additive order: no `Φ_d`, `d ∣ n`, divides `X ^ a + X ^ b` -/
theorem not_dvd_pair (a b : ZMod n) (ho : Odd (addOrderOf (a - b))) (d : ℕ) (hd : d ∣ n) :
    ¬ cyclotomic d ℤ ∣ maskW (Pi.single a 1 + Pi.single b 1) - maskW (0 : ZMod n → ℕ) := by
  intro hdvd
  obtain ⟨hd0, ζ, hζ, hζn, hζ0⟩ := exists_root_of_dvd hd
  have h0 := aeval_eq_zero_of_cyclotomic_dvd _ hd0 hdvd hζ
  rw [maskW_add, maskW_single, maskW_single, maskW_zero, sub_zero, map_add, map_pow, map_pow, aeval_X] at h0
  -- `h0 : ζ ^ a.val + ζ ^ b.val = 0`
  have hab : ζ ^ a.val = ζ ^ (a - b).val * ζ ^ b.val := by
    rw [← pow_val_add hζn, sub_add_cancel]
  have hg : ζ ^ (a - b).val = -1 := by
    have h1 : (ζ ^ (a - b).val + 1) * ζ ^ b.val = 0 := by rw [add_mul, one_mul, ← hab, h0]
    rcases mul_eq_zero.1 h1 with h | h
    · exact eq_neg_of_add_eq_zero_left h
    · exact absurd h (pow_ne_zero _ hζ0)
  have h1 : ζ ^ (addOrderOf (a - b) * (a - b).val) = 1 :=
    pow_mul_val_eq_one hζn (a - b) (addOrderOf_nsmul_eq_zero _)
  rw [mul_comm, pow_mul, hg, ho.neg_one_pow] at h1
  norm_num at h1

/-- two marks `a`, `b` with `a - b` of even additive order: there is `ξ ∈ ℂ` with `ξ ^ n = 1` and
`ξ ^ a + ξ ^ b = 0` -/
theorem exists_root_of_even (a b : ZMod n) (he : Even (addOrderOf (a - b))) :
    ∃ ξ : ℂ, ξ ^ n = 1 ∧ ξ ^ a.val + ξ ^ b.val = 0 := by
  obtain ⟨m, hm⟩ := he
  have hζ := Complex.isPrimitiveRoot_exp n (NeZero.ne n)
  generalize Complex.exp (2 * Real.pi * Complex.I / n) = ζ at hζ
  have hζn : ζ ^ n = 1 := hζ.pow_eq_one
  have hξn : (ζ ^ m) ^ n = 1 := by rw [← pow_mul, mul_comm, pow_mul, hζn, one_pow]
  refine ⟨ζ ^ m, hξn, ?_⟩
  have hsq : (ζ ^ m) ^ (a - b).val * (ζ ^ m) ^ (a - b).val = 1 := by
    have h := pow_mul_val_eq_one hζn (a - b) (addOrderOf_nsmul_eq_zero (a - b))
    rw [hm, add_mul, pow_add, pow_mul] at h
    exact h
  have hne : (ζ ^ m) ^ (a - b).val ≠ 1 := by
    intro h
    rw [← pow_mul, hζ.pow_eq_one_iff_dvd, dvd_mul_val_iff] at h
    have h3 := addOrderOf_dvd_of_nsmul_eq_zero h
    have hpos : 0 < addOrderOf (a - b) := addOrderOf_pos (a - b)
    have h4 := Nat.le_of_dvd (by omega) h3
    omega
  have hneg : (ζ ^ m) ^ (a - b).val = -1 := (mul_self_eq_one_iff.1 hsq).resolve_left hne
  have hab : (ζ ^ m) ^ a.val = (ζ ^ m) ^ (a - b).val * (ζ ^ m) ^ b.val := by
    rw [← pow_val_add hξn, sub_add_cancel]
  rw [hab, hneg]
  ring

end

end Final3Aux

/-- an exceptional pair: two marks whose difference has even additive order -/
def ExceptionalPair {n : ℕ} (w : ZMod n → ℕ) : Prop :=
  ∃ a b : ZMod n, w = Pi.single a 1 + Pi.single b 1 ∧ Even (addOrderOf (a - b))

/-- **The statement on signs for every `n`** (the first final statement of the plan).  The elements of a nonempty
multiset `w` on `ZMod n` that is not an exceptional pair can be split into two parts `u`, `v` so that no `Φ_d`,
`d ∣ n`, divides `maskW u - maskW v`. -/
theorem exists_signs_all (n : ℕ) [NeZero n] (w : ZMod n → ℕ) (hw : ∃ x, w x ≠ 0)
    (hpair : ¬ ExceptionalPair w) :
    ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  by_cases h3 : 3 ≤ ∑ x, w x
  · -- three or more elements: from B, one point for each element of the multiset
    have hcard : 3 ≤ Fintype.card (Σ x : ZMod n, Fin (w x)) := by
      simpa [Fintype.card_sigma] using h3
    obtain ⟨ε, hε⟩ := exists_not_badAt_of_three_le n (NeZero.ne n) hcard
      (fun k : Σ x : ZMod n, Fin (w x) => k.1.val)
    refine ⟨fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card,
      fun x => (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card,
      fun x => ?_, fun d hd hdvd => hε d hd ?_⟩
    · change (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = true).card
        + (Finset.univ.filter fun j : Fin (w x) => ε ⟨x, j⟩ = false).card = w x
      rw [FinalAux.card_true_add_card_false, Fintype.card_fin]
    · unfold BadAt
      rw [FinalAux.P_sigma]
      exact hdvd
  · -- one or two elements: all of them with the sign `+`
    rcases Final3Aux.eq_single_or_pair w hw h3 with ⟨a, rfl⟩ | ⟨a, b, rfl⟩
    · exact ⟨_, 0, fun x => by simp, Final3Aux.not_dvd_single a⟩
    · have ho : Odd (addOrderOf (a - b)) := Nat.not_even_iff_odd.1 fun he => hpair ⟨a, b, rfl, he⟩
      exact ⟨_, 0, fun x => by simp, Final3Aux.not_dvd_pair a b ho⟩

/-- **The exceptional pairs are exceptions** (the second final statement of the plan).  For an exceptional pair `w`,
every splitting `u + v = w` has `maskW u - maskW v` divisible by `Φ_d` for some `d ∣ n`. -/
theorem not_exists_signs_of_exceptionalPair (n : ℕ) [NeZero n] (w : ZMod n → ℕ) (hpair : ExceptionalPair w) :
    ¬ ∃ u v : ZMod n → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ n → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  rintro ⟨u, v, huv, hno⟩
  obtain ⟨a, b, rfl, he⟩ := hpair
  have hab : a ≠ b := by
    rintro rfl
    rw [sub_self, addOrderOf_zero] at he
    exact absurd he (by decide)
  -- the two parts at `a`, at `b` and elsewhere
  have ha : u a + v a = 1 := by
    rw [huv]
    simp [hab]
  have hb : u b + v b = 1 := by
    rw [huv]
    simp [hab.symm]
  have hx : ∀ x, x ≠ a → x ≠ b → u x = 0 ∧ v x = 0 := by
    intro x hxa hxb
    have h := huv x
    rw [Pi.add_apply, Pi.single_eq_of_ne hxa, Pi.single_eq_of_ne hxb] at h
    omega
  -- the value of the difference of the masks at a complex number
  have hval : ∀ z : ℂ, Polynomial.aeval z (maskW u - maskW v)
      = ((u a : ℂ) - (v a : ℂ)) * z ^ a.val + ((u b : ℂ) - (v b : ℂ)) * z ^ b.val := by
    intro z
    rw [Final3Aux.aeval_sub]
    refine Fintype.sum_eq_add a b hab fun x hx' => ?_
    obtain ⟨h1, h2⟩ := hx x hx'.1 hx'.2
    simp [h1, h2]
  by_cases hsame : u a = u b
  · -- the two marks in the same part: `±(X ^ a + X ^ b)`, zero at some `ξ` with `ξ ^ n = 1`
    obtain ⟨ξ, hξn, hξ⟩ := Final3Aux.exists_root_of_even a b he
    have hpos : 0 < orderOf ξ :=
      orderOf_pos_iff.2 (isOfFinOrder_iff_pow_eq_one.2 ⟨n, Nat.pos_of_ne_zero (NeZero.ne n), hξn⟩)
    refine hno (orderOf ξ) (orderOf_dvd_of_pow_eq_one hξn)
      (Lift.TwoAux.cyclotomic_dvd_of_aeval_eq_zero _ hpos (IsPrimitiveRoot.orderOf ξ) ?_)
    have hv : v a = v b := by omega
    rw [hval, hsame, hv, ← mul_add, hξ, mul_zero]
  · -- the two marks in different parts: `±(X ^ a - X ^ b)`, zero at `1`
    refine hno 1 (one_dvd n)
      (Lift.TwoAux.cyclotomic_dvd_of_aeval_eq_zero _ one_pos IsPrimitiveRoot.one ?_)
    rw [hval]
    have hc : (u a = 1 ∧ v a = 0 ∧ u b = 0 ∧ v b = 1) ∨
        (u a = 0 ∧ v a = 1 ∧ u b = 1 ∧ v b = 0) := by
      omega
    rcases hc with ⟨h1, h2, h3, h4⟩ | ⟨h1, h2, h3, h4⟩ <;> simp [h1, h2, h3, h4]

end Pnq
