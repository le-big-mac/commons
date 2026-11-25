/-
The bridge from Fourier zeros to residue-class counts in `ZMod M` (see `ZeroDefs.lean`).
-/
import Pqr.ZeroDefs

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

/-! Helper lemmas live in the namespace `Pqr.Bridge`, so that their names cannot clash with those of the
other files of the project. -/

namespace Bridge

/-! ### Arithmetic of the order -/

theorem dvd_mul_iff_div_gcd_dvd (M x j : ℕ) (hM : M ≠ 0) : M ∣ x * j ↔ M / x.gcd M ∣ j := by
  rw [Nat.div_dvd_iff_dvd_mul (Nat.gcd_dvd_right x M) (Nat.gcd_pos_of_pos_right x (Nat.pos_of_ne_zero hM))]
  constructor
  · intro h
    have h2 := Nat.dvd_gcd h (dvd_mul_right M j)
    rwa [Nat.gcd_mul_right] at h2
  · intro h
    exact h.trans (Nat.mul_dvd_mul_right (Nat.gcd_dvd_left x M) j)

/-- `ξ * j = 0` in `ZMod M` iff the order of `ξ` divides `j`. -/
theorem mul_natCast_eq_zero_iff (ξ : ZMod M) (j : ℕ) : ξ * (j : ZMod M) = 0 ↔ ord ξ ∣ j := by
  have h1 : ξ * (j : ZMod M) = ((ξ.val * j : ℕ) : ZMod M) := by
    rw [Nat.cast_mul, ZMod.natCast_zmod_val]
  rw [h1, ZMod.natCast_eq_zero_iff, ord]
  exact dvd_mul_iff_div_gcd_dvd M ξ.val j (NeZero.ne M)

omit [NeZero M] in
theorem ord_dvd (ξ : ZMod M) : ord ξ ∣ M := Nat.div_dvd_of_dvd (Nat.gcd_dvd_right _ _)

/-! ### Sums over the multiples of a divisor of `M` -/

