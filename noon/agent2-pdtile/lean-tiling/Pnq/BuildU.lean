/-
The construction for the half with `Φ_q ∤ A`: for every pattern a tree with exactly that pattern and the
least size.  (Statement fixed by agent3 / Yonder, 26 November 2026.)
-/
import Pnq.Rule

open Finset

namespace Pnq

variable {p q : ℕ}

namespace BuildU

/-!
The proof of `exists_unbalanced` (everything in this namespace is auxiliary).

The multiset is `A₁`, plus `A₂` if `Fs ⊄ Es`.  `A₁`: the digits are free at the levels of `Es ∪ Fs` and `0`
elsewhere, and the element sits in layer `1` if every digit at a level of `Es ∖ Fs` is nonzero, in layer `0`
otherwise.  `A₂`: the digits are free at the levels of `Es` and `0` elsewhere, one element in every layer.
(When `Es ∖ Fs` is empty this puts the whole of `A₁` in layer `1`, where the note puts it in layer `0`; the
two differ by a renaming of the layers.)

`T Es Fs k d b f` is the subtree below a class of depth `d`, with `k` levels remaining; the multiset is
`T Es Fs n 0 true f` with `f = true` iff `Fs ⊄ Es`.  What is proved about it, each by induction on `k`:
`size_T` (the size), `lay_T_shift` (the part `A₂` adds a constant vector), `not_F0_T` (no subtree is
balanced), `E_T`, `F_T` (the levels of `Es`, `Fs` hold in every subtree), `not_E_T` (a level outside `Es`
fails `E` in the subtrees that have `A₂` if the level is in `Fs`), `not_F_T` (a level outside `Fs` fails `F`
in the subtrees whose flag `b` is up if the level is in `Es`).
-/

/-! ### The empty tree -/

/-- the empty tree of depth `k` -/
def emp : (k : ℕ) → Tree p q k
  | 0 => .leaf fun _ => 0
  | k + 1 => .node fun _ => emp k

theorem lay_emp : ∀ (k : ℕ) (j : Fin q), lay (emp k : Tree p q k) j = 0
  | 0, _ => rfl
  | k + 1, j => by
      simp only [emp, lay_node]
      exact Finset.sum_eq_zero (fun c _ => lay_emp k j)

theorem size_emp (k : ℕ) : size (emp k : Tree p q k) = 0 := by
  unfold size
  exact Finset.sum_eq_zero (fun j _ => lay_emp k j)

/-! ### Counting the levels of a set among `d + 1, …, d + k` -/

/-- the number of levels of `S` among `d + 1, …, d + k` -/
def cnt (S : Finset ℕ) : ℕ → ℕ → ℕ
  | 0, _ => 0
  | k + 1, d => (if d + 1 ∈ S then 1 else 0) + cnt S k (d + 1)

theorem cnt_succ_pos (S : Finset ℕ) (k d : ℕ) (h : d + 1 ∈ S) : cnt S (k + 1) d = cnt S k (d + 1) + 1 := by
  rw [cnt, ite_eq_left h, Nat.add_comm]

theorem cnt_succ_neg (S : Finset ℕ) (k d : ℕ) (h : d + 1 ∉ S) : cnt S (k + 1) d = cnt S k (d + 1) := by
  rw [cnt, ite_eq_right h, Nat.zero_add]

theorem cnt_eq (S : Finset ℕ) : ∀ k d, cnt S k d = (S.filter (fun ℓ => d < ℓ ∧ ℓ ≤ d + k)).card := by
  intro k
  induction k with
  | zero =>
    intro d
    rw [cnt]
    symm
    rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
    intro ℓ _ h
    omega
  | succ k ih =>
    intro d
    by_cases h : d + 1 ∈ S
    · rw [cnt_succ_pos S k d h, ih (d + 1)]
      have hset : S.filter (fun ℓ => d < ℓ ∧ ℓ ≤ d + (k + 1)) =
          insert (d + 1) (S.filter (fun ℓ => d + 1 < ℓ ∧ ℓ ≤ d + 1 + k)) := by
        ext ℓ
        simp only [Finset.mem_filter, Finset.mem_insert]
        constructor
        · rintro ⟨h1, h2, h3⟩
          by_cases hl : ℓ = d + 1
          · exact Or.inl hl
          · exact Or.inr ⟨h1, by omega, by omega⟩
        · rintro (rfl | ⟨h1, h2, h3⟩)
          · exact ⟨h, by omega, by omega⟩
          · exact ⟨h1, by omega, by omega⟩
      rw [hset, Finset.card_insert_of_notMem]
      simp
    · rw [cnt_succ_neg S k d h, ih (d + 1)]
      congr 1
      apply Finset.filter_congr
      intro ℓ hℓ
      have : ℓ ≠ d + 1 := fun e => h (e ▸ hℓ)
      omega

