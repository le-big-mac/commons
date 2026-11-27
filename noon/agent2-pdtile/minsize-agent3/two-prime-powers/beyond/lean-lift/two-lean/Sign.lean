/-
The lemma on signs.  For odd primes `p ≠ q`, the elements of a nonempty multiset on `ZMod (p^a * q^b)` can be given signs `+`, `-`
so that the signed mask polynomial is divisible by no cyclotomic polynomial `Φ_d` with `d ∣ p^a * q^b` (`d = 1` included).
A signing is given as a splitting `w = u + v` into the elements signed `+` and those signed `-`; the signed mask is
`maskW u - maskW v`.
(Statement fixed by agent3 / Yonder on 26 November 2026, before any Lean proof of it.  The lemma and its proof on paper are due to
a fresh instance to which I had put the statement as a question.)
-/
import Pnq.Weighted

open Finset

namespace Pnq

namespace Lift

namespace SignAux

/-! ### Signings

A signing of the multiset `w` is given, in this namespace, by the function `g = u - v : ι → ℤ`
(the number of copies signed `+` minus the number signed `-`): `|g x| ≤ w x` and `g x ≡ w x`
modulo `2`.  Everything here is on a finite type `ι` with an arbitrary "exponent" map `e : ι → ℕ`
(for the theorem, `ι = ZMod n` and `e = ZMod.val`); no group structure is used. -/

/-- `g` is a signing of `w`: `|g x| ≤ w x` and `g x ≡ w x` modulo `2` -/
def Valid {ι : Type*} (w : ι → ℕ) (g : ι → ℤ) : Prop :=
  ∀ x, -(w x : ℤ) ≤ g x ∧ g x ≤ (w x : ℤ) ∧ ((w x : ℤ) - g x) % 2 = 0

/-- the sum of `g` over the elements whose exponent is congruent to `c` modulo `L` -/
def sig {ι : Type*} [Fintype ι] (e : ι → ℕ) (g : ι → ℤ) (L c : ℕ) : ℤ :=
  ∑ x, if e x % L = c % L then g x else 0

/-- A set `s` of elements can be signed with any total `τ` of the right size and parity. -/
theorem exists_sum_eq {ι : Type*} (w : ι → ℕ) (s : Finset ι) :
    ∀ τ : ℤ, -((∑ x ∈ s, w x : ℕ) : ℤ) ≤ τ → τ ≤ ((∑ x ∈ s, w x : ℕ) : ℤ) →
      (((∑ x ∈ s, w x : ℕ) : ℤ) - τ) % 2 = 0 → ∃ g : ι → ℤ, Valid w g ∧ ∑ x ∈ s, g x = τ := by
  classical
  induction s using Finset.induction_on with
  | empty =>
    intro τ h1 h2 _
    have hval : Valid w fun x => (w x : ℤ) := by
      intro x
      change -(w x : ℤ) ≤ (w x : ℤ) ∧ (w x : ℤ) ≤ (w x : ℤ) ∧ ((w x : ℤ) - (w x : ℤ)) % 2 = 0
      omega
    refine ⟨fun x => (w x : ℤ), hval, ?_⟩
    rw [Finset.sum_empty] at h1 h2
    rw [Finset.sum_empty]
    omega
  | insert y s hy ih =>
    intro τ h1 h2 h3
    rw [Finset.sum_insert hy] at h1 h2 h3
    obtain ⟨h, ha, hb, hc, hd, he, hf⟩ : ∃ h : ℤ, -(w y : ℤ) ≤ h ∧ h ≤ (w y : ℤ) ∧
        ((w y : ℤ) - h) % 2 = 0 ∧ -((∑ x ∈ s, w x : ℕ) : ℤ) ≤ τ - h ∧
        τ - h ≤ ((∑ x ∈ s, w x : ℕ) : ℤ) ∧ (((∑ x ∈ s, w x : ℕ) : ℤ) - (τ - h)) % 2 = 0 := by
      rcases le_total (-(w y : ℤ)) (τ - ((∑ x ∈ s, w x : ℕ) : ℤ)) with hle | hle
      · exact ⟨τ - ((∑ x ∈ s, w x : ℕ) : ℤ), by omega, by omega, by omega, by omega, by omega,
          by omega⟩
      · exact ⟨-(w y : ℤ), by omega, by omega, by omega, by omega, by omega, by omega⟩
    obtain ⟨g, hg, hgs⟩ := ih (τ - h) hd he hf
    refine ⟨Function.update g y h, fun x => ?_, ?_⟩
    · by_cases hx : x = y
      · subst hx
        rw [Function.update_self]
        exact ⟨ha, hb, hc⟩
      · rw [Function.update_of_ne hx]
        exact hg x
    · have hne : ∀ x ∈ s, Function.update g y h x = g x := fun x hx =>
        Function.update_of_ne (ne_of_mem_of_not_mem hx hy) _ _
      rw [Finset.sum_insert hy, Function.update_self, Finset.sum_congr rfl hne, hgs]
      ring

