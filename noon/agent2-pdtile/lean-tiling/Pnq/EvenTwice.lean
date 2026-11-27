/-
The statement on signs for every `n`: part T, "the levels of the prime 2 together cost at most twice level 0".
Pure combinatorics, no polynomials.  `ι` a finite type, each `k : ι` with a position `pos k : ℕ` and a value `val k`
in an additive commutative group `V` (any group, any values, `0` allowed); a signing is `ε : ι → Bool`.
`csum pos val ε M r` is the signed sum of the values over the class `r` modulo `M`.  Level `0` is bad if the signed
sum of all values is `0`; level `j + 1` is bad if for every `r < 2^j` the two classes `r` and `r + 2^j` modulo
`2^(j+1)` (the two halves of the class `r` modulo `2^j`) have equal signed sums.
(Theorem T′ of the proof on paper; statement fixed on 27 November 2026, before any Lean proof of it.)
-/
import Pnq.SignDefs

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι] {V : Type*} [AddCommGroup V]

/-- the signed sum `∑ sg (ε k) • val k` over the elements `k` whose position lies in the class `r` modulo `M`
(that is, `pos k % M = r`) -/
def csum (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (M r : ℕ) : V :=
  ∑ k, if pos k % M = r then sg (ε k) • val k else 0

/-- level `j` is bad for the signing `ε`.  Level `0`: the signed sum of all the values is `0`.  Level `j + 1`: for
every `r < 2^j`, the classes `r` and `r + 2^j` modulo `2^(j+1)` have the same signed sum. -/
def levelBad (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) : ℕ → Prop
  | 0 => ∑ k, sg (ε k) • val k = 0
  | j + 1 => ∀ r, r < 2 ^ j →
      csum pos val ε (2 ^ (j + 1)) r = csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j)

/-! Lemmas for the proof of T (`card_exists_levelBad_le`), in the namespace `Pnq.TwiceAux`. -/

namespace TwiceAux

/-- the residue modulo `N` read off the residue modulo `2 * N`: it is the same in the lower half,
and `N` less in the upper half -/
theorem mod_cases (x N : ℕ) (hN : 0 < N) :
    (x % (2 * N) < N ∧ x % N = x % (2 * N)) ∨
      (N ≤ x % (2 * N) ∧ x % (2 * N) < 2 * N ∧ x % N + N = x % (2 * N)) := by
  have h1 : x % (2 * N) % N = x % N := Nat.mod_mod_of_dvd x (Nat.dvd_mul_left N 2)
  have h2 : x % (2 * N) < 2 * N := Nat.mod_lt _ (by omega)
  rw [← h1]
  generalize x % (2 * N) = m at *
  rcases Nat.lt_or_ge m N with h | h
  · left
    exact ⟨h, Nat.mod_eq_of_lt h⟩
  · right
    refine ⟨h, h2, ?_⟩
    rw [Nat.mod_eq_sub_mod h, Nat.mod_eq_of_lt (by omega)]
    omega

/-- the sign of the negated Boolean is the negated sign -/
theorem sg_not (b : Bool) : sg (!b) = -sg b := by
  cases b <;> simp [sg]

/-- the reflection of level `j`: the signing with the signs negated on the elements whose position
lies in the upper half modulo `2^(j+1)` (that is, `2^j ≤ pos k % 2^(j+1)`) -/
def tau {κ : Type*} (pos : κ → ℕ) (j : ℕ) (ε : κ → Bool) : κ → Bool :=
  fun k => if 2 ^ j ≤ pos k % 2 ^ (j + 1) then !ε k else ε k

/-- the reflection is an involution -/
theorem tau_tau {κ : Type*} (pos : κ → ℕ) (j : ℕ) (ε : κ → Bool) :
    tau pos j (tau pos j ε) = ε := by
  funext k
  by_cases h : 2 ^ j ≤ pos k % 2 ^ (j + 1) <;> simp [tau, h]

