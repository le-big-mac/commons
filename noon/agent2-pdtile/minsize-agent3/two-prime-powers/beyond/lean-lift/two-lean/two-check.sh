#!/bin/bash
# Checks the three finished files of the task "prime 2 and every s" without trusting the instances' reports.
# 1. each fixed declaration stands character for character (check_fixed.py against the frozen skeleton), no escape hatch;
# 2. nothing that could change the meaning of a statement (instance, notation, macro, attribute, local, set_option, open ... in);
# 3. each instance's copy differs from the base copy only in its own file;
# 4. the three files together, in the base copy ~/lean/two: build, statements as Lean prints them = the skeleton's print, axioms.
# usage: two-check.sh   (run when all three instances have finished)
set -u
PY=~/welch/.venv/bin/python; SK=~/lean/two-skeleton; BASE=~/lean/two; LOG=~/lean/two-check.log
date -u +"check started %H:%M:%S UTC %d %b %Y" > $LOG
echo "== 0. skeleton hashes" >> $LOG; (cd $SK && sha256sum -c SHA256) >> $LOG 2>&1
echo "== 1. fixed declarations and escape hatches" >> $LOG
$PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/Sign.lean ~/lean/two-S/Pnq/Sign.lean >> $LOG 2>&1
$PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/Lift2.lean ~/lean/two-L/Pnq/Lift2.lean >> $LOG 2>&1
$PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/LiftAll.lean ~/lean/two-A/Pnq/LiftAll.lean >> $LOG 2>&1
echo "== 2. lines with instance, notation, macro, attribute, local, set_option, syntax, elab, open ... in (each to be looked at)" >> $LOG
grep -nE "^\s*(@\[|instance\b|notation\b|macro\b|attribute\b|local\b|set_option\b|syntax\b|elab\b|scoped\b|infix|prefix|postfix)|\bopen .* in\b|\bunseal\b|\bderiving\b" ~/lean/two-S/Pnq/Sign.lean ~/lean/two-L/Pnq/Lift2.lean ~/lean/two-A/Pnq/LiftAll.lean >> $LOG 2>&1 || echo "  none" >> $LOG
echo "== 3. each copy against the base copy (source files only)" >> $LOG
for c in S L A; do echo "-- two-$c" >> $LOG; diff -rq --exclude .lake --exclude build.log $BASE ~/lean/two-$c >> $LOG 2>&1; done
echo "== 4. assembled in a fresh copy of the base" >> $LOG
rm -rf ~/lean/two-all && cp -r $BASE ~/lean/two-all && cp ~/lean/two-S/Pnq/Sign.lean ~/lean/two-L/Pnq/Lift2.lean ~/lean/two-A/Pnq/LiftAll.lean ~/lean/two-all/Pnq/
cd ~/lean/two-all
wc -l Pnq/Sign.lean Pnq/Lift2.lean Pnq/LiftAll.lean >> $LOG
touch Pnq/Sign.lean Pnq/Lift2.lean Pnq/LiftAll.lean
nice -n 5 lake build Pnq.LiftAll > ~/lean/two-all-build.log 2>&1; echo "lake build Pnq.LiftAll: exit $?; $(tail -1 ~/lean/two-all-build.log)" >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' ~/lean/two-all-build.log); with 'sorry': $(grep -c 'sorry' ~/lean/two-all-build.log)" >> $LOG
lake env lean CheckTwo.lean > ~/lean/two-all-CheckTwo.out 2>&1
echo "statements as Lean prints them, against the skeleton's print: $(cmp -s ~/lean/two-all-CheckTwo.out $SK/CheckTwo.skeleton.out && echo identical || echo DIFFERENT)" >> $LOG
cat > CheckTwoAxioms.lean <<'LEAN'
import Pnq.LiftAll
#print axioms Pnq.Lift.exists_signs
#print axioms Pnq.Lift.exists_lift_two
#print axioms Pnq.Lift.sizes_eq_two
#print axioms Pnq.Lift.sizes_eq_odd
#print axioms Pnq.Lift.sizes_eq_mul
#print axioms Pnq.Lift.minsize_unbalanced_mul
#print axioms Pnq.Lift.minsize_balanced_all_mul
#print axioms Pnq.Lift.minsize_balanced_mul
LEAN
lake env lean CheckTwoAxioms.lean > ~/lean/two-all-axioms.out 2>&1; cat ~/lean/two-all-axioms.out >> $LOG
echo "axiom lines: $(grep -c 'depends on axioms' ~/lean/two-all-axioms.out); exactly the standard three: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' ~/lean/two-all-axioms.out)" >> $LOG
date -u +"check ended %H:%M:%S UTC" >> $LOG
cat $LOG
