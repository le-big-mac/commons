/-
The counting core of "weak tiling implies tiling in Z_{pⁿq}" (agent3 / Yonder), with no group in it.

A subset (or multiset) of Z_{pⁿ} × Z_q is stored as a `p`-ary tree of depth `n`: the children of a node are
the residue classes of the next base-`p` digit (lowest digit first), and a leaf holds, for one residue
`u mod pⁿ`, the numbers of elements `(u, j)`, `j : Fin q`.  In this form Lemma 0 of `pnq-agent3.md`
(subtrees) is the definition of the level conditions `E` and `F`.
-/
import Mathlib

open Finset

namespace Pnq

/-- A `p`-ary tree of depth `n` whose leaves are functions `Fin q → ℕ`. -/
inductive Tree (p q : ℕ) : ℕ → Type
  | leaf : (Fin q → ℕ) → Tree p q 0
  | node {n : ℕ} : (Fin p → Tree p q n) → Tree p q (n + 1)

variable {p q : ℕ}

/-- layer counts: the number of elements with second coordinate `j` -/
def lay : {n : ℕ} → Tree p q n → Fin q → ℕ
  | _, .leaf f => f
  | _, .node ch => fun j => ∑ c, lay (ch c) j

/-- number of elements -/
def size {n : ℕ} (t : Tree p q n) : ℕ := ∑ j, lay t j

/-- `E t ℓ` (for `1 ≤ ℓ ≤ n`): the coordinate form of `Φ_{p^ℓ} ∣ A`. -/
def E : {n : ℕ} → Tree p q n → ℕ → Prop
  | _, .leaf _, _ => False
  | _, .node _, 0 => False
  | _, .node ch, 1 => ∀ c c', size (ch c) = size (ch c')
  | _, .node ch, ℓ + 2 => ∀ c, E (ch c) (ℓ + 1)

/-- `F t ℓ` (for `0 ≤ ℓ ≤ n`): the coordinate form of `Φ_{p^ℓ q} ∣ A`; `F t 0` is `Φ_q ∣ A`. -/
def F : {n : ℕ} → Tree p q n → ℕ → Prop
  | _, t, 0 => ∀ j j', lay t j = lay t j'
  | _, .leaf _, _ + 1 => False
  | _, .node ch, 1 => ∀ c c' j j', lay (ch c) j + lay (ch c') j' = lay (ch c) j' + lay (ch c') j
  | _, .node ch, ℓ + 2 => ∀ c, F (ch c) (ℓ + 1)

@[simp] theorem lay_node {n : ℕ} (ch : Fin p → Tree p q n) (j : Fin q) :
    lay (.node ch) j = ∑ c, lay (ch c) j := rfl

theorem size_node {n : ℕ} (ch : Fin p → Tree p q n) :
    size (.node ch) = ∑ c, size (ch c) := by
  unfold size
  simp only [lay_node]
  exact Finset.sum_comm

@[simp] theorem E_node_one {n : ℕ} (ch : Fin p → Tree p q n) :
    E (.node ch) 1 ↔ ∀ c c', size (ch c) = size (ch c') := Iff.rfl

@[simp] theorem E_node_succ {n : ℕ} (ch : Fin p → Tree p q n) (ℓ : ℕ) :
    E (.node ch) (ℓ + 2) ↔ ∀ c, E (ch c) (ℓ + 1) := Iff.rfl

@[simp] theorem F_zero {n : ℕ} (t : Tree p q n) : F t 0 ↔ ∀ j j', lay t j = lay t j' := by
  cases t <;> rfl

@[simp] theorem F_node_one {n : ℕ} (ch : Fin p → Tree p q n) :
    F (.node ch) 1 ↔ ∀ c c' j j', lay (ch c) j + lay (ch c') j' = lay (ch c) j' + lay (ch c') j :=
  Iff.rfl

@[simp] theorem F_node_succ {n : ℕ} (ch : Fin p → Tree p q n) (ℓ : ℕ) :
    F (.node ch) (ℓ + 2) ↔ ∀ c, F (ch c) (ℓ + 1) := Iff.rfl

