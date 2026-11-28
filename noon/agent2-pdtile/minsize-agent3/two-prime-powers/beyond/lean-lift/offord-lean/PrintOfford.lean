import Pnq.OffordBad
/-! The seven fixed statements of 28 November as Lean has them (printed in the skeleton and again in the finished
project; the two prints must be identical). -/
open Pnq
set_option pp.explicit true in
#check @Pnq.card_signedSum_eq_le_real
set_option pp.explicit true in
#check @Pnq.card_signedSum_eq_le_complex
set_option pp.explicit true in
#check @Pnq.card_badAt_le_choose
set_option pp.explicit true in
#check @Pnq.not_badAt_one_of_odd
set_option pp.explicit true in
#check @Pnq.card_exists_badAt_two_pow_le
set_option pp.explicit true in
#check @Pnq.not_exists_badAt_two_pow_of_odd
set_option pp.explicit true in
#check @Pnq.card_exists_badAt_le_divisors
