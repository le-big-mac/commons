/-
The two lower bounds of the balanced half (`Φ_q ∣ A`) for subsets of `ZMod (p^n * q)`, in terms of the Fourier
zeros `Pqr.ZeroAt`.  Derived from `Pnq/Balanced.lean` (the tree) through the bridge of `Pnq/Group.lean`.
(agent3 / Yonder, 26 Nov 2026)
-/
import Pnq.Balanced
import Pnq.SharpGroup

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

open Classical in
/-- the levels beyond `a0` with `Φ_{p^ℓ q} ∣ A` and `Φ_{p^ℓ} ∤ A` -/
noncomputable def levelsBeyond (A : Finset (ZMod (p ^ n * q))) (a0 : ℕ) : Finset ℕ :=
  (levelsF A \ levelsE A).filter (fun ℓ => a0 < ℓ)

theorem gBeyond_treeOf (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) (a0 : ℕ) :
    gBeyond (treeOf A) a0 = levelsBeyond A a0 := by
  unfold gBeyond levelsBeyond
  rw [eSet_treeOf, fSet_treeOf hpq]

/-- **The base bound for sets.** If `Φ_q ∣ A`, `Φ_{p^ℓ q} ∣ A` for every level `ℓ` before `a0`, and
`Φ_{p^{a0} q} ∤ A`, then `|A| ≥ q · p^(e + k')`: `e` the number of levels with `Φ_{p^ℓ} ∣ A`, `k'` the number
of levels beyond `a0` with `Φ_{p^ℓ q} ∣ A` and `Φ_{p^ℓ} ∤ A`. -/
theorem balanced_base_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ n * q))) (a0 : ℕ) (h0 : Pqr.ZeroAt A q)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → Pqr.ZeroAt A (p ^ ℓ * q)) (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hna : ¬ Pqr.ZeroAt A (p ^ a0 * q)) :
    q * p ^ ((levelsE A).card + (levelsBeyond A a0).card) ≤ A.card := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have h := balanced_base hp.two_le hq.two_le ((Nat.coprime_primes hp hq).mpr hpq) (treeOf A) a0
    ((F_treeOf_zero A).2 h0)
    (fun ℓ h1 hl => (F_treeOf hpq A ℓ h1 (by omega)).2 (hlow ℓ h1 hl)) ha1 han
    (fun hF => hna ((F_treeOf hpq A a0 ha1 han).1 hF))
  rw [size_treeOf, gBeyond_treeOf hpq] at h
  simpa only [e, eSet_treeOf] using h

/-- **The bound with the extra fibre, for sets.** If moreover some level beyond `a0` has `Φ_{p^ℓ q} ∣ A` and
`Φ_{p^ℓ} ∤ A`, no level before `a0` has `Φ_{p^ℓ} ∣ A`, and either `Φ_{p^{a0}} ∤ A`, or `p = 2` and every level
`b` strictly between `a0` and the first such level with `Φ_{p^b} ∣ A` also has `Φ_{p^b q} ∣ A`, then
`|A| ≥ q · p^e · (p^k' + 1)`. -/
theorem balanced_plus_zmod (p q n : ℕ) [Fact p.Prime] [Fact q.Prime] (hpq : p ≠ q)
    (A : Finset (ZMod (p ^ n * q))) (a0 : ℕ) (h0 : Pqr.ZeroAt A q)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → Pqr.ZeroAt A (p ^ ℓ * q)) (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hna : ¬ Pqr.ZeroAt A (p ^ a0 * q))
    (hk : (levelsBeyond A a0).Nonempty)
    (h2 : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ¬ Pqr.ZeroAt A (p ^ ℓ))
    (h34 : ¬ Pqr.ZeroAt A (p ^ a0) ∨
      (p = 2 ∧ ∀ b, a0 < b → b ≤ n → (∀ g ∈ levelsBeyond A a0, b < g) →
        Pqr.ZeroAt A (p ^ b) → Pqr.ZeroAt A (p ^ b * q))) :
    q * p ^ (levelsE A).card * (p ^ (levelsBeyond A a0).card + 1) ≤ A.card := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hp0 : 0 < p := hp.pos
  have h := balanced_plus hp.two_le hq.two_le ((Nat.coprime_primes hp hq).mpr hpq) (treeOf A) a0
    ((F_treeOf_zero A).2 h0)
    (fun ℓ h1 hl => (F_treeOf hpq A ℓ h1 (by omega)).2 (hlow ℓ h1 hl)) ha1 han
    (fun hF => hna ((F_treeOf hpq A a0 ha1 han).1 hF))
    (by rw [gBeyond_treeOf hpq]; exact hk)
    (fun ℓ hl hE => by
      have hr := E_range hp0 (treeOf A) ℓ hE
      exact h2 ℓ hr.1 hl ((E_treeOf A ℓ hr.1 hr.2).1 hE))
    (by
      rcases h34 with h | ⟨h2', h⟩
      · exact Or.inl (fun hE => h ((E_treeOf A a0 ha1 han).1 hE))
      · refine Or.inr ⟨h2', fun b hb hg hE => ?_⟩
        have hr := E_range hp0 (treeOf A) b hE
        rw [gBeyond_treeOf hpq] at hg
        exact (F_treeOf hpq A b hr.1 hr.2).2 (h b hb hr.2 hg ((E_treeOf A b hr.1 hr.2).1 hE)))
  rw [size_treeOf, gBeyond_treeOf hpq] at h
  simpa only [e, eSet_treeOf] using h

end Pnq
