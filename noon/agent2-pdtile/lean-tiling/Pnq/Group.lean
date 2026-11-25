/-
The tree of a subset of `ZMod (p^n * q)`, and the bridge between the level conditions `E`, `F` of
`Pnq/Tree.lean` (agent3) and the Fourier zeros `ZeroAt` of `Pqr/ZeroDefs.lean` (agent2).
-/
import Pnq.Tree
import Pqr.Bridge

open Finset

namespace Pnq

variable {p q n : ℕ}

/-- The part of `A` in the residue class `r` modulo `p^d`, as a tree of depth `k`: the children of a node
are the classes of the next base-`p` digit, and a leaf counts the elements in each class modulo `q`.
(Intended for `d + k = n` and `r < p^d`.) -/
def sub (A : Finset (ZMod (p ^ n * q))) : (k : ℕ) → ℕ → ℕ → Tree p q k
  | 0, d, r => .leaf (fun j => (A.filter (fun a => a.val % p ^ d = r ∧ a.val % q = (j : ℕ))).card)
  | k + 1, d, r => .node (fun c => sub A k (d + 1) (r + (c : ℕ) * p ^ d))

/-- the tree of a subset of `ZMod (p^n * q)` -/
def treeOf (A : Finset (ZMod (p ^ n * q))) : Tree p q n := sub A n 0 0

namespace GroupAux

/-! ### Digit arithmetic and two counting lemmas (no group here) -/

/-- `x % b^(d+1) = r + c * b^d` iff `x % b^d = r` and the next base-`b` digit of `x` is `c` -/
theorem mod_pow_succ_eq_iff {b d r c x : ℕ} (hr : r < b ^ d) :
    x % b ^ (d + 1) = r + c * b ^ d ↔ x % b ^ d = r ∧ x / b ^ d % b = c := by
  have hpos : 0 < b ^ d := by omega
  rw [Nat.mod_pow_succ]
  constructor
  · intro h
    have h1 : x % b ^ d = r := by
      have h2 := congrArg (· % b ^ d) h
      simp only [Nat.add_mul_mod_self_left, Nat.add_mul_mod_self_right, Nat.mod_mod] at h2
      rwa [Nat.mod_eq_of_lt hr] at h2
    refine ⟨h1, ?_⟩
    rw [h1, mul_comm c] at h
    exact Nat.eq_of_mul_eq_mul_left hpos (Nat.add_left_cancel h)
  · rintro ⟨h1, h2⟩
    rw [h1, h2, mul_comm]

theorem add_mul_pow_lt {b d r c : ℕ} (hr : r < b ^ d) (hc : c < b) : r + c * b ^ d < b ^ (d + 1) := by
  have h : (c + 1) * b ^ d ≤ b * b ^ d := Nat.mul_le_mul_right _ hc
  rw [pow_succ, mul_comm (b ^ d) b]
  rw [Nat.add_mul, one_mul] at h
  omega

theorem add_mul_pow_mod {b d r c : ℕ} (hr : r < b ^ d) : (r + c * b ^ d) % b ^ d = r := by
  rw [Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hr]

/-- a condition on the residues `r'` in the class `r` mod `b^d` is a condition on each of the `b` classes
mod `b^(d+1)` inside it -/
theorem forall_digit_iff {b d e r : ℕ} (hb : 0 < b) (hr : r < b ^ d) (Φ : ℕ → Prop) :
    (∀ c : Fin b, ∀ r', r' < b ^ e → r' % b ^ (d + 1) = r + (c : ℕ) * b ^ d → Φ r') ↔
      ∀ r', r' < b ^ e → r' % b ^ d = r → Φ r' := by
  constructor
  · intro h r' hr' hmod
    exact h ⟨r' / b ^ d % b, Nat.mod_lt _ hb⟩ r' hr' ((mod_pow_succ_eq_iff hr).2 ⟨hmod, rfl⟩)
  · intro h c r' hr' hmod
    exact h r' hr' ((mod_pow_succ_eq_iff hr).1 hmod).1

/-- splitting a filter according to the value of a function with values in `[0, m)` -/
theorem sum_card_filter_fin {α : Type*} (s : Finset α) (P : α → Prop) [DecidablePred P] (f : α → ℕ)
    (m : ℕ) (hf : ∀ a ∈ s, f a < m) :
    ∑ c : Fin m, (s.filter (fun a => P a ∧ f a = (c : ℕ))).card = (s.filter P).card := by
  simp only [Finset.card_filter]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun a ha => ?_
  rw [Fin.sum_univ_eq_sum_range (fun c => if P a ∧ f a = c then 1 else 0) m]
  by_cases hP : P a
  · simp only [hP, true_and]
    rw [Finset.sum_ite_eq]
    simp [hf a ha]
  · simp [hP]

