/-
**(i)** A weak tiling complement of `A ⊆ ZMod (p^n * q)` gives a step weak tiling complement of the tree of `A`
(averaging over the units, then an induction along the tree).
-/
import Pnq.Step
import Pnq.Group
import Pqr.Counting

open Finset

namespace Pnq

variable {p q n : ℕ} [Fact p.Prime] [Fact q.Prime]

/-! ### Residues of a difference in `ZMod M` -/

/-- For `d ∣ M`: `d` divides the representative of `v - a` iff the representatives of `v` and `a` agree
modulo `d`. -/
private theorem dvd_val_sub_iff {M : ℕ} [NeZero M] {d : ℕ} (hd : d ∣ M) (v a : ZMod M) :
    d ∣ (v - a).val ↔ v.val % d = a.val % d := by
  have h1 : (((v - a).val + a.val : ℕ) : ZMod M) = ((v.val : ℕ) : ZMod M) := by
    rw [Nat.cast_add, ZMod.natCast_zmod_val, ZMod.natCast_zmod_val, ZMod.natCast_zmod_val,
      sub_add_cancel]
  have h2 : (v - a).val + a.val ≡ v.val [MOD d] :=
    ((ZMod.natCast_eq_natCast_iff _ _ _).1 h1).of_dvd hd
  constructor
  · intro h
    have h0 : (v - a).val ≡ 0 [MOD d] := Nat.modEq_zero_iff_dvd.2 h
    have h3 : (v - a).val + a.val ≡ a.val [MOD d] := by
      simpa using h0.add_right a.val
    exact h2.symm.trans h3
  · intro h
    have h3 : (v - a).val + a.val ≡ 0 + a.val [MOD d] := by
      rw [zero_add]
      exact h2.trans h
    exact Nat.modEq_zero_iff_dvd.1 (Nat.ModEq.add_right_cancel' _ h3)

/-- the gcd with a prime power, from the exact power of `p` dividing `x` (capped at `n`) -/
private theorem gcd_prime_pow_eq {p : ℕ} (hp : p.Prime) {x n d : ℕ} (hdn : d ≤ n) (h1 : p ^ d ∣ x)
    (h2 : d < n → ¬ p ^ (d + 1) ∣ x) : x.gcd (p ^ n) = p ^ d := by
  obtain ⟨j, hj, hjeq⟩ := (Nat.dvd_prime_pow hp).1 (Nat.gcd_dvd_right x (p ^ n))
  have hdj : d ≤ j := by
    have h : p ^ d ∣ p ^ j := hjeq ▸ Nat.dvd_gcd h1 (pow_dvd_pow p hdn)
    exact (Nat.pow_dvd_pow_iff_le_right hp.one_lt).1 h
  have hjd : j ≤ d := by
    by_contra hcon
    have hlt : d < n := by omega
    apply h2 hlt
    have h : p ^ (d + 1) ∣ p ^ j := pow_dvd_pow p (by omega)
    exact h.trans (hjeq ▸ Nat.gcd_dvd_left x (p ^ n))
  rw [hjeq, le_antisymm hjd hdj]

/-- the gcd with a prime -/
private theorem gcd_prime_eq {q : ℕ} (hq : q.Prime) (x : ℕ) :
    x.gcd q = if q ∣ x then q else 1 := by
  split_ifs with h
  · exact Nat.gcd_eq_right h
  · exact Nat.Coprime.symm ((Nat.Prime.coprime_iff_not_dvd hq).2 h)

/-- **The gcd of a difference.** If `v` and `a` agree modulo `p^d` and (when `d < n`) not modulo
`p^(d+1)`, then `gcd (v - a, p^n q)` is `p^d`, times `q` if they agree modulo `q`. -/
private theorem gcd_val_sub (hpq : p ≠ q) {d : ℕ} (hdn : d ≤ n) (v a : ZMod (p ^ n * q))
    (h1 : v.val % p ^ d = a.val % p ^ d)
    (h2 : d < n → v.val % p ^ (d + 1) ≠ a.val % p ^ (d + 1)) :
    (v - a).val.gcd (p ^ n * q) = p ^ d * (if v.val % q = a.val % q then q else 1) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hcop : Nat.Coprime (p ^ n) q := Nat.Coprime.pow_left n ((Nat.coprime_primes hp hq).2 hpq)
  rw [Nat.Coprime.gcd_mul _ hcop, gcd_prime_eq hq]
  congr 1
  · apply gcd_prime_pow_eq hp hdn
    · exact (dvd_val_sub_iff (Dvd.dvd.mul_right (pow_dvd_pow p hdn) q) v a).2 h1
    · intro hlt hdvd
      exact h2 hlt ((dvd_val_sub_iff (Dvd.dvd.mul_right (pow_dvd_pow p hlt) q) v a).1 hdvd)
  · simp only [dvd_val_sub_iff (Dvd.intro_left (p ^ n) rfl) v a]

/-! ### The step function -/

/-- The step function read off from `g`: the value of `g` at `p^d` (`b = false`) or `p^d q` (`b = true`). -/
private noncomputable def stepOf (g : ZMod (p ^ n * q) → ℝ) (d : ℕ) (b : Bool) : ℝ :=
  g ((p ^ d * (if b then q else 1) : ℕ) : ZMod (p ^ n * q))

/-- A function that depends only on the gcd with `p^n q` takes the value `stepOf g d _` at a difference
that vanishes in exactly the lowest `d` digits. -/
private theorem g_sub (hpq : p ≠ q) (g : ZMod (p ^ n * q) → ℝ)
    (hg : ∀ x, g x = g ((x.val.gcd (p ^ n * q) : ℕ) : ZMod (p ^ n * q)))
    {d : ℕ} (hdn : d ≤ n) (v a : ZMod (p ^ n * q))
    (h1 : v.val % p ^ d = a.val % p ^ d)
    (h2 : d < n → v.val % p ^ (d + 1) ≠ a.val % p ^ (d + 1)) :
    g (v - a) = if a.val % q = v.val % q then stepOf g d true else stepOf g d false := by
  rw [hg (v - a), gcd_val_sub hpq hdn v a h1 h2]
  unfold stepOf
  by_cases h : v.val % q = a.val % q
  · rw [ite_eq_left h, ite_eq_left h.symm, ite_eq_left rfl]
  · have h' : ¬ a.val % q = v.val % q := fun e => h e.symm
    rw [ite_eq_right h, ite_eq_right h', ite_eq_right Bool.false_ne_true]

/-! ### Existence of points -/

/-- Chinese remainder theorem: a point with given residues modulo `p^d` and `q`. -/
private theorem exists_point (hpq : p ≠ q) {d : ℕ} (hdn : d ≤ n) {r : ℕ} (hr : r < p ^ d)
    (w : Fin q) : ∃ v : ZMod (p ^ n * q), v.val % p ^ d = r ∧ v.val % q = (w : ℕ) := by
  have hp : p.Prime := Fact.out
  have hq : q.Prime := Fact.out
  have hcop : Nat.Coprime (p ^ d) q := Nat.Coprime.pow_left d ((Nat.coprime_primes hp hq).2 hpq)
  obtain ⟨k, hk1, hk2⟩ := Nat.chineseRemainder hcop r w
  refine ⟨(k : ZMod (p ^ n * q)), ?_, ?_⟩
  · rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ (Dvd.dvd.mul_right (pow_dvd_pow p hdn) q)]
    exact (show k % p ^ d = r % p ^ d from hk1).trans (Nat.mod_eq_of_lt hr)
  · rw [ZMod.val_natCast, Nat.mod_mod_of_dvd _ (Dvd.intro_left (p ^ n) rfl)]
    exact (show k % q = (w : ℕ) % q from hk2).trans (Nat.mod_eq_of_lt w.2)

/-! ### Sums over residue classes -/

omit [Fact p.Prime] [Fact q.Prime] in
/-- a sum of a two-valued function over a finite set -/
private theorem sum_class (γt γf : ℝ) (g : ZMod (p ^ n * q) → ℝ) (S : Finset (ZMod (p ^ n * q)))
    (v : ZMod (p ^ n * q)) (w : ℕ)
    (h : ∀ a ∈ S, g (v - a) = if a.val % q = w then γt else γf) :
    ∑ a ∈ S, g (v - a) = γt * ((S.filter (fun a => a.val % q = w)).card : ℝ)
      + γf * ((S.card : ℝ) - ((S.filter (fun a => a.val % q = w)).card : ℝ)) := by
  rw [Finset.sum_congr rfl h, Finset.sum_ite, Finset.sum_const, Finset.sum_const, nsmul_eq_mul,
    nsmul_eq_mul]
  have hc := Finset.card_filter_add_card_filter_not (s := S) (fun a => a.val % q = w)
  have hc' : ((S.filter (fun a => ¬ a.val % q = w)).card : ℝ)
      = (S.card : ℝ) - ((S.filter (fun a => a.val % q = w)).card : ℝ) := by
    rw [← hc]
    push_cast
    ring
  rw [hc']
  ring

/-- the sum over the class `r'` modulo `p^d'`, in terms of the layer counts and the size of its subtree -/
private theorem sum_class_sub (A : Finset (ZMod (p ^ n * q))) (γt γf : ℝ) (g : ZMod (p ^ n * q) → ℝ)
    (k d' r' : ℕ) (hr' : r' < p ^ d') (v : ZMod (p ^ n * q)) (w : Fin q)
    (h : ∀ a ∈ A.filter (fun a => a.val % p ^ d' = r'),
      g (v - a) = if a.val % q = (w : ℕ) then γt else γf) :
    ∑ a ∈ A.filter (fun a => a.val % p ^ d' = r'), g (v - a)
      = γt * (lay (sub A k d' r') w : ℝ)
        + γf * ((size (sub A k d' r') : ℝ) - (lay (sub A k d' r') w : ℝ)) := by
  rw [sum_class γt γf g _ v w h, lay_sub A k d' r' hr' w, size_sub A k d' r' hr',
    Finset.filter_filter]

/-- the residue modulo `p^(d+1)` is the residue modulo `p^d` together with the next digit -/
private theorem mod_pow_succ_iff {p : ℕ} (x d r c : ℕ) (hp : 0 < p) (hr : r < p ^ d) :
    x % p ^ (d + 1) = r + c * p ^ d ↔ x % p ^ d = r ∧ x / p ^ d % p = c := by
  have hpd : 0 < p ^ d := Nat.pow_pos hp
  rw [Nat.mod_pow_succ]
  constructor
  · intro h
    have h1 : x % p ^ d = r := by
      have h' := congrArg (· % p ^ d) h
      simp only [Nat.add_mul_mod_self_left, Nat.add_mul_mod_self_right, Nat.mod_mod,
        Nat.mod_eq_of_lt hr] at h'
      exact h'
    refine ⟨h1, ?_⟩
    rw [h1] at h
    have h2 : p ^ d * (x / p ^ d % p) = p ^ d * c := by
      rw [mul_comm (p ^ d) c]
      omega
    exact Nat.eq_of_mul_eq_mul_left hpd h2
  · rintro ⟨h1, h2⟩
    rw [h1, h2, mul_comm]

/-- a point of the class `r + c p^d` modulo `p^(d+1)` is in the class `r` modulo `p^d` -/
private theorem mod_pow_of_succ {p : ℕ} {x d r c : ℕ} (hp : 0 < p) (hr : r < p ^ d)
    (h : x % p ^ (d + 1) = r + c * p ^ d) : x % p ^ d = r :=
  ((mod_pow_succ_iff x d r c hp hr).1 h).1

omit [Fact q.Prime] in
/-- the class `r` modulo `p^d` is the disjoint union of the classes `r + c p^d` modulo `p^(d+1)` -/
private theorem sum_split (A : Finset (ZMod (p ^ n * q))) (F : ZMod (p ^ n * q) → ℝ) (d r : ℕ)
    (hr : r < p ^ d) :
    ∑ a ∈ A.filter (fun a => a.val % p ^ d = r), F a
      = ∑ c : Fin p, ∑ a ∈ A.filter (fun a => a.val % p ^ (d + 1) = r + (c : ℕ) * p ^ d), F a := by
  have hp : p.Prime := Fact.out
  rw [← Finset.sum_fiberwise_of_maps_to (s := A.filter (fun a => a.val % p ^ d = r))
    (t := Finset.univ) (g := fun a => (⟨a.val / p ^ d % p, Nat.mod_lt _ hp.pos⟩ : Fin p))
    (fun _ _ => Finset.mem_univ _)]
  refine Finset.sum_congr rfl fun c _ => ?_
  rw [Finset.filter_filter]
  refine Finset.sum_congr ?_ fun _ _ => rfl
  refine Finset.filter_congr fun a _ => ?_
  rw [mod_pow_succ_iff a.val d r c hp.pos hr, Fin.ext_iff]

/-! ### The invariant -/

omit [Fact p.Prime] [Fact q.Prime] in
/-- `Tiles` at a tree of depth `0`, in terms of `lay` and `size` -/
private theorem tiles_zero_iff (γ : ℕ → Bool → ℝ) (d : ℕ) (t : Tree p q 0) (ext : Fin q → ℝ) :
    Tiles γ d t ext ↔
      ∀ w, ext w + γ d true * (lay t w : ℝ) + γ d false * ((size t : ℝ) - (lay t w : ℝ)) = 1 := by
  cases t with
  | leaf f => simp only [Tiles, lay, size, Nat.cast_sum]

/-- **The invariant.** If the tiling identity holds at every point of the class `r` modulo `p^d`, with
`ext w` the contribution of the elements outside the class, then the subtree of the class tiles. -/
private theorem tiles_sub (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q))) (g : ZMod (p ^ n * q) → ℝ)
    (hg : ∀ x, g x = g ((x.val.gcd (p ^ n * q) : ℕ) : ZMod (p ^ n * q))) :
    ∀ (k d r : ℕ) (ext : Fin q → ℝ), d + k = n → r < p ^ d →
      (∀ (w : Fin q) (v : ZMod (p ^ n * q)), v.val % p ^ d = r → v.val % q = (w : ℕ) →
        ext w + ∑ a ∈ A.filter (fun a => a.val % p ^ d = r), g (v - a) = 1) →
      Tiles (stepOf g) d (sub A k d r) ext := by
  have hp : p.Prime := Fact.out
  intro k
  induction k with
  | zero =>
    intro d r ext hdk hr H
    rw [tiles_zero_iff]
    intro w
    obtain ⟨v, hv1, hv2⟩ := exists_point (n := n) hpq (by omega) hr w
    have hH := H w v hv1 hv2
    rw [sum_class_sub A (stepOf g d true) (stepOf g d false) g 0 d r hr v w ?_] at hH
    · linarith
    · intro a ha
      have ha' : a.val % p ^ d = r := (Finset.mem_filter.1 ha).2
      have h := g_sub hpq g hg (d := d) (by omega) v a (hv1.trans ha'.symm) (fun hlt => by omega)
      rw [hv2] at h
      exact h
  | succ k ih =>
    intro d r ext hdk hr H
    have hpd : 0 < p ^ d := Nat.pow_pos hp.pos
    have hlt : ∀ c' : Fin p, r + (c' : ℕ) * p ^ d < p ^ (d + 1) := by
      intro c'
      have hc' : (c' : ℕ) + 1 ≤ p := c'.2
      calc r + (c' : ℕ) * p ^ d < p ^ d + (c' : ℕ) * p ^ d := by omega
        _ = ((c' : ℕ) + 1) * p ^ d := by ring
        _ ≤ p * p ^ d := Nat.mul_le_mul_right _ hc'
        _ = p ^ (d + 1) := by ring
    show ∀ c : Fin p, Tiles (stepOf g) (d + 1) (sub A k (d + 1) (r + (c : ℕ) * p ^ d))
      (fun w => ext w + ∑ c' ∈ univ.erase c,
        (stepOf g d true * (lay (sub A k (d + 1) (r + (c' : ℕ) * p ^ d)) w : ℝ)
          + stepOf g d false * ((size (sub A k (d + 1) (r + (c' : ℕ) * p ^ d)) : ℝ)
            - (lay (sub A k (d + 1) (r + (c' : ℕ) * p ^ d)) w : ℝ))))
    intro c
    apply ih (d + 1) (r + (c : ℕ) * p ^ d) _ (by omega) (hlt c)
    intro w v hv1 hv2
    have hvd : v.val % p ^ d = r := mod_pow_of_succ hp.pos hr hv1
    have hH := H w v hvd hv2
    rw [sum_split A (fun a => g (v - a)) d r hr,
      ← Finset.add_sum_erase _ _ (Finset.mem_univ c)] at hH
    have herase : ∑ c' ∈ univ.erase c,
        ∑ a ∈ A.filter (fun a => a.val % p ^ (d + 1) = r + (c' : ℕ) * p ^ d), g (v - a)
        = ∑ c' ∈ univ.erase c,
          (stepOf g d true * (lay (sub A k (d + 1) (r + (c' : ℕ) * p ^ d)) w : ℝ)
            + stepOf g d false * ((size (sub A k (d + 1) (r + (c' : ℕ) * p ^ d)) : ℝ)
              - (lay (sub A k (d + 1) (r + (c' : ℕ) * p ^ d)) w : ℝ))) := by
      refine Finset.sum_congr rfl fun c' hc' => ?_
      have hne : c' ≠ c := (Finset.mem_erase.1 hc').1
      apply sum_class_sub A _ _ g k (d + 1) _ (hlt c') v w
      intro a ha
      have ha' : a.val % p ^ (d + 1) = r + (c' : ℕ) * p ^ d := (Finset.mem_filter.1 ha).2
      have had : a.val % p ^ d = r := mod_pow_of_succ hp.pos hr ha'
      have h := g_sub hpq g hg (d := d) (by omega) v a (hvd.trans had.symm) (fun _ => by
        rw [hv1, ha']
        intro e
        apply hne
        have e' : (c' : ℕ) * p ^ d = (c : ℕ) * p ^ d := by omega
        exact Fin.ext (Nat.eq_of_mul_eq_mul_right hpd e'))
      rw [hv2] at h
      exact h
    rw [herase] at hH
    linarith

/-! ### The theorem -/

theorem exists_stepTiling_tree (hpq : p ≠ q) (A : Finset (ZMod (p ^ n * q)))
    (f : ZMod (p ^ n * q) → ℝ) (h : Pqr.WeakTiling A f) :
    ∃ γ : ℕ → Bool → ℝ, StepTiling γ (treeOf A) := by
  have hg := Pqr.weakTiling_avg_units A f h
  refine ⟨stepOf (Pqr.avg f), fun d b => hg.1 _, ?_, ?_⟩
  · unfold stepOf
    rw [ite_eq_left rfl, ZMod.natCast_self]
    exact hg.2.1
  · apply tiles_sub hpq A (Pqr.avg f) (Pqr.avg_eq_gcd f) n 0 0 (fun _ => 0) (by omega) (by simp)
    intro w v _ _
    rw [zero_add, Finset.filter_true_of_mem (fun a _ => by simp [Nat.mod_one])]
    exact hg.2.2 v

end Pnq
