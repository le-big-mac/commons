/-
Tools for `Pnq/BuildB.lean`, part 2: the recursive description of the multisets of section 6 of the proof
on paper (a shape part with or without whole fibres), and the facts about it that do not depend on the
particular vectors used at the level `a0`.

`bld C k d z i s c` is the subtree below a class of depth `d` (with `k` levels below it).  The state is:
`z` (does the class meet the shape part?), `i` (its digit at level `a0`, once `d ≥ a0`), `s` (below `a0`:
were all digits so far at levels of `E ∖ F` nonzero?), and `c` (the multiplicity of the fibres over the
strings that are `0` outside `E`, which are superposed on everything).
-/
import Pnq.BuildB1

open Finset

namespace Pnq
namespace BuildB

variable {p q : ℕ}

/-- the data of a construction: the pattern `(Es, Fs)`, the first level `a0` missing from `Fs`, a host level
`hb` (`0` if there is none) with the multiplicity `M` of its fibres, the vectors `vec i s` put on a string
with digit `i` at level `a0` (`s` says whether all its digits at the levels of `E ∖ F` beyond `a0` are
nonzero), their totals `r i`, and an extra multiplicity `ex i` of fibres at level `a0`. -/
structure Cfg (p q : ℕ) where
  Es : Finset ℕ
  Fs : Finset ℕ
  a0 : ℕ
  hb : ℕ
  M : ℕ
  vec : Fin p → Bool → Fin q → ℕ
  ex : Fin p → ℕ
  r : Fin p → ℕ

/-- the levels at which the shape part branches (apart from `a0`): `Es`, and the levels of `Fs` beyond `a0` -/
def Cfg.U (C : Cfg p q) : Finset ℕ := C.Es ∪ C.Fs.filter (fun a => C.a0 < a)

theorem Cfg.mem_U (C : Cfg p q) (a : ℕ) : a ∈ C.U ↔ a ∈ C.Es ∨ (a ∈ C.Fs ∧ C.a0 < a) := by
  simp [Cfg.U]

/-- the subtree below a class of depth `d` in state `(z, i, s, c)` -/
def bld (C : Cfg p q) : (k d : ℕ) → Bool → Fin p → Bool → ℕ → Tree p q k
  | 0, _, z, i, s, c => .leaf (fun j => z.toNat * C.vec i s j + c)
  | k + 1, d, z, i, s, c =>
      if d + 1 = C.hb then
        two (bld C k (d + 1) z i s c) (bld C k (d + 1) false i s (c + z.toNat * C.M))
      else if d + 1 = C.a0 then
        .node (fun x => bld C k (d + 1) z x true
          ((if d + 1 ∈ C.Es ∨ x.val = 0 then c else 0) + z.toNat * C.ex x))
      else if d + 1 ∈ C.Es then
        (if d + 1 ∈ C.Fs then two (bld C k (d + 1) z i s c) (bld C k (d + 1) z i s c)
         else two (bld C k (d + 1) z i false c) (bld C k (d + 1) z i s c))
      else if d + 1 ∈ C.U then two (bld C k (d + 1) z i s c) (bld C k (d + 1) z i s 0)
      else two (bld C k (d + 1) z i s c) (bld C k (d + 1) false i s 0)

section unfold

variable (C : Cfg p q) (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ)

theorem bld_host (h1 : d + 1 = C.hb) : bld C (k + 1) d z i s c =
    two (bld C k (d + 1) z i s c) (bld C k (d + 1) false i s (c + z.toNat * C.M)) := by
  rw [bld, ite_eq_left h1]

theorem bld_mid (h1 : d + 1 ≠ C.hb) (h2 : d + 1 = C.a0) : bld C (k + 1) d z i s c =
    .node (fun x => bld C k (d + 1) z x true
      ((if d + 1 ∈ C.Es ∨ x.val = 0 then c else 0) + z.toNat * C.ex x)) := by
  rw [bld, ite_eq_right h1, ite_eq_left h2]

theorem bld_EF (h1 : d + 1 ≠ C.hb) (h2 : d + 1 ≠ C.a0) (h3 : d + 1 ∈ C.Es) (h4 : d + 1 ∈ C.Fs) :
    bld C (k + 1) d z i s c = two (bld C k (d + 1) z i s c) (bld C k (d + 1) z i s c) := by
  rw [bld, ite_eq_right h1, ite_eq_right h2, ite_eq_left h3, ite_eq_left h4]

theorem bld_H (h1 : d + 1 ≠ C.hb) (h2 : d + 1 ≠ C.a0) (h3 : d + 1 ∈ C.Es) (h4 : d + 1 ∉ C.Fs) :
    bld C (k + 1) d z i s c = two (bld C k (d + 1) z i false c) (bld C k (d + 1) z i s c) := by
  rw [bld, ite_eq_right h1, ite_eq_right h2, ite_eq_left h3, ite_eq_right h4]

