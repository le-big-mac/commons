/-
Lemma 5 of "weak tiles of Z_{p²q²} are tiles" (Lemma Y′ of `p2q2-notes-agent3.md`):
if `|A| = pq`, `p` is a zero of `A` and `p²q²` is a zero of `A`, then `pq²` is a zero of `A`.
Proved by counting residue classes: every element of `A` lies in a full class modulo `p²q`, so `A` is invariant under
translation by `p²q`.  (agent3 / Yonder)
-/
import Pqr.Periodic
import Pqr.CM

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

namespace L5

/-! ### Residue-class counts: a little more API -/

/-- `d ∣ w.val` iff `w` is zero modulo `d` -/
theorem dvd_val_iff {d : ℕ} (w : ZMod M) : d ∣ w.val ↔ (ZMod.cast w : ZMod d) = 0 := by
  rw [← ZMod.natCast_eq_zero_iff, ZMod.natCast_val]

/-- the count of a class modulo `d` depends only on the class -/
theorem cnt_congr (A : Finset (ZMod M)) {d : ℕ} (hd : d ∣ M) {a v : ZMod M} (h : d ∣ (a - v).val) :
    cnt A d a = cnt A d v := by
  unfold cnt
  congr 1
  refine Finset.filter_congr fun x _ => ?_
  rw [dvd_val_iff, dvd_val_iff, ZMod.cast_sub hd, ZMod.cast_sub hd]
  rw [dvd_val_iff, ZMod.cast_sub hd, sub_eq_zero] at h
  rw [h]

/-- adding a multiple of `d` does not change the class modulo `d` -/
theorem cnt_add_mul (A : Finset (ZMod M)) {d : ℕ} (hd : d ∣ M) (v : ZMod M) (k : ℕ) :
    cnt A d (v + ((k * d : ℕ) : ZMod M)) = cnt A d v := by
  apply cnt_congr A hd
  rw [add_sub_cancel_left, dvd_val_iff, ZMod.cast_natCast hd, Nat.cast_mul, ZMod.natCast_self, mul_zero]

/-- a finer class has at most as many elements -/
theorem cnt_mono (A : Finset (ZMod M)) {d d' : ℕ} (h : d ∣ d') (v : ZMod M) : cnt A d' v ≤ cnt A d v := by
  unfold cnt
  refine Finset.card_le_card fun a ha => ?_
  rw [Finset.mem_filter] at ha ⊢
  exact ⟨ha.1, h.trans ha.2⟩

/-- an element of `A` is counted in its own class -/
theorem one_le_cnt (A : Finset (ZMod M)) (d : ℕ) {a : ZMod M} (ha : a ∈ A) : 1 ≤ cnt A d a := by
  unfold cnt
  refine Finset.card_pos.2 ⟨a, ?_⟩
  rw [Finset.mem_filter]
  exact ⟨ha, by simp⟩

/-- a nonempty class contains an element of `A` -/
theorem exists_mem_of_cnt_pos (A : Finset (ZMod M)) (d : ℕ) {v : ZMod M} (h : 0 < cnt A d v) :
    ∃ a ∈ A, d ∣ (a - v).val := by
  unfold cnt at h
  obtain ⟨a, ha⟩ := Finset.card_pos.1 h
  rw [Finset.mem_filter] at ha
  exact ⟨a, ha.1, ha.2⟩

