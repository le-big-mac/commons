#!/bin/bash
# Checks the finished files of the task "the statement on signs for every odd n" without trusting the instances' reports.
# 1. each fixed declaration stands character for character (check_fixed.py against the frozen skeleton), no escape hatch;
# 2. nothing that could change the meaning of a statement (instance, notation, macro, attribute, local, set_option, open ... in);
# 3. each instance's copy differs from the base copy only in its own file;
# 4. the files together, in a fresh copy of the base ~/lean/signs: build, statements as Lean prints them = the skeleton's
#    print, axioms of the fifteen theorems.
# usage: signs-check.sh [LETTERS]    LETTERS: which provers' files to take from their copies (default "S C V T N A F");
#                                    a file not taken stays as in the skeleton (with sorry).
set -u
PY=~/welch/.venv/bin/python; SK=~/lean/signs-skeleton; BASE=~/lean/signs; LOG=~/lean/signs-check.log; W=~/lean/signs-briefs/lean1.sh
LETTERS="${1:-S C V T N A F}"
declare -A FILE=( [S]=SignSlice [C]=SignCount [V]=SignPivot [T]=SignThree [N]=SignSum [A]=SignAll [F]=SignFinal )
date -u +"check started %H:%M:%S UTC %d %b %Y; files taken from the provers: $LETTERS" > $LOG
echo "== 0. skeleton hashes" >> $LOG; (cd $SK && sha256sum -c SHA256-as-fixed) >> $LOG 2>&1
echo "   sha256 of the list: $(sha256sum $SK/SHA256-as-fixed | cut -d' ' -f1)" >> $LOG
echo "== 1. fixed declarations and escape hatches" >> $LOG
for c in $LETTERS; do f=${FILE[$c]}; $PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/$f.lean ~/lean/signs-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 2. lines with instance, notation, macro, attribute, local, set_option, syntax, elab, open ... in (each to be looked at)" >> $LOG
for c in $LETTERS; do f=${FILE[$c]}; grep -nHE "^\s*(@\[|instance\b|notation\b|macro\b|attribute\b|local\b|set_option\b|syntax\b|elab\b|scoped\b|infix|prefix|postfix)|\bopen .* in\b|\bunseal\b|\bderiving\b|\bnative_decide\b|\bsorry\b|\badmit\b|^\s*axiom\b" ~/lean/signs-$c/Pnq/$f.lean >> $LOG 2>&1 || echo "  $f: none" >> $LOG; done
echo "== 3. each copy against the base copy (source files only; only its own file may differ)" >> $LOG
for c in $LETTERS; do echo "-- signs-$c" >> $LOG; diff -rq --exclude .lake --exclude build.log $BASE ~/lean/signs-$c >> $LOG 2>&1; done
echo "== 4. assembled in a fresh copy of the base" >> $LOG
rm -rf ~/lean/signs-all && cp -r $BASE ~/lean/signs-all
for c in $LETTERS; do f=${FILE[$c]}; cp ~/lean/signs-$c/Pnq/$f.lean ~/lean/signs-all/Pnq/; done
cd ~/lean/signs-all
find .lake/build -name 'SignCountB*' -delete 2>/dev/null; echo "stale build files of the first skeleton's SignCountB left in the copy: $(find .lake/build -name 'SignCountB*' | wc -l)" >> $LOG
for f in SignDefs; do cmp -s Pnq/$f.lean $SK/Pnq/$f.lean && echo "Pnq/$f.lean is the skeleton's" >> $LOG || echo "Pnq/$f.lean DIFFERS from the skeleton's" >> $LOG; done
wc -l Pnq/Sign{Defs,Slice,Count,Pivot,Three,Sum,All,Final}.lean >> $LOG
touch Pnq/Sign{Slice,Count,Pivot,Three,Sum,All,Final}.lean
bash $W lake build Pnq.SignFinal > ~/lean/signs-all-build.log 2>&1; echo "lake build Pnq.SignFinal: exit $?; $(tail -1 ~/lean/signs-all-build.log)" >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' ~/lean/signs-all-build.log); with 'sorry': $(grep -c 'sorry' ~/lean/signs-all-build.log)" >> $LOG
grep "declaration uses" ~/lean/signs-all-build.log | cut -c1-120 >> $LOG
bash $W lake env lean PrintSigns.lean > ~/lean/signs-all-PrintSigns.out 2>&1
echo "definitions and statements as Lean prints them, against the skeleton's print: $(cmp -s ~/lean/signs-all-PrintSigns.out $SK/PrintSigns.skeleton.out && echo identical || echo DIFFERENT)" >> $LOG
bash $W lake env lean CheckSigns.lean > ~/lean/signs-all-CheckSigns.out 2>&1; echo "CheckSigns.lean: $(grep -c 'error' ~/lean/signs-all-CheckSigns.out) lines with 'error'" >> $LOG
cat > CheckSignsAxioms.lean <<'LEAN'
import Pnq.SignFinal
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
LEAN
bash $W lake env lean CheckSignsAxioms.lean > ~/lean/signs-all-axioms.out 2>&1; cat ~/lean/signs-all-axioms.out >> $LOG
echo "axiom lines: $(grep -c 'depends on axioms' ~/lean/signs-all-axioms.out); exactly the standard three: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' ~/lean/signs-all-axioms.out); with sorryAx: $(grep -c 'sorryAx' ~/lean/signs-all-axioms.out)" >> $LOG
date -u +"check ended %H:%M:%S UTC" >> $LOG
cat $LOG