/-- a level at which `E` holds lies in `1..n` (if `p > 0`) -/
theorem E_range (hp : 0 < p) : ∀ {n : ℕ} (t : Tree p q n) (ℓ : ℕ), E t ℓ → 1 ≤ ℓ ∧ ℓ ≤ n
  | _, .leaf _, _, h => by exact absurd h (by simp [E])
  | _, .node _, 0, h => by exact absurd h (by simp [E])
  | _, .node _, 1, _ => by omega
  | _, .node ch, ℓ + 2, h => by
      have := E_range hp (ch ⟨0, hp⟩) (ℓ + 1) ((E_node_succ ch ℓ).1 h ⟨0, hp⟩)
      omega

/-- a level `≥ 1` at which `F` holds lies in `1..n` (if `p > 0`) -/
theorem F_range (hp : 0 < p) : ∀ {n : ℕ} (t : Tree p q n) (ℓ : ℕ), F t (ℓ + 1) → ℓ + 1 ≤ n
  | _, .leaf _, _, h => by exact absurd h (by simp [F])
  | _, .node _, 0, _ => by omega
  | _, .node ch, ℓ + 1, h => by
      have := F_range hp (ch ⟨0, hp⟩) ℓ ((F_node_succ ch ℓ).1 h ⟨0, hp⟩)
      omega

/-! ### Empty trees -/

theorem lay_eq_zero_of_size {n : ℕ} {t : Tree p q n} (h : size t = 0) (j : Fin q) : lay t j = 0 := by
  unfold size at h
  exact (Finset.sum_eq_zero_iff.1 h) j (Finset.mem_univ j)

theorem size_child_zero {n : ℕ} {ch : Fin p → Tree p q n} (h : size (.node ch) = 0) (c : Fin p) :
    size (ch c) = 0 := by
  rw [size_node] at h
  exact (Finset.sum_eq_zero_iff.1 h) c (Finset.mem_univ c)

/-- an empty tree satisfies every `E` condition in range -/
theorem E_of_empty : ∀ {n : ℕ} (t : Tree p q n) (ℓ : ℕ), size t = 0 → 1 ≤ ℓ → ℓ ≤ n → E t ℓ
  | _, .leaf _, _, _, _, _ => by omega
  | _, .node _, 0, _, _, _ => by omega
  | _, .node ch, 1, h, _, _ => by
      rw [E_node_one]; intro c c'; rw [size_child_zero h c, size_child_zero h c']
  | _, .node ch, ℓ + 2, h, _, _ => by
      rw [E_node_succ]; intro c
      exact E_of_empty (ch c) (ℓ + 1) (size_child_zero h c) (by omega) (by omega)

