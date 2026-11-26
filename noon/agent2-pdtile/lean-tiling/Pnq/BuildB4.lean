/-
Tools for `Pnq/BuildB.lean`, part 4: the vectors put on the strings of the shape part (the three "modes" of
section 6.2 of the proof on paper), and `Good` for data that use them.

Mode U (`a0 ∉ E`): digit `0` at level `a0` carries a unit vector, digit `1` its complement, no other digit.
Mode Q (`a0 ∈ E`): digit `0` carries `1 + e_a - e_b`, digit `1` carries `1 - e_a + e_b`, every other digit `1`.
Mode W (`a0 ∈ E`, `p ≥ 3`): as mode Q for the digits `0` and `1`; the other digits carry whole fibres.
-/
import Pnq.BuildB3

open Finset

namespace Pnq
namespace BuildB

variable {p q : ℕ}

/-! ### The vectors -/

theorem sum_ind (b : ℕ) (hb : b < q) : ∑ j : Fin q, (if j.val = b then 1 else 0) = 1 := by
  rw [Finset.sum_eq_single (⟨b, hb⟩ : Fin q)]
  · simp
  · intro j _ hj
    rw [ite_eq_right]
    intro h
    exact hj (Fin.ext h)
  · intro h
    exact absurd (Finset.mem_univ _) h

/-- the unit vector of layer `0` (`s = false`) or layer `1` (`s = true`) -/
def uv (s : Bool) (j : Fin q) : ℕ := if j.val = (if s then 1 else 0) then 1 else 0

/-- one element in every layer, a second one in layer `aa`, none in layer `bb` -/
def bump (aa bb : ℕ) (j : Fin q) : ℕ := if j.val = bb then 0 else if j.val = aa then 2 else 1

/-- `1 + e_0 - e_1` (`s = false`); for `s = true`: `1 + e_1 - e_0` if `q = 2`, and `1 + e_0 - e_2` if not -/
def wv (s : Bool) (j : Fin q) : ℕ :=
  if s then (if q = 2 then bump 1 0 j else bump 0 2 j) else bump 0 1 j

theorem sum_bump {aa bb : ℕ} (haa : aa < q) (hbb : bb < q) (hne : aa ≠ bb) :
    ∑ j : Fin q, bump aa bb j = q := by
  have h1 : ∀ j : Fin q, bump aa bb j + (if j.val = bb then 1 else 0)
      = 1 + (if j.val = aa then 1 else 0) := by
    intro j
    unfold bump
    split_ifs <;> omega
  have h2 := Finset.sum_congr (s₁ := Finset.univ) rfl (fun j _ => h1 j)
  rw [Finset.sum_add_distrib, Finset.sum_add_distrib, sum_ind bb hbb, sum_ind aa haa] at h2
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul, mul_one] at h2
  omega

/-- what the generic part needs of the two vectors of the digit `0` -/
structure BaseOK (q κ r0 : ℕ) (base : Bool → Fin q → ℕ) : Prop where
  le : ∀ s j, base s j ≤ κ
  tot : ∀ s, ∑ j, base s j = r0
  nc : ∀ a b e, Nat.Coprime (a + b) q → ¬ ∀ j j',
    a * base false j + b * base true j + e = a * base false j' + b * base true j' + e
  n2 : ∀ D W e, 1 ≤ W → ¬ ∀ j j',
    (D * base false j + W * base false j + e) + (D * base false j' + W * base true j' + e)
      = (D * base false j' + W * base false j' + e) + (D * base false j + W * base true j + e)

theorem coprime_double_two {a : ℕ} (h : Nat.Coprime (a + a) 2) : False := by
  have := Nat.Coprime.eq_one_of_dvd h.symm ⟨a, by ring⟩
  omega

theorem coprime_zero {q : ℕ} (hq : 2 ≤ q) (h : Nat.Coprime (0 + 0) q) : False := by
  have := (Nat.coprime_zero_left q).1 h
  omega

