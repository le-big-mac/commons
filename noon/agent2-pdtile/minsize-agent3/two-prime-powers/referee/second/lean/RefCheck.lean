import Pnq.Upset
open Pnq.Upset

-- the three theorems and the lemmas the note names
#print axioms Pnq.Upset.structure_iff
#print axioms Pnq.Upset.lower_bound
#print axioms Pnq.Upset.least_size
#print axioms Pnq.Upset.Aux.rep_of_filtration
#print axioms Pnq.Upset.Aux.rep_all
#check @Pnq.Upset.Aux.rep_of_filtration
#check @Pnq.Upset.Aux.rep_all
#check @Pnq.Upset.Aux.exists_top
#check @Pnq.Upset.Aux.dd_eq_zero
#check @Pnq.Upset.Aux.split
#check @Pnq.Upset.Aux.hatW_eq_zero_of_periodic
#check @Pnq.Upset.Aux.chain
#check @Pnq.Upset.Aux.form_of_dvd
#print Pnq.maskW
#print Pnq.hatW
#print Pnq.Upset.Aux.per

-- the definition of corners evaluated on the worked example of S4 and on two others
#eval corners 36 ({12, 18, 36} : Finset ℕ)
#eval corners 36 (∅ : Finset ℕ)
#eval corners 36 ({2, 3, 4, 6, 9, 12, 18, 36} : Finset ℕ)
#eval ∑ c ∈ corners 100 ({4, 10, 20, 50, 100} : Finset ℕ), 100 / c

-- the hard direction with no hypothesis p ≠ q (so also for p = q), as the note says
example {p q n m : ℕ} [Fact p.Prime] [Fact q.Prime] (D : Finset ℕ) (hD : IsUpSet (p ^ n * q ^ m) D)
    (w : ZMod (p ^ n * q ^ m) → ℕ) (hz : ∀ ξ : ZMod (p ^ n * q ^ m), Pqr.ord ξ ∈ D → Pnq.hatW w ξ = 0) :
    Aux.Rep (p ^ n * q ^ m) D w := Aux.rep_all D hD w hz

-- the easy direction is F1 alone: a function periodic under a corner has no Fourier mass at an order in D
example {M : ℕ} [NeZero M] (D : Finset ℕ) (hD : IsUpSet M D) (c : ℕ) (hc : c ∈ corners M D) (g : ZMod M → ℕ)
    (hg : ∀ x, g (x + (c : ZMod M)) = g x) (ξ : ZMod M) (hξ : Pqr.ord ξ ∈ D) : Pnq.hatW g ξ = 0 :=
  Aux.hatW_eq_zero_of_periodic g _ ξ hg
    (fun h => Aux.corner_not_mem hc (hD.2 _ hξ c ((Pqr.Bridge.mul_natCast_eq_zero_iff ξ _).1 h) (Aux.corner_dvd hc)))
