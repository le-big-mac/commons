/-
The three-way equivalence tile ⇔ pd-tile ⇔ weak tile in `ZMod (p^2 * q^2)`, for distinct primes `p`, `q`.
pd-tiling is `Pqr.PdTiling` (`Pnq/Pd.lean`; Kiss–Londner–Matolcsi–Somlai, arXiv:2411.03854, Definition 1.3).
Added on 26 November 2026: until then the equivalence was stated on the cover page of the folder and was true in
one line, but was not among the checked statements (found by a reader of the prior art).
-/
import P2q2.Main
import Pnq.Pd

open Finset

namespace P2q2

open Pqr

/-- **In `Z_{p²q²}` the tiles, the pd-tiles and the weak tiles are the same sets.** -/
theorem tile_iff_pd_iff_weak_p2q2 (p q : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ 2 * q ^ 2))) :
    ((∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B) ↔ ∃ f, PdTiling A f) ∧
    ((∃ f, PdTiling A f) ↔ ∃ f, WeakTiling A f) := by
  have h1 : (∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B) → ∃ f, PdTiling A f :=
    fun ⟨_, hB⟩ => hB.pdTiling
  have h2 : (∃ f, PdTiling A f) → ∃ f, WeakTiling A f := fun ⟨f, hf⟩ => ⟨f, hf.1⟩
  have h3 : (∃ f, WeakTiling A f) → ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B :=
    fun ⟨f, hf⟩ => weak_tiling_tiles_p2q2 p q hpq A f hf
  exact ⟨⟨h1, fun h => h3 (h2 h)⟩, ⟨h2, fun h => h1 (h3 h)⟩⟩

end P2q2
