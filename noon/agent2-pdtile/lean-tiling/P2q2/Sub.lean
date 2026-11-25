/-
Transport between `ZMod M` and its subgroup of multiples of `r`, identified with `ZMod N` when `M = r * N`.
General (no primes): pieces of a set in the classes modulo `r`, weak tilings of the pieces, and how tilings of
the pieces assemble.
-/
import Pqr.Cyclic

open Finset

set_option linter.unusedSectionVars false

namespace P2q2

open Pqr

/-- `y ↦ r * y`, from `ZMod N` to `ZMod M` (used with `M = r * N`) -/
def iota (M N r : ℕ) (y : ZMod N) : ZMod M := ((r * y.val : ℕ) : ZMod M)

open Classical in
/-- the piece of `A` in the class of `c` modulo `r`, pulled back to `ZMod N` -/
noncomputable def piece (M N r : ℕ) [NeZero N] (A : Finset (ZMod M)) (c : ZMod M) : Finset (ZMod N) :=
  Finset.univ.filter (fun y => c + iota M N r y ∈ A)

variable {M N r : ℕ} [NeZero M] [NeZero N]

/-! ### Basic facts about `iota` -/

theorem mem_piece {A : Finset (ZMod M)} {c : ZMod M} {y : ZMod N} :
    y ∈ piece M N r A c ↔ c + iota M N r y ∈ A := by
  simp [piece]

/-- `iota` of a natural number -/
theorem iota_natCast (hM : M = r * N) (k : ℕ) :
    iota M N r (k : ZMod N) = ((r * k : ℕ) : ZMod M) := by
  subst hM
  unfold iota
  rw [ZMod.val_natCast, ZMod.natCast_eq_natCast_iff]
  exact (Nat.mod_modEq k N).mul_left' r

theorem iota_zero : iota M N r 0 = 0 := by
  simp [iota]

