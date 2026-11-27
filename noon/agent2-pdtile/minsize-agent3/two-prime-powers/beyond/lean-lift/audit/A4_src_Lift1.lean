/-
Lemmas for `Pnq/Lift.lean` that do not mention the reduction: the value of a mask polynomial at a root of unity, the key
lemma (a multiset whose residues modulo `r^(k+1)` are all below `(r - 1) r^k`, one of them taken exactly once, has no
`Φ_{e r^(k+1)}` in its mask, `r ∤ e`), and the arithmetic of the lift (the shape of the new divisors, and the Chinese
remainder theorem in the form used).
-/
import Pnq.Weighted

open Finset

namespace Pnq

namespace Lift

namespace Aux

open Polynomial

section Mask

variable {M : ℕ} [NeZero M]

/-- the value of the mask polynomial at a complex number -/
theorem aeval_maskW (w : ZMod M → ℕ) (z : ℂ) :
    aeval z (maskW w) = ∑ y : ZMod M, (w y : ℂ) * z ^ y.val := by
  simp [maskW, map_sum]

/-- if `Φ_d` divides the mask, the mask vanishes at every primitive `d`-th root of unity -/
theorem sum_eq_zero_of_cyclotomic_dvd (w : ZMod M → ℕ) {d : ℕ} (hd : 0 < d)
    (h : cyclotomic d ℤ ∣ maskW w) {z : ℂ} (hz : IsPrimitiveRoot z d) :
    ∑ y : ZMod M, (w y : ℂ) * z ^ y.val = 0 := by
  obtain ⟨Q, hQ⟩ := h
  have h0 : aeval z (cyclotomic d ℤ) = 0 := by
    have h1 : IsRoot (cyclotomic d ℂ) z := hz.isRoot_cyclotomic hd
    rw [← map_cyclotomic d (algebraMap ℤ ℂ), IsRoot.def, eval_map_algebraMap] at h1
    exact h1
  rw [← aeval_maskW, hQ, map_mul, h0, zero_mul]

