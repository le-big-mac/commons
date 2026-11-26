import Pnq.Upset
/-!
Audit file 5: facts about the two definitions and the three statements, checked by Lean's kernel.
Nothing here is used by the project; it only tests what the fixed text says.
-/
open Finset Pnq Pnq.Upset

namespace Audit

/-! ### `IsUpSet` -/

/-- the same text with the quantifier over `e` bounded by the divisors of `M` (so that it is decidable) -/
def IsUpSetB (M : ℕ) (D : Finset ℕ) : Prop :=
  (∀ d ∈ D, d ∣ M ∧ d ≠ 1) ∧ ∀ d ∈ D, ∀ e ∈ M.divisors, d ∣ e → e ∈ D

instance (M : ℕ) (D : Finset ℕ) : Decidable (IsUpSetB M D) := by
  unfold IsUpSetB; infer_instance

theorem isUpSet_iff_B {M : ℕ} (hM : M ≠ 0) (D : Finset ℕ) : IsUpSet M D ↔ IsUpSetB M D := by
  unfold IsUpSet IsUpSetB
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨h1, fun d hd e he hde => h2 d hd e hde (Nat.dvd_of_mem_divisors he)⟩
  · rintro ⟨h1, h2⟩
    exact ⟨h1, fun d hd e hde heM => h2 d hd e (Nat.mem_divisors.2 ⟨heM, hM⟩) hde⟩

/-- the intended reading: a set of divisors of `M`, none equal to `1`, closed upward among the divisors -/
theorem isUpSet_iff_intended {M : ℕ} (hM : M ≠ 0) (D : Finset ℕ) :
    IsUpSet M D ↔ D ⊆ M.divisors.erase 1 ∧ ∀ d ∈ D, ∀ e ∈ M.divisors, d ∣ e → e ∈ D := by
  rw [isUpSet_iff_B hM]
  unfold IsUpSetB
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨fun d hd => ?_, h2⟩
    exact Finset.mem_erase.2 ⟨(h1 d hd).2, Nat.mem_divisors.2 ⟨(h1 d hd).1, hM⟩⟩
  · rintro ⟨h1, h2⟩
    refine ⟨fun d hd => ?_, h2⟩
    have := Finset.mem_erase.1 (h1 hd)
    exact ⟨Nat.dvd_of_mem_divisors this.2, this.1⟩

/-- an up-set contains neither `0` nor `1` nor a non-divisor -/
theorem isUpSet_excludes {M : ℕ} (hM : M ≠ 0) {D : Finset ℕ} (hD : IsUpSet M D) :
    (0 : ℕ) ∉ D ∧ (1 : ℕ) ∉ D ∧ ∀ d, ¬ d ∣ M → d ∉ D := by
  refine ⟨fun h => hM (Nat.eq_zero_of_zero_dvd (hD.1 0 h).1), fun h => (hD.1 1 h).2 rfl,
    fun d hd h => hd (hD.1 d h).1⟩

/-- the empty set is an up-set, and so is the set of all divisors other than `1` -/
theorem isUpSet_empty (M : ℕ) : IsUpSet M ∅ := by
  constructor <;> intro d hd <;> simp at hd

theorem isUpSet_all {M : ℕ} (hM : M ≠ 0) : IsUpSet M (M.divisors.erase 1) := by
  rw [isUpSet_iff_intended hM]
  refine ⟨subset_rfl, fun d hd e he hde => Finset.mem_erase.2 ⟨?_, he⟩⟩
  rintro rfl
  exact (Finset.mem_erase.1 hd).1 (Nat.dvd_one.1 hde)

/-- outside the theorems' range (`M = 0`) the definition admits `{0}`; `p^n * q^m` is never `0` -/
example : IsUpSet 0 {0} := by
  constructor
  · intro d hd
    rw [Finset.mem_singleton] at hd
    subst hd
    exact ⟨dvd_rfl, by norm_num⟩
  · intro d hd e hde _
    rw [Finset.mem_singleton] at hd ⊢
    subst hd
    exact Nat.eq_zero_of_zero_dvd hde

