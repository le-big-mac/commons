/-
The statement on signs for every odd `n`: S5, the first live level of the prime `3`, counted more exactly.
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignPivot

open Finset

namespace Pnq

namespace ThreeAux

/-!
Lemmas for S5.  The level is `j + 1`, the full group is that of `c < 3^j`, its three classes modulo
`3^(j+1)` are `c + t * 3^j`, `t < 3`.

* If an element lies outside that group, two elements in two classes of the full group and that
  element are a pivot set with three elements, and S2 (a) gives the bound `1/8`.
* Otherwise the three classes hold all `m ≥ 7` elements, so one of them, `X`, holds three elements
  `a1`, `a2`, `a3`; `Y` is another class, `b` an element of it, `Z` the third class.  A bad signing
  has equal sums of signs on `X`, `Y`, `Z` (S0 with `η = 1`).  Counting: each of the 16 ways `x` of
  changing the signs at `a1`, `a2`, `a3`, `b` is a bijection `flip4 … x` of the signings, and of the
  16 images of a signing at most 3 have equal sums (`card_patterns_le`); counting the pairs
  (signing, `x`) with a bad image in two ways gives `#bad * 16 ≤ 3 * 2^m` (`card_mul_card_le`).
-/

/-- the sum of the signs of the signing `ε` over the finset `A` -/
def sgSum {ι : Type*} (ε : ι → Bool) (A : Finset ι) : ℤ := ∑ k ∈ A, sg (ε k)

/-- the signing `ε` with the sign at `a` changed if `x` is `true` -/
def flip {ι : Type*} [DecidableEq ι] (a : ι) (x : Bool) (ε : ι → Bool) : ι → Bool :=
  Function.update ε a (xor (ε a) x)

theorem flip_of_ne {ι : Type*} [DecidableEq ι] (a : ι) (x : Bool) (ε : ι → Bool) {k : ι}
    (h : k ≠ a) : flip a x ε k = ε k := by
  unfold flip
  exact Function.update_of_ne h _ _

theorem flip_self {ι : Type*} [DecidableEq ι] (a : ι) (x : Bool) (ε : ι → Bool) :
    flip a x ε a = xor (ε a) x := by
  unfold flip
  exact Function.update_self _ _ _

theorem flip_flip {ι : Type*} [DecidableEq ι] (a : ι) (x : Bool) (ε : ι → Bool) :
    flip a x (flip a x ε) = ε := by
  funext k
  by_cases h : k = a
  · subst h
    rw [flip_self, flip_self]
    cases ε k <;> cases x <;> rfl
  · rw [flip_of_ne _ _ _ h, flip_of_ne _ _ _ h]

theorem flip_bijective {ι : Type*} [DecidableEq ι] (a : ι) (x : Bool) :
    Function.Bijective (flip a x : (ι → Bool) → (ι → Bool)) :=
  Function.Involutive.bijective (flip_flip a x)

/-- what a flip at `a` does to the sum of the signs over `A` -/
theorem sgSum_flip {ι : Type*} [DecidableEq ι] (a : ι) (x : Bool) (ε : ι → Bool) (A : Finset ι) :
    sgSum (flip a x ε) A = sgSum ε A + if a ∈ A then sg (xor (ε a) x) - sg (ε a) else 0 := by
  unfold sgSum
  by_cases ha : a ∈ A
  · rw [ite_eq_left ha, ← Finset.add_sum_erase A (fun k => sg (flip a x ε k)) ha,
      ← Finset.add_sum_erase A (fun k => sg (ε k)) ha, flip_self]
    have h : ∑ k ∈ A.erase a, sg (flip a x ε k) = ∑ k ∈ A.erase a, sg (ε k) :=
      Finset.sum_congr rfl fun k hk => by rw [flip_of_ne _ _ _ (Finset.ne_of_mem_erase hk)]
    rw [h]
    ring
  · rw [ite_eq_right ha, add_zero]
    refine Finset.sum_congr rfl fun k hk => ?_
    rw [flip_of_ne]
    rintro rfl
    exact ha hk

/-- the four flips at `a1`, `a2`, `a3`, `b` -/
def flip4 {ι : Type*} [DecidableEq ι] (a1 a2 a3 b : ι) (x : Bool × Bool × Bool × Bool)
    (ε : ι → Bool) : ι → Bool :=
  flip a1 x.1 (flip a2 x.2.1 (flip a3 x.2.2.1 (flip b x.2.2.2 ε)))

