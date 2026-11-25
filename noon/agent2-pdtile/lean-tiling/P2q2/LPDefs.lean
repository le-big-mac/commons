/-
The nine-variable linear programme for step functions on `ZMod (p^2 * q^2)`, in Möbius coordinates.

A step function is `x ↦ ∑_{d ∣ gcd(x, M)} μ d`; `mij` stands for `μ (p^i * q^j)`.
* `gab` is the value of the step function on the class of `p^a * q^b` (a partial sum of the `mij`);
* `Llm p q` is its Fourier coefficient at the frequencies of order `p^l * q^m`
  (`∑_{i ≥ l, j ≥ m} mij * p^(2-i) * q^(2-j)`); `L00` is the total mass.
Only definitions here, so that the generated certificate files and the hand-written files can both import it.
-/
import Mathlib

namespace P2q2

/-- nine real numbers `mij = μ (p^i * q^j)` -/
structure Nine where
  (m00 m01 m02 m10 m11 m12 m20 m21 m22 : ℝ)

namespace Nine

def g00 (x : Nine) : ℝ := x.m00
def g01 (x : Nine) : ℝ := x.m00 + x.m01
def g02 (x : Nine) : ℝ := x.m00 + x.m01 + x.m02
def g10 (x : Nine) : ℝ := x.m00 + x.m10
def g11 (x : Nine) : ℝ := x.m00 + x.m01 + x.m10 + x.m11
def g12 (x : Nine) : ℝ := x.m00 + x.m01 + x.m02 + x.m10 + x.m11 + x.m12
def g20 (x : Nine) : ℝ := x.m00 + x.m10 + x.m20
def g21 (x : Nine) : ℝ := x.m00 + x.m01 + x.m10 + x.m11 + x.m20 + x.m21
def g22 (x : Nine) : ℝ := x.m00 + x.m01 + x.m02 + x.m10 + x.m11 + x.m12 + x.m20 + x.m21 + x.m22

def L00 (p q : ℝ) (x : Nine) : ℝ :=
  p^2*q^2*x.m00 + p^2*q*x.m01 + p^2*x.m02 + p*q^2*x.m10 + p*q*x.m11 + p*x.m12 + q^2*x.m20 + q*x.m21 + x.m22
def L01 (p q : ℝ) (x : Nine) : ℝ := p^2*q*x.m01 + p^2*x.m02 + p*q*x.m11 + p*x.m12 + q*x.m21 + x.m22
def L02 (p _q : ℝ) (x : Nine) : ℝ := p^2*x.m02 + p*x.m12 + x.m22
def L10 (p q : ℝ) (x : Nine) : ℝ := p*q^2*x.m10 + p*q*x.m11 + p*x.m12 + q^2*x.m20 + q*x.m21 + x.m22
def L11 (p q : ℝ) (x : Nine) : ℝ := p*q*x.m11 + p*x.m12 + q*x.m21 + x.m22
def L12 (p _q : ℝ) (x : Nine) : ℝ := p*x.m12 + x.m22
def L20 (_p q : ℝ) (x : Nine) : ℝ := q^2*x.m20 + q*x.m21 + x.m22
def L21 (_p q : ℝ) (x : Nine) : ℝ := q*x.m21 + x.m22
def L22 (_p _q : ℝ) (x : Nine) : ℝ := x.m22

/-- the eight sign conditions and the normalisation -/
def Admissible (x : Nine) : Prop :=
  0 ≤ x.g00 ∧ 0 ≤ x.g01 ∧ 0 ≤ x.g02 ∧ 0 ≤ x.g10 ∧ 0 ≤ x.g11 ∧ 0 ≤ x.g12 ∧ 0 ≤ x.g20 ∧ 0 ≤ x.g21 ∧ x.g22 = 1

/-- the Fourier conditions for the zero pattern `z` (`zlm` says that `p^l * q^m` is a zero of the set) -/
def Vanishing (p q : ℝ) (x : Nine) (z01 z02 z10 z11 z12 z20 z21 z22 : Prop) : Prop :=
  (¬ z01 → x.L01 p q = 0) ∧ (¬ z02 → x.L02 p q = 0) ∧ (¬ z10 → x.L10 p q = 0) ∧ (¬ z11 → x.L11 p q = 0) ∧
  (¬ z12 → x.L12 p q = 0) ∧ (¬ z20 → x.L20 p q = 0) ∧ (¬ z21 → x.L21 p q = 0) ∧ (¬ z22 → x.L22 p q = 0)

end Nine

/-- the factor that a prime-power zero contributes to the number `k` dividing `|A|` -/
noncomputable def kfac (z : Prop) (p : ℝ) : ℝ := by classical exact if z then p else 1

theorem kfac_pos (z : Prop) (p : ℝ) (h : z) : kfac z p = p := by simp [kfac, h]
theorem kfac_neg (z : Prop) (p : ℝ) (h : ¬ z) : kfac z p = 1 := by simp [kfac, h]

/-- (T2) and "no orphan" for a zero pattern -/
def PatA (z01 z02 z10 z11 z12 z20 z21 z22 : Prop) : Prop :=
  (z11 → z10 ∨ z01) ∧ (z12 → z10 ∨ z02) ∧ (z21 → z20 ∨ z01) ∧ (z22 → z20 ∨ z02) ∧
  (z10 → z01 → z11) ∧ (z10 → z02 → z12) ∧ (z20 → z01 → z21) ∧ (z20 → z02 → z22)

/-- What the linear programme yields for a zero pattern, a size `n = |A|` and primes `p < q`:
* `¬ z10 ∧ ¬ z01`: neither prime is a zero (Lemma 2 applies);
* `PatA`: (T2) holds and there is no orphan;
* an admissible point with the right Fourier zeros, mass `≤ M / n`, vanishing outside `pZ` (`m0j = 0`) or outside `qZ` (`mi0 = 0`);
* `n = p * q` with `p`, `p²q²` zeros and `pq²` not a zero (excluded by the counting lemma);
* an admissible point with the right Fourier zeros and mass `≤ M / n` whose mass is a number for which `M / mass`
  is never an integer. -/
def Outcome (p q n : ℝ) (z01 z02 z10 z11 z12 z20 z21 z22 : Prop) : Prop :=
  (¬ z10 ∧ ¬ z01) ∨ PatA z01 z02 z10 z11 z12 z20 z21 z22 ∨
  (∃ x : Nine, x.Admissible ∧ x.Vanishing p q z01 z02 z10 z11 z12 z20 z21 z22 ∧ n * x.L00 p q ≤ p^2*q^2 ∧
      x.m00 = 0 ∧ x.m01 = 0 ∧ x.m02 = 0) ∨
  (∃ x : Nine, x.Admissible ∧ x.Vanishing p q z01 z02 z10 z11 z12 z20 z21 z22 ∧ n * x.L00 p q ≤ p^2*q^2 ∧
      x.m00 = 0 ∧ x.m10 = 0 ∧ x.m20 = 0) ∨
  (n = p * q ∧ z10 ∧ z22 ∧ ¬ z12) ∨
  (∃ x : Nine, x.Admissible ∧ x.Vanishing p q z01 z02 z10 z11 z12 z20 z21 z22 ∧ n * x.L00 p q ≤ p^2*q^2 ∧
      x.L00 p q * (p*q - 1) = p^2*(q-1) + q^2*(p-1))

end P2q2