example (D : Finset ℕ) : corners 0 D = ∅ := by simp [corners]

/-! ### `corners` -/

/-- `corners M D` is the set of divisors of `M` not in `D` that are maximal for divisibility among those -/
theorem mem_corners_iff {M : ℕ} (hM : M ≠ 0) (D : Finset ℕ) (c : ℕ) :
    c ∈ corners M D ↔ (c ∣ M ∧ c ∉ D) ∧ ∀ e, e ∣ M → e ∉ D → c ∣ e → e = c := by
  rw [corners, Finset.mem_filter, Finset.mem_sdiff, Nat.mem_divisors]
  constructor
  · rintro ⟨⟨⟨h1, -⟩, h2⟩, h3⟩
    exact ⟨⟨h1, h2⟩, fun e he heD hce =>
      h3 e (Finset.mem_sdiff.2 ⟨Nat.mem_divisors.2 ⟨he, hM⟩, heD⟩) hce⟩
  · rintro ⟨⟨h1, h2⟩, h3⟩
    exact ⟨⟨⟨h1, hM⟩, h2⟩, fun e he hce =>
      h3 e (Nat.dvd_of_mem_divisors (Finset.mem_sdiff.1 he).1) (Finset.mem_sdiff.1 he).2 hce⟩

/-- the corners form an antichain for divisibility -/
theorem corners_antichain {M : ℕ} (D : Finset ℕ) {c c' : ℕ} (hc : c ∈ corners M D)
    (hc' : c' ∈ corners M D) (h : c ∣ c') : c' = c :=
  (Aux.mem_corners.1 hc).2 c' (Aux.mem_corners.1 hc').1 h

/-- there is always a corner -/
theorem corners_nonempty {M : ℕ} (hM : M ≠ 0) {D : Finset ℕ} (hD : IsUpSet M D) :
    (corners M D).Nonempty := by
  obtain ⟨c, hc, -⟩ := Aux.exists_corner D 1 (Aux.one_mem hM hD)
  exact ⟨c, hc⟩

/-- an up-set is recovered from its corners: `d ∈ D` iff `d ∣ M` and `d` divides no corner -/
theorem mem_iff_dvd_no_corner {M : ℕ} (hM : M ≠ 0) {D : Finset ℕ} (hD : IsUpSet M D) (d : ℕ) :
    d ∈ D ↔ d ∣ M ∧ ∀ c ∈ corners M D, ¬ d ∣ c := by
  constructor
  · intro hd
    exact ⟨(hD.1 d hd).1, fun c hc hdc => Aux.corner_not_mem hc (hD.2 d hd c hdc (Aux.corner_dvd hc))⟩
  · rintro ⟨hdM, h⟩
    by_contra hdD
    obtain ⟨c, hc, hdc⟩ := Aux.exists_corner D d (Finset.mem_sdiff.2 ⟨Nat.mem_divisors.2 ⟨hdM, hM⟩, hdD⟩)
    exact h c hc hdc

/-- the corner of the empty up-set is `M` itself, and the corner of the largest up-set is `1` -/
theorem corners_empty {M : ℕ} (hM : M ≠ 0) : corners M ∅ = {M} := by
  ext c
  rw [mem_corners_iff hM, Finset.mem_singleton]
  constructor
  · rintro ⟨⟨h1, -⟩, h2⟩
    exact (h2 M dvd_rfl (by simp) h1).symm
  · rintro rfl
    exact ⟨⟨dvd_rfl, by simp⟩, fun e he _ hce => Nat.dvd_antisymm he hce⟩

theorem corners_all {M : ℕ} (hM : M ≠ 0) : corners M (M.divisors.erase 1) = {1} := by
  ext c
  rw [mem_corners_iff hM, Finset.mem_singleton]
  constructor
  · rintro ⟨⟨h1, h2⟩, -⟩
    by_contra hc
    exact h2 (Finset.mem_erase.2 ⟨hc, Nat.mem_divisors.2 ⟨h1, hM⟩⟩)
  · rintro rfl
    refine ⟨⟨one_dvd _, by simp⟩, fun e he heD _ => ?_⟩
    by_contra h1
    exact heD (Finset.mem_erase.2 ⟨h1, Nat.mem_divisors.2 ⟨he, hM⟩⟩)

/-! ### Periodicity under a corner is constancy on the cosets of `c · ZMod M` -/

/-- for `c ∣ M`: `g (x + c) = g x` for all `x` iff `g` depends only on `x.val % c` -/
theorem periodic_iff_factors {M : ℕ} [NeZero M] {c : ℕ} (hc : c ∣ M) (g : ZMod M → ℕ) :
    (∀ x, g (x + (c : ZMod M)) = g x) ↔ ∀ x y : ZMod M, x.val % c = y.val % c → g x = g y := by
  constructor
  · intro h x y hxy
    -- y - x is a multiple of c
    have key : ∀ (j : ℕ) (x : ZMod M), g (x + j • (c : ZMod M)) = g x := Aux.periodic_nsmul g _ h
    have hmod : ((x.val : ℤ) - y.val) % c = 0 := by
      have : (x.val : ℤ) % c = (y.val : ℤ) % c := by exact_mod_cast hxy
      exact Int.emod_eq_emod_iff_emod_sub_eq_zero.1 this
    obtain ⟨k, hk⟩ := Int.dvd_of_emod_eq_zero hmod
    have hx : x = y + ((c : ℤ) * k : ℤ) := by
      have : ((x.val : ℤ) : ZMod M) = ((y.val : ℤ) : ZMod M) + (((c : ℤ) * k : ℤ) : ZMod M) := by
        rw [← Int.cast_add]; congr 1; omega
      simpa using this
    -- reduce to a natural multiple
    obtain ⟨j, hj⟩ : ∃ j : ℕ, (((c : ℤ) * k : ℤ) : ZMod M) = j • (c : ZMod M) := by
      refine ⟨(k % M).toNat, ?_⟩
      have hMpos : (0 : ℤ) < M := by exact_mod_cast Nat.pos_of_ne_zero (NeZero.ne M)
      have h1 : ((k % M).toNat : ℤ) = k % M := Int.toNat_of_nonneg (Int.emod_nonneg _ hMpos.ne')
      have h2 : ((k : ℤ) : ZMod M) = (((k % M).toNat : ℕ) : ZMod M) := by
        rw [← Int.cast_natCast, h1]
        simp
      rw [nsmul_eq_mul, Int.cast_mul, h2]
      push_cast
      ring
    rw [hx, hj, key]
  · intro h x
    apply h
    obtain ⟨t, rfl⟩ := hc
    have hcpos : 0 < c := Nat.pos_of_ne_zero (fun h0 => NeZero.ne (c * t) (by rw [h0, zero_mul]))
    rw [ZMod.val_add, Nat.mod_mod_of_dvd _ (Dvd.intro t rfl), Nat.add_mod, ZMod.val_natCast,
      Nat.mod_mod_of_dvd _ (Dvd.intro t rfl), Nat.mod_self, add_zero, Nat.mod_mod]

/-- under `c = M` every function is periodic (the corner of `D = ∅`) -/
example {M : ℕ} (g : ZMod M → ℕ) (x : ZMod M) : g (x + (M : ZMod M)) = g x := by
  rw [ZMod.natCast_self, add_zero]

/-- under `c = 1` exactly the constants are periodic (the corner of the largest up-set) -/
example {M : ℕ} [NeZero M] (g : ZMod M → ℕ) :
    (∀ x, g (x + ((1 : ℕ) : ZMod M)) = g x) ↔ ∀ x y, g x = g y := by
  rw [periodic_iff_factors (one_dvd M)]
  simp [Nat.mod_one]

end Audit
