/-
The constructions for the half with `Φ_q ∣ A`: for every pattern a tree with exactly that pattern and the
least size.  (Statements fixed by agent3 / Yonder, 26 November 2026.)
-/
import Pnq.Rule
import Pnq.BuildB5

open Finset

namespace Pnq

variable {p q : ℕ}

/-- **The construction, `Φ_q ∣ A`, every level in `F`.** For every set `Es` of levels in `1..n` there is a
balanced tree whose levels of `E` are exactly `Es`, whose levels `≥ 1` of `F` are all of `1..n`, and which has
`q · p^|Es|` elements. -/
theorem exists_balanced_all (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) :
    ∃ t : Tree p q n, F t 0 ∧ eSet t = Es ∧ fSet t = Finset.Icc 1 n ∧ size t = q * p ^ Es.card := by
  refine ⟨BuildB.fib Es n 0, BuildB.F_fib hp Es n 0 0 (Nat.zero_le _), ?_, ?_, ?_⟩
  · ext ℓ
    rw [mem_eSet]
    constructor
    · rintro ⟨h1, h2, h3⟩
      have := (BuildB.E_fib hp (by omega) Es n 0 ℓ h1 h2).1 h3
      rwa [Nat.zero_add] at this
    · intro h
      have h' := Finset.mem_Icc.1 (hE h)
      refine ⟨h'.1, h'.2, (BuildB.E_fib hp (by omega) Es n 0 ℓ h'.1 h'.2).2 ?_⟩
      rwa [Nat.zero_add]
  · ext ℓ
    rw [mem_fSet, Finset.mem_Icc]
    constructor
    · rintro ⟨h1, h2, -⟩
      exact ⟨h1, h2⟩
    · rintro ⟨h1, h2⟩
      exact ⟨h1, h2, BuildB.F_fib hp Es n 0 ℓ h2⟩
  · rw [BuildB.size_fib (by omega), BuildB.pw_root hE]

