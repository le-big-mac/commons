import Pnq.EvenFinal
/-! The eight definitions and the fourteen fixed statements as Lean has them (printed in the skeleton and again in the
finished project; the two prints must be identical). -/
open Pnq
#print Pnq.F3
#print Pnq.val3
#print Pnq.Bad3
#print Pnq.bad3Set
#print Pnq.classSum3
#print Pnq.csum
#print Pnq.levelBad
#print Pnq.ExceptionalPair
set_option pp.explicit true in
#check @Pnq.card_exists_levelBad_le
set_option pp.explicit true in
#check @Pnq.bad3_of_badAt
set_option pp.explicit true in
#check @Pnq.classSum3_eq_of_bad3
set_option pp.explicit true in
#check @Pnq.bad3_of_not_live
set_option pp.explicit true in
#check @Pnq.card_bad3Set_mul_two_pow_card_le
set_option pp.explicit true in
#check @Pnq.card_bad3Set_mul_two_pow_rank_le
set_option pp.explicit true in
#check @Pnq.bad3_one_iff
set_option pp.explicit true in
#check @Pnq.card_bad3Set_one
set_option pp.explicit true in
#check @Pnq.card_exists_bad3_le
set_option pp.explicit true in
#check @Pnq.sum_half_pow_mu_lt
set_option pp.explicit true in
#check @Pnq.exists_not_bad3
set_option pp.explicit true in
#check @Pnq.exists_not_badAt_of_three_le
set_option pp.explicit true in
#check @Pnq.exists_signs_all
set_option pp.explicit true in
#check @Pnq.not_exists_signs_of_exceptionalPair
