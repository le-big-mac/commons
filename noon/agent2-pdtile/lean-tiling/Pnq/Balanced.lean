import Pnq.Sharp

open Finset

namespace Pnq

variable {p q : ℕ}

open Classical in
/-- the levels beyond `a0` that are in `F` and not in `E` -/
noncomputable def gBeyond {n : ℕ} (t : Tree p q n) (a0 : ℕ) : Finset ℕ :=
  (fSet t \ eSet t).filter (fun ℓ => a0 < ℓ)

/-!
The least size of a balanced multiset on `Z_{pⁿ} × Z_q` with a given pattern: the lower bounds
(Proposition 7 and the case `x = 1` of Theorem B of `minsize/prove/proof.md`, sections 1 to 5).

A "class of depth `d`" of the paper is a subtree here.  "A pair `(E, F)` contained in the pattern of a
class" is a pair of finsets `E'`, `F'` with `∀ ℓ ∈ E', E t ℓ` and `∀ ℓ ∈ F', 1 ≤ ℓ ∧ F t ℓ`.  The shifted
pair of the paper is `(sh E', sh F')`.  "The class has a witness at level `g`" is `¬ E t g` (with `g` in
range, which here always follows from `g ∈ F'`).
-/

theorem mem_gBeyond {n : ℕ} (t : Tree p q n) (a0 ℓ : ℕ) :
    ℓ ∈ gBeyond t a0 ↔ (ℓ ∈ fSet t ∧ ℓ ∉ eSet t) ∧ a0 < ℓ := by
  unfold gBeyond
  rw [Finset.mem_filter, Finset.mem_sdiff]

/-! ### The three sets of integers, and the arithmetic (A1) to (A5) -/

/-- `S_u = {p^u t + q m : t ≥ 1, m ≥ 0}` -/
def InS (p q u x : ℕ) : Prop := ∃ t m, 1 ≤ t ∧ x = p ^ u * t + q * m

/-- `S_u⁺ = {p^u t + q m : t ≥ 1, m ≥ 1}` -/
def InSplus (p q u x : ℕ) : Prop := ∃ t m, 1 ≤ t ∧ 1 ≤ m ∧ x = p ^ u * t + q * m

/-- `Q_u = {q p^u t : t ≥ 1}` -/
def InQ (p q u x : ℕ) : Prop := ∃ t, 1 ≤ t ∧ x = q * p ^ u * t

/-- `S_0` is the set of positive integers -/
theorem InS.of_pos {x : ℕ} (hx : 1 ≤ x) : InS p q 0 x := ⟨x, 0, hx, by simp⟩

theorem InS.pos (hp : 0 < p) {u x : ℕ} (h : InS p q u x) : 1 ≤ x := by
  obtain ⟨t, m, ht, rfl⟩ := h
  have : 0 < p ^ u * t := Nat.mul_pos (Nat.pow_pos hp) ht
  omega

theorem InQ.le {u x : ℕ} (h : InQ p q u x) : q * p ^ u ≤ x := by
  obtain ⟨t, ht, rfl⟩ := h
  exact Nat.le_mul_of_pos_right _ ht

/-- (A1) for `S` -/
theorem InS.mul_p {u x : ℕ} (h : InS p q u x) : InS p q (u + 1) (p * x) := by
  obtain ⟨t, m, ht, rfl⟩ := h
  exact ⟨t, p * m, ht, by ring⟩

/-- (A1) for `S⁺` -/
theorem InSplus.mul_p (hp : 0 < p) {u x : ℕ} (h : InSplus p q u x) :
    InSplus p q (u + 1) (p * x) := by
  obtain ⟨t, m, ht, hm, rfl⟩ := h
  exact ⟨t, p * m, ht, Nat.mul_pos hp hm, by ring⟩

/-- (A1) for `Q` -/
theorem InQ.mul_p {u x : ℕ} (h : InQ p q u x) : InQ p q (u + 1) (p * x) := by
  obtain ⟨t, ht, rfl⟩ := h
  exact ⟨t, ht, by ring⟩

/-- (A2) `S_u + S_u ⊆ S_u` -/
theorem InS.add {u x y : ℕ} (hx : InS p q u x) (hy : InS p q u y) : InS p q u (x + y) := by
  obtain ⟨t, m, ht, rfl⟩ := hx
  obtain ⟨t', m', -, rfl⟩ := hy
  exact ⟨t + t', m + m', by omega, by ring⟩

/-- (A2) `S_u + qZ_{≥0} ⊆ S_u` -/
theorem InS.add_dvd {u x y : ℕ} (hx : InS p q u x) (hy : q ∣ y) : InS p q u (x + y) := by
  obtain ⟨t, m, ht, rfl⟩ := hx
  obtain ⟨m', rfl⟩ := hy
  exact ⟨t, m + m', ht, by ring⟩

theorem InS.add_or {u x y : ℕ} (hx : InS p q u x) (hy : InS p q u y ∨ q ∣ y) :
    InS p q u (x + y) := by
  rcases hy with h | h
  · exact hx.add h
  · exact hx.add_dvd h

/-- (A2) `S_u + qZ_{≥1} ⊆ S_u⁺` -/
theorem InS.add_mul_pos {u x m : ℕ} (hx : InS p q u x) (hm : 1 ≤ m) :
    InSplus p q u (x + q * m) := by
  obtain ⟨t, m', ht, rfl⟩ := hx
  exact ⟨t, m' + m, ht, by omega, by ring⟩

/-- (A2) `S_u⁺ + S_u ⊆ S_u⁺` -/
theorem InSplus.add {u x y : ℕ} (hx : InSplus p q u x) (hy : InS p q u y) :
    InSplus p q u (x + y) := by
  obtain ⟨t, m, ht, hm, rfl⟩ := hx
  obtain ⟨t', m', -, rfl⟩ := hy
  exact ⟨t + t', m + m', by omega, by omega, by ring⟩

/-- (A2) `S_u⁺ + qZ_{≥0} ⊆ S_u⁺` -/
theorem InSplus.add_dvd {u x y : ℕ} (hx : InSplus p q u x) (hy : q ∣ y) :
    InSplus p q u (x + y) := by
  obtain ⟨t, m, ht, hm, rfl⟩ := hx
  obtain ⟨m', rfl⟩ := hy
  exact ⟨t, m + m', ht, by omega, by ring⟩

theorem InSplus.add_or {u x y : ℕ} (hx : InSplus p q u x) (hy : InS p q u y ∨ q ∣ y) :
    InSplus p q u (x + y) := by
  rcases hy with h | h
  · exact hx.add h
  · exact hx.add_dvd h

/-- (A3) `Q_u + S_u ⊆ S_u⁺` -/
theorem InQ.add_S (hp : 0 < p) {u x y : ℕ} (hx : InQ p q u x) (hy : InS p q u y) :
    InSplus p q u (x + y) := by
  obtain ⟨t', ht', rfl⟩ := hx
  obtain ⟨t, m, ht, rfl⟩ := hy
  have : 0 < p ^ u * t' := Nat.mul_pos (Nat.pow_pos hp) ht'
  exact ⟨t, p ^ u * t' + m, ht, by omega, by ring⟩

/-- (A3) `Q_u + qZ_{≥1} ⊆ S_u⁺` -/
theorem InQ.add_mul_pos (hq : 0 < q) {u x m : ℕ} (hx : InQ p q u x) (hm : 1 ≤ m) :
    InSplus p q u (x + q * m) := by
  obtain ⟨t', ht', rfl⟩ := hx
  obtain ⟨s, rfl⟩ : ∃ s, t' = s + 1 := ⟨t' - 1, by omega⟩
  exact ⟨q, p ^ u * s + m, hq, by omega, by ring⟩

/-- in `p^u t + q m` with `t ≥ 1`, if `q` divides the sum then `t` is a positive multiple of `q` -/
theorem exists_mul_of_dvd (hpq : Nat.Coprime p q) {u t m : ℕ} (ht : 1 ≤ t)
    (hd : q ∣ p ^ u * t + q * m) : ∃ s, 1 ≤ s ∧ t = q * s := by
  have h1 : q ∣ p ^ u * t := (Nat.dvd_add_left (dvd_mul_right q m)).1 hd
  have h2 : q ∣ t := (Nat.Coprime.dvd_mul_left (Nat.Coprime.pow_left u hpq).symm).1 h1
  obtain ⟨s, rfl⟩ := h2
  refine ⟨s, ?_, rfl⟩
  rcases Nat.eq_zero_or_pos s with h | h
  · rw [h, mul_zero] at ht
    omega
  · exact h

