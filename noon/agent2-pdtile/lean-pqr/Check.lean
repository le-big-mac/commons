import Pqr

/-! Run `lake env lean Check.lean` after `lake build`. Each line should print
`depends on axioms: [propext, Classical.choice, Quot.sound]` and nothing else. -/

-- Z_{pqr}
#print axioms Pqr.weak_tiling_tiles
#print axioms Pqr.weak_tiling_tiles_cyclic
#print axioms Pqr.weak_tiling_iff_tiling_cyclic
#print axioms Pqr.structured_of_bounds
#print axioms Pqr.bounds_of_stepTiling
#print axioms Pqr.exists_stepTiling
-- any cyclic group
#print axioms Pqr.weakTiling_iff_countingCert
#print axioms Pqr.zeroAt_of_hat_eq_zero
#print axioms Pqr.S_bound
#print axioms Pqr.C_bound
#print axioms Pqr.zeroAt_iff_cnt
#print axioms Pqr.zeroAt_prime_pow
#print axioms Pqr.zeroAt_prime_pow_mul
#print axioms Pqr.tiling_of_zeroAt
#print axioms Pqr.card_digitSet
#print axioms Pqr.zeroAt_digitSet
#print axioms Pqr.prod_minFac_dvd_card
#print axioms Pqr.tiling_of_T1_T2
#print axioms Pqr.T1_of_no_orphan
#print axioms Pqr.weak_tiling_tiles_prime_pow
#print axioms Pqr.zeroAt_iff_cyclotomic_dvd
#print axioms Pqr.tiling_of_T1_T2_digitSet