/-- a set with an even number of elements can be signed with total `0` -/
theorem exists_sum_zero {ι : Type*} (w : ι → ℕ) (s : Finset ι)
    (h : (∑ x ∈ s, w x) % 2 = 0) : ∃ g : ι → ℤ, Valid w g ∧ ∑ x ∈ s, g x = 0 :=
  exists_sum_eq w s 0 (by omega) (by omega) (by omega)

/-- a set with an odd number of elements can be signed with total `1` -/
theorem exists_sum_one {ι : Type*} (w : ι → ℕ) (s : Finset ι)
    (h : (∑ x ∈ s, w x) % 2 = 1) : ∃ g : ι → ℤ, Valid w g ∧ ∑ x ∈ s, g x = 1 :=
  exists_sum_eq w s 1 (by omega) (by omega) (by omega)

/-- a set with an odd number of elements can be signed with total `-1` -/
theorem exists_sum_neg_one {ι : Type*} (w : ι → ℕ) (s : Finset ι)
    (h : (∑ x ∈ s, w x) % 2 = 1) : ∃ g : ι → ℤ, Valid w g ∧ ∑ x ∈ s, g x = -1 :=
  exists_sum_eq w s (-1) (by omega) (by omega) (by omega)

/-- a nonempty set can be signed with a total not divisible by `q` (the total is `1` or `2`) -/
theorem exists_base {ι : Type*} (q : ℕ) (hq2 : ¬ (q : ℤ) ∣ 2) (w : ι → ℕ)
    (s : Finset ι) (hs : ∑ x ∈ s, w x ≠ 0) : ∃ g : ι → ℤ, Valid w g ∧ ¬ (q : ℤ) ∣ ∑ x ∈ s, g x := by
  rcases Nat.mod_two_eq_zero_or_one (∑ x ∈ s, w x) with h | h
  · obtain ⟨g, hg, hgs⟩ := exists_sum_eq w s 2 (by omega) (by omega) (by omega)
    exact ⟨g, hg, by rw [hgs]; exact hq2⟩
  · obtain ⟨g, hg, hgs⟩ := exists_sum_one w s h
    refine ⟨g, hg, ?_⟩
    rw [hgs]
    exact fun h1 => hq2 (dvd_trans h1 (one_dvd 2))

/-- the greedy step: a set can be signed so that a total `T` not divisible by `q` stays so (the
set gets `0` if its number of elements is even and `1` or `-1` if it is odd) -/
theorem exists_greedy {ι : Type*} (q : ℕ) (hq2 : ¬ (q : ℤ) ∣ 2) (w : ι → ℕ)
    (s : Finset ι) (T : ℤ) (hT : ¬ (q : ℤ) ∣ T) :
    ∃ g : ι → ℤ, Valid w g ∧ ¬ (q : ℤ) ∣ T + ∑ x ∈ s, g x := by
  rcases Nat.mod_two_eq_zero_or_one (∑ x ∈ s, w x) with h | h
  · obtain ⟨g, hg, hs⟩ := exists_sum_zero w s h
    exact ⟨g, hg, by rw [hs, add_zero]; exact hT⟩
  · by_cases hd : (q : ℤ) ∣ T + 1
    · obtain ⟨g, hg, hs⟩ := exists_sum_neg_one w s h
      refine ⟨g, hg, ?_⟩
      rw [hs]
      intro hd'
      apply hq2
      have h2 := dvd_sub hd hd'
      have e : T + 1 - (T + -1) = 2 := by ring
      rwa [e] at h2
    · obtain ⟨g, hg, hs⟩ := exists_sum_one w s h
      exact ⟨g, hg, by rw [hs]; exact hd⟩

