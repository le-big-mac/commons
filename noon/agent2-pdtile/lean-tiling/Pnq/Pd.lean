/-
pd-tiling (Kiss–Londner–Matolcsi–Somlai, arXiv:2411.03854, Definition 1.3) and the three-way equivalence
tile ⇔ pd-tile ⇔ weak tile in `ZMod (p^n * q)` and in `ZMod (p * q * r)`.
-/
import Pnq.Main

open Finset

namespace Pqr

/-- `f` is a pd-tiling complement of `A ⊆ ZMod M`: a weak tiling complement (`f ≥ 0`, `f 0 = 1`, `1_A * f = 1`)
whose Fourier transform is real and nonnegative. -/
def PdTiling {M : ℕ} [NeZero M] (A : Finset (ZMod M)) (f : ZMod M → ℝ) : Prop :=
  WeakTiling A f ∧ ∀ ξ : ZMod M, ∃ r : ℝ, 0 ≤ r ∧ ft f ξ = (r : ℂ)

/-! ### The normalised autocorrelation of a tiling complement -/

/-- the normalised autocorrelation `(1/|B|) · 1_B * 1_{-B}` of a set `B ⊆ ZMod M`:
`x ↦ #{(b, b') ∈ B × B : b - b' = x} / |B|` -/
noncomputable def autocorr {M : ℕ} (B : Finset (ZMod M)) (x : ZMod M) : ℝ :=
  (∑ b ∈ B, ∑ b' ∈ B, if b - b' = x then (1 : ℝ) else 0) / B.card