theorem baseOK_uv (hq : 2 ≤ q) : BaseOK q 1 1 (uv (q := q)) := by
  have u00 : uv false (⟨0, by omega⟩ : Fin q) = 1 := by simp [uv]
  have u01 : uv false (⟨1, by omega⟩ : Fin q) = 0 := by simp [uv]
  have u10 : uv true (⟨0, by omega⟩ : Fin q) = 0 := by simp [uv]
  have u11 : uv true (⟨1, by omega⟩ : Fin q) = 1 := by simp [uv]
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro s j
    unfold uv
    split_ifs <;> omega
  · intro s
    unfold uv
    exact sum_ind _ (by split_ifs <;> omega)
  · intro a b e hcop h
    have h01 := h ⟨0, by omega⟩ ⟨1, by omega⟩
    rw [u00, u01, u10, u11] at h01
    have hab : a = b := by omega
    subst hab
    by_cases hq2 : q = 2
    · subst hq2
      exact coprime_double_two hcop
    · have h02 := h ⟨0, by omega⟩ ⟨2, by omega⟩
      have u02 : uv false (⟨2, by omega⟩ : Fin q) = 0 := by simp [uv]
      have u12 : uv true (⟨2, by omega⟩ : Fin q) = 0 := by simp [uv]
      rw [u00, u10, u02, u12] at h02
      have ha : a = 0 := by omega
      subst ha
      exact coprime_zero hq hcop
  · intro D W e hW h
    have h01 := h ⟨0, by omega⟩ ⟨1, by omega⟩
    rw [u00, u01, u10, u11] at h01
    omega

theorem baseOK_wv (hq : 2 ≤ q) : BaseOK q 2 q (wv (q := q)) := by
  have w00 : wv false (⟨0, by omega⟩ : Fin q) = 2 := by simp [wv, bump]
  have w01 : wv false (⟨1, by omega⟩ : Fin q) = 0 := by simp [wv, bump]
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro s j
    unfold wv bump
    split_ifs <;> omega
  · intro s
    cases s
    · simp only [wv, Bool.false_eq_true, ↓reduceIte]
      exact sum_bump (by omega) (by omega) (by omega)
    · by_cases hq2 : q = 2
      · simp only [wv, ↓reduceIte, hq2]
        subst hq2
        exact sum_bump (by omega) (by omega) (by omega)
      · simp only [wv, ↓reduceIte, hq2]
        exact sum_bump (by omega) (by omega) (by omega)
  · intro a b e hcop h
    have h01 := h ⟨0, by omega⟩ ⟨1, by omega⟩
    by_cases hq2 : q = 2
    · subst hq2
      have w10 : wv true (⟨0, by omega⟩ : Fin 2) = 0 := by simp [wv, bump]
      have w11 : wv true (⟨1, by omega⟩ : Fin 2) = 2 := by simp [wv, bump]
      rw [w00, w01, w10, w11] at h01
      have hab : a = b := by omega
      subst hab
      exact coprime_double_two hcop
    · have w10 : wv true (⟨0, by omega⟩ : Fin q) = 2 := by simp [wv, bump, hq2]
      have w11 : wv true (⟨1, by omega⟩ : Fin q) = 1 := by simp [wv, bump, hq2]
      rw [w00, w01, w10, w11] at h01
      have ha : a = 0 := by omega
      have hb : b = 0 := by omega
      subst ha hb
      exact coprime_zero hq hcop
  · intro D W e hW h
    have h01 := h ⟨0, by omega⟩ ⟨1, by omega⟩
    by_cases hq2 : q = 2
    · subst hq2
      have w10 : wv true (⟨0, by omega⟩ : Fin 2) = 0 := by simp [wv, bump]
      have w11 : wv true (⟨1, by omega⟩ : Fin 2) = 2 := by simp [wv, bump]
      rw [w00, w01, w10, w11] at h01
      omega
    · have w10 : wv true (⟨0, by omega⟩ : Fin q) = 2 := by simp [wv, bump, hq2]
      have w11 : wv true (⟨1, by omega⟩ : Fin q) = 1 := by simp [wv, bump, hq2]
      rw [w00, w01, w10, w11] at h01
      omega

/-! ### The vectors of all digits, from those of the digit `0` -/

/-- digit `0`: `base s`; digit `1`: `κ - base s`; every other digit: the constant vector `rest` -/
def vecM (κ rest : ℕ) (base : Bool → Fin q → ℕ) (x : Fin p) (s : Bool) (j : Fin q) : ℕ :=
  if x.val = 0 then base s j else if x.val = 1 then κ - base s j else rest

/-- the totals -/
def rM (r0 r1 rr : ℕ) (x : Fin p) : ℕ := if x.val = 0 then r0 else if x.val = 1 then r1 else rr