theorem flip4_bijective {ι : Type*} [DecidableEq ι] (a1 a2 a3 b : ι)
    (x : Bool × Bool × Bool × Bool) :
    Function.Bijective (flip4 a1 a2 a3 b x : (ι → Bool) → (ι → Bool)) :=
  (flip_bijective a1 x.1).comp ((flip_bijective a2 x.2.1).comp
    ((flip_bijective a3 x.2.2.1).comp (flip_bijective b x.2.2.2)))

/-- of the 16 patterns of four signs, at most 3 give a prescribed sum of the first three and a
prescribed fourth (the signs are written as changes of given signs `p1`, `p2`, `p3`, `q`) -/
theorem card_patterns_le (p1 p2 p3 q : Bool) (u v : ℤ) :
    (Finset.univ.filter fun x : Bool × Bool × Bool × Bool =>
      sg (xor p1 x.1) + sg (xor p2 x.2.1) + sg (xor p3 x.2.2.1) = u ∧
        sg (xor q x.2.2.2) = v).card ≤ 3 := by
  by_cases h : ∃ x0 : Bool × Bool × Bool × Bool,
      sg (xor p1 x0.1) + sg (xor p2 x0.2.1) + sg (xor p3 x0.2.2.1) = u ∧ sg (xor q x0.2.2.2) = v
  · obtain ⟨x0, rfl, rfl⟩ := h
    revert p1 p2 p3 q x0
    decide
  · have h0 : (Finset.univ.filter fun x : Bool × Bool × Bool × Bool =>
        sg (xor p1 x.1) + sg (xor p2 x.2.1) + sg (xor p3 x.2.2.1) = u ∧
          sg (xor q x.2.2.2) = v) = ∅ := by
      rw [Finset.filter_eq_empty_iff]
      intro x _ hx
      exact h ⟨x, hx⟩
    rw [h0]
    simp

/-- counting twice: if `φ x`, `x : α`, are bijections of the signings and every signing has at
most `n` of its images `φ x ε` in `B`, then `#B * #α ≤ n * 2^m` -/
theorem card_mul_card_le {ι α : Type*} [Fintype ι] [Fintype α]
    (φ : α → (ι → Bool) → (ι → Bool)) (hφ : ∀ x, Function.Bijective (φ x))
    (B : Finset (ι → Bool)) (n : ℕ)
    (hn : ∀ ε, (Finset.univ.filter fun x => φ x ε ∈ B).card ≤ n) :
    B.card * Fintype.card α ≤ n * 2 ^ Fintype.card ι := by
  classical
  have h1 : ∀ x, (Finset.univ.filter fun ε => φ x ε ∈ B).card = B.card := by
    intro x
    apply Finset.card_bijective (φ x) (hφ x)
    intro ε
    simp
  calc B.card * Fintype.card α = ∑ _x : α, B.card := by simp [mul_comm]
    _ = ∑ x : α, ∑ ε : ι → Bool, if φ x ε ∈ B then 1 else 0 := by
        refine Finset.sum_congr rfl fun x _ => ?_
        rw [← h1 x, Finset.card_filter]
    _ = ∑ ε : ι → Bool, ∑ x : α, if φ x ε ∈ B then 1 else 0 := Finset.sum_comm
    _ = ∑ ε : ι → Bool, (Finset.univ.filter fun x => φ x ε ∈ B).card := by
        refine Finset.sum_congr rfl fun ε _ => ?_
        rw [Finset.card_filter]
    _ ≤ ∑ _ε : ι → Bool, n := Finset.sum_le_sum fun ε _ => hn ε
    _ = n * 2 ^ Fintype.card ι := by simp [mul_comm]

