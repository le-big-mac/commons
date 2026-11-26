/-
Tools for `Pnq/BuildB.lean`, part 5: the counting of levels (the sets of the rule against the powers `pw`),
and the trees of the constructions for a pattern, with their sizes written with `pw`.
-/
import Pnq.BuildB4

open Finset

namespace Pnq
namespace BuildB

variable {p q : ℕ}

/-- the levels at which the shape part branches: `Es`, and the levels of `Fs` beyond `a0` -/
def UU (Es Fs : Finset ℕ) (a0 : ℕ) : Finset ℕ := Es ∪ Fs.filter (fun a => a0 < a)

theorem mem_UU {Es Fs : Finset ℕ} {a0 a : ℕ} : a ∈ UU Es Fs a0 ↔ a ∈ Es ∨ (a ∈ Fs ∧ a0 < a) := by
  simp [UU]

theorem mem_gOf {Es Fs : Finset ℕ} {a0 g : ℕ} : g ∈ gOf Es Fs a0 ↔ g ∈ Fs ∧ g ∉ Es ∧ a0 < g := by
  simp [gOf, and_assoc]

theorem mem_gOf_of_UU {Es Fs : Finset ℕ} {a0 g : ℕ} (h : g ∈ UU Es Fs a0) (hE : g ∉ Es) :
    g ∈ gOf Es Fs a0 := by
  rcases mem_UU.1 h with h | h
  · exact absurd h hE
  · exact mem_gOf.2 ⟨h.1, hE, h.2⟩