/-- A sum over the elements of `ZMod M` whose representative is a multiple of `j`, parametrised. -/
theorem sum_dvd_val (j : ℕ) (hj : j ∣ M) (G : ZMod M → ℂ) :
    ∑ t : ZMod M, (if j ∣ t.val then G t else 0)
      = ∑ s ∈ range (M / j), G ((j * s : ℕ) : ZMod M) := by
  have hM : 0 < M := Nat.pos_of_ne_zero (NeZero.ne M)
  have hj0 : 0 < j := Nat.pos_of_dvd_of_pos hj hM
  have hlt : ∀ s ∈ range (M / j), j * s < M := by
    intro s hs
    calc j * s < j * (M / j) := Nat.mul_lt_mul_of_pos_left (mem_range.1 hs) hj0
      _ = M := Nat.mul_div_cancel' hj
  rw [← Finset.sum_filter]
  symm
  refine Finset.sum_nbij' (fun s => ((j * s : ℕ) : ZMod M)) (fun t => t.val / j) ?_ ?_ ?_ ?_ ?_
  · intro s hs
    rw [mem_filter]
    refine ⟨mem_univ _, ?_⟩
    rw [ZMod.val_natCast, Nat.mod_eq_of_lt (hlt s hs)]
    exact dvd_mul_right j s
  · intro t ht
    rw [mem_range]
    exact Nat.div_lt_div_of_lt_of_dvd hj (ZMod.val_lt t)
  · intro s hs
    rw [ZMod.val_natCast, Nat.mod_eq_of_lt (hlt s hs), Nat.mul_div_cancel_left s hj0]
  · intro t ht
    rw [Nat.mul_div_cancel' (mem_filter.1 ht).2, ZMod.natCast_zmod_val]
  · intro s _
    rfl

/-- The sum of a character of `ZMod M` over the multiples of `j`. -/
theorem sum_char_multiples (j : ℕ) (hj : j ∣ M) (η : ZMod M) :
    ∑ t : ZMod M, (if j ∣ t.val then ZMod.stdAddChar (η * t) else 0)
      = if η * (j : ZMod M) = 0 then ((M / j : ℕ) : ℂ) else 0 := by
  rw [sum_dvd_val j hj]
  have hpow : ∀ s : ℕ, ZMod.stdAddChar (η * ((j * s : ℕ) : ZMod M))
      = ZMod.stdAddChar (η * (j : ZMod M)) ^ s := by
    intro s
    rw [← AddChar.map_nsmul_eq_pow, nsmul_eq_mul]
    congr 1
    push_cast
    ring
  simp_rw [hpow]
  split_ifs with h
  · simp [h]
  · have hz : ZMod.stdAddChar (η * (j : ZMod M)) ≠ 1 := by
      intro h1
      apply h
      rw [← AddChar.map_zero_eq_one (ZMod.stdAddChar (N := M))] at h1
      exact ZMod.injective_stdAddChar h1
    have hzM : ZMod.stdAddChar (η * (j : ZMod M)) ^ (M / j) = 1 := by
      rw [← AddChar.map_nsmul_eq_pow, nsmul_eq_mul]
      have h0 : ((M / j : ℕ) : ZMod M) * (η * (j : ZMod M)) = 0 := by
        calc ((M / j : ℕ) : ZMod M) * (η * (j : ZMod M))
            = η * ((j * (M / j) : ℕ) : ZMod M) := by push_cast; ring
          _ = 0 := by rw [Nat.mul_div_cancel' hj, ZMod.natCast_self, mul_zero]
      rw [h0, AddChar.map_zero_eq_one]
    have hgeom := geom_sum_mul (ZMod.stdAddChar (η * (j : ZMod M))) (M / j)
    rw [hzM, sub_self] at hgeom
    exact (mul_eq_zero.1 hgeom).resolve_right (sub_ne_zero.2 hz)

/-! ### (1) The transform of a count function -/

theorem sum_cnt_mul_char (A : Finset (ZMod M)) (j : ℕ) (hj : j ∣ M) (ξ : ZMod M) :
    ∑ v : ZMod M, (cnt A j v : ℂ) * ZMod.stdAddChar (ξ * v)
      = hat A ξ * (if ord ξ ∣ j then ((M / j : ℕ) : ℂ) else 0) := by
  have h1 : ∀ v : ZMod M, (cnt A j v : ℂ) * ZMod.stdAddChar (ξ * v)
      = ∑ a ∈ A, (if j ∣ (a - v).val then ZMod.stdAddChar (ξ * v) else 0) := by
    intro v
    rw [cnt, Finset.card_filter, Nat.cast_sum, Finset.sum_mul]
    refine Finset.sum_congr rfl fun a _ => ?_
    split_ifs <;> simp
  simp_rw [h1]
  rw [Finset.sum_comm, hat, Finset.sum_mul]
  refine Finset.sum_congr rfl fun a _ => ?_
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
  rw [← Finset.mul_sum, sum_char_multiples j hj]
  simp only [neg_mul, neg_eq_zero, mul_natCast_eq_zero_iff]

/-! ### Fourier uniqueness on `ZMod M` -/

theorem fourier_uniq_zmod (g : ZMod M → ℂ)
    (h : ∀ ξ : ZMod M, ∑ v, g v * ZMod.stdAddChar (ξ * v) = 0) : g = 0 := by
  classical
  funext w
  have hterm : ∀ v, ∑ ξ : ZMod M, ZMod.stdAddChar (-(ξ * w)) * (g v * ZMod.stdAddChar (ξ * v))
      = g v * (if v - w = 0 then (Fintype.card (ZMod M) : ℂ) else 0) := by
    intro v
    have hs := AddChar.sum_mulShift (R' := ℂ) (v - w) (ZMod.isPrimitive_stdAddChar M)
    rw [show (if v - w = 0 then (Fintype.card (ZMod M) : ℂ) else 0)
        = ((if v - w = 0 then Fintype.card (ZMod M) else 0 : ℕ) : ℂ) by split_ifs <;> simp,
      ← hs, Finset.mul_sum]
    refine Finset.sum_congr rfl fun ξ _ => ?_
    rw [mul_sub, sub_eq_add_neg, AddChar.map_add_eq_mul]
    ring
  have key : ∑ ξ : ZMod M, ZMod.stdAddChar (-(ξ * w)) * ∑ v, g v * ZMod.stdAddChar (ξ * v)
      = g w * Fintype.card (ZMod M) := by
    simp_rw [Finset.mul_sum]
    rw [Finset.sum_comm]
    simp_rw [hterm, sub_eq_zero]
    simp
  have h0 : g w * Fintype.card (ZMod M) = 0 := by
    rw [← key]
    simp [h]
  have hc : (Fintype.card (ZMod M) : ℂ) ≠ 0 := Nat.cast_ne_zero.2 Fintype.card_ne_zero
  exact (mul_eq_zero.1 h0).resolve_right hc

/-! ### (2) The bridge -/

/-- The bridge, for a family of divisors indexed by an arbitrary type (repetitions allowed). -/
theorem zeroAt_iff_cnt_aux {ι : Type*} (A : Finset (ZMod M)) (d : ℕ) (s : Finset ι) (J : ι → ℕ)
    (c : ι → ℤ) (hS : ∀ i ∈ s, J i ∣ M)
    (hc : ∀ e, e ∣ M → (∑ i ∈ s, if e ∣ J i then c i else 0) = if e = d then 1 else 0) :
    ZeroAt A d ↔ ∀ v : ZMod M, ∑ i ∈ s, c i * (J i : ℤ) * (cnt A (J i) v : ℤ) = 0 := by
  have hM : (M : ℂ) ≠ 0 := Nat.cast_ne_zero.2 (NeZero.ne M)
  have key : ∀ ξ : ZMod M,
      ∑ v : ZMod M, ((∑ i ∈ s, c i * (J i : ℤ) * (cnt A (J i) v : ℤ) : ℤ) : ℂ)
          * ZMod.stdAddChar (ξ * v)
        = hat A ξ * M * (if ord ξ = d then 1 else 0) := by
    intro ξ
    calc ∑ v : ZMod M, ((∑ i ∈ s, c i * (J i : ℤ) * (cnt A (J i) v : ℤ) : ℤ) : ℂ)
          * ZMod.stdAddChar (ξ * v)
        = ∑ i ∈ s, (c i : ℂ) * ((J i : ℂ)
            * ∑ v : ZMod M, (cnt A (J i) v : ℂ) * ZMod.stdAddChar (ξ * v)) := by
          push_cast
          simp_rw [Finset.sum_mul, Finset.mul_sum]
          rw [Finset.sum_comm]
          refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun v _ => by ring
      _ = ∑ i ∈ s, hat A ξ * M * (((if ord ξ ∣ J i then c i else 0 : ℤ)) : ℂ) := by
          refine Finset.sum_congr rfl fun i hi => ?_
          rw [sum_cnt_mul_char A (J i) (hS i hi) ξ]
          have hJ : (J i : ℂ) * ((M / J i : ℕ) : ℂ) = M := by
            rw [← Nat.cast_mul, Nat.mul_div_cancel' (hS i hi)]
          split_ifs
          · linear_combination (c i : ℂ) * hat A ξ * hJ
          · simp
      _ = hat A ξ * M * (if ord ξ = d then 1 else 0) := by
          rw [← Finset.mul_sum, ← Int.cast_sum, hc _ (ord_dvd ξ)]
          split_ifs <;> simp
  constructor
  · intro hz v
    have h0 := fourier_uniq_zmod
      (fun v => ((∑ i ∈ s, c i * (J i : ℤ) * (cnt A (J i) v : ℤ) : ℤ) : ℂ)) (fun ξ => by
        rw [key]
        split_ifs with h
        · rw [hz ξ h]; simp
        · simp)
    have h1 : ((∑ i ∈ s, c i * (J i : ℤ) * (cnt A (J i) v : ℤ) : ℤ) : ℂ) = 0 := congrFun h0 v
    exact_mod_cast h1
  · intro hg ξ hξ
    have h1 := key ξ
    simp only [hg, Int.cast_zero, zero_mul, Finset.sum_const_zero, hξ, ite_true, mul_one] at h1
    exact (mul_eq_zero.1 h1.symm).resolve_right hM

end Bridge

/-- **Bridge.** Let `c j`, `j ∈ S`, be integers attached to divisors `j` of `M` such that
`∑_{j ∈ S, e ∣ j} c j = [e = d]` for every divisor `e` of `M`.  Then `A` has no Fourier mass at order `d`
iff `∑_{j ∈ S} c j · j · #{a ∈ A : a ≡ v mod j} = 0` for every `v`. -/
theorem zeroAt_iff_cnt (A : Finset (ZMod M)) (d : ℕ) (S : Finset ℕ) (c : ℕ → ℤ)
    (hS : ∀ j ∈ S, j ∣ M)
    (hc : ∀ e, e ∣ M → (∑ j ∈ S, if e ∣ j then c j else 0) = if e = d then 1 else 0) :
    ZeroAt A d ↔ ∀ v : ZMod M, ∑ j ∈ S, c j * (j : ℤ) * (cnt A j v : ℤ) = 0 :=
  Bridge.zeroAt_iff_cnt_aux A d S (fun j => j) c hS hc

set_option linter.unusedSectionVars false in
/-- every element of `A` is congruent to `v` modulo 1 -/
theorem cnt_one (A : Finset (ZMod M)) (v : ZMod M) : cnt A 1 v = A.card := by
  simp [cnt]

/-! ### (4), (5) Divisors of `p ^ (ℓ + 1)` and of `p ^ (ℓ + 1) * q` -/

namespace Bridge

theorem dvd_prime_pow_succ_iff {p : ℕ} (hp : p.Prime) (ℓ e : ℕ) :
    e ∣ p ^ (ℓ + 1) ↔ e ∣ p ^ ℓ ∨ e = p ^ (ℓ + 1) := by
  rw [Nat.dvd_prime_pow hp, Nat.dvd_prime_pow hp]
  constructor
  · rintro ⟨k, hk, rfl⟩
    rcases Nat.lt_or_eq_of_le hk with h | rfl
    · exact Or.inl ⟨k, Nat.lt_succ_iff.1 h, rfl⟩
    · exact Or.inr rfl
  · rintro (⟨k, hk, rfl⟩ | rfl)
    · exact ⟨k, Nat.le_succ_of_le hk, rfl⟩
    · exact ⟨ℓ + 1, le_rfl, rfl⟩

theorem not_prime_pow_succ_dvd {p : ℕ} (hp : p.Prime) (ℓ : ℕ) : ¬ p ^ (ℓ + 1) ∣ p ^ ℓ := by
  rw [Nat.pow_dvd_pow_iff_le_right hp.one_lt]
  omega

/-- `[e ∣ p^(ℓ+1)] - [e ∣ p^ℓ] = [e = p^(ℓ+1)]` -/
theorem indicator_prime_pow {p : ℕ} (hp : p.Prime) (ℓ e : ℕ) :
    (if e ∣ p ^ (ℓ + 1) then (1 : ℤ) else 0) + (if e ∣ p ^ ℓ then -1 else 0)
      = if e = p ^ (ℓ + 1) then 1 else 0 := by
  have h1 := dvd_prime_pow_succ_iff hp ℓ e
  have h2 : e = p ^ (ℓ + 1) → ¬ e ∣ p ^ ℓ := fun he => he ▸ not_prime_pow_succ_dvd hp ℓ
  split_ifs <;> first | (norm_num; done) | (exfalso; tauto)

/-- `[e ∣ p^(ℓ+1) q] - [e ∣ p^ℓ q] - [e ∣ p^(ℓ+1)] + [e ∣ p^ℓ] = [e = p^(ℓ+1) q]` -/
theorem indicator_prime_pow_mul {p q : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) (ℓ e : ℕ) :
    (if e ∣ p ^ (ℓ + 1) * q then (1 : ℤ) else 0) + (if e ∣ p ^ ℓ * q then -1 else 0)
        + (if e ∣ p ^ (ℓ + 1) then -1 else 0) + (if e ∣ p ^ ℓ then 1 else 0)
      = if e = p ^ (ℓ + 1) * q then 1 else 0 := by
  have hcop : Nat.Coprime p q := (Nat.coprime_primes hp hq).2 hpq
  have h43 : e ∣ p ^ ℓ → e ∣ p ^ (ℓ + 1) := fun h => h.trans (pow_dvd_pow p (Nat.le_succ ℓ))
  have h42 : e ∣ p ^ ℓ → e ∣ p ^ ℓ * q := fun h => h.mul_right q
  have h31 : e ∣ p ^ (ℓ + 1) → e ∣ p ^ (ℓ + 1) * q := fun h => h.mul_right q
  have h21 : e ∣ p ^ ℓ * q → e ∣ p ^ (ℓ + 1) * q := fun h =>
    h.trans (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ ℓ)) q)
  have h234 : e ∣ p ^ ℓ * q → e ∣ p ^ (ℓ + 1) → e ∣ p ^ ℓ := by
    intro h2 h3
    obtain ⟨k, -, rfl⟩ := (Nat.dvd_prime_pow hp).1 h3
    exact (Nat.Coprime.pow_left k hcop).dvd_of_dvd_mul_right h2
  have hE1 : e = p ^ (ℓ + 1) * q → e ∣ p ^ (ℓ + 1) * q := fun h => h ▸ dvd_rfl
  have hE2 : e = p ^ (ℓ + 1) * q → ¬ e ∣ p ^ ℓ * q := by
    rintro rfl h
    exact not_prime_pow_succ_dvd hp ℓ (Nat.dvd_of_mul_dvd_mul_right hq.pos h)
  have hE3 : e = p ^ (ℓ + 1) * q → ¬ e ∣ p ^ (ℓ + 1) := by
    rintro rfl h
    have hqp : q ∣ p := hq.dvd_of_dvd_pow ((dvd_mul_left q _).trans h)
    exact hpq ((Nat.prime_dvd_prime_iff_eq hq hp).1 hqp).symm
  have hmain : e ∣ p ^ (ℓ + 1) * q → ¬ e ∣ p ^ ℓ * q → ¬ e ∣ p ^ (ℓ + 1) → e = p ^ (ℓ + 1) * q := by
    intro h1 h2 h3
    obtain ⟨e₁, e₂, he₁, he₂, rfl⟩ := Nat.dvd_mul.1 h1
    rcases (Nat.dvd_prime hq).1 he₂ with rfl | rfl
    · rw [mul_one] at h3
      exact absurd he₁ h3
    · rcases (dvd_prime_pow_succ_iff hp ℓ e₁).1 he₁ with h | rfl
      · exact absurd (Nat.mul_dvd_mul_right h e₂) h2
      · rfl
  by_cases hE : e = p ^ (ℓ + 1) * q
  · rw [ite_eq_left (hE1 hE), ite_eq_right (hE2 hE), ite_eq_right (hE3 hE), ite_eq_right (fun h => hE3 hE (h43 h)),
      ite_eq_left hE]
    norm_num
  · by_cases P2 : e ∣ p ^ ℓ * q <;> by_cases P3 : e ∣ p ^ (ℓ + 1)
    · rw [ite_eq_left (h21 P2), ite_eq_left P2, ite_eq_left P3, ite_eq_left (h234 P2 P3), ite_eq_right hE]
      norm_num
    · rw [ite_eq_left (h21 P2), ite_eq_left P2, ite_eq_right P3, ite_eq_right (fun h => P3 (h43 h)), ite_eq_right hE]
      norm_num
    · rw [ite_eq_left (h31 P3), ite_eq_right P2, ite_eq_left P3, ite_eq_right (fun h => P2 (h42 h)), ite_eq_right hE]
      norm_num
    · rw [ite_eq_right (fun h => hE (hmain h P2 P3)), ite_eq_right P2, ite_eq_right P3,
        ite_eq_right (fun h => P3 (h43 h)), ite_eq_right hE]
      norm_num

end Bridge

/-- order a prime power: the count of a class mod `p^(ℓ+1)` is `1/p` of the count of its class mod `p^ℓ` -/
theorem zeroAt_prime_pow (A : Finset (ZMod M)) (p : ℕ) (hp : p.Prime) (ℓ : ℕ)
    (h : p ^ (ℓ + 1) ∣ M) :
    ZeroAt A (p ^ (ℓ + 1)) ↔ ∀ v : ZMod M, p * cnt A (p ^ (ℓ + 1)) v = cnt A (p ^ ℓ) v := by
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
  rw [Bridge.zeroAt_iff_cnt_aux A (p ^ (ℓ + 1)) (Finset.univ : Finset (Fin 2)) ![p ^ (ℓ + 1), p ^ ℓ]
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
    exact Bridge.indicator_prime_pow hp ℓ e

/-- order a prime power times another prime: the `p × q` arrays of counts are additive -/
theorem zeroAt_prime_pow_mul (A : Finset (ZMod M)) (p q : ℕ) (hp : p.Prime) (hq : q.Prime)
    (hpq : p ≠ q) (ℓ : ℕ) (h : p ^ (ℓ + 1) * q ∣ M) :
    ZeroAt A (p ^ (ℓ + 1) * q) ↔ ∀ v : ZMod M,
      p * q * cnt A (p ^ (ℓ + 1) * q) v + cnt A (p ^ ℓ) v
        = q * cnt A (p ^ ℓ * q) v + p * cnt A (p ^ (ℓ + 1)) v := by
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
  rw [Bridge.zeroAt_iff_cnt_aux A (p ^ (ℓ + 1) * q) (Finset.univ : Finset (Fin 4))
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
    exact Bridge.indicator_prime_pow_mul hp hq hpq ℓ e

end Pqr
