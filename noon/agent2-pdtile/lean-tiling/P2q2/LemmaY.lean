/-
The one counting lemma of the proof (Yonder's Lemma Y'): a set of `p * q` elements of `ZMod (p^2 * q^2)` that
has the zeros `p` and `p^2 * q^2` also has the zero `p * q^2`.
-/
import Pqr.Bridge
import Pqr.CM

open Finset

namespace P2q2

open Pqr

/-! Helper lemmas live in the namespace `P2q2.LemmaY`. -/

namespace LemmaY

/-! ### Residue classes modulo a divisor of `M` -/

section General

variable {M : ℕ} [NeZero M]

/-- for `d ∣ M`: the representative of `x` is divisible by `d` iff the image of `x` in `ZMod d` is zero -/
theorem dvd_val_iff {d : ℕ} (hd : d ∣ M) (x : ZMod M) :
    d ∣ x.val ↔ ZMod.castHom hd (ZMod d) x = 0 := by
  rw [ZMod.castHom_apply, ← ZMod.natCast_val, ZMod.natCast_eq_zero_iff]

theorem dvd_val_sub_comm {d : ℕ} (hd : d ∣ M) {x y : ZMod M} (h : d ∣ (x - y).val) :
    d ∣ (y - x).val := by
  rw [dvd_val_iff hd] at h ⊢
  rw [← neg_sub, map_neg, h, neg_zero]

theorem dvd_val_sub_trans {d : ℕ} (hd : d ∣ M) {x y z : ZMod M} (h1 : d ∣ (x - y).val)
    (h2 : d ∣ (y - z).val) : d ∣ (x - z).val := by
  rw [dvd_val_iff hd] at h1 h2 ⊢
  rw [← sub_add_sub_cancel x y z, map_add, h1, h2, add_zero]

/-- the count modulo `e` only depends on the class modulo `e` -/
theorem cnt_congr (A : Finset (ZMod M)) {e : ℕ} (he : e ∣ M) {v w : ZMod M}
    (h : e ∣ (v - w).val) : cnt A e v = cnt A e w := by
  unfold cnt
  congr 1
  refine Finset.filter_congr fun a _ => ?_
  exact ⟨fun h1 => dvd_val_sub_trans he h1 h, fun h1 => dvd_val_sub_trans he h1 (dvd_val_sub_comm he h)⟩

omit [NeZero M] in
/-- a class modulo `d` is contained in the class modulo any divisor of `d` -/
theorem cnt_mono (A : Finset (ZMod M)) {e d : ℕ} (hed : e ∣ d) (v : ZMod M) :
    cnt A d v ≤ cnt A e v :=
  Finset.card_le_card (Finset.monotone_filter_right _ fun _ _ h => hed.trans h)

/-- a class modulo `d` has `M / d` elements -/
theorem card_class {d : ℕ} (hd : d ∣ M) (v : ZMod M) :
    (Finset.univ.filter (fun x : ZMod M => d ∣ (x - v).val)).card = M / d := by
  have h1 := Bridge.sum_dvd_val d hd (fun _ => (1 : ℂ))
  rw [Finset.card_filter, ← Equiv.sum_comp (Equiv.subRight v).symm]
  have h2 : ((∑ t : ZMod M, if d ∣ t.val then 1 else 0 : ℕ) : ℂ) = ((M / d : ℕ) : ℂ) := by
    push_cast
    rw [h1]
    simp
  have h3 := Nat.cast_injective h2
  rw [← h3]
  refine Finset.sum_congr rfl fun t _ => ?_
  simp

theorem cnt_le (A : Finset (ZMod M)) {d : ℕ} (hd : d ∣ M) (v : ZMod M) : cnt A d v ≤ M / d := by
  rw [← card_class hd v]
  exact Finset.card_le_card (Finset.filter_subset_filter _ (Finset.subset_univ A))

/-- if the count of a class is less than its size, the class has an element outside `A` -/
theorem exists_notMem_of_cnt_lt (A : Finset (ZMod M)) {d : ℕ} (hd : d ∣ M) (v : ZMod M)
    (h : cnt A d v < M / d) : ∃ w, d ∣ (w - v).val ∧ w ∉ A := by
  by_contra hcon
  push Not at hcon
  have h1 : M / d ≤ cnt A d v := by
    rw [← card_class hd v]
    exact Finset.card_le_card fun w hw =>
      mem_filter.2 ⟨hcon w (mem_filter.1 hw).2, (mem_filter.1 hw).2⟩
  omega

