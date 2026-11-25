/-
From a step weak-tiling complement on the tree to the three upper bounds (agent3 / Yonder).

A *step complement* is a function `γ : ℕ → Bool → ℝ`: `γ d true` is the weight of an element that agrees
with the point on exactly the lowest `d` base-`p` digits and lies in the same layer, `γ d false` the weight
of one in another layer; `d = n` means the same residue mod `pⁿ`.  The identity `1_A ∗ f = 1` is written by
recursion on the tree, carrying the contribution of everything outside the current subtree as a function
of the layer.  No characters appear: summing the identity over subtrees gives the linear relations that
the Fourier transform would give.
-/
import Pnq.Tree

open Finset

namespace Pnq

variable {p q : ℕ}

/-- contribution to a point of layer `w` from one sibling subtree `s`, at agreement depth `d` -/
def sib (γ : ℕ → Bool → ℝ) (d : ℕ) {n : ℕ} (s : Tree p q n) (w : Fin q) : ℝ :=
  γ d true * (lay s w : ℝ) + γ d false * ((size s : ℝ) - (lay s w : ℝ))

/-- the outside contribution seen from child `c` of a node at depth `d` -/
def extChild (γ : ℕ → Bool → ℝ) (d : ℕ) {n : ℕ} (ch : Fin p → Tree p q n) (c : Fin p)
    (ext : Fin q → ℝ) : Fin q → ℝ :=
  fun w => ext w + ∑ c' ∈ Finset.univ.erase c, sib γ d (ch c') w

/-- the weak-tiling identity at every point of a subtree whose root is at depth `d`, given the
contribution `ext` of all elements outside the subtree -/
def Tiles (γ : ℕ → Bool → ℝ) : {n : ℕ} → ℕ → Tree p q n → (Fin q → ℝ) → Prop
  | _, d, .leaf f, ext =>
      ∀ w, ext w + γ d true * (f w : ℝ) + γ d false * ((∑ j, (f j : ℝ)) - (f w : ℝ)) = 1
  | _, d, .node ch, ext => ∀ c, Tiles γ (d + 1) (ch c) (extChild γ d ch c ext)

/-- a step weak-tiling complement of the set stored in `t` -/
def StepTiling (γ : ℕ → Bool → ℝ) {n : ℕ} (t : Tree p q n) : Prop :=
  (∀ d b, 0 ≤ γ d b) ∧ γ n true = 1 ∧ Tiles γ 0 t (fun _ => 0)

/-- `K p γ d m`: the sum of `γ` over the elements of the same layer in a subtree of depth `m` rooted at
depth `d` (seen from one of its points) -/
def K (p : ℕ) (γ : ℕ → Bool → ℝ) : ℕ → ℕ → ℝ
  | d, 0 => γ d true
  | d, m + 1 => K p γ (d + 1) m + ((p : ℝ) ^ (m + 1) - (p : ℝ) ^ m) * γ d true

/-- `J p γ d m`: the same for one other layer -/
def J (p : ℕ) (γ : ℕ → Bool → ℝ) : ℕ → ℕ → ℝ
  | d, 0 => γ d false
  | d, m + 1 => J p γ (d + 1) m + ((p : ℝ) ^ (m + 1) - (p : ℝ) ^ m) * γ d false

/-- `G`: the sum of `γ` over a whole subtree, all layers -/
def G (p q : ℕ) (γ : ℕ → Bool → ℝ) (d m : ℕ) : ℝ := K p γ d m + ((q : ℝ) - 1) * J p γ d m

theorem size_leaf (f : Fin q → ℕ) : size (Tree.leaf (p := p) f) = ∑ j, f j := rfl

theorem sum_erase_all {α : Type*} [Fintype α] [DecidableEq α] (h : α → ℝ) :
    ∑ c, ∑ c' ∈ Finset.univ.erase c, h c' = ((Fintype.card α : ℝ) - 1) * ∑ c, h c := by
  have : ∀ c, ∑ c' ∈ Finset.univ.erase c, h c' = (∑ c', h c') - h c := fun c => by
    rw [Finset.sum_erase_eq_sub (Finset.mem_univ c)]
  simp only [this, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  ring

/-- **Sum over one layer of a subtree.** -/
theorem tiles_layer_sum (γ : ℕ → Bool → ℝ) :
    ∀ {n : ℕ} (t : Tree p q n) (d : ℕ) (ext : Fin q → ℝ), Tiles γ d t ext → ∀ w,
      (p : ℝ) ^ n * ext w + (lay t w : ℝ) * K p γ d n + ((size t : ℝ) - (lay t w : ℝ)) * J p γ d n
        = (p : ℝ) ^ n
  | _, .leaf f, d, ext, h, w => by
      have := h w
      simp only [size_leaf, lay, K, J, pow_zero, one_mul, Nat.cast_sum]
      linarith
  | _, .node (n := n) ch, d, ext, h, w => by
      have ih : ∀ c, (p : ℝ) ^ n * extChild γ d ch c ext w + (lay (ch c) w : ℝ) * K p γ (d + 1) n
          + ((size (ch c) : ℝ) - (lay (ch c) w : ℝ)) * J p γ (d + 1) n = (p : ℝ) ^ n :=
        fun c => tiles_layer_sum γ (ch c) (d + 1) _ (h c) w
      have hsum := Finset.sum_congr (s₁ := (Finset.univ : Finset (Fin p))) rfl (fun c _ => ih c)
      have hL : (lay (Tree.node ch) w : ℝ) = ∑ c, (lay (ch c) w : ℝ) := by
        rw [lay_node]; push_cast; rfl
      have hR : (size (Tree.node ch) : ℝ) = ∑ c, (size (ch c) : ℝ) := by
        rw [size_node]; push_cast; rfl
      have hext : ∑ c, extChild γ d ch c ext w
          = (p : ℝ) * ext w + ((p : ℝ) - 1) * (γ d true * (∑ c, (lay (ch c) w : ℝ))
              + γ d false * ((∑ c, (size (ch c) : ℝ)) - ∑ c, (lay (ch c) w : ℝ))) := by
        unfold extChild
        rw [Finset.sum_add_distrib, sum_erase_all (fun c' => sib γ d (ch c') w)]
        simp only [sib, Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
          Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum]
      simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.sum_mul,
        Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
      rw [hext] at hsum
      rw [hL, hR]
      simp only [K, J]
      linear_combination hsum

