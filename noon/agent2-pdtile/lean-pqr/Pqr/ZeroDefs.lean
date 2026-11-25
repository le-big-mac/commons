/-
The two bounds for weak tiles of an arbitrary cyclic group `ZMod M`, and the bridge from Fourier zeros to
residue-class counts.  These are (S) and (C) of `pnq-agent3.md`, (I2), with the Delsarte parameter removed:

* `S_bound`: a weak tile has at most as many elements as any nonempty set with at least its Fourier zeros;
* `C_bound`: if no two distinct elements of `B` differ by an element whose order is a Fourier zero of the weak
  tile `A`, then `|A| · |B| ≤ M`;
* `zeroAt_iff_cnt`: "the indicator of `A` has no Fourier mass at the frequencies of order `d`" as a linear
  condition on the residue-class counts `cnt A j v`.
-/
import Pqr.Counting

open Finset

namespace Pqr

variable {M : ℕ} [NeZero M]

/-- the Fourier coefficient of the indicator of `A` at the frequency `ξ` -/
noncomputable def hat (A : Finset (ZMod M)) (ξ : ZMod M) : ℂ := ∑ a ∈ A, ZMod.stdAddChar (ξ * a)

/-- the order of `ξ` as an element of the additive group `ZMod M` -/
def ord (ξ : ZMod M) : ℕ := M / ξ.val.gcd M

/-- The indicator of `A` has no Fourier mass at the frequencies of order `d`.  (For a set of residues this
says that the cyclotomic polynomial `Φ_d` divides its mask polynomial.) -/
def ZeroAt (A : Finset (ZMod M)) (d : ℕ) : Prop := ∀ ξ : ZMod M, ord ξ = d → hat A ξ = 0

end Pqr
