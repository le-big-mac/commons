/-
Part A: a weak tiling complement can be replaced by a step function (Galois + averaging).
-/
import Pqr.Defs

open Finset

namespace Pqr

/-- `f` is a weak tiling complement of `A` in `G`: `f ≥ 0`, `f 0 = 1`, `1_A * f = 1`. -/
def WeakTiling {G : Type*} [AddCommGroup G] (A : Finset G) (f : G → ℝ) : Prop :=
  (∀ v, 0 ≤ f v) ∧ f 0 = 1 ∧ ∀ v, ∑ a ∈ A, f (v - a) = 1

/-! ### (A1) Galois conjugation -/

open Polynomial in
/-- (A1) Galois conjugation for integer combinations of `M`-th roots of unity: if
`∑ c i * z i = 0` with all `z i` being `M`-th roots of unity and `k` is coprime to `M`, then
`∑ c i * z i ^ k = 0`. -/
theorem galois_sum {ι : Type*} (s : Finset ι) (M : ℕ) (hM : M ≠ 0) (c : ι → ℤ) (z : ι → ℂ)
    (hz : ∀ i ∈ s, z i ^ M = 1) (k : ℕ) (hk : k.Coprime M)
    (h : ∑ i ∈ s, (c i : ℂ) * z i = 0) : ∑ i ∈ s, (c i : ℂ) * z i ^ k = 0 := by
  classical
  have : NeZero M := ⟨hM⟩
  set ω : ℂ := Complex.exp (2 * Real.pi * Complex.I / M) with hω
  have hprim : IsPrimitiveRoot ω M := Complex.isPrimitiveRoot_exp M hM
  have hprimk : IsPrimitiveRoot (ω ^ k) M := hprim.pow_of_coprime k hk
  -- every `z i` is a power of `ω`
  have he : ∀ i, ∃ e : ℕ, i ∈ s → ω ^ e = z i := by
    intro i
    by_cases hi : i ∈ s
    · obtain ⟨e, -, he⟩ := hprim.eq_pow_of_pow_eq_one (hz i hi)
      exact ⟨e, fun _ => he⟩
    · exact ⟨0, fun h => absurd h hi⟩
  choose e he using he
  set P : ℚ[X] := ∑ i ∈ s, C (c i : ℚ) * X ^ e i with hP
  have hev : ∀ x : ℂ, aeval x P = ∑ i ∈ s, (c i : ℂ) * x ^ e i := by
    intro x
    simp [hP, map_sum]
  have h0 : aeval ω P = 0 := by
    rw [hev, ← h]
    exact Finset.sum_congr rfl fun i hi => by rw [he i hi]
  have hdvd : minpoly ℚ ω ∣ P := minpoly.dvd ℚ ω h0
  -- `ω` and `ω ^ k` have the same minimal polynomial, the cyclotomic polynomial
  have hmin : minpoly ℚ (ω ^ k) = minpoly ℚ ω := by
    rw [← cyclotomic_eq_minpoly_rat hprim (Nat.pos_of_ne_zero hM),
      ← cyclotomic_eq_minpoly_rat hprimk (Nat.pos_of_ne_zero hM)]
  have h1 : aeval (ω ^ k) P = 0 := by
    obtain ⟨Q, hQ⟩ := hdvd
    rw [hQ, ← hmin, map_mul, minpoly.aeval, zero_mul]
  rw [hev] at h1
  rw [← h1]
  exact Finset.sum_congr rfl fun i hi => by rw [← he i hi, ← pow_mul, ← pow_mul, mul_comm k]

/-! ### (A2) Fourier uniqueness -/

/-- (A2) A function on a finite abelian group all of whose Fourier coefficients vanish is zero. -/
theorem fourier_uniq {G : Type*} [AddCommGroup G] [Fintype G] (g : G → ℂ)
    (h : ∀ ψ : AddChar G ℂ, ∑ v, g v * ψ v = 0) : g = 0 := by
  classical
  funext w
  have hterm : ∀ v, ∑ ψ : AddChar G ℂ, ψ (-w) * (g v * ψ v)
      = g v * (if v - w = 0 then (Fintype.card G : ℂ) else 0) := by
    intro v
    rw [← AddChar.sum_apply_eq_ite, Finset.mul_sum]
    refine Finset.sum_congr rfl fun ψ _ => ?_
    rw [sub_eq_add_neg, AddChar.map_add_eq_mul]
    ring
  have key : ∑ ψ : AddChar G ℂ, ψ (-w) * ∑ v, g v * ψ v = g w * Fintype.card G := by
    simp_rw [Finset.mul_sum]
    rw [Finset.sum_comm]
    simp_rw [hterm, sub_eq_zero]
    simp
  have h0 : g w * Fintype.card G = 0 := by
    rw [← key]
    simp [h]
  have hc : (Fintype.card G : ℂ) ≠ 0 := Nat.cast_ne_zero.2 Fintype.card_ne_zero
  simpa [hc] using h0