theorem cnt_root (S : Finset ℕ) (n : ℕ) (h : S ⊆ Finset.Icc 1 n) : cnt S n 0 = S.card := by
  rw [cnt_eq]
  congr 1
  apply Finset.filter_true_of_mem
  intro ℓ hℓ
  have := Finset.mem_Icc.1 (h hℓ)
  omega

/-! ### Sums over the children and over the layers -/

/-- a sum over the children in which only child `0` contributes -/
theorem sum_fin_zero (hp : 0 < p) (X : Fin p → ℕ) (h : ∀ c : Fin p, c.val ≠ 0 → X c = 0) :
    ∑ c, X c = X ⟨0, hp⟩ := by
  apply Finset.sum_eq_single
  · intro c _ hc
    exact h c (fun h0 => hc (Fin.ext h0))
  · intro h
    exact absurd (Finset.mem_univ _) h

theorem le_sum_fin (X : Fin p → ℕ) (c : Fin p) : X c ≤ ∑ c, X c :=
  Finset.single_le_sum (fun _ _ => Nat.zero_le _) (Finset.mem_univ c)

theorem sum_layer_one (v : ℕ) (hv : v < q) : ∑ j : Fin q, (if j.val = v then 1 else 0) = 1 := by
  rw [Finset.sum_eq_single (⟨v, hv⟩ : Fin q)]
  · simp
  · intro j _ hj
    rw [ite_eq_right]
    intro h
    exact hj (Fin.ext h)
  · intro h
    exact absurd (Finset.mem_univ _) h

theorem lay_two_le {n : ℕ} (t : Tree p q n) {j j' : Fin q} (h : j ≠ j') : lay t j + lay t j' ≤ size t := by
  unfold size
  rw [← Finset.sum_pair (f := fun j => lay t j) h]
  exact Finset.sum_le_sum_of_subset (Finset.subset_univ _)

/-! ### The builder -/

/-- The subtree of the construction below a class of depth `d`, with `k` levels remaining (the levels
`d + 1, …, d + k`).  The flag `b` says that every digit so far at a level of `Es ∖ Fs` was nonzero; the flag
`f` says that the part `A₂` is present in this class.  The part `A₁` is always present.  At a leaf: one
element in layer `1` if `b`, in layer `0` if not; and one more in every layer if `f`.  At a node whose split
is the level `a = d + 1`: if `a ∈ Es ∩ Fs` all children keep `(b, f)`; if `a ∈ Es ∖ Fs` child `c` gets
`(b ∧ c ≠ 0, f)`; if `a ∈ Fs ∖ Es` child `c` gets `(b, f ∧ c = 0)`; if `a ∉ Es ∪ Fs` child `0` keeps `(b, f)`
and the other children are empty. -/
def T (Es Fs : Finset ℕ) : (k : ℕ) → ℕ → Bool → Bool → Tree p q k
  | 0, _, b, f => .leaf fun j =>
      (if j.val = (if b then 1 else 0) then 1 else 0) + (if f then 1 else 0)
  | k + 1, d, b, f => .node fun c =>
      if d + 1 ∈ Es then
        if d + 1 ∈ Fs then T Es Fs k (d + 1) b f
        else T Es Fs k (d + 1) (b && decide (c.val ≠ 0)) f
      else
        if d + 1 ∈ Fs then T Es Fs k (d + 1) b (f && decide (c.val = 0))
        else if c.val = 0 then T Es Fs k (d + 1) b f else emp k

