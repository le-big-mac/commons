import Pnq.Tree

open Finset

namespace Pnq

variable {p q : ℕ}

open Classical in
/-- the levels `1..n` at which `F` holds (level 0 is left out) -/
noncomputable def fSet {n : ℕ} (t : Tree p q n) : Finset ℕ := (Finset.Icc 1 n).filter (fun ℓ => F t ℓ)

/-! ### The set of levels in `F`, and how the level sets of a node sit over those of its children -/

open Classical in
/-- the levels `1..n` at which every child satisfies `F` (the set `F⁻` of the note) -/
noncomputable def fMinus {n : ℕ} (ch : Fin p → Tree p q n) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => ∀ c, F (ch c) ℓ)

theorem mem_fSet {n : ℕ} (t : Tree p q n) (ℓ : ℕ) : ℓ ∈ fSet t ↔ 1 ≤ ℓ ∧ ℓ ≤ n ∧ F t ℓ := by
  simp [fSet, and_assoc]

theorem mem_fMinus {n : ℕ} (ch : Fin p → Tree p q n) (ℓ : ℕ) :
    ℓ ∈ fMinus ch ↔ 1 ≤ ℓ ∧ ℓ ≤ n ∧ ∀ c, F (ch c) ℓ := by
  simp [fMinus, and_assoc]

/-- (b) every child's `fSet` contains `F⁻` -/
theorem fMinus_subset {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p) : fMinus ch ⊆ fSet (ch c) := by
  intro ℓ h
  rw [mem_fMinus] at h
  exact (mem_fSet _ _).2 ⟨h.1, h.2.1, h.2.2 c⟩

/-- (a) the levels `≥ 2` of `fSet` of a node are `F⁻` shifted up by one -/
theorem fSet_erase_one {n : ℕ} (ch : Fin p → Tree p q n) :
    (fSet (.node ch)).erase 1 = (fMinus ch).image (· + 1) := by
  ext ℓ
  simp only [Finset.mem_erase, mem_fSet, Finset.mem_image, mem_fMinus]
  constructor
  · rintro ⟨h1, h2, h3, h4⟩
    obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 2 := ⟨ℓ - 2, by omega⟩
    exact ⟨m + 1, ⟨by omega, by omega, (F_node_succ ch m).1 h4⟩, rfl⟩
  · rintro ⟨m, ⟨h1, h2, h3⟩, rfl⟩
    obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
    exact ⟨by omega, by omega, by omega, (F_node_succ ch k).2 h3⟩

theorem succ_injective' : Function.Injective (fun m : ℕ => m + 1) := fun a b h => by simpa using h

/-- if `S` without the level 1 is `T` shifted up by one, then `|S|` is `|T|`, plus one if `1 ∈ S` -/
theorem card_of_erase_one {S T : Finset ℕ} (h : S.erase 1 = T.image (· + 1)) :
    S.card = T.card + (if 1 ∈ S then 1 else 0) := by
  have hc : (T.image (· + 1)).card = T.card := Finset.card_image_of_injective _ succ_injective'
  by_cases h1 : 1 ∈ S
  · rw [ite_eq_left h1, ← hc, ← h, Finset.card_erase_of_mem h1]
    have := Finset.card_pos.2 ⟨1, h1⟩
    omega
  · rw [ite_eq_right h1, ← hc, ← h, Finset.erase_eq_of_notMem h1]
    rfl

theorem union_erase_one {n : ℕ} (ch : Fin p → Tree p q n) :
    (eSet (.node ch) ∪ fSet (.node ch)).erase 1 = (eMinus ch ∪ fMinus ch).image (· + 1) := by
  rw [Finset.erase_union_distrib, eSet_erase_one, fSet_erase_one, Finset.image_union]

