/-
The two reductions to `ZMod (p * q^2)` and `ZMod (p^2 * q)`:
* Lemma 2: a weak tile with a weak complement that is positive on the units lies in a class modulo `p` or
  modulo `q`, and tiles;
* Lemma 3: a weak tile with a weak complement vanishing outside the multiples of `p` (or of `q`) tiles.
-/
import P2q2.Sub
import P2q2.Common

open Finset

namespace P2q2

open Pqr

/-- Divisibility of `x.val` by a divisor `d` of `M` is the vanishing of the image of `x` in `ZMod d`. -/
theorem dvd_val_iff_castHom {M d : ℕ} [NeZero M] (hd : d ∣ M) (x : ZMod M) :
    d ∣ x.val ↔ ZMod.castHom hd (ZMod d) x = 0 := by
  rw [ZMod.castHom_apply, ← ZMod.natCast_val, ZMod.natCast_eq_zero_iff]

/-- Divisibility of `.val` by a divisor of `M` is compatible with subtraction in `ZMod M`. -/
theorem dvd_val_sub {M d : ℕ} [NeZero M] (hd : d ∣ M) (x y : ZMod M) (hx : d ∣ x.val) (hy : d ∣ y.val) :
    d ∣ (x - y).val := by
  rw [dvd_val_iff_castHom hd] at hx hy ⊢
  rw [map_sub, hx, hy, sub_zero]

/-- Divisibility of `.val` by a divisor of `M` is compatible with addition in `ZMod M`. -/
theorem dvd_val_add {M d : ℕ} [NeZero M] (hd : d ∣ M) (x y : ZMod M) (hx : d ∣ x.val) (hy : d ∣ y.val) :
    d ∣ (x + y).val := by
  rw [dvd_val_iff_castHom hd] at hx hy ⊢
  rw [map_add, hx, hy, add_zero]