/-- **Sum over a whole subtree.** -/
theorem tiles_sum (γ : ℕ → Bool → ℝ) {n : ℕ} (t : Tree p q n) (d : ℕ) (ext : Fin q → ℝ)
    (h : Tiles γ d t ext) :
    (p : ℝ) ^ n * ∑ w, ext w + (size t : ℝ) * G p q γ d n = (q : ℝ) * (p : ℝ) ^ n := by
  have hsum := Finset.sum_congr (s₁ := (Finset.univ : Finset (Fin q))) rfl
    (fun w _ => tiles_layer_sum γ t d ext h w)
  have hS : (size t : ℝ) = ∑ w, (lay t w : ℝ) := by
    unfold size; push_cast; rfl
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.sum_mul,
    Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul] at hsum
  rw [← hS] at hsum
  unfold G
  linear_combination hsum

/-! ### The linear relations forced by a failing level condition -/

/-- vanishes when the children's layer counts are not additive (the relation `f̂ = 0` at order `p^ℓ q`) -/
def Xrel (p : ℕ) (γ : ℕ → Bool → ℝ) (d m : ℕ) : ℝ :=
  K p γ (d + 1) m - J p γ (d + 1) m - (p : ℝ) ^ m * (γ d true - γ d false)

/-- together with `Xrel`: `Xrel + q * Yrel` vanishes when the children's sizes are not all equal -/
def Yrel (p : ℕ) (γ : ℕ → Bool → ℝ) (d m : ℕ) : ℝ := J p γ (d + 1) m - (p : ℝ) ^ m * γ d false

theorem node_rel (γ : ℕ → Bool → ℝ) {n : ℕ} (ch : Fin p → Tree p q n) (d : ℕ) (ext : Fin q → ℝ)
    (h : Tiles γ d (.node ch) ext) (c : Fin p) (w : Fin q) :
    (lay (ch c) w : ℝ) * Xrel p γ d n + (size (ch c) : ℝ) * Yrel p γ d n
      = (p : ℝ) ^ n * (1 - ext w - γ d true * (lay (Tree.node ch) w : ℝ)
          - γ d false * ((size (Tree.node ch) : ℝ) - (lay (Tree.node ch) w : ℝ))) := by
  have h1 := tiles_layer_sum γ (ch c) (d + 1) _ (h c) w
  have hL : (lay (Tree.node ch) w : ℝ) = ∑ c, (lay (ch c) w : ℝ) := by
    rw [lay_node]; push_cast; rfl
  have hR : (size (Tree.node ch) : ℝ) = ∑ c, (size (ch c) : ℝ) := by
    rw [size_node]; push_cast; rfl
  have hext : extChild γ d ch c ext w = ext w + (γ d true * ((lay (Tree.node ch) w : ℝ) - lay (ch c) w)
      + γ d false * (((size (Tree.node ch) : ℝ) - size (ch c))
          - ((lay (Tree.node ch) w : ℝ) - lay (ch c) w))) := by
    unfold extChild
    rw [Finset.sum_erase_eq_sub (Finset.mem_univ c), hL, hR]
    simp only [sib, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum]
    ring
  rw [hext] at h1
  unfold Xrel Yrel
  linear_combination h1

theorem X_of_not_F1 (γ : ℕ → Bool → ℝ) {n : ℕ} (ch : Fin p → Tree p q n) (d : ℕ) (ext : Fin q → ℝ)
    (h : Tiles γ d (.node ch) ext) (hF : ¬ F (.node ch) 1) : Xrel p γ d n = 0 := by
  rw [F_node_one] at hF
  push Not at hF
  obtain ⟨c, c', j, j', hne⟩ := hF
  have e1 := node_rel γ ch d ext h c j
  have e2 := node_rel γ ch d ext h c' j'
  have e3 := node_rel γ ch d ext h c j'
  have e4 := node_rel γ ch d ext h c' j
  have hcoef : ((lay (ch c) j : ℝ) + lay (ch c') j' - lay (ch c) j' - lay (ch c') j)
      * Xrel p γ d n = 0 := by linear_combination e1 + e2 - e3 - e4
  rcases mul_eq_zero.1 hcoef with h0 | h0
  · exfalso
    apply hne
    have : ((lay (ch c) j + lay (ch c') j' : ℕ) : ℝ) = ((lay (ch c) j' + lay (ch c') j : ℕ) : ℝ) := by
      push_cast; linarith
    exact_mod_cast this
  · exact h0