/-- the children of `T Es Fs (k + 1) d b f` -/
def child (Es Fs : Finset ℕ) (k d : ℕ) (b f : Bool) (c : Fin p) : Tree p q k :=
  if d + 1 ∈ Es then
    if d + 1 ∈ Fs then T Es Fs k (d + 1) b f
    else T Es Fs k (d + 1) (b && decide (c.val ≠ 0)) f
  else
    if d + 1 ∈ Fs then T Es Fs k (d + 1) b (f && decide (c.val = 0))
    else if c.val = 0 then T Es Fs k (d + 1) b f else emp k

variable (Es Fs : Finset ℕ)

theorem T_zero (d : ℕ) (b f : Bool) :
    (T Es Fs 0 d b f : Tree p q 0) = .leaf fun j =>
      (if j.val = (if b then 1 else 0) then 1 else 0) + (if f then 1 else 0) := rfl

theorem T_succ (k d : ℕ) (b f : Bool) :
    (T Es Fs (k + 1) d b f : Tree p q (k + 1)) = .node (child Es Fs k d b f) := rfl

variable {Es Fs}

theorem child_EF {k d : ℕ} {b f : Bool} (hE : d + 1 ∈ Es) (hF : d + 1 ∈ Fs) (c : Fin p) :
    (child Es Fs k d b f c : Tree p q k) = T Es Fs k (d + 1) b f := by
  simp only [child, ite_eq_left hE, ite_eq_left hF]

theorem child_E {k d : ℕ} {b f : Bool} (hE : d + 1 ∈ Es) (hF : d + 1 ∉ Fs) (c : Fin p) :
    (child Es Fs k d b f c : Tree p q k) = T Es Fs k (d + 1) (b && decide (c.val ≠ 0)) f := by
  simp only [child, ite_eq_left hE, ite_eq_right hF]

theorem child_F {k d : ℕ} {b f : Bool} (hE : d + 1 ∉ Es) (hF : d + 1 ∈ Fs) (c : Fin p) :
    (child Es Fs k d b f c : Tree p q k) = T Es Fs k (d + 1) b (f && decide (c.val = 0)) := by
  simp only [child, ite_eq_right hE, ite_eq_left hF]

theorem child_N {k d : ℕ} {b f : Bool} (hE : d + 1 ∉ Es) (hF : d + 1 ∉ Fs) (c : Fin p) :
    (child Es Fs k d b f c : Tree p q k) = if c.val = 0 then T Es Fs k (d + 1) b f else emp k := by
  simp only [child, ite_eq_right hE, ite_eq_right hF]

variable (Es Fs)

/-- every child is a subtree of the construction or is empty -/
theorem child_cases (k d : ℕ) (b f : Bool) (c : Fin p) :
    (∃ b' f', (child Es Fs k d b f c : Tree p q k) = T Es Fs k (d + 1) b' f') ∨
      (child Es Fs k d b f c : Tree p q k) = emp k := by
  by_cases hE : d + 1 ∈ Es
  · by_cases hF : d + 1 ∈ Fs
    · exact Or.inl ⟨_, _, child_EF hE hF c⟩
    · exact Or.inl ⟨_, _, child_E hE hF c⟩
  · by_cases hF : d + 1 ∈ Fs
    · exact Or.inl ⟨_, _, child_F hE hF c⟩
    · rw [child_N hE hF]
      by_cases hc : c.val = 0
      · exact Or.inl ⟨_, _, ite_eq_left hc⟩
      · exact Or.inr (ite_eq_right hc)

/-- child `0` keeps the flag `f` -/
theorem child_zero (hp : 0 < p) (k d : ℕ) (b f : Bool) :
    ∃ b', (child Es Fs k d b f ⟨0, hp⟩ : Tree p q k) = T Es Fs k (d + 1) b' f := by
  by_cases hE : d + 1 ∈ Es
  · by_cases hF : d + 1 ∈ Fs
    · exact ⟨_, child_EF hE hF _⟩
    · exact ⟨_, child_E hE hF _⟩
  · by_cases hF : d + 1 ∈ Fs
    · refine ⟨b, ?_⟩
      rw [child_F hE hF]
      simp
    · refine ⟨b, ?_⟩
      rw [child_N hE hF]
      simp

