/-
The statement on signs for every odd `n`: pivot sets and ranks.  The number of occupied classes modulo `p^j` is at least
`(p - 1) rank + 1`; a live level has a pivot set with `(p - 1) rank` elements (S2 (b)); so a live level `i` of `p` costs a
factor `2^((p-1) rank)` (S2); and ranks are small (S3).
(Statements fixed on 27 November 2026, before any Lean proof of them.)
-/
import Pnq.SignCount

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι]

namespace PivotAux

/-- A count by fibres: if `f` maps `S` into `T`, every fibre over `T` is nonempty and the fibre over `c ∈ T` has at
least `n` elements, then `|T| - 1 + n ≤ |S|`. -/
theorem card_fiber_bound {α β : Type*} [DecidableEq β] (S : Finset α) (T : Finset β) (f : α → β)
    (hf : ∀ x ∈ S, f x ∈ T) (hne : ∀ b ∈ T, ∃ x ∈ S, f x = b) (c : β) (hc : c ∈ T) (n : ℕ)
    (hn : n ≤ (S.filter fun x => f x = c).card) :
    T.card + n ≤ S.card + 1 := by
  have hmaps : (S : Set α).MapsTo f T := fun x hx => hf x hx
  rw [Finset.card_eq_sum_card_fiberwise hmaps, ← Finset.add_sum_erase T _ hc]
  have h1 : (T.erase c).card ≤ ∑ b ∈ T.erase c, (S.filter fun x => f x = b).card := by
    rw [Finset.card_eq_sum_ones]
    apply Finset.sum_le_sum
    intro b hb
    obtain ⟨x, hx, hxb⟩ := hne b (Finset.mem_of_mem_erase hb)
    exact Finset.card_pos.mpr ⟨x, Finset.mem_filter.mpr ⟨hx, hxb⟩⟩
  have h2 := Finset.card_erase_of_mem hc
  have h3 : 0 < T.card := Finset.card_pos.mpr ⟨c, hc⟩
  omega

/-- no level is counted up to `0` -/
theorem rank_zero (e : ι → ℕ) (p : ℕ) : rank e p 0 = 0 := by
  simp [rank]

/-- the rank goes up by one at a live level and stays at a level that is not live -/
theorem rank_succ (e : ι → ℕ) (p j : ℕ) :
    rank e p (j + 1) = rank e p j + if live e p (j + 1) = true then 1 else 0 := by
  unfold rank
  rw [← Finset.insert_Icc_right_eq_Icc_add_one (by omega : 1 ≤ j + 1), Finset.filter_insert]
  split_ifs with h
  · rw [Finset.card_insert_of_notMem (by simp)]
  · simp

/-- the rank goes up by one at a live level -/
theorem rank_succ_of_live (e : ι → ℕ) (p j : ℕ) (h : live e p (j + 1) = true) :
    rank e p (j + 1) = rank e p j + 1 := by
  simp [rank_succ, h]

/-- the rank stays at a level that is not live -/
theorem rank_succ_of_not_live (e : ι → ℕ) (p j : ℕ) (h : ¬ live e p (j + 1) = true) :
    rank e p (j + 1) = rank e p j := by
  simp [rank_succ, h]

/-- reduction modulo `p^j` maps the occupied classes modulo `p^(j+1)` onto those modulo `p^j` -/
theorem card_image_le_succ (e : ι → ℕ) (p j : ℕ) :
    (Finset.univ.image fun k => e k % p ^ j).card ≤ (Finset.univ.image fun k => e k % p ^ (j + 1)).card := by
  have h : (Finset.univ.image fun k => e k % p ^ j) =
      (Finset.univ.image fun k => e k % p ^ (j + 1)).image fun r => r % p ^ j := by
    rw [Finset.image_image]
    apply Finset.image_congr
    intro k _
    exact (Nat.mod_mod_of_dvd (e k) (pow_dvd_pow p (Nat.le_succ j))).symm
  rw [h]
  exact Finset.card_image_le