theorem bld_G (h1 : d + 1 ≠ C.hb) (h2 : d + 1 ≠ C.a0) (h3 : d + 1 ∉ C.Es) (h4 : d + 1 ∈ C.U) :
    bld C (k + 1) d z i s c = two (bld C k (d + 1) z i s c) (bld C k (d + 1) z i s 0) := by
  rw [bld, ite_eq_right h1, ite_eq_right h2, ite_eq_right h3, ite_eq_left h4]

theorem bld_N (h1 : d + 1 ≠ C.hb) (h2 : d + 1 ≠ C.a0) (h3 : d + 1 ∉ C.Es) (h4 : d + 1 ∉ C.U) :
    bld C (k + 1) d z i s c = two (bld C k (d + 1) z i s c) (bld C k (d + 1) false i s 0) := by
  rw [bld, ite_eq_right h1, ite_eq_right h2, ite_eq_right h3, ite_eq_right h4]

/-- the six kinds of level -/
theorem bld_cases :
    (d + 1 = C.hb ∧ bld C (k + 1) d z i s c =
        two (bld C k (d + 1) z i s c) (bld C k (d + 1) false i s (c + z.toNat * C.M))) ∨
    (d + 1 ≠ C.hb ∧ d + 1 = C.a0 ∧ bld C (k + 1) d z i s c =
        .node (fun x => bld C k (d + 1) z x true
          ((if d + 1 ∈ C.Es ∨ x.val = 0 then c else 0) + z.toNat * C.ex x))) ∨
    (d + 1 ≠ C.hb ∧ d + 1 ≠ C.a0 ∧ d + 1 ∈ C.Es ∧ d + 1 ∈ C.Fs ∧ bld C (k + 1) d z i s c =
        two (bld C k (d + 1) z i s c) (bld C k (d + 1) z i s c)) ∨
    (d + 1 ≠ C.hb ∧ d + 1 ≠ C.a0 ∧ d + 1 ∈ C.Es ∧ d + 1 ∉ C.Fs ∧ bld C (k + 1) d z i s c =
        two (bld C k (d + 1) z i false c) (bld C k (d + 1) z i s c)) ∨
    (d + 1 ≠ C.hb ∧ d + 1 ≠ C.a0 ∧ d + 1 ∉ C.Es ∧ d + 1 ∈ C.U ∧ bld C (k + 1) d z i s c =
        two (bld C k (d + 1) z i s c) (bld C k (d + 1) z i s 0)) ∨
    (d + 1 ≠ C.hb ∧ d + 1 ≠ C.a0 ∧ d + 1 ∉ C.Es ∧ d + 1 ∉ C.U ∧ bld C (k + 1) d z i s c =
        two (bld C k (d + 1) z i s c) (bld C k (d + 1) false i s 0)) := by
  by_cases h1 : d + 1 = C.hb
  · exact Or.inl ⟨h1, bld_host C k d z i s c h1⟩
  by_cases h2 : d + 1 = C.a0
  · exact Or.inr (Or.inl ⟨h1, h2, bld_mid C k d z i s c h1 h2⟩)
  by_cases h3 : d + 1 ∈ C.Es
  · by_cases h4 : d + 1 ∈ C.Fs
    · exact Or.inr (Or.inr (Or.inl ⟨h1, h2, h3, h4, bld_EF C k d z i s c h1 h2 h3 h4⟩))
    · exact Or.inr (Or.inr (Or.inr (Or.inl ⟨h1, h2, h3, h4, bld_H C k d z i s c h1 h2 h3 h4⟩)))
  · by_cases h4 : d + 1 ∈ C.U
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inl ⟨h1, h2, h3, h4, bld_G C k d z i s c h1 h2 h3 h4⟩))))
    · exact Or.inr (Or.inr (Or.inr (Or.inr (Or.inr ⟨h1, h2, h3, h4, bld_N C k d z i s c h1 h2 h3 h4⟩))))

end unfold

/-! ### Layer vectors -/

/-- a class that does not meet the shape part and carries no fibres is empty -/
theorem lay_bld_empty (hp : 0 < p) (C : Cfg p q) :
    ∀ (k d : ℕ) (i : Fin p) (s : Bool) (j : Fin q), lay (bld C k d false i s 0) j = 0
  | 0, _, _, _, _ => by simp [bld, lay]
  | k + 1, d, i, s, j => by
      have ih := lay_bld_empty hp C k (d + 1)
      rcases bld_cases C k d false i s 0 with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · rw [e, lay_two hp]; simp [ih]
      · rw [e, lay_node]; simp [ih]
      all_goals rw [e, lay_two hp]; simp [ih]