/-- the count: `X`, `Y`, `Z` pairwise disjoint, three elements in `X` and one in `Y`; then at most
`3/16` of all signings have equal sums of signs on `X`, `Y` and `Z` -/
theorem card_mul_sixteen_le {ι : Type*} [Fintype ι] (X Y Z : Finset ι)
    (a1 a2 a3 b : ι) (h1 : a1 ∈ X) (h2 : a2 ∈ X) (h3 : a3 ∈ X) (hb : b ∈ Y)
    (h12 : a1 ≠ a2) (h13 : a1 ≠ a3) (h23 : a2 ≠ a3)
    (hXY : Disjoint X Y) (hXZ : Disjoint X Z) (hYZ : Disjoint Y Z)
    (B : Finset (ι → Bool)) (hB : ∀ ε ∈ B, sgSum ε X = sgSum ε Z ∧ sgSum ε Y = sgSum ε Z) :
    B.card * 16 ≤ 3 * 2 ^ Fintype.card ι := by
  classical
  have h1Y : a1 ∉ Y := Finset.disjoint_left.mp hXY h1
  have h2Y : a2 ∉ Y := Finset.disjoint_left.mp hXY h2
  have h3Y : a3 ∉ Y := Finset.disjoint_left.mp hXY h3
  have h1Z : a1 ∉ Z := Finset.disjoint_left.mp hXZ h1
  have h2Z : a2 ∉ Z := Finset.disjoint_left.mp hXZ h2
  have h3Z : a3 ∉ Z := Finset.disjoint_left.mp hXZ h3
  have hbX : b ∉ X := Finset.disjoint_right.mp hXY hb
  have hbZ : b ∉ Z := Finset.disjoint_left.mp hYZ hb
  have h1b : a1 ≠ b := fun h => hbX (h ▸ h1)
  have h2b : a2 ≠ b := fun h => hbX (h ▸ h2)
  have h3b : a3 ≠ b := fun h => hbX (h ▸ h3)
  have hn : ∀ ε, (Finset.univ.filter fun x => flip4 a1 a2 a3 b x ε ∈ B).card ≤ 3 := by
    intro ε
    refine le_trans (Finset.card_le_card ?_) (card_patterns_le (ε a1) (ε a2) (ε a3) (ε b)
      (sgSum ε Z - sgSum ε X + (sg (ε a1) + sg (ε a2) + sg (ε a3)))
      (sgSum ε Z - sgSum ε Y + sg (ε b)))
    intro x hx
    rw [Finset.mem_filter] at hx ⊢
    refine ⟨Finset.mem_univ _, ?_⟩
    obtain ⟨hX, hY⟩ := hB _ hx.2
    simp only [flip4, sgSum_flip, ite_eq_left h1, ite_eq_left h2, ite_eq_left h3, ite_eq_left hb,
      ite_eq_right h1Y, ite_eq_right h2Y, ite_eq_right h3Y, ite_eq_right h1Z, ite_eq_right h2Z,
      ite_eq_right h3Z, ite_eq_right hbX, ite_eq_right hbZ, add_zero,
      flip_of_ne _ _ _ h12, flip_of_ne _ _ _ h13, flip_of_ne _ _ _ h1b, flip_of_ne _ _ _ h23,
      flip_of_ne _ _ _ h2b, flip_of_ne _ _ _ h3b] at hX hY
    constructor <;> linarith
  have key := card_mul_card_le (flip4 a1 a2 a3 b) (flip4_bijective a1 a2 a3 b) B 3 hn
  have h16 : Fintype.card (Bool × Bool × Bool × Bool) = 16 := by simp
  rw [h16] at key
  exact key

