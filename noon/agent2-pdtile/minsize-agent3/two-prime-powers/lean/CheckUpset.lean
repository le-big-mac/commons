import Pnq.Upset
open Pnq.Upset
-- the corners of some up-sets of the divisors of 36 and of 100, and the sums of M / c
#eval (corners 36 {12, 18, 36}, ∑ c ∈ corners 36 {12, 18, 36}, 36 / c)
#eval (corners 36 {36}, ∑ c ∈ corners 36 {36}, 36 / c)
#eval (corners 36 {6, 12, 18, 36}, ∑ c ∈ corners 36 {6, 12, 18, 36}, 36 / c)
#eval (corners 36 ∅, ∑ c ∈ corners 36 (∅ : Finset ℕ), 36 / c)
#eval (corners 36 {2, 3, 4, 6, 9, 12, 18, 36}, ∑ c ∈ corners 36 {2, 3, 4, 6, 9, 12, 18, 36}, 36 / c)
#eval (corners 100 {20, 50, 100}, ∑ c ∈ corners 100 {20, 50, 100}, 100 / c)