theorem vecM_tot {κ rest r0 r1 rr : ℕ} {base : Bool → Fin q → ℕ} (hle : ∀ s j, base s j ≤ κ)
    (htot : ∀ s, ∑ j, base s j = r0) (hr1 : r1 + r0 = q * κ) (hrr : rr = q * rest)
    (x : Fin p) (s : Bool) : ∑ j, vecM κ rest base x s j = rM r0 r1 rr x := by
  unfold vecM rM
  by_cases h0 : x.val = 0
  · simp only [ite_eq_left h0]
    exact htot s
  by_cases h1 : x.val = 1
  · simp only [ite_eq_right h0, ite_eq_left h1]
    have h : ∑ j, (κ - base s j) + ∑ j, base s j = q * κ := by
      rw [← Finset.sum_add_distrib, Finset.sum_congr rfl (fun j _ => Nat.sub_add_cancel (hle s j))]
      simp
    rw [htot s] at h
    omega
  · simp only [ite_eq_right h0, ite_eq_right h1]
    simp [hrr]

theorem vecM_col (hp : 2 ≤ p) {κ rest : ℕ} {base : Bool → Fin q → ℕ} (hle : ∀ s j, base s j ≤ κ)
    (s : Bool) (j : Fin q) : ∑ x : Fin p, vecM κ rest base x s j = κ + (p - 2) * rest := by
  unfold vecM
  rw [sum_ite_zero_one hp, Nat.add_sub_of_le (hle s j)]

