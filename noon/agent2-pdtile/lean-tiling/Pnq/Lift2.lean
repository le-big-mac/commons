/-
Lifting along the prime 2.  If `N = 2^k * (p^a * q^b)` with odd primes `p ≠ q`, a nonempty multiset on `ZMod N` can be lifted to
`ZMod (N * 2)` with the same number of elements and exactly the same cyclotomic divisors of its mask polynomial.  So the sizes of
the multisets with exactly a given pattern of divisors of `N` are the same on `ZMod N` and on `ZMod (N * 2)`.
(Statements fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of them.  On paper: the lift is read off from a
signing, by the lemma on signs, of the elements in one class modulo `2^k`.)
-/
import Pnq.Lift
import Pnq.Sign

open Finset

namespace Pnq

namespace Lift

namespace TwoAux

open Polynomial

/-- for `η` with `η ^ 2^k = -1`, the power `η ^ n` is `η ^ (n mod 2^k)` up to the sign `(-1) ^ (n / 2^k)` -/
theorem pow_eq_neg_one_pow_mul {η : ℂ} {k : ℕ} (hη : η ^ 2 ^ k = -1) (n : ℕ) :
    η ^ n = (-1) ^ (n / 2 ^ k) * η ^ (n % 2 ^ k) := by
  conv_lhs => rw [← Nat.div_add_mod n (2 ^ k), pow_add, pow_mul, hη]

/-- a root of unity of order `2^(k+1)` has `η ^ 2^k = -1` -/
theorem pow_two_pow_eq_neg_one {η : ℂ} {k : ℕ} (hη : IsPrimitiveRoot η (2 ^ (k + 1))) :
    η ^ 2 ^ k = -1 := by
  have h := hη.pow_of_dvd (pow_ne_zero k two_ne_zero) (pow_dvd_pow 2 (Nat.le_succ k))
  have h2 : 2 ^ (k + 1) / 2 ^ k = 2 := by
    rw [pow_succ, Nat.mul_div_cancel_left _ (pow_pos two_pos k)]
  rw [h2] at h
  exact h.eq_neg_one_of_two_right

/-- if the value at a primitive `e`-th root of unity is `0`, then `Φ_e` divides -/
theorem cyclotomic_dvd_of_aeval_eq_zero (P : ℤ[X]) {e : ℕ} (he : 0 < e) {ω : ℂ}
    (hω : IsPrimitiveRoot ω e) (h : aeval ω P = 0) : cyclotomic e ℤ ∣ P := by
  rw [cyclotomic_eq_minpoly hω he]
  exact minpoly.isIntegrallyClosed_dvd (hω.isIntegral he) h

