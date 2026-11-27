#!/bin/bash
# Checks the two finished files of the task "sets on larger groups" without trusting the instances' reports.
# 1. each fixed declaration stands character for character (check_fixed.py against the frozen skeleton), no escape hatch;
# 2. nothing that could change the meaning of a statement (instance, notation, macro, attribute, local, set_option, open ... in);
# 3. each instance's copy differs from the base copy only in its own file;
# 4. the two files together, in a fresh copy of the base ~/lean/sets: build, statements as Lean prints them = the skeleton's print, axioms.
# usage: sets-check.sh   (run when both instances have finished)
set -u
PY=~/welch/.venv/bin/python; SK=~/lean/sets-skeleton; BASE=~/lean/sets; LOG=~/lean/sets-check.log
date -u +"check started %H:%M:%S UTC %d %b %Y" > $LOG
echo "== 0. skeleton hashes" >> $LOG; (cd $SK && sha256sum -c SHA256) >> $LOG 2>&1
echo "== 1. fixed declarations and escape hatches" >> $LOG
$PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/SetLift.lean ~/lean/sets-S/Pnq/SetLift.lean >> $LOG 2>&1
$PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/SetAll.lean ~/lean/sets-A/Pnq/SetAll.lean >> $LOG 2>&1
echo "== 2. lines with instance, notation, macro, attribute, local, set_option, syntax, elab, open ... in (each to be looked at)" >> $LOG
grep -nE "^\s*(@\[|instance\b|notation\b|macro\b|attribute\b|local\b|set_option\b|syntax\b|elab\b|scoped\b|infix|prefix|postfix)|\bopen .* in\b|\bunseal\b|\bderiving\b" ~/lean/sets-S/Pnq/SetLift.lean ~/lean/sets-A/Pnq/SetAll.lean >> $LOG 2>&1 || echo "  none" >> $LOG
echo "== 3. each copy against the base copy (source files only)" >> $LOG
for c in S A; do echo "-- sets-$c" >> $LOG; diff -rq --exclude .lake --exclude build.log $BASE ~/lean/sets-$c >> $LOG 2>&1; done
echo "== 4. assembled in a fresh copy of the base" >> $LOG
rm -rf ~/lean/sets-all && cp -r $BASE ~/lean/sets-all && cp ~/lean/sets-S/Pnq/SetLift.lean ~/lean/sets-A/Pnq/SetAll.lean ~/lean/sets-all/Pnq/
cd ~/lean/sets-all
wc -l Pnq/SetLift.lean Pnq/SetAll.lean >> $LOG
touch Pnq/SetLift.lean Pnq/SetAll.lean
nice -n 5 lake build Pnq.SetAll > ~/lean/sets-all-build.log 2>&1; echo "lake build Pnq.SetAll: exit $?; $(tail -1 ~/lean/sets-all-build.log)" >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' ~/lean/sets-all-build.log); with 'sorry': $(grep -c 'sorry' ~/lean/sets-all-build.log)" >> $LOG
lake env lean CheckSets.lean > ~/lean/sets-all-CheckSets.out 2>&1
echo "statements as Lean prints them, against the skeleton's print: $(cmp -s ~/lean/sets-all-CheckSets.out $SK/CheckSets.skeleton.out && echo identical || echo DIFFERENT)" >> $LOG
cat > CheckSetsAxioms.lean <<'LEAN'
import Pnq.SetAll
#print axioms Pnq.Lift.exists_set_lift
#print axioms Pnq.Lift.set_sizes_iff_mul
#print axioms Pnq.Lift.minsize_unbalanced_set
#print axioms Pnq.Lift.minsize_balanced_all_set
#print axioms Pnq.Lift.minsize_balanced_set
LEAN
lake env lean CheckSetsAxioms.lean > ~/lean/sets-all-axioms.out 2>&1; cat ~/lean/sets-all-axioms.out >> $LOG
echo "axiom lines: $(grep -c 'depends on axioms' ~/lean/sets-all-axioms.out); exactly the standard three: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' ~/lean/sets-all-axioms.out)" >> $LOG
date -u +"check ended %H:%M:%S UTC" >> $LOG
cat $LOG