theorem iota_add (hM : M = r * N) (y y' : ZMod N) :
    iota M N r (y + y') = iota M N r y + iota M N r y' := by
  have h := iota_natCast hM (y.val + y'.val)
  rw [Nat.cast_add, ZMod.natCast_zmod_val, ZMod.natCast_zmod_val] at h
  rw [h]
  unfold iota
  push_cast
  ring

theorem iota_neg (hM : M = r * N) (y : ZMod N) : iota M N r (-y) = -iota M N r y := by
  have h := iota_add hM (-y) y
  rw [neg_add_cancel, iota_zero] at h
  exact eq_neg_of_add_eq_zero_left h.symm

theorem iota_sub (hM : M = r * N) (y y' : ZMod N) :
    iota M N r (y - y') = iota M N r y - iota M N r y' := by
  rw [sub_eq_add_neg, iota_add hM, iota_neg hM, ← sub_eq_add_neg]

theorem r_ne_zero (hM : M = r * N) : r ≠ 0 := by
  rintro rfl
  exact NeZero.ne M (by rw [hM, zero_mul])

theorem iota_injective (hM : M = r * N) : Function.Injective (iota M N r) := by
  intro y y' h
  have hr : r ≠ 0 := r_ne_zero hM
  subst hM
  unfold iota at h
  rw [ZMod.natCast_eq_natCast_iff] at h
  have h2 : y.val ≡ y'.val [MOD N] := Nat.ModEq.mul_left_cancel' hr h
  exact ZMod.val_injective N (Nat.ModEq.eq_of_lt_of_lt h2 (ZMod.val_lt y) (ZMod.val_lt y'))

/-- divisibility of the value by `r ∣ M` is the vanishing of the reduction modulo `r` -/
theorem dvd_val_iff (hr : r ∣ M) (x : ZMod M) :
    r ∣ x.val ↔ (ZMod.castHom hr (ZMod r)) x = 0 := by
  rw [ZMod.castHom_apply, ← ZMod.natCast_val, ZMod.natCast_eq_zero_iff]

theorem dvd_val_iota (hM : M = r * N) (y : ZMod N) : r ∣ (iota M N r y).val := by
  subst hM
  unfold iota
  rw [ZMod.val_natCast]
  exact (Nat.dvd_mod_iff (dvd_mul_right r N)).2 (dvd_mul_right r _)

/-- the image of `iota` is the set of multiples of `r` -/
theorem exists_iota_iff (hM : M = r * N) (x : ZMod M) :
    (∃ y, iota M N r y = x) ↔ r ∣ x.val := by
  constructor
  · rintro ⟨y, rfl⟩
    exact dvd_val_iota hM y
  · rintro ⟨k, hk⟩
    refine ⟨(k : ZMod N), ?_⟩
    rw [iota_natCast hM, ← hk, ZMod.natCast_zmod_val]

/-- subtracting the residue modulo `r` gives a multiple of `r` -/
theorem dvd_val_sub_mod (hr : r ∣ M) (w : ZMod M) :
    r ∣ (w - ((w.val % r : ℕ) : ZMod M)).val := by
  rw [dvd_val_iff hr, map_sub, map_natCast, ZMod.natCast_mod, ZMod.natCast_val,
    ZMod.castHom_apply, sub_self]

/-- the residue modulo `r` of `iota z + j` with `j < r` is `j` -/
theorem mod_eq_of_iota_add (hM : M = r * N) (w : ZMod M) (z : ZMod N) (j : ℕ) (hj : j < r)
    (hw : w = iota M N r z + (j : ZMod M)) : w.val % r = j := by
  have hr : r ∣ M := hM ▸ dvd_mul_right r N
  have h1 : (ZMod.castHom hr (ZMod r)) (iota M N r z) = 0 :=
    (dvd_val_iff hr _).1 (dvd_val_iota hM z)
  have h2 := congrArg (ZMod.castHom hr (ZMod r)) hw
  rw [map_add, h1, zero_add, map_natCast, ZMod.castHom_apply, ← ZMod.natCast_val,
    ZMod.natCast_eq_natCast_iff'] at h2
  rw [h2, Nat.mod_eq_of_lt hj]

/-- the sum over a piece, rewritten as a sum over the part of `A` in the class of `c` -/
theorem sum_piece (hM : M = r * N) (A : Finset (ZMod M)) (f : ZMod M → ℝ) (c : ZMod M)
    (y : ZMod N) :
    ∑ x ∈ piece M N r A c, f (iota M N r (y - x))
      = ∑ a ∈ (piece M N r A c).image (fun x => c + iota M N r x),
          f (c + iota M N r y - a) := by
  rw [Finset.sum_image]
  · refine Finset.sum_congr rfl fun x _ => ?_
    rw [iota_sub hM]
    congr 1
    abel
  · intro x _ x' _ hxx'
    exact iota_injective hM (add_left_cancel hxx')

theorem image_piece_subset (A : Finset (ZMod M)) (c : ZMod M) :
    (piece M N r A c).image (fun x => c + iota M N r x) ⊆ A := by
  intro a ha
  obtain ⟨x, hx, rfl⟩ := Finset.mem_image.1 ha
  exact mem_piece.1 hx

/-- an element of `A` in the class of `c` comes from the piece -/
theorem mem_image_piece (hM : M = r * N) (A : Finset (ZMod M)) (c a : ZMod M) (ha : a ∈ A)
    (hd : r ∣ (a - c).val) : a ∈ (piece M N r A c).image (fun x => c + iota M N r x) := by
  obtain ⟨z, hz⟩ := (exists_iota_iff hM _).2 hd
  have hca : c + iota M N r z = a := by rw [hz]; abel
  exact Finset.mem_image.2 ⟨z, mem_piece.2 (hca ▸ ha), hca⟩

/-! ### Weak tilings of the pieces -/

/-- If a weak complement `f` of `A` vanishes outside the multiples of `r`, every piece of `A` is a weak tile of
`ZMod N` with the weak complement `f ∘ iota`. -/
theorem weakTiling_piece_of_support (hM : M = r * N) (A : Finset (ZMod M)) (f : ZMod M → ℝ)
    (h : WeakTiling A f) (hsupp : ∀ x : ZMod M, ¬ r ∣ x.val → f x = 0) (c : ZMod M) :
    WeakTiling (piece M N r A c) (fun y => f (iota M N r y)) := by
  refine ⟨fun y => h.1 _, by simpa [iota_zero] using h.2.1, fun y => ?_⟩
  rw [sum_piece hM, ← h.2.2 (c + iota M N r y)]
  apply Finset.sum_subset (image_piece_subset A c)
  intro a ha hna
  apply hsupp
  intro hdvd
  obtain ⟨z, hz⟩ := (exists_iota_iff hM _).2 hdvd
  apply hna
  apply mem_image_piece hM A c a ha
  have : a - c = iota M N r (y - z) := by rw [iota_sub hM, hz]; abel
  rw [this]
  exact dvd_val_iota hM _

/-- If `A` lies in one class modulo `r`, its piece there is a weak tile of `ZMod N` (for any weak complement). -/
theorem weakTiling_piece_of_subset (hM : M = r * N) (A : Finset (ZMod M)) (f : ZMod M → ℝ)
    (h : WeakTiling A f) (c : ZMod M) (hA : ∀ a ∈ A, r ∣ (a - c).val) :
    WeakTiling (piece M N r A c) (fun y => f (iota M N r y)) := by
  refine ⟨fun y => h.1 _, by simpa [iota_zero] using h.2.1, fun y => ?_⟩
  have himg : (piece M N r A c).image (fun x => c + iota M N r x) = A :=
    Finset.Subset.antisymm (image_piece_subset A c)
      (fun a ha => mem_image_piece hM A c a ha (hA a ha))
  rw [sum_piece hM, himg]
  exact h.2.2 _

/-! ### Assembling tilings -/

/-- If all pieces of `A` tile `ZMod N` with the same complement, `A` tiles `ZMod M`. -/
theorem tiling_of_pieces (hM : M = r * N) (A : Finset (ZMod M)) (B' : Finset (ZMod N))
    (h : ∀ c : ZMod M, IsTiling (piece M N r A c) B') : ∃ B : Finset (ZMod M), IsTiling A B := by
  refine ⟨B'.image (iota M N r), fun v => ?_⟩
  obtain ⟨⟨x, b⟩, ⟨hx, hb, hxb⟩, huniq⟩ := h v 0
  simp only at hx hb hxb
  refine ⟨(v + iota M N r x, iota M N r b), ⟨mem_piece.1 hx, Finset.mem_image_of_mem _ hb, ?_⟩, ?_⟩
  · show v + iota M N r x + iota M N r b = v
    rw [add_assoc, ← iota_add hM, hxb, iota_zero, add_zero]
  · rintro ⟨a', β'⟩ ⟨ha', hβ', hab'⟩
    simp only at ha' hβ' hab'
    obtain ⟨b', hb', rfl⟩ := Finset.mem_image.1 hβ'
    have ha'eq : a' = v + iota M N r (-b') := by rw [iota_neg hM, ← hab']; abel
    have hmem : -b' ∈ piece M N r A v := mem_piece.2 (ha'eq ▸ ha')
    have := huniq (-b', b') ⟨hmem, hb', neg_add_cancel b'⟩
    simp only [Prod.mk.injEq] at this
    obtain ⟨h1, h2⟩ := this
    rw [ha'eq, h1, h2]

/-- If `A` lies in one class modulo `r` and its piece tiles `ZMod N`, then `A` tiles `ZMod M`. -/
theorem tiling_of_piece_subset (hM : M = r * N) (A : Finset (ZMod M)) (c : ZMod M)
    (hA : ∀ a ∈ A, r ∣ (a - c).val) (B' : Finset (ZMod N)) (h : IsTiling (piece M N r A c) B') :
    ∃ B : Finset (ZMod M), IsTiling A B := by
  have hr : r ∣ M := hM ▸ dvd_mul_right r N
  have hr0 : 0 < r := Nat.pos_of_ne_zero (r_ne_zero hM)
  refine ⟨(B' ×ˢ Finset.range r).image (fun bj => iota M N r bj.1 + ((bj.2 : ℕ) : ZMod M)),
    fun v => ?_⟩
  obtain ⟨y, hy⟩ := (exists_iota_iff hM _).2 (dvd_val_sub_mod hr (v - c))
  obtain ⟨⟨x, b⟩, ⟨hx, hb, hxb⟩, huniq⟩ := h y
  simp only at hx hb hxb
  refine ⟨(c + iota M N r x, iota M N r b + (((v - c).val % r : ℕ) : ZMod M)),
    ⟨mem_piece.1 hx, ?_, ?_⟩, ?_⟩
  · exact Finset.mem_image.2 ⟨(b, (v - c).val % r),
      Finset.mem_product.2 ⟨hb, Finset.mem_range.2 (Nat.mod_lt _ hr0)⟩, rfl⟩
  · show c + iota M N r x + (iota M N r b + (((v - c).val % r : ℕ) : ZMod M)) = v
    have hsum : iota M N r x + iota M N r b = v - c - (((v - c).val % r : ℕ) : ZMod M) := by
      rw [← iota_add hM, hxb, hy]
    calc c + iota M N r x + (iota M N r b + (((v - c).val % r : ℕ) : ZMod M))
        = c + (iota M N r x + iota M N r b) + (((v - c).val % r : ℕ) : ZMod M) := by abel
      _ = v := by rw [hsum]; abel
  · rintro ⟨a', β'⟩ ⟨ha', hβ', hab'⟩
    simp only at ha' hβ' hab'
    obtain ⟨⟨b', j'⟩, hbj, rfl⟩ := Finset.mem_image.1 hβ'
    obtain ⟨hb', hj'⟩ := Finset.mem_product.1 hbj
    simp only [Finset.mem_range] at hb' hj'
    obtain ⟨x', hx'⟩ := (exists_iota_iff hM _).2 (hA a' ha')
    have ha'eq : a' = c + iota M N r x' := by rw [hx']; abel
    have hx'mem : x' ∈ piece M N r A c := mem_piece.2 (ha'eq ▸ ha')
    have hvc : v - c = iota M N r (x' + b') + (j' : ZMod M) := by
      rw [← hab', ha'eq, iota_add hM]; abel
    have hjj : (v - c).val % r = j' := mod_eq_of_iota_add hM _ _ _ hj' hvc
    have hyy : y = x' + b' := by
      apply iota_injective hM
      rw [hy, hjj, hvc]; abel
    have := huniq (x', b') ⟨hx'mem, hb', hyy.symm⟩
    simp only [Prod.mk.injEq] at this
    obtain ⟨h1, h2⟩ := this
    rw [ha'eq, hjj, h1, h2]

end P2q2
