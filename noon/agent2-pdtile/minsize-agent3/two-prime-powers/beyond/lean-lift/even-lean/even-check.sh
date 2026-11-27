#!/bin/bash
# Checks the finished files of the task "the statement on signs for every n" without trusting the instances' reports.
# 1. each fixed declaration stands character for character (check_fixed.py against the frozen skeleton), no escape hatch;
# 2. nothing that could change the meaning of a statement (instance, notation, macro, attribute, local, set_option, open ... in);
# 3. each instance's copy differs from the base copy only in its own file;
# 4. the files together, in a fresh copy of the base ~/lean/even: build, statements as Lean prints them = the skeleton's
#    print, axioms of the fourteen theorems.
# usage: even-check.sh [LETTERS]    LETTERS: which provers' files to take from their copies (default "T S C L N A F");
#                                   a file not taken stays as in the skeleton (with sorry).
set -u
PY=~/welch/.venv/bin/python; SK=~/lean/even-skeleton; BASE=~/lean/even; LOG=~/lean/even-check.log; W=~/lean/signs-briefs/lean1.sh
LETTERS="${1:-T S C L N A F}"
declare -A FILE=( [T]=EvenTwice [S]=EvenSlice [C]=EvenCount [L]=EvenLadder [N]=EvenSum [A]=EvenAll [F]=EvenFinal )
date -u +"check started %H:%M:%S UTC %d %b %Y; files taken from the provers: $LETTERS" > $LOG
echo "== 0. skeleton hashes" >> $LOG; (cd $SK && sha256sum -c SHA256-as-fixed) >> $LOG 2>&1
echo "   sha256 of the list: $(sha256sum $SK/SHA256-as-fixed | cut -d' ' -f1)" >> $LOG
echo "== 1. fixed declarations and escape hatches" >> $LOG
for c in $LETTERS; do f=${FILE[$c]}; $PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/$f.lean ~/lean/even-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 2. lines with instance, notation, macro, attribute, local, set_option, syntax, elab, open ... in (each to be looked at)" >> $LOG
for c in $LETTERS; do f=${FILE[$c]}; grep -nHE "^\s*(@\[|instance\b|notation\b|macro\b|attribute\b|local\b|set_option\b|syntax\b|elab\b|scoped\b|infix|prefix|postfix)|\bopen .* in\b|\bunseal\b|\bderiving\b|\bnative_decide\b|\bsorry\b|\badmit\b|^\s*axiom\b" ~/lean/even-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 3. each copy against the base copy (source files only; only its own file may differ)" >> $LOG
for c in $LETTERS; do echo "-- even-$c" >> $LOG; diff -rq --exclude .lake --exclude build.log $BASE ~/lean/even-$c >> $LOG 2>&1; done
echo "== 4. assembled in a fresh copy of the base" >> $LOG
[ "$(realpath -- ~/lean/even-all 2>/dev/null)" = "/home/agent3/lean/even-all" ] || [ ! -e ~/lean/even-all ] || { echo "even-all resolves elsewhere: stopping" >> $LOG; cat $LOG; exit 1; }
[ -L ~/lean/even-all ] && { echo "even-all is a link: stopping" >> $LOG; cat $LOG; exit 1; }
rm -rf /home/agent3/lean/even-all && cp -a $BASE ~/lean/even-all
for c in $LETTERS; do f=${FILE[$c]}; cp ~/lean/even-$c/Pnq/$f.lean ~/lean/even-all/Pnq/; done
cd ~/lean/even-all
for f in EvenDefs; do cmp -s Pnq/$f.lean $SK/Pnq/$f.lean && echo "Pnq/$f.lean is the skeleton's" >> $LOG || echo "Pnq/$f.lean DIFFERS from the skeleton's" >> $LOG; done
wc -l Pnq/Even{Defs,Twice,Slice,Count,Ladder,Sum,All,Final}.lean >> $LOG
touch Pnq/Even{Twice,Slice,Count,Ladder,Sum,All,Final}.lean
bash $W lake build Pnq.EvenFinal > ~/lean/even-all-build.log 2>&1; echo "lake build Pnq.EvenFinal: exit $?; $(tail -1 ~/lean/even-all-build.log)" >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' ~/lean/even-all-build.log); with 'sorry': $(grep -c 'sorry' ~/lean/even-all-build.log)" >> $LOG
grep "declaration uses" ~/lean/even-all-build.log | cut -c1-120 >> $LOG
bash $W lake env lean PrintEven.lean > ~/lean/even-all-PrintEven.out 2>&1
echo "definitions and statements as Lean prints them, against the skeleton's print: $(cmp -s ~/lean/even-all-PrintEven.out $SK/PrintEven.skeleton.out && echo identical || echo DIFFERENT)" >> $LOG
bash $W lake env lean CheckEven.lean > ~/lean/even-all-CheckEven.out 2>&1; echo "CheckEven.lean: $(grep -c 'error' ~/lean/even-all-CheckEven.out) lines with 'error'" >> $LOG
cat > CheckEvenAxioms.lean <<'LEAN'
import Pnq.EvenFinal
#print axioms Pnq.card_exists_levelBad_le
#print axioms Pnq.bad3_of_badAt
#print axioms Pnq.classSum3_eq_of_bad3
#print axioms Pnq.bad3_of_not_live
#print axioms Pnq.card_bad3Set_mul_two_pow_card_le
#print axioms Pnq.card_bad3Set_mul_two_pow_rank_le
#print axioms Pnq.bad3_one_iff
#print axioms Pnq.card_bad3Set_one
#print axioms Pnq.card_exists_bad3_le
#print axioms Pnq.sum_half_pow_mu_lt
#print axioms Pnq.exists_not_bad3
#print axioms Pnq.exists_not_badAt_of_three_le
#print axioms Pnq.exists_signs_all
#print axioms Pnq.not_exists_signs_of_exceptionalPair
LEAN
bash $W lake env lean CheckEvenAxioms.lean > ~/lean/even-all-axioms.out 2>&1; cat ~/lean/even-all-axioms.out >> $LOG
echo "axiom lines: $(grep -c 'depends on axioms' ~/lean/even-all-axioms.out); exactly the standard three: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' ~/lean/even-all-axioms.out); with sorryAx: $(grep -c 'sorryAx' ~/lean/even-all-axioms.out)" >> $LOG
date -u +"check ended %H:%M:%S UTC" >> $LOG
cat $LOG
