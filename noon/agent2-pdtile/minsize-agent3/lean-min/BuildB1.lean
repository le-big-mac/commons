/-
Tools for `Pnq/BuildB.lean` (the constructions for the half with `Φ_q ∣ A`), part 1: sums over `Fin p`,
powers of `p` counted along the levels, nodes with one special child, and the fibre trees of Theorem A.
-/
import Pnq.Rule

open Finset

namespace Pnq
namespace BuildB

variable {p q : ℕ}

/-! ### Sums over `Fin p` -/

theorem sum_ite_zero (hp : 0 < p) (A B : ℕ) :
    ∑ x : Fin p, (if x.val = 0 then A else B) = A + (p - 1) * B := by
  obtain ⟨m, rfl⟩ : ∃ m, p = m + 1 := ⟨p - 1, by omega⟩
  rw [Fin.sum_univ_succ]
  simp

theorem sum_ite_zero_one (hp : 2 ≤ p) (A B D : ℕ) :
    ∑ x : Fin p, (if x.val = 0 then A else if x.val = 1 then B else D) = A + B + (p - 2) * D := by
  obtain ⟨m, rfl⟩ : ∃ m, p = m + 2 := ⟨p - 2, by omega⟩
  rw [Fin.sum_univ_succ, Fin.sum_univ_succ]
  simp
  omega

theorem add_pred_mul (hp : 0 < p) (X : ℕ) : X + (p - 1) * X = p * X := by
  have h : p - 1 + 1 = p := by omega
  calc X + (p - 1) * X = (p - 1 + 1) * X := by ring
    _ = p * X := by rw [h]

/-! ### `pw p S k d`: the power of `p` whose exponent is the number of levels of `S` in `(d, d + k]` -/

/-- `p ^ #(S ∩ (d, d + k])`, by recursion on `k` -/
def pw (p : ℕ) (S : Finset ℕ) : ℕ → ℕ → ℕ
  | 0, _ => 1
  | k + 1, d => (if d + 1 ∈ S then p else 1) * pw p S k (d + 1)

theorem pw_succ_mem {S : Finset ℕ} {d : ℕ} (k : ℕ) (h : d + 1 ∈ S) :
    pw p S (k + 1) d = p * pw p S k (d + 1) := by
  simp [pw, h]

theorem pw_succ_not {S : Finset ℕ} {d : ℕ} (k : ℕ) (h : d + 1 ∉ S) :
    pw p S (k + 1) d = pw p S k (d + 1) := by
  simp [pw, h]

theorem pw_pos (hp : 0 < p) (S : Finset ℕ) : ∀ k d, 0 < pw p S k d
  | 0, _ => Nat.one_pos
  | k + 1, d => by
      rw [pw]
      exact Nat.mul_pos (by split_ifs <;> omega) (pw_pos hp S k (d + 1))

