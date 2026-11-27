import Pnq.SignFinal
/-! Audit: the ten definitions and the fifteen statements as Lean has them.  First the default print, then with every
implicit argument shown. -/
#print Pnq.sg
#print Pnq.P
#print Pnq.BadAt
#print Pnq.badSet
#print Pnq.classSum
#print Pnq.live
#print Pnq.rank
#print Pnq.IsPivot
#print Pnq.μ
#print Pnq.lhsN1
#check @Pnq.classSum_eq_of_badAt
#check @Pnq.badAt_of_not_live
#check @Pnq.card_badSet_mul_two_pow_card_le
#check @Pnq.badAt_one_iff
#check @Pnq.card_badSet_one
#check @Pnq.rank_lt_card_image
#check @Pnq.exists_isPivot
#check @Pnq.card_badSet_mul_two_pow_rank_le
#check @Pnq.rank_lt_card
#check @Pnq.card_badSet_three_pow_mul_le
#check @Pnq.lhsN1_lt_one
#check @Pnq.exists_not_badAt
#check @Pnq.exists_signs_odd
#check @Pnq.exists_lift_two_all
#check @Pnq.sizes_eq_two_all
#check @Pnq.mem_badSet
#check @Pnq.live_iff
#check @Pnq.Lift.exists_signs
#check @Pnq.Lift.exists_lift_two
#check @Pnq.Lift.sizes_eq_two
#check @Pnq.Lift.TwoAux.exists_lift_two_aux
#print axioms Pnq.classSum_eq_of_badAt
#print axioms Pnq.badAt_of_not_live
#print axioms Pnq.card_badSet_mul_two_pow_card_le
#print axioms Pnq.badAt_one_iff
#print axioms Pnq.card_badSet_one
#print axioms Pnq.rank_lt_card_image
#print axioms Pnq.exists_isPivot
#print axioms Pnq.card_badSet_mul_two_pow_rank_le
#print axioms Pnq.rank_lt_card
#print axioms Pnq.card_badSet_three_pow_mul_le
#print axioms Pnq.lhsN1_lt_one
#print axioms Pnq.exists_not_badAt
#print axioms Pnq.exists_signs_odd
#print axioms Pnq.exists_lift_two_all
#print axioms Pnq.sizes_eq_two_all
#print axioms Pnq.mem_badSet
#print axioms Pnq.live_iff
#print axioms Pnq.Lift.exists_signs
#print axioms Pnq.Lift.TwoAux.exists_lift_two_aux
#print axioms Pnq.Lift.sum_reduce
#print axioms Pnq.Lift.cyclotomic_dvd_reduce_iff
set_option pp.explicit true
set_option pp.fullNames true
set_option pp.universes true
#print Pnq.sg
#print Pnq.P
#print Pnq.BadAt
#print Pnq.badSet
#print Pnq.classSum
#print Pnq.live
#print Pnq.rank
#print Pnq.IsPivot
#print Pnq.μ
#print Pnq.lhsN1
#check @Pnq.classSum_eq_of_badAt
#check @Pnq.badAt_of_not_live
#check @Pnq.card_badSet_mul_two_pow_card_le
#check @Pnq.badAt_one_iff
#check @Pnq.card_badSet_one
#check @Pnq.rank_lt_card_image
#check @Pnq.exists_isPivot
#check @Pnq.card_badSet_mul_two_pow_rank_le
#check @Pnq.rank_lt_card
#check @Pnq.card_badSet_three_pow_mul_le
#check @Pnq.lhsN1_lt_one
#check @Pnq.exists_not_badAt
#check @Pnq.exists_signs_odd
#check @Pnq.exists_lift_two_all
#check @Pnq.sizes_eq_two_all