theorem XY_of_not_E1 (γ : ℕ → Bool → ℝ) {n : ℕ} (ch : Fin p → Tree p q n) (d : ℕ) (ext : Fin q → ℝ)
    (h : Tiles γ d (.node ch) ext) (hE : ¬ E (.node ch) 1) :
    Xrel p γ d n + (q : ℝ) * Yrel p γ d n = 0 := by
  rw [E_node_one] at hE
  push Not at hE
  obtain ⟨c, c', hne⟩ := hE
  have hS : ∀ c, (size (ch c) : ℝ) = ∑ w, (lay (ch c) w : ℝ) := fun c => by
    unfold size; push_cast; rfl
  have s1 := Finset.sum_congr (s₁ := (Finset.univ : Finset (Fin q))) rfl
    (fun w _ => node_rel γ ch d ext h c w)
  have s2 := Finset.sum_congr (s₁ := (Finset.univ : Finset (Fin q))) rfl
    (fun w _ => node_rel γ ch d ext h c' w)
  simp only [Finset.sum_add_distrib, ← Finset.sum_mul, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul] at s1 s2
  rw [← hS] at s1 s2
  have hcoef : ((size (ch c) : ℝ) - size (ch c')) * (Xrel p γ d n + (q : ℝ) * Yrel p γ d n) = 0 := by
    linear_combination s1 - s2
  rcases mul_eq_zero.1 hcoef with h0 | h0
  · exfalso
    apply hne
    have : (size (ch c) : ℝ) = size (ch c') := by linarith
    exact_mod_cast this
  · exact h0

/-- if `F` fails at level `ℓ + 1` of a subtree rooted at depth `d`, then `Xrel` vanishes at depth `d + ℓ` -/
theorem X_of_not_F (γ : ℕ → Bool → ℝ) :
    ∀ {n : ℕ} (t : Tree p q n) (d ℓ m : ℕ) (ext : Fin q → ℝ), ℓ + m + 1 = n → Tiles γ d t ext →
      ¬ F t (ℓ + 1) → Xrel p γ (d + ℓ) m = 0
  | _, .leaf _, _, _, _, _, hn, _, _ => by omega
  | _, .node (n := n) ch, d, 0, m, ext, hn, h, hF => by
      obtain rfl : m = n := by omega
      exact X_of_not_F1 γ ch d ext h hF
  | _, .node (n := n) ch, d, ℓ + 1, m, ext, hn, h, hF => by
      rw [F_node_succ] at hF
      push Not at hF
      obtain ⟨c, hc⟩ := hF
      have := X_of_not_F γ (ch c) (d + 1) ℓ m _ (by omega) (h c) hc
      rw [show d + (ℓ + 1) = d + 1 + ℓ by omega]
      exact this

/-- if `E` fails at level `ℓ + 1` of a subtree rooted at depth `d`, then `Xrel + q * Yrel` vanishes at
depth `d + ℓ` -/
theorem XY_of_not_E (γ : ℕ → Bool → ℝ) :
    ∀ {n : ℕ} (t : Tree p q n) (d ℓ m : ℕ) (ext : Fin q → ℝ), ℓ + m + 1 = n → Tiles γ d t ext →
      ¬ E t (ℓ + 1) → Xrel p γ (d + ℓ) m + (q : ℝ) * Yrel p γ (d + ℓ) m = 0
  | _, .leaf _, _, _, _, _, hn, _, _ => by omega
  | _, .node (n := n) ch, d, 0, m, ext, hn, h, hE => by
      obtain rfl : m = n := by omega
      exact XY_of_not_E1 γ ch d ext h hE
  | _, .node (n := n) ch, d, ℓ + 1, m, ext, hn, h, hE => by
      rw [E_node_succ] at hE
      push Not at hE
      obtain ⟨c, hc⟩ := hE
      have := XY_of_not_E γ (ch c) (d + 1) ℓ m _ (by omega) (h c) hc
      rw [show d + (ℓ + 1) = d + 1 + ℓ by omega]
      exact this

/-! ### How the sums of `γ` change from one depth to the next -/

theorem K_succ (γ : ℕ → Bool → ℝ) (d m : ℕ) :
    K p γ d (m + 1) = K p γ (d + 1) m + ((p : ℝ) ^ (m + 1) - (p : ℝ) ^ m) * γ d true := rfl

theorem J_succ (γ : ℕ → Bool → ℝ) (d m : ℕ) :
    J p γ d (m + 1) = J p γ (d + 1) m + ((p : ℝ) ^ (m + 1) - (p : ℝ) ^ m) * γ d false := rfl

theorem pow_step_nonneg (hp : 1 ≤ p) (m : ℕ) : (0 : ℝ) ≤ (p : ℝ) ^ (m + 1) - (p : ℝ) ^ m := by
  have h1 : (1 : ℝ) ≤ p := by exact_mod_cast hp
  have h2 : (0 : ℝ) ≤ (p : ℝ) ^ m := by positivity
  rw [pow_succ]
  nlinarith

theorem K_nonneg (hp : 1 ≤ p) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) :
    ∀ (m d : ℕ), 0 ≤ K p γ d m
  | 0, d => hγ d true
  | m + 1, d => by
      rw [K_succ]
      exact add_nonneg (K_nonneg hp hγ m (d + 1)) (mul_nonneg (pow_step_nonneg hp m) (hγ d true))

theorem J_nonneg (hp : 1 ≤ p) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) :
    ∀ (m d : ℕ), 0 ≤ J p γ d m
  | 0, d => hγ d false
  | m + 1, d => by
      rw [J_succ]
      exact add_nonneg (J_nonneg hp hγ m (d + 1)) (mul_nonneg (pow_step_nonneg hp m) (hγ d false))

theorem G_nonneg (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) (m d : ℕ) :
    0 ≤ G p q γ d m := by
  have hq' : (0 : ℝ) ≤ (q : ℝ) - 1 := by
    have : (1 : ℝ) ≤ q := by exact_mod_cast hq
    linarith
  exact add_nonneg (K_nonneg hp hγ m d) (mul_nonneg hq' (J_nonneg hp hγ m d))

theorem K_mono (hp : 1 ≤ p) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) (d m : ℕ) :
    K p γ (d + 1) m ≤ K p γ d (m + 1) := by
  rw [K_succ]
  linarith [mul_nonneg (pow_step_nonneg hp m) (hγ d true)]

theorem G_mono (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) (d m : ℕ) :
    G p q γ (d + 1) m ≤ G p q γ d (m + 1) := by
  have hq' : (0 : ℝ) ≤ (q : ℝ) - 1 := by
    have : (1 : ℝ) ≤ q := by exact_mod_cast hq
    linarith
  have h1 := mul_nonneg (pow_step_nonneg hp m) (hγ d true)
  have h2 := mul_nonneg hq' (mul_nonneg (pow_step_nonneg hp m) (hγ d false))
  unfold G
  rw [K_succ, J_succ]
  linarith

/-- a level outside `E` multiplies the total by `p` -/
theorem G_mul (γ : ℕ → Bool → ℝ) (d m : ℕ)
    (h : Xrel p γ d m + (q : ℝ) * Yrel p γ d m = 0) :
    G p q γ d (m + 1) = (p : ℝ) * G p q γ (d + 1) m := by
  unfold G
  rw [K_succ, J_succ, pow_succ]
  unfold Xrel Yrel at h
  linear_combination (1 - (p : ℝ)) * h

/-- a level outside `E` and outside `F` multiplies the same-layer sum by `p` -/
theorem K_mul (hq : 1 ≤ q) (γ : ℕ → Bool → ℝ) (d m : ℕ) (hX : Xrel p γ d m = 0)
    (hXY : Xrel p γ d m + (q : ℝ) * Yrel p γ d m = 0) :
    K p γ d (m + 1) = (p : ℝ) * K p γ (d + 1) m := by
  have hq' : (q : ℝ) ≠ 0 := by
    have : (1 : ℝ) ≤ q := by exact_mod_cast hq
    linarith
  have hY : Yrel p γ d m = 0 := by
    have : (q : ℝ) * Yrel p γ d m = 0 := by linarith
    exact (mul_eq_zero.1 this).resolve_left hq'
  rw [K_succ, pow_succ]
  unfold Xrel at hX
  unfold Yrel at hY
  linear_combination (1 - (p : ℝ)) * hX + (1 - (p : ℝ)) * hY

/-- a level in `E` and outside `F`: the total below it is at least `min p q` times the same-layer sum
above it (the clique bound of the note, with no clique) -/
theorem L2_step (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) (d m : ℕ)
    (hX : Xrel p γ d m = 0) :
    ((min p q : ℕ) : ℝ) * K p γ (d + 1) m ≤ G p q γ d (m + 1) := by
  have hJ := J_nonneg hp hγ m (d + 1)
  have hpm : (0 : ℝ) ≤ (p : ℝ) ^ m := by positivity
  have hU : 0 ≤ (p : ℝ) ^ m * γ d false := mul_nonneg hpm (hγ d false)
  have hT : 0 ≤ (p : ℝ) ^ m * γ d true := mul_nonneg hpm (hγ d true)
  have hp1 : (1 : ℝ) ≤ p := by exact_mod_cast hp
  have hq1 : (1 : ℝ) ≤ q := by exact_mod_cast hq
  unfold Xrel at hX
  unfold G
  rw [K_succ, J_succ, pow_succ]
  rcases le_total p q with hpq | hpq
  · rw [min_eq_left hpq]
    have hpq' : (p : ℝ) ≤ q := by exact_mod_cast hpq
    have key : K p γ (d + 1) m + ((p : ℝ) ^ m * p - (p : ℝ) ^ m) * γ d true
        + ((q : ℝ) - 1) * (J p γ (d + 1) m + ((p : ℝ) ^ m * p - (p : ℝ) ^ m) * γ d false)
        - (p : ℝ) * K p γ (d + 1) m
        = ((q : ℝ) - p) * J p γ (d + 1) m + (q : ℝ) * ((p : ℝ) - 1) * ((p : ℝ) ^ m * γ d false) := by
      linear_combination (1 - (p : ℝ)) * hX
    have n1 : 0 ≤ ((q : ℝ) - p) * J p γ (d + 1) m := mul_nonneg (by linarith) hJ
    have n2 : 0 ≤ (q : ℝ) * ((p : ℝ) - 1) * ((p : ℝ) ^ m * γ d false) :=
      mul_nonneg (mul_nonneg (by linarith) (by linarith)) hU
    linarith
  · rw [min_eq_right hpq]
    have hpq' : (q : ℝ) ≤ p := by exact_mod_cast hpq
    have key : K p γ (d + 1) m + ((p : ℝ) ^ m * p - (p : ℝ) ^ m) * γ d true
        + ((q : ℝ) - 1) * (J p γ (d + 1) m + ((p : ℝ) ^ m * p - (p : ℝ) ^ m) * γ d false)
        - (q : ℝ) * K p γ (d + 1) m
        = ((p : ℝ) - q) * ((p : ℝ) ^ m * γ d true) + (p : ℝ) * ((q : ℝ) - 1) * ((p : ℝ) ^ m * γ d false) := by
      linear_combination (1 - (q : ℝ)) * hX
    have n1 : 0 ≤ ((p : ℝ) - q) * ((p : ℝ) ^ m * γ d true) := mul_nonneg (by linarith) hT
    have n2 : 0 ≤ (p : ℝ) * ((q : ℝ) - 1) * ((p : ℝ) ^ m * γ d false) :=
      mul_nonneg (mul_nonneg (by linarith) (by linarith)) hU
    linarith

/-! ### Counting the levels outside `E` -/

open Classical in
/-- the number of levels among `a + 1, …, a + k` at which `E` fails -/
noncomputable def failI {n : ℕ} (t : Tree p q n) (a k : ℕ) : ℕ :=
  ((Finset.range k).filter (fun i => ¬ E t (a + i + 1))).card

theorem failI_zero {n : ℕ} (t : Tree p q n) (a : ℕ) : failI t a 0 = 0 := by
  simp [failI]

open Classical in
theorem failI_succ {n : ℕ} (t : Tree p q n) (a k : ℕ) :
    failI t a (k + 1) = failI t a k + (if E t (a + k + 1) then 0 else 1) := by
  unfold failI
  rw [Finset.range_add_one, Finset.filter_insert]
  by_cases h : E t (a + k + 1)
  · simp [h]
  · simp [h]

theorem failI_split {n : ℕ} (t : Tree p q n) (a : ℕ) (hE : E t (a + 1)) :
    ∀ k, failI t 0 (a + 1 + k) = failI t 0 a + failI t (a + 1) k
  | 0 => by
      classical
      rw [failI_zero, Nat.add_zero, failI_succ]
      simp [hE]
  | k + 1 => by
      classical
      rw [show a + 1 + (k + 1) = (a + 1 + k) + 1 by omega, failI_succ, failI_succ, failI_split t a hE k]
      simp [Nat.add_assoc]

/-- the levels at which `E` fails and those at which it holds make up all of `1..n` -/
theorem fail_total {n : ℕ} (t : Tree p q n) : failI t 0 n + e t = n := by
  classical
  have h1 : ((Finset.range n).filter (fun i => E t (0 + i + 1))).card = e t := by
    unfold e
    rw [← Finset.card_image_of_injective _ (fun a b h => by simpa using h : Function.Injective (· + 1))]
    congr 1
    ext ℓ
    simp only [Finset.mem_image, Finset.mem_filter, Finset.mem_range, mem_eSet]
    constructor
    · rintro ⟨i, ⟨hi, hE⟩, rfl⟩
      exact ⟨by omega, by omega, by simpa using hE⟩
    · rintro ⟨h1, h2, hE⟩
      obtain ⟨i, rfl⟩ : ∃ i, ℓ = i + 1 := ⟨ℓ - 1, by omega⟩
      exact ⟨i, ⟨by omega, by simpa using hE⟩, rfl⟩
  have h2 := Finset.card_filter_add_card_filter_not (s := Finset.range n)
    (fun i => E t (0 + i + 1))
  rw [Finset.card_range] at h2
  unfold failI
  omega

/-! ### Chains of inequalities down the levels -/

theorem G_chain (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) {n : ℕ}
    (t : Tree p q n) (hT : Tiles γ 0 t (fun _ => 0)) :
    ∀ k m, k + m = n → (p : ℝ) ^ failI t 0 k * G p q γ k m ≤ G p q γ 0 n
  | 0, m, h => by
      obtain rfl : m = n := by omega
      simp [failI_zero]
  | k + 1, m, h => by
      classical
      have ih := G_chain hp hq hγ t hT k (m + 1) (by omega)
      have hpk : (0 : ℝ) ≤ (p : ℝ) ^ failI t 0 k := by positivity
      rw [failI_succ]
      by_cases hE : E t (0 + k + 1)
      · simp only [hE, ↓reduceIte, add_zero]
        exact le_trans (mul_le_mul_of_nonneg_left (G_mono hp hq hγ k m) hpk) ih
      · simp only [hE, ↓reduceIte]
        have hrel := XY_of_not_E γ t 0 k m _ (by omega) hT (by simpa using hE)
        rw [Nat.zero_add] at hrel
        have hmul := G_mul γ k m hrel
        calc (p : ℝ) ^ (failI t 0 k + 1) * G p q γ (k + 1) m
            = (p : ℝ) ^ failI t 0 k * ((p : ℝ) * G p q γ (k + 1) m) := by ring
          _ = (p : ℝ) ^ failI t 0 k * G p q γ k (m + 1) := by rw [hmul]
          _ ≤ G p q γ 0 n := ih

theorem K_chain (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) {n : ℕ}
    (t : Tree p q n) (hT : Tiles γ 0 t (fun _ => 0)) (a : ℕ)
    (hFE : ∀ i, a ≤ i → F t (i + 1) → E t (i + 1)) :
    ∀ k m, a + k + m = n → (p : ℝ) ^ failI t a k * K p γ (a + k) m ≤ K p γ a (k + m)
  | 0, m, _ => by
      simp [failI_zero]
  | k + 1, m, h => by
      classical
      have ih := K_chain hp hq hγ t hT a hFE k (m + 1) (by omega)
      rw [show k + (m + 1) = k + 1 + m by omega] at ih
      have hpk : (0 : ℝ) ≤ (p : ℝ) ^ failI t a k := by positivity
      rw [failI_succ]
      by_cases hE : E t (a + k + 1)
      · simp only [hE, ↓reduceIte, add_zero]
        exact le_trans (mul_le_mul_of_nonneg_left (K_mono hp hγ (a + k) m) hpk) ih
      · simp only [hE, ↓reduceIte]
        have hF : ¬ F t (a + k + 1) := fun hF => hE (hFE (a + k) (by omega) hF)
        have hX := X_of_not_F γ t 0 (a + k) m _ (by omega) hT hF
        have hXY := XY_of_not_E γ t 0 (a + k) m _ (by omega) hT hE
        rw [Nat.zero_add] at hX hXY
        have hmul := K_mul hq γ (a + k) m hX hXY
        calc (p : ℝ) ^ (failI t a k + 1) * K p γ (a + (k + 1)) m
            = (p : ℝ) ^ failI t a k * ((p : ℝ) * K p γ (a + k + 1) m) := by ring
          _ = (p : ℝ) ^ failI t a k * K p γ (a + k) (m + 1) := by rw [hmul]
          _ ≤ K p γ a (k + 1 + m) := ih

/-! ### The three bounds of the note, from a step complement -/

theorem total_eq {γ : ℕ → Bool → ℝ} {n : ℕ} {t : Tree p q n} (h : Tiles γ 0 t (fun _ => 0)) :
    (size t : ℝ) * G p q γ 0 n = (q : ℝ) * (p : ℝ) ^ n := by
  have := tiles_sum γ t 0 (fun _ => 0) h
  simpa using this

theorem K_top (γ : ℕ → Bool → ℝ) (d : ℕ) : K p γ d 0 = γ d true := rfl

theorem G_top (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} (hγ : ∀ d b, 0 ≤ γ d b) {n : ℕ}
    (h1 : γ n true = 1) : 1 ≤ G p q γ n 0 := by
  have hq' : (0 : ℝ) ≤ (q : ℝ) - 1 := by
    have : (1 : ℝ) ≤ q := by exact_mod_cast hq
    linarith
  have hJ : J p γ n 0 = γ n false := rfl
  unfold G
  rw [K_top, hJ, h1]
  linarith [mul_nonneg hq' (hγ n false)]

theorem step_size_pos (hp : 0 < p) (hq : 0 < q) {γ : ℕ → Bool → ℝ} {n : ℕ} {t : Tree p q n}
    (hT : Tiles γ 0 t (fun _ => 0)) : 0 < size t := by
  by_contra hcon
  have hz : size t = 0 := by omega
  have h := total_eq hT
  have hpos : (0 : ℝ) < (q : ℝ) * (p : ℝ) ^ n :=
    mul_pos (by exact_mod_cast hq) (pow_pos (by exact_mod_cast hp) n)
  rw [hz] at h
  simp only [Nat.cast_zero, zero_mul] at h
  linarith

/-- **(U1)** `|A| ≤ p^e q`. -/
theorem step_U1 (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} {n : ℕ} {t : Tree p q n}
    (hst : StepTiling γ t) : size t ≤ p ^ e t * q := by
  obtain ⟨hγ, h1, hT⟩ := hst
  have hsum := total_eq hT
  have hch := G_chain hp hq hγ t hT n 0 (by omega)
  have htop := G_top (p := p) hq hγ h1
  have hfe := fail_total t
  have hpf : (0 : ℝ) < (p : ℝ) ^ failI t 0 n := pow_pos (by exact_mod_cast hp) _
  have hsz : (0 : ℝ) ≤ (size t : ℝ) := Nat.cast_nonneg _
  have hG : (p : ℝ) ^ failI t 0 n ≤ G p q γ 0 n := by nlinarith
  have hpn : (p : ℝ) ^ n = (p : ℝ) ^ failI t 0 n * (p : ℝ) ^ e t := by rw [← pow_add, hfe]
  have key : (size t : ℝ) * (p : ℝ) ^ failI t 0 n
      ≤ ((p : ℝ) ^ e t * q) * (p : ℝ) ^ failI t 0 n := by
    calc (size t : ℝ) * (p : ℝ) ^ failI t 0 n ≤ (size t : ℝ) * G p q γ 0 n :=
          mul_le_mul_of_nonneg_left hG hsz
      _ = (q : ℝ) * (p : ℝ) ^ n := hsum
      _ = ((p : ℝ) ^ e t * q) * (p : ℝ) ^ failI t 0 n := by rw [hpn]; ring
  have := le_of_mul_le_mul_right key hpf
  exact_mod_cast this

/-- **(U2)** if `Φ_q ∤ A` and every level in `F` is in `E`, then `|A| ≤ p^e`. -/
theorem step_U2 (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} {n : ℕ} {t : Tree p q n}
    (hst : StepTiling γ t) (h0 : ¬ F t 0) (hFE : ∀ ℓ, F t (ℓ + 1) → E t (ℓ + 1)) :
    size t ≤ p ^ e t := by
  obtain ⟨hγ, h1, hT⟩ := hst
  have hsum := total_eq hT
  have hch := K_chain hp hq hγ t hT 0 (fun i _ hF => hFE i hF) n 0 (by omega)
  simp only [Nat.zero_add, Nat.add_zero] at hch
  have hKtop : K p γ n 0 = 1 := h1
  rw [hKtop, mul_one] at hch
  -- the layer counts are not all equal, so the same-layer sum equals the other-layer sum
  rw [F_zero] at h0
  push Not at h0
  obtain ⟨j, j', hne⟩ := h0
  have r1 := tiles_layer_sum γ t 0 _ hT j
  have r2 := tiles_layer_sum γ t 0 _ hT j'
  simp only [mul_zero, zero_add] at r1 r2
  have hKJ : K p γ 0 n = J p γ 0 n := by
    have hc : ((lay t j : ℝ) - lay t j') * (K p γ 0 n - J p γ 0 n) = 0 := by
      linear_combination r1 - r2
    rcases mul_eq_zero.1 hc with h | h
    · exfalso
      apply hne
      have : (lay t j : ℝ) = lay t j' := by linarith
      exact_mod_cast this
    · linarith
  have hG : G p q γ 0 n = (q : ℝ) * K p γ 0 n := by
    unfold G
    rw [← hKJ]
    ring
  have hq' : (0 : ℝ) < q := by exact_mod_cast hq
  have hsK : (size t : ℝ) * K p γ 0 n = (p : ℝ) ^ n := by
    have : (q : ℝ) * ((size t : ℝ) * K p γ 0 n) = (q : ℝ) * (p : ℝ) ^ n := by
      rw [← hsum, hG]; ring
    exact mul_left_cancel₀ hq'.ne' this
  have hfe := fail_total t
  have hpf : (0 : ℝ) < (p : ℝ) ^ failI t 0 n := pow_pos (by exact_mod_cast hp) _
  have hsz : (0 : ℝ) ≤ (size t : ℝ) := Nat.cast_nonneg _
  have hpn : (p : ℝ) ^ n = (p : ℝ) ^ failI t 0 n * (p : ℝ) ^ e t := by rw [← pow_add, hfe]
  have key : (size t : ℝ) * (p : ℝ) ^ failI t 0 n ≤ (p : ℝ) ^ e t * (p : ℝ) ^ failI t 0 n := by
    calc (size t : ℝ) * (p : ℝ) ^ failI t 0 n ≤ (size t : ℝ) * K p γ 0 n :=
          mul_le_mul_of_nonneg_left hch hsz
      _ = (p : ℝ) ^ n := hsK
      _ = (p : ℝ) ^ e t * (p : ℝ) ^ failI t 0 n := by rw [hpn]; ring
  have := le_of_mul_le_mul_right key hpf
  exact_mod_cast this

/-- **(L2)** if `Φ_q ∣ A`, a level `a + 1` is in `E` and not in `F`, and above it `E` and `F` agree,
then `|A| · min p q ≤ p^e q`. -/
theorem step_L2 (hp : 1 ≤ p) (hq : 1 ≤ q) {γ : ℕ → Bool → ℝ} {n : ℕ} {t : Tree p q n}
    (hst : StepTiling γ t) (a : ℕ) (hEa : E t (a + 1)) (hFa : ¬ F t (a + 1))
    (hagree : ∀ ℓ, a < ℓ → (E t (ℓ + 1) ↔ F t (ℓ + 1))) :
    size t * min p q ≤ p ^ e t * q := by
  obtain ⟨hγ, h1, hT⟩ := hst
  have hrange := (E_range (Nat.lt_of_lt_of_le Nat.zero_lt_one hp) t (a + 1) hEa).2
  obtain ⟨m₁, hm⟩ : ∃ m₁, a + 1 + m₁ = n := ⟨n - (a + 1), by omega⟩
  have hsum := total_eq hT
  -- above level a + 1: the same-layer sum
  have htop := K_chain hp hq hγ t hT (a + 1) (fun i hi hF => (hagree i (by omega)).2 hF) m₁ 0
    (by omega)
  have hKn : K p γ (a + 1 + m₁) 0 = 1 := by rw [hm]; exact h1
  rw [hKn, mul_one, Nat.add_zero] at htop
  -- at level a + 1
  have hX := X_of_not_F γ t 0 a m₁ _ (by omega) hT hFa
  rw [Nat.zero_add] at hX
  have hmid := L2_step hp hq hγ a m₁ hX
  -- below level a + 1: the total
  have hbot := G_chain hp hq hγ t hT a (m₁ + 1) (by omega)
  -- the levels outside E
  have hsplit := failI_split t a hEa m₁
  rw [hm] at hsplit
  have hfe := fail_total t
  have hp0 : (0 : ℝ) < (p : ℝ) := by exact_mod_cast hp
  have hf0 : (0 : ℝ) ≤ (p : ℝ) ^ failI t 0 a := (pow_pos hp0 _).le
  have hμ : (0 : ℝ) ≤ ((min p q : ℕ) : ℝ) := Nat.cast_nonneg _
  have hG : ((min p q : ℕ) : ℝ) * ((p : ℝ) ^ failI t 0 a * (p : ℝ) ^ failI t (a + 1) m₁)
      ≤ G p q γ 0 n := by
    calc ((min p q : ℕ) : ℝ) * ((p : ℝ) ^ failI t 0 a * (p : ℝ) ^ failI t (a + 1) m₁)
        = (p : ℝ) ^ failI t 0 a * (((min p q : ℕ) : ℝ) * (p : ℝ) ^ failI t (a + 1) m₁) := by ring
      _ ≤ (p : ℝ) ^ failI t 0 a * (((min p q : ℕ) : ℝ) * K p γ (a + 1) m₁) :=
          mul_le_mul_of_nonneg_left (mul_le_mul_of_nonneg_left htop hμ) hf0
      _ ≤ (p : ℝ) ^ failI t 0 a * G p q γ a (m₁ + 1) := mul_le_mul_of_nonneg_left hmid hf0
      _ ≤ G p q γ 0 n := hbot
  have hpf : (0 : ℝ) < (p : ℝ) ^ failI t 0 n := pow_pos hp0 _
  have hsz : (0 : ℝ) ≤ (size t : ℝ) := Nat.cast_nonneg _
  have hpn : (p : ℝ) ^ n = (p : ℝ) ^ failI t 0 n * (p : ℝ) ^ e t := by rw [← pow_add, hfe]
  have hpff : (p : ℝ) ^ failI t 0 n = (p : ℝ) ^ failI t 0 a * (p : ℝ) ^ failI t (a + 1) m₁ := by
    rw [hsplit, pow_add]
  have key : ((size t : ℝ) * ((min p q : ℕ) : ℝ)) * (p : ℝ) ^ failI t 0 n
      ≤ ((p : ℝ) ^ e t * q) * (p : ℝ) ^ failI t 0 n := by
    calc ((size t : ℝ) * ((min p q : ℕ) : ℝ)) * (p : ℝ) ^ failI t 0 n
        = (size t : ℝ) * (((min p q : ℕ) : ℝ) * ((p : ℝ) ^ failI t 0 a * (p : ℝ) ^ failI t (a + 1) m₁)) := by
          rw [hpff]; ring
      _ ≤ (size t : ℝ) * G p q γ 0 n := mul_le_mul_of_nonneg_left hG hsz
      _ = (q : ℝ) * (p : ℝ) ^ n := hsum
      _ = ((p : ℝ) ^ e t * q) * (p : ℝ) ^ failI t 0 n := by rw [hpn]; ring
  have := le_of_mul_le_mul_right key hpf
  exact_mod_cast this

open Classical in
/-- **A set with a step weak-tiling complement satisfies (T1) and (T2).**  The size is `p^e`, times `q`
if `Φ_q ∣ A`; and if `Φ_q ∣ A` then every level in `E` is in `F`. -/
theorem step_structure (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} (t : Tree p q n)
    (γ : ℕ → Bool → ℝ) (hst : StepTiling γ t) :
    size t = p ^ e t * (if F t 0 then q else 1) ∧ (F t 0 → ∀ ℓ, E t (ℓ + 1) → F t (ℓ + 1)) :=
  counting hp hq hpq t (step_size_pos (by omega) (by omega) hst.2.2)
    (step_U1 (by omega) (by omega) hst)
    (fun h0 hFE => step_U2 (by omega) (by omega) hst h0 hFE)
    (fun _ a hEa hFa hag => step_L2 (by omega) (by omega) hst a hEa hFa hag)

/-! ### The interface, in the form asked for by the group side (Noon, `lean-pnq-group/`) -/

/-- `Tiles` at a leaf, unfolded -/
theorem Tiles_leaf (γ : ℕ → Bool → ℝ) (d : ℕ) (f : Fin q → ℕ) (ext : Fin q → ℝ) :
    Tiles γ d (Tree.leaf (p := p) f) ext ↔
      ∀ w, ext w + γ d true * (f w : ℝ) + γ d false * ((∑ j, (f j : ℝ)) - (f w : ℝ)) = 1 := Iff.rfl

/-- `Tiles` at a node, with `extChild` and `sib` unfolded -/
theorem Tiles_node (γ : ℕ → Bool → ℝ) (d : ℕ) {n : ℕ} (ch : Fin p → Tree p q n) (ext : Fin q → ℝ) :
    Tiles γ d (Tree.node ch) ext ↔
      ∀ c, Tiles γ (d + 1) (ch c) (fun w => ext w + ∑ c' ∈ Finset.univ.erase c,
        (γ d true * (lay (ch c') w : ℝ) + γ d false * ((size (ch c') : ℝ) - (lay (ch c') w : ℝ)))) :=
  Iff.rfl

/-- **The three hypotheses of `counting`, from a step complement.** -/
theorem bounds_of_stepTiling (hp : 2 ≤ p) (hq : 2 ≤ q) {n : ℕ} (t : Tree p q n) (γ : ℕ → Bool → ℝ)
    (h : StepTiling γ t) :
    0 < size t ∧ size t ≤ p ^ e t * q ∧
    (¬ F t 0 → (∀ ℓ, F t (ℓ + 1) → E t (ℓ + 1)) → size t ≤ p ^ e t) ∧
    (F t 0 → ∀ a, E t (a + 1) → ¬ F t (a + 1) →
      (∀ ℓ, a < ℓ → (E t (ℓ + 1) ↔ F t (ℓ + 1))) → size t * min p q ≤ p ^ e t * q) :=
  ⟨step_size_pos (by omega) (by omega) h.2.2, step_U1 (by omega) (by omega) h,
    fun h0 hFE => step_U2 (by omega) (by omega) h h0 hFE,
    fun _ a hEa hFa hag => step_L2 (by omega) (by omega) h a hEa hFa hag⟩

end Pnq