/-- some child keeps both flags -/
theorem child_keep (hp : 2 ≤ p) (k d : ℕ) (b f : Bool) :
    ∃ c, (child Es Fs k d b f c : Tree p q k) = T Es Fs k (d + 1) b f := by
  by_cases hE : d + 1 ∈ Es
  · by_cases hF : d + 1 ∈ Fs
    · exact ⟨⟨0, by omega⟩, child_EF hE hF _⟩
    · refine ⟨⟨1, hp⟩, ?_⟩
      rw [child_E hE hF]
      simp
  · by_cases hF : d + 1 ∈ Fs
    · refine ⟨⟨0, by omega⟩, ?_⟩
      rw [child_F hE hF]
      simp
    · refine ⟨⟨0, by omega⟩, ?_⟩
      rw [child_N hE hF]
      simp

/-! ### Sizes and layer vectors -/

/-- the size of a subtree: its part `A₁` has `p ^ (number of levels of Es ∪ Fs)` elements, its part `A₂`,
if present, `q * p ^ (number of levels of Es)` -/
theorem size_T (hp : 0 < p) (hq : 2 ≤ q) : ∀ (k d : ℕ) (b f : Bool),
    size (T Es Fs k d b f : Tree p q k) =
      p ^ cnt (Es ∪ Fs) k d + (if f then q * p ^ cnt Es k d else 0) := by
  intro k
  induction k with
  | zero =>
    intro d b f
    rw [T_zero]
    simp only [size, lay, cnt, pow_zero, mul_one]
    rw [Finset.sum_add_distrib, sum_layer_one _ (by cases b <;> simp <;> omega)]
    cases f <;> simp
  | succ k ih =>
    intro d b f
    rw [T_succ, size_node]
    by_cases hE : d + 1 ∈ Es
    · have hU : d + 1 ∈ Es ∪ Fs := Finset.mem_union_left _ hE
      rw [cnt_succ_pos _ k d hU, cnt_succ_pos _ k d hE]
      have hc : ∀ c : Fin p, size (child Es Fs k d b f c : Tree p q k) =
          p ^ cnt (Es ∪ Fs) k (d + 1) + (if f then q * p ^ cnt Es k (d + 1) else 0) := by
        intro c
        by_cases hF : d + 1 ∈ Fs
        · rw [child_EF hE hF, ih]
        · rw [child_E hE hF, ih]
      rw [Finset.sum_congr rfl (fun c _ => hc c), Finset.sum_const, Finset.card_univ, Fintype.card_fin,
        smul_eq_mul]
      cases f
      · simp only [Bool.false_eq_true, ite_false, Nat.add_zero]
        ring
      · simp only [ite_true]
        ring
    · rw [cnt_succ_neg _ k d hE]
      by_cases hF : d + 1 ∈ Fs
      · have hU : d + 1 ∈ Es ∪ Fs := Finset.mem_union_right _ hF
        rw [cnt_succ_pos _ k d hU]
        have hc : ∀ c : Fin p, size (child Es Fs k d b f c : Tree p q k) =
            p ^ cnt (Es ∪ Fs) k (d + 1) +
              (if c.val = 0 then (if f then q * p ^ cnt Es k (d + 1) else 0) else 0) := by
          intro c
          rw [child_F hE hF, ih]
          by_cases h0 : c.val = 0 <;> simp [h0]
        rw [Finset.sum_congr rfl (fun c _ => hc c), Finset.sum_add_distrib, Finset.sum_const,
          Finset.card_univ, Fintype.card_fin, smul_eq_mul, sum_fin_zero hp _ (fun c h0 => ite_eq_right h0)]
        simp only [ite_true]
        ring
      · have hU : d + 1 ∉ Es ∪ Fs := by
          rw [Finset.mem_union]
          tauto
        rw [cnt_succ_neg _ k d hU, sum_fin_zero hp]
        · rw [child_N hE hF, ite_eq_left rfl, ih]
        · intro c h0
          rw [child_N hE hF, ite_eq_right h0, size_emp]

