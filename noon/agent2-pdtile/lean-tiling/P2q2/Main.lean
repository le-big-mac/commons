/-
Weak tiling implies tiling in `ZMod (p^2 * q^2)`, for distinct primes `p`, `q`: the assembly.

* `exists_nine` (`Nine.lean`): a weak tile has a step complement, whose nine Möbius coefficients satisfy the
  constraints of the linear programme of its zero pattern;
* `dispatchA`, `dispatchB` (generated, `DispatchA.lean`, `DispatchB.lean`, from the certificates in the files
  `Certs*.lean`): for `p < q` and each zero pattern, one of six outcomes;
* each outcome ends with a tiling or a contradiction: `tiling_of_units_charged` (Lemma 2), `tiling_of_patA`
  (Coven–Meyerowitz), `tiling_of_support_p`, `tiling_of_support_q` (Lemma 3), `zeroAt_pq2_of_card` (the counting
  lemma), `no_card` (arithmetic).
-/
import P2q2.DispatchA
import P2q2.DispatchB
import P2q2.Nine
import P2q2.Pattern
import P2q2.Reduce
import P2q2.LemmaY
import P2q2.Arith

open Finset

namespace P2q2

open Pqr

/-- The linear-programming fact behind Lemma 2: if the transform of a step complement vanishes at the orders
`p` and `q`, the complement is positive on the units. -/
theorem m00_pos (p q n : ℝ) (ha : Atoms p q) (x : Nine) (hadm : x.Admissible) (h10 : x.L10 p q = 0)
    (h01 : x.L01 p q = 0) (hn : n * x.L00 p q = p ^ 2 * q ^ 2) (hn0 : 0 < n) : 0 < x.m00 := by
  obtain ⟨a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21,
    a22, a23, a24⟩ := ha
  obtain ⟨hg00, hg01, hg02, hg10, hg11, hg12, hg20, hg21, hg22e⟩ := hadm
  have hg22 : 0 ≤ x.g22 := by rw [hg22e]; norm_num
  have hL : 0 < x.L00 p q := by
    have h1 : 0 < n * x.L00 p q := by rw [hn]; positivity
    exact (mul_pos_iff_of_pos_left hn0).1 h1
  have key : (p - 1) * (q - 1) * (p ^ 2 * q ^ 2) * x.m00
      = (p * q - p - q) * x.L00 p q
        + p * q * ((p - 1) * (q - 1) * x.g11 + (p - 1) * x.g12 + (q - 1) * x.g21 + x.g22) := by
    simp only [Nine.L00, Nine.L10, Nine.L01, Nine.g11, Nine.g12, Nine.g21, Nine.g22] at *
    linear_combination (-(p - 1) * q) * h10 + (-(p * (q - 1))) * h01
  have hc : 0 < (p - 1) * (q - 1) * (p ^ 2 * q ^ 2) := by positivity
  have hr : 0 < (p - 1) * (q - 1) * (p ^ 2 * q ^ 2) * x.m00 := by rw [key]; positivity
  exact (mul_pos_iff_of_pos_left hc).1 hr

variable (p q : ℕ) [Fact p.Prime] [Fact q.Prime]