/-- the fibres of multiplicity `c` are superposed on the rest -/
theorem lay_bld_c (hp : 0 < p) (C : Cfg p q) (hh : C.hb = 0 ∨ C.hb ∈ C.Es) (j : Fin q) :
    ∀ (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ),
      lay (bld C k d z i s c) j = lay (bld C k d z i s 0) j + c * pw p C.Es k d := by
  obtain ⟨m, rfl⟩ : ∃ m, p = m + 1 := ⟨p - 1, by omega⟩
  intro k
  induction k with
  | zero => intro d z i s c; simp [bld, lay, pw]
  | succ k ih =>
    intro d z i s c
    have hU : d + 1 ∉ C.U → d + 1 ∉ C.Es := fun h h' => h ((C.mem_U _).2 (Or.inl h'))
    rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
      ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
    · have hE : d + 1 ∈ C.Es := by
        rcases hh with h | h
        · omega
        · rw [h1]; exact h
      rw [e, bld_host C k d z i s 0 h1, lay_two hp, lay_two hp, pw_succ_mem k hE,
        ih (d + 1) z i s c, ih (d + 1) false i s (c + z.toNat * C.M),
        ih (d + 1) false i s (0 + z.toNat * C.M)]
      simp only [Nat.add_sub_cancel]
      ring
    · have t : ∀ (x : Fin (m + 1)) (c' : ℕ),
          lay (bld C k (d + 1) z x true (c' + z.toNat * C.ex x)) j
            = lay (bld C k (d + 1) z x true (0 + z.toNat * C.ex x)) j
              + c' * pw (m + 1) C.Es k (d + 1) := by
        intro x c'
        rw [ih (d + 1) z x true (c' + _), ih (d + 1) z x true (0 + _)]
        ring
      rw [e, bld_mid C k d z i s 0 h1 h2, lay_node, lay_node]
      simp only [ite_self]
      rw [Finset.sum_congr rfl
        (fun x _ => t x (if d + 1 ∈ C.Es ∨ x.val = 0 then c else 0)), Finset.sum_add_distrib]
      congr 1
      by_cases hE : d + 1 ∈ C.Es
      · simp only [hE, true_or, ite_true, pw_succ_mem k hE, Finset.sum_const, Finset.card_univ,
          Fintype.card_fin, smul_eq_mul]
        ring
      · simp only [hE, false_or, pw_succ_not k hE, ite_mul, zero_mul]
        rw [sum_ite_zero hp]
        simp
    · rw [e, bld_EF C k d z i s 0 h1 h2 h3 h4, lay_two hp, lay_two hp, pw_succ_mem k h3,
        ih (d + 1) z i s c]
      simp only [Nat.add_sub_cancel]
      ring
    · rw [e, bld_H C k d z i s 0 h1 h2 h3 h4, lay_two hp, lay_two hp, pw_succ_mem k h3,
        ih (d + 1) z i false c, ih (d + 1) z i s c]
      simp only [Nat.add_sub_cancel]
      ring
    · rw [e, bld_G C k d z i s 0 h1 h2 h3 h4, lay_two hp, lay_two hp, pw_succ_not k h3,
        ih (d + 1) z i s c]
      ring
    · rw [e, bld_N C k d z i s 0 h1 h2 h3 h4, lay_two hp, lay_two hp, pw_succ_not k (hU h4),
        ih (d + 1) z i s c]
      ring

theorem size_bld_c (hp : 0 < p) (C : Cfg p q) (hh : C.hb = 0 ∨ C.hb ∈ C.Es)
    (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ) :
    size (bld C k d z i s c) = size (bld C k d z i s 0) + q * (c * pw p C.Es k d) := by
  unfold size
  rw [Finset.sum_congr rfl (fun j _ => lay_bld_c hp C hh j k d z i s c), Finset.sum_add_distrib,
    Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul]

/-! ### The layer vector of a class of depth `≥ a0` -/

/-- the number of strings of the shape part below a class all of whose further digits at the levels of
`E ∖ F` are nonzero -/
def Wc (C : Cfg p q) : ℕ → ℕ → ℕ
  | 0, _ => 1
  | k + 1, d =>
      (if d + 1 = C.hb then 1 else if d + 1 ∈ C.Es then (if d + 1 ∈ C.Fs then p else p - 1)
        else if d + 1 ∈ C.U then p else 1) * Wc C k (d + 1)

/-- the number of the other strings of the shape part below a class -/
def Dc (C : Cfg p q) : ℕ → ℕ → ℕ
  | 0, _ => 0
  | k + 1, d =>
      if d + 1 = C.hb then Dc C k (d + 1)
      else if d + 1 ∈ C.Es then
        (if d + 1 ∈ C.Fs then p * Dc C k (d + 1)
         else Dc C k (d + 1) + Wc C k (d + 1) + (p - 1) * Dc C k (d + 1))
      else if d + 1 ∈ C.U then p * Dc C k (d + 1) else Dc C k (d + 1)

/-- the number of elements in each layer that the fibres at the host level add to a class -/
def hc (C : Cfg p q) : ℕ → ℕ → ℕ
  | 0, _ => 0
  | k + 1, d =>
      if d + 1 = C.hb then hc C k (d + 1) + (p - 1) * (C.M * pw p C.Es k (d + 1))
      else if d + 1 ∈ C.U then p * hc C k (d + 1) else hc C k (d + 1)

theorem lay_bld_below (hp : 0 < p) (C : Cfg p q) (hh : C.hb = 0 ∨ C.hb ∈ C.Es) (j : Fin q) :
    ∀ (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool), C.a0 ≤ d →
      lay (bld C k d z i s 0) j
        = z.toNat * (Dc C k d * C.vec i false j + Wc C k d * C.vec i s j + hc C k d) := by
  obtain ⟨m, rfl⟩ : ∃ m, p = m + 1 := ⟨p - 1, by omega⟩
  intro k
  induction k with
  | zero => intro d z i s _; simp [bld, lay, Dc, Wc, hc]
  | succ k ih =>
    intro d z i s hd
    have hU : d + 1 ∈ C.Es → d + 1 ∈ C.U := fun h' => (C.mem_U _).2 (Or.inl h')
    rcases bld_cases C k d z i s 0 with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
      ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
    · rw [e, lay_two hp, ih (d + 1) z i s (by omega),
        lay_bld_c hp C hh j k (d + 1) false i s (0 + z.toNat * C.M), lay_bld_empty hp]
      simp only [Dc, Wc, hc, h1, ite_true, Nat.add_sub_cancel]
      ring
    · omega
    · rw [e, lay_two hp, ih (d + 1) z i s (by omega)]
      simp only [Dc, Wc, hc, h1, h3, h4, hU h3, ite_true, ite_false, Nat.add_sub_cancel]
      ring
    · rw [e, lay_two hp, ih (d + 1) z i false (by omega), ih (d + 1) z i s (by omega)]
      simp only [Dc, Wc, hc, h1, h3, h4, hU h3, ite_true, ite_false, Nat.add_sub_cancel]
      ring
    · rw [e, lay_two hp, ih (d + 1) z i s (by omega)]
      simp only [Dc, Wc, hc, h1, h3, h4, ite_true, ite_false, Nat.add_sub_cancel]
      ring
    · rw [e, lay_two hp, ih (d + 1) z i s (by omega), lay_bld_empty hp]
      simp only [Dc, Wc, hc, h1, h3, h4, ite_false, Nat.add_sub_cancel]
      ring

theorem coprime_DW (hp : 0 < p) (hpq : Nat.Coprime p q) (C : Cfg p q) :
    ∀ k d, Nat.Coprime (Dc C k d + Wc C k d) q := by
  obtain ⟨m, rfl⟩ : ∃ m, p = m + 1 := ⟨p - 1, by omega⟩
  intro k
  induction k with
  | zero => intro d; simp [Dc, Wc]
  | succ k ih =>
    intro d
    have key : Dc C (k + 1) d + Wc C (k + 1) d = Dc C k (d + 1) + Wc C k (d + 1) ∨
        Dc C (k + 1) d + Wc C (k + 1) d = (m + 1) * (Dc C k (d + 1) + Wc C k (d + 1)) := by
      by_cases h1 : d + 1 = C.hb
      · left; simp only [Dc, Wc, h1, ite_true]; ring
      by_cases h3 : d + 1 ∈ C.Es
      · right
        by_cases h4 : d + 1 ∈ C.Fs
        · simp only [Dc, Wc, h1, h3, h4, ite_true, ite_false]; ring
        · simp only [Dc, Wc, h1, h3, h4, ite_true, ite_false, Nat.add_sub_cancel]; ring
      · by_cases h4 : d + 1 ∈ C.U
        · right; simp only [Dc, Wc, h1, h3, h4, ite_true, ite_false]; ring
        · left; simp only [Dc, Wc, h1, h3, h4, ite_false]; ring
    rcases key with h | h
    · rw [h]; exact ih (d + 1)
    · rw [h]; exact Nat.Coprime.mul_left hpq (ih (d + 1))

theorem Wc_pos (hp : 2 ≤ p) (C : Cfg p q) : ∀ k d, 1 ≤ Wc C k d
  | 0, _ => le_refl 1
  | k + 1, d => by
      rw [Wc]
      exact Nat.mul_pos (by split_ifs <;> omega) (Wc_pos hp C k (d + 1))

end BuildB
end Pnq
