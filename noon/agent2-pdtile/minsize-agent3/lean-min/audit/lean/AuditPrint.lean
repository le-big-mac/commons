import Pnq.MinGroup

-- Audit scratch: print the three theorems and the definitions they rest on with every
-- constant and instance spelled out.

#print axioms Pnq.minsize_unbalanced_zmod
#print axioms Pnq.minsize_balanced_all_zmod
#print axioms Pnq.minsize_balanced_zmod

set_option pp.all true in
#print Pnq.maskW
set_option pp.all true in
#print Pnq.levelsEW
set_option pp.all true in
#print Pnq.levelsFW
set_option pp.all true in
#print Pnq.gOf
set_option pp.all true in
#print Pnq.xOf
set_option pp.all true in
#print Pnq.minU
set_option pp.all true in
#print Pnq.minB
set_option pp.all true in
#check @Pnq.minsize_unbalanced_zmod
set_option pp.all true in
#check @Pnq.minsize_balanced_all_zmod
set_option pp.all true in
#check @Pnq.minsize_balanced_zmod