/-- **The construction, `Φ_q ∣ A`, some level missing from `F`.** Let `Es`, `Fs` be sets of levels in `1..n`
and `a0` the first level in `1..n` that is not in `Fs`.  There is a balanced tree whose levels of `E` are
exactly `Es`, whose levels `≥ 1` of `F` are exactly `Fs`, and which has `minB p q Es Fs a0` elements. -/
theorem exists_balanced (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) (n : ℕ) (Es Fs : Finset ℕ)
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) (a0 : ℕ) (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) :
    ∃ t : Tree p q n, F t 0 ∧ eSet t = Es ∧ fSet t = Fs ∧ size t = minB p q Es Fs a0 := by
  have hGlt : ∀ g ∈ gOf Es Fs a0, a0 < g := fun g hg => (BuildB.mem_gOf.1 hg).2.2
  have hMpos : 1 ≤ p ^ (gOf Es Fs a0).card := Nat.one_le_pow _ _ (by omega)
  have hpU : ∀ k, 0 < BuildB.pw p (BuildB.UU Es Fs a0) k a0 := fun k => BuildB.pw_pos (by omega) _ k a0
  by_cases c1 : gOf Es Fs a0 = ∅
  · -- case (I) of the proof on paper: clause (1), no level beyond `a0` is in `Fs` and not in `Es`
    obtain ⟨t, h1, h2, h3, h4⟩ := BuildB.exists_mode0 hp hq hpq hE hF ha1 han hlow hna 0 1 0 (Or.inl rfl)
      (fun _ hp2 k _ => BuildB.mid_zero hq (hp2 ▸ hpq) (hpU k))
      (fun g hgU hgE => by
        have hg := BuildB.mem_gOf_of_UU hgU hgE
        rw [c1] at hg
        exact absurd hg (Finset.notMem_empty g))
    refine ⟨t, h1, h2, h3, ?_⟩
    rw [h4]
    exact BuildB.size_eq hE hF 0 (by unfold xOf; rw [ite_eq_left (Or.inl c1)])
  by_cases c2 : ∃ ℓ ∈ Es, ℓ < a0
  · -- case (III): clause (2), a level `b` of `Es` before `a0` is the host level
    obtain ⟨b, hbE, hba⟩ := c2
    have hb1 : 1 ≤ b := (Finset.mem_Icc.1 (hE hbE)).1
    obtain ⟨t, h1, h2, h3, h4⟩ := BuildB.exists_mode0 hp hq hpq hE hF ha1 han hlow hna b
      (p ^ (gOf Es Fs a0).card) 0
      (Or.inr ⟨hbE, by omega,
        fun k hk => BuildB.pw_UU hF b k hk (fun g hg => by have := hGlt g hg; omega), fun h => by omega⟩)
      (fun _ hp2 k _ => BuildB.mid_zero hq (hp2 ▸ hpq) (hpU k))
      (fun g hgU hgE => Or.inr
        ⟨by omega, by have := hGlt g (BuildB.mem_gOf_of_UU hgU hgE); omega, hMpos⟩)
    refine ⟨t, h1, h2, h3, ?_⟩
    rw [h4]
    exact BuildB.size_eq hE hF 0 (by unfold xOf; rw [ite_eq_left (Or.inr (Or.inl ⟨b, hbE, hba⟩))])
  by_cases c3 : a0 ∈ Es ∧ 3 ≤ p
  · -- case (IV): clause (3), the level `a0` itself is the host level
    obtain ⟨t, h1, h2, h3, h4⟩ := BuildB.exists_modeW c3.2 hq hpq hE hF ha1 han hlow hna c3.1
      (p ^ (gOf Es Fs a0).card) hMpos (fun k hk => BuildB.pw_UU hF a0 k hk hGlt)
    refine ⟨t, h1, h2, h3, ?_⟩
    rw [h4]
    exact BuildB.size_eq hE hF 0 (by unfold xOf; rw [ite_eq_left (Or.inr (Or.inr (Or.inl c3)))])
  by_cases c4 : a0 ∈ Es ∧ p = 2 ∧ ∃ b ∈ Es \ Fs, a0 < b ∧ ∀ g ∈ gOf Es Fs a0, b < g
  · -- case (V): clause (4), a level `b` of `Es ∖ Fs` between `a0` and the levels of `gOf` is the host level
    have c4' := c4
    obtain ⟨haE, -, b, hb, hab, hbg⟩ := c4
    have hbE := (Finset.mem_sdiff.1 hb).1
    have hbF := (Finset.mem_sdiff.1 hb).2
    obtain ⟨t, h1, h2, h3, h4⟩ := BuildB.exists_mode0 hp hq hpq hE hF ha1 han hlow hna b
      (p ^ (gOf Es Fs a0).card) 0
      (Or.inr ⟨hbE, by omega, fun k hk => BuildB.pw_UU hF b k hk hbg, fun _ => ⟨hbF, haE⟩⟩)
      (fun h => absurd haE h)
      (fun g hgU hgE => Or.inr ⟨by omega, hbg g (BuildB.mem_gOf_of_UU hgU hgE), hMpos⟩)
    refine ⟨t, h1, h2, h3, ?_⟩
    rw [h4]
    exact BuildB.size_eq hE hF 0 (by unfold xOf; rw [ite_eq_left (Or.inr (Or.inr (Or.inr c4')))])
  · -- case (II): no clause holds; the shape part with one fibre over every string that is `0` outside `Es`
    have hx : xOf p Es Fs a0 = 1 := by
      unfold xOf
      rw [ite_eq_right]
      rintro (h | h | h | h)
      · exact c1 h
      · exact c2 h
      · exact c3 h
      · exact c4 h
    have hU2 : a0 ∉ Es → p = 2 → ∀ k, a0 + k = n →
        BuildB.pw p (BuildB.UU Es Fs a0) k a0 + q * (1 * BuildB.pw p Es k a0)
          ≠ (q - 1) * BuildB.pw p (BuildB.UU Es Fs a0) k a0 := by
      intro _ hp2 k hk
      subst hp2
      obtain ⟨c, hc⟩ : ∃ c, (gOf Es Fs a0).card = c + 1 :=
        ⟨(gOf Es Fs a0).card - 1, by
          have := Finset.card_pos.2 (Finset.ne_empty_iff_nonempty.1 c1)
          omega⟩
      rw [BuildB.pw_UU hF a0 k hk hGlt, hc, pow_succ']
      exact BuildB.mid_one hpq (BuildB.pw_pos (by omega) Es k a0)
    obtain ⟨t, h1, h2, h3, h4⟩ := BuildB.exists_mode0 hp hq hpq hE hF ha1 han hlow hna 0 1 1 (Or.inl rfl)
      hU2 (fun _ _ _ => Or.inl (le_refl 1))
    refine ⟨t, h1, h2, h3, ?_⟩
    rw [h4]
    exact BuildB.size_eq hE hF 1 hx

end Pnq
