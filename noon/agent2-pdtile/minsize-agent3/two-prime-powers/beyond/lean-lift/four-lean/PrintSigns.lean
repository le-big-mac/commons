import Pnq.SignFinal
/-! The ten definitions and the fifteen fixed statements as Lean has them (printed in the skeleton and again in the
finished project; the two prints must be identical). -/
open Pnq
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
set_option pp.explicit true in
#check @Pnq.classSum_eq_of_badAt
set_option pp.explicit true in
#check @Pnq.badAt_of_not_live
set_option pp.explicit true in
#check @Pnq.card_badSet_mul_two_pow_card_le
set_option pp.explicit true in
#check @Pnq.badAt_one_iff
set_option pp.explicit true in
#check @Pnq.card_badSet_one
set_option pp.explicit true in
#check @Pnq.rank_lt_card_image
set_option pp.explicit true in
#check @Pnq.exists_isPivot
set_option pp.explicit true in
#check @Pnq.card_badSet_mul_two_pow_rank_le
set_option pp.explicit true in
#check @Pnq.rank_lt_card
set_option pp.explicit true in
#check @Pnq.card_badSet_three_pow_mul_le
set_option pp.explicit true in
#check @Pnq.lhsN1_lt_one
set_option pp.explicit true in
#check @Pnq.exists_not_badAt
set_option pp.explicit true in
#check @Pnq.exists_signs_odd
set_option pp.explicit true in
#check @Pnq.exists_lift_two_all
set_option pp.explicit true in
#check @Pnq.sizes_eq_two_all