/-- the part `A₂` adds a constant to the layer vector -/
theorem lay_T_shift (hp : 0 < p) : ∀ (k d : ℕ) (b f : Bool) (j : Fin q),
    lay (T Es Fs k d b f : Tree p q k) j =
      lay (T Es Fs k d b false : Tree p q k) j + (if f then p ^ cnt Es k d else 0) := by
  intro k
  induction k with
  | zero =>
    intro d b f j
    rw [T_zero, T_zero]
    cases f <;> simp [lay, cnt]
  | succ k ih =>
    intro d b f j
    rw [T_succ, T_succ, lay_node, lay_node]
    by_cases hE : d + 1 ∈ Es
    · rw [cnt_succ_pos _ k d hE]
      have hc : ∀ c : Fin p, lay (child Es Fs k d b f c : Tree p q k) j =
          lay (child Es Fs k d b false c : Tree p q k) j + (if f then p ^ cnt Es k (d + 1) else 0) := by
        intro c
        by_cases hF : d + 1 ∈ Fs
        · rw [child_EF hE hF, child_EF hE hF, ih]
        · rw [child_E hE hF, child_E hE hF, ih]
      rw [Finset.sum_congr rfl (fun c _ => hc c), Finset.sum_add_distrib, Finset.sum_const,
        Finset.card_univ, Fintype.card_fin, smul_eq_mul]
      cases f
      · simp
      · simp only [ite_true]
        ring
    · rw [cnt_succ_neg _ k d hE]
      have hc : ∀ c : Fin p, lay (child Es Fs k d b f c : Tree p q k) j =
          lay (child Es Fs k d b false c : Tree p q k) j +
            (if c.val = 0 then (if f then p ^ cnt Es k (d + 1) else 0) else 0) := by
        intro c
        by_cases hF : d + 1 ∈ Fs
        · rw [child_F hE hF, child_F hE hF, ih (d + 1) b (f && decide (c.val = 0)) j]
          by_cases h0 : c.val = 0 <;> simp [h0]
        · rw [child_N hE hF, child_N hE hF]
          by_cases h0 : c.val = 0
          · rw [ite_eq_left h0, ite_eq_left h0, ite_eq_left h0, ih (d + 1) b f j]
          · rw [ite_eq_right h0, ite_eq_right h0, ite_eq_right h0]
            rfl
      rw [Finset.sum_congr rfl (fun c _ => hc c), Finset.sum_add_distrib,
        sum_fin_zero hp _ (fun c h0 => ite_eq_right h0)]
      simp

/-- with the flag `b` down and no `A₂`, everything is in layer `0` -/
theorem lay_T_false : ∀ (k d : ℕ) (j : Fin q), j.val ≠ 0 →
    lay (T Es Fs k d false false : Tree p q k) j = 0 := by
  intro k
  induction k with
  | zero =>
    intro d j hj
    rw [T_zero]
    simp [lay, hj]
  | succ k ih =>
    intro d j hj
    rw [T_succ, lay_node]
    apply Finset.sum_eq_zero
    intro c _
    by_cases hE : d + 1 ∈ Es
    · by_cases hF : d + 1 ∈ Fs
      · rw [child_EF hE hF]
        exact ih (d + 1) j hj
      · rw [child_E hE hF]
        exact ih (d + 1) j hj
    · by_cases hF : d + 1 ∈ Fs
      · rw [child_F hE hF]
        exact ih (d + 1) j hj
      · rw [child_N hE hF]
        by_cases h0 : c.val = 0
        · rw [ite_eq_left h0]
          exact ih (d + 1) j hj
        · rw [ite_eq_right h0]
          exact lay_emp k j

theorem lay_T_false_zero (hp : 0 < p) (hq : 2 ≤ q) (k d : ℕ) :
    lay (T Es Fs k d false false : Tree p q k) ⟨0, by omega⟩ = p ^ cnt (Es ∪ Fs) k d := by
  have h := size_T Es Fs hp hq k d false false
  simp only [Bool.false_eq_true, ite_false, Nat.add_zero] at h
  rw [← h]
  unfold size
  symm
  apply Finset.sum_eq_single
  · intro j _ hj
    exact lay_T_false Es Fs k d j (fun h0 => hj (Fin.ext h0))
  · intro h
    exact absurd (Finset.mem_univ _) h

/-- with the flag `b` up, layer `1` is reached -/
theorem lay_T_true_pos (hp : 2 ≤ p) (hq : 2 ≤ q) : ∀ (k d : ℕ) (f : Bool),
    0 < lay (T Es Fs k d true f : Tree p q k) ⟨1, hq⟩ := by
  intro k
  induction k with
  | zero =>
    intro d f
    rw [T_zero]
    simp [lay]
  | succ k ih =>
    intro d f
    rw [T_succ, lay_node]
    obtain ⟨c, hc⟩ := child_keep Es Fs hp k d true f
    refine lt_of_lt_of_le ?_ (le_sum_fin _ c)
    rw [hc]
    exact ih (d + 1) f