/-- The Fourier transform of a convolution with an indicator function. -/
theorem sum_conv_mul_char {G : Type*} [AddCommGroup G] [Fintype G] (A : Finset G) (h : G → ℂ)
    (ψ : AddChar G ℂ) :
    ∑ v, (∑ a ∈ A, h (v - a)) * ψ v = (∑ a ∈ A, ψ a) * ∑ w, h w * ψ w := by
  simp_rw [Finset.sum_mul]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun a _ => ?_
  calc ∑ v, h (v - a) * ψ v = ∑ w, h (w + a - a) * ψ (w + a) :=
        (Equiv.sum_comp (Equiv.addRight a) (fun v => h (v - a) * ψ v)).symm
    _ = ψ a * ∑ w, h w * ψ w := by
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl fun w _ => ?_
        rw [add_sub_cancel_right, AddChar.map_add_eq_mul]
        ring

/-! ### (A3) Dilation invariance -/

/-- (A3) If `f` is a weak tiling complement of `A` in a finite abelian group `G` and `k` is
coprime to the order of `G`, then `v ↦ f (k • v)` is a weak tiling complement of `A` too. -/
theorem weakTiling_nsmul {G : Type*} [AddCommGroup G] [Fintype G]
    (A : Finset G) (f : G → ℝ) (h : WeakTiling A f) (k : ℕ) (hk : (Fintype.card G).Coprime k) :
    WeakTiling A (fun v => f (k • v)) := by
  classical
  obtain ⟨hnn, h0, htile⟩ := h
  refine ⟨fun v => hnn _, by simpa using h0, ?_⟩
  -- the dilation as an additive equivalence
  have hbij : Function.Bijective (nsmulAddMonoidHom k : G →+ G) :=
    Nat.Coprime.nsmul_right_bijective (G := G) (n := k) (by rwa [Nat.card_eq_fintype_card])
  let σ : G ≃+ G := AddEquiv.ofBijective (nsmulAddMonoidHom k : G →+ G) hbij
  have hσ : ∀ v, σ v = k • v := fun v => rfl
  -- Fourier form of the tiling identity
  have hF : ∀ χ : AddChar G ℂ, (∑ a ∈ A, χ a) * ∑ w, (f w : ℂ) * χ w = ∑ v, χ v := by
    intro χ
    rw [← sum_conv_mul_char A (fun w => (f w : ℂ)) χ]
    refine Finset.sum_congr rfl fun v _ => ?_
    rw [← Complex.ofReal_sum, htile v]
    simp
  have key : ∀ ψ : AddChar G ℂ, ∑ v, ((∑ a ∈ A, (f (k • (v - a)) : ℂ)) - 1) * ψ v = 0 := by
    intro ψ
    simp_rw [sub_mul, one_mul]
    rw [Finset.sum_sub_distrib, sum_conv_mul_char A (fun w => (f (k • w) : ℂ)) ψ]
    set χ : AddChar G ℂ := ψ.compAddMonoidHom (σ.symm : G →+ G) with hχ
    have hχk : ∀ v, χ (k • v) = ψ v := by
      intro v
      rw [hχ, AddChar.compAddMonoidHom_apply, ← hσ]
      simp
    have hFχ : ∑ w, (f (k • w) : ℂ) * ψ w = ∑ w, (f w : ℂ) * χ w := by
      rw [← Equiv.sum_comp σ.toEquiv (fun w => (f w : ℂ) * χ w)]
      refine Finset.sum_congr rfl fun w _ => ?_
      simp [hσ, hχk]
    have hsumχ : ∑ v, χ v = ∑ v, ψ v := by
      rw [← Equiv.sum_comp σ.toEquiv (fun v => χ v)]
      refine Finset.sum_congr rfl fun w _ => ?_
      simp [hσ, hχk]
    rw [hFχ, sub_eq_zero]
    by_cases hψ : ψ = 0
    · -- the trivial character
      have hSχ : ∑ a ∈ A, ψ a = ∑ a ∈ A, χ a := by
        refine Finset.sum_congr rfl fun a _ => ?_
        rw [hχ, AddChar.compAddMonoidHom_apply, hψ]
        simp
      rw [hSχ, hF χ, hsumχ]
    · -- a nontrivial character
      have hz : ∑ v, ψ v = 0 := AddChar.sum_eq_zero_iff_ne_zero.2 hψ
      rw [hz]
      have hprod := hF χ
      rw [hsumχ, hz] at hprod
      rcases mul_eq_zero.1 hprod with hS | hFz
      · have hS' : ∑ a ∈ A, (((1 : ℤ) : ℂ)) * χ a = 0 := by simpa using hS
        have hgal := galois_sum A (Fintype.card G) Fintype.card_ne_zero (fun _ => 1)
          (fun a => χ a)
          (fun a _ => by
            rw [← AddChar.map_nsmul_eq_pow, card_nsmul_eq_zero, AddChar.map_zero_eq_one])
          k hk.symm hS'
        have hSψ : ∑ a ∈ A, ψ a = 0 := by
          rw [← hgal]
          refine Finset.sum_congr rfl fun a _ => ?_
          rw [← AddChar.map_nsmul_eq_pow, hχk]
          simp
        rw [hSψ, zero_mul]
      · rw [hFz, mul_zero]
  have hg := fourier_uniq (fun v => (∑ a ∈ A, (f (k • (v - a)) : ℂ)) - 1) key
  intro v
  have hv := congrFun hg v
  simp only [Pi.zero_apply, sub_eq_zero] at hv
  exact_mod_cast hv

