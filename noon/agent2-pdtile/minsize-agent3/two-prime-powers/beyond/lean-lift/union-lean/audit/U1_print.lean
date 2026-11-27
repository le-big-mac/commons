import Pnq.EvenWhole
/-! Audit of the evening of 27 November (statements U and Corollary U): the two statements printed with every
instance (`pp.all`), their universe levels, and the definitions they use. -/
open Pnq
set_option pp.all true in
#check @Pnq.card_exists_exists_levelBad_le
set_option pp.all true in
#check @Pnq.card_exists_badAt_le
set_option pp.universes true in
#check @Pnq.card_exists_exists_levelBad_le
set_option pp.universes true in
#check @Pnq.card_exists_badAt_le
#print Pnq.csum
#print Pnq.levelBad
#print Pnq.sg
#print Pnq.P
#print Pnq.BadAt
#print axioms Pnq.card_exists_exists_levelBad_le
#print axioms Pnq.card_exists_badAt_le
#print axioms Pnq.card_exists_levelBad_le
