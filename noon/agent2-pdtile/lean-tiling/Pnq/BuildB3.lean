/-
Tools for `Pnq/BuildB.lean`, part 3: the pattern and the size of the tree `bld C n 0 true i0 true c0`, under
the hypotheses `Good C n c0` on the data `C` (which part 4 checks for the vectors actually used).
-/
import Pnq.BuildB2

open Finset

namespace Pnq
namespace BuildB

variable {p q : ℕ}

/-- the total of a string of the shape part, as seen from depth `d`: above `a0` the classes are balanced and
the totals come in multiples of `q`; from `a0` on the total is `r i` for the digit `i` at level `a0` -/
def Cfg.R (C : Cfg p q) (d : ℕ) (i : Fin p) : ℕ := if d < C.a0 then q else C.r i

/-- what is asked of the vectors `vec i s` and their totals `r i` -/
structure VecOK (C : Cfg p q) : Prop where
  hV1 : ∀ i s, ∑ j, C.vec i s j = C.r i
  hcol : ∀ s j j', ∑ x, C.vec x s j = ∑ x, C.vec x s j'
  hr0 : ∀ x : Fin p, x.val = 0 → 1 ≤ C.r x
  hNC : ∀ x : Fin p, x.val = 0 → ∀ a b e, Nat.Coprime (a + b) q → ¬ ∀ j j',
    a * C.vec x false j + b * C.vec x true j + e = a * C.vec x false j' + b * C.vec x true j' + e
  hN2 : ∀ x : Fin p, x.val = 0 → ∀ D W e, 1 ≤ W → ¬ ∀ j j',
    (D * C.vec x false j + W * C.vec x false j + e) + (D * C.vec x false j' + W * C.vec x true j' + e)
      = (D * C.vec x false j' + W * C.vec x false j' + e) + (D * C.vec x false j + W * C.vec x true j + e)
  hN1 : ∀ x y : Fin p, x.val = 0 → y.val = 1 → ∀ a b e e', Nat.Coprime (a + b) q → ¬ ∀ j j',
    (a * C.vec x false j + b * C.vec x true j + e) + (a * C.vec y false j' + b * C.vec y true j' + e')
      = (a * C.vec x false j' + b * C.vec x true j' + e) + (a * C.vec y false j + b * C.vec y true j + e')

/-- what is asked of the data of a construction; `c0` is the multiplicity of the superposed fibres -/
structure Good (C : Cfg p q) (n c0 : ℕ) : Prop extends VecOK C where
  hp : 2 ≤ p
  hq : 2 ≤ q
  hpq : Nat.Coprime p q
  ha1 : 1 ≤ C.a0
  han : C.a0 ≤ n
  hna : C.a0 ∉ C.Fs
  hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < C.a0 → ℓ ∈ C.Fs
  host : C.hb = 0 ∨ (C.hb ∈ C.Es ∧ C.hb ≠ C.a0 ∧
    (∀ k, C.hb + k = n → pw p C.U k C.hb = C.M * pw p C.Es k C.hb) ∧
    (C.a0 < C.hb → C.hb ∉ C.Fs ∧ ∀ i, C.r i = q))
  hex0 : ∀ x : Fin p, x.val = 0 → C.ex x = 0
  hmidS : ∀ k d, d + 1 = C.a0 → d + 1 + k = n →
    ∑ x, (C.r x * pw p C.U k (d + 1) + q * (C.ex x * pw p C.Es k (d + 1))) = q * pw p C.U (k + 1) d
  hmidE : C.a0 ∈ C.Es → ∀ k, C.a0 + k = n → ∀ x x',
    C.r x * pw p C.U k C.a0 + q * (C.ex x * pw p C.Es k C.a0)
      = C.r x' * pw p C.U k C.a0 + q * (C.ex x' * pw p C.Es k C.a0)
  hmidF : C.a0 ∉ C.Es → ∀ k, C.a0 + k = n → ¬ ∀ x x' : Fin p,
    C.r x * pw p C.U k C.a0 + q * (((if x.val = 0 then c0 else 0) + C.ex x) * pw p C.Es k C.a0)
      = C.r x' * pw p C.U k C.a0 + q * (((if x'.val = 0 then c0 else 0) + C.ex x') * pw p C.Es k C.a0)
  hG : ∀ g, g ∈ C.U → g ∉ C.Es → 1 ≤ c0 ∨ (C.hb ≠ 0 ∧ C.hb < g ∧ 1 ≤ C.M) ∨ ∃ x, 1 ≤ C.ex x