/-- modulo `M` itself the count is the indicator of `A` -/
theorem cnt_self (A : Finset (ZMod M)) (v : ZMod M) : cnt A M v = if v ∈ A then 1 else 0 := by
  classical
  unfold cnt
  have h1 : A.filter (fun a => M ∣ (a - v).val) = A.filter (fun a => a = v) := by
    refine Finset.filter_congr fun a _ => ?_
    constructor
    · intro h
      have h2 : (a - v).val = 0 := Nat.eq_zero_of_dvd_of_lt h (ZMod.val_lt _)
      exact sub_eq_zero.1 ((ZMod.val_eq_zero _).1 h2)
    · rintro rfl
      simp
  rw [h1, Finset.filter_eq' A v]
  split_ifs <;> simp

theorem cnt_self_le_one (A : Finset (ZMod M)) (v : ZMod M) : cnt A M v ≤ 1 := by
  rw [cnt_self]
  split_ifs <;> simp

/-- `n ≡ t d (mod d e)` iff `d ∣ n` and the next digit is `t` -/
theorem modEq_mul_iff {d e : ℕ} (hd : 0 < d) (n t : ℕ) (ht : t < e) :
    n ≡ t * d [MOD d * e] ↔ d ∣ n ∧ (n / d) % e = t := by
  constructor
  · intro h
    have h1 : d ∣ n := by
      have h2 : n ≡ t * d [MOD d] := h.of_dvd (dvd_mul_right d e)
      exact Nat.modEq_zero_iff_dvd.1 (h2.trans (Nat.modEq_zero_iff_dvd.2 (dvd_mul_left _ _)))
    refine ⟨h1, ?_⟩
    obtain ⟨m, rfl⟩ := h1
    rw [Nat.mul_div_cancel_left m hd]
    have h3 : d * m ≡ d * t [MOD d * e] := by rwa [mul_comm t] at h
    have h4 : m ≡ t [MOD e] := Nat.ModEq.mul_left_cancel' hd.ne' h3
    have h5 : m % e = t % e := h4
    rw [h5, Nat.mod_eq_of_lt ht]
  · rintro ⟨⟨m, rfl⟩, h2⟩
    rw [Nat.mul_div_cancel_left m hd] at h2
    have h4 : m ≡ t [MOD e] := by
      have h5 : m % e = t % e := by rw [h2, Nat.mod_eq_of_lt ht]
      exact h5
    rw [mul_comm t]
    exact Nat.ModEq.mul_left' _ h4

/-- **Splitting**: a class modulo `d` is the disjoint union of `e` classes modulo `d e`. -/
theorem cnt_split (A : Finset (ZMod M)) {d e : ℕ} (hd : 0 < d) (he : 0 < e) (h : d * e ∣ M)
    (v : ZMod M) :
    cnt A d v = ∑ t ∈ range e, cnt A (d * e) (v + ((t * d : ℕ) : ZMod M)) := by
  classical
  unfold cnt
  rw [Finset.card_eq_sum_card_fiberwise (f := fun x : ZMod M => ((x - v).val / d) % e)
    (t := range e) (fun x _ => mem_coe.2 (mem_range.2 (Nat.mod_lt _ he)))]
  refine Finset.sum_congr rfl fun t ht => ?_
  congr 1
  rw [Finset.filter_filter]
  refine Finset.filter_congr fun x _ => ?_
  rw [show x - (v + ((t * d : ℕ) : ZMod M)) = (x - v) - ((t * d : ℕ) : ZMod M) by ring,
    CM.dvd_val_sub_natCast h, modEq_mul_iff hd _ t (mem_range.1 ht)]

/-- a sum of `n` numbers, each at most 1, that equals `n` consists of ones -/
theorem all_one_of_sum_eq {n : ℕ} (f : ℕ → ℕ) (hf : ∀ t ∈ range n, f t ≤ 1)
    (hs : ∑ t ∈ range n, f t = n) : ∀ t ∈ range n, f t = 1 := by
  by_contra hne
  push Not at hne
  obtain ⟨t, ht, h1⟩ := hne
  have h2 : ∑ t ∈ range n, f t < ∑ _t ∈ range n, 1 :=
    Finset.sum_lt_sum hf ⟨t, ht, lt_of_le_of_ne (hf t ht) h1⟩
  simp at h2
  omega

/-- a sum of `n` numbers, each at most 1, that is less than `n` has a zero term -/
theorem exists_zero_of_sum_lt {n : ℕ} (f : ℕ → ℕ) (hf : ∀ t ∈ range n, f t ≤ 1)
    (hs : ∑ t ∈ range n, f t < n) : ∃ t ∈ range n, f t = 0 := by
  by_contra hne
  push Not at hne
  have h1 : ∀ t ∈ range n, f t = 1 := fun t ht => by
    have := hf t ht
    have := hne t ht
    omega
  rw [Finset.sum_congr rfl h1] at hs
  simp at hs

end L5

/-! ### The lemma, in counting form -/

/-- If every class modulo `p` holds `q` elements of `A` and, in every class modulo `pq`, the `p × q` array of `A` is
additive, then every element of `A` lies in a full class modulo `p²q`. -/
theorem translate_mem_of_counts (p q : ℕ) (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) (hM : M = p ^ 2 * q ^ 2)
    (A : Finset (ZMod M)) (hP : ∀ v, cnt A p v = q)
    (hadd : ∀ v, p * q * cnt A M v + cnt A (p * q) v = q * cnt A (p * q ^ 2) v + p * cnt A (p ^ 2 * q) v) :
    ∀ a ∈ A, a + ((p ^ 2 * q : ℕ) : ZMod M) ∈ A := by
  classical
  have hp0 : 0 < p := hp.pos
  have hq0 : 0 < q := hq.pos
  have hpndq : ¬ p ∣ q := fun h => hpq ((Nat.prime_dvd_prime_iff_eq hp hq).1 h)
  have dM1 : (p ^ 2 * q) * q = M := by rw [hM]; ring
  have dM2 : (p * q ^ 2) * p = M := by rw [hM]; ring
  have d1 : p ^ 2 * q ∣ M := ⟨q, dM1.symm⟩
  have d2 : p * q ^ 2 ∣ M := ⟨p, dM2.symm⟩
  have d3 : p * q ∣ M := ⟨p * q, by rw [hM]; ring⟩
  -- rows and columns of a box, as sums of the indicator
  have hRow : ∀ v, cnt A (p ^ 2 * q) v = ∑ t ∈ range q, cnt A M (v + ((t * (p ^ 2 * q) : ℕ) : ZMod M)) := by
    intro v
    have := L5.cnt_split A (d := p ^ 2 * q) (e := q) (by positivity) hq0 (by rw [dM1]) v
    rwa [dM1] at this
  have hCol : ∀ v, cnt A (p * q ^ 2) v = ∑ t ∈ range p, cnt A M (v + ((t * (p * q ^ 2) : ℕ) : ZMod M)) := by
    intro v
    have := L5.cnt_split A (d := p * q ^ 2) (e := p) (by positivity) hp0 (by rw [dM2]) v
    rwa [dM2] at this
  have hRow_le : ∀ v, cnt A (p ^ 2 * q) v ≤ q := by
    intro v
    rw [hRow v]
    calc ∑ t ∈ range q, cnt A M (v + ((t * (p ^ 2 * q) : ℕ) : ZMod M)) ≤ ∑ _t ∈ range q, 1 :=
          Finset.sum_le_sum fun t _ => L5.cnt_self_le_one A _
      _ = q := by simp
  have hCol_le : ∀ v, cnt A (p * q ^ 2) v ≤ p := by
    intro v
    rw [hCol v]
    calc ∑ t ∈ range p, cnt A M (v + ((t * (p * q ^ 2) : ℕ) : ZMod M)) ≤ ∑ _t ∈ range p, 1 :=
          Finset.sum_le_sum fun t _ => L5.cnt_self_le_one A _
      _ = p := by simp
  have hN_le : ∀ v, cnt A (p * q) v ≤ q := fun v => (L5.cnt_mono A (dvd_mul_right p q) v).trans (hP v).le
  -- Step A
  have stepA : ∀ a ∈ A, cnt A (p ^ 2 * q) a = q ∨
      (cnt A (p * q ^ 2) a = p ∧ cnt A (p * q) a = p * cnt A (p ^ 2 * q) a) := by
    intro a ha
    by_cases hr : cnt A (p ^ 2 * q) a = q
    · exact Or.inl hr
    right
    have hlt : cnt A (p ^ 2 * q) a < q := lt_of_le_of_ne (hRow_le a) hr
    rw [hRow a] at hlt
    obtain ⟨t, -, ht0⟩ := L5.exists_zero_of_sum_lt _ (fun t _ => L5.cnt_self_le_one A _) hlt
    set v := a + ((t * (p ^ 2 * q) : ℕ) : ZMod M) with hv
    have hRv : cnt A (p ^ 2 * q) v = cnt A (p ^ 2 * q) a := L5.cnt_add_mul A d1 a t
    have hNv : cnt A (p * q) v = cnt A (p * q) a := by
      have h1 : (t * (p ^ 2 * q) : ℕ) = (t * p) * (p * q) := by ring
      rw [hv, h1]
      exact L5.cnt_add_mul A d3 a (t * p)
    have ea := hadd a
    have ev := hadd v
    rw [L5.cnt_self, if_pos ha] at ea
    rw [ht0, hRv, hNv] at ev
    have hc := hCol_le a
    have h3 : q * cnt A (p * q ^ 2) a = q * (p + cnt A (p * q ^ 2) v) := by nlinarith
    have h4 : cnt A (p * q ^ 2) a = p + cnt A (p * q ^ 2) v := Nat.eq_of_mul_eq_mul_left hq0 h3
    have h5 : cnt A (p * q ^ 2) v = 0 := by omega
    refine ⟨by omega, ?_⟩
    rw [h5] at ev
    linarith
  -- Step B
  have stepB : ∀ a ∈ A, cnt A (p * q) a = q ∨ p ∣ cnt A (p * q) a := by
    intro a ha
    rcases stepA a ha with h | ⟨-, h⟩
    · left
      have ea := hadd a
      rw [L5.cnt_self, if_pos ha, h] at ea
      have h1 : cnt A (p * q) a = q * cnt A (p * q ^ 2) a := by linarith
      have h2 : 1 ≤ cnt A (p * q ^ 2) a := L5.one_le_cnt A _ ha
      have h3 := hN_le a
      have h4 : q * 1 ≤ q * cnt A (p * q ^ 2) a := Nat.mul_le_mul_left q h2
      omega
    · right
      exact ⟨_, h⟩
  -- Step C
  have stepC : ∀ v, cnt A (p * q) v = q ∨ p ∣ cnt A (p * q) v := by
    intro v
    rcases Nat.eq_zero_or_pos (cnt A (p * q) v) with h | h
    · right
      rw [h]
      exact dvd_zero p
    · obtain ⟨a, ha, hav⟩ := L5.exists_mem_of_cnt_pos A _ h
      rw [← L5.cnt_congr A d3 hav]
      exact stepB a ha
  -- Step D
  have hPsplit : ∀ v, cnt A p v = ∑ t ∈ range q, cnt A (p * q) (v + ((t * p : ℕ) : ZMod M)) :=
    fun v => L5.cnt_split A hp0 hq0 d3 v
  have stepD : ∀ a ∈ A, cnt A (p * q) a = q := by
    intro a ha
    by_contra hne
    have hdvd0 : p ∣ cnt A (p * q) a := (stepB a ha).resolve_left hne
    have hpos : 1 ≤ cnt A (p * q) a := L5.one_le_cnt A _ ha
    have hsum := hPsplit a
    rw [hP a] at hsum
    have h0 : cnt A (p * q) (a + ((0 * p : ℕ) : ZMod M)) = cnt A (p * q) a := by simp
    have hall : ∀ t ∈ range q, p ∣ cnt A (p * q) (a + ((t * p : ℕ) : ZMod M)) := by
      intro t ht
      rcases stepC (a + ((t * p : ℕ) : ZMod M)) with h | h
      · exfalso
        by_cases ht0 : t = 0
        · rw [ht0, h0] at h
          exact hne h
        · have hsub : ({0, t} : Finset ℕ) ⊆ range q := by
            intro x hx
            rcases Finset.mem_insert.1 hx with rfl | hx
            · exact Finset.mem_range.2 hq0
            · rw [Finset.mem_singleton.1 hx]; exact ht
          have h2 := Finset.sum_le_sum_of_subset (f := fun t => cnt A (p * q) (a + ((t * p : ℕ) : ZMod M))) hsub
          rw [Finset.sum_pair (Ne.symm ht0), h0, h, ← hsum] at h2
          omega
      · exact h
    exact hpndq (hsum ▸ Finset.dvd_sum hall)
  -- Step E
  have stepE : ∀ a ∈ A, cnt A (p ^ 2 * q) a = q := by
    intro a ha
    rcases stepA a ha with h | ⟨-, h⟩
    · exact h
    · exfalso
      rw [stepD a ha] at h
      exact hpndq ⟨_, h⟩
  -- Step F
  intro a ha
  have h1 := stepE a ha
  rw [hRow a] at h1
  have h2 := L5.all_one_of_sum_eq _ (fun t _ => L5.cnt_self_le_one A _) h1 1
    (Finset.mem_range.2 hq.one_lt)
  rw [one_mul, L5.cnt_self] at h2
  by_contra hna
  rw [if_neg hna] at h2
  exact zero_ne_one h2

/-- **Lemma 5.** In `ZMod (p² q²)`: if `|A| = pq`, `p` is a zero of `A` and `p²q²` is a zero of `A`, then `pq²` is a
zero of `A`. -/
theorem zeroAt_p_qsq_of_card (p q : ℕ) (hp : p.Prime) (hq : q.Prime) (hpq : p ≠ q) (hM : M = p ^ 2 * q ^ 2)
    (A : Finset (ZMod M)) (hcard : A.card = p * q) (h1 : ZeroAt A p) (h2 : ZeroAt A (p ^ 2 * q ^ 2)) :
    ZeroAt A (p * q ^ 2) := by
  have hpM : p ^ (0 + 1) ∣ M := ⟨p * q ^ 2, by rw [hM]; ring⟩
  have hP : ∀ v, cnt A p v = q := by
    intro v
    have h3 := (zeroAt_prime_pow A p hp 0 hpM).1 (by simpa using h1) v
    rw [zero_add, pow_one, pow_zero, cnt_one, hcard] at h3
    exact Nat.eq_of_mul_eq_mul_left hp.pos h3
  have hMM : p ^ (1 + 1) * q ^ (1 + 1) ∣ M := by rw [hM]
  have hadd : ∀ v, p * q * cnt A M v + cnt A (p * q) v = q * cnt A (p * q ^ 2) v + p * cnt A (p ^ 2 * q) v := by
    intro v
    have h3 := (zeroAt_prime_pow_mul_pow A p q hp hq hpq 1 1 hMM).1 (by simpa using h2) v
    simp only [pow_one] at h3
    rw [show (1 + 1 : ℕ) = 2 from rfl, ← hM] at h3
    exact h3
  refine zeroAt_of_translate A (p ^ 2 * q) (translate_mem_of_counts p q hp hq hpq hM A hP hadd) _ ?_
  intro h
  have h4 : p * q * q ∣ p * q * p := by
    have : p * q ^ 2 = p * q * q := by ring
    have h' : p ^ 2 * q = p * q * p := by ring
    rwa [this, h'] at h
  have h5 : q ∣ p := Nat.dvd_of_mul_dvd_mul_left (Nat.mul_pos hp.pos hq.pos) h4
  exact hpq ((Nat.prime_dvd_prime_iff_eq hq hp).1 h5).symm

end Pqr