/-- In a weak tiling, the weak complement vanishes on the nonzero differences of `A`. -/
theorem weakTiling_diff_eq_zero {G : Type*} [AddCommGroup G] (A : Finset G) (f : G → ℝ)
    (h : WeakTiling A f) {a a' : G} (ha : a ∈ A) (ha' : a' ∈ A) (hne : a ≠ a') : f (a - a') = 0 := by
  classical
  obtain ⟨hnn, h0, hsum⟩ := h
  have h1 := hsum a
  have hsub : ({a, a'} : Finset G) ⊆ A := by
    intro x hx
    rcases mem_insert.mp hx with rfl | hx
    · exact ha
    · rw [mem_singleton.mp hx]; exact ha'
  have h2 : ∑ x ∈ ({a, a'} : Finset G), f (a - x) ≤ ∑ x ∈ A, f (a - x) :=
    sum_le_sum_of_subset_of_nonneg hsub (fun x _ _ => hnn _)
  rw [sum_pair hne, sub_self, h0, h1] at h2
  have h3 := hnn (a - a')
  linarith

variable (p q : ℕ) [Fact p.Prime] [Fact q.Prime]

/-- Lemma 3 for `p`. -/
theorem tiling_of_support_p (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (f : ZMod (p ^ 2 * q ^ 2) → ℝ)
    (h : WeakTiling A f) (hsupp : ∀ x : ZMod (p ^ 2 * q ^ 2), ¬ p ∣ x.val → f x = 0) :
    ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have : NeZero (p ^ 2 * q ^ 2) := ⟨(Nat.mul_pos (pow_pos hp.pos 2) (pow_pos hq.pos 2)).ne'⟩
  have : NeZero (q ^ 2 * p) := ⟨(Nat.mul_pos (pow_pos hq.pos 2) hp.pos).ne'⟩
  have hM : p ^ 2 * q ^ 2 = p * (q ^ 2 * p) := by ring
  obtain ⟨B', hB'⟩ := exists_common_complement_pnq q p 2 (Ne.symm hpq)
    (fun c : ZMod (p ^ 2 * q ^ 2) => piece (p ^ 2 * q ^ 2) (q ^ 2 * p) p A c)
    (fun y => f (iota (p ^ 2 * q ^ 2) (q ^ 2 * p) p y))
    (fun c => weakTiling_piece_of_support hM A f h hsupp c)
  exact tiling_of_pieces hM A B' hB'

/-- Lemma 3 for `q`. -/
theorem tiling_of_support_q (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (f : ZMod (p ^ 2 * q ^ 2) → ℝ)
    (h : WeakTiling A f) (hsupp : ∀ x : ZMod (p ^ 2 * q ^ 2), ¬ q ∣ x.val → f x = 0) :
    ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have : NeZero (p ^ 2 * q ^ 2) := ⟨(Nat.mul_pos (pow_pos hp.pos 2) (pow_pos hq.pos 2)).ne'⟩
  have : NeZero (p ^ 2 * q) := ⟨(Nat.mul_pos (pow_pos hp.pos 2) hq.pos).ne'⟩
  have hM : p ^ 2 * q ^ 2 = q * (p ^ 2 * q) := by ring
  obtain ⟨B', hB'⟩ := exists_common_complement_pnq p q 2 hpq
    (fun c : ZMod (p ^ 2 * q ^ 2) => piece (p ^ 2 * q ^ 2) (p ^ 2 * q) q A c)
    (fun y => f (iota (p ^ 2 * q ^ 2) (p ^ 2 * q) q y))
    (fun c => weakTiling_piece_of_support hM A f h hsupp c)
  exact tiling_of_pieces hM A B' hB'

/-- Lemma 2. -/
theorem tiling_of_units_charged (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2)))
    (f : ZMod (p ^ 2 * q ^ 2) → ℝ) (h : WeakTiling A f)
    (hunit : ∀ x : ZMod (p ^ 2 * q ^ 2), ¬ p ∣ x.val → ¬ q ∣ x.val → 0 < f x) :
    ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have : NeZero (p ^ 2 * q ^ 2) := ⟨(Nat.mul_pos (pow_pos hp.pos 2) (pow_pos hq.pos 2)).ne'⟩
  have : NeZero (q ^ 2 * p) := ⟨(Nat.mul_pos (pow_pos hq.pos 2) hp.pos).ne'⟩
  have : NeZero (p ^ 2 * q) := ⟨(Nat.mul_pos (pow_pos hp.pos 2) hq.pos).ne'⟩
  have hMp : p ^ 2 * q ^ 2 = p * (q ^ 2 * p) := by ring
  have hMq : p ^ 2 * q ^ 2 = q * (p ^ 2 * q) := by ring
  have hpM : p ∣ p ^ 2 * q ^ 2 := ⟨_, hMp⟩
  have hqM : q ∣ p ^ 2 * q ^ 2 := ⟨_, hMq⟩
  -- every difference of two elements of `A` is divisible by `p` or by `q`
  have hdiff : ∀ a ∈ A, ∀ a' ∈ A, p ∣ (a - a').val ∨ q ∣ (a - a').val := by
    intro a ha a' ha'
    by_cases hne : a = a'
    · left
      rw [hne, sub_self, ZMod.val_zero]
      exact dvd_zero p
    · by_contra hcon
      push Not at hcon
      have h1 := hunit (a - a') hcon.1 hcon.2
      have h2 := weakTiling_diff_eq_zero A f h ha ha' hne
      linarith
  obtain ⟨a₀, ha₀⟩ := nonempty_of_weakTiling A f h
  -- `A` lies in one class modulo `p` or in one class modulo `q`
  have hclaim : (∀ a ∈ A, p ∣ (a - a₀).val) ∨ (∀ a ∈ A, q ∣ (a - a₀).val) := by
    by_contra hcon
    push Not at hcon
    obtain ⟨⟨a, ha, hpa⟩, ⟨b, hb, hqb⟩⟩ := hcon
    have hqa : q ∣ (a - a₀).val := (hdiff a ha a₀ ha₀).resolve_left hpa
    have hpb : p ∣ (b - a₀).val := (hdiff b hb a₀ ha₀).resolve_right hqb
    rcases hdiff a ha b hb with hab | hab
    · apply hpa
      have := dvd_val_add hpM _ _ hab hpb
      have e : a - b + (b - a₀) = a - a₀ := by abel
      rwa [e] at this
    · apply hqb
      have := dvd_val_sub hqM _ _ hqa hab
      have e : a - a₀ - (a - b) = b - a₀ := by abel
      rwa [e] at this
  rcases hclaim with hA | hA
  · obtain ⟨B', hB'⟩ := Pnq.weak_tiling_tiles_pnq q p 2 (Ne.symm hpq) _ _
      (weakTiling_piece_of_subset hMp A f h a₀ hA)
    exact tiling_of_piece_subset hMp A a₀ hA B' hB'
  · obtain ⟨B', hB'⟩ := Pnq.weak_tiling_tiles_pnq p q 2 hpq _ _
      (weakTiling_piece_of_subset hMq A f h a₀ hA)
    exact tiling_of_piece_subset hMq A a₀ hA B' hB'

end P2q2
