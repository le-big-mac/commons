/-
The same theorem stated in the cyclic group `ZMod (p * q * r)`, by the Chinese remainder theorem.
-/
import Pqr.Main

open Finset

set_option linter.unusedSectionVars false

namespace Pqr

/-- weak tiling complements are transported by group isomorphisms -/
theorem WeakTiling.map {G H : Type*} [AddCommGroup G] [AddCommGroup H] (e : G ≃+ H)
    {A : Finset G} {f : G → ℝ} (h : WeakTiling A f) :
    WeakTiling (A.map e.toEquiv.toEmbedding) (fun w => f (e.symm w)) := by
  refine ⟨fun w => h.1 _, by simpa using h.2.1, fun w => ?_⟩
  rw [Finset.sum_map]
  have := h.2.2 (e.symm w)
  simpa [map_sub] using this

/-- tilings are transported back by group isomorphisms -/
theorem IsTiling.of_map {G H : Type*} [AddCommGroup G] [AddCommGroup H] (e : G ≃+ H)
    {A : Finset G} {B' : Finset H} (h : IsTiling (A.map e.toEquiv.toEmbedding) B') :
    IsTiling A (B'.map e.symm.toEquiv.toEmbedding) := by
  intro v
  obtain ⟨⟨a', b'⟩, ⟨ha', hb', hab⟩, huniq⟩ := h (e v)
  simp only [Finset.mem_map, Equiv.coe_toEmbedding] at ha'
  obtain ⟨a, ha, rfl⟩ := ha'
  refine ⟨(a, e.symm b'), ⟨ha, ?_, ?_⟩, ?_⟩
  · simp only [Finset.mem_map, Equiv.coe_toEmbedding]
    exact ⟨b', hb', rfl⟩
  · apply e.injective
    simpa using hab
  · rintro ⟨a2, b2⟩ ⟨ha2, hb2, hab2⟩
    simp only [Finset.mem_map, Equiv.coe_toEmbedding] at hb2
    obtain ⟨b2', hb2', rfl⟩ := hb2
    have := huniq (e a2, b2') ⟨by simpa using ha2, hb2', by
      have := congrArg e hab2
      simpa using this⟩
    simp only [Prod.mk.injEq] at this
    obtain ⟨h1, h2⟩ := this
    rw [e.injective h1, h2]
    rfl

/-- The easy direction, in any finite abelian group: a tile has a weak tiling complement (the
indicator of a translate of its tiling complement). -/
theorem IsTiling.weakTiling {G : Type*} [AddCommGroup G] [DecidableEq G] {A B : Finset G}
    (h : IsTiling A B) : ∃ f : G → ℝ, WeakTiling A f := by
  obtain ⟨⟨a0, b0⟩, ⟨-, hb0, -⟩, -⟩ := h 0
  simp only at hb0
  refine ⟨fun x => if x + b0 ∈ B then 1 else 0, fun v => by positivity, by simp [hb0],
    fun v => ?_⟩
  obtain ⟨⟨a1, b1⟩, ⟨ha1, hb1, hab⟩, huniq⟩ := h (v + b0)
  simp only at ha1 hb1 hab
  have hb1' : v - a1 + b0 = b1 := by
    calc v - a1 + b0 = (v + b0) - a1 := by abel
      _ = b1 := by rw [← hab]; abel
  rw [Finset.sum_eq_single a1]
  · simp [hb1', hb1]
  · intro a ha hne
    have : v - a + b0 ∉ B := by
      intro hmem
      have := huniq (a, v - a + b0) ⟨ha, hmem, by simp only; abel⟩
      exact hne (Prod.mk.inj this).1
    simp [this]
  · intro hna
    exact absurd ha1 hna

variable (p q r : ℕ) [Fact p.Prime] [Fact q.Prime] [Fact r.Prime]

/-- the Chinese remainder isomorphism `Z_{pqr} ≅ Z_p × Z_q × Z_r` of additive groups -/
noncomputable def crt3 (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r) :
    ZMod (p * q * r) ≃+ ZMod p × ZMod q × ZMod r :=
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hr : r.Prime := Fact.out
  have c1 : (p * q).Coprime r :=
    Nat.Coprime.mul_left ((Nat.coprime_primes hp hr).mpr hpr) ((Nat.coprime_primes hq hr).mpr hqr)
  have c2 : p.Coprime q := (Nat.coprime_primes hp hq).mpr hpq
  ((ZMod.chineseRemainder c1).toAddEquiv.trans
    (AddEquiv.prodCongr (ZMod.chineseRemainder c2).toAddEquiv (AddEquiv.refl (ZMod r)))).trans
    AddEquiv.prodAssoc

/-- **Weak tiling implies tiling in the cyclic group `Z_{pqr}`**, `p`, `q`, `r` distinct primes. -/
theorem weak_tiling_tiles_cyclic (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (A : Finset (ZMod (p * q * r))) (f : ZMod (p * q * r) → ℝ) (h : WeakTiling A f) :
    ∃ B : Finset (ZMod (p * q * r)), IsTiling A B := by
  obtain ⟨B', hB'⟩ := weak_tiling_tiles p q r hpq hpr hqr _ _ (h.map (crt3 p q r hpq hpr hqr))
  exact ⟨_, hB'.of_map (crt3 p q r hpq hpr hqr)⟩

/-- In particular every set that pd-tiles `Z_{pqr}` (a weak tiling complement whose Fourier
transform is also nonnegative; that extra hypothesis is not needed) tiles. -/
theorem pd_tiling_tiles_cyclic (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (A : Finset (ZMod (p * q * r))) (f : ZMod (p * q * r) → ℝ) (h : WeakTiling A f)
    (_hpd : ∀ k : ZMod (p * q * r), 0 ≤ (ZMod.dft (fun x => (f x : ℂ)) k).re) :
    ∃ B : Finset (ZMod (p * q * r)), IsTiling A B :=
  weak_tiling_tiles_cyclic p q r hpq hpr hqr A f h

/-- **Tiles and weak tiles of `Z_{pqr}` are the same sets.** -/
theorem weak_tiling_iff_tiling_cyclic (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r)
    (A : Finset (ZMod (p * q * r))) :
    (∃ f : ZMod (p * q * r) → ℝ, WeakTiling A f) ↔ ∃ B : Finset (ZMod (p * q * r)), IsTiling A B :=
  ⟨fun ⟨f, hf⟩ => weak_tiling_tiles_cyclic p q r hpq hpr hqr A f hf, fun ⟨_, hB⟩ => hB.weakTiling⟩

end Pqr