namespace Good

variable {C : Cfg p q} {n c0 : ℕ}

theorem hp0 (G : Good C n c0) : 0 < p := by have := G.hp; omega

theorem hh (G : Good C n c0) : C.hb = 0 ∨ C.hb ∈ C.Es := by
  rcases G.host with h | h
  · exact Or.inl h
  · exact Or.inr h.1

theorem hne (G : Good C n c0) : C.hb ≠ C.a0 := by
  rcases G.host with h | h
  · have := G.ha1; omega
  · exact h.2.1

theorem host_mem (G : Good C n c0) {d : ℕ} (h1 : d + 1 = C.hb) : d + 1 ∈ C.Es := by
  rcases G.host with h | h
  · omega
  · rw [h1]; exact h.1

theorem host_pw (G : Good C n c0) {d k : ℕ} (h1 : d + 1 = C.hb) (hk : d + 1 + k = n) :
    pw p C.U k (d + 1) = C.M * pw p C.Es k (d + 1) := by
  rcases G.host with h | h
  · omega
  · rw [h1]; exact h.2.2.1 k (by omega)

theorem host_R (G : Good C n c0) {d : ℕ} (h1 : d + 1 = C.hb) (i : Fin p) (d' : ℕ)
    (hd' : d' = d ∨ d' = d + 1) : C.R d' i = q := by
  unfold Cfg.R
  split_ifs with hlt
  · rfl
  · rcases G.host with h | h
    · omega
    · have := h.2.1
      exact (h.2.2.2 (by omega)).2 i

end Good

/-! ### Classes of depth `< a0` are balanced -/

theorem lay_two_congr (hp : 0 < p) {k : ℕ} (A B : Tree p q k) (j j' : Fin q)
    (hA : lay A j = lay A j') (hB : lay B j = lay B j') : lay (two A B) j = lay (two A B) j' := by
  rw [lay_two hp, lay_two hp, hA, hB]

theorem lay_bld_above {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) (j j' : Fin q) :
    ∀ (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ), d + k = n → d < C.a0 →
      lay (bld C k d z i s c) j = lay (bld C k d z i s c) j' := by
  have hp := G.hp0
  intro k
  induction k with
  | zero => intro d z i s c h1 h2; have := G.han; omega
  | succ k ih =>
    intro d z i s c hdk hd
    have hne := G.hne
    rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
      ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
    · rw [e]
      exact lay_two_congr hp _ _ j j' (ih (d + 1) _ _ _ _ (by omega) (by omega))
        (ih (d + 1) _ _ _ _ (by omega) (by omega))
    · have term : ∀ (x : Fin p) (jj : Fin q),
          lay (bld C k (d + 1) z x true
            ((if d + 1 ∈ C.Es ∨ x.val = 0 then c else 0) + z.toNat * C.ex x)) jj
          = z.toNat * Dc C k (d + 1) * C.vec x false jj + z.toNat * Wc C k (d + 1) * C.vec x true jj
            + (z.toNat * hc C k (d + 1)
              + ((if d + 1 ∈ C.Es ∨ x.val = 0 then c else 0) + z.toNat * C.ex x)
                * pw p C.Es k (d + 1)) := by
        intro x jj
        rw [lay_bld_c hp C G.hh, lay_bld_below hp C G.hh jj k (d + 1) z x true (by omega)]
        ring
      rw [e, lay_node, lay_node, Finset.sum_congr rfl (fun x _ => term x j),
        Finset.sum_congr rfl (fun x _ => term x j')]
      simp only [Finset.sum_add_distrib, ← Finset.mul_sum]
      rw [G.hcol false j j', G.hcol true j j']
    all_goals
      rw [e]
      exact lay_two_congr hp _ _ j j' (ih (d + 1) _ _ _ _ (by omega) (by omega))
        (ih (d + 1) _ _ _ _ (by omega) (by omega))

/-! ### Sizes -/

theorem size_bld_zero {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) :
    ∀ (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool), d + k = n →
      size (bld C k d z i s 0) = z.toNat * (C.R d i * pw p C.U k d) := by
  have hp := G.hp0
  obtain ⟨m, rfl⟩ : ∃ m, p = m + 1 := ⟨p - 1, by omega⟩
  intro k
  induction k with
  | zero =>
    intro d z i s hd
    have h : ¬ d < C.a0 := by have := G.han; omega
    simp [bld, size, lay, pw, Cfg.R, h, ← Finset.mul_sum, G.hV1]
  | succ k ih =>
    intro d z i s hdk
    have hU : d + 1 ∈ C.Es → d + 1 ∈ C.U := fun h' => (C.mem_U _).2 (Or.inl h')
    have hR : d + 1 ≠ C.a0 → C.R d i = C.R (d + 1) i := by
      intro h
      unfold Cfg.R
      split_ifs <;> first | rfl | omega
    rcases bld_cases C k d z i s 0 with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
      ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
    · rw [e, size_two hp, ih (d + 1) z i s (by omega), size_bld_c hp C G.hh,
        ih (d + 1) false i s (by omega), pw_succ_mem k (hU (G.host_mem h1)),
        G.host_R h1 i d (Or.inl rfl), G.host_R h1 i (d + 1) (Or.inr rfl), G.host_pw h1 (by omega)]
      simp only [Bool.toNat_false, zero_mul, zero_add, Nat.add_sub_cancel]
      ring
    · have term : ∀ x : Fin (m + 1),
          size (bld C k (d + 1) z x true
            ((if d + 1 ∈ C.Es ∨ x.val = 0 then 0 else 0) + z.toNat * C.ex x))
          = z.toNat * (C.r x * pw (m + 1) C.U k (d + 1) + q * (C.ex x * pw (m + 1) C.Es k (d + 1))) := by
        intro x
        have hRx : C.R (d + 1) x = C.r x := by
          unfold Cfg.R
          rw [ite_eq_right (by omega)]
        rw [size_bld_c hp C G.hh, ih (d + 1) z x true (by omega), hRx]
        simp only [ite_self]
        ring
      have hRd : C.R d i = q := by
        unfold Cfg.R
        rw [ite_eq_left (by omega)]
      rw [e, size_node, Finset.sum_congr rfl (fun x _ => term x), ← Finset.mul_sum,
        G.hmidS k d h2 (by omega), hRd]
    · rw [e, size_two hp, ih (d + 1) z i s (by omega), pw_succ_mem k (hU h3), hR h2]
      simp only [Nat.add_sub_cancel]
      ring
    · rw [e, size_two hp, ih (d + 1) z i false (by omega), ih (d + 1) z i s (by omega),
        pw_succ_mem k (hU h3), hR h2]
      simp only [Nat.add_sub_cancel]
      ring
    · rw [e, size_two hp, ih (d + 1) z i s (by omega), pw_succ_mem k h4, hR h2]
      simp only [Nat.add_sub_cancel]
      ring
    · rw [e, size_two hp, ih (d + 1) z i s (by omega), ih (d + 1) false i s (by omega),
        pw_succ_not k h4, hR h2]
      simp only [Bool.toNat_false, zero_mul, mul_zero, add_zero]

theorem size_bld {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0)
    (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ) (hdk : d + k = n) :
    size (bld C k d z i s c) = z.toNat * (C.R d i * pw p C.U k d) + q * (c * pw p C.Es k d) := by
  rw [size_bld_c G.hp0 C G.hh, size_bld_zero G k d z i s hdk]

/-! ### The levels at which the conditions hold -/

theorem E_bld_holds {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) :
    ∀ (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ), d + k = n →
      ∀ ℓ, 1 ≤ ℓ → ℓ ≤ k → d + ℓ ∈ C.Es → E (bld C k d z i s c) ℓ := by
  have hp := G.hp
  intro k
  induction k with
  | zero => intro d z i s c _ ℓ h1 h2; omega
  | succ k ih =>
    intro d z i s c hdk ℓ hℓ1 hℓk hmem
    rcases ℓ with _ | _ | ℓ
    · omega
    · -- the level just below this class
      rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · rw [e, E_two_one hp, size_bld G _ _ _ _ _ _ (by omega), size_bld G _ _ _ _ _ _ (by omega),
          G.host_R h1 i (d + 1) (Or.inr rfl), G.host_pw h1 (by omega)]
        simp only [Bool.toNat_false, zero_mul, zero_add]
        ring
      · rw [e, E_node_one]
        intro x x'
        have hRx : ∀ y : Fin p, C.R (d + 1) y = C.r y := by
          intro y
          unfold Cfg.R
          rw [ite_eq_right (by omega)]
        have hm := G.hmidE (h2 ▸ hmem) k (by omega) x x'
        rw [← h2] at hm
        rw [size_bld G _ _ _ _ _ _ (by omega), size_bld G _ _ _ _ _ _ (by omega), hRx, hRx]
        simp only [hmem, true_or, ite_true]
        cases z
        · simp
        · simp only [Bool.toNat_true, one_mul]
          linarith
      · rw [e, E_two_one hp]
      · rw [e, E_two_one hp, size_bld G _ _ _ _ _ _ (by omega), size_bld G _ _ _ _ _ _ (by omega)]
      · exact absurd hmem h3
      · exact absurd hmem h3
    · -- deeper levels
      have hmem' : d + 1 + (ℓ + 1) ∈ C.Es := by
        have e' : d + 1 + (ℓ + 1) = d + (ℓ + 1 + 1) := by omega
        rw [e']; exact hmem
      rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · rw [e, E_two_succ hp]
        exact ⟨ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem',
          ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem'⟩
      · rw [e, E_node_succ]
        intro x
        exact ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem'
      all_goals
        rw [e, E_two_succ hp]
        exact ⟨ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem',
          ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem'⟩

theorem F_two_one_of_const (hp : 2 ≤ p) {k : ℕ} (A B : Tree p q k)
    (hA : ∀ j j', lay A j = lay A j') (hB : ∀ j j', lay B j = lay B j') : F (two A B) 1 := by
  rw [F_two_one hp]
  intro j j'
  rw [hA j j', hB j j']

theorem F_bld_holds {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) :
    ∀ (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ), d + k = n →
      ∀ ℓ, 1 ≤ ℓ → ℓ ≤ k → d + ℓ ∈ C.Fs → F (bld C k d z i s c) ℓ := by
  have hp := G.hp
  intro k
  induction k with
  | zero => intro d z i s c _ ℓ h1 h2; omega
  | succ k ih =>
    intro d z i s c hdk ℓ hℓ1 hℓk hmem
    rcases ℓ with _ | _ | ℓ
    · omega
    · -- the level just below this class
      have hna := G.hna
      have hne := G.hne
      by_cases hd : d + 1 < C.a0
      · -- above `a0`: all children are balanced
        rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
          ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
        · rw [e]
          exact F_two_one_of_const hp _ _
            (fun j j' => lay_bld_above G j j' k (d + 1) _ _ _ _ (by omega) hd)
            (fun j j' => lay_bld_above G j j' k (d + 1) _ _ _ _ (by omega) hd)
        · omega
        all_goals
          rw [e]
          exact F_two_one_of_const hp _ _
            (fun j j' => lay_bld_above G j j' k (d + 1) _ _ _ _ (by omega) hd)
            (fun j j' => lay_bld_above G j j' k (d + 1) _ _ _ _ (by omega) hd)
      · have hd' : C.a0 < d + 1 := by
          rcases Nat.lt_or_ge C.a0 (d + 1) with h | h
          · exact h
          · have h' : d + 1 = C.a0 := by omega
            rw [h'] at hmem
            exact absurd hmem hna
        rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
          ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
        · rcases G.host with h | h
          · omega
          · have := (h.2.2.2 (by omega)).1
            rw [← h1] at this
            exact absurd hmem this
        · omega
        · rw [e, F_two_one hp]
          intro j j'
          exact Nat.add_comm _ _
        · exact absurd hmem h4
        · rw [e, F_two_one hp]
          intro j j'
          rw [lay_bld_c G.hp0 C G.hh j k (d + 1) z i s c, lay_bld_c G.hp0 C G.hh j' k (d + 1) z i s c]
          ring
        · exact absurd ((C.mem_U _).2 (Or.inr ⟨hmem, hd'⟩)) h4
    · -- deeper levels
      have hmem' : d + 1 + (ℓ + 1) ∈ C.Fs := by
        have e' : d + 1 + (ℓ + 1) = d + (ℓ + 1 + 1) := by omega
        rw [e']; exact hmem
      rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · rw [e, F_two_succ hp]
        exact ⟨ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem',
          ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem'⟩
      · rw [e, F_node_succ]
        intro x
        exact ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem'
      all_goals
        rw [e, F_two_succ hp]
        exact ⟨ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem',
          ih (d + 1) _ _ _ _ (by omega) (ℓ + 1) (by omega) (by omega) hmem'⟩

/-! ### The levels at which the conditions fail -/

/-- `E` fails at a level outside `U`, in the class with all digits `0` -/
theorem E_bld_failsN {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) (i0 : Fin p) (hi0 : i0.val = 0) :
    ∀ (k d : ℕ) (s : Bool), d + k = n →
      ∀ ℓ, 1 ≤ ℓ → ℓ ≤ k → d + ℓ ∉ C.U → ¬ E (bld C k d true i0 s c0) ℓ := by
  have hp := G.hp
  intro k
  induction k with
  | zero => intro d s _ ℓ h1 h2; omega
  | succ k ih =>
    intro d s hdk ℓ hℓ1 hℓk hmem
    have hEU : ∀ a, a ∈ C.Es → a ∈ C.U := fun a h' => (C.mem_U _).2 (Or.inl h')
    rcases ℓ with _ | _ | ℓ
    · omega
    · -- the level just below this class
      have hmem1 : d + 1 ∉ C.U := hmem
      rcases bld_cases C k d true i0 s c0 with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · exact absurd (hEU _ (G.host_mem h1)) hmem1
      · have hnE : d + 1 ∉ C.Es := fun h => hmem1 (hEU _ h)
        rw [e, E_node_one]
        intro h
        apply G.hmidF (h2 ▸ hnE) k (by omega)
        intro x x'
        have hRx : ∀ y : Fin p, C.R (d + 1) y = C.r y := by
          intro y
          unfold Cfg.R
          rw [ite_eq_right (by omega)]
        have hxx := h x x'
        rw [size_bld G _ _ _ _ _ _ (by omega), size_bld G _ _ _ _ _ _ (by omega), hRx, hRx] at hxx
        simp only [hnE, false_or, Bool.toNat_true, one_mul] at hxx
        rw [h2] at hxx
        exact hxx
      · exact absurd (hEU _ h3) hmem1
      · exact absurd (hEU _ h3) hmem1
      · exact absurd h4 hmem1
      · rw [e, E_two_one hp, size_bld G _ _ _ _ _ _ (by omega), size_bld G _ _ _ _ _ _ (by omega)]
        have hRpos : 0 < C.R (d + 1) i0 := by
          unfold Cfg.R
          split_ifs
          · have := G.hq; omega
          · exact G.hr0 i0 hi0
        have hpos := Nat.mul_pos hRpos (pw_pos (p := p) G.hp0 C.U k (d + 1))
        simp only [Bool.toNat_true, one_mul, Bool.toNat_false, zero_mul, mul_zero, add_zero]
        omega
    · -- deeper levels: go into the first child
      have hmem' : d + 1 + (ℓ + 1) ∉ C.U := by
        have e' : d + 1 + (ℓ + 1) = d + (ℓ + 1 + 1) := by omega
        rw [e']; exact hmem
      rcases bld_cases C k d true i0 s c0 with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · rw [e, E_two_succ hp]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) hmem' h.1
      · rw [e, E_node_succ]
        intro h
        have h0 := h i0
        simp only [hi0, or_true, ite_true, G.hex0 i0 hi0, mul_zero, add_zero] at h0
        exact ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) hmem' h0
      all_goals
        rw [e, E_two_succ hp]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) hmem' h.1

/-- `E` fails at a level of `U ∖ Es`, in a class that carries fibres (or will carry them further down the
class with all digits `0`: below the host level, or below level `a0` if there are extra fibres there) -/
theorem E_bld_failsG {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) (i0 : Fin p) (hi0 : i0.val = 0) :
    ∀ (k d : ℕ) (z : Bool) (i : Fin p) (s : Bool) (c : ℕ) (ℓ : ℕ), 1 ≤ ℓ → ℓ ≤ k →
      d + ℓ ∈ C.U → d + ℓ ∉ C.Es →
      (1 ≤ c ∨ (z = true ∧ d < C.hb ∧ C.hb < d + ℓ ∧ 1 ≤ C.M) ∨
        (z = true ∧ d < C.a0 ∧ C.a0 < d + ℓ ∧ ∃ x, 1 ≤ C.ex x)) →
      ¬ E (bld C k d z i s c) ℓ := by
  have hp := G.hp
  intro k
  induction k with
  | zero => intro d z i s c ℓ h1 h2; omega
  | succ k ih =>
    intro d z i s c ℓ hℓ1 hℓk hU hnE hw
    rcases ℓ with _ | _ | ℓ
    · omega
    · -- the level just below this class
      have hU1 : d + 1 ∈ C.U := hU
      have hnE1 : d + 1 ∉ C.Es := hnE
      have hc : 1 ≤ c := by
        rcases hw with h | ⟨_, h, h', _⟩ | ⟨_, h, h', _⟩
        · exact h
        · omega
        · omega
      rcases bld_cases C k d z i s c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · exact absurd (G.host_mem h1) hnE1
      · rcases (C.mem_U _).1 hU1 with h | h
        · exact absurd h hnE1
        · omega
      · exact absurd h3 hnE1
      · exact absurd h3 hnE1
      · rw [e, E_two_one hp, size_bld_c G.hp0 C G.hh k (d + 1) z i s c]
        have h1' := pw_pos (p := p) G.hp0 C.Es k (d + 1)
        have h2' : 0 < q * (c * pw p C.Es k (d + 1)) :=
          Nat.mul_pos (by have := G.hq; omega) (Nat.mul_pos hc h1')
        omega
      · exact absurd hU1 h4
    · -- deeper levels
      have e' : d + 1 + (ℓ + 1) = d + (ℓ + 1 + 1) := by omega
      have hU' : d + 1 + (ℓ + 1) ∈ C.U := by rw [e']; exact hU
      have hnE' : d + 1 + (ℓ + 1) ∉ C.Es := by rw [e']; exact hnE
      by_cases h1 : d + 1 = C.hb
      · rw [bld_host C k d z i s c h1, E_two_succ hp]
        intro h
        rcases hw with hc | ⟨hz, hd, hd', hM⟩ | ⟨hz, hd, hd', hx⟩
        · exact ih (d + 1) _ _ _ _ (ℓ + 1) (by omega) (by omega) hU' hnE' (Or.inl hc) h.1
        · refine ih (d + 1) _ _ _ _ (ℓ + 1) (by omega) (by omega) hU' hnE' (Or.inl ?_) h.2
          rw [hz]
          simp only [Bool.toNat_true, one_mul]
          omega
        · have := G.hne
          exact ih (d + 1) _ _ _ _ (ℓ + 1) (by omega) (by omega) hU' hnE'
            (Or.inr (Or.inr ⟨hz, by omega, by omega, hx⟩)) h.1
      by_cases h2 : d + 1 = C.a0
      · rw [bld_mid C k d z i s c h1 h2, E_node_succ]
        intro h
        rcases hw with hc | ⟨hz, hd, hd', hM⟩ | ⟨hz, hd, hd', x, hx⟩
        · refine ih (d + 1) _ _ _ _ (ℓ + 1) (by omega) (by omega) hU' hnE' (Or.inl ?_) (h i0)
          simp only [hi0, or_true, ite_true]
          omega
        · exact ih (d + 1) _ _ _ _ (ℓ + 1) (by omega) (by omega) hU' hnE'
            (Or.inr (Or.inl ⟨hz, by omega, by omega, hM⟩)) (h i0)
        · refine ih (d + 1) _ _ _ _ (ℓ + 1) (by omega) (by omega) hU' hnE' (Or.inl ?_) (h x)
          rw [hz]
          simp only [Bool.toNat_true, one_mul]
          omega
      · have hw' : 1 ≤ c ∨ (z = true ∧ d + 1 < C.hb ∧ C.hb < d + 1 + (ℓ + 1) ∧ 1 ≤ C.M) ∨
            (z = true ∧ d + 1 < C.a0 ∧ C.a0 < d + 1 + (ℓ + 1) ∧ ∃ x, 1 ≤ C.ex x) := by
          rcases hw with hc | ⟨hz, hd, hd', hM⟩ | ⟨hz, hd, hd', hx⟩
          · exact Or.inl hc
          · exact Or.inr (Or.inl ⟨hz, by omega, by omega, hM⟩)
          · exact Or.inr (Or.inr ⟨hz, by omega, by omega, hx⟩)
        rcases bld_cases C k d z i s c with ⟨h1', e⟩ | ⟨h1', h2', e⟩ | ⟨h1', h2', h3, h4, e⟩ |
          ⟨h1', h2', h3, h4, e⟩ | ⟨h1', h2', h3, h4, e⟩ | ⟨h1', h2', h3, h4, e⟩
        · exact absurd h1' h1
        · exact absurd h2' h2
        all_goals
          rw [e, E_two_succ hp]
          exact fun h => ih (d + 1) _ _ _ _ (ℓ + 1) (by omega) (by omega) hU' hnE' hw' h.1

/-- `F` fails at a level `≥ a0` outside `Fs`, in the class with digit `0` up to level `a0`, digit `1` at
the levels of `E ∖ F` beyond `a0`, and `0` elsewhere -/
theorem F_bld_fails {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) (i0 i1 : Fin p) (hi0 : i0.val = 0)
    (hi1 : i1.val = 1) :
    ∀ (k d c : ℕ), d + k = n →
      ∀ ℓ, 1 ≤ ℓ → ℓ ≤ k → C.a0 ≤ d + ℓ → d + ℓ ∉ C.Fs → ¬ F (bld C k d true i0 true c) ℓ := by
  have hp := G.hp
  have hp0 := G.hp0
  intro k
  induction k with
  | zero => intro d c _ ℓ h1 h2; omega
  | succ k ih =>
    intro d c hdk ℓ hℓ1 hℓk ha hmem
    rcases ℓ with _ | _ | ℓ
    · omega
    · -- the level just below this class
      have ha1 : C.a0 ≤ d + 1 := ha
      have hmem1 : d + 1 ∉ C.Fs := hmem
      have hlay : ∀ (x : Fin p) (s' : Bool) (c' : ℕ) (j : Fin q),
          lay (bld C k (d + 1) true x s' c') j
            = Dc C k (d + 1) * C.vec x false j + Wc C k (d + 1) * C.vec x s' j
              + (hc C k (d + 1) + c' * pw p C.Es k (d + 1)) := by
        intro x s' c' j
        rw [lay_bld_c hp0 C G.hh, lay_bld_below hp0 C G.hh j k (d + 1) true x s' ha1]
        simp only [Bool.toNat_true, one_mul]
        ring
      have hlayF : ∀ (x : Fin p) (s' : Bool) (c' : ℕ) (j : Fin q),
          lay (bld C k (d + 1) false x s' c') j = c' * pw p C.Es k (d + 1) := by
        intro x s' c' j
        rw [lay_bld_c hp0 C G.hh, lay_bld_empty hp0, zero_add]
      have hcop := coprime_DW hp0 G.hpq C k (d + 1)
      rcases bld_cases C k d true i0 true c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · rw [e, F_two_one hp]
        intro h
        refine G.hNC i0 hi0 _ _ (hc C k (d + 1) + c * pw p C.Es k (d + 1)) hcop ?_
        intro j j'
        have hjj := h j j'
        simp only [hlay, hlayF] at hjj
        omega
      · rw [e, F_node_one]
        intro h
        refine G.hN1 i0 i1 hi0 hi1 _ _
          (hc C k (d + 1) + ((if d + 1 ∈ C.Es ∨ i0.val = 0 then c else 0) + true.toNat * C.ex i0)
            * pw p C.Es k (d + 1))
          (hc C k (d + 1) + ((if d + 1 ∈ C.Es ∨ i1.val = 0 then c else 0) + true.toNat * C.ex i1)
            * pw p C.Es k (d + 1)) hcop ?_
        intro j j'
        have hjj := h i0 i1 j j'
        simp only [hlay] at hjj
        exact hjj
      · exact absurd h4 hmem1
      · rw [e, F_two_one hp]
        intro h
        refine G.hN2 i0 hi0 (Dc C k (d + 1)) _ (hc C k (d + 1) + c * pw p C.Es k (d + 1))
          (Wc_pos hp C k (d + 1)) ?_
        intro j j'
        have hjj := h j j'
        simp only [hlay] at hjj
        exact hjj
      · rcases (C.mem_U _).1 h4 with h | h
        · exact absurd h h3
        · exact absurd h.1 hmem1
      · rw [e, F_two_one hp]
        intro h
        refine G.hNC i0 hi0 _ _ (hc C k (d + 1) + c * pw p C.Es k (d + 1)) hcop ?_
        intro j j'
        have hjj := h j j'
        simp only [hlay, hlayF] at hjj
        omega
    · -- deeper levels
      have e' : d + 1 + (ℓ + 1) = d + (ℓ + 1 + 1) := by omega
      have ha' : C.a0 ≤ d + 1 + (ℓ + 1) := by omega
      have hmem' : d + 1 + (ℓ + 1) ∉ C.Fs := by rw [e']; exact hmem
      rcases bld_cases C k d true i0 true c with ⟨h1, e⟩ | ⟨h1, h2, e⟩ | ⟨h1, h2, h3, h4, e⟩ |
        ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩ | ⟨h1, h2, h3, h4, e⟩
      · rw [e, F_two_succ hp]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) ha' hmem' h.1
      · rw [e, F_node_succ]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) ha' hmem' (h i0)
      · rw [e, F_two_succ hp]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) ha' hmem' h.1
      · rw [e, F_two_succ hp]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) ha' hmem' h.2
      · rw [e, F_two_succ hp]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) ha' hmem' h.1
      · rw [e, F_two_succ hp]
        exact fun h => ih (d + 1) _ (by omega) (ℓ + 1) (by omega) (by omega) ha' hmem' h.1

/-! ### The tree of a construction -/

/-- **The tree of good data has the pattern and the size it should have.** -/
theorem pattern_bld {C : Cfg p q} {n c0 : ℕ} (G : Good C n c0) (hE : C.Es ⊆ Finset.Icc 1 n)
    (hF : C.Fs ⊆ Finset.Icc 1 n) (i0 i1 : Fin p) (hi0 : i0.val = 0) (hi1 : i1.val = 1) :
    F (bld C n 0 true i0 true c0) 0 ∧ eSet (bld C n 0 true i0 true c0) = C.Es ∧
      fSet (bld C n 0 true i0 true c0) = C.Fs ∧
      size (bld C n 0 true i0 true c0) = q * pw p C.U n 0 + q * (c0 * pw p C.Es n 0) := by
  have ha1 := G.ha1
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [F_zero]
    intro j j'
    exact lay_bld_above G j j' n 0 _ _ _ _ (by omega) (by omega)
  · ext ℓ
    rw [mem_eSet]
    constructor
    · rintro ⟨h1, h2, h3⟩
      by_contra hn
      by_cases hU : ℓ ∈ C.U
      · refine E_bld_failsG G i0 hi0 n 0 true i0 true c0 ℓ h1 h2 (by rwa [Nat.zero_add])
          (by rwa [Nat.zero_add]) ?_ h3
        have ha : C.a0 < ℓ := by
          rcases (C.mem_U _).1 hU with h | h
          · exact absurd h hn
          · exact h.2
        rcases G.hG ℓ hU hn with h | ⟨h, h', hM⟩ | h
        · exact Or.inl h
        · exact Or.inr (Or.inl ⟨rfl, by omega, by omega, hM⟩)
        · exact Or.inr (Or.inr ⟨rfl, by omega, by omega, h⟩)
      · exact E_bld_failsN G i0 hi0 n 0 true (by omega) ℓ h1 h2 (by rwa [Nat.zero_add]) h3
    · intro h
      have h' := Finset.mem_Icc.1 (hE h)
      exact ⟨h'.1, h'.2, E_bld_holds G n 0 _ _ _ _ (by omega) ℓ h'.1 h'.2 (by rwa [Nat.zero_add])⟩
  · ext ℓ
    rw [mem_fSet]
    constructor
    · rintro ⟨h1, h2, h3⟩
      by_contra hn
      have ha : C.a0 ≤ ℓ := by
        by_contra hlt
        exact hn (G.hlow ℓ h1 (by omega))
      exact F_bld_fails G i0 i1 hi0 hi1 n 0 c0 (by omega) ℓ h1 h2 (by omega)
        (by rwa [Nat.zero_add]) h3
    · intro h
      have h' := Finset.mem_Icc.1 (hF h)
      exact ⟨h'.1, h'.2, F_bld_holds G n 0 _ _ _ _ (by omega) ℓ h'.1 h'.2 (by rwa [Nat.zero_add])⟩
  · have hR : C.R 0 i0 = q := by
      unfold Cfg.R
      rw [ite_eq_left (by omega)]
    rw [size_bld G n 0 true i0 true c0 (by omega), hR]
    simp only [Bool.toNat_true, one_mul]

end BuildB
end Pnq
