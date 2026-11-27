import Pnq.EvenWhole
/-! The two fixed statements of the evening of 27 November as Lean has them (printed in the skeleton and again in the
finished project; the two prints must be identical). -/
open Pnq
set_option pp.explicit true in
#check @Pnq.card_exists_exists_levelBad_le
set_option pp.explicit true in
#check @Pnq.card_exists_badAt_le