/-- **Key lemma.**  `e` odd, `ω` a root of unity of order `e`.  If `Φ_{e 2^(k+1)}` divides the mask of `w`, then for every
class `c` modulo `2^k` the sum of `(-1) ^ (y / 2^k) ω ^ y` over the elements `y` of `w` in that class is `0`.  (The
polynomial `∑_y w(y) (-1)^(y / 2^k) ω^y Y^(y mod 2^k)` has degree below `2^k` and vanishes at the `2^k` roots of unity of
order `2^(k+1)`, so it is `0`; the sum is its coefficient at `c`.) -/
theorem class_sum_eq_zero {M : ℕ} [NeZero M] (w : ZMod M → ℕ) (k e : ℕ) (he0 : e ≠ 0) (he : ¬ 2 ∣ e)
    (hdvd : cyclotomic (e * 2 ^ (k + 1)) ℤ ∣ maskW w) {ω : ℂ} (hω : IsPrimitiveRoot ω e) (c : ℕ) :
    ∑ y : ZMod M, (w y : ℂ) *
      (if y.val % 2 ^ k = c then (-1 : ℂ) ^ (y.val / 2 ^ k) * ω ^ y.val else 0) = 0 := by
  have hRpos : 0 < 2 ^ (k + 1) := pow_pos two_pos _
  have hco : e.Coprime (2 ^ (k + 1)) :=
    Nat.Coprime.pow_right _ (Nat.Coprime.symm ((Nat.Prime.coprime_iff_not_dvd Nat.prime_two).2 he))
  -- the polynomial in `Y`
  set ℓ : ℂ[X] := ∑ y : ZMod M,
    C ((w y : ℂ) * ((-1 : ℂ) ^ (y.val / 2 ^ k) * ω ^ y.val)) * X ^ (y.val % 2 ^ k) with hℓ
  -- it vanishes at every root of unity of order `2^(k+1)`
  have hroot : ∀ η ∈ primitiveRoots (2 ^ (k + 1)) ℂ, ℓ.eval η = 0 := by
    intro η hη
    rw [mem_primitiveRoots hRpos] at hη
    have hprim : IsPrimitiveRoot (ω * η) (e * 2 ^ (k + 1)) := by
      have e1 : orderOf ω = e := hω.eq_orderOf.symm
      have e2 : orderOf η = 2 ^ (k + 1) := hη.eq_orderOf.symm
      rw [IsPrimitiveRoot.iff_orderOf,
        (Commute.all ω η).orderOf_mul_eq_mul_orderOf_of_coprime (by rw [e1, e2]; exact hco), e1, e2]
    have hsum := Aux.sum_eq_zero_of_cyclotomic_dvd w (Nat.mul_pos (Nat.pos_of_ne_zero he0) hRpos) hdvd hprim
    rw [← hsum, hℓ, eval_finsetSum]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [eval_mul, eval_C, eval_pow, eval_X, mul_pow,
      pow_eq_neg_one_pow_mul (pow_two_pow_eq_neg_one hη) y.val]
    ring
  -- its degree is below the number of these roots
  have hdeg : ℓ.natDegree < (primitiveRoots (2 ^ (k + 1)) ℂ).card := by
    rw [Complex.card_primitiveRoots, Nat.totient_prime_pow_succ Nat.prime_two]
    have hpos : 0 < 2 ^ k := pow_pos two_pos k
    have hle : ℓ.natDegree ≤ 2 ^ k - 1 := by
      refine natDegree_sum_le_of_forall_le _ _ fun y _ => ?_
      refine (natDegree_C_mul_X_pow_le _ _).trans ?_
      have := Nat.mod_lt y.val hpos
      omega
    omega
  have hzero : ℓ = 0 := eq_zero_of_natDegree_lt_card_of_eval_eq_zero' ℓ _ hroot hdeg
  -- the sum is its coefficient at `c`
  have hcoeff : ℓ.coeff c = ∑ y : ZMod M, (w y : ℂ) *
      (if y.val % 2 ^ k = c then (-1 : ℂ) ^ (y.val / 2 ^ k) * ω ^ y.val else 0) := by
    rw [hℓ, finsetSum_coeff]
    refine Finset.sum_congr rfl fun y _ => ?_
    rw [coeff_C_mul_X_pow]
    by_cases h : y.val % 2 ^ k = c
    · rw [ite_eq_left h, ite_eq_left h.symm]
    · rw [ite_eq_right h, ite_eq_right (Ne.symm h), mul_zero]
  rw [← hcoeff, hzero, coeff_zero]