/-- The classes that are kept at the level `j + 1`: the occupied classes modulo `p^(j+1)` other than the classes
`c < p^j` whose group is full.  Every kept class is occupied; the class `c < p^j` of a full group is not kept; and if
there is a full group, the number of kept classes is at least `N_j + (p - 1) - 1` and less than `N_(j+1)`. -/
theorem exists_keep (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (j : ℕ) :
    ∃ R : Finset ℕ,
      (∀ r ∈ R, ∃ k, e k % p ^ (j + 1) = r) ∧
      (∀ c, c < p ^ j → (∀ t, t < p → ∃ k, e k % p ^ (j + 1) = c + t * p ^ j) → c ∉ R) ∧
      (∀ c, c < p ^ j → (∀ t, t < p → ∃ k, e k % p ^ (j + 1) = c + t * p ^ j) →
        (Finset.univ.image fun k => e k % p ^ j).card + (p - 1) ≤ R.card + 1 ∧
          R.card + 1 ≤ (Finset.univ.image fun k => e k % p ^ (j + 1)).card) := by
  classical
  have hpj : 0 < p ^ j := pow_pos hp.pos j
  have hSmem : ∀ r, r ∈ (Finset.univ.image fun k => e k % p ^ (j + 1)) ↔ ∃ k, e k % p ^ (j + 1) = r := by
    intro r; simp
  have hTmem : ∀ r, r ∈ (Finset.univ.image fun k => e k % p ^ j) ↔ ∃ k, e k % p ^ j = r := by
    intro r; simp
  have hmod : ∀ n, n % p ^ (j + 1) % p ^ j = n % p ^ j := fun n =>
    Nat.mod_mod_of_dvd n (pow_dvd_pow p (Nat.le_succ j))
  refine ⟨(Finset.univ.image fun k => e k % p ^ (j + 1)).filter fun r =>
    ¬ (r < p ^ j ∧ ∀ t, t < p → ∃ k, e k % p ^ (j + 1) = r + t * p ^ j), ?_, ?_, ?_⟩
  · intro r hr
    exact (hSmem r).mp (Finset.mem_filter.mp hr).1
  · intro c hc hfull hmem
    exact (Finset.mem_filter.mp hmem).2 ⟨hc, hfull⟩
  · intro c hc hfull
    have hcS : c ∈ (Finset.univ.image fun k => e k % p ^ (j + 1)) := by
      obtain ⟨k, hk⟩ := hfull 0 hp.pos
      exact (hSmem c).mpr ⟨k, by simpa using hk⟩
    constructor
    · refine card_fiber_bound _ _ (fun r => r % p ^ j) ?_ ?_ c ?_ (p - 1) ?_
      · intro x hx
        obtain ⟨k, hk⟩ := (hSmem x).mp (Finset.mem_filter.mp hx).1
        exact (hTmem _).mpr ⟨k, by rw [← hk, hmod]⟩
      · intro b hb
        obtain ⟨k, hk⟩ := (hTmem b).mp hb
        have hb_lt : b < p ^ j := by rw [← hk]; exact Nat.mod_lt _ hpj
        by_cases hfb : ∀ t, t < p → ∃ k, e k % p ^ (j + 1) = b + t * p ^ j
        · refine ⟨b + 1 * p ^ j, Finset.mem_filter.mpr ⟨(hSmem _).mpr (hfb 1 hp.one_lt), ?_⟩, ?_⟩
          · intro h
            have h1 := h.1
            omega
          · rw [Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hb_lt]
        · refine ⟨e k % p ^ (j + 1), Finset.mem_filter.mpr ⟨(hSmem _).mpr ⟨k, rfl⟩, ?_⟩, ?_⟩
          · intro h
            have h1 : e k % p ^ (j + 1) = b := by
              rw [← hk, ← hmod (e k), Nat.mod_eq_of_lt h.1]
            rw [h1] at h
            exact hfb h.2
          · rw [hmod, hk]
      · obtain ⟨k, hk⟩ := hfull 0 hp.pos
        refine (hTmem c).mpr ⟨k, ?_⟩
        rw [← hmod, hk, Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hc]
      · have hinj : Set.InjOn (fun t => c + t * p ^ j) (Finset.Ico 1 p : Set ℕ) := by
          intro t _ t' _ h
          have h' : t * p ^ j = t' * p ^ j := Nat.add_left_cancel h
          exact Nat.eq_of_mul_eq_mul_right hpj h'
        calc p - 1 = (Finset.Ico 1 p).card := by simp
          _ = ((Finset.Ico 1 p).image fun t => c + t * p ^ j).card :=
              (Finset.card_image_of_injOn hinj).symm
          _ ≤ _ := Finset.card_le_card (by
              intro x hx
              obtain ⟨t, ht, rfl⟩ := Finset.mem_image.mp hx
              have ht' := Finset.mem_Ico.mp ht
              refine Finset.mem_filter.mpr
                ⟨Finset.mem_filter.mpr ⟨(hSmem _).mpr (hfull t ht'.2), ?_⟩, ?_⟩
              · intro h
                have h1 := h.1
                have h2 : p ^ j ≤ t * p ^ j := Nat.le_mul_of_pos_left _ ht'.1
                omega
              · rw [Nat.add_mul_mod_self_right, Nat.mod_eq_of_lt hc])
    · exact Finset.card_lt_card (Finset.filter_ssubset.mpr ⟨c, hcS, fun h => h ⟨hc, hfull⟩⟩)

end PivotAux

/-- **The number of occupied classes** (the plan's `N_j ≥ 1 + (p - 1) rank p j`, in S2 (b) and S3).  For a nonempty
`ι` and a prime `p`, the number of classes modulo `p^j` that are occupied is at least `(p - 1) * rank e p j + 1`. -/
theorem rank_lt_card_image [Nonempty ι] (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (j : ℕ) :
    (p - 1) * rank e p j + 1 ≤ (Finset.univ.image fun k => e k % p ^ j).card := by
  induction j with
  | zero =>
    rw [PivotAux.rank_zero]
    have h : (Finset.univ.image fun k => e k % p ^ 0).Nonempty :=
      Finset.image_nonempty.mpr Finset.univ_nonempty
    have := Finset.card_pos.mpr h
    omega
  | succ j ih =>
    by_cases hl : live e p (j + 1) = true
    · rw [PivotAux.rank_succ_of_live e p j hl]
      obtain ⟨c, hc, hfull⟩ := (live_iff e p (j + 1)).mp hl
      rw [Nat.add_sub_cancel] at hc hfull
      obtain ⟨R, -, -, hR⟩ := PivotAux.exists_keep e hp j
      obtain ⟨h1, h2⟩ := hR c hc hfull
      have h3 : (p - 1) * (rank e p j + 1) = (p - 1) * rank e p j + (p - 1) := by ring
      omega
    · rw [PivotAux.rank_succ_of_not_live e p j hl]
      have := PivotAux.card_image_le_succ e p j
      omega

/-- **S2 (b) (a large pivot set).**  `p` prime, `i ≥ 1`.  If the level `i` of `p` is live, there is a pivot set for
that level with at least `(p - 1) * rank e p i` elements. -/
theorem exists_isPivot (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i)
    (hlive : live e p i = true) :
    ∃ J : Finset ι, IsPivot e p i J ∧ (p - 1) * rank e p i ≤ J.card := by
  classical
  obtain ⟨j, rfl⟩ : ∃ j, i = j + 1 := ⟨i - 1, by omega⟩
  have hpj : 0 < p ^ j := pow_pos hp.pos j
  obtain ⟨c, hc, hfull⟩ := (live_iff e p (j + 1)).mp hlive
  rw [Nat.add_sub_cancel] at hc hfull
  obtain ⟨k0, -⟩ := hfull 0 hp.pos
  have hne : Nonempty ι := ⟨k0⟩
  obtain ⟨R, hRocc, hRdrop, hR⟩ := PivotAux.exists_keep e hp j
  obtain ⟨h1, -⟩ := hR c hc hfull
  choose g hg using hRocc
  have hinj : Function.Injective fun r : R => g r.val r.property := by
    intro r r' h
    have h' : e (g r.val r.property) % p ^ (j + 1) = e (g r'.val r'.property) % p ^ (j + 1) := by
      have h'' : g r.val r.property = g r'.val r'.property := h
      rw [h'']
    rw [hg r.val r.property, hg r'.val r'.property] at h'
    exact Subtype.ext h'
  refine ⟨R.attach.image fun r => g r.val r.property, ⟨?_, ?_⟩, ?_⟩
  · intro k hk k' hk' hkk
    obtain ⟨r, -, rfl⟩ := Finset.mem_image.mp hk
    obtain ⟨r', -, rfl⟩ := Finset.mem_image.mp hk'
    rw [hg r.val r.property, hg r'.val r'.property] at hkk
    have : r = r' := Subtype.ext hkk
    rw [this]
  · intro c'
    rw [Nat.add_sub_cancel]
    by_cases hf : ∀ t, t < p → ∃ k, e k % p ^ (j + 1) = c' % p ^ j + t * p ^ j
    · refine ⟨0, hp.pos, ?_⟩
      intro k hk heq
      obtain ⟨r, -, rfl⟩ := Finset.mem_image.mp hk
      rw [hg r.val r.property, Nat.zero_mul, Nat.add_zero] at heq
      exact hRdrop (c' % p ^ j) (Nat.mod_lt _ hpj) hf (heq ▸ r.property)
    · by_contra hcon
      apply hf
      intro t ht
      by_contra hno
      exact hcon ⟨t, ht, fun k _ hk => hno ⟨k, hk⟩⟩
  · rw [Finset.card_image_of_injective _ hinj, Finset.card_attach,
      PivotAux.rank_succ_of_live e p j hlive]
    have h2 := rank_lt_card_image e hp j
    have h3 : (p - 1) * (rank e p j + 1) = (p - 1) * rank e p j + (p - 1) := by ring
    omega

/-- **S2 (what a live level costs).**  `p` prime, `i ≥ 1`, `p ∤ d`, the level `i` of `p` live.  Then
`#{ε bad at p^i * d} * 2^((p - 1) * rank e p i) ≤ 2^m`. -/
theorem card_badSet_mul_two_pow_rank_le (e : ι → ℕ) {p : ℕ} (hp : p.Prime) {i : ℕ} (hi : 1 ≤ i) {d : ℕ}
    (hd : ¬ p ∣ d) (hlive : live e p i = true) :
    (badSet e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i) ≤ 2 ^ Fintype.card ι := by
  obtain ⟨J, hJ, hcard⟩ := exists_isPivot e hp hi hlive
  calc (badSet e (p ^ i * d)).card * 2 ^ ((p - 1) * rank e p i)
      ≤ (badSet e (p ^ i * d)).card * 2 ^ J.card :=
        Nat.mul_le_mul_left _ (Nat.pow_le_pow_right (by norm_num) hcard)
    _ ≤ 2 ^ Fintype.card ι := card_badSet_mul_two_pow_card_le e hp hi hd hJ

/-- **S3 (ranks are small).**  For a nonempty `ι`, every prime `p` and every `i`: `(p - 1) * rank e p i + 1 ≤ m`. -/
theorem rank_lt_card [Nonempty ι] (e : ι → ℕ) {p : ℕ} (hp : p.Prime) (i : ℕ) :
    (p - 1) * rank e p i + 1 ≤ Fintype.card ι := by
  have h1 := rank_lt_card_image e hp i
  have h2 : (Finset.univ.image fun k => e k % p ^ i).card ≤ Fintype.card ι := by
    rw [← Finset.card_univ]
    exact Finset.card_image_le
  omega

end Pnq