/-- the subtrees with the flag `b` down and up do not have equal shapes -/
theorem not_shape (hp : 2 ≤ p) (hq : 2 ≤ q) (k d : ℕ) (f : Bool) :
    lay (T Es Fs k d false f : Tree p q k) ⟨0, by omega⟩ + lay (T Es Fs k d true f : Tree p q k) ⟨1, hq⟩ ≠
      lay (T Es Fs k d false f : Tree p q k) ⟨1, hq⟩ + lay (T Es Fs k d true f : Tree p q k) ⟨0, by omega⟩ := by
  have hp0 : 0 < p := by omega
  rw [lay_T_shift Es Fs hp0 k d false f, lay_T_shift Es Fs hp0 k d true f,
    lay_T_shift Es Fs hp0 k d false f, lay_T_shift Es Fs hp0 k d true f]
  have h1 := lay_T_false Es Fs (p := p) k d (⟨1, hq⟩ : Fin q) (by simp)
  have h2 := lay_T_false_zero Es Fs hp0 hq k d
  have h3 := lay_T_true_pos Es Fs hp hq k d false
  have h4 := lay_two_le (T Es Fs k d true false : Tree p q k) (j := ⟨0, by omega⟩) (j' := ⟨1, hq⟩)
    (by intro h; simpa using congrArg Fin.val h)
  have h5 := size_T Es Fs hp0 hq k d true false
  simp only [Bool.false_eq_true, ite_false, Nat.add_zero] at h5
  omega

/-- no subtree is balanced: the part `A₁` has a power of `p` elements, the part `A₂` is constant -/
theorem not_F0_T (hp : 0 < p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (k d : ℕ) (b f : Bool) :
    ¬ F (T Es Fs k d b f : Tree p q k) 0 := by
  intro h
  have h1 := q_dvd_size _ h
  rw [size_T Es Fs hp hq] at h1
  have h2 : q ∣ p ^ cnt (Es ∪ Fs) k d := by
    cases f
    · simpa using h1
    · simp only [ite_true] at h1
      exact (Nat.dvd_add_left (dvd_mul_right q _)).1 h1
  have h3 : q = 1 := Nat.Coprime.eq_one_of_dvd (Nat.Coprime.pow_right _ hpq.symm) h2
  omega

/-! ### The pattern -/

/-- at a level of `Es` the children have equal sizes, in every subtree -/
theorem E_T (hp : 0 < p) (hq : 2 ≤ q) : ∀ (k d : ℕ) (b f : Bool) (ℓ a : ℕ), a = d + ℓ + 1 → a ∈ Es →
    ℓ + 1 ≤ k → E (T Es Fs k d b f : Tree p q k) (ℓ + 1) := by
  intro k
  induction k with
  | zero =>
    intro d b f ℓ a _ _ h
    omega
  | succ k ih =>
    intro d b f ℓ a ha hmem hle
    rw [T_succ]
    rcases ℓ with _ | ℓ
    · have hE : d + 1 ∈ Es := by
        subst ha
        simpa using hmem
      rw [E_node_one]
      intro c c'
      by_cases hF : d + 1 ∈ Fs
      · rw [child_EF hE hF, child_EF hE hF]
      · rw [child_E hE hF, child_E hE hF, size_T Es Fs hp hq, size_T Es Fs hp hq]
    · rw [E_node_succ]
      intro c
      rcases child_cases Es Fs k d b f c with ⟨b', f', h⟩ | h
      · rw [h]
        exact ih (d + 1) b' f' ℓ a (by omega) hmem (by omega)
      · rw [h]
        exact E_of_empty _ _ (size_emp k) (by omega) (by omega)

/-- at a level of `Fs` the children have equal shapes, in every subtree -/
theorem F_T (hp : 0 < p) : ∀ (k d : ℕ) (b f : Bool) (ℓ a : ℕ), a = d + ℓ + 1 → a ∈ Fs →
    ℓ + 1 ≤ k → F (T Es Fs k d b f : Tree p q k) (ℓ + 1) := by
  intro k
  induction k with
  | zero =>
    intro d b f ℓ a _ _ h
    omega
  | succ k ih =>
    intro d b f ℓ a ha hmem hle
    rw [T_succ]
    rcases ℓ with _ | ℓ
    · have hF : d + 1 ∈ Fs := by
        subst ha
        simpa using hmem
      rw [F_node_one]
      intro c c' j j'
      by_cases hE : d + 1 ∈ Es
      · rw [child_EF hE hF, child_EF hE hF]
        exact Nat.add_comm _ _
      · rw [child_F hE hF, child_F hE hF]
        have h1 := lay_T_shift Es Fs hp k (d + 1) b (f && decide (c.val = 0)) j
        have h2 := lay_T_shift Es Fs hp k (d + 1) b (f && decide (c.val = 0)) j'
        have h3 := lay_T_shift Es Fs hp k (d + 1) b (f && decide (c'.val = 0)) j
        have h4 := lay_T_shift Es Fs hp k (d + 1) b (f && decide (c'.val = 0)) j'
        omega
    · rw [F_node_succ]
      intro c
      rcases child_cases Es Fs k d b f c with ⟨b', f', h⟩ | h
      · rw [h]
        exact ih (d + 1) b' f' ℓ a (by omega) hmem (by omega)
      · rw [h]
        exact F_of_empty _ _ (size_emp k) (by omega)

/-- at a level outside `Es` the children's sizes are not equal, in the subtrees that have the part `A₂`
if the level is in `Fs` -/
theorem not_E_T (hp : 2 ≤ p) (hq : 2 ≤ q) : ∀ (k d : ℕ) (b f : Bool) (ℓ a : ℕ), a = d + ℓ + 1 → a ∉ Es →
    (a ∈ Fs → f = true) → ¬ E (T Es Fs k d b f : Tree p q k) (ℓ + 1) := by
  have hp0 : 0 < p := by omega
  intro k
  induction k with
  | zero =>
    intro d b f ℓ a _ _ _ h
    rw [T_zero] at h
    exact h
  | succ k ih =>
    intro d b f ℓ a ha hnE hFf h
    rw [T_succ] at h
    rcases ℓ with _ | ℓ
    · have hE : d + 1 ∉ Es := by
        subst ha
        simpa using hnE
      rw [E_node_one] at h
      have h01 := h ⟨0, hp0⟩ ⟨1, hp⟩
      by_cases hF : d + 1 ∈ Fs
      · have hf : f = true := hFf (by subst ha; simpa using hF)
        subst hf
        rw [child_F hE hF, child_F hE hF, size_T Es Fs hp0 hq, size_T Es Fs hp0 hq] at h01
        have hpos : 0 < q * p ^ cnt Es k (d + 1) := Nat.mul_pos (by omega) (Nat.pow_pos hp0)
        simp at h01
        omega
      · rw [child_N hE hF, child_N hE hF, ite_eq_left rfl, ite_eq_right (by simp), size_emp,
          size_T Es Fs hp0 hq] at h01
        have hpos : 0 < p ^ cnt (Es ∪ Fs) k (d + 1) := Nat.pow_pos hp0
        omega
    · rw [E_node_succ] at h
      obtain ⟨b', hb'⟩ := child_zero Es Fs hp0 k d b f
      have h0 := h ⟨0, hp0⟩
      rw [hb'] at h0
      exact ih (d + 1) b' f ℓ a (by omega) hnE hFf h0

/-- at a level outside `Fs` the children do not have equal shapes, in the subtrees that have the flag `b`
up if the level is in `Es` -/
theorem not_F_T (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) : ∀ (k d : ℕ) (b f : Bool) (ℓ a : ℕ),
    a = d + ℓ + 1 → a ∉ Fs → (a ∈ Es → b = true) → ¬ F (T Es Fs k d b f : Tree p q k) (ℓ + 1) := by
  have hp0 : 0 < p := by omega
  intro k
  induction k with
  | zero =>
    intro d b f ℓ a _ _ _ h
    rw [T_zero] at h
    exact h
  | succ k ih =>
    intro d b f ℓ a ha hnF hEb h
    rw [T_succ] at h
    rcases ℓ with _ | ℓ
    · have hF : d + 1 ∉ Fs := by
        subst ha
        simpa using hnF
      rw [F_node_one] at h
      by_cases hE : d + 1 ∈ Es
      · have hb : b = true := hEb (by subst ha; simpa using hE)
        subst hb
        have h01 := h ⟨0, hp0⟩ ⟨1, hp⟩ ⟨0, by omega⟩ ⟨1, hq⟩
        rw [child_E hE hF, child_E hE hF] at h01
        simp only [ne_eq, not_true_eq_false, decide_false, Bool.and_false, one_ne_zero,
          not_false_eq_true, decide_true, Bool.and_true] at h01
        exact not_shape Es Fs hp hq k (d + 1) f h01
      · apply not_F0_T Es Fs hp0 hq hpq k (d + 1) b f
        rw [F_zero]
        intro j j'
        have h01 := h ⟨0, hp0⟩ ⟨1, hp⟩ j j'
        rw [child_N hE hF, child_N hE hF, ite_eq_left rfl, ite_eq_right (by simp), lay_emp, lay_emp] at h01
        exact h01
    · rw [F_node_succ] at h
      obtain ⟨c, hc⟩ := child_keep Es Fs hp k d b f
      have h0 := h c
      rw [hc] at h0
      exact ih (d + 1) b f ℓ a (by omega) hnF hEb h0

end BuildU

/-- **The construction, `Φ_q ∤ A`.** For all sets `Es`, `Fs` of levels in `1..n` there is a tree (a multiset
on `Z_{pⁿ} × Z_q`) that is not balanced, whose levels of `E` are exactly `Es`, whose levels `≥ 1` of `F` are
exactly `Fs`, and which has `minU p q Es Fs` elements. -/
theorem exists_unbalanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) :
    ∃ t : Tree p q n, ¬ F t 0 ∧ eSet t = Es ∧ fSet t = Fs ∧ size t = minU p q Es Fs := by
  have hp0 : 0 < p := by omega
  obtain ⟨f, hf⟩ : ∃ f : Bool, f = true ↔ ¬ Fs ⊆ Es := ⟨decide (¬ Fs ⊆ Es), by simp⟩
  refine ⟨BuildU.T Es Fs n 0 true f, BuildU.not_F0_T Es Fs hp0 hq hpq n 0 true f, ?_, ?_, ?_⟩
  · ext ℓ
    rw [mem_eSet]
    constructor
    · rintro ⟨h1, h2, h3⟩
      by_contra hℓ
      obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
      refine BuildU.not_E_T Es Fs hp hq n 0 true f m (m + 1) (by omega) hℓ ?_ h3
      intro hmF
      by_contra hff
      have hsub : Fs ⊆ Es := by
        by_contra h
        exact hff (hf.2 h)
      exact hℓ (hsub hmF)
    · intro hℓ
      have hr := Finset.mem_Icc.1 (hE hℓ)
      obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
      exact ⟨hr.1, hr.2, BuildU.E_T Es Fs hp0 hq n 0 true f m (m + 1) (by omega) hℓ hr.2⟩
  · ext ℓ
    rw [mem_fSet]
    constructor
    · rintro ⟨h1, h2, h3⟩
      by_contra hℓ
      obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
      exact BuildU.not_F_T Es Fs hp hq hpq n 0 true f m (m + 1) (by omega) hℓ (fun _ => rfl) h3
    · intro hℓ
      have hr := Finset.mem_Icc.1 (hF hℓ)
      obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
      exact ⟨hr.1, hr.2, BuildU.F_T Es Fs hp0 n 0 true f m (m + 1) (by omega) hℓ hr.2⟩
  · rw [BuildU.size_T Es Fs hp0 hq, BuildU.cnt_root _ n (Finset.union_subset hE hF),
      BuildU.cnt_root _ n hE]
    unfold minU
    by_cases h : Fs ⊆ Es
    · have hf' : f = false := by
        cases f
        · rfl
        · exact absurd h (hf.1 rfl)
      rw [ite_eq_left h, hf', Finset.union_eq_left.2 h]
      simp
    · have hf' : f = true := hf.2 h
      rw [ite_eq_right h, hf', ← card_add_card_sdiff, pow_add]
      simp only [ite_true]
      ring

end Pnq