/-- A `P × Q` array of natural numbers is additive iff every entry is determined by its row sum, its
column sum and the total sum. -/
theorem additive_iff {P Q : ℕ} (hP : 0 < P) (hQ : 0 < Q) (X : Fin P → Fin Q → ℕ) :
    (∀ c c' j j', X c j + X c' j' = X c j' + X c' j) ↔
      ∀ c j, P * Q * X c j + ∑ c', ∑ j', X c' j' = Q * ∑ c', X c' j + P * ∑ j', X c j' := by
  constructor
  · intro h c j
    have h1 : ∑ c' : Fin P, ∑ j' : Fin Q, (X c j + X c' j')
        = ∑ c' : Fin P, ∑ j' : Fin Q, (X c j' + X c' j) :=
      Finset.sum_congr rfl fun c' _ => Finset.sum_congr rfl fun j' _ => h c c' j j'
    simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      smul_eq_mul, ← Finset.mul_sum] at h1
    rw [mul_assoc]
    omega
  · intro h c c' j j'
    have h1 := h c j
    have h2 := h c' j'
    have h3 := h c j'
    have h4 := h c' j
    apply Nat.eq_of_mul_eq_mul_left (Nat.mul_pos hP hQ)
    rw [mul_add, mul_add]
    omega

/-- divisibility of a difference in `ZMod M` by a divisor of `M`, in terms of representatives -/
theorem dvd_val_sub_iff {M : ℕ} [NeZero M] {d : ℕ} (hd : d ∣ M) (a v : ZMod M) :
    d ∣ (a - v).val ↔ a.val % d = v.val % d := by
  rw [← ZMod.natCast_eq_zero_iff, ZMod.natCast_val, ZMod.cast_sub hd, sub_eq_zero,
    ← ZMod.natCast_val a, ← ZMod.natCast_val v, ZMod.natCast_eq_natCast_iff']

/-! ### Counts of residue classes -/

/-- `N(d, r)`: the number of elements of `A` in the class `r` mod `p^d` -/
def cntP (A : Finset (ZMod (p ^ n * q))) (d r : ℕ) : ℕ :=
  (A.filter (fun a => a.val % p ^ d = r)).card

/-- `L(d, r, j)`: the number of elements of `A` in the class `r` mod `p^d` and the class `j` mod `q` -/
def cntPQ (A : Finset (ZMod (p ^ n * q))) (d r j : ℕ) : ℕ :=
  (A.filter (fun a => a.val % p ^ d = r ∧ a.val % q = j)).card

end GroupAux

variable [Fact p.Prime] [Fact q.Prime]

instance : NeZero (p ^ n * q) :=
  ⟨Nat.mul_ne_zero (pow_ne_zero _ (Fact.out : p.Prime).ne_zero) (Fact.out : q.Prime).ne_zero⟩

namespace GroupAux

omit [Fact q.Prime] in
theorem cntPQ_succ (A : Finset (ZMod (p ^ n * q))) (d r j : ℕ) (hr : r < p ^ d) :
    ∑ c : Fin p, cntPQ A (d + 1) (r + (c : ℕ) * p ^ d) j = cntPQ A d r j := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  unfold cntPQ
  rw [← sum_card_filter_fin A (fun a => a.val % p ^ d = r ∧ a.val % q = j)
    (fun a => a.val / p ^ d % p) p (fun a _ => Nat.mod_lt _ hp)]
  refine Finset.sum_congr rfl fun c _ => congrArg Finset.card (Finset.filter_congr fun a _ => ?_)
  rw [mod_pow_succ_eq_iff hr]
  tauto

omit [Fact q.Prime] in
theorem cntP_succ (A : Finset (ZMod (p ^ n * q))) (d r : ℕ) (hr : r < p ^ d) :
    ∑ c : Fin p, cntP A (d + 1) (r + (c : ℕ) * p ^ d) = cntP A d r := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  unfold cntP
  rw [← sum_card_filter_fin A (fun a => a.val % p ^ d = r)
    (fun a => a.val / p ^ d % p) p (fun a _ => Nat.mod_lt _ hp)]
  refine Finset.sum_congr rfl fun c _ => congrArg Finset.card (Finset.filter_congr fun a _ => ?_)
  rw [mod_pow_succ_eq_iff hr]

omit [Fact p.Prime] in
theorem cntPQ_sum (A : Finset (ZMod (p ^ n * q))) (d r : ℕ) :
    ∑ j : Fin q, cntPQ A d r j = cntP A d r := by
  have hq : 0 < q := (Fact.out : q.Prime).pos
  unfold cntPQ cntP
  exact sum_card_filter_fin A (fun a => a.val % p ^ d = r) (fun a => a.val % q) q
    (fun a _ => Nat.mod_lt _ hq)

omit [Fact q.Prime] in
theorem lay_sub_aux (A : Finset (ZMod (p ^ n * q))) (k : ℕ) :
    ∀ d r : ℕ, r < p ^ d → ∀ j : Fin q, lay (sub A k d r) j = cntPQ A d r j := by
  induction k with
  | zero => intro d r _ j; rfl
  | succ k ih =>
    intro d r hr j
    rw [← cntPQ_succ A d r j hr]
    show ∑ c : Fin p, lay (sub A k (d + 1) (r + (c : ℕ) * p ^ d)) j = _
    exact Finset.sum_congr rfl fun c _ => ih (d + 1) _ (add_mul_pow_lt hr c.isLt) j

theorem size_sub_aux (A : Finset (ZMod (p ^ n * q))) (k d r : ℕ) (hr : r < p ^ d) :
    size (sub A k d r) = cntP A d r := by
  unfold size
  rw [← cntPQ_sum]
  exact Finset.sum_congr rfl fun j _ => lay_sub_aux A k d r hr j

/-- the meaning of `E` for a subtree: equal counts in the `p` classes below each class `r'` at depth `e` -/
theorem E_sub (A : Finset (ZMod (p ^ n * q))) (m : ℕ) :
    ∀ k d r e : ℕ, m < k → r < p ^ d → e = d + m →
      (E (sub A k d r) (m + 1) ↔ ∀ r', r' < p ^ e → r' % p ^ d = r → ∀ c c' : Fin p,
        cntP A (e + 1) (r' + (c : ℕ) * p ^ e) = cntP A (e + 1) (r' + (c' : ℕ) * p ^ e)) := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  induction m with
  | zero =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    obtain rfl : e = d := by omega
    show (∀ c c' : Fin p, size (sub A k (e + 1) (r + (c : ℕ) * p ^ e))
      = size (sub A k (e + 1) (r + (c' : ℕ) * p ^ e))) ↔ _
    have hs : ∀ c : Fin p, size (sub A k (e + 1) (r + (c : ℕ) * p ^ e))
        = cntP A (e + 1) (r + (c : ℕ) * p ^ e) :=
      fun c => size_sub_aux A k (e + 1) _ (add_mul_pow_lt hr c.isLt)
    simp only [hs]
    constructor
    · intro h r' hr' hmod c c'
      rw [Nat.mod_eq_of_lt hr'] at hmod
      subst hmod
      exact h c c'
    · intro h c c'
      exact h r hr (Nat.mod_eq_of_lt hr) c c'
  | succ m ih =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    show (∀ c : Fin p, E (sub A k (d + 1) (r + (c : ℕ) * p ^ d)) (m + 1)) ↔ _
    refine Iff.trans (forall_congr' fun c =>
      ih k (d + 1) _ e (by omega) (add_mul_pow_lt hr c.isLt) (by omega)) ?_
    exact forall_digit_iff hp hr _

omit [Fact q.Prime] in
/-- the meaning of `F` for a subtree: additive `p × q` arrays below each class `r'` at depth `e` -/
theorem F_sub (A : Finset (ZMod (p ^ n * q))) (m : ℕ) :
    ∀ k d r e : ℕ, m < k → r < p ^ d → e = d + m →
      (F (sub A k d r) (m + 1) ↔ ∀ r', r' < p ^ e → r' % p ^ d = r →
        ∀ (c c' : Fin p) (j j' : Fin q),
          cntPQ A (e + 1) (r' + (c : ℕ) * p ^ e) j + cntPQ A (e + 1) (r' + (c' : ℕ) * p ^ e) j'
            = cntPQ A (e + 1) (r' + (c : ℕ) * p ^ e) j'
              + cntPQ A (e + 1) (r' + (c' : ℕ) * p ^ e) j) := by
  have hp : 0 < p := (Fact.out : p.Prime).pos
  induction m with
  | zero =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    obtain rfl : e = d := by omega
    show (∀ (c c' : Fin p) (j j' : Fin q),
      lay (sub A k (e + 1) (r + (c : ℕ) * p ^ e)) j + lay (sub A k (e + 1) (r + (c' : ℕ) * p ^ e)) j'
        = lay (sub A k (e + 1) (r + (c : ℕ) * p ^ e)) j'
          + lay (sub A k (e + 1) (r + (c' : ℕ) * p ^ e)) j) ↔ _
    have hs : ∀ (c : Fin p) (j : Fin q), lay (sub A k (e + 1) (r + (c : ℕ) * p ^ e)) j
        = cntPQ A (e + 1) (r + (c : ℕ) * p ^ e) j :=
      fun c j => lay_sub_aux A k (e + 1) _ (add_mul_pow_lt hr c.isLt) j
    simp only [hs]
    constructor
    · intro h r' hr' hmod c c' j j'
      rw [Nat.mod_eq_of_lt hr'] at hmod
      subst hmod
      exact h c c' j j'
    · intro h c c' j j'
      exact h r hr (Nat.mod_eq_of_lt hr) c c' j j'
  | succ m ih =>
    intro k d r e hk hr he
    obtain ⟨k, rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    show (∀ c : Fin p, F (sub A k (d + 1) (r + (c : ℕ) * p ^ d)) (m + 1)) ↔ _
    refine Iff.trans (forall_congr' fun c =>
      ih k (d + 1) _ e (by omega) (add_mul_pow_lt hr c.isLt) (by omega)) ?_
    exact forall_digit_iff hp hr _

/-! ### Counts `cnt` in terms of residues of representatives -/

theorem cnt_pow (A : Finset (ZMod (p ^ n * q))) {d : ℕ} (hd : d ≤ n) (v : ZMod (p ^ n * q)) :
    Pqr.cnt A (p ^ d) v = cntP A d (v.val % p ^ d) := by
  unfold Pqr.cnt cntP
  exact congrArg Finset.card (Finset.filter_congr fun a _ =>
    dvd_val_sub_iff ((pow_dvd_pow p hd).mul_right q) a v)

theorem cnt_pow_mul (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) {d : ℕ} (hd : d ≤ n)
    (v : ZMod (p ^ n * q)) :
    Pqr.cnt A (p ^ d * q) v = cntPQ A d (v.val % p ^ d) (v.val % q) := by
  have hcop : Nat.Coprime (p ^ d) q :=
    Nat.Coprime.pow_left d ((Nat.coprime_primes Fact.out Fact.out).2 hpq)
  unfold Pqr.cnt cntPQ
  refine congrArg Finset.card (Finset.filter_congr fun a _ => ?_)
  rw [dvd_val_sub_iff (Nat.mul_dvd_mul_right (pow_dvd_pow p hd) q) a v]
  exact (Nat.modEq_and_modEq_iff_modEq_mul hcop).symm

theorem cnt_q (A : Finset (ZMod (p ^ n * q))) (v : ZMod (p ^ n * q)) :
    Pqr.cnt A q v = (A.filter (fun a => a.val % q = v.val % q)).card := by
  unfold Pqr.cnt
  exact congrArg Finset.card (Finset.filter_congr fun a _ =>
    dvd_val_sub_iff (dvd_mul_left q _) a v)

omit [Fact p.Prime] [Fact q.Prime] in
/-- every residue mod `p^d` is attained -/
theorem exists_val_mod_pow {d : ℕ} (hd : d ≤ n) (s : ℕ) (hs : s < p ^ d) :
    ∃ v : ZMod (p ^ n * q), v.val % p ^ d = s :=
  ⟨(s : ZMod (p ^ n * q)), by
    rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ ((pow_dvd_pow p hd).mul_right q),
      Nat.mod_eq_of_lt hs]⟩

omit [Fact p.Prime] [Fact q.Prime] in
/-- every residue mod `q` is attained -/
theorem exists_val_mod_q (j : ℕ) (hj : j < q) : ∃ v : ZMod (p ^ n * q), v.val % q = j :=
  ⟨(j : ZMod (p ^ n * q)), by
    rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ (dvd_mul_left q _), Nat.mod_eq_of_lt hj]⟩

/-- Chinese remainder theorem: every pair of residues mod `p^d` and mod `q` is attained -/
theorem exists_val_mod_pow_q (hpq : p ≠ q) {d : ℕ} (hd : d ≤ n) (s j : ℕ) (hs : s < p ^ d)
    (hj : j < q) : ∃ v : ZMod (p ^ n * q), v.val % p ^ d = s ∧ v.val % q = j := by
  have hcop : Nat.Coprime (p ^ d) q :=
    Nat.Coprime.pow_left d ((Nat.coprime_primes Fact.out Fact.out).2 hpq)
  obtain ⟨k, hk1, hk2⟩ := Nat.chineseRemainder hcop s j
  refine ⟨(k : ZMod (p ^ n * q)), ?_, ?_⟩
  · rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ ((pow_dvd_pow p hd).mul_right q)]
    exact Eq.trans hk1 (Nat.mod_eq_of_lt hs)
  · rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ (dvd_mul_left q _)]
    exact Eq.trans hk2 (Nat.mod_eq_of_lt hj)

end GroupAux

open GroupAux

set_option linter.unusedSectionVars false in
/-- layer counts of a subtree -/
theorem lay_sub (A : Finset (ZMod (p ^ n * q))) (k d r : ℕ) (hr : r < p ^ d) (j : Fin q) :
    lay (sub A k d r) j = (A.filter (fun a => a.val % p ^ d = r ∧ a.val % q = (j : ℕ))).card :=
  lay_sub_aux A k d r hr j

/-- size of a subtree -/
theorem size_sub (A : Finset (ZMod (p ^ n * q))) (k d r : ℕ) (hr : r < p ^ d) :
    size (sub A k d r) = (A.filter (fun a => a.val % p ^ d = r)).card :=
  size_sub_aux A k d r hr

theorem size_treeOf (A : Finset (ZMod (p ^ n * q))) : size (treeOf A) = A.card := by
  rw [treeOf, size_sub A n 0 0 (by simp)]
  simp [Nat.mod_one]

/-- level `ℓ` is in `E` iff `Φ_{p^ℓ}` divides the mask polynomial -/
theorem E_treeOf (A : Finset (ZMod (p ^ n * q))) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    E (treeOf A) ℓ ↔ Pqr.ZeroAt A (p ^ ℓ) := by
  obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
  have hp : p.Prime := Fact.out
  have hm : m ≤ n := by omega
  rw [Pqr.zeroAt_prime_pow A p hp m ((pow_dvd_pow p hn).mul_right q), treeOf,
    E_sub A m n 0 0 m (by omega) (by simp) (by simp)]
  simp only [cnt_pow A hn, cnt_pow A hm]
  constructor
  · intro h v
    have hr' : v.val % p ^ m < p ^ m := Nat.mod_lt _ (pow_pos hp.pos m)
    rw [← cntP_succ A m _ hr', Nat.mod_pow_succ, mul_comm (p ^ m),
      Finset.sum_congr rfl (fun c' _ => h _ hr' (Nat.mod_one _) c'
        ⟨v.val / p ^ m % p, Nat.mod_lt _ hp.pos⟩)]
    simp
  · intro h r' hr' _ c c'
    have key : ∀ c : Fin p, p * cntP A (m + 1) (r' + (c : ℕ) * p ^ m) = cntP A m r' := by
      intro c
      obtain ⟨v, hv⟩ := exists_val_mod_pow (q := q) hn (r' + (c : ℕ) * p ^ m)
        (add_mul_pow_lt hr' c.isLt)
      have hv' : v.val % p ^ m = r' := by
        rw [← Nat.mod_mod_of_dvd v.val (pow_dvd_pow p (Nat.le_succ m)), hv, add_mul_pow_mod hr']
      have h2 := h v
      rwa [hv, hv'] at h2
    exact Nat.eq_of_mul_eq_mul_left hp.pos ((key c).trans (key c').symm)

/-- `0 ∈ F` iff `Φ_q` divides the mask polynomial -/
theorem F_treeOf_zero (A : Finset (ZMod (p ^ n * q))) : F (treeOf A) 0 ↔ Pqr.ZeroAt A q := by
  have hq : q.Prime := Fact.out
  have h := Pqr.zeroAt_prime_pow A q hq 0 (by rw [zero_add, pow_one]; exact dvd_mul_left q _)
  simp only [zero_add, pow_one, pow_zero, Pqr.cnt_one, cnt_q] at h
  rw [h, F_zero, treeOf]
  have hl : ∀ j : Fin q,
      lay (sub A n 0 0) j = (A.filter (fun a => a.val % q = (j : ℕ))).card := by
    intro j
    rw [lay_sub A n 0 0 (by simp) j]
    simp [Nat.mod_one]
  have hsum : ∑ j : Fin q, (A.filter (fun a => a.val % q = (j : ℕ))).card = A.card := by
    have h3 := sum_card_filter_fin A (fun _ => True) (fun a => a.val % q) q
      (fun a _ => Nat.mod_lt _ hq.pos)
    simpa using h3
  simp only [hl]
  constructor
  · intro h2 v
    rw [← hsum, Finset.sum_congr rfl (fun j' _ => h2 j' ⟨v.val % q, Nat.mod_lt _ hq.pos⟩)]
    simp
  · intro h2 j j'
    have key : ∀ j : Fin q, q * (A.filter (fun a => a.val % q = (j : ℕ))).card = A.card := by
      intro j
      obtain ⟨v, hv⟩ := exists_val_mod_q (p := p) (n := n) (j : ℕ) j.isLt
      have h3 := h2 v
      rwa [hv] at h3
    exact Nat.eq_of_mul_eq_mul_left hq.pos ((key j).trans (key j').symm)

/-- level `ℓ ≥ 1` is in `F` iff `Φ_{p^ℓ q}` divides the mask polynomial -/
theorem F_treeOf (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) (ℓ : ℕ) (h1 : 1 ≤ ℓ) (hn : ℓ ≤ n) :
    F (treeOf A) ℓ ↔ Pqr.ZeroAt A (p ^ ℓ * q) := by
  obtain ⟨m, rfl⟩ : ∃ m, ℓ = m + 1 := ⟨ℓ - 1, by omega⟩
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hm : m ≤ n := by omega
  rw [Pqr.zeroAt_prime_pow_mul A p q hp hq hpq m (Nat.mul_dvd_mul_right (pow_dvd_pow p hn) q),
    treeOf, F_sub A m n 0 0 m (by omega) (by simp) (by simp)]
  simp only [cnt_pow A hn, cnt_pow A hm, cnt_pow_mul hpq A hn, cnt_pow_mul hpq A hm]
  -- for one class `r'` mod `p^m`: additivity of the array of the `p × q` classes inside it
  have key : ∀ r', r' < p ^ m →
      ((∀ (c c' : Fin p) (j j' : Fin q),
          cntPQ A (m + 1) (r' + (c : ℕ) * p ^ m) j + cntPQ A (m + 1) (r' + (c' : ℕ) * p ^ m) j'
            = cntPQ A (m + 1) (r' + (c : ℕ) * p ^ m) j'
              + cntPQ A (m + 1) (r' + (c' : ℕ) * p ^ m) j) ↔
        ∀ (c : Fin p) (j : Fin q),
          p * q * cntPQ A (m + 1) (r' + (c : ℕ) * p ^ m) j + cntP A m r'
            = q * cntPQ A m r' j + p * cntP A (m + 1) (r' + (c : ℕ) * p ^ m)) := by
    intro r' hr'
    have h2 := additive_iff hp.pos hq.pos
      (fun (c : Fin p) (j : Fin q) => cntPQ A (m + 1) (r' + (c : ℕ) * p ^ m) j)
    simp only [cntPQ_sum, cntP_succ A m r' hr', cntPQ_succ A m r' _ hr'] at h2
    exact h2
  constructor
  · intro h v
    have hr' : v.val % p ^ m < p ^ m := Nat.mod_lt _ (pow_pos hp.pos m)
    have h2 := (key _ hr').1 (h _ hr' (Nat.mod_one _)) ⟨v.val / p ^ m % p, Nat.mod_lt _ hp.pos⟩
      ⟨v.val % q, Nat.mod_lt _ hq.pos⟩
    rw [Nat.mod_pow_succ, mul_comm (p ^ m)]
    exact h2
  · intro h r' hr' _
    rw [key r' hr']
    intro c j
    obtain ⟨v, hv1, hv2⟩ := exists_val_mod_pow_q hpq hn (r' + (c : ℕ) * p ^ m) (j : ℕ)
      (add_mul_pow_lt hr' c.isLt) j.isLt
    have hv' : v.val % p ^ m = r' := by
      rw [← Nat.mod_mod_of_dvd v.val (pow_dvd_pow p (Nat.le_succ m)), hv1, add_mul_pow_mod hr']
    have h2 := h v
    rwa [hv1, hv2, hv'] at h2

end Pnq
