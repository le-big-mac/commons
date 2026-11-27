import Pnq.EvenWhole

/-! Audit of the evening of 27 November (Corollary U): `BadAt e ε d` depends only on the exponents modulo `d`, so for
`d ∣ n` only on the exponents modulo `n`.  Proved here without any `sorry` statement.  Scratch file of the audit. -/

open Pnq Finset

namespace AuditUnion

/-- bad at `d` is the same for the exponents and for their remainders modulo `d` -/
theorem badAt_mod {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) (d : ℕ) :
    BadAt (fun k => e k % d) ε d ↔ BadAt e ε d := by
  unfold BadAt
  have key : Polynomial.cyclotomic d ℤ ∣ P e ε - P (fun k => e k % d) ε := by
    unfold P
    rw [← Finset.sum_sub_distrib]
    refine Finset.dvd_sum fun k _ => ?_
    rw [← mul_sub]
    refine Dvd.dvd.mul_left ?_ _
    have h1 : (Polynomial.X : Polynomial ℤ) ^ e k - Polynomial.X ^ (e k % d)
        = Polynomial.X ^ (e k % d) * ((Polynomial.X ^ d) ^ (e k / d) - 1) := by
      rw [mul_sub, mul_one, ← pow_mul, ← pow_add, Nat.mod_add_div]
    rw [h1]
    refine Dvd.dvd.mul_left ?_ _
    have h2 : (Polynomial.X ^ d - 1 : Polynomial ℤ) ∣ (Polynomial.X ^ d) ^ (e k / d) - 1 := by
      simpa using sub_dvd_pow_sub_pow (Polynomial.X ^ d : Polynomial ℤ) 1 (e k / d)
    exact (Polynomial.cyclotomic.dvd_X_pow_sub_one d ℤ).trans h2
  exact (dvd_iff_dvd_of_dvd_sub key).symm

/-- for `d ∣ n`: bad at `d` is the same for the exponents and for their remainders modulo `n` -/
theorem badAt_mod_of_dvd {ι : Type*} [Fintype ι] (e : ι → ℕ) (ε : ι → Bool) {d n : ℕ} (h : d ∣ n) :
    BadAt (fun k => e k % n) ε d ↔ BadAt e ε d := by
  rw [← badAt_mod e ε d, ← badAt_mod (fun k => e k % n) ε d]
  simp only [Nat.mod_mod_of_dvd _ h]

end AuditUnion

#print axioms AuditUnion.badAt_mod
#print axioms AuditUnion.badAt_mod_of_dvd
