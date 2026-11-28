/-
"Twice" for several systems of values at once (Theorem U of the note of the evening of 27 November 2026).
`ι` a finite type, each `k : ι` with a position `pos k : ℕ`; `κ` any type of indices, and for each `c : κ` a system of
values `val c : ι → V` in an additive commutative group `V` (any group, any values, `0` allowed).  The positions are
the same for every `c`.  The signings for which some level `0, …, K` is bad for the values of SOME `c` number at most
twice those for which level `0` is bad for the values of some `c`.
For a single `c` this is `card_exists_levelBad_le` of `Pnq/EvenTwice.lean`.
(Statement fixed before any Lean proof of it.)
-/
import Pnq.EvenTwice

open Finset

namespace Pnq

variable {ι : Type*} [Fintype ι] {V : Type*} [AddCommGroup V]

/-! Lemmas for the proof of U (`card_exists_exists_levelBad_le`), in the namespace `Pnq.UnionAux`: the sets `F`, `B`,
`A` of `Pnq.TwiceAux` with "for some `c`" put in, and the four steps of the proof of T for them.  The reflection
`TwiceAux.tau pos j` does not mention the values, so it is the same map for every `c`. -/

namespace UnionAux

open Classical in
/-- `FU d`: the signings for which, for some `c`, every class modulo `2^d` has signed sum `0` for the values
`val c` (the union over `c` of the sets `TwiceAux.F pos (val c) d`) -/
noncomputable def FU {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (d : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε : ι → Bool => ∃ c, ε ∈ TwiceAux.F pos (val c) d

/-- membership in `FU d` (unfolding) -/
theorem mem_FU {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (d : ℕ) (ε : ι → Bool) :
    ε ∈ FU pos val d ↔ ∃ c, ε ∈ TwiceAux.F pos (val c) d := by
  simp [FU]

open Classical in
/-- `BU j`: the signings for which level `j` is bad for the values of some `c` -/
noncomputable def BU {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (j : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε : ι → Bool => ∃ c, levelBad pos (val c) ε j

/-- membership in `BU j` (unfolding) -/
theorem mem_BU {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (j : ℕ) (ε : ι → Bool) :
    ε ∈ BU pos val j ↔ ∃ c, levelBad pos (val c) ε j := by
  simp [BU]

open Classical in
/-- `AU K`: the signings for which some level `j ≤ K` is bad for the values of some `c` -/
noncomputable def AU {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (K : ℕ) : Finset (ι → Bool) :=
  Finset.univ.filter fun ε : ι → Bool => ∃ c, ∃ j, j ≤ K ∧ levelBad pos (val c) ε j

/-- membership in `AU K` (unfolding) -/
theorem mem_AU {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (K : ℕ) (ε : ι → Bool) :
    ε ∈ AU pos val K ↔ ∃ c, ∃ j, j ≤ K ∧ levelBad pos (val c) ε j := by
  simp [AU]

/-- (a′) `FU (d+1) ⊆ FU d` -/
theorem FU_succ_subset {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (d : ℕ) :
    FU pos val (d + 1) ⊆ FU pos val d := by
  intro ε hε
  rw [mem_FU] at hε ⊢
  obtain ⟨c, hc⟩ := hε
  exact ⟨c, TwiceAux.F_succ_subset pos (val c) d hc⟩

/-- `FU 0 = BU 0` -/
theorem FU_zero_eq {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) : FU pos val 0 = BU pos val 0 := by
  ext ε
  rw [mem_FU, mem_BU]
  exact exists_congr fun c => TwiceAux.mem_F_zero pos (val c) ε

/-- `AU 0 = BU 0` -/
theorem AU_zero_eq {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) : AU pos val 0 = BU pos val 0 := by
  ext ε
  rw [mem_AU, mem_BU]
  constructor
  · rintro ⟨c, j, hj, h⟩
    have hj0 : j = 0 := by omega
    rw [hj0] at h
    exact ⟨c, h⟩
  · rintro ⟨c, h⟩
    exact ⟨c, 0, le_refl 0, h⟩

/-- (b′) as many signings have level `j + 1` bad for some `c` as there are in `FU j`: the reflection
`TwiceAux.tau pos j`, the same for every `c`, maps the one set onto the other -/
theorem card_BU_succ {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (j : ℕ) :
    (BU pos val (j + 1)).card = (FU pos val j).card := by
  refine Finset.card_nbij' (TwiceAux.tau pos j) (TwiceAux.tau pos j) ?_ ?_ ?_ ?_
  · intro ε hε
    rw [Finset.mem_coe, mem_BU] at hε
    obtain ⟨c, hc⟩ := hε
    rw [Finset.mem_coe, mem_FU]
    exact ⟨c, (TwiceAux.levelBad_succ_iff pos (val c) ε j).mp hc⟩
  · intro ε hε
    rw [Finset.mem_coe, mem_FU] at hε
    obtain ⟨c, hc⟩ := hε
    rw [Finset.mem_coe, mem_BU]
    refine ⟨c, ?_⟩
    rw [TwiceAux.levelBad_succ_iff, TwiceAux.tau_tau]
    exact hc
  · intro ε _
    exact TwiceAux.tau_tau pos j ε
  · intro ε _
    exact TwiceAux.tau_tau pos j ε

/-- (c′) on `FU (j+1)` level `j + 1` is bad for some `c` -/
theorem FU_succ_subset_BU {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (j : ℕ) :
    FU pos val (j + 1) ⊆ BU pos val (j + 1) := by
  intro ε hε
  rw [mem_FU] at hε
  obtain ⟨c, hc⟩ := hε
  rw [mem_BU]
  exact ⟨c, (TwiceAux.mem_B pos (val c) (j + 1) ε).mp (TwiceAux.F_succ_subset_B pos (val c) j hc)⟩

/-- (c′) on `FU d` level `0` is bad for some `c` -/
theorem FU_subset_BU_zero {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (d : ℕ) :
    FU pos val d ⊆ BU pos val 0 := by
  intro ε hε
  rw [mem_FU] at hε
  obtain ⟨c, hc⟩ := hε
  rw [mem_BU]
  exact ⟨c, (TwiceAux.mem_F_zero pos (val c) ε).mp (TwiceAux.F_subset_zero pos (val c) d hc)⟩

/-- (d′) a signing with some level `≤ K + 1` bad for some `c` has some level `≤ K` bad for some `c`, or has level
`K + 1` bad for some `c` and is not in `FU (K+1)` (if it is in `FU (K+1)`, level `0` is bad for some `c`) -/
theorem AU_succ_subset {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (K : ℕ) :
    AU pos val (K + 1) ⊆ AU pos val K ∪ (BU pos val (K + 1) \ FU pos val (K + 1)) := by
  intro ε hε
  rw [mem_AU] at hε
  obtain ⟨c, j, hj, h⟩ := hε
  rw [Finset.mem_union, mem_AU, Finset.mem_sdiff, mem_BU]
  by_cases hjK : j ≤ K
  · left
    exact ⟨c, j, hjK, h⟩
  · have hj' : j = K + 1 := by omega
    rw [hj'] at h
    by_cases h0 : ε ∈ BU pos val 0
    · left
      rw [mem_BU] at h0
      obtain ⟨c0, hc0⟩ := h0
      exact ⟨c0, 0, Nat.zero_le _, hc0⟩
    · right
      exact ⟨⟨c, h⟩, fun hF => h0 (FU_subset_BU_zero pos val (K + 1) hF)⟩

/-- (d′) the stronger statement that goes through the induction on `K` -/
theorem card_AU_add_card_FU_le {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (K : ℕ) :
    (AU pos val K).card + (FU pos val K).card ≤ 2 * (BU pos val 0).card := by
  induction K with
  | zero =>
    rw [AU_zero_eq, FU_zero_eq]
    omega
  | succ K ih =>
    have h2 : (BU pos val (K + 1) \ FU pos val (K + 1)).card + (FU pos val (K + 1)).card =
        (FU pos val K).card := by
      rw [Finset.card_sdiff_add_card_eq_card (FU_succ_subset_BU pos val K), card_BU_succ]
    have h3 := (Finset.card_le_card (AU_succ_subset pos val K)).trans (Finset.card_union_le _ _)
    omega

end UnionAux

open Classical in
/-- **U (several systems of values).**  For every `K`, the number of signings `ε` such that level `j` is bad for the
values `val c`, for some index `c` and some `j ≤ K`, is at most twice the number of signings such that level `0` is
bad for the values `val c` for some index `c`. -/
theorem card_exists_exists_levelBad_le {κ : Type*} (pos : ι → ℕ) (val : κ → ι → V) (K : ℕ) :
    (Finset.univ.filter fun ε : ι → Bool => ∃ c, ∃ j, j ≤ K ∧ levelBad pos (val c) ε j).card ≤
      2 * (Finset.univ.filter fun ε : ι → Bool => ∃ c, levelBad pos (val c) ε 0).card := by
  exact (Nat.le_add_right _ _).trans (UnionAux.card_AU_add_card_FU_le pos val K)

end Pnq