theorem vecM_n1 {κ rest : ℕ} {base : Bool → Fin q → ℕ} (hle : ∀ s j, base s j ≤ κ)
    (hnc : ∀ a b e, Nat.Coprime (a + b) q → ¬ ∀ j j',
      a * base false j + b * base true j + e = a * base false j' + b * base true j' + e)
    (x y : Fin p) (hx : x.val = 0) (hy : y.val = 1) (a b e e' : ℕ) (hcop : Nat.Coprime (a + b) q) :
    ¬ ∀ j j', (a * vecM κ rest base x false j + b * vecM κ rest base x true j + e)
        + (a * vecM κ rest base y false j' + b * vecM κ rest base y true j' + e')
      = (a * vecM κ rest base x false j' + b * vecM κ rest base x true j' + e)
        + (a * vecM κ rest base y false j + b * vecM κ rest base y true j + e') := by
  intro h
  apply hnc a b 0 hcop
  intro j j'
  have hjj := h j j'
  have hx' : ∀ s jj, vecM κ rest base x s jj = base s jj := by
    intro s jj
    unfold vecM
    rw [ite_eq_left hx]
  have hy' : ∀ s jj, vecM κ rest base y s jj = κ - base s jj := by
    intro s jj
    unfold vecM
    rw [ite_eq_right (by omega), ite_eq_left hy]
  simp only [hx', hy'] at hjj
  have f : ∀ (t : ℕ) s jj, t * (κ - base s jj) + t * base s jj = t * κ := by
    intro t s jj
    rw [← Nat.mul_add, Nat.sub_add_cancel (hle s jj)]
  have f1 := f a false j
  have f2 := f a false j'
  have f3 := f b true j
  have f4 := f b true j'
  omega

theorem vecOK_of_base {C : Cfg p q} {κ rest r0 r1 rr : ℕ} {base : Bool → Fin q → ℕ} (hp : 2 ≤ p)
    (hvec : C.vec = vecM κ rest base) (hr : C.r = rM r0 r1 rr) (B : BaseOK q κ r0 base)
    (hr1 : r1 + r0 = q * κ) (hrr : rr = q * rest) (hr0 : 1 ≤ r0) : VecOK C where
  hV1 := by
    intro i s
    rw [hvec, hr]
    exact vecM_tot B.le B.tot hr1 hrr i s
  hcol := by
    intro s j j'
    rw [hvec, vecM_col hp B.le, vecM_col hp B.le]
  hr0 := by
    intro x hx
    rw [hr]
    unfold rM
    rw [ite_eq_left hx]
    exact hr0
  hNC := by
    intro x hx a b e hcop h
    apply B.nc a b e hcop
    intro j j'
    have hjj := h j j'
    rw [hvec] at hjj
    simp only [vecM, ite_eq_left hx] at hjj
    exact hjj
  hN2 := by
    intro x hx D W e hW h
    apply B.n2 D W e hW
    intro j j'
    have hjj := h j j'
    rw [hvec] at hjj
    simp only [vecM, ite_eq_left hx] at hjj
    exact hjj
  hN1 := by
    intro x y hx hy a b e e' hcop
    rw [hvec]
    exact vecM_n1 B.le B.nc x y hx hy a b e e' hcop

/-! ### The three modes -/

theorem two_add_pred2_mul (hp : 2 ≤ p) (X : ℕ) : X + X + (p - 2) * X = p * X := by
  have h : p - 2 + 2 = p := by omega
  calc X + X + (p - 2) * X = (p - 2 + 2) * X := by ring
    _ = p * X := by rw [h]

/-- mode U: `a0 ∉ E`; a host level, if there is one, lies before `a0` -/
theorem good_U {C : Cfg p q} {n c0 : ℕ} (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q)
    (hvec : C.vec = vecM 1 0 uv) (hr : C.r = rM 1 (q - 1) 0) (hex : ∀ x, C.ex x = 0)
    (ha1 : 1 ≤ C.a0) (han : C.a0 ≤ n) (hna : C.a0 ∉ C.Fs)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < C.a0 → ℓ ∈ C.Fs) (haE : C.a0 ∉ C.Es)
    (host : C.hb = 0 ∨ (C.hb ∈ C.Es ∧ C.hb < C.a0 ∧
      ∀ k, C.hb + k = n → pw p C.U k C.hb = C.M * pw p C.Es k C.hb))
    (hU2 : p = 2 → ∀ k, C.a0 + k = n →
      pw p C.U k C.a0 + q * (c0 * pw p C.Es k C.a0) ≠ (q - 1) * pw p C.U k C.a0)
    (hG : ∀ g, g ∈ C.U → g ∉ C.Es → 1 ≤ c0 ∨ (C.hb ≠ 0 ∧ C.hb < g ∧ 1 ≤ C.M)) :
    Good C n c0 :=
  { toVecOK := vecOK_of_base hp hvec hr (baseOK_uv hq) (by omega) (by simp) (le_refl 1)
    hp := hp
    hq := hq
    hpq := hpq
    ha1 := ha1
    han := han
    hna := hna
    hlow := hlow
    host := by
      rcases host with h | ⟨h1, h2, h3⟩
      · exact Or.inl h
      · exact Or.inr ⟨h1, by omega, h3, fun h => by omega⟩
    hex0 := fun x _ => hex x
    hmidS := by
      intro k d h1 h2
      have hnU : d + 1 ∉ C.U := by
        rw [C.mem_U]
        rintro (h | ⟨_, h⟩)
        · exact haE (h1 ▸ h)
        · omega
      have term : ∀ x : Fin p, C.r x * pw p C.U k (d + 1) + q * (C.ex x * pw p C.Es k (d + 1))
          = if x.val = 0 then pw p C.U k (d + 1)
            else if x.val = 1 then (q - 1) * pw p C.U k (d + 1) else 0 := by
        intro x
        rw [hr, hex]
        unfold rM
        split_ifs <;> simp
      rw [pw_succ_not k hnU, Finset.sum_congr rfl (fun x _ => term x), sum_ite_zero_one hp, mul_zero,
        add_zero, add_pred_mul (by omega)]
    hmidE := fun h => absurd h haE
    hmidF := by
      intro _ k hk hall
      have r0 : C.r (⟨0, by omega⟩ : Fin p) = 1 := by rw [hr]; simp [rM]
      have r1 : C.r (⟨1, by omega⟩ : Fin p) = q - 1 := by rw [hr]; simp [rM]
      have h01 := hall ⟨0, by omega⟩ ⟨1, by omega⟩
      rw [r0, r1, hex, hex] at h01
      simp only [↓reduceIte, one_ne_zero, add_zero, zero_mul, mul_zero, one_mul] at h01
      by_cases hp2 : p = 2
      · exact hU2 hp2 k hk h01
      · have r2 : C.r (⟨2, by omega⟩ : Fin p) = 0 := by rw [hr]; simp [rM]
        have h02 := hall ⟨0, by omega⟩ ⟨2, by omega⟩
        rw [r0, r2, hex, hex] at h02
        simp only [↓reduceIte, OfNat.ofNat_ne_zero, add_zero, zero_mul, mul_zero, one_mul] at h02
        have := pw_pos (p := p) (by omega) C.U k C.a0
        omega
    hG := by
      intro g h1 h2
      rcases hG g h1 h2 with h | h
      · exact Or.inl h
      · exact Or.inr (Or.inl h) }

/-- mode Q: `a0 ∈ E` -/
theorem good_Q {C : Cfg p q} {n c0 : ℕ} (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q)
    (hvec : C.vec = vecM 2 1 wv) (hr : C.r = rM q q q) (hex : ∀ x, C.ex x = 0)
    (ha1 : 1 ≤ C.a0) (han : C.a0 ≤ n) (hna : C.a0 ∉ C.Fs)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < C.a0 → ℓ ∈ C.Fs) (haE : C.a0 ∈ C.Es)
    (host : C.hb = 0 ∨ (C.hb ∈ C.Es ∧ C.hb ≠ C.a0 ∧
      (∀ k, C.hb + k = n → pw p C.U k C.hb = C.M * pw p C.Es k C.hb) ∧
      (C.a0 < C.hb → C.hb ∉ C.Fs)))
    (hG : ∀ g, g ∈ C.U → g ∉ C.Es → 1 ≤ c0 ∨ (C.hb ≠ 0 ∧ C.hb < g ∧ 1 ≤ C.M)) :
    Good C n c0 := by
  have hrq : ∀ x, C.r x = q := by
    intro x
    rw [hr]
    unfold rM
    split_ifs <;> rfl
  exact
  { toVecOK := vecOK_of_base hp hvec hr (baseOK_wv hq) (by omega) (by simp) (by omega)
    hp := hp
    hq := hq
    hpq := hpq
    ha1 := ha1
    han := han
    hna := hna
    hlow := hlow
    host := by
      rcases host with h | ⟨h1, h2, h3, h4⟩
      · exact Or.inl h
      · exact Or.inr ⟨h1, h2, h3, fun h => ⟨h4 h, hrq⟩⟩
    hex0 := fun x _ => hex x
    hmidS := by
      intro k d h1 h2
      have hU : d + 1 ∈ C.U := (C.mem_U _).2 (Or.inl (by rw [h1]; exact haE))
      rw [pw_succ_mem k hU]
      simp only [hrq, hex, zero_mul, mul_zero, add_zero, Finset.sum_const, Finset.card_univ,
        Fintype.card_fin, smul_eq_mul]
      ring
    hmidE := by
      intro _ k _ x x'
      rw [hrq, hrq, hex, hex]
    hmidF := fun h => absurd haE h
    hG := by
      intro g h1 h2
      rcases hG g h1 h2 with h | h
      · exact Or.inl h
      · exact Or.inr (Or.inl h) }

/-- mode W: `a0 ∈ E`, `p ≥ 3`, no host level; the digits `≥ 2` at level `a0` carry whole fibres -/
theorem good_W {C : Cfg p q} {n c0 : ℕ} (hp : 3 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q)
    (hvec : C.vec = vecM 2 0 wv) (hr : C.r = rM q q 0)
    (hex : ∀ x, C.ex x = if 2 ≤ x.val then C.M else 0) (hb0 : C.hb = 0)
    (ha1 : 1 ≤ C.a0) (han : C.a0 ≤ n) (hna : C.a0 ∉ C.Fs)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < C.a0 → ℓ ∈ C.Fs) (haE : C.a0 ∈ C.Es)
    (hM : ∀ k, C.a0 + k = n → pw p C.U k C.a0 = C.M * pw p C.Es k C.a0) (hM1 : 1 ≤ C.M) :
    Good C n c0 := by
  have term : ∀ (P PE : ℕ) (x : Fin p), C.r x * P + q * (C.ex x * PE)
      = if x.val = 0 then q * P else if x.val = 1 then q * P else q * (C.M * PE) := by
    intro P PE x
    rw [hr, hex]
    unfold rM
    split_ifs <;> omega
  exact
  { toVecOK := vecOK_of_base (by omega) hvec hr (baseOK_wv hq) (by omega) (by simp) (by omega)
    hp := by omega
    hq := hq
    hpq := hpq
    ha1 := ha1
    han := han
    hna := hna
    hlow := hlow
    host := Or.inl hb0
    hex0 := by
      intro x hx
      rw [hex, ite_eq_right (by omega)]
    hmidS := by
      intro k d h1 h2
      have hU : d + 1 ∈ C.U := (C.mem_U _).2 (Or.inl (by rw [h1]; exact haE))
      have hM' := hM k (by omega)
      rw [← h1] at hM'
      rw [pw_succ_mem k hU, Finset.sum_congr rfl (fun x _ => term _ _ x),
        sum_ite_zero_one (by omega), hM', two_add_pred2_mul (by omega)]
      ring
    hmidE := by
      intro _ k hk x x'
      rw [term, term, hM k hk]
      split_ifs <;> rfl
    hmidF := fun h => absurd haE h
    hG := fun g _ _ => Or.inr (Or.inr ⟨⟨2, by omega⟩, by rw [hex]; simpa using hM1⟩) }

end BuildB
end Pnq