/-! ### (A5) Averaging -/

/-- An average of weak tiling complements is a weak tiling complement. -/
theorem weakTiling_avg {G : Type*} [AddCommGroup G] {ι : Type*} [Fintype ι] [Nonempty ι]
    (A : Finset G) (F : ι → G → ℝ) (h : ∀ i, WeakTiling A (F i)) :
    WeakTiling A (fun v => (∑ i, F i v) / Fintype.card ι) := by
  have hc : (Fintype.card ι : ℝ) ≠ 0 := Nat.cast_ne_zero.2 Fintype.card_ne_zero
  refine ⟨fun v => div_nonneg (Finset.sum_nonneg fun i _ => (h i).1 v) (Nat.cast_nonneg _),
    ?_, fun v => ?_⟩
  · simp only [(h _).2.1]
    simp [hc]
  · rw [← Finset.sum_div, Finset.sum_comm]
    simp only [(h _).2.2 v]
    simp [hc]

variable (p q r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime]

/-- the indicator array of a subset of `ZMod p × ZMod q × ZMod r` -/
def ind (A : Finset (ZMod p × ZMod q × ZMod r)) : ZMod p → ZMod q → ZMod r → ℤ :=
  fun i j k => if (i, j, k) ∈ A then 1 else 0

/-! ### (A4) Coordinatewise dilations -/