theorem autocorr_nonneg {M : ℕ} (B : Finset (ZMod M)) (x : ZMod M) : 0 ≤ autocorr B x :=
  div_nonneg
    (Finset.sum_nonneg fun b _ => Finset.sum_nonneg fun b' _ => by split_ifs <;> norm_num)
    (Nat.cast_nonneg _)

theorem autocorr_zero {M : ℕ} (B : Finset (ZMod M)) (hB : B.Nonempty) : autocorr B 0 = 1 := by
  unfold autocorr
  have hrow : ∀ b ∈ B, ∑ b' ∈ B, (if b - b' = 0 then (1 : ℝ) else 0) = 1 := by
    intro b hb
    rw [Finset.sum_eq_single_of_mem b hb]
    · simp
    · intro b' _ hne
      rw [ite_eq_right]
      rw [sub_eq_zero]
      exact fun h => hne h.symm
  rw [Finset.sum_congr rfl hrow, Finset.sum_const, nsmul_eq_mul, mul_one]
  exact div_self (Nat.cast_ne_zero.2 hB.card_pos.ne')

/-- in a tiling `A ⊕ B = ZMod M` every `w` has exactly one representation `a + b`, counted as a sum -/
theorem IsTiling.sum_sum_ite {M : ℕ} {A B : Finset (ZMod M)} (h : IsTiling A B) (w : ZMod M) :
    ∑ a ∈ A, ∑ b ∈ B, (if a + b = w then (1 : ℝ) else 0) = 1 := by
  obtain ⟨⟨a1, b1⟩, ⟨ha1, hb1, hab⟩, huniq⟩ := h w
  simp only at ha1 hb1 hab
  rw [Finset.sum_eq_single_of_mem a1 ha1, Finset.sum_eq_single_of_mem b1 hb1]
  · simp [hab]
  · intro b hb hne
    rw [ite_eq_right]
    intro hw
    exact hne (Prod.mk.inj (huniq (a1, b) ⟨ha1, hb, hw⟩)).2
  · intro a ha hne
    refine Finset.sum_eq_zero fun b hb => ?_
    rw [ite_eq_right]
    intro hw
    exact hne (Prod.mk.inj (huniq (a, b) ⟨ha, hb, hw⟩)).1

/-- a tiling complement is nonempty -/
theorem IsTiling.nonempty_right {M : ℕ} {A B : Finset (ZMod M)} (h : IsTiling A B) : B.Nonempty := by
  obtain ⟨⟨a0, b0⟩, ⟨-, hb0, -⟩, -⟩ := h 0
  exact ⟨b0, hb0⟩

/-- `1_A * autocorr B = 1` for a tiling `A ⊕ B = ZMod M` -/
theorem IsTiling.sum_autocorr {M : ℕ} {A B : Finset (ZMod M)} (h : IsTiling A B) (v : ZMod M) :
    ∑ a ∈ A, autocorr B (v - a) = 1 := by
  unfold autocorr
  rw [← Finset.sum_div]
  have key : ∑ a ∈ A, ∑ b ∈ B, ∑ b' ∈ B, (if b - b' = v - a then (1 : ℝ) else 0) = B.card := by
    have hiff : ∀ a b b' : ZMod M, (if b - b' = v - a then (1 : ℝ) else 0)
        = if a + b = v + b' then 1 else 0 := by
      intro a b b'
      have : b - b' = v - a ↔ a + b = v + b' := by
        constructor <;> intro h <;> linear_combination h
      simp only [this]
    simp only [hiff]
    calc ∑ a ∈ A, ∑ b ∈ B, ∑ b' ∈ B, (if a + b = v + b' then (1 : ℝ) else 0)
        = ∑ b' ∈ B, ∑ a ∈ A, ∑ b ∈ B, (if a + b = v + b' then (1 : ℝ) else 0) := by
          rw [Finset.sum_comm (s := B) (t := A)]
          exact Finset.sum_congr rfl fun a _ => Finset.sum_comm
      _ = ∑ b' ∈ B, (1 : ℝ) := Finset.sum_congr rfl fun b' _ => h.sum_sum_ite _
      _ = B.card := by simp
  rw [key]
  exact div_self (Nat.cast_ne_zero.2 h.nonempty_right.card_pos.ne')

/-- the Fourier transform of the normalised autocorrelation of `B` is `|B̂|² / |B|` -/
theorem ft_autocorr {M : ℕ} [NeZero M] (B : Finset (ZMod M)) (ξ : ZMod M) :
    ft (autocorr B) ξ = ((Complex.normSq (hat B ξ) / B.card : ℝ) : ℂ) := by
  rw [Complex.ofReal_div, normSq_hat]
  unfold ft autocorr
  simp only [Complex.ofReal_div, Complex.ofReal_sum, div_mul_eq_mul_div, ← Finset.sum_div,
    Complex.ofReal_natCast]
  congr 1
  simp only [Finset.sum_mul]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun b _ => ?_
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun b' _ => ?_
  rw [Finset.sum_eq_single (b - b')]
  · simp [mul_comm]
  · intro w _ hne
    simp [Ne.symm hne]
  · simp

/-- a tile is a pd-tile: if `A ⊕ B = ZMod M` then `f = (1/|B|) · 1_B * 1_{-B}` is a pd-tiling complement -/
theorem IsTiling.pdTiling {M : ℕ} [NeZero M] {A B : Finset (ZMod M)} (h : IsTiling A B) :
    ∃ f : ZMod M → ℝ, PdTiling A f :=
  ⟨autocorr B, ⟨autocorr_nonneg B, autocorr_zero B h.nonempty_right, h.sum_autocorr⟩,
    fun ξ => ⟨Complex.normSq (hat B ξ) / B.card,
      div_nonneg (Complex.normSq_nonneg _) (Nat.cast_nonneg _), ft_autocorr B ξ⟩⟩

instance instNeZeroPQR (p q r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime] : NeZero (p * q * r) :=
  ⟨Nat.mul_ne_zero (Nat.mul_ne_zero (Fact.out : p.Prime).ne_zero (Fact.out : q.Prime).ne_zero)
    (Fact.out : r.Prime).ne_zero⟩

/-- **In `Z_{pⁿq}` the tiles, the pd-tiles and the weak tiles are the same sets.** -/
theorem tile_iff_pd_iff_weak_pnq (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ n * q))) :
    ((∃ B : Finset (ZMod (p ^ n * q)), IsTiling A B) ↔ ∃ f, PdTiling A f) ∧
    ((∃ f, PdTiling A f) ↔ ∃ f, WeakTiling A f) := by
  have h1 : (∃ B : Finset (ZMod (p ^ n * q)), IsTiling A B) → ∃ f, PdTiling A f :=
    fun ⟨_, hB⟩ => hB.pdTiling
  have h2 : (∃ f, PdTiling A f) → ∃ f, WeakTiling A f := fun ⟨f, hf⟩ => ⟨f, hf.1⟩
  have h3 : (∃ f, WeakTiling A f) → ∃ B : Finset (ZMod (p ^ n * q)), IsTiling A B :=
    fun ⟨f, hf⟩ => Pnq.weak_tiling_tiles_pnq p q n hpq A f hf
  exact ⟨⟨h1, fun h => h3 (h2 h)⟩, ⟨h2, fun h => h1 (h3 h)⟩⟩

/-- **In `Z_{pqr}` the tiles, the pd-tiles and the weak tiles are the same sets.** -/
theorem tile_iff_pd_iff_weak_pqr (p q r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime]
    (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r) (A : Finset (ZMod (p * q * r))) :
    ((∃ B : Finset (ZMod (p * q * r)), IsTiling A B) ↔ ∃ f, PdTiling A f) ∧
    ((∃ f, PdTiling A f) ↔ ∃ f, WeakTiling A f) := by
  have h1 : (∃ B : Finset (ZMod (p * q * r)), IsTiling A B) → ∃ f, PdTiling A f :=
    fun ⟨_, hB⟩ => hB.pdTiling
  have h2 : (∃ f, PdTiling A f) → ∃ f, WeakTiling A f := fun ⟨f, hf⟩ => ⟨f, hf.1⟩
  have h3 : (∃ f, WeakTiling A f) → ∃ B : Finset (ZMod (p * q * r)), IsTiling A B :=
    fun ⟨f, hf⟩ => weak_tiling_tiles_cyclic p q r hpq hpr hqr A f hf
  exact ⟨⟨h1, fun h => h3 (h2 h)⟩, ⟨h2, fun h => h1 (h3 h)⟩⟩

end Pqr