/-- **Weak tiling implies tiling in `Z_{p²q²}`** (the case `p < q`). -/
theorem weak_tiling_tiles_p2q2_of_lt (hlt : p < q) (A : Finset (ZMod (p ^ 2 * q ^ 2)))
    (f : ZMod (p ^ 2 * q ^ 2) → ℝ) (h : WeakTiling A f) :
    ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B := by
  have hpq : p ≠ q := hlt.ne
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  obtain ⟨μ, hμ, hadm, hvan, hcard⟩ := exists_nine p q hpq A f h
  have hA : A.Nonempty := nonempty_of_weakTiling A f h
  have hn0 : (0 : ℝ) < A.card := Nat.cast_pos.2 hA.card_pos
  have hk := kfac_le_card p q hpq A hA
  have hp2 : (2 : ℝ) ≤ p := by exact_mod_cast hp.two_le
  have hpq1 : (p : ℝ) + 1 ≤ q := by exact_mod_cast Nat.succ_le_of_lt hlt
  have ha := atoms_of (p : ℝ) q hp2 hpq1
  have hqp2 : q ≠ p ^ 2 := by
    intro e
    have hd : p ∣ q := e ▸ dvd_pow_self p two_ne_zero
    exact hpq ((Nat.prime_dvd_prime_iff_eq hp hq).1 hd)
  have hout : Outcome (p : ℝ) q A.card (ZeroAt A q) (ZeroAt A (q ^ 2)) (ZeroAt A p) (ZeroAt A (p * q))
      (ZeroAt A (p * q ^ 2)) (ZeroAt A (p ^ 2)) (ZeroAt A (p ^ 2 * q)) (ZeroAt A (p ^ 2 * q ^ 2)) := by
    have b0 := ha.a0
    have b1 := ha.a1
    have b3 := ha.a3
    rcases Nat.lt_or_gt_of_ne hqp2 with hlt2 | hgt2
    · have h0 : (q : ℝ) + 1 ≤ (p : ℝ) ^ 2 := by exact_mod_cast Nat.succ_le_of_lt hlt2
      have h1 : (0 : ℝ) < (p : ℝ) ^ 2 - q := by linarith
      have h2 : (0 : ℝ) < 2 * (p : ℝ) ^ 2 * q - (p : ℝ) ^ 2 - (q : ℝ) ^ 2 := by
        have e : 2 * (p : ℝ) ^ 2 * q - (p : ℝ) ^ 2 - (q : ℝ) ^ 2
            = q * ((p : ℝ) ^ 2 - q) + (p : ℝ) ^ 2 * ((q : ℝ) - 1) := by ring
        rw [e]; positivity
      exact dispatchA (p : ℝ) q A.card ha h1 h2 _ _ _ _ _ _ _ _ (Nine.ofMu p q μ) hadm hvan hcard hn0 hk
    · have h0 : (p : ℝ) ^ 2 + 1 ≤ q := by exact_mod_cast Nat.succ_le_of_lt hgt2
      have h1 : (0 : ℝ) < -(p : ℝ) ^ 2 + q := by linarith
      exact dispatchB (p : ℝ) q A.card ha h1 _ _ _ _ _ _ _ _ (Nine.ofMu p q μ) hadm hvan hcard hn0 hk
  rcases hout with ⟨h10, h01⟩ | hpat | ⟨x', hx', hv', hle', s0, s1, s2⟩ | ⟨x', hx', hv', hle', s0, s1, s2⟩ |
    ⟨hn, h10, h22, h12⟩ | ⟨x', hx', hv', hle', heq⟩
  · -- neither `p` nor `q` is a zero: the step complement is positive on the units (Lemma 2)
    have hm : 0 < (Nine.ofMu p q μ).m00 :=
      m00_pos (p : ℝ) q A.card ha (Nine.ofMu p q μ) hadm (hvan.2.2.1 h10) (hvan.1 h01) hcard hn0
    refine tiling_of_units_charged p q hpq A _ hμ (fun y hy1 hy2 => ?_)
    rw [stepFn_unit p q hpq μ y hy1 hy2]
    exact hm
  · -- (T2) and no orphan
    exact tiling_of_patA p q hpq A f h hpat
  · -- an optimal complement vanishing outside `pZ` (Lemma 3)
    have hw := weakTiling_of_nine p q hpq A hA x' hx' hv' hle'
    exact tiling_of_support_p p q hpq A _ hw
      (fun y hy => stepFn_toMu_of_not_dvd_p p q hpq x' s0 s1 s2 y hy)
  · -- an optimal complement vanishing outside `qZ` (Lemma 3)
    have hw := weakTiling_of_nine p q hpq A hA x' hx' hv' hle'
    exact tiling_of_support_q p q hpq A _ hw
      (fun y hy => stepFn_toMu_of_not_dvd_q p q hpq x' s0 s1 s2 y hy)
  · -- `|A| = pq` with the zeros `p`, `p²q²` but not `pq²`: excluded by the counting lemma
    have hc : A.card = p * q := by exact_mod_cast hn
    exact absurd (zeroAt_pq2_of_card p q hpq A hc h10 h22) h12
  · -- the size would not be an integer
    have hw := weakTiling_of_nine p q hpq A hA x' hx' hv' hle'
    have hc := card_mul_L00_of_weakTiling_toMu p q hpq A x' hw
    refine (no_card p q A.card hp hq hpq ?_).elim
    rw [← heq]
    linear_combination ((p : ℝ) * q - 1) * hc

/-- **Weak tiling implies tiling in `Z_{p²q²}`.** If `A ⊆ ZMod (p^2 * q^2)`, `p ≠ q` primes, has a weak tiling
complement (`f ≥ 0`, `f 0 = 1`, `∑ a ∈ A, f (v - a) = 1` for all `v`), then `A ⊕ B = ZMod (p^2 * q^2)` for some `B`. -/
theorem weak_tiling_tiles_p2q2 (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2)))
    (f : ZMod (p ^ 2 * q ^ 2) → ℝ) (h : WeakTiling A f) :
    ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B := by
  rcases Nat.lt_or_gt_of_ne hpq with hlt | hgt
  · exact weak_tiling_tiles_p2q2_of_lt p q hlt A f h
  · -- exchange the two primes: `ZMod (p^2 * q^2) ≃+ ZMod (q^2 * p^2)`
    let e : ZMod (p ^ 2 * q ^ 2) ≃+ ZMod (q ^ 2 * p ^ 2) :=
      (ZMod.ringEquivCongr (Nat.mul_comm (p ^ 2) (q ^ 2))).toAddEquiv
    obtain ⟨B', hB'⟩ := weak_tiling_tiles_p2q2_of_lt q p hgt (A.map e.toEquiv.toEmbedding) _ (h.map e)
    exact ⟨_, hB'.of_map e⟩

/-- **Tiles and weak tiles of `Z_{p²q²}` are the same sets.** -/
theorem weak_tiling_iff_tiling_p2q2 (hpq : p ≠ q) (A : Finset (ZMod (p ^ 2 * q ^ 2))) :
    (∃ f : ZMod (p ^ 2 * q ^ 2) → ℝ, WeakTiling A f) ↔ ∃ B : Finset (ZMod (p ^ 2 * q ^ 2)), IsTiling A B :=
  ⟨fun ⟨f, hf⟩ => weak_tiling_tiles_p2q2 p q hpq A f hf, fun ⟨_, hB⟩ => hB.weakTiling⟩

end P2q2
