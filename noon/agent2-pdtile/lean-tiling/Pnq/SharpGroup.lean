/-
The sharp form of Lemma 3, and the bound `p^{|E ∪ F|}`, for subsets of `ZMod (p^n * q)`, in terms of the
Fourier zeros `Pqr.ZeroAt` (for a set, `ZeroAt A d` says that `Φ_d` divides the mask polynomial).
Derived from `Pnq/Sharp.lean` (the tree) through the bridge of `Pnq/Group.lean`.  (agent3 / Yonder, 26 Nov 2026)
-/
import Pnq.Sharp
import Pnq.Group

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ} ∣ A` -/
noncomputable def levelsE (A : Finset (ZMod (p ^ n * q))) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Pqr.ZeroAt A (p ^ ℓ))

open Classical in
/-- the levels `ℓ` in `1..n` with `Φ_{p^ℓ q} ∣ A` -/
noncomputable def levelsF (A : Finset (ZMod (p ^ n * q))) : Finset ℕ :=
  (Finset.Icc 1 n).filter (fun ℓ => Pqr.ZeroAt A (p ^ ℓ * q))

theorem eSet_treeOf (A : Finset (ZMod (p ^ n * q))) :
    eSet (treeOf A) = levelsE A := by
  ext ℓ
  simp only [mem_eSet, levelsE, Finset.mem_filter, Finset.mem_Icc]
  constructor
  · rintro ⟨h1, hn, hE⟩
    exact ⟨⟨h1, hn⟩, (E_treeOf A ℓ h1 hn).1 hE⟩
  · rintro ⟨⟨h1, hn⟩, hZ⟩
    exact ⟨h1, hn, (E_treeOf A ℓ h1 hn).2 hZ⟩

theorem fSet_treeOf (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) :
    fSet (treeOf A) = levelsF A := by
  ext ℓ
  simp only [mem_fSet, levelsF, Finset.mem_filter, Finset.mem_Icc]
  constructor
  · rintro ⟨h1, hn, hF⟩
    exact ⟨⟨h1, hn⟩, (F_treeOf hpq A ℓ h1 hn).1 hF⟩
  · rintro ⟨⟨h1, hn⟩, hZ⟩
    exact ⟨h1, hn, (F_treeOf hpq A ℓ h1 hn).2 hZ⟩

/-- **The bound `p^{|E ∪ F|}` for sets.** If `Φ_q ∤ A`, then `|A| ≥ p^r`, where `r` is the number of levels
`ℓ` in `1..n` at which `Φ_{p^ℓ}` or `Φ_{p^ℓ q}` divides `A`. -/
theorem pow_card_levels_le_card (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ n * q))) (h0 : ¬ Pqr.ZeroAt A q) :
    p ^ (levelsE A ∪ levelsF A).card ≤ A.card := by
  have hp : p.Prime := Fact.out
  have h := pow_card_union_le_size hp.two_le (treeOf A) (fun h => h0 ((F_treeOf_zero A).1 h))
  rwa [eSet_treeOf, fSet_treeOf hpq, size_treeOf] at h

/-- **The sharp form of Lemma 3 for sets.** If `Φ_q ∤ A` and `k ≥ 1` levels `ℓ` in `1..n` have
`Φ_{p^ℓ q} ∣ A` and `Φ_{p^ℓ} ∤ A`, then `|A| ≥ p^e (p^k + q)`, `e` the number of levels with `Φ_{p^ℓ} ∣ A`. -/
theorem sharp_lemma3_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ n * q))) (h0 : ¬ Pqr.ZeroAt A q)
    (hk : (levelsF A \ levelsE A).Nonempty) :
    p ^ (levelsE A).card * (p ^ (levelsF A \ levelsE A).card + q) ≤ A.card := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have h := sharp_lemma3 hp.two_le hq.two_le ((Nat.coprime_primes hp hq).mpr hpq) (treeOf A)
    (fun h => h0 ((F_treeOf_zero A).1 h)) (by rwa [eSet_treeOf, fSet_treeOf hpq])
  rw [size_treeOf] at h
  simpa only [e, eSet_treeOf, fSet_treeOf hpq] using h

end Pnq