/-- (A4) an element of `S_u` that is a multiple of `q` is in `Q_u ∪ S_u⁺`, and is at least `q p^u` -/
theorem InS.of_dvd (hpq : Nat.Coprime p q) {u x : ℕ} (hx : InS p q u x) (hd : q ∣ x) :
    (InQ p q u x ∨ InSplus p q u x) ∧ q * p ^ u ≤ x := by
  obtain ⟨t, m, ht, rfl⟩ := hx
  obtain ⟨s, hs, rfl⟩ := exists_mul_of_dvd hpq ht hd
  have hle : q * p ^ u ≤ p ^ u * (q * s) :=
    calc q * p ^ u = p ^ u * (q * 1) := by ring
      _ ≤ p ^ u * (q * s) := Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ hs)
  refine ⟨?_, le_trans hle (Nat.le_add_right _ _)⟩
  rcases Nat.eq_zero_or_pos m with hm | hm
  · left
    subst hm
    exact ⟨s, hs, by ring⟩
  · right
    exact ⟨q * s, m, ht, hm, rfl⟩

/-- (A5) an element of `S_u⁺` that is a multiple of `q` is at least `q p^u + q` -/
theorem InSplus.le_of_dvd (hpq : Nat.Coprime p q) {u x : ℕ} (hx : InSplus p q u x) (hd : q ∣ x) :
    q * p ^ u + q ≤ x := by
  obtain ⟨t, m, ht, hm, rfl⟩ := hx
  obtain ⟨s, hs, rfl⟩ := exists_mul_of_dvd hpq ht hd
  have hle : q * p ^ u ≤ p ^ u * (q * s) :=
    calc q * p ^ u = p ^ u * (q * 1) := by ring
      _ ≤ p ^ u * (q * s) := Nat.mul_le_mul_left _ (Nat.mul_le_mul_left _ hs)
  have hle2 : q ≤ q * m := Nat.le_mul_of_pos_right _ hm
  omega

/-- two multiples of `d`, one larger than the other, differ by at least `d` -/
theorem add_le_of_dvd_of_lt {d a x : ℕ} (h1 : d ∣ a) (h2 : d ∣ x) (h3 : a < x) : a + d ≤ x := by
  obtain ⟨k, rfl⟩ := h1
  obtain ⟨l, rfl⟩ := h2
  have hkl : k < l := Nat.lt_of_mul_lt_mul_left h3
  calc d * k + d = d * (k + 1) := by ring
    _ ≤ d * l := Nat.mul_le_mul_left d hkl

/-- a sum of terms each in `S_u` or in `qZ_{≥0}` is in `S_u` or in `qZ_{≥0}` -/
theorem sum_InS_or_dvd {ι : Type*} (s : Finset ι) (f : ι → ℕ) (u : ℕ)
    (h : ∀ c ∈ s, InS p q u (f c) ∨ q ∣ f c) :
    InS p q u (∑ c ∈ s, f c) ∨ q ∣ ∑ c ∈ s, f c := by
  classical
  induction s using Finset.induction_on with
  | empty => right; simp
  | insert a s ha ih =>
    rw [Finset.sum_insert ha]
    have ih' := ih (fun c hc => h c (Finset.mem_insert_of_mem hc))
    rcases h a (Finset.mem_insert_self a s) with h1 | h1
    · exact Or.inl (h1.add_or ih')
    · rcases ih' with h2 | h2
      · left
        rw [add_comm]
        exact h2.add_dvd h1
      · exact Or.inr (dvd_add h1 h2)

/-! ### Shifting a set of levels down by one -/

/-- the levels `≥ 2` of `S`, shifted down by one (the sets `E⁻`, `F⁻` of a contained pair) -/
def sh (S : Finset ℕ) : Finset ℕ := (S.filter (fun ℓ => 2 ≤ ℓ)).image (fun ℓ => ℓ - 1)

theorem mem_sh {S : Finset ℕ} {m : ℕ} : m ∈ sh S ↔ 1 ≤ m ∧ m + 1 ∈ S := by
  unfold sh
  simp only [Finset.mem_image, Finset.mem_filter]
  constructor
  · rintro ⟨ℓ, ⟨hℓ, h2⟩, rfl⟩
    have h : ℓ - 1 + 1 = ℓ := by omega
    exact ⟨by omega, by rw [h]; exact hℓ⟩
  · rintro ⟨h1, h⟩
    exact ⟨m + 1, ⟨h, by omega⟩, by omega⟩

theorem pred_mem_sh {S : Finset ℕ} {g : ℕ} (h2 : 2 ≤ g) (hg : g ∈ S) : g - 1 ∈ sh S := by
  have h : g - 1 + 1 = g := by omega
  exact mem_sh.2 ⟨by omega, by rw [h]; exact hg⟩

theorem sh_union (A B : Finset ℕ) : sh (A ∪ B) = sh A ∪ sh B := by
  ext m
  simp only [mem_sh, Finset.mem_union]
  tauto

theorem card_sh {S : Finset ℕ} (h0 : 0 ∉ S) :
    S.card = (sh S).card + (if 1 ∈ S then 1 else 0) := by
  apply card_of_erase_one
  ext ℓ
  simp only [Finset.mem_erase, Finset.mem_image, mem_sh]
  constructor
  · rintro ⟨h1, h⟩
    have hne : ℓ ≠ 0 := fun h' => h0 (h' ▸ h)
    have he : ℓ - 1 + 1 = ℓ := by omega
    exact ⟨ℓ - 1, ⟨by omega, by rw [he]; exact h⟩, he⟩
  · rintro ⟨m, ⟨h1, h⟩, rfl⟩
    exact ⟨by omega, h⟩

theorem card_sh_pos {S : Finset ℕ} (h0 : 0 ∉ S) (h1 : 1 ∈ S) : S.card = (sh S).card + 1 := by
  rw [card_sh h0, ite_eq_left h1]

theorem card_sh_neg {S : Finset ℕ} (h0 : 0 ∉ S) (h1 : 1 ∉ S) : S.card = (sh S).card := by
  rw [card_sh h0, ite_eq_right h1, add_zero]

theorem card_union_sh_pos {A B : Finset ℕ} (hA : 0 ∉ A) (hB : 0 ∉ B) (h1 : 1 ∈ A ∨ 1 ∈ B) :
    (A ∪ B).card = (sh A ∪ sh B).card + 1 := by
  rw [← sh_union]
  exact card_sh_pos (by simp [hA, hB]) (Finset.mem_union.2 h1)