/-- the class `0` modulo `1` is everything -/
theorem csum_one (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) :
    csum pos val ε 1 0 = ∑ k, sg (ε k) • val k := by
  unfold csum
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [Nat.mod_one, ite_eq_left rfl]

/-- (a) the class `r` modulo `2^d` is the union of the classes `r` and `r + 2^d` modulo `2^(d+1)` -/
theorem csum_split (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (d r : ℕ) (hr : r < 2 ^ d) :
    csum pos val ε (2 ^ d) r =
      csum pos val ε (2 ^ (d + 1)) r + csum pos val ε (2 ^ (d + 1)) (r + 2 ^ d) := by
  unfold csum
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl fun k _ => ?_
  have hN : 0 < 2 ^ d := Nat.two_pow_pos d
  rw [pow_succ']
  generalize 2 ^ d = N at *
  rcases mod_cases (pos k) N hN with ⟨h1, h2⟩ | ⟨h1, h2, h3⟩
  · have e2 : ¬ pos k % (2 * N) = r + N := by omega
    rw [ite_eq_right e2, add_zero, h2]
  · have e2 : ¬ pos k % (2 * N) = r := by omega
    rw [ite_eq_right e2, zero_add]
    by_cases hm : pos k % (2 * N) = r + N
    · have e1 : pos k % N = r := by omega
      rw [ite_eq_left e1, ite_eq_left hm]
    · have e1 : ¬ pos k % N = r := by omega
      rw [ite_eq_right e1, ite_eq_right hm]

/-- (b) the class sums of the reflected signing modulo `2^j` are the differences of the two halves
modulo `2^(j+1)` of the class sums of the signing -/
theorem csum_tau (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (j r : ℕ) (hr : r < 2 ^ j) :
    csum pos val (tau pos j ε) (2 ^ j) r =
      csum pos val ε (2 ^ (j + 1)) r - csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j) := by
  unfold csum
  rw [← Finset.sum_sub_distrib]
  refine Finset.sum_congr rfl fun k _ => ?_
  have hN : 0 < 2 ^ j := Nat.two_pow_pos j
  simp only [tau]
  rw [pow_succ']
  generalize 2 ^ j = N at *
  rcases mod_cases (pos k) N hN with ⟨h1, h2⟩ | ⟨h1, h2, h3⟩
  · have e0 : ¬ N ≤ pos k % (2 * N) := by omega
    have e2 : ¬ pos k % (2 * N) = r + N := by omega
    rw [ite_eq_right e0, ite_eq_right e2, sub_zero, h2]
  · have e2 : ¬ pos k % (2 * N) = r := by omega
    rw [ite_eq_left h1, ite_eq_right e2, zero_sub, sg_not, neg_smul]
    by_cases hm : pos k % (2 * N) = r + N
    · have e1 : pos k % N = r := by omega
      rw [ite_eq_left e1, ite_eq_left hm]
    · have e1 : ¬ pos k % N = r := by omega
      rw [ite_eq_right e1, ite_eq_right hm, neg_zero]

open Classical in
/-- `F d`: the signings for which every class modulo `2^d` has signed sum `0` -/
noncomputable def F (pos : ι → ℕ) (val : ι → V) (d : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε => ∀ r, r < 2 ^ d → csum pos val ε (2 ^ d) r = 0

/-- membership in `F d` (unfolding) -/
theorem mem_F (pos : ι → ℕ) (val : ι → V) (d : ℕ) (ε : ι → Bool) :
    ε ∈ F pos val d ↔ ∀ r, r < 2 ^ d → csum pos val ε (2 ^ d) r = 0 := by
  simp [F]

/-- (a) `F (d+1) ⊆ F d` -/
theorem F_succ_subset (pos : ι → ℕ) (val : ι → V) (d : ℕ) : F pos val (d + 1) ⊆ F pos val d := by
  intro ε hε
  rw [mem_F] at hε ⊢
  intro r hr
  have h2 : (2 : ℕ) ^ (d + 1) = 2 * 2 ^ d := pow_succ' 2 d
  rw [csum_split pos val ε d r hr, hε r (by omega), hε (r + 2 ^ d) (by omega), add_zero]

/-- `F 0` is "level `0` is bad" -/
theorem mem_F_zero (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) :
    ε ∈ F pos val 0 ↔ levelBad pos val ε 0 := by
  rw [mem_F]
  change (∀ r, r < 2 ^ 0 → csum pos val ε (2 ^ 0) r = 0) ↔ ∑ k, sg (ε k) • val k = 0
  rw [pow_zero, ← csum_one pos val ε]
  constructor
  · intro h
    exact h 0 Nat.one_pos
  · intro h r hr
    have hr0 : r = 0 := by omega
    rw [hr0]
    exact h

/-- `F d ⊆ F 0` -/
theorem F_subset_zero (pos : ι → ℕ) (val : ι → V) (d : ℕ) : F pos val d ⊆ F pos val 0 := by
  induction d with
  | zero => exact Finset.Subset.refl _
  | succ d ih => exact (F_succ_subset pos val d).trans ih

/-- (b) level `j + 1` is bad for `ε` exactly when the reflected signing lies in `F j` -/
theorem levelBad_succ_iff (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (j : ℕ) :
    levelBad pos val ε (j + 1) ↔ tau pos j ε ∈ F pos val j := by
  rw [mem_F]
  change (∀ r, r < 2 ^ j →
      csum pos val ε (2 ^ (j + 1)) r = csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j)) ↔ _
  refine forall_congr' fun r => forall_congr' fun hr => ?_
  rw [csum_tau pos val ε j r hr, sub_eq_zero]

open Classical in
/-- `A K`: the signings for which some level `j ≤ K` is bad -/
noncomputable def A (pos : ι → ℕ) (val : ι → V) (K : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ levelBad pos val ε j

/-- membership in `A K` (unfolding) -/
theorem mem_A (pos : ι → ℕ) (val : ι → V) (K : ℕ) (ε : ι → Bool) :
    ε ∈ A pos val K ↔ ∃ j, j ≤ K ∧ levelBad pos val ε j := by
  simp [A]

open Classical in
/-- `B j`: the signings for which level `j` is bad -/
noncomputable def B (pos : ι → ℕ) (val : ι → V) (j : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε : ι → Bool => levelBad pos val ε j

/-- membership in `B j` (unfolding) -/
theorem mem_B (pos : ι → ℕ) (val : ι → V) (j : ℕ) (ε : ι → Bool) :
    ε ∈ B pos val j ↔ levelBad pos val ε j := by
  simp [B]

/-- `F 0 = B 0` -/
theorem F_zero_eq (pos : ι → ℕ) (val : ι → V) : F pos val 0 = B pos val 0 := by
  ext ε
  rw [mem_F_zero, mem_B]

/-- `A 0 = B 0` -/
theorem A_zero_eq (pos : ι → ℕ) (val : ι → V) : A pos val 0 = B pos val 0 := by
  ext ε
  rw [mem_A, mem_B]
  constructor
  · rintro ⟨j, hj, h⟩
    have hj0 : j = 0 := by omega
    rw [hj0] at h
    exact h
  · intro h
    exact ⟨0, le_refl 0, h⟩

/-- (b) as many signings have level `j + 1` bad as there are in `F j` -/
theorem card_B_succ (pos : ι → ℕ) (val : ι → V) (j : ℕ) :
    (B pos val (j + 1)).card = (F pos val j).card := by
  refine Finset.card_nbij' (tau pos j) (tau pos j) ?_ ?_ ?_ ?_
  · intro ε hε
    rw [Finset.mem_coe, mem_B] at hε
    exact (levelBad_succ_iff pos val ε j).mp hε
  · intro ε hε
    rw [Finset.mem_coe] at hε
    rw [Finset.mem_coe, mem_B, levelBad_succ_iff, tau_tau]
    exact hε
  · intro ε _
    exact tau_tau pos j ε
  · intro ε _
    exact tau_tau pos j ε

/-- (c) on `F (j+1)` level `j + 1` is bad (both halves are `0`) -/
theorem F_succ_subset_B (pos : ι → ℕ) (val : ι → V) (j : ℕ) :
    F pos val (j + 1) ⊆ B pos val (j + 1) := by
  intro ε hε
  rw [mem_F] at hε
  rw [mem_B]
  change ∀ r, r < 2 ^ j →
      csum pos val ε (2 ^ (j + 1)) r = csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j)
  intro r hr
  have h2 : (2 : ℕ) ^ (j + 1) = 2 * 2 ^ j := pow_succ' 2 j
  rw [hε r (by omega), hε (r + 2 ^ j) (by omega)]

/-- (d) a signing with some level `≤ K + 1` bad has some level `≤ K` bad, or has level `K + 1` bad
and is not in `F (K+1)` (if it is in `F (K+1)`, level `0` is bad) -/
theorem A_succ_subset (pos : ι → ℕ) (val : ι → V) (K : ℕ) :
    A pos val (K + 1) ⊆ A pos val K ∪ (B pos val (K + 1) \ F pos val (K + 1)) := by
  intro ε hε
  rw [mem_A] at hε
  obtain ⟨j, hj, h⟩ := hε
  rw [Finset.mem_union, mem_A, Finset.mem_sdiff, mem_B]
  by_cases hjK : j ≤ K
  · left
    exact ⟨j, hjK, h⟩
  · have hj' : j = K + 1 := by omega
    rw [hj'] at h
    by_cases h0 : levelBad pos val ε 0
    · left
      exact ⟨0, Nat.zero_le _, h0⟩
    · right
      exact ⟨h, fun hF => h0 ((mem_F_zero pos val ε).mp (F_subset_zero pos val (K + 1) hF))⟩

/-- (d) the stronger statement that goes through the induction on `K` -/
theorem card_A_add_card_F_le (pos : ι → ℕ) (val : ι → V) (K : ℕ) :
    (A pos val K).card + (F pos val K).card ≤ 2 * (B pos val 0).card := by
  induction K with
  | zero =>
    rw [A_zero_eq, F_zero_eq]
    omega
  | succ K ih =>
    have h2 : (B pos val (K + 1) \ F pos val (K + 1)).card + (F pos val (K + 1)).card =
        (F pos val K).card := by
      rw [Finset.card_sdiff_add_card_eq_card (F_succ_subset_B pos val K), card_B_succ]
    have h3 := (Finset.card_le_card (A_succ_subset pos val K)).trans (Finset.card_union_le _ _)
    omega

end TwiceAux

/-- `levelBad` at level `0` (unfolding) -/
theorem levelBad_zero (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) :
    levelBad pos val ε 0 ↔ ∑ k, sg (ε k) • val k = 0 :=
  Iff.rfl

/-- `levelBad` at level `j + 1` (unfolding) -/
theorem levelBad_succ (pos : ι → ℕ) (val : ι → V) (ε : ι → Bool) (j : ℕ) :
    levelBad pos val ε (j + 1) ↔ ∀ r, r < 2 ^ j →
      csum pos val ε (2 ^ (j + 1)) r = csum pos val ε (2 ^ (j + 1)) (r + 2 ^ j) :=
  Iff.rfl

open Classical in
/-- **T (twice level 0).**  For every `K`, the number of signings for which some level `j ≤ K` is bad is at most
twice the number of signings for which level `0` is bad. -/
theorem card_exists_levelBad_le (pos : ι → ℕ) (val : ι → V) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ j, j ≤ K ∧ levelBad pos val ε j).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => levelBad pos val ε 0).card := by
  exact (Nat.le_add_right _ _).trans (TwiceAux.card_A_add_card_F_le pos val K)

end Pnq