/-- S5 with the level written as `j + 1` and the full group, that of `c`, given -/
theorem main_aux {ι : Type*} [Fintype ι] (e : ι → ℕ) (hm : 7 ≤ Fintype.card ι) (j c : ℕ)
    (hc : c < 3 ^ j) (hfull : ∀ t, t < 3 → ∃ k, e k % 3 ^ (j + 1) = c + t * 3 ^ j) :
    (badSet e (3 ^ (j + 1))).card * 16 ≤ 3 * 2 ^ Fintype.card ι := by
  classical
  have hQ : 0 < 3 ^ j := by positivity
  have h3 : 3 ^ (j + 1) = 3 * 3 ^ j := by ring
  have hdvd : 3 ^ j ∣ 3 ^ (j + 1) := Dvd.intro_left 3 h3.symm
  by_cases hN : ∃ k2, e k2 % 3 ^ j ≠ c
  · -- an element outside the full group: a pivot set with three elements
    obtain ⟨k2, hk2⟩ := hN
    obtain ⟨k0, hk0⟩ := hfull 0 (by norm_num)
    obtain ⟨k1, hk1⟩ := hfull 1 (by norm_num)
    have hr : ∀ t, e k2 % 3 ^ (j + 1) ≠ c + t * 3 ^ j := by
      intro t ht
      apply hk2
      rw [← Nat.mod_mod_of_dvd (e k2) hdvd, ht, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hc]
    have hr0 := hr 0
    have hr1 := hr 1
    have hr2 := hr 2
    have hJ : IsPivot e 3 (j + 1) {k0, k1, k2} := by
      constructor
      · intro k hk k' hk' h
        simp only [Finset.mem_insert, Finset.mem_singleton] at hk hk'
        rcases hk with rfl | rfl | rfl <;> rcases hk' with rfl | rfl | rfl <;>
          first | rfl | (exfalso; omega)
      · intro c'
        simp only [Nat.add_sub_cancel]
        have hc'lt : c' % 3 ^ j < 3 ^ j := Nat.mod_lt _ hQ
        by_cases hc' : c' % 3 ^ j = c
        · refine ⟨2, by norm_num, ?_⟩
          intro k hk
          simp only [Finset.mem_insert, Finset.mem_singleton] at hk
          rcases hk with rfl | rfl | rfl <;> omega
        · by_cases h : e k2 % 3 ^ (j + 1) = c' % 3 ^ j
          · refine ⟨1, by norm_num, ?_⟩
            intro k hk
            simp only [Finset.mem_insert, Finset.mem_singleton] at hk
            rcases hk with rfl | rfl | rfl <;> omega
          · refine ⟨0, by norm_num, ?_⟩
            intro k hk
            simp only [Finset.mem_insert, Finset.mem_singleton] at hk
            rcases hk with rfl | rfl | rfl <;> omega
    have hcard : ({k0, k1, k2} : Finset ι).card = 3 := by
      rw [Finset.card_eq_three]
      refine ⟨k0, k1, k2, ?_, ?_, ?_, rfl⟩
      · rintro rfl; omega
      · rintro rfl; omega
      · rintro rfl; omega
    have hS := card_badSet_mul_two_pow_card_le e Nat.prime_three (i := j + 1) (by omega)
      (d := 1) (by norm_num) hJ
    rw [mul_one, hcard] at hS
    omega
  · -- every element lies in the full group: its three classes hold all the elements
    have hN' : ∀ k, e k % 3 ^ j = c := fun k => by_contra fun h => hN ⟨k, h⟩
    let C : ℕ → Finset ι := fun t =>
      Finset.univ.filter fun k => e k % 3 ^ (j + 1) = c + t * 3 ^ j
    have hC : ∀ t k, k ∈ C t ↔ e k % 3 ^ (j + 1) = c + t * 3 ^ j := by
      intro t k
      simp only [C, Finset.mem_filter, Finset.mem_univ, true_and]
    have hcover : ∀ k, k ∈ C 0 ∨ k ∈ C 1 ∨ k ∈ C 2 := by
      intro k
      rw [hC, hC, hC]
      have h1 : e k % 3 ^ (j + 1) % 3 ^ j = c := by
        rw [Nat.mod_mod_of_dvd _ hdvd]
        exact hN' k
      have h2 : e k % 3 ^ (j + 1) < 3 ^ j * 3 := by
        rw [mul_comm, ← h3]
        exact Nat.mod_lt _ (by positivity)
      have h4 := Nat.div_add_mod (e k % 3 ^ (j + 1)) (3 ^ j)
      have h5 : e k % 3 ^ (j + 1) / 3 ^ j < 3 := Nat.div_lt_of_lt_mul h2
      generalize e k % 3 ^ (j + 1) / 3 ^ j = q at h4 h5
      interval_cases q <;> omega
    have hsum : 7 ≤ (C 0).card + (C 1).card + (C 2).card := by
      have hu : (Finset.univ : Finset ι) ⊆ C 0 ∪ C 1 ∪ C 2 := by
        intro k _
        simp only [Finset.mem_union]
        rcases hcover k with h | h | h
        · exact Or.inl (Or.inl h)
        · exact Or.inl (Or.inr h)
        · exact Or.inr h
      have hu1 := Finset.card_le_card hu
      have hu2 := Finset.card_union_le (C 0 ∪ C 1) (C 2)
      have hu3 := Finset.card_union_le (C 0) (C 1)
      rw [Finset.card_univ] at hu1
      omega
    have hdisj : ∀ t t', t ≠ t' → Disjoint (C t) (C t') := by
      intro t t' htt
      rw [Finset.disjoint_left]
      intro k hk hk'
      rw [hC] at hk hk'
      apply htt
      have h : t * 3 ^ j = t' * 3 ^ j := by omega
      exact Nat.eq_of_mul_eq_mul_right hQ h
    have hne : ∀ t, t < 3 → (C t).Nonempty := by
      intro t ht
      obtain ⟨k, hk⟩ := hfull t ht
      exact ⟨k, (hC t k).mpr hk⟩
    -- a bad signing has equal sums on the three classes (S0 with `η = 1`)
    have hbad : ∀ ε ∈ badSet e (3 ^ (j + 1)), ∀ t t', t < 3 → t' < 3 →
        sgSum ε (C t) = sgSum ε (C t') := by
      intro ε hε t t' ht ht'
      rw [mem_badSet] at hε
      have h := classSum_eq_of_badAt e ε Nat.prime_three (i := j + 1) (by omega) (d := 1)
        (by norm_num) IsPrimitiveRoot.one (by rwa [mul_one]) c t t' ht ht'
      simp only [Nat.add_sub_cancel, Nat.mod_eq_of_lt hc] at h
      have hcs : ∀ s, classSum e ε 1 (3 ^ (j + 1)) (c + s * 3 ^ j) =
          ((sgSum ε (C s) : ℤ) : ℂ) := by
        intro s
        simp only [classSum, sgSum, C, one_pow, mul_one, Finset.sum_filter]
        push_cast
        rfl
      rw [hcs, hcs] at h
      exact_mod_cast h
    -- the count, for a class `tX` with three elements and the other two classes `tY`, `tZ`
    have hfin : ∀ tX tY tZ, tX < 3 → tY < 3 → tZ < 3 → tX ≠ tY → tX ≠ tZ → tY ≠ tZ →
        2 < (C tX).card → (badSet e (3 ^ (j + 1))).card * 16 ≤ 3 * 2 ^ Fintype.card ι := by
      intro tX tY tZ hX hY hZ hXY hXZ hYZ h3c
      obtain ⟨a1, a2, a3, h1, h2, h3', h12, h13, h23⟩ := Finset.two_lt_card_iff.mp h3c
      obtain ⟨b, hb⟩ := hne tY hY
      exact card_mul_sixteen_le (C tX) (C tY) (C tZ) a1 a2 a3 b h1 h2 h3' hb h12 h13 h23
        (hdisj _ _ hXY) (hdisj _ _ hXZ) (hdisj _ _ hYZ) _
        (fun ε hε => ⟨hbad ε hε _ _ hX hZ, hbad ε hε _ _ hY hZ⟩)
    by_cases h0 : 2 < (C 0).card
    · exact hfin 0 1 2 (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (by norm_num) h0
    by_cases h1 : 2 < (C 1).card
    · exact hfin 1 0 2 (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (by norm_num) h1
    · exact hfin 2 0 1 (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
        (by norm_num) (by omega)

end ThreeAux

variable {ι : Type*} [Fintype ι]

/-- **S5 (the first live level of the prime 3).**  If `m ≥ 7`, the level `i` of the prime `3` is live and
`rank e 3 i = 1`, then `#{ε bad at 3^i} * 16 ≤ 3 * 2^m`. -/
theorem card_badSet_three_pow_mul_le (e : ι → ℕ) (hm : 7 ≤ Fintype.card ι) {i : ℕ}
    (hlive : live e 3 i = true) (hrank : rank e 3 i = 1) :
    (badSet e (3 ^ i)).card * 16 ≤ 3 * 2 ^ Fintype.card ι := by
  rw [live_iff] at hlive
  obtain ⟨c, hc, hfull⟩ := hlive
  -- the level `0` is never live, so `i = j + 1`
  obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := by
    refine ⟨i - 1, ?_⟩
    by_contra h
    have h0 : i = 0 := by omega
    subst h0
    obtain ⟨k, hk⟩ := hfull 1 (by norm_num)
    simp at hc hk
    omega
  simp only [Nat.add_sub_cancel] at hc hfull
  exact ThreeAux.main_aux e hm j c hc hfull

end Pnq