/-- **Key lemma.**  `r` a prime, `r ∤ e`.  If every element `y` of the multiset `w` has `y mod r^(k+1) < (r - 1) r^k`,
and one element `y₀` is the only one with its residue modulo `r^(k+1)`, then `Φ_{e r^(k+1)}` does not divide the mask of
`w`.  (For a primitive `e`-th root `ω`, the polynomial `∑_y w(y) ω^y Y^(y mod r^(k+1))` has degree below
`(r - 1) r^k = φ(r^(k+1))` and vanishes at every primitive `r^(k+1)`-th root of unity, so it is `0`; but its coefficient
at `y₀ mod r^(k+1)` is the single term `w(y₀) ω^y₀`.) -/
theorem not_cyclotomic_dvd_of_single (w : ZMod M → ℕ) {r : ℕ} (hr : r.Prime) (k e : ℕ)
    (he0 : e ≠ 0) (he : ¬ r ∣ e)
    (h1 : ∀ y, w y ≠ 0 → y.val % r ^ (k + 1) < (r - 1) * r ^ k)
    (y₀ : ZMod M) (hy₀ : w y₀ ≠ 0)
    (h2 : ∀ y, w y ≠ 0 → y.val % r ^ (k + 1) = y₀.val % r ^ (k + 1) → y = y₀) :
    ¬ cyclotomic (e * r ^ (k + 1)) ℤ ∣ maskW w := by
  intro hdvd
  have hRpos : 0 < r ^ (k + 1) := pow_pos hr.pos _
  have hco : e.Coprime (r ^ (k + 1)) :=
    Nat.Coprime.pow_right _ (Nat.Coprime.symm ((Nat.Prime.coprime_iff_not_dvd hr).2 he))
  obtain ⟨ω, hω⟩ : ∃ ω : ℂ, IsPrimitiveRoot ω e := ⟨_, Complex.isPrimitiveRoot_exp e he0⟩
  have hω0 : ω ≠ 0 := hω.ne_zero he0
  -- the polynomial in `Y`
  set ℓ : ℂ[X] := ∑ y : ZMod M, C ((w y : ℂ) * ω ^ y.val) * X ^ (y.val % r ^ (k + 1)) with hℓ
  -- it vanishes at every primitive `r^(k+1)`-th root of unity
  have hroot : ∀ η ∈ primitiveRoots (r ^ (k + 1)) ℂ, ℓ.eval η = 0 := by
    intro η hη
    rw [mem_primitiveRoots hRpos] at hη
    have hprim : IsPrimitiveRoot (ω * η) (e * r ^ (k + 1)) := by
      have e1 : orderOf ω = e := hω.eq_orderOf.symm
      have e2 : orderOf η = r ^ (k + 1) := hη.eq_orderOf.symm
      rw [IsPrimitiveRoot.iff_orderOf,
        (Commute.all ω η).orderOf_mul_eq_mul_orderOf_of_coprime (by rw [e1, e2]; exact hco), e1, e2]
    have hsum := sum_eq_zero_of_cyclotomic_dvd w (Nat.mul_pos (Nat.pos_of_ne_zero he0) hRpos) hdvd hprim
    rw [← hsum, hℓ, eval_finsetSum]
    refine Finset.sum_congr rfl fun y _ => ?_
    have hpow : η ^ (y.val % r ^ (k + 1)) = η ^ y.val := by
      conv_rhs => rw [← Nat.div_add_mod y.val (r ^ (k + 1)), pow_add, pow_mul, hη.pow_eq_one, one_pow, one_mul]
    rw [eval_mul, eval_C, eval_pow, eval_X, hpow, mul_pow, mul_assoc]
  -- its degree is below the number of these roots
  have hdeg : ℓ.natDegree < (primitiveRoots (r ^ (k + 1)) ℂ).card := by
    rw [Complex.card_primitiveRoots, Nat.totient_prime_pow_succ hr]
    have hpos : 0 < (r - 1) * r ^ k := Nat.mul_pos (Nat.sub_pos_of_lt hr.one_lt) (pow_pos hr.pos k)
    have hle : ℓ.natDegree ≤ (r - 1) * r ^ k - 1 := by
      refine natDegree_sum_le_of_forall_le _ _ fun y _ => ?_
      by_cases hy : w y = 0
      · simp [hy]
      · refine (natDegree_C_mul_X_pow_le _ _).trans ?_
        have := h1 y hy
        omega
    rw [mul_comm]
    omega
  have hzero : ℓ = 0 := eq_zero_of_natDegree_lt_card_of_eval_eq_zero' ℓ _ hroot hdeg
  -- but one coefficient is a single term
  have hcoeff : ℓ.coeff (y₀.val % r ^ (k + 1)) = (w y₀ : ℂ) * ω ^ y₀.val := by
    rw [hℓ, finsetSum_coeff, Finset.sum_eq_single y₀]
    · rw [coeff_C_mul_X_pow, ite_eq_left rfl]
    · intro y _ hy
      rw [coeff_C_mul_X_pow]
      by_cases hwy : w y = 0
      · simp [hwy]
      · rw [ite_eq_right]
        intro hβ
        exact hy (h2 y hwy hβ.symm)
    · intro h
      exact absurd (Finset.mem_univ _) h
  rw [hzero, coeff_zero] at hcoeff
  exact mul_ne_zero (Nat.cast_ne_zero.2 hy₀) (pow_ne_zero _ hω0) hcoeff.symm

end Mask