theorem pw_mul {S T V : Finset ℕ} (hV : ∀ a, a ∈ V ↔ a ∈ S ∨ a ∈ T) (hd : ∀ a, a ∈ S → a ∉ T) :
    ∀ k d, pw p V k d = pw p S k d * pw p T k d
  | 0, _ => by simp [pw]
  | k + 1, d => by
      simp only [pw]
      rw [pw_mul hV hd k (d + 1)]
      by_cases hS : d + 1 ∈ S
      · have hT := hd _ hS
        have hV' := (hV _).2 (Or.inl hS)
        rw [ite_eq_left hV', ite_eq_left hS, ite_eq_right hT]
        ring
      · by_cases hT : d + 1 ∈ T
        · have hV' := (hV _).2 (Or.inr hT)
          rw [ite_eq_left hV', ite_eq_right hS, ite_eq_left hT]
          ring
        · have hV' : d + 1 ∉ V := by
            intro h
            rcases (hV _).1 h with h | h
            · exact hS h
            · exact hT h
          rw [ite_eq_right hV', ite_eq_right hS, ite_eq_right hT]
          ring

/-- below a level `L` that lies before all levels of `gOf`, the shape part has `p ^ |gOf|` times as many
strings as there are strings that are `0` outside `Es` -/
theorem pw_UU {n : ℕ} {Es Fs : Finset ℕ} {a0 : ℕ} (hF : Fs ⊆ Finset.Icc 1 n) (L k : ℕ)
    (hLk : L + k = n) (hL : ∀ g ∈ gOf Es Fs a0, L < g) :
    pw p (UU Es Fs a0) k L = p ^ (gOf Es Fs a0).card * pw p Es k L := by
  have h1 : pw p (UU Es Fs a0) k L = pw p Es k L * pw p (gOf Es Fs a0) k L :=
    pw_mul (fun a => by rw [mem_UU, mem_gOf]; tauto) (fun a ha h => (mem_gOf.1 h).2.1 ha) k L
  have h2 : pw p (gOf Es Fs a0) k L = p ^ (gOf Es Fs a0).card := by
    rw [pw_eq]
    congr 2
    apply Finset.filter_true_of_mem
    intro g hg
    have := (Finset.mem_Icc.1 (hF (mem_gOf.1 hg).1)).2
    exact ⟨hL g hg, by omega⟩
  rw [h1, h2]
  ring

/-- the size of the tree of a construction is the value of the rule -/
theorem size_eq {n : ℕ} {Es Fs : Finset ℕ} {a0 : ℕ} (hE : Es ⊆ Finset.Icc 1 n)
    (hF : Fs ⊆ Finset.Icc 1 n) (c0 : ℕ) (hx : xOf p Es Fs a0 = c0) :
    q * pw p (UU Es Fs a0) n 0 + q * (c0 * pw p Es n 0) = minB p q Es Fs a0 := by
  have h1 := pw_UU (p := p) (Es := Es) (a0 := a0) hF 0 n (by omega) (fun g hg => by
    have := Finset.mem_Icc.1 (hF (mem_gOf.1 hg).1)
    omega)
  rw [h1, pw_root hE]
  unfold minB
  rw [hx]
  ring

/-! ### The two arithmetic facts for level `a0` when `p = 2` and `a0 ∉ E` -/

theorem odd_of_coprime_two (hpq : Nat.Coprime 2 q) : q % 2 = 1 := by
  by_contra hc
  have hd : 2 ∣ q := by omega
  have := Nat.Coprime.eq_one_of_dvd hpq hd
  omega

theorem mid_zero (hq : 2 ≤ q) (hpq : Nat.Coprime 2 q) {P PE : ℕ} (hP : 0 < P) :
    P + q * (0 * PE) ≠ (q - 1) * P := by
  have hodd := odd_of_coprime_two hpq
  have h2 : 2 * P ≤ (q - 1) * P := Nat.mul_le_mul_right _ (by omega)
  simp only [zero_mul, mul_zero, add_zero]
  omega

theorem mid_one (hpq : Nat.Coprime 2 q) {T PE : ℕ} (hPE : 0 < PE) :
    2 * T * PE + q * (1 * PE) ≠ (q - 1) * (2 * T * PE) := by
  have hodd := odd_of_coprime_two hpq
  intro h
  have h' : (2 * T + q) * PE = (2 * ((q - 1) * T)) * PE := by
    calc (2 * T + q) * PE = 2 * T * PE + q * (1 * PE) := by ring
      _ = (q - 1) * (2 * T * PE) := h
      _ = (2 * ((q - 1) * T)) * PE := by ring
  have h'' := Nat.eq_of_mul_eq_mul_right hPE h'
  omega

/-! ### The trees -/

/-- the construction in mode Q (if `a0 ∈ Es`) or U (if not), with a host level `hb` (or none: `hb = 0`)
and superposed fibres of multiplicity `c0` -/
theorem exists_mode0 (hp : 2 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} {Es Fs : Finset ℕ}
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) {a0 : ℕ} (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) (hb M c0 : ℕ)
    (host : hb = 0 ∨ (hb ∈ Es ∧ hb ≠ a0 ∧
      (∀ k, hb + k = n → pw p (UU Es Fs a0) k hb = M * pw p Es k hb) ∧
      (a0 < hb → hb ∉ Fs ∧ a0 ∈ Es)))
    (hU2 : a0 ∉ Es → p = 2 → ∀ k, a0 + k = n →
      pw p (UU Es Fs a0) k a0 + q * (c0 * pw p Es k a0) ≠ (q - 1) * pw p (UU Es Fs a0) k a0)
    (hG : ∀ g, g ∈ UU Es Fs a0 → g ∉ Es → 1 ≤ c0 ∨ (hb ≠ 0 ∧ hb < g ∧ 1 ≤ M)) :
    ∃ t : Tree p q n, F t 0 ∧ eSet t = Es ∧ fSet t = Fs ∧
      size t = q * pw p (UU Es Fs a0) n 0 + q * (c0 * pw p Es n 0) := by
  by_cases haE : a0 ∈ Es
  · have G : Good (⟨Es, Fs, a0, hb, M, vecM 2 1 wv, fun _ => 0, rM q q q⟩ : Cfg p q) n c0 :=
      good_Q hp hq hpq rfl rfl (fun _ => rfl) ha1 han hna hlow haE
        (by
          rcases host with h | ⟨h1, h2, h3, h4⟩
          · exact Or.inl h
          · exact Or.inr ⟨h1, h2, h3, fun h => (h4 h).1⟩) hG
    exact ⟨_, pattern_bld G hE hF ⟨0, by omega⟩ ⟨1, by omega⟩ rfl rfl⟩
  · have host' : hb = 0 ∨ (hb ∈ Es ∧ hb < a0 ∧
        ∀ k, hb + k = n → pw p (UU Es Fs a0) k hb = M * pw p Es k hb) := by
      rcases host with h | ⟨h1, h2, h3, h4⟩
      · exact Or.inl h
      · refine Or.inr ⟨h1, ?_, h3⟩
        by_contra hc
        exact haE (h4 (by omega)).2
    have G : Good (⟨Es, Fs, a0, hb, M, vecM 1 0 uv, fun _ => 0, rM 1 (q - 1) 0⟩ : Cfg p q) n c0 :=
      good_U hp hq hpq rfl rfl (fun _ => rfl) ha1 han hna hlow haE host' (hU2 haE) hG
    exact ⟨_, pattern_bld G hE hF ⟨0, by omega⟩ ⟨1, by omega⟩ rfl rfl⟩

/-- the construction in mode W (`a0 ∈ Es`, `p ≥ 3`): whole fibres of multiplicity `M` on the digits `≥ 2` at
level `a0` -/
theorem exists_modeW (hp : 3 ≤ p) (hq : 2 ≤ q) (hpq : Nat.Coprime p q) {n : ℕ} {Es Fs : Finset ℕ}
    (hE : Es ⊆ Finset.Icc 1 n) (hF : Fs ⊆ Finset.Icc 1 n) {a0 : ℕ} (ha1 : 1 ≤ a0) (han : a0 ≤ n)
    (hlow : ∀ ℓ, 1 ≤ ℓ → ℓ < a0 → ℓ ∈ Fs) (hna : a0 ∉ Fs) (haE : a0 ∈ Es) (M : ℕ) (hM1 : 1 ≤ M)
    (hM : ∀ k, a0 + k = n → pw p (UU Es Fs a0) k a0 = M * pw p Es k a0) :
    ∃ t : Tree p q n, F t 0 ∧ eSet t = Es ∧ fSet t = Fs ∧
      size t = q * pw p (UU Es Fs a0) n 0 + q * (0 * pw p Es n 0) := by
  have G : Good (⟨Es, Fs, a0, 0, M, vecM 2 0 wv, fun x => if 2 ≤ x.val then M else 0, rM q q 0⟩ :
      Cfg p q) n 0 :=
    good_W hp hq hpq rfl rfl (fun _ => rfl) rfl ha1 han hna hlow haE hM hM1
  exact ⟨_, pattern_bld G hE hF ⟨0, by omega⟩ ⟨1, by omega⟩ rfl rfl⟩

end BuildB
end Pnq