/-- if the count of a class equals its size, the class is contained in `A` -/
theorem mem_of_cnt_eq (A : Finset (ZMod M)) {d : ℕ} (hd : d ∣ M) (v : ZMod M)
    (h : cnt A d v = M / d) {w : ZMod M} (hw : d ∣ (w - v).val) : w ∈ A := by
  by_contra hwA
  have h1 : cnt A d v < M / d := by
    rw [← card_class hd v]
    refine Finset.card_lt_card ⟨Finset.filter_subset_filter _ (Finset.subset_univ A), fun hsub => ?_⟩
    exact hwA (mem_filter.1 (hsub (mem_filter.2 ⟨mem_univ w, hw⟩))).1
  omega

/-- the count modulo `M` is the indicator of `A` -/
theorem cnt_self (A : Finset (ZMod M)) (v : ZMod M) : cnt A M v = if v ∈ A then 1 else 0 := by
  classical
  have h1 : A.filter (fun a => M ∣ (a - v).val) = A.filter (fun a => a = v) := by
    refine Finset.filter_congr fun a _ => ?_
    constructor
    · intro h
      have h2 := Nat.eq_zero_of_dvd_of_lt h (ZMod.val_lt _)
      exact sub_eq_zero.1 ((ZMod.val_eq_zero _).1 h2)
    · rintro rfl
      simp
  rw [cnt, h1, Finset.filter_eq']
  split_ifs <;> simp

end General

/-! ### The bridge for an order `p ^ (a + 1) * q ^ (b + 1)` -/

theorem pow_mul_pow_dvd_iff {p q : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) (i j c d : ℕ) :
    p ^ i * q ^ j ∣ p ^ c * q ^ d ↔ i ≤ c ∧ j ≤ d := by
  have hcop : Nat.Coprime p q := (Nat.coprime_primes hp hq).2 hpq
  constructor
  · intro h
    have h1 : p ^ i ∣ p ^ c :=
      (Nat.Coprime.pow i d hcop).dvd_of_dvd_mul_right ((dvd_mul_right _ _).trans h)
    have h2 : q ^ j ∣ q ^ d :=
      (Nat.Coprime.pow j c hcop.symm).dvd_of_dvd_mul_left ((dvd_mul_left _ _).trans h)
    exact ⟨(Nat.pow_dvd_pow_iff_le_right hp.one_lt).1 h1, (Nat.pow_dvd_pow_iff_le_right hq.one_lt).1 h2⟩
  · rintro ⟨h1, h2⟩
    exact Nat.mul_dvd_mul (pow_dvd_pow p h1) (pow_dvd_pow q h2)

theorem pow_mul_pow_eq_iff {p q : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) (i j c d : ℕ) :
    p ^ i * q ^ j = p ^ c * q ^ d ↔ i = c ∧ j = d := by
  constructor
  · intro h
    have h1 := (pow_mul_pow_dvd_iff hp hq hpq i j c d).1 (h ▸ dvd_rfl)
    have h2 := (pow_mul_pow_dvd_iff hp hq hpq c d i j).1 (h ▸ dvd_rfl)
    omega
  · rintro ⟨rfl, rfl⟩
    rfl

/-- `[e ∣ p^(a+1) q^(b+1)] - [e ∣ p^a q^(b+1)] - [e ∣ p^(a+1) q^b] + [e ∣ p^a q^b] = [e = p^(a+1) q^(b+1)]` -/
theorem indicator_two_prime_pow {p q : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) (a b e : ℕ) :
    (if e ∣ p ^ (a + 1) * q ^ (b + 1) then (1 : ℤ) else 0) + (if e ∣ p ^ a * q ^ (b + 1) then -1 else 0)
        + (if e ∣ p ^ (a + 1) * q ^ b then -1 else 0) + (if e ∣ p ^ a * q ^ b then 1 else 0)
      = if e = p ^ (a + 1) * q ^ (b + 1) then 1 else 0 := by
  by_cases h : e ∣ p ^ (a + 1) * q ^ (b + 1)
  · obtain ⟨e₁, e₂, he₁, he₂, rfl⟩ := Nat.dvd_mul.1 h
    obtain ⟨i, -, rfl⟩ := (Nat.dvd_prime_pow hp).1 he₁
    obtain ⟨j, -, rfl⟩ := (Nat.dvd_prime_pow hq).1 he₂
    simp only [pow_mul_pow_dvd_iff hp hq hpq, pow_mul_pow_eq_iff hp hq hpq]
    split_ifs <;> omega
  · have h2 : ¬ e ∣ p ^ a * q ^ (b + 1) := fun h' =>
      h (h'.trans (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ a)) _))
    have h3 : ¬ e ∣ p ^ (a + 1) * q ^ b := fun h' =>
      h (h'.trans (Nat.mul_dvd_mul_left _ (pow_dvd_pow q (Nat.le_succ b))))
    have h4 : ¬ e ∣ p ^ a * q ^ b := fun h' =>
      h (h'.trans (Nat.mul_dvd_mul (pow_dvd_pow p (Nat.le_succ a)) (pow_dvd_pow q (Nat.le_succ b))))
    have h5 : ¬ e = p ^ (a + 1) * q ^ (b + 1) := fun h' => h (h' ▸ dvd_rfl)
    rw [ite_eq_right h, ite_eq_right h2, ite_eq_right h3, ite_eq_right h4, ite_eq_right h5]
    norm_num

/-- order a product of two prime powers: the arrays of counts are additive -/
theorem zeroAt_two_prime_pow {M : ℕ} [NeZero M] (A : Finset (ZMod M)) (p q : ℕ) (hp : p.Prime)
    (hq : q.Prime) (hpq : p ≠ q) (a b : ℕ) (h : p ^ (a + 1) * q ^ (b + 1) ∣ M) :
    ZeroAt A (p ^ (a + 1) * q ^ (b + 1)) ↔ ∀ v : ZMod M,
      p * q * cnt A (p ^ (a + 1) * q ^ (b + 1)) v + cnt A (p ^ a * q ^ b) v
        = q * cnt A (p ^ a * q ^ (b + 1)) v + p * cnt A (p ^ (a + 1) * q ^ b) v := by
  have h1 : p ^ a * q ^ (b + 1) ∣ M :=
    (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ a)) _).trans h
  have h2 : p ^ (a + 1) * q ^ b ∣ M :=
    (Nat.mul_dvd_mul_left _ (pow_dvd_pow q (Nat.le_succ b))).trans h
  have h3 : p ^ a * q ^ b ∣ M :=
    (Nat.mul_dvd_mul_right (pow_dvd_pow p (Nat.le_succ a)) _).trans h2
  have hpl : (p : ℤ) ^ a * (q : ℤ) ^ b ≠ 0 :=
    mul_ne_zero (pow_ne_zero _ (Nat.cast_ne_zero.2 hp.ne_zero)) (pow_ne_zero _ (Nat.cast_ne_zero.2 hq.ne_zero))
  have key : ∀ X Y Z W : ℕ,
      ((1 : ℤ) * ((p ^ (a + 1) * q ^ (b + 1) : ℕ) : ℤ) * (X : ℤ)
          + (-1) * ((p ^ a * q ^ (b + 1) : ℕ) : ℤ) * (Y : ℤ)
          + (-1) * ((p ^ (a + 1) * q ^ b : ℕ) : ℤ) * (Z : ℤ) + 1 * ((p ^ a * q ^ b : ℕ) : ℤ) * (W : ℤ) = 0)
        ↔ p * q * X + W = q * Y + p * Z := by
    intro X Y Z W
    push_cast
    constructor
    · intro h4
      have h5 : ((p : ℤ) ^ a * (q : ℤ) ^ b) * ((p : ℤ) * q * X + W - (q * Y + p * Z)) = 0 := by
        linear_combination h4
      have h6 : (p : ℤ) * q * X + W = q * Y + p * Z := by
        have := (mul_eq_zero.1 h5).resolve_left hpl
        linarith
      exact_mod_cast h6
    · intro h4
      have h5 : (p : ℤ) * q * X + W = q * Y + p * Z := by exact_mod_cast h4
      linear_combination ((p : ℤ) ^ a * (q : ℤ) ^ b) * h5
  rw [Bridge.zeroAt_iff_cnt_aux A (p ^ (a + 1) * q ^ (b + 1)) (Finset.univ : Finset (Fin 4))
    ![p ^ (a + 1) * q ^ (b + 1), p ^ a * q ^ (b + 1), p ^ (a + 1) * q ^ b, p ^ a * q ^ b]
    ![1, -1, -1, 1] ?_ ?_]
  · refine forall_congr' fun v => ?_
    rw [Fin.sum_univ_four]
    exact key _ _ _ _
  · intro i _
    fin_cases i
    · exact h
    · exact h1
    · exact h2
    · exact h3
  · intro e _
    rw [Fin.sum_univ_four]
    exact indicator_two_prime_pow hp hq hpq a b e

/-! ### The set `A` of the lemma -/

section Main

variable {p q : ℕ} [Fact p.Prime] [Fact q.Prime]

omit [Fact p.Prime] [Fact q.Prime] in
theorem dvd_p : p ∣ p ^ 2 * q ^ 2 := ⟨p * q ^ 2, by ring⟩

omit [Fact p.Prime] [Fact q.Prime] in
theorem dvd_pq : p * q ∣ p ^ 2 * q ^ 2 := ⟨p * q, by ring⟩

omit [Fact p.Prime] [Fact q.Prime] in
theorem dvd_p2q : p ^ 2 * q ∣ p ^ 2 * q ^ 2 := ⟨q, by ring⟩

omit [Fact p.Prime] [Fact q.Prime] in
theorem dvd_pq2 : p * q ^ 2 ∣ p ^ 2 * q ^ 2 := ⟨p, by ring⟩

theorem div_p2q : p ^ 2 * q ^ 2 / (p ^ 2 * q) = q := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  exact Nat.div_eq_of_eq_mul_right (Nat.mul_pos (pow_pos hp.pos 2) hq.pos) (by ring)

theorem div_pq2 : p ^ 2 * q ^ 2 / (p * q ^ 2) = p := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  exact Nat.div_eq_of_eq_mul_right (Nat.mul_pos hp.pos (pow_pos hq.pos 2)) (by ring)

/-- An element of `A` whose row (class modulo `p²q`) is not full: its class modulo `pq` has a number of
elements of `A` divisible by `p`. -/
theorem step1 (A : Finset (ZMod (p ^ 2 * q ^ 2)))
    (hii : ∀ v, p * q * cnt A (p ^ 2 * q ^ 2) v + cnt A (p * q) v
      = q * cnt A (p * q ^ 2) v + p * cnt A (p ^ 2 * q) v)
    {a : ZMod (p ^ 2 * q ^ 2)} (ha : a ∈ A) (hρ : cnt A (p ^ 2 * q) a < q) :
    p ∣ cnt A (p * q) a := by
  have hq : q.Prime := Fact.out
  obtain ⟨w, hw, hwA⟩ := exists_notMem_of_cnt_lt A dvd_p2q a (by rwa [div_p2q])
  have h1 : cnt A (p ^ 2 * q) w = cnt A (p ^ 2 * q) a := cnt_congr A dvd_p2q hw
  have h2 : cnt A (p * q) w = cnt A (p * q) a :=
    cnt_congr A dvd_pq (Dvd.dvd.trans ⟨p, by ring⟩ hw)
  have e1 := hii w
  have e2 := hii a
  rw [cnt_self, ite_eq_right hwA, h1, h2] at e1
  rw [cnt_self, ite_eq_left ha] at e2
  have hκ : cnt A (p * q ^ 2) a ≤ p := by
    have := cnt_le A dvd_pq2 a
    rwa [div_pq2] at this
  have h3 : q * cnt A (p * q ^ 2) a = q * (p + cnt A (p * q ^ 2) w) := by linarith
  have h4 := Nat.eq_of_mul_eq_mul_left hq.pos h3
  have h5 : cnt A (p * q ^ 2) w = 0 := by omega
  rw [h5] at e1
  exact ⟨cnt A (p ^ 2 * q) a, by linarith⟩

/-- No element of `A` has a row that is not full. -/
theorem step2 (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) (hi : ∀ v, cnt A p v = q)
    (hii : ∀ v, p * q * cnt A (p ^ 2 * q ^ 2) v + cnt A (p * q) v
      = q * cnt A (p * q ^ 2) v + p * cnt A (p ^ 2 * q) v)
    {a₀ : ZMod (p ^ 2 * q ^ 2)} (ha₀ : a₀ ∈ A) (hρ : cnt A (p ^ 2 * q) a₀ < q) : False := by
  classical
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hnd : ¬ p ∣ q := fun h => hpq ((Nat.prime_dvd_prime_iff_eq hp hq).1 h)
  by_cases hc : ∃ a ∈ A, p ∣ (a - a₀).val ∧ q ≤ cnt A (p ^ 2 * q) a
  · -- some element of the class of `a₀` modulo `p` has a full row: that row is the whole class
    obtain ⟨a', -, hd, hge⟩ := hc
    have hN : q ≤ cnt A (p * q) a' := hge.trans (cnt_mono A ⟨p, by ring⟩ a')
    have hsub : A.filter (fun a => p * q ∣ (a - a').val) ⊆ A.filter (fun a => p ∣ (a - a').val) :=
      Finset.monotone_filter_right _ fun a _ h => (dvd_mul_right p q).trans h
    have heq := Finset.eq_of_subset_of_card_le hsub (by
      change cnt A p a' ≤ cnt A (p * q) a'
      rw [hi]
      exact hN)
    have hmem : a₀ ∈ A.filter (fun a => p ∣ (a - a').val) :=
      mem_filter.2 ⟨ha₀, dvd_val_sub_comm dvd_p hd⟩
    rw [← heq] at hmem
    have h0 : cnt A (p * q) a₀ = cnt A (p * q) a' := cnt_congr A dvd_pq (mem_filter.1 hmem).2
    have hle : cnt A (p * q) a' ≤ q := (cnt_mono A (dvd_mul_right p q) a').trans (hi a').le
    have h1 := step1 A hii ha₀ hρ
    rw [h0, le_antisymm hle hN] at h1
    exact hnd h1
  · -- every element of the class of `a₀` modulo `p` has a row that is not full
    push Not at hc
    have hS : ∀ a ∈ A, p ∣ (a - a₀).val → p ∣ cnt A (p * q) a :=
      fun a ha hd => step1 A hii ha (hc a ha hd)
    have hcard : (A.filter (fun a => p ∣ (a - a₀).val)).card = q := hi a₀
    apply hnd
    rw [← hcard, Finset.card_eq_sum_card_fiberwise (f := ZMod.castHom dvd_pq (ZMod (p * q)))
      (t := (A.filter (fun a => p ∣ (a - a₀).val)).image (ZMod.castHom dvd_pq (ZMod (p * q))))
      (fun x hx => mem_coe.2 (mem_image_of_mem _ hx))]
    refine Finset.dvd_sum fun c hc' => ?_
    obtain ⟨a', ha'S, rfl⟩ := mem_image.1 hc'
    obtain ⟨ha', hd'⟩ := mem_filter.1 ha'S
    have hfib : (A.filter (fun a => p ∣ (a - a₀).val)).filter
          (fun a => ZMod.castHom dvd_pq (ZMod (p * q)) a = ZMod.castHom dvd_pq (ZMod (p * q)) a')
        = A.filter (fun a => p * q ∣ (a - a').val) := by
      ext a
      simp only [mem_filter]
      constructor
      · rintro ⟨⟨haA, -⟩, hf⟩
        exact ⟨haA, (dvd_val_iff dvd_pq _).2 (by rw [map_sub, hf, sub_self])⟩
      · rintro ⟨haA, hd⟩
        refine ⟨⟨haA, dvd_val_sub_trans dvd_p ((dvd_mul_right p q).trans hd) hd'⟩, ?_⟩
        have h1 := (dvd_val_iff dvd_pq _).1 hd
        rwa [map_sub, sub_eq_zero] at h1
    rw [hfib]
    exact hS a' ha' hd'

end Main

end LemmaY

open LemmaY in
theorem zeroAt_pq2_of_card (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ 2 * q ^ 2))) (hcard : A.card = p * q) (hp : ZeroAt A p)
    (hpq2 : ZeroAt A (p ^ 2 * q ^ 2)) : ZeroAt A (p * q ^ 2) := by
  classical
  have hp' : p.Prime := Fact.out
  have hq' : q.Prime := Fact.out
  -- (i) every class modulo `p` has `q` elements of `A`
  have hi : ∀ v, cnt A p v = q := by
    intro v
    have h := (zeroAt_prime_pow A p hp' 0 (by rw [zero_add, pow_one]; exact dvd_p)).1
      (by rwa [zero_add, pow_one]) v
    rw [zero_add, pow_one, pow_zero, cnt_one, hcard] at h
    exact Nat.eq_of_mul_eq_mul_left hp'.pos h
  -- (ii) the count identity of the zero `p² q²`
  have hii : ∀ v, p * q * cnt A (p ^ 2 * q ^ 2) v + cnt A (p * q) v
      = q * cnt A (p * q ^ 2) v + p * cnt A (p ^ 2 * q) v := by
    intro v
    have h := (zeroAt_two_prime_pow A p q hp' hq' hpq 1 1 dvd_rfl).1 hpq2 v
    simpa only [Nat.reduceAdd, pow_one] using h
  -- Claim: every row meeting `A` is contained in `A`
  have hclaim : ∀ a ∈ A, cnt A (p ^ 2 * q) a = q := by
    intro a ha
    by_contra hne
    have hle : cnt A (p ^ 2 * q) a ≤ q := by
      have := cnt_le A dvd_p2q a
      rwa [div_p2q] at this
    exact step2 hpq A hi hii ha (lt_of_le_of_ne hle hne)
  -- so `A` is invariant under the translation by `p² q`
  have hinv : ∀ a ∈ A, a + ((p ^ 2 * q : ℕ) : ZMod (p ^ 2 * q ^ 2)) ∈ A := by
    intro a ha
    refine mem_of_cnt_eq A dvd_p2q a (by rw [hclaim a ha, div_p2q]) ?_
    rw [add_sub_cancel_left, dvd_val_iff dvd_p2q, map_natCast, ZMod.natCast_self]
  have himage : A.image (· + ((p ^ 2 * q : ℕ) : ZMod (p ^ 2 * q ^ 2))) = A :=
    Finset.eq_of_subset_of_card_le
      (fun x hx => by
        obtain ⟨a, ha, rfl⟩ := mem_image.1 hx
        exact hinv a ha)
      (by rw [Finset.card_image_of_injective _ (add_left_injective _)])
  -- hence its Fourier transform vanishes at the frequencies not killed by `p² q`
  intro ξ hξ
  have hsum : hat A ξ = ZMod.stdAddChar (ξ * ((p ^ 2 * q : ℕ) : ZMod (p ^ 2 * q ^ 2))) * hat A ξ := by
    unfold hat
    conv_lhs => rw [← himage]
    rw [Finset.sum_image (fun x _ y _ h => add_left_injective _ h), Finset.mul_sum]
    refine Finset.sum_congr rfl fun a _ => ?_
    rw [mul_add, AddChar.map_add_eq_mul, mul_comm]
  have hne : ξ * ((p ^ 2 * q : ℕ) : ZMod (p ^ 2 * q ^ 2)) ≠ 0 := by
    rw [Ne, Bridge.mul_natCast_eq_zero_iff, hξ]
    intro hdvd
    have h1 : p * q * q ∣ p * q * p := by
      have h2 : p * q * q = p * q ^ 2 := by ring
      have h3 : p * q * p = p ^ 2 * q := by ring
      rw [h2, h3]
      exact hdvd
    have h4 : q ∣ p := Nat.dvd_of_mul_dvd_mul_left (Nat.mul_pos hp'.pos hq'.pos) h1
    exact hpq ((Nat.prime_dvd_prime_iff_eq hq' hp').1 h4).symm
  have hne1 : ZMod.stdAddChar (ξ * ((p ^ 2 * q : ℕ) : ZMod (p ^ 2 * q ^ 2))) ≠ (1 : ℂ) :=
    fun h => hne ((DigitSets.stdAddChar_eq_one_iff _).1 h)
  have h0 : (1 - ZMod.stdAddChar (ξ * ((p ^ 2 * q : ℕ) : ZMod (p ^ 2 * q ^ 2)))) * hat A ξ = 0 := by
    linear_combination hsum
  exact (mul_eq_zero.1 h0).resolve_left (sub_ne_zero.2 hne1.symm)

end P2q2