/-- (A4) Chinese remainder theorem: every triple of units is the reduction of a natural number
coprime to `p * q * r`. -/
theorem exists_nat_cast_eq (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (α : (ZMod p)ˣ) (β : (ZMod q)ˣ) (δ : (ZMod r)ˣ) :
    ∃ k : ℕ, (Fintype.card (ZMod p × ZMod q × ZMod r)).Coprime k ∧
      (k : ZMod p) = α ∧ (k : ZMod q) = β ∧ (k : ZMod r) = δ := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hr : r.Prime := Fact.out
  have cpq : p.Coprime q := (Nat.coprime_primes hp hq).2 hpq
  have cpr : p.Coprime r := (Nat.coprime_primes hp hr).2 hpr
  have cqr : q.Coprime r := (Nat.coprime_primes hq hr).2 hqr
  obtain ⟨k₁, hk₁p, hk₁q⟩ := Nat.chineseRemainder cpq (α : ZMod p).val (β : ZMod q).val
  obtain ⟨k, hk1, hkr⟩ :=
    Nat.chineseRemainder (Nat.Coprime.mul_left cpr cqr) k₁ (δ : ZMod r).val
  have hkp : (k : ZMod p) = α := by
    have hmod : k ≡ (α : ZMod p).val [MOD p] := (hk1.of_mul_right q).trans hk₁p
    rw [(ZMod.natCast_eq_natCast_iff _ _ _).2 hmod, ZMod.natCast_zmod_val]
  have hkq : (k : ZMod q) = β := by
    have hmod : k ≡ (β : ZMod q).val [MOD q] := (hk1.of_mul_left p).trans hk₁q
    rw [(ZMod.natCast_eq_natCast_iff _ _ _).2 hmod, ZMod.natCast_zmod_val]
  have hkr' : (k : ZMod r) = δ := by
    rw [(ZMod.natCast_eq_natCast_iff _ _ _).2 hkr, ZMod.natCast_zmod_val]
  refine ⟨k, ?_, hkp, hkq, hkr'⟩
  have c1 : p.Coprime k := ((ZMod.isUnit_iff_coprime k p).1 (hkp ▸ α.isUnit)).symm
  have c2 : q.Coprime k := ((ZMod.isUnit_iff_coprime k q).1 (hkq ▸ β.isUnit)).symm
  have c3 : r.Coprime k := ((ZMod.isUnit_iff_coprime k r).1 (hkr' ▸ δ.isUnit)).symm
  simp only [Fintype.card_prod, ZMod.card]
  exact Nat.Coprime.mul_left c1 (Nat.Coprime.mul_left c2 c3)

/-- Every element of `ZMod n` (`n` prime) is a unit multiple of `0` or `1`. -/
theorem exists_unit_mul (n : ℕ) [Fact n.Prime] (x : ZMod n) :
    ∃ α : (ZMod n)ˣ, (α : ZMod n) * (bif decide (x = 0) then 0 else 1) = x := by
  by_cases hx : x = 0
  · exact ⟨1, by simp [hx]⟩
  · exact ⟨Units.mk0 x hx, by simp [hx]⟩

/-! ### (A6) The main theorem -/

theorem exists_stepTiling (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (A : Finset (ZMod p × ZMod q × ZMod r)) (f : ZMod p × ZMod q × ZMod r → ℝ)
    (h : WeakTiling A f) : ∃ γ : Bool → Bool → Bool → ℝ, StepTiling (ind p q r A) γ := by
  classical
  -- the dilated complements, indexed by triples of units
  let F : (ZMod p)ˣ × (ZMod q)ˣ × (ZMod r)ˣ → ZMod p × ZMod q × ZMod r → ℝ :=
    fun u v => f ((u.1 : ZMod p) * v.1, (u.2.1 : ZMod q) * v.2.1, (u.2.2 : ZMod r) * v.2.2)
  have hF : ∀ u, WeakTiling A (F u) := by
    rintro ⟨α, β, δ⟩
    obtain ⟨k, hk, hkp, hkq, hkr⟩ := exists_nat_cast_eq p q r hpq hpr hqr α β δ
    have hdil := weakTiling_nsmul A f h k hk
    have hfun : (fun v => f (k • v)) = F (α, β, δ) := by
      funext ⟨x, y, z⟩
      simp only [F, Prod.smul_mk, nsmul_eq_mul, hkp, hkq, hkr]
    rw [← hfun]
    exact hdil
  -- their average
  let fbar : ZMod p × ZMod q × ZMod r → ℝ :=
    fun v => (∑ u, F u v) / Fintype.card ((ZMod p)ˣ × (ZMod q)ˣ × (ZMod r)ˣ)
  have hbar : WeakTiling A fbar := weakTiling_avg A F hF
  -- the average is invariant under coordinatewise dilations
  have hinv : ∀ (α : (ZMod p)ˣ) (β : (ZMod q)ˣ) (δ : (ZMod r)ˣ) (x : ZMod p) (y : ZMod q)
      (z : ZMod r), fbar ((α : ZMod p) * x, (β : ZMod q) * y, (δ : ZMod r) * z) = fbar (x, y, z) := by
    intro α β δ x y z
    simp only [fbar]
    congr 1
    rw [← Equiv.sum_comp (Equiv.mulRight (α, β, δ)) (fun u => F u (x, y, z))]
    refine Finset.sum_congr rfl fun u _ => ?_
    simp [F, mul_assoc]
  -- hence it is a step function
  let γ : Bool → Bool → Bool → ℝ := fun b1 b2 b3 =>
    fbar (bif b1 then 0 else 1, bif b2 then 0 else 1, bif b3 then 0 else 1)
  have hstep : ∀ (x : ZMod p) (y : ZMod q) (z : ZMod r),
      fbar (x, y, z) = γ (decide (x = 0)) (decide (y = 0)) (decide (z = 0)) := by
    intro x y z
    obtain ⟨α, hα⟩ := exists_unit_mul p x
    obtain ⟨β, hβ⟩ := exists_unit_mul q y
    obtain ⟨δ, hδ⟩ := exists_unit_mul r z
    have := hinv α β δ (bif decide (x = 0) then 0 else 1) (bif decide (y = 0) then 0 else 1)
      (bif decide (z = 0) then 0 else 1)
    rw [hα, hβ, hδ] at this
    exact this
  refine ⟨γ, fun b1 b2 b3 => hbar.1 _, ?_, fun i j k => ?_⟩
  · exact hbar.2.1
  · rw [← hbar.2.2 (i, j, k), ← Fintype.sum_ite_mem A, Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun i' _ => ?_
    rw [Fintype.sum_prod_type]
    refine Finset.sum_congr rfl fun j' _ => ?_
    refine Finset.sum_congr rfl fun k' _ => ?_
    simp only [ind]
    split_ifs with hm
    · rw [Prod.mk_sub_mk, Prod.mk_sub_mk, hstep]
      simp [sub_eq_zero, eq_comm]
    · simp

end Pqr