/-- a sum against `push L v` is a sum over the points `L x` -/
theorem sum_push {N r : ℕ} [NeZero N] [Fact r.Prime] {L : ZMod N → ZMod (N * r)}
    (hL : ∀ x, ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) (L x) = x) (v : ZMod N → ℕ)
    (g : ZMod (N * r) → ℂ) :
    ∑ y, (Aux.push L v y : ℂ) * g y = ∑ x, (v x : ℂ) * g (L x) := by
  have h : ∀ y : ZMod (N * r), (Aux.push L v y : ℂ) * g y
      = ∑ x, if y = L x then (v x : ℂ) * g (L x) else 0 := by
    intro y
    rw [Finset.sum_eq_single (ZMod.castHom (Nat.dvd_mul_right N r) (ZMod N) y)]
    · unfold Aux.push
      split_ifs with h1
      · rw [← h1]
      · simp
    · intro x _ hx
      rw [ite_eq_right]
      intro hy
      apply hx
      rw [hy, hL]
    · intro h
      exact absurd (Finset.mem_univ _) h
  rw [Finset.sum_congr rfl fun y _ => h y, Finset.sum_comm]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [Finset.sum_ite_eq' Finset.univ (L x), ite_eq_left (Finset.mem_univ _)]

/-- the arithmetic of a lift: if `n mod 2^(k+1)` is `m mod 2^k + t 2^k`, then `n` and `m` are in the same class modulo
`2^k`, and `n / 2^k` has the parity of `t` -/
theorem mod_and_div_of_section {k n m t : ℕ} (h : n % 2 ^ (k + 1) = m % 2 ^ k + t * 2 ^ k) :
    n % 2 ^ k = m % 2 ^ k ∧ n / 2 ^ k % 2 = t := by
  have hpos : 0 < 2 ^ k := pow_pos two_pos k
  constructor
  · rw [← Nat.mod_mod_of_dvd n (pow_dvd_pow 2 (Nat.le_succ k)), h, Nat.add_mul_mod_self_right, Nat.mod_mod]
  · rw [← Nat.mod_mul_right_div_self, ← pow_succ, h, Nat.add_mul_div_right _ _ hpos,
      Nat.div_eq_of_lt (Nat.mod_lt _ hpos), zero_add]

/-- The Chinese remainder theorem in the form used: for `N = 2^k N'`, `N'` odd, and a class `c` modulo `2^k`, the
elements of `ZMod N` in the class `c` correspond one to one to `ZMod N'` by reduction modulo `N'`. -/
theorem exists_class_section {N : ℕ} [NeZero N] (k N' : ℕ) [NeZero N'] (hN : N = 2 ^ k * N')
    (hN' : ¬ 2 ∣ N') (c : ℕ) (hc : c < 2 ^ k) :
    ∃ σ : ZMod N' → ZMod N, (∀ z, (σ z).val % 2 ^ k = c) ∧ (∀ z, (((σ z).val : ℕ) : ZMod N') = z) ∧
      ∀ x : ZMod N, x.val % 2 ^ k = c → σ ((x.val : ℕ) : ZMod N') = x := by
  have hco : (2 ^ k).Coprime N' :=
    Nat.Coprime.pow_left _ ((Nat.Prime.coprime_iff_not_dvd Nat.prime_two).2 hN')
  have hkN : 2 ^ k ∣ N := ⟨N', hN⟩
  have hN'N : N' ∣ N := ⟨2 ^ k, by rw [hN, mul_comm]⟩
  have key : ∀ z : ZMod N', ∃ x : ZMod N, x.val % 2 ^ k = c ∧ ((x.val : ℕ) : ZMod N') = z := by
    intro z
    obtain ⟨m, hm1, hm2⟩ := Nat.chineseRemainder hco c z.val
    refine ⟨(m : ZMod N), ?_, ?_⟩
    · rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ hkN]
      exact (show m % 2 ^ k = c % 2 ^ k from hm1).trans (Nat.mod_eq_of_lt hc)
    · rw [ZMod.val_natCast]
      have h3 : m % N ≡ z.val [MOD N'] := ((Nat.mod_modEq m N).of_dvd hN'N).trans hm2
      exact ((ZMod.natCast_eq_natCast_iff _ _ N').2 h3).trans (ZMod.natCast_zmod_val z)
  choose σ h1 h2 using key
  refine ⟨σ, h1, h2, fun x hx => ?_⟩
  have e1 : (σ ((x.val : ℕ) : ZMod N')).val ≡ x.val [MOD 2 ^ k] := (h1 _).trans hx.symm
  have e2 : (σ ((x.val : ℕ) : ZMod N')).val ≡ x.val [MOD N'] :=
    (ZMod.natCast_eq_natCast_iff _ _ N').1 (h2 _)
  have e3 : (σ ((x.val : ℕ) : ZMod N')).val ≡ x.val [MOD 2 ^ k * N'] :=
    (Nat.modEq_and_modEq_iff_modEq_mul hco).1 ⟨e1, e2⟩
  rw [← hN] at e3
  have e4 := (ZMod.natCast_eq_natCast_iff _ _ N).2 e3
  rwa [ZMod.natCast_zmod_val, ZMod.natCast_zmod_val] at e4

/-- a sum over the class `c` modulo `2^k` of a function of the residue modulo `N'` is a sum over `ZMod N'` -/
theorem sum_class {N : ℕ} [NeZero N] (k N' : ℕ) [NeZero N'] (hN : N = 2 ^ k * N') (hN' : ¬ 2 ∣ N')
    (c : ℕ) (hc : c < 2 ^ k) (g : ZMod N' → ℂ) :
    ∑ x : ZMod N, (if x.val % 2 ^ k = c then g ((x.val : ℕ) : ZMod N') else 0) = ∑ z : ZMod N', g z := by
  obtain ⟨σ, h1, h2, h3⟩ := exists_class_section (N := N) k N' hN hN' c hc
  symm
  refine Fintype.sum_of_injective σ ?_ _ _ ?_ ?_
  · intro z z' h
    rw [← h2 z, ← h2 z', h]
  · intro x hx
    rw [ite_eq_right]
    intro hxc
    exact hx ⟨_, h3 x hxc⟩
  · intro z
    rw [ite_eq_left (h1 z), h2 z]

/-- **Lifting along 2, from a signing.**  `N = 2^k N'` with `N'` odd.  If every nonempty multiset on `ZMod N'` can be
split into two parts `u`, `v` such that no `Φ_e`, `e ∣ N'`, divides `maskW u - maskW v`, then every nonempty multiset on
`ZMod N` is the reduction of a multiset on `ZMod (N * 2)` whose mask is divisible by no `Φ_d` with `d ∣ N * 2`, `d ∤ N`.
(Fix a class `c` modulo `2^k` that holds an element; the elements of that class counted by `u` go to their lifts with
residue below `2^k` modulo `2^(k+1)`, those counted by `v` to the other lift; the elements of the other classes go to
their lifts with residue below `2^k`.) -/
theorem exists_lift_two_aux {N : ℕ} [NeZero N] (k N' : ℕ) [NeZero N'] (hN : N = 2 ^ k * N')
    (hN' : ¬ 2 ∣ N')
    (hsigns : ∀ B : ZMod N' → ℕ, (∃ z, B z ≠ 0) → ∃ u v : ZMod N' → ℕ, (∀ z, u z + v z = B z) ∧
      ∀ e, e ∣ N' → ¬ cyclotomic e ℤ ∣ maskW u - maskW v)
    (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ cyclotomic d ℤ ∣ maskW w' := by
  obtain ⟨x₀, hx₀⟩ := hw
  have hpos : 0 < 2 ^ k := pow_pos two_pos k
  have hN'N : N' ∣ N := ⟨2 ^ k, by rw [hN, mul_comm]⟩
  -- the class of `x₀`
  obtain ⟨c, hc⟩ : ∃ c, x₀.val % 2 ^ k = c := ⟨_, rfl⟩
  have hclt : c < 2 ^ k := hc ▸ Nat.mod_lt _ hpos
  obtain ⟨σ, -, -, hσ3⟩ := exists_class_section (N := N) k N' hN hN' c hclt
  -- the signs on that class
  obtain ⟨u, v, huv, hno⟩ := hsigns (fun z => w (σ z))
    ⟨((x₀.val : ℕ) : ZMod N'), by rw [hσ3 x₀ hc]; exact hx₀⟩
  -- the two lifts of each element
  obtain ⟨L₀, hL₀, hβ₀⟩ := Aux.exists_section (N := N) (r := 2) k N' hN hN' 0 (by omega)
  obtain ⟨L₁, hL₁, hβ₁⟩ := Aux.exists_section (N := N) (r := 2) k N' hN hN' 1 (by omega)
  -- the elements that go low, and those that go high
  obtain ⟨u', hu'⟩ : ∃ u' : ZMod N → ℕ, ∀ x, u' x =
      if x.val % 2 ^ k = c then u ((x.val : ℕ) : ZMod N') else w x := ⟨_, fun _ => rfl⟩
  obtain ⟨v', hv'⟩ : ∃ v' : ZMod N → ℕ, ∀ x, v' x =
      if x.val % 2 ^ k = c then v ((x.val : ℕ) : ZMod N') else 0 := ⟨_, fun _ => rfl⟩
  refine ⟨Aux.push L₀ u' + Aux.push L₁ v', ?_, fun d hd hnd hdvd => ?_⟩
  · -- the reduction is `w`
    rw [Aux.reduce_add, Aux.reduce_push hL₀, Aux.reduce_push hL₁]
    funext x
    rw [Pi.add_apply, hu', hv']
    by_cases hx : x.val % 2 ^ k = c
    · rw [ite_eq_left hx, ite_eq_left hx, huv, hσ3 x hx]
    · rw [ite_eq_right hx, ite_eq_right hx, add_zero]
  · -- no new cyclotomic divisor
    have hd' : d ∣ 2 ^ k * N' * 2 := by
      rw [← hN]
      exact hd
    have hnd' : ¬ d ∣ 2 ^ k * N' := by
      rw [← hN]
      exact hnd
    obtain ⟨e, he0, he, rfl⟩ := Aux.exists_eq_mul_pow Nat.prime_two hN' hd' hnd'
    have heN' : e ∣ N' := by
      have h : 2 ^ k * N' * 2 = N' * 2 ^ (k + 1) := by ring
      rw [h] at hd'
      exact Nat.dvd_of_mul_dvd_mul_right (pow_pos two_pos _) hd'
    obtain ⟨ω, hω⟩ : ∃ ω : ℂ, IsPrimitiveRoot ω e := ⟨_, Complex.isPrimitiveRoot_exp e he0⟩
    have hωN' : ω ^ N' = 1 := by
      obtain ⟨f, hf⟩ := heN'
      rw [hf, pow_mul, hω.pow_eq_one, one_pow]
    refine hno e heN' (cyclotomic_dvd_of_aeval_eq_zero _ (Nat.pos_of_ne_zero he0) hω ?_)
    -- the sum over the class `c`
    have hkey := class_sum_eq_zero (Aux.push L₀ u' + Aux.push L₁ v') k e he0 he hdvd hω c
    -- the weight at a lift `L x` with `t = 0` or `t = 1`
    have hG : ∀ (L : ZMod N → ZMod (N * 2)) (t : ℕ),
        (∀ x, ZMod.castHom (Nat.dvd_mul_right N 2) (ZMod N) (L x) = x) →
        (∀ x, (L x).val % 2 ^ (k + 1) = x.val % 2 ^ k + t * 2 ^ k) → ∀ x : ZMod N,
        (if (L x).val % 2 ^ k = c then (-1 : ℂ) ^ ((L x).val / 2 ^ k) * ω ^ (L x).val else 0)
          = if x.val % 2 ^ k = c then (-1 : ℂ) ^ t * ω ^ (((x.val : ℕ) : ZMod N')).val else 0 := by
      intro L t hL hβ x
      obtain ⟨m1, m2⟩ := mod_and_div_of_section (hβ x)
      have m3 : (L x).val % N = x.val := by
        rw [← Aux.val_castHom, hL]
      have m4 : ω ^ (L x).val = ω ^ (((x.val : ℕ) : ZMod N')).val := by
        rw [ZMod.val_natCast, ← m3, Nat.mod_mod_of_dvd _ hN'N]
        exact pow_eq_pow_mod _ hωN'
      rw [m1, neg_one_pow_eq_pow_mod_two, m2, m4]
    have h0 := sum_push hL₀ u'
      (fun y => if y.val % 2 ^ k = c then (-1 : ℂ) ^ (y.val / 2 ^ k) * ω ^ y.val else 0)
    have h1 := sum_push hL₁ v'
      (fun y => if y.val % 2 ^ k = c then (-1 : ℂ) ^ (y.val / 2 ^ k) * ω ^ y.val else 0)
    simp only [hG L₀ 0 hL₀ hβ₀] at h0
    simp only [hG L₁ 1 hL₁ hβ₁] at h1
    simp only [Pi.add_apply, Nat.cast_add, add_mul, Finset.sum_add_distrib] at hkey
    rw [h0, h1, ← Finset.sum_add_distrib] at hkey
    -- the same sum, over `ZMod N'`
    have hsum : ∑ z : ZMod N', ((u z : ℂ) - (v z : ℂ)) * ω ^ z.val = 0 := by
      rw [← sum_class (N := N) k N' hN hN' c hclt]
      refine Eq.trans (Finset.sum_congr rfl fun x _ => ?_) hkey
      rw [hu', hv']
      by_cases hx : x.val % 2 ^ k = c
      · simp only [hx, ↓reduceIte]
        ring
      · simp only [hx, ↓reduceIte]
        ring
    rw [map_sub, Aux.aeval_maskW, Aux.aeval_maskW, ← Finset.sum_sub_distrib]
    refine Eq.trans (Finset.sum_congr rfl fun z _ => ?_) hsum
    ring

end TwoAux

/-- **The lemma on lifts for the prime 2**, for `N` whose odd part is `p^a * q^b`. -/
theorem exists_lift_two {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q)
    (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b)) (w : ZMod N → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ w' : ZMod (N * 2) → ℕ, reduce w' = w ∧
      ∀ d, d ∣ N * 2 → ¬ d ∣ N → ¬ Polynomial.cyclotomic d ℤ ∣ maskW w' := by
  have hpp : p.Prime := Fact.out
  have hqp : q.Prime := Fact.out
  have hN' : ¬ 2 ∣ p ^ a * q ^ b := by
    intro h
    rcases (Nat.Prime.dvd_mul Nat.prime_two).1 h with h | h
    · exact hp ((Nat.prime_dvd_prime_iff_eq Nat.prime_two hpp).1 (Nat.prime_two.dvd_of_dvd_pow h)).symm
    · exact hq ((Nat.prime_dvd_prime_iff_eq Nat.prime_two hqp).1 (Nat.prime_two.dvd_of_dvd_pow h)).symm
  exact TwoAux.exists_lift_two_aux k (p ^ a * q ^ b) hN hN'
    (fun B hB => exists_signs p q hp hq hpq a b B hB) w hw

/-- **Sizes are the same, for the prime 2.** -/
theorem sizes_eq_two {N : ℕ} [NeZero N] (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q)
    (k a b : ℕ) (hN : N = 2 ^ k * (p ^ a * q ^ b)) (P : Finset ℕ) (hP : ∀ d ∈ P, d ∣ N) :
    {s | ∃ w' : ZMod (N * 2) → ℕ, ∑ y, w' y = s ∧ 0 < s ∧
        ∀ d, d ∣ N * 2 → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w' ↔ d ∈ P)} =
    {s | ∃ w : ZMod N → ℕ, ∑ x, w x = s ∧ 0 < s ∧
        ∀ d, d ∣ N → d ≠ 1 → (Polynomial.cyclotomic d ℤ ∣ maskW w ↔ d ∈ P)} := by
  ext s
  simp only [Set.mem_ofPred_eq]
  constructor
  · rintro ⟨w', hs, hpos, hpat⟩
    refine ⟨reduce w', (sum_reduce w').trans hs, hpos, fun d hd hd1 => ?_⟩
    rw [cyclotomic_dvd_reduce_iff w' d hd]
    exact hpat d (Dvd.dvd.mul_right hd 2) hd1
  · rintro ⟨w, hs, hpos, hpat⟩
    have hw : ∃ x, w x ≠ 0 := Aux.exists_ne_zero_of_sum_pos w (hs ▸ hpos)
    obtain ⟨w', hred, hnew⟩ := exists_lift_two p q hp hq hpq k a b hN w hw
    subst hred
    refine ⟨w', (sum_reduce w').symm.trans hs, hpos, fun d hd hd1 => ?_⟩
    by_cases hdN : d ∣ N
    · rw [← cyclotomic_dvd_reduce_iff w' d hdN]
      exact hpat d hdN hd1
    · exact iff_of_false (hnew d hd hdN) fun h => hdN (hP d h)

end Lift

end Pnq
