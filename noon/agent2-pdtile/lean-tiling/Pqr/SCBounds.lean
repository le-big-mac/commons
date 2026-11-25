/-
The bounds (S) and (C) for weak tiles of an arbitrary cyclic group `ZMod M` (see `ZeroDefs.lean`).
-/
import Pqr.ZeroDefs

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

/-! ### Preliminaries on the standard character and on `ord` -/

/-- the Fourier transform of a real function on `ZMod M` -/
noncomputable def ft (f : ZMod M → ℝ) (ξ : ZMod M) : ℂ :=
  ∑ w, (f w : ℂ) * ZMod.stdAddChar (ξ * w)

/-- Orthogonality: the sum of `ψ (ξ * v)` over `v` is `M` if `ξ = 0` and `0` otherwise. -/
theorem sum_stdAddChar_mul (ξ : ZMod M) :
    ∑ v : ZMod M, (ZMod.stdAddChar (ξ * v) : ℂ) = if ξ = 0 then (M : ℂ) else 0 := by
  classical
  have h := AddChar.sum_mulShift (R' := ℂ) ξ (ZMod.isPrimitive_stdAddChar M)
  simp only [mul_comm _ ξ, ZMod.card] at h
  rw [h]
  split_ifs <;> simp

/-- The Fourier transform of a convolution with an indicator function. -/
theorem conv_ft (A : Finset (ZMod M)) (f : ZMod M → ℝ) (ξ : ZMod M) :
    ∑ v, (∑ a ∈ A, (f (v - a) : ℂ)) * ZMod.stdAddChar (ξ * v) = hat A ξ * ft f ξ := by
  have h := sum_conv_mul_char A (fun w => (f w : ℂ)) ((ZMod.stdAddChar (N := M)).mulShift ξ)
  simpa only [AddChar.mulShift_apply, hat, ft] using h

/-- **(0)** The tiling identity on the Fourier side. -/
theorem hat_mul_ft (A : Finset (ZMod M)) (f : ZMod M → ℝ) (h : WeakTiling A f) (ξ : ZMod M) :
    hat A ξ * ft f ξ = if ξ = 0 then (M : ℂ) else 0 := by
  rw [← conv_ft, ← sum_stdAddChar_mul]
  refine Finset.sum_congr rfl fun v _ => ?_
  rw [← Complex.ofReal_sum, h.2.2 v]
  simp

theorem hat_zero (A : Finset (ZMod M)) : hat A 0 = (A.card : ℂ) := by
  simp [hat]

theorem ft_zero (f : ZMod M → ℝ) : ft f 0 = ((∑ w, f w : ℝ) : ℂ) := by
  simp [ft]

omit [NeZero M] in
/-- A weak tile is nonempty. -/
theorem nonempty_of_weakTiling (A : Finset (ZMod M)) (f : ZMod M → ℝ) (h : WeakTiling A f) :
    A.Nonempty := by
  rcases A.eq_empty_or_nonempty with hA | hA
  · have h1 := h.2.2 0
    rw [hA] at h1
    simp at h1
  · exact hA

/-- `|A| * ∑ f = M` for a weak tiling. -/
theorem card_mul_sum (A : Finset (ZMod M)) (f : ZMod M → ℝ) (h : WeakTiling A f) :
    (A.card : ℝ) * ∑ w, f w = M := by
  have h0 := hat_mul_ft A f h 0
  rw [hat_zero, ft_zero, ite_eq_left rfl] at h0
  exact_mod_cast h0

omit [NeZero M] in
theorem ord_dvd (ξ : ZMod M) : ord ξ ∣ M :=
  Nat.div_dvd_of_dvd (Nat.gcd_dvd_right _ _)

theorem ord_eq_one_iff (ξ : ZMod M) : ord ξ = 1 ↔ ξ = 0 := by
  have hM : M ≠ 0 := NeZero.ne M
  constructor
  · intro h
    have hg : ξ.val.gcd M ∣ M := Nat.gcd_dvd_right _ _
    have h1 : M = ξ.val.gcd M := by
      have := Nat.div_mul_cancel hg
      rw [show M / ξ.val.gcd M = 1 from h, one_mul] at this
      exact this.symm
    have h2 : M ∣ ξ.val := by
      have := Nat.gcd_dvd_left ξ.val M
      rwa [← h1] at this
    have h3 : ξ.val = 0 := Nat.eq_zero_of_dvd_of_lt h2 (ZMod.val_lt ξ)
    exact (ZMod.val_eq_zero ξ).1 h3
  · rintro rfl
    simp [ord, Nat.div_self (Nat.pos_of_ne_zero hM)]

/-- Elements of equal order have equal gcd with `M`. -/
theorem gcd_eq_of_ord_eq (ξ ξ' : ZMod M) (h : ord ξ' = ord ξ) : ξ'.val.gcd M = ξ.val.gcd M := by
  have hM : 0 < M := Nat.pos_of_ne_zero (NeZero.ne M)
  have hg : ξ.val.gcd M ∣ M := Nat.gcd_dvd_right _ _
  have hg' : ξ'.val.gcd M ∣ M := Nat.gcd_dvd_right _ _
  have h1 : M / ξ.val.gcd M * ξ.val.gcd M = M := Nat.div_mul_cancel hg
  have h2 : M / ξ'.val.gcd M * ξ'.val.gcd M = M := Nat.div_mul_cancel hg'
  have h3 : M / ξ'.val.gcd M = M / ξ.val.gcd M := h
  rw [h3] at h2
  have hpos : 0 < M / ξ.val.gcd M := Nat.div_pos (Nat.le_of_dvd hM hg) (Nat.gcd_pos_of_pos_right _ hM)
  exact Nat.eq_of_mul_eq_mul_left hpos (h2.trans h1.symm)

/-- Elements of equal order differ by a unit. -/
theorem exists_unit_mul_of_ord_eq (ξ ξ' : ZMod M) (h : ord ξ' = ord ξ) :
    ∃ w : (ZMod M)ˣ, ξ' = w * ξ := by
  obtain ⟨u, hu⟩ := eq_unit_mul_gcd ξ
  obtain ⟨u', hu'⟩ := eq_unit_mul_gcd ξ'
  rw [gcd_eq_of_ord_eq ξ ξ' h] at hu'
  refine ⟨u' * u⁻¹, ?_⟩
  conv_rhs => rw [hu]
  rw [hu', Units.val_mul, mul_assoc, ← mul_assoc (↑u⁻¹ : ZMod M), Units.inv_mul, one_mul]

/-- Galois: the Fourier zeros of a set are a union of classes of frequencies of equal order. -/
theorem zeroAt_of_hat_eq_zero (A : Finset (ZMod M)) (ξ : ZMod M) (h : hat A ξ = 0) :
    ZeroAt A (ord ξ) := by
  intro ξ' hξ'
  have hM : M ≠ 0 := NeZero.ne M
  obtain ⟨w, hw⟩ := exists_unit_mul_of_ord_eq ξ ξ' hξ'
  have hk : ((w : ZMod M).val).Coprime M := ZMod.val_coe_unit_coprime w
  have h' : ∑ a ∈ A, (((1 : ℤ) : ℂ)) * ZMod.stdAddChar (ξ * a) = 0 := by
    simpa [hat] using h
  have hgal := galois_sum A M hM (fun _ => 1) (fun a => ZMod.stdAddChar (ξ * a))
    (fun a _ => by
      rw [← AddChar.map_nsmul_eq_pow, nsmul_eq_mul, ZMod.natCast_self, zero_mul,
        AddChar.map_zero_eq_one])
    _ hk h'
  rw [hat, ← hgal]
  refine Finset.sum_congr rfl fun a _ => ?_
  rw [← AddChar.map_nsmul_eq_pow, nsmul_eq_mul, ZMod.natCast_zmod_val, hw, mul_assoc]
  simp

/-- Fourier uniqueness on `ZMod M` in terms of the standard character. -/
theorem zmod_fourier_uniq (g : ZMod M → ℂ)
    (h : ∀ ξ : ZMod M, ∑ v, g v * ZMod.stdAddChar (ξ * v) = 0) : g = 0 := by
  have h0 : ZMod.dft g = 0 := by
    funext k
    rw [ZMod.dft_apply, Pi.zero_apply, ← h (-k)]
    refine Finset.sum_congr rfl fun j _ => ?_
    rw [smul_eq_mul, mul_comm, neg_mul, mul_comm k]
  exact (LinearEquiv.map_eq_zero_iff _).1 h0

/-- **(S)** A weak tile has at most as many elements as any nonempty set with at least its Fourier zeros. -/
theorem S_bound (A A' : Finset (ZMod M)) (f : ZMod M → ℝ) (h : WeakTiling A f) (hA' : A'.Nonempty)
    (hZ : ∀ d, d ∣ M → d ≠ 1 → ZeroAt A d → ZeroAt A' d) : A.card ≤ A'.card := by
  have hA : A.Nonempty := nonempty_of_weakTiling A f h
  have hApos : (0 : ℝ) < A.card := Nat.cast_pos.2 hA.card_pos
  have hsum := card_mul_sum A f h
  set c : ℝ := (A'.card : ℝ) / A.card with hc
  -- all Fourier coefficients of `1_{A'} * f - c` vanish
  have key : ∀ ξ : ZMod M,
      ∑ v, ((∑ a ∈ A', (f (v - a) : ℂ)) - c) * ZMod.stdAddChar (ξ * v) = 0 := by
    intro ξ
    simp_rw [sub_mul]
    rw [Finset.sum_sub_distrib, conv_ft, ← Finset.mul_sum, sum_stdAddChar_mul]
    by_cases hξ : ξ = 0
    · subst hξ
      rw [ite_eq_left rfl, hat_zero, ft_zero, sub_eq_zero]
      have : (A'.card : ℝ) * ∑ w, f w = c * M := by
        rw [hc, ← hsum]
        field_simp
      exact_mod_cast this
    · rw [ite_eq_right hξ, mul_zero, sub_zero]
      have hprod := hat_mul_ft A f h ξ
      rw [ite_eq_right hξ] at hprod
      rcases mul_eq_zero.1 hprod with hAz | hFz
      · have hZA : ZeroAt A (ord ξ) := zeroAt_of_hat_eq_zero A ξ hAz
        have hZA' : ZeroAt A' (ord ξ) :=
          hZ _ (ord_dvd ξ) (fun h1 => hξ ((ord_eq_one_iff ξ).1 h1)) hZA
        rw [hZA' ξ rfl, zero_mul]
      · rw [hFz, mul_zero]
  have hg := zmod_fourier_uniq (fun v => (∑ a ∈ A', (f (v - a) : ℂ)) - c) key
  obtain ⟨v, hv⟩ := hA'
  have hv0 := congrFun hg v
  simp only [Pi.zero_apply, sub_eq_zero] at hv0
  have hv1 : ∑ a ∈ A', f (v - a) = c := by exact_mod_cast hv0
  have hge : f (v - v) ≤ ∑ a ∈ A', f (v - a) :=
    Finset.single_le_sum (f := fun a => f (v - a)) (fun a _ => h.1 _) hv
  rw [sub_self, h.2.1, hv1, hc, le_div_iff₀ hApos, one_mul] at hge
  exact_mod_cast hge

/-- `|B̂(w)|²` as a double sum over `B`. -/
theorem normSq_hat (B : Finset (ZMod M)) (w : ZMod M) :
    (Complex.normSq (hat B w) : ℂ) = ∑ b ∈ B, ∑ b' ∈ B, ZMod.stdAddChar ((b - b') * w) := by
  rw [← Complex.mul_conj, hat, map_sum, Finset.sum_mul_sum]
  refine Finset.sum_congr rfl fun b _ => Finset.sum_congr rfl fun b' _ => ?_
  rw [← AddChar.map_neg_eq_conj, ← AddChar.map_add_eq_mul]
  congr 1
  ring

/-- The double sum of the Fourier transform over differences is a nonnegative quadratic form. -/
theorem sum_sum_ft_sub (B : Finset (ZMod M)) (f : ZMod M → ℝ) :
    ∑ b ∈ B, ∑ b' ∈ B, ft f (b - b')
      = ((∑ w, f w * Complex.normSq (hat B w) : ℝ) : ℂ) := by
  rw [Complex.ofReal_sum]
  simp_rw [Complex.ofReal_mul, normSq_hat, ft, Finset.mul_sum]
  symm
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun b _ => ?_
  rw [Finset.sum_comm]

/-- **(C)** If no two distinct elements of `B` differ by an element whose order is a Fourier zero of the
weak tile `A`, then `|A| · |B| ≤ M`. -/
theorem C_bound (A B : Finset (ZMod M)) (f : ZMod M → ℝ) (h : WeakTiling A f)
    (hB : ∀ b ∈ B, ∀ b' ∈ B, b ≠ b' → ¬ ZeroAt A (ord (b - b'))) : A.card * B.card ≤ M := by
  classical
  rcases B.eq_empty_or_nonempty with hBe | hBne
  · simp [hBe]
  have hA : A.Nonempty := nonempty_of_weakTiling A f h
  have hApos : (0 : ℝ) < A.card := Nat.cast_pos.2 hA.card_pos
  have hBpos : (0 : ℝ) < B.card := Nat.cast_pos.2 hBne.card_pos
  have hsum := card_mul_sum A f h
  -- the Fourier transform of `f` vanishes at the differences of distinct elements of `B`
  have hoff : ∀ b ∈ B, ∀ b' ∈ B, b ≠ b' → ft f (b - b') = 0 := by
    intro b hb b' hb' hne
    have hξ : b - b' ≠ 0 := sub_ne_zero.2 hne
    have hprod := hat_mul_ft A f h (b - b')
    rw [ite_eq_right hξ] at hprod
    rcases mul_eq_zero.1 hprod with hAz | hFz
    · exact absurd (zeroAt_of_hat_eq_zero A _ hAz) (hB b hb b' hb' hne)
    · exact hFz
  -- so only the diagonal of the double sum survives
  have hdiag : ∑ b ∈ B, ∑ b' ∈ B, ft f (b - b') = ((B.card * ∑ w, f w : ℝ) : ℂ) := by
    have hrow : ∀ b ∈ B, ∑ b' ∈ B, ft f (b - b') = ft f 0 := by
      intro b hb
      rw [Finset.sum_eq_single_of_mem b hb (fun b' hb' hne => hoff b hb b' hb' (Ne.symm hne)),
        sub_self]
    rw [Finset.sum_congr rfl hrow, Finset.sum_const, ft_zero, nsmul_eq_mul]
    push_cast
    rfl
  rw [sum_sum_ft_sub] at hdiag
  have hreal : ∑ w, f w * Complex.normSq (hat B w) = B.card * ∑ w, f w :=
    Complex.ofReal_injective hdiag
  -- the quadratic form is at least its term at `0`
  have hge : f 0 * Complex.normSq (hat B 0) ≤ ∑ w, f w * Complex.normSq (hat B w) :=
    Finset.single_le_sum (f := fun w => f w * Complex.normSq (hat B w))
      (fun w _ => mul_nonneg (h.1 w) (Complex.normSq_nonneg _)) (Finset.mem_univ 0)
  rw [h.2.1, one_mul, hat_zero, Complex.normSq_natCast, hreal] at hge
  have hS : (B.card : ℝ) ≤ ∑ w, f w := le_of_mul_le_mul_left hge hBpos
  have hfin : (A.card : ℝ) * B.card ≤ M := by
    rw [← hsum]
    exact mul_le_mul_of_nonneg_left hS hApos.le
  exact_mod_cast hfin

end Pqr