/-- an empty tree satisfies every `F` condition in range -/
theorem F_of_empty : ∀ {n : ℕ} (t : Tree p q n) (ℓ : ℕ), size t = 0 → ℓ ≤ n → F t ℓ
  | _, t, 0, h, _ => by
      rw [F_zero]; intro j j'; rw [lay_eq_zero_of_size h j, lay_eq_zero_of_size h j']
  | _, .leaf _, _ + 1, _, _ => by omega
  | _, .node ch, 1, h, _ => by
      rw [F_node_one]; intro c c' j j'
      simp [lay_eq_zero_of_size (size_child_zero h c), lay_eq_zero_of_size (size_child_zero h c')]
  | _, .node ch, ℓ + 2, h, _ => by
      rw [F_node_succ]; intro c
      exact F_of_empty (ch c) (ℓ + 1) (size_child_zero h c) (by omega)

/-! ### The set of levels in `E`, and its size -/

open Classical in
/-- the levels `1..n` at which `E` holds -/
noncomputable def eSet {n : ℕ} (t : Tree p q n) : Finset ℕ := (Finset.Icc 1 n).filter (fun ℓ => E t ℓ)

/-- `e(A)`: the number of prime powers `p^ℓ` with `Φ_{p^ℓ} ∣ A` -/
noncomputable def e {n : ℕ} (t : Tree p q n) : ℕ := (eSet t).card

open Classical in
/-- the levels at which every child satisfies `E` (the set `E⁻` of the note) -/
noncomputable def eMinus {n : ℕ} (ch : Fin p → Tree p q n) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => ∀ c, E (ch c) ℓ)

theorem mem_eSet {n : ℕ} (t : Tree p q n) (ℓ : ℕ) : ℓ ∈ eSet t ↔ 1 ≤ ℓ ∧ ℓ ≤ n ∧ E t ℓ := by
  simp [eSet, and_assoc]

theorem mem_eMinus {n : ℕ} (ch : Fin p → Tree p q n) (ℓ : ℕ) :
    ℓ ∈ eMinus ch ↔ 1 ≤ ℓ ∧ ℓ ≤ n ∧ ∀ c, E (ch c) ℓ := by
  simp [eMinus, and_assoc]

theorem eMinus_subset {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p) : eMinus ch ⊆ eSet (ch c) := by
  intro ℓ h
  rw [mem_eMinus] at h
  exact (mem_eSet _ _).2 ⟨h.1, h.2.1, h.2.2 c⟩

theorem eMinus_card_le {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p) : (eMinus ch).card ≤ e (ch c) :=
  Finset.card_le_card (eMinus_subset ch c)

theorem eSet_erase_one {n : ℕ} (ch : Fin p → Tree p q n) :
    (eSet (.node ch)).erase 1 = (eMinus ch).image (· + 1) := by
  ext ℓ
  simp only [Finset.mem_erase, mem_eSet, Finset.mem_image, mem_eMinus]
  constructor
  · rintro ⟨h1, h2, h3, h4⟩
    obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 2 := ⟨ℓ - 2, by omega⟩
    exact ⟨m + 1, ⟨by omega, by omega, (E_node_succ ch m).1 h4⟩, rfl⟩
  · rintro ⟨m, ⟨h1, h2, h3⟩, rfl⟩
    obtain ⟨k, rfl⟩ : ∃ k, m = k + 1 := ⟨m - 1, by omega⟩
    exact ⟨by omega, by omega, by omega, (E_node_succ ch k).2 h3⟩

open Classical in
/-- `e` of a node: one more than `|E⁻|` if the children have equal sizes, `|E⁻|` otherwise -/
theorem e_node {n : ℕ} (ch : Fin p → Tree p q n) :
    e (.node ch) = (if E (.node ch) 1 then 1 else 0) + (eMinus ch).card := by
  have hc : ((eMinus ch).image (· + 1)).card = (eMinus ch).card :=
    Finset.card_image_of_injective _ (fun a b h => by simpa using h)
  unfold e
  by_cases h1 : E (.node ch) 1
  · have hm : 1 ∈ eSet (.node ch) := (mem_eSet _ _).2 ⟨le_refl 1, by omega, h1⟩
    simp only [h1, ↓reduceIte]
    rw [← hc, ← eSet_erase_one, Finset.card_erase_of_mem hm]
    have := Finset.card_pos.2 ⟨1, hm⟩
    omega
  · have hm : 1 ∉ eSet (.node ch) := fun h => h1 ((mem_eSet _ _).1 h).2.2
    simp only [h1, ↓reduceIte]
    rw [← hc, ← eSet_erase_one, Finset.erase_eq_of_notMem hm]
    simp

theorem e_node_pos {n : ℕ} {ch : Fin p → Tree p q n} (h : E (.node ch) 1) :
    e (.node ch) = (eMinus ch).card + 1 := by
  classical
  rw [e_node]; simp only [h, ↓reduceIte]; omega

theorem e_node_neg {n : ℕ} {ch : Fin p → Tree p q n} (h : ¬ E (.node ch) 1) :
    e (.node ch) = (eMinus ch).card := by
  classical
  rw [e_node]; simp only [h, ↓reduceIte]; omega

/-! ### Divisibility: `p^e ∣ |A|`, and `q ∣ |A|` when `Φ_q ∣ A` -/

theorem pow_e_dvd_size : ∀ {n : ℕ} (t : Tree p q n), p ^ e t ∣ size t
  | _, .leaf _ => by simp [e, eSet]
  | _, .node ch => by
      have h : ∀ c, p ^ (eMinus ch).card ∣ size (ch c) := fun c =>
        (pow_dvd_pow p (eMinus_card_le ch c)).trans (pow_e_dvd_size (ch c))
      rw [size_node]
      by_cases h1 : E (.node ch) 1
      · rw [e_node_pos h1]
        rcases Nat.eq_zero_or_pos p with hp | hp
        · subst hp; simp
        · have hc : ∀ c, size (ch c) = size (ch ⟨0, hp⟩) := fun c => h1 c ⟨0, hp⟩
          rw [Finset.sum_congr rfl (fun c _ => hc c), Finset.sum_const, Finset.card_univ,
            Fintype.card_fin, smul_eq_mul, pow_succ, mul_comm]
          exact Nat.mul_dvd_mul (dvd_refl p) (h ⟨0, hp⟩)
      · rw [e_node_neg h1]
        exact Finset.dvd_sum (fun c _ => h c)

theorem q_dvd_size {n : ℕ} (t : Tree p q n) (h0 : F t 0) : q ∣ size t := by
  rw [F_zero] at h0
  rcases Nat.eq_zero_or_pos q with hq | hq
  · subst hq; simp [size]
  · unfold size
    rw [Finset.sum_congr rfl (fun j _ => h0 j ⟨0, hq⟩), Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, smul_eq_mul]
    exact dvd_mul_right q _

theorem size_eq_q_mul {n : ℕ} (t : Tree p q n) (h0 : F t 0) (j : Fin q) : size t = q * lay t j := by
  rw [F_zero] at h0
  unfold size
  rw [Finset.sum_congr rfl (fun j' _ => h0 j' j), Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul]

theorem pow_e_mul_q_dvd_size (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n) (h0 : F t 0) :
    p ^ e t * q ∣ size t :=
  Nat.Coprime.mul_dvd_of_dvd_of_dvd (Nat.Coprime.pow_left _ hpq) (pow_e_dvd_size t) (q_dvd_size t h0)

/-! ### Sizes of a node and of its children -/

theorem size_node_of_E1 {n : ℕ} {ch : Fin p → Tree p q n} (h1 : E (.node ch) 1) (c : Fin p) :
    size (.node ch) = p * size (ch c) := by
  rw [size_node, Finset.sum_congr rfl (fun c' _ => h1 c' c), Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul]

theorem size_child_le {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p) :
    size (ch c) ≤ size (.node ch) := by
  rw [size_node]
  exact Finset.single_le_sum (f := fun c => size (ch c)) (fun _ _ => Nat.zero_le _) (Finset.mem_univ c)

theorem size_two_children_le {n : ℕ} (ch : Fin p → Tree p q n) {c0 c1 : Fin p} (h : c0 ≠ c1) :
    size (ch c0) + size (ch c1) ≤ size (.node ch) := by
  rw [size_node, ← Finset.sum_pair (f := fun c => size (ch c)) h]
  exact Finset.sum_le_sum_of_subset (Finset.subset_univ _)

theorem not_F0_node {n : ℕ} {ch : Fin p → Tree p q n} (h0 : ¬ F (.node ch) 0) :
    ∃ c, ¬ F (ch c) 0 := by
  by_contra hcon
  push Not at hcon
  apply h0
  rw [F_zero]
  intro j j'
  simp only [lay_node]
  exact Finset.sum_congr rfl (fun c _ => (F_zero _).1 (hcon c) j j')

/-! ### Lemma 3 (lower bound) -/

/-- The case `a = 1` of Lemma 3: the array of the children's layer counts is additive, the children's
sizes are not all equal, and the layer counts of the node are not all equal. -/
theorem lemma3_base (hq : 0 < q) (hpq : Nat.Coprime p q) {n : ℕ} (ch : Fin p → Tree p q n)
    (h0 : ¬ F (.node ch) 0) (hF : F (.node ch) 1) (hE : ¬ E (.node ch) 1) :
    p ^ e (.node ch) * (p + q) ≤ size (.node ch) := by
  rw [e_node_neg hE]
  set k := (eMinus ch).card with hk
  rw [F_node_one] at hF
  have hdiv : ∀ c, p ^ k ∣ size (ch c) := fun c =>
    (pow_dvd_pow p (eMinus_card_le ch c)).trans (pow_e_dvd_size (ch c))
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
  have hα_dvd : p ^ k ∣ α := by
    have h1 : p ^ k ∣ q * α := by
      have := hdiv c1
      rw [hc1eq] at this
      exact (Nat.dvd_add_right (hdiv c0)).1 this
    exact (Nat.Coprime.dvd_mul_left (Nat.Coprime.pow_left k hpq)).1 h1
  have hα_ge : p ^ k ≤ α := Nat.le_of_dvd hαpos hα_dvd
  -- the smallest child is not empty
  have hc0pos : 0 < size (ch c0) := by
    by_contra hcon
    have hz : size (ch c0) = 0 := by omega
    apply h0
    rw [F_zero]
    intro j j'
    simp only [lay_node]
    refine Finset.sum_congr rfl (fun c _ => ?_)
    have h := hF c c0 j j'
    rw [lay_eq_zero_of_size hz j, lay_eq_zero_of_size hz j'] at h
    omega
  have hc0_ge : p ^ k ≤ size (ch c0) := Nat.le_of_dvd hc0pos (hdiv c0)
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
  calc p ^ k * (p + q) = p * p ^ k + q * p ^ k := by ring
    _ ≤ p * size (ch c0) + q * α :=
      Nat.add_le_add (Nat.mul_le_mul_left p hc0_ge) (Nat.mul_le_mul_left q hα_ge)
    _ ≤ size (.node ch) := hsum

/-- **Lemma 3.** If `Φ_q ∤ A` and some level `a ≥ 1` has `Φ_{p^a q} ∣ A` and `Φ_{p^a} ∤ A`, then
`|A| ≥ p^{e(A)} (p + q)`. -/
theorem lemma3 (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) :
    ∀ {n : ℕ} (t : Tree p q n) (a : ℕ), ¬ F t 0 → F t (a + 1) → ¬ E t (a + 1) →
      p ^ e t * (p + q) ≤ size t
  | _, .leaf _, _, _, hF, _ => by exact absurd hF (by simp [F])
  | _, .node ch, 0, h0, hF, hE => lemma3_base (by omega) hpq ch h0 hF hE
  | _, .node ch, a + 1, h0, hF, hE => by
      have hp0 : 0 < p := by omega
      rw [F_node_succ] at hF
      rw [E_node_succ] at hE
      set k := (eMinus ch).card with hk
      by_cases hex : ∃ c, ¬ E (ch c) (a + 1) ∧ ¬ F (ch c) 0
      · -- (α) one child has both properties
        obtain ⟨c, hEc, hFc⟩ := hex
        have ih := lemma3 hp hq hpq (ch c) a hFc (hF c) hEc
        have hk_le : p ^ k * (p + q) ≤ size (ch c) :=
          le_trans (Nat.mul_le_mul_right _ (Nat.pow_le_pow_right hp0 (eMinus_card_le ch c))) ih
        by_cases h1 : E (.node ch) 1
        · rw [e_node_pos h1, size_node_of_E1 h1 c, pow_succ]
          calc p ^ k * p * (p + q) = p * (p ^ k * (p + q)) := by ring
            _ ≤ p * size (ch c) := Nat.mul_le_mul_left p hk_le
        · rw [e_node_neg h1]
          exact le_trans hk_le (size_child_le ch c)
      · -- (β) the two properties sit in different children
        push Not at hex
        obtain ⟨c0, hEc0⟩ : ∃ c0, ¬ E (ch c0) (a + 1) := by
          by_contra hcon
          push Not at hcon
          exact hE hcon
        obtain ⟨c1, hFc1⟩ := not_F0_node h0
        have hFc0 : F (ch c0) 0 := hex c0 hEc0
        have hEc1 : E (ch c1) (a + 1) := by
          by_contra hcon
          exact hFc1 (hex c1 hcon)
        have hne : c0 ≠ c1 := by
          rintro rfl
          exact hFc1 hFc0
        have hrange : a + 1 ≤ _ := F_range hp0 (ch c0) a (hF c0)
        have hc0pos : 0 < size (ch c0) := by
          by_contra hcon
          exact hEc0 (E_of_empty (ch c0) (a + 1) (by omega) (by omega) hrange)
        have hc1pos : 0 < size (ch c1) := by
          by_contra hcon
          exact hFc1 (F_of_empty (ch c1) 0 (by omega) (Nat.zero_le _))
        have hd0 : p ^ k * q ∣ size (ch c0) :=
          (Nat.mul_dvd_mul (pow_dvd_pow p (eMinus_card_le ch c0)) (dvd_refl q)).trans
            (pow_e_mul_q_dvd_size hpq (ch c0) hFc0)
        have hk1 : k + 1 ≤ e (ch c1) := by
          have hnot : a + 1 ∉ eMinus ch := by
            intro hmem
            exact hEc0 (((mem_eMinus ch (a + 1)).1 hmem).2.2 c0)
          have hsub : insert (a + 1) (eMinus ch) ⊆ eSet (ch c1) := by
            intro ℓ hℓ
            rcases Finset.mem_insert.1 hℓ with rfl | hℓ
            · exact (mem_eSet _ _).2 ⟨by omega, hrange, hEc1⟩
            · exact eMinus_subset ch c1 hℓ
          have := Finset.card_le_card hsub
          rw [Finset.card_insert_of_notMem hnot] at this
          exact this
        have hd1 : p ^ (k + 1) ∣ size (ch c1) :=
          (pow_dvd_pow p hk1).trans (pow_e_dvd_size (ch c1))
        by_cases h1 : E (.node ch) 1
        · have hs : size (ch c0) = size (ch c1) := h1 c0 c1
          have hd : p ^ (k + 1) * q ∣ size (ch c1) :=
            Nat.Coprime.mul_dvd_of_dvd_of_dvd (Nat.Coprime.pow_left _ hpq) hd1
              (hs ▸ dvd_of_mul_left_dvd hd0)
          have hge : p ^ (k + 1) * q ≤ size (ch c1) := Nat.le_of_dvd hc1pos hd
          have hpq' : p + q ≤ p * q := by nlinarith
          rw [e_node_pos h1, size_node_of_E1 h1 c1]
          calc p ^ (k + 1) * (p + q) ≤ p ^ (k + 1) * (p * q) := Nat.mul_le_mul_left _ hpq'
            _ = p * (p ^ (k + 1) * q) := by ring
            _ ≤ p * size (ch c1) := Nat.mul_le_mul_left p hge
        · have hge0 : p ^ k * q ≤ size (ch c0) := Nat.le_of_dvd hc0pos hd0
          have hge1 : p ^ (k + 1) ≤ size (ch c1) := Nat.le_of_dvd hc1pos hd1
          rw [e_node_neg h1]
          calc p ^ k * (p + q) = p ^ k * q + p ^ (k + 1) := by ring
            _ ≤ size (ch c0) + size (ch c1) := Nat.add_le_add hge0 hge1
            _ ≤ size (.node ch) := size_two_children_le ch hne

/-! ### Lemma 4 (structure) -/

/-- if `p^m ∣ p^k * q` with `p ≥ 2` and `p`, `q` coprime, then `m ≤ k` -/
theorem exp_le_of_pow_dvd (hp : 2 ≤ p) (hpq : Nat.Coprime p q) {m k : ℕ} (h : p ^ m ∣ p ^ k * q) :
    m ≤ k :=
  (Nat.pow_dvd_pow_iff_le_right (by omega)).1
    (Nat.Coprime.dvd_of_dvd_mul_right (Nat.Coprime.pow_left m hpq) h)

/-- **Lemma 4.** If `A` is nonempty, `Φ_q ∣ A`, `|A| = p^{e(A)} q`, and some level `b` has
`Φ_{p^b q} ∣ A` and `Φ_{p^b} ∤ A`, then every level `a < b` with `Φ_{p^a} ∣ A` has `Φ_{p^a q} ∣ A`. -/
theorem lemma4 (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) :
    ∀ {n : ℕ} (t : Tree p q n) (b : ℕ), 0 < size t → F t 0 → size t = p ^ e t * q →
      F t (b + 1) → ¬ E t (b + 1) → ∀ a, a < b → E t (a + 1) → F t (a + 1)
  | _, .leaf _, _, _, _, _, hFb, _ => by exact absurd hFb (by simp [F])
  | _, .node _, 0, _, _, _, _, _ => fun a ha => absurd ha (Nat.not_lt_zero a)
  | _, .node ch, b + 1, hpos, hF0, hsize, hFb, hEb => by
      have hp0 : 0 < p := by omega
      have hq0 : 0 < q := by omega
      rw [F_node_succ] at hFb
      rw [E_node_succ] at hEb
      set k := (eMinus ch).card with hk
      have hpk : 0 < p ^ k := Nat.pow_pos hp0
      have hrange : b + 1 ≤ _ := F_range hp0 (ch ⟨0, hp0⟩) b (hFb ⟨0, hp0⟩)
      have hbnot : b + 1 ∉ eMinus ch := by
        intro hmem
        exact hEb ((mem_eMinus ch (b + 1)).1 hmem).2.2
      -- a child whose `e` is at most `k` has exactly the levels of `eMinus`
      have key : ∀ c, e (ch c) ≤ k → eMinus ch = eSet (ch c) := fun c hle =>
        Finset.eq_of_subset_of_card_le (eMinus_subset ch c) hle
      by_cases h1 : E (.node ch) 1
      · -- all children have the same size `p^k q`
        have hs : ∀ c, size (ch c) = p ^ k * q := by
          intro c
          have h := size_node_of_E1 h1 c
          rw [hsize, e_node_pos h1, pow_succ] at h
          have h' : p * (p ^ k * q) = p * size (ch c) := by rw [← h]; ring
          exact (Nat.eq_of_mul_eq_mul_left hp0 h').symm
        have hek : ∀ c, e (ch c) = k := by
          intro c
          have h1' := eMinus_card_le ch c
          have h2 : e (ch c) ≤ k := exp_le_of_pow_dvd hp hpq (hs c ▸ pow_e_dvd_size (ch c))
          omega
        have hEcb : ∀ c, ¬ E (ch c) (b + 1) := by
          intro c hE
          apply hbnot
          rw [key c (hek c).le]
          exact (mem_eSet _ _).2 ⟨by omega, hrange, hE⟩
        have hF0c : ∀ c, F (ch c) 0 := by
          intro c
          by_contra hcon
          have h3 := lemma3 hp hq hpq (ch c) b hcon (hFb c) (hEcb c)
          rw [hek c, hs c] at h3
          have : p ^ k * q < p ^ k * (p + q) := Nat.mul_lt_mul_of_pos_left (by omega) hpk
          omega
        intro a ha hEa
        rcases a with _ | a
        · rw [F_node_one]
          intro c c' j j'
          rw [(F_zero _).1 (hF0c c) j j', (F_zero _).1 (hF0c c') j' j]
        · rw [F_node_succ]
          rw [E_node_succ] at hEa
          intro c
          exact lemma4 hp hq hpq (ch c) b (by rw [hs c]; exact Nat.mul_pos hpk hq0) (hF0c c)
            (by rw [hs c, hek c]) (hFb c) (hEcb c) a (by omega) (hEa c)
      · -- the children's sizes are not all equal: the whole set sits in one child
        have he : e (.node ch) = k := e_node_neg h1
        rw [he] at hsize
        have hkind : ∀ c, ¬ F (ch c) 0 → E (ch c) (b + 1) := by
          intro c hF0c
          by_contra hEc
          have h3 := lemma3 hp hq hpq (ch c) b hF0c (hFb c) hEc
          have h4 := size_child_le ch c
          have h5 : p ^ k * (p + q) ≤ p ^ e (ch c) * (p + q) :=
            Nat.mul_le_mul_right _ (Nat.pow_le_pow_right hp0 (eMinus_card_le ch c))
          have : p ^ k * q < p ^ k * (p + q) := Nat.mul_lt_mul_of_pos_left (by omega) hpk
          omega
        obtain ⟨cs, hcs_pos, hcs_F0⟩ : ∃ c, 0 < size (ch c) ∧ F (ch c) 0 := by
          by_contra hcon
          push Not at hcon
          apply hEb
          intro c
          rcases Nat.eq_zero_or_pos (size (ch c)) with hz | hpos'
          · exact E_of_empty (ch c) (b + 1) hz (by omega) hrange
          · exact hkind c (hcon c hpos')
        have hdvd : p ^ e (ch cs) * q ∣ size (ch cs) := pow_e_mul_q_dvd_size hpq (ch cs) hcs_F0
        have hge : p ^ k * q ≤ size (ch cs) :=
          le_trans (Nat.mul_le_mul_right _ (Nat.pow_le_pow_right hp0 (eMinus_card_le ch cs)))
            (Nat.le_of_dvd hcs_pos hdvd)
        have hcs_size : size (ch cs) = p ^ k * q := by
          have := size_child_le ch cs
          omega
        have hothers : ∀ c, c ≠ cs → size (ch c) = 0 := by
          intro c hc
          have := size_two_children_le ch hc
          omega
        have hek : e (ch cs) = k := by
          have h1' := eMinus_card_le ch cs
          have h2 : e (ch cs) ≤ k := exp_le_of_pow_dvd hp hpq (hcs_size ▸ pow_e_dvd_size (ch cs))
          omega
        have hEcs : ¬ E (ch cs) (b + 1) := by
          intro hE
          apply hbnot
          rw [key cs hek.le]
          exact (mem_eSet _ _).2 ⟨by omega, hrange, hE⟩
        intro a ha hEa
        rcases a with _ | a
        · exact absurd hEa h1
        · rw [F_node_succ]
          rw [E_node_succ] at hEa
          intro c
          by_cases hc : c = cs
          · subst hc
            exact lemma4 hp hq hpq (ch c) b hcs_pos hcs_F0 (by rw [hcs_size, hek]) (hFb c) hEcs a
              (by omega) (hEa c)
          · exact F_of_empty (ch c) (a + 1) (hothers c hc) (by omega)

/-! ### The counting theorem (Section 5 of the note, with the three bounds as hypotheses) -/

open Classical in
/-- **Counting theorem.** Let `A` be nonempty and suppose its size obeys the three upper bounds that weak
tiling gives: (U1) `|A| ≤ p^e q`; (U2) `|A| ≤ p^e` if `Φ_q ∤ A` and every level in `F` is in `E`; (L2)
`|A| · min(p, q) ≤ p^e q` if `Φ_q ∣ A`, some level `a` is in `E` and not in `F`, and above `a` the sets
`E` and `F` agree.  Then (T1) `|A| = p^e`, times `q` if `Φ_q ∣ A`; and (T2) if `Φ_q ∣ A` then every
level in `E` is in `F`. -/
theorem counting (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n)
    (hpos : 0 < size t)
    (U1 : size t ≤ p ^ e t * q)
    (U2 : ¬ F t 0 → (∀ ℓ, F t (ℓ + 1) → E t (ℓ + 1)) → size t ≤ p ^ e t)
    (L2 : F t 0 → ∀ a, E t (a + 1) → ¬ F t (a + 1) →
      (∀ ℓ, a < ℓ → (E t (ℓ + 1) ↔ F t (ℓ + 1))) → size t * min p q ≤ p ^ e t * q) :
    size t = p ^ e t * (if F t 0 then q else 1) ∧ (F t 0 → ∀ ℓ, E t (ℓ + 1) → F t (ℓ + 1)) := by
  have hp0 : 0 < p := by omega
  have hpe : 0 < p ^ e t := Nat.pow_pos hp0
  by_cases h0 : F t 0
  · have hsize : size t = p ^ e t * q :=
      Nat.le_antisymm U1 (Nat.le_of_dvd hpos (pow_e_mul_q_dvd_size hpq t h0))
    refine ⟨by simp only [h0, ↓reduceIte]; exact hsize, fun _ => ?_⟩
    by_contra hcon
    push Not at hcon
    obtain ⟨ℓ0, hE0, hF0⟩ := hcon
    -- the largest level in `E` and not in `F`
    let S : Finset ℕ := (Finset.range n).filter (fun ℓ => E t (ℓ + 1) ∧ ¬ F t (ℓ + 1))
    have hmemS : ∀ ℓ, ℓ ∈ S ↔ E t (ℓ + 1) ∧ ¬ F t (ℓ + 1) := by
      intro ℓ
      simp only [S, Finset.mem_filter, Finset.mem_range]
      constructor
      · exact fun h => h.2
      · intro h
        have := (E_range hp0 t (ℓ + 1) h.1).2
        exact ⟨by omega, h⟩
    have hne : S.Nonempty := ⟨ℓ0, (hmemS ℓ0).2 ⟨hE0, hF0⟩⟩
    obtain ⟨hEa, hFa⟩ := (hmemS _).1 (Finset.max'_mem S hne)
    set a := S.max' hne with ha
    have hmax : ∀ ℓ, a < ℓ → E t (ℓ + 1) → F t (ℓ + 1) := by
      intro ℓ hℓ hE
      by_contra hF
      have := Finset.le_max' S ℓ ((hmemS ℓ).2 ⟨hE, hF⟩)
      omega
    by_cases hb : ∃ b, a < b ∧ F t (b + 1) ∧ ¬ E t (b + 1)
    · obtain ⟨b, hab, hFb, hEb⟩ := hb
      exact hFa (lemma4 hp hq hpq t b hpos h0 hsize hFb hEb a hab hEa)
    · push Not at hb
      have h2 := L2 h0 a hEa hFa (fun ℓ hℓ => ⟨hmax ℓ hℓ, hb ℓ hℓ⟩)
      rw [← hsize] at h2
      have hmin : 2 ≤ min p q := le_min hp hq
      have : size t * 2 ≤ size t * min p q := Nat.mul_le_mul_left _ hmin
      omega
  · refine ⟨?_, fun h => absurd h h0⟩
    simp only [h0, ↓reduceIte, mul_one]
    have hFE : ∀ ℓ, F t (ℓ + 1) → E t (ℓ + 1) := by
      intro ℓ hF
      by_contra hE
      have h3 := lemma3 hp hq hpq t ℓ h0 hF hE
      have : p ^ e t * q < p ^ e t * (p + q) := Nat.mul_lt_mul_of_pos_left (by omega) hpe
      omega
    exact Nat.le_antisymm (U2 h0 hFE) (Nat.le_of_dvd hpos (pow_e_dvd_size t))

end Pnq