theorem sdiff_erase_one {n : ℕ} (ch : Fin p → Tree p q n) :
    (fSet (.node ch) \ eSet (.node ch)).erase 1 = (fMinus ch \ eMinus ch).image (· + 1) := by
  rw [Finset.erase_sdiff_distrib, eSet_erase_one, fSet_erase_one,
    Finset.image_sdiff _ _ succ_injective']

theorem one_mem_eSet_node {n : ℕ} (ch : Fin p → Tree p q n) :
    1 ∈ eSet (.node ch) ↔ E (.node ch) 1 := by
  rw [mem_eSet]
  exact ⟨fun h => h.2.2, fun h => ⟨le_refl 1, by omega, h⟩⟩

theorem one_mem_fSet_node {n : ℕ} (ch : Fin p → Tree p q n) :
    1 ∈ fSet (.node ch) ↔ F (.node ch) 1 := by
  rw [mem_fSet]
  exact ⟨fun h => h.2.2, fun h => ⟨le_refl 1, by omega, h⟩⟩

/-- `|E ∪ F|` of a node is at most `|E⁻ ∪ F⁻| + 1` -/
theorem card_union_node_le {n : ℕ} (ch : Fin p → Tree p q n) :
    (eSet (.node ch) ∪ fSet (.node ch)).card ≤ (eMinus ch ∪ fMinus ch).card + 1 := by
  rw [card_of_erase_one (union_erase_one ch)]
  split_ifs <;> omega

/-- `|E ∪ F|` of a node is `|E⁻ ∪ F⁻|` if neither `E` nor `F` holds at level 1 -/
theorem card_union_node_of_not {n : ℕ} (ch : Fin p → Tree p q n) (hE : ¬ E (.node ch) 1)
    (hF : ¬ F (.node ch) 1) :
    (eSet (.node ch) ∪ fSet (.node ch)).card = (eMinus ch ∪ fMinus ch).card := by
  have h1 : 1 ∉ eSet (.node ch) ∪ fSet (.node ch) := by
    rw [Finset.mem_union, one_mem_eSet_node, one_mem_fSet_node]
    tauto
  rw [card_of_erase_one (union_erase_one ch), ite_eq_right h1]
  rfl

theorem one_mem_sdiff_node {n : ℕ} (ch : Fin p → Tree p q n) :
    1 ∈ fSet (.node ch) \ eSet (.node ch) ↔ F (.node ch) 1 ∧ ¬ E (.node ch) 1 := by
  rw [Finset.mem_sdiff, one_mem_eSet_node, one_mem_fSet_node]

/-- `|F ∖ E|` of a node is `|F⁻ ∖ E⁻| + 1` if level 1 is in `F` and not in `E` -/
theorem card_sdiff_node_pos {n : ℕ} (ch : Fin p → Tree p q n) (hF : F (.node ch) 1)
    (hE : ¬ E (.node ch) 1) :
    (fSet (.node ch) \ eSet (.node ch)).card = (fMinus ch \ eMinus ch).card + 1 := by
  rw [card_of_erase_one (sdiff_erase_one ch), ite_eq_left ((one_mem_sdiff_node ch).2 ⟨hF, hE⟩)]

/-- `|F ∖ E|` of a node is `|F⁻ ∖ E⁻|` otherwise -/
theorem card_sdiff_node_neg {n : ℕ} (ch : Fin p → Tree p q n)
    (h : ¬ (F (.node ch) 1 ∧ ¬ E (.node ch) 1)) :
    (fSet (.node ch) \ eSet (.node ch)).card = (fMinus ch \ eMinus ch).card := by
  rw [card_of_erase_one (sdiff_erase_one ch),
    ite_eq_right (fun hm => h ((one_mem_sdiff_node ch).1 hm))]
  rfl

/-- `|A| + |B ∖ A| = |A ∪ B|` -/
theorem card_add_card_sdiff (A B : Finset ℕ) : A.card + (B \ A).card = (A ∪ B).card := by
  have h := Finset.card_sdiff_add_card B A
  rw [Finset.union_comm] at h
  omega

/-- (b) for every child, `E⁻ ∪ F⁻ ⊆ E(child) ∪ F(child)` -/
theorem union_subset_child {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p) :
    eMinus ch ∪ fMinus ch ⊆ eSet (ch c) ∪ fSet (ch c) :=
  Finset.union_subset_union (eMinus_subset ch c) (fMinus_subset ch c)

/-! ### Balanced and unbalanced children -/

/-- (d) an unbalanced tree is not empty -/
theorem size_pos_of_not_F0 {n : ℕ} (t : Tree p q n) (h0 : ¬ F t 0) : 0 < size t := by
  by_contra hcon
  exact h0 (F_of_empty t 0 (by omega) (Nat.zero_le _))

/-- (c) if the children's layer counts form an additive array and the node is unbalanced, then every
child is unbalanced -/
theorem not_F0_child_of_F1 {n : ℕ} {ch : Fin p → Tree p q n} (h0 : ¬ F (.node ch) 0)
    (hF : F (.node ch) 1) (c : Fin p) : ¬ F (ch c) 0 := by
  intro hc
  apply h0
  rw [F_zero] at hc ⊢
  rw [F_node_one] at hF
  intro j j'
  simp only [lay_node]
  refine Finset.sum_congr rfl (fun c' _ => ?_)
  have h := hF c c' j j'
  have h2 := hc j j'
  omega

/-- (e), in the form used: if the children's layer counts form an additive array, their sizes are not
all equal, every size is a multiple of `d` (coprime to `q`) and every size is at least `m`, then the
node has at least `p m + q d` elements.  (The sizes differ by multiples of `q`; a largest exceeds a
smallest by a positive multiple of `q d`.)  This is the arithmetic of `lemma3_base`. -/
theorem additive_bound (hq : 0 < q) {n : ℕ} (ch : Fin p → Tree p q n)
    (hF : F (.node ch) 1) (hE : ¬ E (.node ch) 1) (d m : ℕ) (hd : Nat.Coprime d q)
    (hdiv : ∀ c, d ∣ size (ch c)) (hm : ∀ c, m ≤ size (ch c)) :
    p * m + q * d ≤ size (.node ch) := by
  rw [F_node_one] at hF
  have hp : 0 < p := by
    rcases Nat.eq_zero_or_pos p with h | h
    · subst h
      exact absurd (fun c _ => Fin.elim0 c) hE
    · exact h
  -- a child of least size
  obtain ⟨c0, -, hmin⟩ := Finset.exists_min_image Finset.univ (fun c => size (ch c))
    ⟨⟨0, hp⟩, Finset.mem_univ _⟩
  let j0 : Fin q := ⟨0, hq⟩
  -- size (ch c) - size (ch c0) = q * (N c j0 - N c0 j0)
  have hrow : ∀ c, size (ch c) + q * lay (ch c0) j0 = size (ch c0) + q * lay (ch c) j0 := by
    intro c
    have h := Finset.sum_congr (s₁ := Finset.univ) rfl (fun j _ => hF c c0 j j0)
    simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      smul_eq_mul] at h
    unfold size
    omega
  -- some child is strictly larger
  obtain ⟨c1, hc1⟩ : ∃ c1, size (ch c0) < size (ch c1) := by
    by_contra hcon
    push Not at hcon
    apply hE
    intro c c'
    have h1 := hmin c (Finset.mem_univ _)
    have h2 := hmin c' (Finset.mem_univ _)
    have h3 := hcon c
    have h4 := hcon c'
    omega
  have hlt : lay (ch c0) j0 < lay (ch c1) j0 := by
    have h := hrow c1
    by_contra hcon
    push Not at hcon
    have := Nat.mul_le_mul_left q hcon
    omega
  obtain ⟨α, hα⟩ : ∃ α, lay (ch c1) j0 = lay (ch c0) j0 + α := ⟨_, (Nat.add_sub_cancel' hlt.le).symm⟩
  have hαpos : 0 < α := by omega
  have hc1eq : size (ch c1) = size (ch c0) + q * α := by
    have h := hrow c1
    rw [hα, Nat.mul_add] at h
    omega
  have hα_dvd : d ∣ α := by
    have h1 : d ∣ q * α := by
      have := hdiv c1
      rw [hc1eq] at this
      exact (Nat.dvd_add_right (hdiv c0)).1 this
    exact (Nat.Coprime.dvd_mul_left hd).1 h1
  have hα_ge : d ≤ α := Nat.le_of_dvd hαpos hα_dvd
  -- add up
  have hsum : p * size (ch c0) + q * α ≤ size (.node ch) := by
    rw [size_node]
    have hle : ∀ c ∈ (Finset.univ : Finset (Fin p)),
        size (ch c0) + (if c = c1 then q * α else 0) ≤ size (ch c) := by
      intro c _
      by_cases hcc : c = c1
      · subst hcc; simp [hc1eq]
      · simp [hcc, hmin c (Finset.mem_univ _)]
    calc p * size (ch c0) + q * α
        = ∑ c : Fin p, (size (ch c0) + (if c = c1 then q * α else 0)) := by
          simp [Finset.sum_add_distrib]
      _ ≤ ∑ c, size (ch c) := Finset.sum_le_sum hle
  calc p * m + q * d ≤ p * size (ch c0) + q * α :=
        Nat.add_le_add (Nat.mul_le_mul_left p (hm c0)) (Nat.mul_le_mul_left q hα_ge)
    _ ≤ size (.node ch) := hsum

/-! ### Claim U -/

theorem pow_card_union_le_size_aux (hp : 2 ≤ p) :
    ∀ {n : ℕ} (t : Tree p q n), ¬ F t 0 → p ^ (eSet t ∪ fSet t).card ≤ size t
  | _, .leaf f, h0 => by
      have hpos := size_pos_of_not_F0 _ h0
      have hempty : eSet (Tree.leaf (p := p) f) ∪ fSet (Tree.leaf (p := p) f) = ∅ := by
        simp [eSet, fSet]
      rw [hempty, Finset.card_empty, pow_zero]
      omega
  | _, .node ch, h0 => by
      have hp0 : 0 < p := by omega
      -- an unbalanced child has at least `p^|E⁻ ∪ F⁻|` elements
      have hchild : ∀ c, ¬ F (ch c) 0 → p ^ (eMinus ch ∪ fMinus ch).card ≤ size (ch c) := fun c hc =>
        le_trans (Nat.pow_le_pow_right hp0 (Finset.card_le_card (union_subset_child ch c)))
          (pow_card_union_le_size_aux hp (ch c) hc)
      have hle := card_union_node_le ch
      by_cases hF : F (.node ch) 1
      · -- every child is unbalanced
        calc p ^ (eSet (.node ch) ∪ fSet (.node ch)).card
            ≤ p ^ ((eMinus ch ∪ fMinus ch).card + 1) := Nat.pow_le_pow_right hp0 hle
          _ = ∑ _c : Fin p, p ^ (eMinus ch ∪ fMinus ch).card := by
              simp [pow_succ, mul_comm]
          _ ≤ ∑ c, size (ch c) :=
              Finset.sum_le_sum (fun c _ => hchild c (not_F0_child_of_F1 h0 hF c))
          _ = size (.node ch) := (size_node ch).symm
      · obtain ⟨c, hc⟩ := not_F0_node h0
        by_cases hE : E (.node ch) 1
        · -- the children have one size, and one of them is unbalanced
          rw [size_node_of_E1 hE c]
          calc p ^ (eSet (.node ch) ∪ fSet (.node ch)).card
              ≤ p ^ ((eMinus ch ∪ fMinus ch).card + 1) := Nat.pow_le_pow_right hp0 hle
            _ = p * p ^ (eMinus ch ∪ fMinus ch).card := by ring
            _ ≤ p * size (ch c) := Nat.mul_le_mul_left p (hchild c hc)
        · -- level 1 is in neither set
          rw [card_union_node_of_not ch hE hF]
          exact le_trans (hchild c hc) (size_child_le ch c)

/-! ### Claim G: the three facts about a child, and a witness -/

/-- (I) a child to which the recursion applies has at least `p^{|E⁻|} (p^{|G⁻|} + q)` elements -/
theorem sharp_child_I (hp0 : 0 < p) {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p)
    (ih : p ^ e (ch c) * (p ^ (fSet (ch c) \ eSet (ch c)).card + q) ≤ size (ch c)) :
    p ^ (eMinus ch).card * (p ^ (fMinus ch \ eMinus ch).card + q) ≤ size (ch c) := by
  have h1 : (eMinus ch).card ≤ e (ch c) := eMinus_card_le ch c
  have h2 : (eMinus ch).card + (fMinus ch \ eMinus ch).card
      ≤ e (ch c) + (fSet (ch c) \ eSet (ch c)).card := by
    unfold e
    rw [card_add_card_sdiff, card_add_card_sdiff]
    exact Finset.card_le_card (union_subset_child ch c)
  calc p ^ (eMinus ch).card * (p ^ (fMinus ch \ eMinus ch).card + q)
      = p ^ ((eMinus ch).card + (fMinus ch \ eMinus ch).card) + p ^ (eMinus ch).card * q := by ring
    _ ≤ p ^ (e (ch c) + (fSet (ch c) \ eSet (ch c)).card) + p ^ e (ch c) * q :=
        Nat.add_le_add (Nat.pow_le_pow_right hp0 h2)
          (Nat.mul_le_mul_right _ (Nat.pow_le_pow_right hp0 h1))
    _ = p ^ e (ch c) * (p ^ (fSet (ch c) \ eSet (ch c)).card + q) := by ring
    _ ≤ size (ch c) := ih

/-- (II) if every level of `G⁻` is in `E` of the child, `p^{|E⁻| + |G⁻|}` divides its size -/
theorem sharp_child_II {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p)
    (h : ∀ ℓ ∈ fMinus ch \ eMinus ch, ℓ ∈ eSet (ch c)) :
    p ^ ((eMinus ch).card + (fMinus ch \ eMinus ch).card) ∣ size (ch c) := by
  have hsub : eMinus ch ∪ fMinus ch ⊆ eSet (ch c) := by
    intro ℓ hℓ
    by_cases hm : ℓ ∈ eMinus ch
    · exact eMinus_subset ch c hm
    · rcases Finset.mem_union.1 hℓ with h' | h'
      · exact absurd h' hm
      · exact h ℓ (Finset.mem_sdiff.2 ⟨h', hm⟩)
  have hcard : (eMinus ch).card + (fMinus ch \ eMinus ch).card ≤ e (ch c) := by
    rw [card_add_card_sdiff]
    exact Finset.card_le_card hsub
  exact (pow_dvd_pow p hcard).trans (pow_e_dvd_size (ch c))

/-- (III) a balanced child has size a multiple of `p^{|E⁻|} q` -/
theorem sharp_child_III (hpq : Nat.Coprime p q) {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p)
    (hc : F (ch c) 0) : p ^ (eMinus ch).card * q ∣ size (ch c) :=
  (Nat.mul_dvd_mul (pow_dvd_pow p (eMinus_card_le ch c)) (dvd_refl q)).trans
    (pow_e_mul_q_dvd_size hpq (ch c) hc)

/-- a witness: if `G⁻` is not empty, some child is not empty and misses `E` at a level of `G⁻` -/
theorem exists_witness {n : ℕ} (ch : Fin p → Tree p q n) (h : (fMinus ch \ eMinus ch).Nonempty) :
    ∃ c ℓ, ℓ ∈ fMinus ch \ eMinus ch ∧ ℓ ∉ eSet (ch c) ∧ 0 < size (ch c) := by
  obtain ⟨ℓ, hℓ⟩ := h
  have hℓ' := Finset.mem_sdiff.1 hℓ
  have hf := (mem_fMinus ch ℓ).1 hℓ'.1
  have hne : ¬ ∀ c, E (ch c) ℓ := fun hall => hℓ'.2 ((mem_eMinus ch ℓ).2 ⟨hf.1, hf.2.1, hall⟩)
  push Not at hne
  obtain ⟨c, hc⟩ := hne
  refine ⟨c, ℓ, hℓ, fun hm => hc ((mem_eSet _ _).1 hm).2.2, ?_⟩
  by_contra hcon
  exact hc (E_of_empty (ch c) ℓ (by omega) hf.1 hf.2.1)

theorem add_le_mul_of_two_le {a b : ℕ} (ha : 2 ≤ a) (hb : 2 ≤ b) : a + b ≤ a * b := by
  nlinarith

/-! ### Claim G -/

theorem sharp_lemma3_aux (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) :
    ∀ {n : ℕ} (t : Tree p q n), ¬ F t 0 → (fSet t \ eSet t).Nonempty →
      p ^ e t * (p ^ (fSet t \ eSet t).card + q) ≤ size t
  | _, .leaf f, _, hne => by
      exfalso
      obtain ⟨ℓ, hℓ⟩ := hne
      obtain ⟨h1, h2, -⟩ := (mem_fSet _ _).1 (Finset.mem_sdiff.1 hℓ).1
      omega
  | _, .node ch, h0, hne => by
      have hp0 : 0 < p := by omega
      have hq0 : 0 < q := by omega
      obtain ⟨em, hem⟩ : ∃ em, em = (eMinus ch).card := ⟨_, rfl⟩
      obtain ⟨gm, hgm⟩ : ∃ gm, gm = (fMinus ch \ eMinus ch).card := ⟨_, rfl⟩
      have hkpos : 0 < (fSet (.node ch) \ eSet (.node ch)).card := Finset.card_pos.2 hne
      -- the three facts about a child
      have hI : ∀ c, ¬ F (ch c) 0 → (∃ ℓ ∈ fMinus ch \ eMinus ch, ℓ ∉ eSet (ch c)) →
          p ^ em * (p ^ gm + q) ≤ size (ch c) := by
        intro c hc hw
        obtain ⟨ℓ, hℓ, hnot⟩ := hw
        rw [hem, hgm]
        refine sharp_child_I hp0 ch c (sharp_lemma3_aux hp hq hpq (ch c) hc ⟨ℓ, ?_⟩)
        exact Finset.mem_sdiff.2 ⟨fMinus_subset ch c (Finset.mem_sdiff.1 hℓ).1, hnot⟩
      have hII : ∀ c, (∀ ℓ ∈ fMinus ch \ eMinus ch, ℓ ∈ eSet (ch c)) →
          p ^ (em + gm) ∣ size (ch c) := by
        intro c h
        rw [hem, hgm]
        exact sharp_child_II ch c h
      have hIII : ∀ c, F (ch c) 0 → p ^ em * q ∣ size (ch c) := by
        intro c h
        rw [hem]
        exact sharp_child_III hpq ch c h
      by_cases hF : F (.node ch) 1
      · by_cases hE : E (.node ch) 1
        · -- level 1 in `F` and in `E`: all children unbalanced, of one size; a witness is under (I)
          have hk : (fSet (.node ch) \ eSet (.node ch)).card = gm := by
            rw [hgm]
            exact card_sdiff_node_neg ch (fun h => h.2 hE)
          have hgne : (fMinus ch \ eMinus ch).Nonempty := Finset.card_pos.1 (by omega)
          obtain ⟨c0, ℓ, hℓ, hnot, -⟩ := exists_witness ch hgne
          have h1 := hI c0 (not_F0_child_of_F1 h0 hF c0) ⟨ℓ, hℓ, hnot⟩
          rw [hk, e_node_pos hE, ← hem, size_node_of_E1 hE c0, pow_succ]
          calc p ^ em * p * (p ^ gm + q) = p * (p ^ em * (p ^ gm + q)) := by ring
            _ ≤ p * size (ch c0) := Nat.mul_le_mul_left p h1
        · -- level 1 in `F` and not in `E`: Claim U for every child, and the additive array
          have hk : (fSet (.node ch) \ eSet (.node ch)).card = gm + 1 := by
            rw [hgm]
            exact card_sdiff_node_pos ch hF hE
          have hm : ∀ c, p ^ (em + gm) ≤ size (ch c) := by
            intro c
            have hU := pow_card_union_le_size_aux hp (ch c) (not_F0_child_of_F1 h0 hF c)
            have hcard : em + gm ≤ (eSet (ch c) ∪ fSet (ch c)).card := by
              rw [hem, hgm, card_add_card_sdiff]
              exact Finset.card_le_card (union_subset_child ch c)
            exact le_trans (Nat.pow_le_pow_right hp0 hcard) hU
          have hdiv : ∀ c, p ^ em ∣ size (ch c) := by
            intro c
            rw [hem]
            exact (pow_dvd_pow p (eMinus_card_le ch c)).trans (pow_e_dvd_size (ch c))
          have hb := additive_bound hq0 ch hF hE (p ^ em) (p ^ (em + gm))
            (Nat.Coprime.pow_left em hpq) hdiv hm
          rw [hk, e_node_neg hE, ← hem]
          calc p ^ em * (p ^ (gm + 1) + q) = p * p ^ (em + gm) + q * p ^ em := by ring
            _ ≤ size (.node ch) := hb
      · -- level 1 not in `F`
        have hk : (fSet (.node ch) \ eSet (.node ch)).card = gm := by
          rw [hgm]
          exact card_sdiff_node_neg ch (fun h => hF h.1)
        have hgpos : 0 < gm := by omega
        have hgne : (fMinus ch \ eMinus ch).Nonempty := Finset.card_pos.1 (by omega)
        obtain ⟨c0, ℓ0, hℓ0, hnot0, hc0pos⟩ := exists_witness ch hgne
        obtain ⟨c1, hc1⟩ := not_F0_node h0
        by_cases hex : ∃ c, ¬ F (ch c) 0 ∧ ∃ ℓ ∈ fMinus ch \ eMinus ch, ℓ ∉ eSet (ch c)
        · -- some unbalanced child is under (I)
          obtain ⟨c, hc, hw⟩ := hex
          have h1 := hI c hc hw
          by_cases hE : E (.node ch) 1
          · rw [hk, e_node_pos hE, ← hem, size_node_of_E1 hE c, pow_succ]
            calc p ^ em * p * (p ^ gm + q) = p * (p ^ em * (p ^ gm + q)) := by ring
              _ ≤ p * size (ch c) := Nat.mul_le_mul_left p h1
          · rw [hk, e_node_neg hE, ← hem]
            exact le_trans h1 (size_child_le ch c)
        · -- every unbalanced child is under (II); the witness is balanced, under (III)
          have hall : ∀ c, ¬ F (ch c) 0 → ∀ ℓ ∈ fMinus ch \ eMinus ch, ℓ ∈ eSet (ch c) := by
            intro c hc ℓ hℓ
            by_contra hnot
            exact hex ⟨c, hc, ℓ, hℓ, hnot⟩
          have hd1 : p ^ (em + gm) ∣ size (ch c1) := hII c1 (hall c1 hc1)
          have hc0bal : F (ch c0) 0 := by
            by_contra hcon
            exact hnot0 (hall c0 hcon ℓ0 hℓ0)
          have hd0 : p ^ em * q ∣ size (ch c0) := hIII c0 hc0bal
          have hc1pos : 0 < size (ch c1) := size_pos_of_not_F0 _ hc1
          by_cases hE : E (.node ch) 1
          · -- level 1 in `E`: one size, a multiple of `p^{|E⁻| + k} q`
            have hs : size (ch c0) = size (ch c1) := hE c0 c1
            have hd : p ^ (em + gm) * q ∣ size (ch c1) :=
              Nat.Coprime.mul_dvd_of_dvd_of_dvd (Nat.Coprime.pow_left _ hpq) hd1
                (hs ▸ dvd_of_mul_left_dvd hd0)
            have hge : p ^ (em + gm) * q ≤ size (ch c1) := Nat.le_of_dvd hc1pos hd
            have hpg : 2 ≤ p ^ gm :=
              calc 2 ≤ p := hp
                _ = p ^ 1 := (pow_one p).symm
                _ ≤ p ^ gm := Nat.pow_le_pow_right hp0 hgpos
            have hpq' : p ^ gm + q ≤ p ^ gm * q := add_le_mul_of_two_le hpg hq
            rw [hk, e_node_pos hE, ← hem, size_node_of_E1 hE c1, pow_succ]
            calc p ^ em * p * (p ^ gm + q) ≤ p ^ em * p * (p ^ gm * q) :=
                  Nat.mul_le_mul_left _ hpq'
              _ = p * (p ^ (em + gm) * q) := by ring
              _ ≤ p * size (ch c1) := Nat.mul_le_mul_left p hge
          · -- level 1 not in `E`: two different children, one under (II), one under (III)
            have hne01 : c0 ≠ c1 := by
              rintro rfl
              exact hc1 hc0bal
            have hge0 : p ^ em * q ≤ size (ch c0) := Nat.le_of_dvd hc0pos hd0
            have hge1 : p ^ (em + gm) ≤ size (ch c1) := Nat.le_of_dvd hc1pos hd1
            rw [hk, e_node_neg hE, ← hem]
            calc p ^ em * (p ^ gm + q) = p ^ em * q + p ^ (em + gm) := by ring
              _ ≤ size (ch c0) + size (ch c1) := Nat.add_le_add hge0 hge1
              _ ≤ size (.node ch) := size_two_children_le ch hne01

/-! ### The two theorems -/

/-- **Claim U.** If `Φ_q ∤ A`, then `|A| ≥ p^{|E ∪ F|}`. -/
theorem pow_card_union_le_size (hp : 2 ≤ p) :
    ∀ {n : ℕ} (t : Tree p q n), ¬ F t 0 → p ^ (eSet t ∪ fSet t).card ≤ size t := by
  intro n t h0
  exact pow_card_union_le_size_aux hp t h0

/-- **Claim G, the sharp form of Lemma 3.** If `Φ_q ∤ A` and `k ≥ 1` levels lie in `F` and not in `E`,
then `|A| ≥ p^{e} (p^{k} + q)`. -/
theorem sharp_lemma3 (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) :
    ∀ {n : ℕ} (t : Tree p q n), ¬ F t 0 → (fSet t \ eSet t).Nonempty →
      p ^ e t * (p ^ (fSet t \ eSet t).card + q) ≤ size t := by
  intro n t h0 hne
  exact sharp_lemma3_aux hp hq hpq t h0 hne

end Pnq