theorem pw_eq (S : Finset ℕ) :
    ∀ k d, pw p S k d = p ^ (S.filter (fun a => d < a ∧ a ≤ d + k)).card
  | 0, d => by
      have h : S.filter (fun a => d < a ∧ a ≤ d + 0) = ∅ := by
        apply Finset.filter_eq_empty_iff.2
        intro a _
        omega
      rw [h]
      rfl
  | k + 1, d => by
      rw [pw, pw_eq S k (d + 1)]
      by_cases h : d + 1 ∈ S
      · have h' : S.filter (fun a => d < a ∧ a ≤ d + (k + 1)) =
            insert (d + 1) (S.filter (fun a => d + 1 < a ∧ a ≤ d + 1 + k)) := by
          ext a
          simp only [Finset.mem_filter, Finset.mem_insert]
          constructor
          · rintro ⟨ha, h1, h2⟩
            by_cases hh : a = d + 1
            · left; exact hh
            · right; exact ⟨ha, by omega, by omega⟩
          · rintro (rfl | ⟨ha, h1, h2⟩)
            · exact ⟨h, by omega, by omega⟩
            · exact ⟨ha, by omega, by omega⟩
        rw [h', Finset.card_insert_of_notMem (by simp), ite_eq_left h, pow_succ]
        ring
      · have h' : S.filter (fun a => d < a ∧ a ≤ d + (k + 1)) =
            S.filter (fun a => d + 1 < a ∧ a ≤ d + 1 + k) := by
          ext a
          simp only [Finset.mem_filter]
          constructor
          · rintro ⟨ha, h1, h2⟩
            refine ⟨ha, ?_, by omega⟩
            by_contra hc
            have hh : a = d + 1 := by omega
            exact h (hh ▸ ha)
          · rintro ⟨ha, h1, h2⟩
            exact ⟨ha, by omega, by omega⟩
        rw [h', ite_eq_right h, one_mul]

/-- for a set of levels in `1..n`, `pw` from the root is `p ^ |S|` -/
theorem pw_root {S : Finset ℕ} {n : ℕ} (hS : S ⊆ Finset.Icc 1 n) : pw p S n 0 = p ^ S.card := by
  rw [pw_eq]
  congr 2
  apply Finset.filter_true_of_mem
  intro a ha
  have := Finset.mem_Icc.1 (hS ha)
  omega

/-! ### A node whose children other than the first are all the same -/

/-- the node with first child `A` and all other children `B` -/
def two {k : ℕ} (A B : Tree p q k) : Tree p q (k + 1) := .node (fun x => if x.val = 0 then A else B)

theorem lay_two (hp : 0 < p) {k : ℕ} (A B : Tree p q k) (j : Fin q) :
    lay (two A B) j = lay A j + (p - 1) * lay B j := by
  unfold two
  rw [lay_node, ← sum_ite_zero hp]
  exact Finset.sum_congr rfl (fun x _ => by split_ifs <;> rfl)

theorem size_two (hp : 0 < p) {k : ℕ} (A B : Tree p q k) :
    size (two A B) = size A + (p - 1) * size B := by
  unfold two
  rw [size_node, ← sum_ite_zero hp]
  exact Finset.sum_congr rfl (fun x _ => by split_ifs <;> rfl)

theorem E_two_one (hp : 2 ≤ p) {k : ℕ} (A B : Tree p q k) : E (two A B) 1 ↔ size A = size B := by
  unfold two
  rw [E_node_one]
  constructor
  · intro h
    have := h ⟨0, by omega⟩ ⟨1, by omega⟩
    simpa using this
  · intro h c c'
    split_ifs <;> simp [h]

theorem E_two_succ (hp : 2 ≤ p) {k : ℕ} (A B : Tree p q k) (ℓ : ℕ) :
    E (two A B) (ℓ + 2) ↔ E A (ℓ + 1) ∧ E B (ℓ + 1) := by
  unfold two
  rw [E_node_succ]
  constructor
  · intro h
    have h0 := h ⟨0, by omega⟩
    have h1 := h ⟨1, by omega⟩
    simp only [↓reduceIte, one_ne_zero] at h0 h1
    exact ⟨h0, h1⟩
  · rintro ⟨hA, hB⟩ c
    split_ifs <;> assumption

theorem F_two_one (hp : 2 ≤ p) {k : ℕ} (A B : Tree p q k) :
    F (two A B) 1 ↔ ∀ j j', lay A j + lay B j' = lay A j' + lay B j := by
  unfold two
  rw [F_node_one]
  constructor
  · intro h j j'
    have := h ⟨0, by omega⟩ ⟨1, by omega⟩ j j'
    simpa using this
  · intro h c c' j j'
    have := h j j'
    split_ifs <;> omega

theorem F_two_succ (hp : 2 ≤ p) {k : ℕ} (A B : Tree p q k) (ℓ : ℕ) :
    F (two A B) (ℓ + 2) ↔ F A (ℓ + 1) ∧ F B (ℓ + 1) := by
  unfold two
  rw [F_node_succ]
  constructor
  · intro h
    have h0 := h ⟨0, by omega⟩
    have h1 := h ⟨1, by omega⟩
    simp only [↓reduceIte, one_ne_zero] at h0 h1
    exact ⟨h0, h1⟩
  · rintro ⟨hA, hB⟩ c
    split_ifs <;> assumption

theorem size_of_lay_const {k : ℕ} (t : Tree p q k) (v : ℕ) (h : ∀ j, lay t j = v) : size t = q * v := by
  unfold size
  rw [Finset.sum_congr rfl (fun j _ => h j), Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    smul_eq_mul]

/-! ### The fibre trees (Theorem A) -/

/-- the empty tree -/
def emp : (k : ℕ) → Tree p q k
  | 0 => .leaf (fun _ => 0)
  | k + 1 => two (emp k) (emp k)

theorem lay_emp (hp : 0 < p) : ∀ (k : ℕ) (j : Fin q), lay (emp (p := p) k) j = 0
  | 0, _ => rfl
  | k + 1, j => by
      rw [emp, lay_two hp, lay_emp hp k j]
      simp

theorem size_emp (hp : 0 < p) (k : ℕ) : size (emp (p := p) (q := q) k) = 0 := by
  rw [size_of_lay_const _ 0 (lay_emp hp k)]
  simp

/-- one element in every layer over every string that is `0` at the levels outside `T`; the subtree at depth
`d` with `k` levels below it -/
def fib (T : Finset ℕ) : (k d : ℕ) → Tree p q k
  | 0, _ => .leaf (fun _ => 1)
  | k + 1, d =>
      if d + 1 ∈ T then two (fib T k (d + 1)) (fib T k (d + 1)) else two (fib T k (d + 1)) (emp k)

theorem lay_fib (hp : 0 < p) (T : Finset ℕ) :
    ∀ (k d : ℕ) (j : Fin q), lay (fib (p := p) T k d) j = pw p T k d
  | 0, _, _ => rfl
  | k + 1, d, j => by
      rw [fib]
      split_ifs with h
      · rw [lay_two hp, lay_fib hp T k (d + 1) j, pw_succ_mem k h, add_pred_mul hp]
      · rw [lay_two hp, lay_fib hp T k (d + 1) j, lay_emp hp, pw_succ_not k h]
        simp

theorem size_fib (hp : 0 < p) (T : Finset ℕ) (k d : ℕ) :
    size (fib (p := p) (q := q) T k d) = q * pw p T k d :=
  size_of_lay_const _ _ (lay_fib hp T k d)

theorem E_fib (hp : 2 ≤ p) (hq : 0 < q) (T : Finset ℕ) :
    ∀ (k d ℓ : ℕ), 1 ≤ ℓ → ℓ ≤ k → (E (fib (p := p) (q := q) T k d) ℓ ↔ d + ℓ ∈ T)
  | 0, _, ℓ, h1, h2 => by omega
  | k + 1, d, 0, h1, _ => by omega
  | k + 1, d, 1, _, _ => by
      rw [fib]
      split_ifs with h
      · rw [E_two_one hp]
        exact iff_of_true rfl h
      · rw [E_two_one hp, size_emp (by omega), size_fib (by omega)]
        have := pw_pos (p := p) (by omega) T k (d + 1)
        have := Nat.mul_pos hq this
        exact iff_of_false (by omega) h
  | k + 1, d, ℓ + 2, _, h2 => by
      have ih := E_fib hp hq T k (d + 1) (ℓ + 1) (by omega) (by omega)
      have e : d + 1 + (ℓ + 1) = d + (ℓ + 2) := by omega
      rw [e] at ih
      rw [fib]
      split_ifs with h
      · rw [E_two_succ hp, ih, and_self]
      · rw [E_two_succ hp, ih]
        exact and_iff_left (E_of_empty _ _ (size_emp (by omega) k) (by omega) (by omega))

theorem F_fib (hp : 2 ≤ p) (T : Finset ℕ) :
    ∀ (k d ℓ : ℕ), ℓ ≤ k → F (fib (p := p) (q := q) T k d) ℓ
  | k, d, 0, _ => by
      rw [F_zero]
      intro j j'
      rw [lay_fib (by omega), lay_fib (by omega)]
  | 0, _, ℓ + 1, h => by omega
  | k + 1, d, 1, _ => by
      rw [fib]
      split_ifs with h
      · rw [F_two_one hp]
        intro j j'
        rw [lay_fib (by omega), lay_fib (by omega)]
      · rw [F_two_one hp]
        intro j j'
        rw [lay_fib (by omega), lay_fib (by omega), lay_emp (by omega), lay_emp (by omega)]
  | k + 1, d, ℓ + 2, h2 => by
      have ih := F_fib hp T k (d + 1) (ℓ + 1) (by omega)
      rw [fib]
      split_ifs with h
      · rw [F_two_succ hp]
        exact ⟨ih, ih⟩
      · rw [F_two_succ hp]
        exact ⟨ih, F_of_empty _ _ (size_emp (by omega) k) (by omega)⟩

end BuildB
end Pnq