/-- a divisor of `r^k N' r` that does not divide `r^k N'`, where `r ∤ N'`, is `e r^(k+1)` with `r ∤ e` -/
theorem exists_eq_mul_pow {r : ℕ} (hr : r.Prime) {k N' d : ℕ} (hN' : ¬ r ∣ N')
    (hd : d ∣ r ^ k * N' * r) (hnd : ¬ d ∣ r ^ k * N') :
    ∃ e, e ≠ 0 ∧ ¬ r ∣ e ∧ d = e * r ^ (k + 1) := by
  have hN'0 : N' ≠ 0 := by
    rintro rfl
    exact hN' (dvd_zero r)
  have hd0 : d ≠ 0 := by
    rintro rfl
    have h0 : r ^ k * N' * r = 0 := zero_dvd_iff.1 hd
    exact Nat.mul_ne_zero (Nat.mul_ne_zero (pow_ne_zero k hr.ne_zero) hN'0) hr.ne_zero h0
  obtain ⟨j, e, he, rfl⟩ := Nat.exists_eq_pow_mul_and_not_dvd hd0 r hr.ne_one
  have hcop : Nat.Coprime r e := (Nat.Prime.coprime_iff_not_dvd hr).2 he
  have heq : r ^ k * N' * r = r ^ (k + 1) * N' := by ring
  rw [heq] at hd
  have heN : e ∣ N' :=
    (Nat.Coprime.pow_right (k + 1) hcop.symm).dvd_of_dvd_mul_left ((dvd_mul_left e (r ^ j)).trans hd)
  have hj : j ≤ k + 1 := by
    have h2 : r ^ j ∣ r ^ (k + 1) :=
      (Nat.Coprime.pow_left j ((Nat.Prime.coprime_iff_not_dvd hr).2 hN')).dvd_of_dvd_mul_right
        ((dvd_mul_right (r ^ j) e).trans hd)
    exact (Nat.pow_dvd_pow_iff_le_right hr.one_lt).1 h2
  have hj' : j = k + 1 := by
    by_contra hne
    have hjk : j ≤ k := by omega
    exact hnd (Nat.mul_dvd_mul (pow_dvd_pow r hjk) heN)
  subst hj'
  exact ⟨e, fun h => he (h ▸ dvd_zero r), he, mul_comm _ _⟩

/-- the Chinese remainder theorem in the form used: a number congruent to `a` modulo `r^k N'` whose residue modulo
`r^(k+1)` is `a mod r^k + t r^k` -/
theorem exists_crt {r : ℕ} (hr : r.Prime) (k : ℕ) {N' : ℕ} (hN' : ¬ r ∣ N') (a t : ℕ) (ht : t + 1 ≤ r) :
    ∃ c : ℕ, c ≡ a [MOD r ^ k * N'] ∧ c % r ^ (k + 1) = a % r ^ k + t * r ^ k := by
  have hco : (r ^ (k + 1)).Coprime N' := Nat.Coprime.pow_left _ ((Nat.Prime.coprime_iff_not_dvd hr).2 hN')
  have hco' : (r ^ k).Coprime N' := Nat.Coprime.pow_left _ ((Nat.Prime.coprime_iff_not_dvd hr).2 hN')
  obtain ⟨c, hc1, hc2⟩ := Nat.chineseRemainder hco (a % r ^ k + t * r ^ k) a
  have hrk : 0 < r ^ k := pow_pos hr.pos k
  have hlt : a % r ^ k + t * r ^ k < r ^ (k + 1) := by
    have h1 : a % r ^ k < r ^ k := Nat.mod_lt _ hrk
    calc a % r ^ k + t * r ^ k < r ^ k + t * r ^ k := by omega
      _ = (t + 1) * r ^ k := by ring
      _ ≤ r * r ^ k := Nat.mul_le_mul_right _ ht
      _ = r ^ (k + 1) := by ring
  refine ⟨c, ?_, ?_⟩
  · refine (Nat.modEq_and_modEq_iff_modEq_mul hco').1 ⟨?_, hc2⟩
    have h3 : c ≡ a % r ^ k + t * r ^ k [MOD r ^ k] := hc1.of_dvd (pow_dvd_pow r (Nat.le_succ k))
    refine h3.trans ?_
    unfold Nat.ModEq
    rw [Nat.add_mul_mod_self_right, Nat.mod_mod]
  · exact (show c % r ^ (k + 1) = (a % r ^ k + t * r ^ k) % r ^ (k + 1) from hc1).trans (Nat.mod_eq_of_lt hlt)

end Aux

end Lift

end Pnq