/-- One level of the construction.  Two sibling classes `D1`, `D2` and the rest `R` of the
siblings are signed so that the total stays away from `0` modulo `q`, and so that two of the three
classes with the totals `T` (the class already signed), `∑ D1`, `∑ D2` have different totals
modulo `q`. -/
theorem step3 {ι : Type*} (q : ℕ) (hq2 : ¬ (q : ℤ) ∣ 2) (w : ι → ℕ)
    (D1 D2 R : Finset ι) (T : ℤ) (hT : ¬ (q : ℤ) ∣ T) :
    ∃ h1 h2 hR : ι → ℤ, Valid w h1 ∧ Valid w h2 ∧ Valid w hR ∧
      ¬ (q : ℤ) ∣ T + (∑ x ∈ D1, h1 x) + (∑ x ∈ D2, h2 x) + (∑ x ∈ R, hR x) ∧
      (¬ (q : ℤ) ∣ (∑ x ∈ D1, h1 x) - T ∨ ¬ (q : ℤ) ∣ (∑ x ∈ D2, h2 x) - T ∨
        ¬ (q : ℤ) ∣ (∑ x ∈ D1, h1 x) - (∑ x ∈ D2, h2 x)) := by
  rcases Nat.mod_two_eq_zero_or_one (∑ x ∈ D1, w x) with e1 | o1
  · obtain ⟨h1, hv1, hs1⟩ := exists_sum_zero w D1 e1
    obtain ⟨h2, hv2, hs2⟩ := exists_greedy q hq2 w D2 T hT
    obtain ⟨hR, hvR, hsR⟩ := exists_greedy q hq2 w R _ hs2
    refine ⟨h1, h2, hR, hv1, hv2, hvR, ?_, Or.inl ?_⟩
    · rw [hs1, add_zero]
      exact hsR
    · rw [hs1, zero_sub, dvd_neg]
      exact hT
  · rcases Nat.mod_two_eq_zero_or_one (∑ x ∈ D2, w x) with e2 | o2
    · obtain ⟨h2, hv2, hs2⟩ := exists_sum_zero w D2 e2
      obtain ⟨h1, hv1, hs1⟩ := exists_greedy q hq2 w D1 T hT
      obtain ⟨hR, hvR, hsR⟩ := exists_greedy q hq2 w R _ hs1
      refine ⟨h1, h2, hR, hv1, hv2, hvR, ?_, Or.inr (Or.inl ?_)⟩
      · rw [hs2, add_zero]
        exact hsR
      · rw [hs2, zero_sub, dvd_neg]
        exact hT
    · obtain ⟨h1, hv1, hs1⟩ := exists_sum_one w D1 o1
      obtain ⟨h2, hv2, hs2⟩ := exists_sum_neg_one w D2 o2
      obtain ⟨hR, hvR, hsR⟩ := exists_greedy q hq2 w R T hT
      refine ⟨h1, h2, hR, hv1, hv2, hvR, ?_, Or.inr (Or.inr ?_)⟩
      · rw [hs1, hs2]
        have e : T + 1 + -1 = T := by ring
        rw [e]
        exact hsR
      · rw [hs1, hs2]
        have e : (1 : ℤ) - -1 = 2 := by norm_num
        rw [e]
        exact hq2

/-- the class of `n` modulo `p * M`, in terms of its last digit in base `p` and of `n / p` -/
theorem mod_mul_iff (p M r c n : ℕ) (hr : r < p) :
    n % (p * M) = (r + p * c) % (p * M) ↔ n % p = r ∧ n / p % M = c % M := by
  have hp : 0 < p := by omega
  rw [Nat.mod_mul, Nat.mod_mul, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hr,
    Nat.add_mul_div_left _ _ hp, Nat.div_eq_of_lt hr, zero_add]
  constructor
  · intro h
    have h1 : n % p = r := by
      have h2 := congrArg (fun k => k % p) h
      simp only [Nat.add_mul_mod_self_left, Nat.mod_mod, Nat.mod_eq_of_lt hr] at h2
      exact h2
    refine ⟨h1, ?_⟩
    rw [h1] at h
    exact Nat.eq_of_mul_eq_mul_left hp (Nat.add_left_cancel h)
  · rintro ⟨h1, h2⟩
    rw [h1, h2]