theorem card_union_sh_neg {A B : Finset ℕ} (hA : 0 ∉ A) (hB : 0 ∉ B) (h1 : 1 ∉ A) (h1' : 1 ∉ B) :
    (A ∪ B).card = (sh A ∪ sh B).card := by
  rw [← sh_union]
  exact card_sh_neg (by simp [hA, hB]) (by simp [h1, h1'])

/-! ### Levels of a node and of its children -/

theorem not_E_zero {n : ℕ} (t : Tree p q n) : ¬ E t 0 := by
  cases t <;> simp [E]

theorem F_le (hp : 0 < p) {n : ℕ} (t : Tree p q n) {ℓ : ℕ} (h1 : 1 ≤ ℓ) (h : F t ℓ) : ℓ ≤ n := by
  obtain ⟨k, rfl⟩ : ∃ k, ℓ = k + 1 := ⟨ℓ - 1, by omega⟩
  exact F_range hp t k h

theorem E_child {n : ℕ} {ch : Fin p → Tree p q n} {m : ℕ} (hm : 1 ≤ m) (h : E (.node ch) (m + 1))
    (c : Fin p) : E (ch c) m := by
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
  exact (E_node_succ ch k).1 h c

theorem F_child {n : ℕ} {ch : Fin p → Tree p q n} {m : ℕ} (hm : 1 ≤ m) (h : F (.node ch) (m + 1))
    (c : Fin p) : F (ch c) m := by
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
  exact (F_node_succ ch k).1 h c

theorem exists_not_E_child {n : ℕ} {ch : Fin p → Tree p q n} {m : ℕ} (hm : 1 ≤ m)
    (h : ¬ E (.node ch) (m + 1)) : ∃ c, ¬ E (ch c) m := by
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
  by_contra hcon
  push Not at hcon
  exact h ((E_node_succ ch k).2 hcon)

theorem exists_not_F_child {n : ℕ} {ch : Fin p → Tree p q n} {m : ℕ} (hm : 1 ≤ m)
    (h : ¬ F (.node ch) (m + 1)) : ∃ c, ¬ F (ch c) m := by
  obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
  by_contra hcon
  push Not at hcon
  exact h ((F_node_succ ch k).2 hcon)

/-- (0) for `E`: the shifted set is contained in the pattern of every child -/
theorem E_sh {n : ℕ} {ch : Fin p → Tree p q n} {E' : Finset ℕ} (hE : ∀ ℓ ∈ E', E (.node ch) ℓ)
    (c : Fin p) : ∀ m ∈ sh E', E (ch c) m := fun _ hm =>
  E_child (mem_sh.1 hm).1 (hE _ (mem_sh.1 hm).2) c

/-- (0) for `F`: the shifted set is contained in the pattern of every child -/
theorem F_sh {n : ℕ} {ch : Fin p → Tree p q n} {F' : Finset ℕ}
    (hF : ∀ ℓ ∈ F', 1 ≤ ℓ ∧ F (.node ch) ℓ) (c : Fin p) : ∀ m ∈ sh F', 1 ≤ m ∧ F (ch c) m :=
  fun _ hm => ⟨(mem_sh.1 hm).1, F_child (mem_sh.1 hm).1 (hF _ (mem_sh.1 hm).2).2 c⟩

theorem zero_notMem_of_E {n : ℕ} {t : Tree p q n} {E' : Finset ℕ} (hE : ∀ ℓ ∈ E', E t ℓ) :
    0 ∉ E' := fun h => not_E_zero t (hE 0 h)

theorem zero_notMem_of_F {n : ℕ} {t : Tree p q n} {F' : Finset ℕ} (hF : ∀ ℓ ∈ F', 1 ≤ ℓ ∧ F t ℓ) :
    0 ∉ F' := fun h => by
  have := (hF 0 h).1
  omega

/-- a witness at a level `g ≥ 2` of a node (some class at that level has children of unequal totals)
sits in a child, at the child's level `g - 1`, and that child is not empty -/
theorem exists_witness_child (hp : 0 < p) {n : ℕ} {ch : Fin p → Tree p q n} {g : ℕ} (h2 : 2 ≤ g)
    (hF : F (.node ch) g) (hw : ¬ E (.node ch) g) :
    ∃ c, ¬ E (ch c) (g - 1) ∧ 0 < size (ch c) := by
  obtain ⟨γ, rfl⟩ : ∃ γ, g = γ + 2 := ⟨g - 2, by omega⟩
  have hgn : γ + 2 ≤ n + 1 := F_le hp _ (by omega) hF
  obtain ⟨c, hc⟩ := exists_not_E_child (m := γ + 1) (by omega) hw
  refine ⟨c, hc, ?_⟩
  by_contra hcon
  exact hc (E_of_empty (ch c) (γ + 1) (by omega) (by omega) (by omega))

/-! ### Lemma 2 for a contained set -/

theorem subset_eSet (hp : 0 < p) {n : ℕ} (t : Tree p q n) {E' : Finset ℕ}
    (hE : ∀ ℓ ∈ E', E t ℓ) : E' ⊆ eSet t := by
  intro ℓ hℓ
  have h := hE ℓ hℓ
  have hr := E_range hp t ℓ h
  exact (mem_eSet t ℓ).2 ⟨hr.1, hr.2, h⟩

/-- **Lemma 2**, first part: `p^|E'|` divides the size -/
theorem pow_card_dvd_size (hp : 0 < p) {n : ℕ} (t : Tree p q n) {E' : Finset ℕ}
    (hE : ∀ ℓ ∈ E', E t ℓ) : p ^ E'.card ∣ size t :=
  (pow_dvd_pow p (Finset.card_le_card (subset_eSet hp t hE))).trans (pow_e_dvd_size t)

/-- **Lemma 2**, second part: `q p^|E'|` divides the size of a balanced tree -/
theorem q_mul_pow_card_dvd_size (hp : 0 < p) (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n)
    {E' : Finset ℕ} (hE : ∀ ℓ ∈ E', E t ℓ) (h0 : F t 0) : q * p ^ E'.card ∣ size t :=
  Nat.Coprime.mul_dvd_of_dvd_of_dvd (Nat.Coprime.pow_left _ hpq).symm (q_dvd_size t h0)
    (pow_card_dvd_size hp t hE)

/-! ### Lemma 1: children of equal shapes -/

/-- **Lemma 1 (a).** If the children have equal shapes, the size of the node is `p` times the size of a
child of least size plus a multiple `q D` of `q`, and `D ≥ 1` unless the children have equal sizes. -/
theorem equal_shapes_decomp (hp : 0 < p) (hq : 0 < q) {n : ℕ} (ch : Fin p → Tree p q n)
    (hF : F (.node ch) 1) :
    ∃ c0 D, size (.node ch) = p * size (ch c0) + q * D ∧ (¬ E (.node ch) 1 → 1 ≤ D) := by
  rw [F_node_one] at hF
  obtain ⟨c0, -, hmin⟩ := Finset.exists_min_image Finset.univ (fun c => size (ch c))
    ⟨⟨0, hp⟩, Finset.mem_univ _⟩
  let j0 : Fin q := ⟨0, hq⟩
  have hrow : ∀ c, size (ch c) + q * lay (ch c0) j0 = size (ch c0) + q * lay (ch c) j0 := by
    intro c
    have h := Finset.sum_congr (s₁ := Finset.univ) rfl (fun j _ => hF c c0 j j0)
    simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      smul_eq_mul] at h
    unfold size
    omega
  have hd : ∀ c, size (ch c) = size (ch c0) + q * (lay (ch c) j0 - lay (ch c0) j0) := by
    intro c
    have h := hrow c
    have h1 := hmin c (Finset.mem_univ _)
    have h2 : lay (ch c0) j0 ≤ lay (ch c) j0 := by
      by_contra hcon
      push Not at hcon
      have := Nat.mul_lt_mul_of_pos_left hcon hq
      omega
    obtain ⟨α, hα⟩ : ∃ α, lay (ch c) j0 = lay (ch c0) j0 + α :=
      ⟨_, (Nat.add_sub_cancel' h2).symm⟩
    rw [hα, Nat.mul_add] at h
    rw [hα, Nat.add_sub_cancel_left]
    omega
  refine ⟨c0, ∑ c, (lay (ch c) j0 - lay (ch c0) j0), ?_, ?_⟩
  · rw [size_node, Finset.sum_congr rfl (fun c _ => hd c), Finset.sum_add_distrib,
      Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul, Finset.mul_sum]
  · intro hE
    by_contra hcon
    have hz : ∑ c, (lay (ch c) j0 - lay (ch c0) j0) = 0 := by omega
    apply hE
    intro c c'
    have h1 := (Finset.sum_eq_zero_iff.1 hz) c (Finset.mem_univ _)
    have h2 := (Finset.sum_eq_zero_iff.1 hz) c' (Finset.mem_univ _)
    rw [hd c, hd c', h1, h2]

/-- **Lemma 1 (b)**, the other half: if a balanced node has children of equal shapes, every child is
balanced -/
theorem F0_child_of_F1 (hp : 0 < p) {n : ℕ} {ch : Fin p → Tree p q n} (h0 : F (.node ch) 0)
    (hF : F (.node ch) 1) (c : Fin p) : F (ch c) 0 := by
  rw [F_zero] at h0 ⊢
  rw [F_node_one] at hF
  intro j j'
  have h := h0 j j'
  simp only [lay_node] at h
  have hs : ∑ c' : Fin p, (lay (ch c') j + lay (ch c) j')
      = ∑ c' : Fin p, (lay (ch c') j' + lay (ch c) j) :=
    Finset.sum_congr rfl (fun c' _ => hF c' c j j')
  simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    smul_eq_mul] at hs
  have h3 : p * lay (ch c) j' = p * lay (ch c) j := by omega
  exact (Nat.eq_of_mul_eq_mul_left hp h3).symm

/-- balanced children have equal shapes -/
theorem F1_of_children_F0 {n : ℕ} {ch : Fin p → Tree p q n} (h : ∀ c, F (ch c) 0) :
    F (.node ch) 1 := by
  rw [F_node_one]
  intro c c' j j'
  rw [(F_zero _).1 (h c) j j', (F_zero _).1 (h c') j' j]

/-- if a node and all its children but one are balanced, so is that one -/
theorem F0_of_others {n : ℕ} {ch : Fin p → Tree p q n} (h0 : F (.node ch) 0) (c : Fin p)
    (h : ∀ c', c' ≠ c → F (ch c') 0) : F (ch c) 0 := by
  rw [F_zero] at h0 ⊢
  intro j j'
  have h1 := h0 j j'
  simp only [lay_node] at h1
  have e1 : ∀ j, ∑ c', lay (ch c') j
      = lay (ch c) j + ∑ c' ∈ Finset.univ.erase c, lay (ch c') j := fun j =>
    (Finset.add_sum_erase Finset.univ (fun c' => lay (ch c') j) (Finset.mem_univ c)).symm
  rw [e1 j, e1 j'] at h1
  have h2 : ∑ c' ∈ Finset.univ.erase c, lay (ch c') j
      = ∑ c' ∈ Finset.univ.erase c, lay (ch c') j' :=
    Finset.sum_congr rfl (fun c' hc' => (F_zero _).1 (h c' (Finset.ne_of_mem_erase hc')) j j')
  omega

/-- for `p = 2`: a balanced node whose two children have unequal shapes has two unbalanced children -/
theorem unbalanced_children_of_two (hp2 : p = 2) {n : ℕ} {ch : Fin p → Tree p q n}
    (h0 : F (.node ch) 0) (h1 : ¬ F (.node ch) 1) (c : Fin p) : ¬ F (ch c) 0 := by
  intro hc
  apply h1
  apply F1_of_children_F0
  intro c'
  by_cases hcc : c' = c
  · rw [hcc]
    exact hc
  · apply F0_of_others h0 c'
    intro c'' hne
    have h3 : c'' = c := by
      apply Fin.ext
      have ha := c.isLt
      have hb := c'.isLt
      have hd := c''.isLt
      have h4 : (c' : ℕ) ≠ c := fun h => hcc (Fin.ext h)
      have h5 : (c'' : ℕ) ≠ c' := fun h => hne (Fin.ext h)
      omega
    rw [h3]
    exact hc

/-! ### The total of the other children -/

/-- the total of the children other than `c` -/
def rest {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p) : ℕ :=
  ∑ c' ∈ Finset.univ.erase c, size (ch c')

theorem size_node_eq_add_rest {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p) :
    size (.node ch) = size (ch c) + rest ch c := by
  rw [size_node]
  exact (Finset.add_sum_erase Finset.univ (fun c' => size (ch c')) (Finset.mem_univ c)).symm

/-- every child's total is in `S_u` (if unbalanced) or in `qZ_{≥0}` (if balanced) -/
theorem child_InS_or_dvd {n : ℕ} {ch : Fin p → Tree p q n} {u : ℕ}
    (ih : ∀ c, ¬ F (ch c) 0 → InS p q u (size (ch c))) (c : Fin p) :
    InS p q u (size (ch c)) ∨ q ∣ size (ch c) := by
  by_cases hc : F (ch c) 0
  · exact Or.inr (q_dvd_size _ hc)
  · exact Or.inl (ih c hc)

theorem rest_InS_or_dvd {n : ℕ} {ch : Fin p → Tree p q n} {u : ℕ}
    (ih : ∀ c, ¬ F (ch c) 0 → InS p q u (size (ch c))) (c : Fin p) :
    InS p q u (rest ch c) ∨ q ∣ rest ch c :=
  sum_InS_or_dvd _ _ u (fun c' _ => child_InS_or_dvd ih c')

/-- if some other child is unbalanced, the total of the other children is in `S_u` -/
theorem rest_InS {n : ℕ} {ch : Fin p → Tree p q n} {u : ℕ}
    (ih : ∀ c, ¬ F (ch c) 0 → InS p q u (size (ch c))) {c c1 : Fin p} (hne : c1 ≠ c)
    (hc1 : ¬ F (ch c1) 0) : InS p q u (rest ch c) := by
  unfold rest
  rw [← Finset.add_sum_erase (Finset.univ.erase c) (fun c' => size (ch c'))
    (Finset.mem_erase.2 ⟨hne, Finset.mem_univ c1⟩)]
  exact (ih c1 hc1).add_or (sum_InS_or_dvd _ _ u (fun c' _ => child_InS_or_dvd ih c'))

/-- a balanced child that is not empty, in an unbalanced node: the node's total is in `S_u⁺` -/
theorem balanced_child_Splus {n : ℕ} {ch : Fin p → Tree p q n} {u : ℕ}
    (ih : ∀ c, ¬ F (ch c) 0 → InS p q u (size (ch c))) (h0 : ¬ F (.node ch) 0) {c : Fin p}
    (hcb : F (ch c) 0) (hcpos : 0 < size (ch c)) : InSplus p q u (size (ch c) + rest ch c) := by
  obtain ⟨c1, hc1⟩ := not_F0_node h0
  have hne : c1 ≠ c := by
    rintro rfl
    exact hc1 hcb
  have hRS := rest_InS ih hne hc1
  obtain ⟨m, hm⟩ := q_dvd_size _ hcb
  have hmpos : 1 ≤ m := by
    rcases Nat.eq_zero_or_pos m with h | h
    · rw [h, mul_zero] at hm
      omega
    · exact h
  rw [hm, add_comm]
  exact hRS.add_mul_pos hmpos

/-! ### Lemma 3: the size of an unbalanced tree is in `S_u` -/

/-- **Lemma 3.** For an unbalanced tree and a pair `(E', F')` contained in its pattern, the size is in
`S_u`, `u = |E' ∪ F'|`. -/
theorem size_mem_S (hp : 2 ≤ p) (hq : 2 ≤ q) :
    ∀ {n : ℕ} (t : Tree p q n) (E' F' : Finset ℕ), ¬ F t 0 → (∀ ℓ ∈ E', E t ℓ) →
      (∀ ℓ ∈ F', 1 ≤ ℓ ∧ F t ℓ) → InS p q (E' ∪ F').card (size t)
  | _, .leaf f, E', F', h0, hE, hF => by
      have hp0 : 0 < p := by omega
      have hE0 : E' = ∅ := Finset.eq_empty_of_forall_notMem (fun ℓ hℓ => by
        have := E_range hp0 _ ℓ (hE ℓ hℓ)
        omega)
      have hF0 : F' = ∅ := Finset.eq_empty_of_forall_notMem (fun ℓ hℓ => by
        have := F_le hp0 _ (hF ℓ hℓ).1 (hF ℓ hℓ).2
        have := (hF ℓ hℓ).1
        omega)
      rw [hE0, hF0, Finset.union_empty, Finset.card_empty]
      exact InS.of_pos (size_pos_of_not_F0 _ h0)
  | _, .node ch, E', F', h0, hE, hF => by
      have hp0 : 0 < p := by omega
      have hq0 : 0 < q := by omega
      have hE0 := zero_notMem_of_E hE
      have hF0 := zero_notMem_of_F hF
      have ih : ∀ c, ¬ F (ch c) 0 → InS p q (sh E' ∪ sh F').card (size (ch c)) := fun c hc =>
        size_mem_S hp hq (ch c) (sh E') (sh F') hc (E_sh hE c) (F_sh hF c)
      by_cases h1F : 1 ∈ F'
      · -- level 1 in `F'`: equal shapes, the least child is unbalanced
        have hF1 : F (.node ch) 1 := (hF 1 h1F).2
        obtain ⟨c0, D, hsz, -⟩ := equal_shapes_decomp hp0 hq0 ch hF1
        rw [card_union_sh_pos hE0 hF0 (Or.inr h1F), hsz]
        exact (ih c0 (not_F0_child_of_F1 h0 hF1 c0)).mul_p.add_dvd (dvd_mul_right q D)
      · obtain ⟨c, hc⟩ := not_F0_node h0
        by_cases h1E : 1 ∈ E'
        · -- level 1 in `E'` and not in `F'`: one total, some child unbalanced
          have hE1 : E (.node ch) 1 := hE 1 h1E
          rw [card_union_sh_pos hE0 hF0 (Or.inl h1E), size_node_of_E1 hE1 c]
          exact (ih c hc).mul_p
        · -- level 1 in neither
          rw [card_union_sh_neg hE0 hF0 h1E h1F, size_node_eq_add_rest ch c]
          exact (ih c hc).add_or (rest_InS_or_dvd ih c)

/-! ### Lemma 4: with a witness at a level of `F'`, the size is in `S_u⁺ ∪ Q_u` -/

/-- **Lemma 4.** For an unbalanced tree, a pair `(E', F')` contained in its pattern and a witness at a
level `g ∈ F'`, the size is in `S_u⁺ ∪ Q_u`, `u = |E' ∪ F'|`. -/
theorem size_mem_Splus_or_Q (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) :
    ∀ {n : ℕ} (t : Tree p q n) (E' F' : Finset ℕ) (g : ℕ), ¬ F t 0 → (∀ ℓ ∈ E', E t ℓ) →
      (∀ ℓ ∈ F', 1 ≤ ℓ ∧ F t ℓ) → g ∈ F' → ¬ E t g →
      InSplus p q (E' ∪ F').card (size t) ∨ InQ p q (E' ∪ F').card (size t)
  | _, .leaf f, E', F', g, h0, hE, hF, hg, hw => by
      have := F_le (by omega) (Tree.leaf (p := p) f) (hF g hg).1 (hF g hg).2
      have := (hF g hg).1
      omega
  | _, .node ch, E', F', g, h0, hE, hF, hg, hw => by
      have hp0 : 0 < p := by omega
      have hq0 : 0 < q := by omega
      have hE0 := zero_notMem_of_E hE
      have hF0 := zero_notMem_of_F hF
      have ih : ∀ c, ¬ F (ch c) 0 → InS p q (sh E' ∪ sh F').card (size (ch c)) := fun c hc =>
        size_mem_S hp hq (ch c) (sh E') (sh F') hc (E_sh hE c) (F_sh hF c)
      obtain ⟨hg1, hFg⟩ := hF g hg
      by_cases h1F : 1 ∈ F'
      · -- level 1 in `F'`: every child is unbalanced
        have hF1 : F (.node ch) 1 := (hF 1 h1F).2
        have hunb := not_F0_child_of_F1 h0 hF1
        rw [card_union_sh_pos hE0 hF0 (Or.inr h1F)]
        by_cases hE1 : E (.node ch) 1
        · -- equal totals: the witness is deeper, in an unbalanced child
          have hne1 : g ≠ 1 := fun h => hw (by rw [h]; exact hE1)
          have h2 : 2 ≤ g := by omega
          obtain ⟨c, hc, -⟩ := exists_witness_child hp0 h2 hFg hw
          rw [size_node_of_E1 hE1 c]
          rcases size_mem_Splus_or_Q hp hq hpq (ch c) (sh E') (sh F') (g - 1) (hunb c)
            (E_sh hE c) (F_sh hF c) (pred_mem_sh h2 hg) hc with h | h
          · exact Or.inl (h.mul_p hp0)
          · exact Or.inr h.mul_p
        · -- unequal totals: a positive multiple of `q` is added
          obtain ⟨c0, D, hsz, hD⟩ := equal_shapes_decomp hp0 hq0 ch hF1
          rw [hsz]
          exact Or.inl ((ih c0 (hunb c0)).mul_p.add_mul_pos (hD hE1))
      · have hne1 : g ≠ 1 := fun h => h1F (by rw [← h]; exact hg)
        have h2 : 2 ≤ g := by omega
        obtain ⟨c, hc, hcpos⟩ := exists_witness_child hp0 h2 hFg hw
        have ih4 : ¬ F (ch c) 0 → InSplus p q (sh E' ∪ sh F').card (size (ch c)) ∨
            InQ p q (sh E' ∪ sh F').card (size (ch c)) := fun hcu =>
          size_mem_Splus_or_Q hp hq hpq (ch c) (sh E') (sh F') (g - 1) hcu (E_sh hE c)
            (F_sh hF c) (pred_mem_sh h2 hg) hc
        by_cases h1E : 1 ∈ E'
        · -- level 1 in `E'` and not in `F'`: one total `s`
          have hE1 : E (.node ch) 1 := hE 1 h1E
          rw [card_union_sh_pos hE0 hF0 (Or.inl h1E), size_node_of_E1 hE1 c]
          have hs : InSplus p q (sh E' ∪ sh F').card (size (ch c)) ∨
              InQ p q (sh E' ∪ sh F').card (size (ch c)) := by
            by_cases hcb : F (ch c) 0
            · obtain ⟨c1, hc1⟩ := not_F0_node h0
              have h3 := ih c1 hc1
              rw [hE1 c1 c] at h3
              exact (h3.of_dvd hpq (q_dvd_size _ hcb)).1.symm
            · exact ih4 hcb
          rcases hs with h | h
          · exact Or.inl (h.mul_p hp0)
          · exact Or.inr h.mul_p
        · -- level 1 in neither
          rw [card_union_sh_neg hE0 hF0 h1E h1F, size_node_eq_add_rest ch c]
          by_cases hcb : F (ch c) 0
          · exact Or.inl (balanced_child_Splus ih h0 hcb hcpos)
          · rcases ih4 hcb with h | h
            · exact Or.inl (h.add_or (rest_InS_or_dvd ih c))
            · rcases rest_InS_or_dvd ih c with h' | h'
              · exact Or.inl (h.add_S hp0 h')
              · obtain ⟨m, hm⟩ := h'
                rcases Nat.eq_zero_or_pos m with hz | hpos
                · right
                  rw [hm, hz, mul_zero, add_zero]
                  exact h
                · left
                  rw [hm]
                  exact h.add_mul_pos hq0 hpos

/-! ### Lemma 5: no level of `E' ∖ F'` before the witness, then the size is in `S_u⁺` -/

/-- **Lemma 5.** For an unbalanced tree, a pair `(E', F')` contained in its pattern, a witness at a level
`g ∈ F'`, and no level of `E' ∖ F'` before `g`, the size is in `S_u⁺`, `u = |E' ∪ F'|`. -/
theorem size_mem_Splus (hp : 2 ≤ p) (hq : 2 ≤ q) :
    ∀ {n : ℕ} (t : Tree p q n) (E' F' : Finset ℕ) (g : ℕ), ¬ F t 0 → (∀ ℓ ∈ E', E t ℓ) →
      (∀ ℓ ∈ F', 1 ≤ ℓ ∧ F t ℓ) → g ∈ F' → ¬ E t g → (∀ ℓ ∈ E', ℓ < g → ℓ ∈ F') →
      InSplus p q (E' ∪ F').card (size t)
  | _, .leaf f, E', F', g, h0, hE, hF, hg, hw, hno => by
      have := F_le (by omega) (Tree.leaf (p := p) f) (hF g hg).1 (hF g hg).2
      have := (hF g hg).1
      omega
  | _, .node ch, E', F', g, h0, hE, hF, hg, hw, hno => by
      have hp0 : 0 < p := by omega
      have hq0 : 0 < q := by omega
      have hE0 := zero_notMem_of_E hE
      have hF0 := zero_notMem_of_F hF
      have ih : ∀ c, ¬ F (ch c) 0 → InS p q (sh E' ∪ sh F').card (size (ch c)) := fun c hc =>
        size_mem_S hp hq (ch c) (sh E') (sh F') hc (E_sh hE c) (F_sh hF c)
      obtain ⟨hg1, hFg⟩ := hF g hg
      -- the shifted pair has no level of `E⁻ ∖ F⁻` before `g - 1`
      have hno' : ∀ m ∈ sh E', m < g - 1 → m ∈ sh F' := fun m hm hlt =>
        mem_sh.2 ⟨(mem_sh.1 hm).1, hno _ (mem_sh.1 hm).2 (by omega)⟩
      by_cases h1F : 1 ∈ F'
      · have hF1 : F (.node ch) 1 := (hF 1 h1F).2
        have hunb := not_F0_child_of_F1 h0 hF1
        rw [card_union_sh_pos hE0 hF0 (Or.inr h1F)]
        by_cases hE1 : E (.node ch) 1
        · have hne1 : g ≠ 1 := fun h => hw (by rw [h]; exact hE1)
          have h2 : 2 ≤ g := by omega
          obtain ⟨c, hc, -⟩ := exists_witness_child hp0 h2 hFg hw
          rw [size_node_of_E1 hE1 c]
          exact (size_mem_Splus hp hq (ch c) (sh E') (sh F') (g - 1) (hunb c) (E_sh hE c)
            (F_sh hF c) (pred_mem_sh h2 hg) hc hno').mul_p hp0
        · obtain ⟨c0, D, hsz, hD⟩ := equal_shapes_decomp hp0 hq0 ch hF1
          rw [hsz]
          exact (ih c0 (hunb c0)).mul_p.add_mul_pos (hD hE1)
      · have hne1 : g ≠ 1 := fun h => h1F (by rw [← h]; exact hg)
        have h2 : 2 ≤ g := by omega
        -- level 1 cannot be in `E'`: it would be a level of `E' ∖ F'` before `g`
        have h1E : 1 ∉ E' := fun h => h1F (hno 1 h (by omega))
        obtain ⟨c, hc, hcpos⟩ := exists_witness_child hp0 h2 hFg hw
        rw [card_union_sh_neg hE0 hF0 h1E h1F, size_node_eq_add_rest ch c]
        by_cases hcb : F (ch c) 0
        · exact balanced_child_Splus ih h0 hcb hcpos
        · exact (size_mem_Splus hp hq (ch c) (sh E') (sh F') (g - 1) hcb (E_sh hE c)
            (F_sh hF c) (pred_mem_sh h2 hg) hc hno').add_or (rest_InS_or_dvd ih c)

/-! ### Lemma 6 and Proposition 7 -/

/-- **Lemma 6.** A balanced node whose children do not all have equal shapes, with a pair `(E', F')`
contained in its pattern, has at least `q p^u` elements, `u = |E' ∪ F'|`. -/
theorem balanced_unequal_bound (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ}
    (ch : Fin p → Tree p q n) (E' F' : Finset ℕ) (h0 : F (.node ch) 0) (h1 : ¬ F (.node ch) 1)
    (hE : ∀ ℓ ∈ E', E (.node ch) ℓ) (hF : ∀ ℓ ∈ F', 1 ≤ ℓ ∧ F (.node ch) ℓ) :
    q * p ^ (E' ∪ F').card ≤ size (.node ch) := by
  have hE0 := zero_notMem_of_E hE
  have hF0 := zero_notMem_of_F hF
  have ih : ∀ c, ¬ F (ch c) 0 → InS p q (sh E' ∪ sh F').card (size (ch c)) := fun c hc =>
    size_mem_S hp hq (ch c) (sh E') (sh F') hc (E_sh hE c) (F_sh hF c)
  have h1F : 1 ∉ F' := fun h => h1 (hF 1 h).2
  obtain ⟨c1, hc1⟩ : ∃ c, ¬ F (ch c) 0 := by
    by_contra hcon
    push Not at hcon
    exact h1 (F1_of_children_F0 hcon)
  have hqd : q ∣ size (.node ch) := q_dvd_size _ h0
  by_cases h1E : 1 ∈ E'
  · have hE1 : E (.node ch) 1 := hE 1 h1E
    rw [size_node_of_E1 hE1 c1] at hqd
    have hqs : q ∣ size (ch c1) := (Nat.Coprime.dvd_mul_left hpq.symm).1 hqd
    have h3 := ((ih c1 hc1).of_dvd hpq hqs).2
    rw [card_union_sh_pos hE0 hF0 (Or.inl h1E), size_node_of_E1 hE1 c1]
    calc q * p ^ ((sh E' ∪ sh F').card + 1) = p * (q * p ^ (sh E' ∪ sh F').card) := by ring
      _ ≤ p * size (ch c1) := Nat.mul_le_mul_left p h3
  · rw [card_union_sh_neg hE0 hF0 h1E h1F]
    have hS : InS p q (sh E' ∪ sh F').card (size (.node ch)) := by
      rw [size_node_eq_add_rest ch c1]
      exact (ih c1 hc1).add_or (rest_InS_or_dvd ih c1)
    exact (hS.of_dvd hpq hqd).2

/-- **Proposition 7**, for a contained pair: a balanced tree with the levels `1..a0-1` in `F` and `a0`
not in `F`, a set `E'` of levels in `E` and a set `F'` of levels beyond `a0` in `F`, has at least
`q p^|E' ∪ F'|` elements. -/
theorem prop7_gen (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) :
    ∀ {n : ℕ} (t : Tree p q n) (a0 : ℕ) (E' F' : Finset ℕ), F t 0 →
      (∀ ℓ, 1 ≤ ℓ → ℓ < a0 → F t ℓ) → 1 ≤ a0 → a0 ≤ n → ¬ F t a0 →
      (∀ ℓ ∈ E', E t ℓ) → (∀ ℓ ∈ F', a0 < ℓ ∧ F t ℓ) → q * p ^ (E' ∪ F').card ≤ size t
  | _, .leaf f, a0, E', F', h0, hlow, ha1, han, hna, hE, hF => by omega
  | _, .node ch, a0, E', F', h0, hlow, ha1, han, hna, hE, hF => by
      have hp0 : 0 < p := by omega
      have hF' : ∀ ℓ ∈ F', 1 ≤ ℓ ∧ F (.node ch) ℓ := fun ℓ hℓ =>
        ⟨by have := (hF ℓ hℓ).1; omega, (hF ℓ hℓ).2⟩
      rcases Nat.lt_or_ge a0 2 with ha | ha
      · -- `a0 = 1`: the node itself is the class `P`
        have ha0 : a0 = 1 := by omega
        subst ha0
        exact balanced_unequal_bound hp hq hpq ch E' F' h0 hna hE hF'
      · -- `a0 ≥ 2`: every child is balanced; go into a child where level `a0 - 1` is not in `F`
        obtain ⟨a, rfl⟩ : ∃ a, a0 = a + 2 := ⟨a0 - 2, by omega⟩
        have hE0 := zero_notMem_of_E hE
        have hF0 := zero_notMem_of_F hF'
        have h1F : 1 ∉ F' := fun h => by have := (hF 1 h).1; omega
        have hF1 : F (.node ch) 1 := hlow 1 (le_refl 1) (by omega)
        have hbal := F0_child_of_F1 hp0 h0 hF1
        obtain ⟨c, hc⟩ := exists_not_F_child (m := a + 1) (by omega) hna
        have ih := prop7_gen hp hq hpq (ch c) (a + 1) (sh E') (sh F') (hbal c)
          (fun ℓ h1 h2 => F_child h1 (hlow (ℓ + 1) (by omega) (by omega)) c) (by omega)
          (by omega) hc (E_sh hE c)
          (fun m hm => ⟨by have := (hF _ (mem_sh.1 hm).2).1; omega, (F_sh hF' c m hm).2⟩)
        by_cases h1E : 1 ∈ E'
        · rw [card_union_sh_pos hE0 hF0 (Or.inl h1E), size_node_of_E1 (hE 1 h1E) c]
          calc q * p ^ ((sh E' ∪ sh F').card + 1) = p * (q * p ^ (sh E' ∪ sh F').card) := by ring
            _ ≤ p * size (ch c) := Nat.mul_le_mul_left p ih
        · rw [card_union_sh_neg hE0 hF0 h1E h1F]
          exact le_trans ih (size_child_le ch c)

/-! ### Theorem B, the case with the extra fibre -/

/-- **Theorem B, Step 2** (the class `P` is the node itself, `a0 = 1`): a balanced node whose children
have unequal shapes, a pair `(E', F')` contained in its pattern, a witness at a level `g ∈ F'`, and
either (α) `1 ∉ E'`, or (β) `p = 2` and no level of `E' ∖ F'` strictly between `1` and `g`. -/
theorem thmB_step2 (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ}
    (ch : Fin p → Tree p q n) (E' F' : Finset ℕ) (g : ℕ) (h0 : F (.node ch) 0)
    (h1 : ¬ F (.node ch) 1) (hE : ∀ ℓ ∈ E', E (.node ch) ℓ)
    (hF : ∀ ℓ ∈ F', 1 < ℓ ∧ F (.node ch) ℓ) (hg : g ∈ F') (hw : ¬ E (.node ch) g)
    (h34 : 1 ∉ E' ∨ (p = 2 ∧ ∀ b ∈ E', 1 < b → b < g → b ∈ F')) :
    q * p ^ (E' ∪ F').card + q * p ^ E'.card ≤ size (.node ch) := by
  have hp0 : 0 < p := by omega
  have hF' : ∀ ℓ ∈ F', 1 ≤ ℓ ∧ F (.node ch) ℓ := fun ℓ hℓ =>
    ⟨(hF ℓ hℓ).1.le, (hF ℓ hℓ).2⟩
  have hE0 := zero_notMem_of_E hE
  have hF0 := zero_notMem_of_F hF'
  have h1F : 1 ∉ F' := fun h => h1 (hF 1 h).2
  have ih : ∀ c, ¬ F (ch c) 0 → InS p q (sh E' ∪ sh F').card (size (ch c)) := fun c hc =>
    size_mem_S hp hq (ch c) (sh E') (sh F') hc (E_sh hE c) (F_sh hF' c)
  obtain ⟨hg1, hFg⟩ := hF g hg
  have h2 : 2 ≤ g := hg1
  -- the witness class lies in the child `c`, which is not empty
  obtain ⟨c, hc, hcpos⟩ := exists_witness_child hp0 h2 hFg hw
  have hgm : g - 1 ∈ sh F' := pred_mem_sh h2 hg
  have hqd : q ∣ size (.node ch) := q_dvd_size _ h0
  have hsub : (sh E').card ≤ (sh E' ∪ sh F').card := Finset.card_le_card Finset.subset_union_left
  have hdd : q * p ^ (sh E').card ∣ q * p ^ (sh E' ∪ sh F').card :=
    Nat.mul_dvd_mul_left q (pow_dvd_pow p hsub)
  by_cases h1E : 1 ∈ E'
  · -- case (β)
    obtain ⟨hp2, hb⟩ : p = 2 ∧ ∀ b ∈ E', 1 < b → b < g → b ∈ F' := by
      rcases h34 with h | h
      · exact absurd h1E h
      · exact h
    have hE1 : E (.node ch) 1 := hE 1 h1E
    have hunb := unbalanced_children_of_two hp2 h0 h1
    have h5 := size_mem_Splus hp hq (ch c) (sh E') (sh F') (g - 1) (hunb c) (E_sh hE c)
      (F_sh hF' c) hgm hc (fun m hm hlt =>
        mem_sh.2 ⟨(mem_sh.1 hm).1, hb _ (mem_sh.1 hm).2 (by have := (mem_sh.1 hm).1; omega)
          (by omega)⟩)
    have hsz := size_node_of_E1 hE1 c
    have hqs : q ∣ size (ch c) := by
      rw [hsz] at hqd
      exact (Nat.Coprime.dvd_mul_left hpq.symm).1 hqd
    have h5' := h5.le_of_dvd hpq hqs
    have hd : q * p ^ (sh E').card ∣ size (ch c) :=
      Nat.Coprime.mul_dvd_of_dvd_of_dvd (Nat.Coprime.pow_left _ hpq).symm hqs
        (pow_card_dvd_size hp0 (ch c) (E_sh hE c))
    have h6 := add_le_of_dvd_of_lt hdd hd (by omega)
    rw [card_union_sh_pos hE0 hF0 (Or.inl h1E), card_sh_pos hE0 h1E, hsz]
    calc q * p ^ ((sh E' ∪ sh F').card + 1) + q * p ^ ((sh E').card + 1)
        = p * (q * p ^ (sh E' ∪ sh F').card + q * p ^ (sh E').card) := by ring
      _ ≤ p * size (ch c) := Nat.mul_le_mul_left p h6
  · -- case (α)
    obtain ⟨c1, hc1⟩ : ∃ c, ¬ F (ch c) 0 := by
      by_contra hcon
      push Not at hcon
      exact h1 (F1_of_children_F0 hcon)
    have hdn : q * p ^ (sh E').card ∣ size (.node ch) := by
      have h := q_mul_pow_card_dvd_size hp0 hpq (.node ch) hE h0
      rwa [card_sh_neg hE0 h1E] at h
    rw [card_union_sh_neg hE0 hF0 h1E h1F, card_sh_neg hE0 h1E]
    by_cases hb : ∃ b, F (ch b) 0 ∧ 0 < size (ch b)
    · -- some child is balanced and not empty
      obtain ⟨b, hbb, hbpos⟩ := hb
      have hbd : q * p ^ (sh E').card ∣ size (ch b) :=
        q_mul_pow_card_dvd_size hp0 hpq (ch b) (E_sh hE b) hbb
      have hbge := Nat.le_of_dvd hbpos hbd
      have hne : c1 ≠ b := by
        rintro rfl
        exact hc1 hbb
      have hRS := rest_InS ih hne hc1
      have hsz := size_node_eq_add_rest ch b
      have hqR : q ∣ rest ch b := by
        rw [hsz] at hqd
        exact (Nat.dvd_add_right (q_dvd_size _ hbb)).1 hqd
      have h3 := (hRS.of_dvd hpq hqR).2
      omega
    · -- every child that is not empty is unbalanced
      push Not at hb
      have hcu : ¬ F (ch c) 0 := fun h => by
        have := hb c h
        omega
      have h4 := size_mem_Splus_or_Q hp hq hpq (ch c) (sh E') (sh F') (g - 1) hcu (E_sh hE c)
        (F_sh hF' c) hgm hc
      obtain ⟨c2, hne2, hc2⟩ : ∃ c2, c2 ≠ c ∧ ¬ F (ch c2) 0 := by
        by_contra hcon
        push Not at hcon
        exact hcu (F0_of_others h0 c hcon)
      have hRS := rest_InS ih hne2 hc2
      have hsz := size_node_eq_add_rest ch c
      have hgt : q * p ^ (sh E' ∪ sh F').card < size (.node ch) := by
        rcases h4 with h | h
        · have hqd' : q ∣ size (ch c) + rest ch c := by
            rw [← hsz]
            exact hqd
          have h3 := (h.add hRS).le_of_dvd hpq hqd'
          omega
        · have h3 := h.le
          have h3' := hRS.pos hp0
          omega
      exact add_le_of_dvd_of_lt hdd hdn hgt

/-- **Theorem B (x = 1)**, for a contained pair, by descent through the levels `1..a0-1`. -/
theorem thmB_gen (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) :
    ∀ {n : ℕ} (t : Tree p q n) (a0 : ℕ) (E' F' : Finset ℕ) (g : ℕ), F t 0 →
      (∀ ℓ, 1 ≤ ℓ → ℓ < a0 → F t ℓ) → 1 ≤ a0 → a0 ≤ n → ¬ F t a0 →
      (∀ ℓ ∈ E', a0 ≤ ℓ ∧ E t ℓ) → (∀ ℓ ∈ F', a0 < ℓ ∧ F t ℓ) → g ∈ F' → ¬ E t g →
      (a0 ∉ E' ∨ (p = 2 ∧ ∀ b ∈ E', a0 < b → b < g → b ∈ F')) →
      q * p ^ (E' ∪ F').card + q * p ^ E'.card ≤ size t
  | _, .leaf f, a0, E', F', g, h0, hlow, ha1, han, hna, hE, hF, hg, hw, h34 => by omega
  | _, .node ch, a0, E', F', g, h0, hlow, ha1, han, hna, hE, hF, hg, hw, h34 => by
      have hp0 : 0 < p := by omega
      have hE'' : ∀ ℓ ∈ E', E (.node ch) ℓ := fun ℓ hℓ => (hE ℓ hℓ).2
      have hF'' : ∀ ℓ ∈ F', 1 ≤ ℓ ∧ F (.node ch) ℓ := fun ℓ hℓ =>
        ⟨by have := (hF ℓ hℓ).1; omega, (hF ℓ hℓ).2⟩
      rcases Nat.lt_or_ge a0 2 with ha | ha
      · -- `a0 = 1`: Step 2
        have ha0 : a0 = 1 := by omega
        subst ha0
        exact thmB_step2 hp hq hpq ch E' F' g h0 hna hE'' hF hg hw h34
      · obtain ⟨a, rfl⟩ : ∃ a, a0 = a + 2 := ⟨a0 - 2, by omega⟩
        have hE0 := zero_notMem_of_E hE''
        have hF0 := zero_notMem_of_F hF''
        have h1E : 1 ∉ E' := fun h => by have := (hE 1 h).1; omega
        have h1F : 1 ∉ F' := fun h => by have := (hF 1 h).1; omega
        have hF1 : F (.node ch) 1 := hlow 1 (le_refl 1) (by omega)
        have hbal := F0_child_of_F1 hp0 h0 hF1
        obtain ⟨c, hc⟩ := exists_not_F_child (m := a + 1) (by omega) hna
        have hlowc : ∀ ℓ, 1 ≤ ℓ → ℓ < a + 1 → F (ch c) ℓ := fun ℓ h1 h2 =>
          F_child h1 (hlow (ℓ + 1) (by omega) (by omega)) c
        have hFc : ∀ m ∈ sh F', a + 1 < m ∧ F (ch c) m := fun m hm =>
          ⟨by have := (hF _ (mem_sh.1 hm).2).1; omega, (F_sh hF'' c m hm).2⟩
        rw [card_union_sh_neg hE0 hF0 h1E h1F, card_sh_neg hE0 h1E]
        by_cases hex : ∃ c', c' ≠ c ∧ 0 < size (ch c')
        · -- Step 1: another child is not empty
          obtain ⟨c', hne, hpos⟩ := hex
          have h7 := prop7_gen hp hq hpq (ch c) (a + 1) (sh E') (sh F') (hbal c) hlowc
            (by omega) (by omega) hc (E_sh hE'' c) hFc
          have hd := q_mul_pow_card_dvd_size hp0 hpq (ch c') (E_sh hE'' c') (hbal c')
          have h8 := Nat.le_of_dvd hpos hd
          have h9 := size_two_children_le ch (Ne.symm hne)
          omega
        · -- the child `c` is the only one that is not empty: pass to it
          push Not at hex
          have hsz : size (.node ch) = size (ch c) := by
            have hr : rest ch c = 0 := by
              unfold rest
              exact Finset.sum_eq_zero (fun c' hc' => by
                have := hex c' (Finset.ne_of_mem_erase hc')
                omega)
            rw [size_node_eq_add_rest ch c, hr, add_zero]
          obtain ⟨hg1, hFg⟩ := hF g hg
          have h2 : 2 ≤ g := by omega
          obtain ⟨c'', hc'', hpos''⟩ := exists_witness_child hp0 h2 hFg hw
          have hcc : c'' = c := by
            by_contra hne
            have := hex c'' hne
            omega
          rw [hcc] at hc''
          rw [hsz]
          exact thmB_gen hp hq hpq (ch c) (a + 1) (sh E') (sh F') (g - 1) (hbal c) hlowc
            (by omega) (by omega) hc
            (fun m hm => ⟨by have := (hE _ (mem_sh.1 hm).2).1; omega, E_sh hE'' c m hm⟩) hFc
            (pred_mem_sh h2 hg) hc''
            (by
              rcases h34 with h | ⟨hp2, hb⟩
              · exact Or.inl (fun hm => h (mem_sh.1 hm).2)
              · exact Or.inr ⟨hp2, fun b hbm h1 h2' =>
                  mem_sh.2 ⟨(mem_sh.1 hbm).1, hb _ (mem_sh.1 hbm).2 (by omega) (by omega)⟩⟩)

/-! ### The two theorems -/

/-- **Proposition 7.** A balanced multiset in which `a0` is the first level missing from `F` has at least
`q · p^(e + k')` elements, `k'` the number of levels beyond `a0` that are in `F` and not in `E`. -/
theorem balanced_base (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n) (a0 : ℕ)
    (h0 : F t 0) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → F t ℓ) (ha1 : 1 ≤ a0) (han : a0 ≤ n) (hna : ¬ F t a0) :
    q * p ^ (e t + (gBeyond t a0).card) ≤ size t := by
  have hE : ∀ ℓ ∈ eSet t, E t ℓ := fun ℓ hℓ => ((mem_eSet t ℓ).1 hℓ).2.2
  have hG : ∀ ℓ ∈ gBeyond t a0, a0 < ℓ ∧ F t ℓ := fun ℓ hℓ =>
    ⟨((mem_gBeyond t a0 ℓ).1 hℓ).2, ((mem_fSet t ℓ).1 ((mem_gBeyond t a0 ℓ).1 hℓ).1.1).2.2⟩
  have hdisj : Disjoint (eSet t) (gBeyond t a0) := by
    rw [Finset.disjoint_left]
    intro ℓ h1 h2
    exact ((mem_gBeyond t a0 ℓ).1 h2).1.2 h1
  have h := prop7_gen hp hq hpq t a0 (eSet t) (gBeyond t a0) h0 hlow ha1 han hna hE hG
  rw [Finset.card_union_of_disjoint hdisj] at h
  exact h

/-- **Theorem B, the case with the extra fibre.** If moreover some level beyond `a0` is in `F` and not in `E`,
no level before `a0` is in `E`, and either `a0` is not in `E`, or `p = 2` and every level of `E` strictly between
`a0` and the first level of `gBeyond` is in `F`, then there are at least `q · p^e · (p^k' + 1)` elements. -/
theorem balanced_plus (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n) (a0 : ℕ)
    (h0 : F t 0) (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → F t ℓ) (ha1 : 1 ≤ a0) (han : a0 ≤ n) (hna : ¬ F t a0)
    (hk : (gBeyond t a0).Nonempty)
    (h2 : ∀ ℓ, ℓ < a0 → ¬ E t ℓ)
    (h34 : ¬ E t a0 ∨ (p = 2 ∧ ∀ b, a0 < b → (∀ g ∈ gBeyond t a0, b < g) → E t b → F t b)) :
    q * p ^ e t * (p ^ (gBeyond t a0).card + 1) ≤ size t := by
  -- the first level of `gBeyond`
  obtain ⟨g, hgmem, hgmin⟩ : ∃ g ∈ gBeyond t a0, ∀ g' ∈ gBeyond t a0, g ≤ g' :=
    ⟨(gBeyond t a0).min' hk, Finset.min'_mem _ hk, fun g' hg' => Finset.min'_le _ g' hg'⟩
  have hg' := (mem_gBeyond t a0 g).1 hgmem
  obtain ⟨hg1, hgn, hFg⟩ := (mem_fSet t g).1 hg'.1.1
  have hEg : ¬ E t g := fun h => hg'.1.2 ((mem_eSet t g).2 ⟨hg1, hgn, h⟩)
  -- the pair: all of `E`, and the levels of `F` beyond `a0`
  obtain ⟨F', hF'def⟩ : ∃ F' : Finset ℕ, F' = (fSet t).filter (fun ℓ => a0 < ℓ) := ⟨_, rfl⟩
  have hmemF' : ∀ ℓ, ℓ ∈ F' ↔ ℓ ∈ fSet t ∧ a0 < ℓ := fun ℓ => by
    rw [hF'def, Finset.mem_filter]
  have hE : ∀ ℓ ∈ eSet t, a0 ≤ ℓ ∧ E t ℓ := fun ℓ hℓ => by
    have hEl := ((mem_eSet t ℓ).1 hℓ).2.2
    refine ⟨?_, hEl⟩
    by_contra hlt
    exact h2 ℓ (by omega) hEl
  have hF : ∀ ℓ ∈ F', a0 < ℓ ∧ F t ℓ := fun ℓ hℓ =>
    ⟨((hmemF' ℓ).1 hℓ).2, ((mem_fSet t ℓ).1 ((hmemF' ℓ).1 hℓ).1).2.2⟩
  have hgF : g ∈ F' := (hmemF' g).2 ⟨hg'.1.1, hg'.2⟩
  have hcase : a0 ∉ eSet t ∨ (p = 2 ∧ ∀ b ∈ eSet t, a0 < b → b < g → b ∈ F') := by
    rcases h34 with h | ⟨hp2, hb⟩
    · exact Or.inl (fun hm => h ((mem_eSet t a0).1 hm).2.2)
    · refine Or.inr ⟨hp2, fun b hbm hab hbg => ?_⟩
      have hbE := (mem_eSet t b).1 hbm
      have hFb := hb b hab (fun g' hg' => lt_of_lt_of_le hbg (hgmin g' hg')) hbE.2.2
      exact (hmemF' b).2 ⟨(mem_fSet t b).2 ⟨hbE.1, hbE.2.1, hFb⟩, hab⟩
  have h := thmB_gen hp hq hpq t a0 (eSet t) F' g h0 hlow ha1 han hna hE hF hgF hEg hcase
  have hsd : F' \ eSet t = gBeyond t a0 := by
    ext ℓ
    rw [Finset.mem_sdiff, hmemF', mem_gBeyond]
    tauto
  have hcard : (eSet t ∪ F').card = (eSet t).card + (gBeyond t a0).card := by
    rw [← card_add_card_sdiff, hsd]
  rw [hcard] at h
  calc q * p ^ e t * (p ^ (gBeyond t a0).card + 1)
      = q * p ^ ((eSet t).card + (gBeyond t a0).card) + q * p ^ (eSet t).card := by
        unfold e
        ring
    _ ≤ size t := h

end Pnq