/-- two classes with different totals, in the form used below -/
theorem wit_of_ne {ι : Type*} [Fintype ι] (q : ℕ) (e : ι → ℕ) (g : ι → ℤ) (L c c' : ℕ)
    (h : ¬ (q : ℤ) ∣ sig e g L c - sig e g L c') :
    ∃ c0 t : ℕ, ¬ (q : ℤ) ∣ sig e g L c0 - sig e g L (c0 + t * 1) := by
  rcases le_total c c' with hle | hle
  · exact ⟨c, c' - c, by rwa [mul_one, Nat.add_sub_cancel' hle]⟩
  · refine ⟨c', c - c', ?_⟩
    rw [mul_one, Nat.add_sub_cancel' hle, dvd_sub_comm]
    exact h

/-- **The signs.**  For `p ≥ 3` and `q ∤ 2`: a nonempty multiset `w` on `ι` has a signing `g`
whose total is not divisible by `q` and such that at every level `i < a` there are two classes
modulo `p^(i+1)`, congruent modulo `p^i`, whose totals differ modulo `q`.  Induction on `a`, from
the root down: the class modulo `p` of a chosen element is signed by the statement for `a - 1`
(with the exponents divided by `p`), the other classes modulo `p` by `step3`. -/
theorem exists_good (p q : ℕ) (hp3 : 3 ≤ p) (hq2 : ¬ (q : ℤ) ∣ 2) {ι : Type*} [Fintype ι] :
    ∀ (a : ℕ) (e : ι → ℕ) (w : ι → ℕ), (∃ x, w x ≠ 0) →
      ∃ g : ι → ℤ, Valid w g ∧ ¬ (q : ℤ) ∣ ∑ x, g x ∧
        ∀ i, i < a → ∃ c t : ℕ,
          ¬ (q : ℤ) ∣ sig e g (p ^ (i + 1)) c - sig e g (p ^ (i + 1)) (c + t * p ^ i) := by
  intro a
  induction a with
  | zero =>
    intro e w hw
    obtain ⟨xs, hxs⟩ := hw
    have hne : ∑ x, w x ≠ 0 := fun h0 =>
      hxs ((Finset.sum_eq_zero_iff.1 h0) xs (Finset.mem_univ xs))
    obtain ⟨g, hv, hg⟩ := exists_base q hq2 w Finset.univ hne
    exact ⟨g, hv, hg, fun i hi => absurd hi (Nat.not_lt_zero i)⟩
  | succ a ih =>
    intro e w hw
    obtain ⟨xs, hxs⟩ := hw
    have hp0 : 0 < p := by omega
    obtain ⟨r, hr⟩ : ∃ r, r = e xs % p := ⟨_, rfl⟩
    have hrp : r < p := hr ▸ Nat.mod_lt _ hp0
    -- the class of `xs` modulo `p`, by induction
    obtain ⟨g', hv', hT, hW⟩ := ih (fun x => e x / p) (fun x => if e x % p = r then w x else 0)
      ⟨xs, by rw [ite_eq_left hr.symm]; exact hxs⟩
    have hv'r : ∀ x, e x % p = r →
        -(w x : ℤ) ≤ g' x ∧ g' x ≤ (w x : ℤ) ∧ ((w x : ℤ) - g' x) % 2 = 0 := by
      intro x hx
      have h := hv' x
      simp only [ite_eq_left hx] at h
      exact h
    have hz : ∀ x, e x % p ≠ r → g' x = 0 := by
      intro x hx
      have h := hv' x
      simp only [ite_eq_right hx] at h
      omega
    -- two other classes modulo `p`
    obtain ⟨t1, t2, ht1, ht2, h12, h1r, h2r⟩ :
        ∃ t1 t2 : ℕ, t1 < p ∧ t2 < p ∧ t1 ≠ t2 ∧ t1 ≠ r ∧ t2 ≠ r := by
      rcases Nat.lt_or_ge r 1 with h | h
      · exact ⟨1, 2, by omega, by omega, by omega, by omega, by omega⟩
      · rcases Nat.lt_or_ge r 2 with h' | h'
        · exact ⟨0, 2, by omega, by omega, by omega, by omega, by omega⟩
        · exact ⟨0, 1, by omega, by omega, by omega, by omega, by omega⟩
    obtain ⟨h1, h2, hR, hv1, hv2, hvR, htot, hwit⟩ := step3 q hq2 w
      (Finset.univ.filter fun x => e x % p = t1) (Finset.univ.filter fun x => e x % p = t2)
      (Finset.univ.filter fun x => e x % p ≠ r ∧ e x % p ≠ t1 ∧ e x % p ≠ t2) (∑ x, g' x) hT
    simp only [Finset.sum_filter] at htot hwit
    -- the signing
    obtain ⟨g, hg⟩ : ∃ g : ι → ℤ, g = fun x => if e x % p = r then g' x else
        if e x % p = t1 then h1 x else if e x % p = t2 then h2 x else hR x := ⟨_, rfl⟩
    have hg_r : ∀ x, e x % p = r → g x = g' x := by
      intro x hx
      rw [hg]
      exact ite_eq_left hx
    have hg_1 : ∀ x, e x % p = t1 → g x = h1 x := by
      intro x hx
      have hxr : ¬ e x % p = r := by omega
      rw [hg]
      exact (ite_eq_right hxr).trans (ite_eq_left hx)
    have hg_2 : ∀ x, e x % p = t2 → g x = h2 x := by
      intro x hx
      have hxr : ¬ e x % p = r := by omega
      have hx1 : ¬ e x % p = t1 := by omega
      rw [hg]
      exact (ite_eq_right hxr).trans ((ite_eq_right hx1).trans (ite_eq_left hx))
    have hg_R : ∀ x, e x % p ≠ r → e x % p ≠ t1 → e x % p ≠ t2 → g x = hR x := by
      intro x hxr hx1 hx2
      rw [hg]
      exact (ite_eq_right hxr).trans ((ite_eq_right hx1).trans (ite_eq_right hx2))
    -- it is a signing of `w`
    have hvg : Valid w g := by
      intro x
      by_cases hx : e x % p = r
      · rw [hg_r x hx]
        exact hv'r x hx
      · by_cases hx1 : e x % p = t1
        · rw [hg_1 x hx1]
          exact hv1 x
        · by_cases hx2 : e x % p = t2
          · rw [hg_2 x hx2]
            exact hv2 x
          · rw [hg_R x hx hx1 hx2]
            exact hvR x
    -- its total
    have hsum : ∑ x, g x = ∑ x, g' x + (∑ x, if e x % p = t1 then h1 x else 0)
        + (∑ x, if e x % p = t2 then h2 x else 0)
        + (∑ x, if e x % p ≠ r ∧ e x % p ≠ t1 ∧ e x % p ≠ t2 then hR x else 0) := by
      rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
      refine Finset.sum_congr rfl fun x _ => ?_
      by_cases hx : e x % p = r
      · have e1 : ¬ e x % p = t1 := by omega
        have e2 : ¬ e x % p = t2 := by omega
        have e3 : ¬ (e x % p ≠ r ∧ e x % p ≠ t1 ∧ e x % p ≠ t2) := fun h => h.1 hx
        rw [hg_r x hx, ite_eq_right e1, ite_eq_right e2, ite_eq_right e3]
        ring
      · by_cases hx1 : e x % p = t1
        · have e2 : ¬ e x % p = t2 := by omega
          have e3 : ¬ (e x % p ≠ r ∧ e x % p ≠ t1 ∧ e x % p ≠ t2) := fun h => h.2.1 hx1
          rw [hg_1 x hx1, hz x hx, ite_eq_left hx1, ite_eq_right e2, ite_eq_right e3]
          ring
        · by_cases hx2 : e x % p = t2
          · have e3 : ¬ (e x % p ≠ r ∧ e x % p ≠ t1 ∧ e x % p ≠ t2) := fun h => h.2.2 hx2
            rw [hg_2 x hx2, hz x hx, ite_eq_right hx1, ite_eq_left hx2, ite_eq_right e3]
            ring
          · rw [hg_R x hx hx1 hx2, hz x hx, ite_eq_right hx1, ite_eq_right hx2,
              ite_eq_left ⟨hx, hx1, hx2⟩]
            ring
    -- the totals of the classes modulo `p`
    have hs : ∀ t, t < p → sig e g (p ^ (0 + 1)) t = ∑ x, if e x % p = t then g x else 0 := by
      intro t ht
      unfold sig
      rw [zero_add, pow_one, Nat.mod_eq_of_lt ht]
    have hs_r : sig e g (p ^ (0 + 1)) r = ∑ x, g' x := by
      rw [hs r hrp]
      refine Finset.sum_congr rfl fun x _ => ?_
      by_cases hx : e x % p = r
      · rw [ite_eq_left hx, hg_r x hx]
      · rw [ite_eq_right hx, hz x hx]
    have hs_1 : sig e g (p ^ (0 + 1)) t1 = ∑ x, if e x % p = t1 then h1 x else 0 := by
      rw [hs t1 ht1]
      refine Finset.sum_congr rfl fun x _ => ?_
      by_cases hx : e x % p = t1
      · rw [ite_eq_left hx, ite_eq_left hx, hg_1 x hx]
      · rw [ite_eq_right hx, ite_eq_right hx]
    have hs_2 : sig e g (p ^ (0 + 1)) t2 = ∑ x, if e x % p = t2 then h2 x else 0 := by
      rw [hs t2 ht2]
      refine Finset.sum_congr rfl fun x _ => ?_
      by_cases hx : e x % p = t2
      · rw [ite_eq_left hx, ite_eq_left hx, hg_2 x hx]
      · rw [ite_eq_right hx, ite_eq_right hx]
    -- the totals of the classes modulo `p^(i+2)` inside the class of `xs` modulo `p`
    have hlift : ∀ i c : ℕ,
        sig e g (p ^ (i + 1 + 1)) (r + p * c) = sig (fun x => e x / p) g' (p ^ (i + 1)) c := by
      intro i c
      unfold sig
      refine Finset.sum_congr rfl fun x _ => ?_
      have key := mod_mul_iff p (p ^ (i + 1)) r c (e x) hrp
      rw [pow_succ' p (i + 1)]
      by_cases hx : e x % p = r
      · rw [hg_r x hx]
        by_cases hc : e x / p % p ^ (i + 1) = c % p ^ (i + 1)
        · rw [ite_eq_left (key.2 ⟨hx, hc⟩), ite_eq_left hc]
        · rw [ite_eq_right fun h => hc (key.1 h).2, ite_eq_right hc]
      · rw [ite_eq_right fun h => hx (key.1 h).1, hz x hx, ite_self]
    refine ⟨g, hvg, ?_, ?_⟩
    · rw [hsum]
      exact htot
    · intro i hi
      cases i with
      | zero =>
        rw [pow_zero]
        rcases hwit with hw1 | hw2 | hw12
        · exact wit_of_ne q e g _ t1 r (by rw [hs_1, hs_r]; exact hw1)
        · exact wit_of_ne q e g _ t2 r (by rw [hs_2, hs_r]; exact hw2)
        · exact wit_of_ne q e g _ t1 t2 (by rw [hs_1, hs_2]; exact hw12)
      | succ i =>
        obtain ⟨c, t, hct⟩ := hW i (by omega)
        refine ⟨r + p * c, t, ?_⟩
        have e1 : r + p * c + t * p ^ (i + 1) = r + p * (c + t * p ^ i) := by ring
        rw [e1, hlift, hlift]
        exact hct

/-! ### What has to be avoided -/

/-- the sum of the coefficients of a polynomial at the exponents congruent to `c` modulo `L`, as a
linear map -/
noncomputable def lam (R : Type*) [CommRing R] (L c : ℕ) : Polynomial R →ₗ[R] R :=
  Polynomial.lsum fun n => if n % L = c % L then LinearMap.id else 0

theorem lam_monomial (R : Type*) [CommRing R] (L c n : ℕ) (r : R) :
    lam R L c (Polynomial.monomial n r) = if n % L = c % L then r else 0 := by
  unfold lam
  rw [Polynomial.lsum_apply, Polynomial.sum_monomial_index]
  · split_ifs <;> simp
  · split_ifs <;> simp

/-- multiplication by `X^m` moves the classes modulo `L` by `m` -/
theorem lam_X_pow_mul (R : Type*) [CommRing R] (L c c' m : ℕ)
    (h : ∀ n, (n + m) % L = c % L ↔ n % L = c' % L) (f : Polynomial R) :
    lam R L c (Polynomial.X ^ m * f) = lam R L c' f := by
  induction f using Polynomial.induction_on' with
  | add f1 f2 h1 h2 => rw [mul_add, map_add, map_add, h1, h2]
  | monomial n r =>
    rw [Polynomial.X_pow_mul_monomial, lam_monomial, lam_monomial]
    simp only [h n]

/-- a multiple of `X^L - 1` has the sum `0` of coefficients in every class of exponents modulo
`L` -/
theorem lam_eq_zero_of_dvd (R : Type*) [CommRing R] (L c : ℕ) (F : Polynomial R)
    (h : Polynomial.X ^ L - 1 ∣ F) : lam R L c F = 0 := by
  obtain ⟨k, rfl⟩ := h
  rw [sub_mul, one_mul, map_sub,
    lam_X_pow_mul R L c c L (fun n => by rw [Nat.add_mod_right]) k, sub_self]

theorem lam_sum (R : Type*) [CommRing R] {ι : Type*} [Fintype ι] (e : ι → ℕ) (γ : ι → R)
    (L c : ℕ) :
    lam R L c (∑ x, Polynomial.C (γ x) * Polynomial.X ^ e x)
      = ∑ x, if e x % L = c % L then γ x else 0 := by
  rw [map_sum]
  refine Finset.sum_congr rfl fun x _ => ?_
  rw [Polynomial.C_mul_X_pow_eq_monomial, lam_monomial]

/-- If `X^L - 1` divides `(X^m - 1) * ∑ γ(x) X^(e x)`, the class sums of `γ` modulo `L` are
invariant under the shift by `m`. -/
theorem class_sum_shift (R : Type*) [CommRing R] {ι : Type*} [Fintype ι] (e : ι → ℕ) (γ : ι → R)
    (L m c : ℕ)
    (h : Polynomial.X ^ L - 1 ∣
      (Polynomial.X ^ m - 1) * ∑ x, Polynomial.C (γ x) * Polynomial.X ^ e x) :
    (∑ x, if e x % L = c % L then γ x else 0) = ∑ x, if e x % L = (c + m) % L then γ x else 0 := by
  have hs : ∀ n, (n + m) % L = (c + m) % L ↔ n % L = c % L := fun n =>
    ⟨fun h' => Nat.ModEq.add_right_cancel' m h', fun h' => Nat.ModEq.add_right m h'⟩
  have h0 := lam_eq_zero_of_dvd R L (c + m) _ h
  rw [sub_mul, one_mul, map_sub, lam_X_pow_mul R L (c + m) c m hs, lam_sum, lam_sum,
    sub_eq_zero] at h0
  exact h0

/-- **What has to be avoided.**  If the total of `g` is not divisible by `q` and at every level
`i < a` two classes modulo `p^(i+1)` that are congruent modulo `p^i` have totals that differ
modulo `q`, then no `Φ_(p^i q^j)` with `i ≤ a` divides `∑ g(x) X^(e x)`. -/
theorem not_cyclotomic_dvd (p q : ℕ) [hp : Fact p.Prime] [hq : Fact q.Prime] (hpq : p ≠ q)
    {ι : Type*} [Fintype ι] (e : ι → ℕ) (g : ι → ℤ) (a : ℕ) (h1 : ¬ (q : ℤ) ∣ ∑ x, g x)
    (h2 : ∀ i, i < a → ∃ c t : ℕ,
      ¬ (q : ℤ) ∣ sig e g (p ^ (i + 1)) c - sig e g (p ^ (i + 1)) (c + t * p ^ i))
    (i j : ℕ) (hi : i ≤ a) :
    ¬ Polynomial.cyclotomic (p ^ i * q ^ j) ℤ ∣ ∑ x, Polynomial.C (g x) * Polynomial.X ^ e x := by
  intro hdvd
  -- modulo `q`
  have hmap : Polynomial.cyclotomic (p ^ i * q ^ j) (ZMod q) ∣
      ∑ x, Polynomial.C ((g x : ℤ) : ZMod q) * Polynomial.X ^ e x := by
    have h := Polynomial.map_dvd (Int.castRingHom (ZMod q)) hdvd
    rw [Polynomial.map_cyclotomic, Polynomial.map_sum] at h
    have e1 : ∀ x, Polynomial.map (Int.castRingHom (ZMod q))
        (Polynomial.C (g x) * Polynomial.X ^ e x)
          = Polynomial.C ((g x : ℤ) : ZMod q) * Polynomial.X ^ e x := by
      intro x
      rw [Polynomial.map_mul, Polynomial.map_C, Polynomial.map_pow, Polynomial.map_X]
      rfl
    rw [Finset.sum_congr rfl fun x _ => e1 x] at h
    exact h
  -- `Φ_(p^i)` divides modulo `q`
  have hpi : Polynomial.cyclotomic (p ^ i) (ZMod q) ∣
      ∑ x, Polynomial.C ((g x : ℤ) : ZMod q) * Polynomial.X ^ e x := by
    rcases Nat.eq_zero_or_pos j with hj | hj
    · rw [hj, pow_zero, mul_one] at hmap
      exact hmap
    · have hnd : ¬ q ∣ p ^ i := fun h =>
        hpq ((Nat.prime_dvd_prime_iff_eq hq.out hp.out).1 (hq.out.dvd_of_dvd_pow h)).symm
      rw [mul_comm, Polynomial.cyclotomic_mul_prime_pow_eq (ZMod q) hnd hj] at hmap
      have hlt : q ^ (j - 1) < q ^ j := Nat.pow_lt_pow_right hq.out.one_lt (Nat.sub_lt hj one_pos)
      exact (dvd_pow_self _ (Nat.sub_ne_zero_of_lt hlt)).trans hmap
  rcases Nat.eq_zero_or_pos i with hi0 | hipos
  · -- `X - 1` divides modulo `q`: the total is `0` modulo `q`
    rw [hi0, pow_zero, Polynomial.cyclotomic_one] at hpi
    obtain ⟨k, hk⟩ := hpi
    have h3 := congrArg (Polynomial.eval 1) hk
    simp only [Polynomial.eval_finsetSum, Polynomial.eval_mul, Polynomial.eval_C,
      Polynomial.eval_pow, Polynomial.eval_X, one_pow, mul_one, Polynomial.eval_sub,
      Polynomial.eval_one, sub_self, zero_mul] at h3
    apply h1
    rw [← ZMod.intCast_zmod_eq_zero_iff_dvd, Int.cast_sum]
    exact h3
  · obtain ⟨k, rfl⟩ : ∃ k, i = k + 1 := ⟨i - 1, by omega⟩
    obtain ⟨c, t, hct⟩ := h2 k (by omega)
    apply hct
    have hd1 : (Polynomial.X ^ p ^ (k + 1) - 1 : Polynomial (ZMod q)) ∣
        (Polynomial.X ^ (t * p ^ k) - 1) *
          ∑ x, Polynomial.C ((g x : ℤ) : ZMod q) * Polynomial.X ^ e x := by
      rw [← Polynomial.cyclotomic_prime_pow_mul_X_pow_sub_one (ZMod q) p k, mul_comm]
      refine mul_dvd_mul ?_ hpi
      have h4 := sub_dvd_pow_sub_pow (Polynomial.X ^ p ^ k : Polynomial (ZMod q)) 1 t
      rw [one_pow, ← pow_mul, mul_comm (p ^ k) t] at h4
      exact h4
    have h5 := class_sum_shift (ZMod q) e (fun x => ((g x : ℤ) : ZMod q)) (p ^ (k + 1))
      (t * p ^ k) c hd1
    rw [← ZMod.intCast_zmod_eq_zero_iff_dvd]
    unfold sig
    rw [Int.cast_sub, Int.cast_sum, Int.cast_sum, sub_eq_zero]
    have e2 : ∀ (P : Prop) [Decidable P] (z : ℤ),
        (((if P then z else 0 : ℤ)) : ZMod q) = if P then ((z : ℤ) : ZMod q) else 0 := by
      intro P _ z
      split_ifs
      · rfl
      · exact Int.cast_zero
    simp only [e2]
    exact h5

end SignAux

/-- **The lemma on signs.** -/
theorem exists_signs (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hp : p ≠ 2) (hq : q ≠ 2) (hpq : p ≠ q) (a b : ℕ)
    (w : ZMod (p ^ a * q ^ b) → ℕ) (hw : ∃ x, w x ≠ 0) :
    ∃ u v : ZMod (p ^ a * q ^ b) → ℕ, (∀ x, u x + v x = w x) ∧
      ∀ d, d ∣ p ^ a * q ^ b → ¬ Polynomial.cyclotomic d ℤ ∣ maskW u - maskW v := by
  have hpP : p.Prime := Fact.out
  have hqP : q.Prime := Fact.out
  have hp3 : 3 ≤ p := by
    have := hpP.two_le
    omega
  have hq2 : ¬ (q : ℤ) ∣ 2 := by
    intro h
    have h' : q ∣ 2 := by exact_mod_cast h
    have := Nat.le_of_dvd (by norm_num) h'
    have := hqP.two_le
    omega
  obtain ⟨g, hv, hg1, hg2⟩ := SignAux.exists_good p q hp3 hq2 a
    (fun x : ZMod (p ^ a * q ^ b) => x.val) w hw
  refine ⟨fun x => (((w x : ℤ) + g x) / 2).toNat, fun x => (((w x : ℤ) - g x) / 2).toNat, ?_, ?_⟩
  · intro x
    have := hv x
    change (((w x : ℤ) + g x) / 2).toNat + (((w x : ℤ) - g x) / 2).toNat = w x
    omega
  · intro d hd hdvd
    obtain ⟨d1, d2, hd1, hd2, rfl⟩ := Nat.dvd_mul.1 hd
    obtain ⟨i, hi, rfl⟩ := (Nat.dvd_prime_pow hpP).1 hd1
    obtain ⟨j, -, rfl⟩ := (Nat.dvd_prime_pow hqP).1 hd2
    refine SignAux.not_cyclotomic_dvd p q hpq (fun x : ZMod (p ^ a * q ^ b) => x.val) g a hg1 hg2
      i j hi ?_
    have e1 : maskW (fun x => (((w x : ℤ) + g x) / 2).toNat)
        - maskW (fun x => (((w x : ℤ) - g x) / 2).toNat)
          = ∑ x : ZMod (p ^ a * q ^ b), Polynomial.C (g x) * Polynomial.X ^ x.val := by
      rw [maskW, maskW, ← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl fun x _ => ?_
      rw [← sub_mul, ← Polynomial.C_sub]
      have h3 : (((((w x : ℤ) + g x) / 2).toNat : ℕ) : ℤ)
          - (((((w x : ℤ) - g x) / 2).toNat : ℕ) : ℤ) = g x := by
        have := hv x
        omega
      rw [h3]
    rw [← e1]
    exact hdvd

end Lift

end Pnq
