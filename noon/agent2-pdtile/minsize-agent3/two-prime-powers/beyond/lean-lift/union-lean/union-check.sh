#!/bin/bash
# Checks the finished files of the task "twice for the whole of Z_n" (Theorem U, Corollary U) without trusting the
# instances' reports.
# 1. each fixed declaration stands character for character (check_fixed.py against the frozen skeleton), no escape hatch;
# 2. nothing that could change the meaning of a statement (instance, notation, macro, attribute, local, set_option, open ... in);
# 3. each instance's copy differs from the base copy only in its own file;
# 4. the two files together, in a fresh copy of the base ~/lean/even-U: build, statements as Lean prints them = the
#    skeleton's print, axioms of the two theorems.
# usage: union-check.sh [LETTERS]    LETTERS: which provers' files to take from their copies (default "U W")
set -u
PY=~/welch/.venv/bin/python; SK=~/lean/union-skeleton; BASE=~/lean/even-U; LOG=~/lean/union-check.log; W=~/lean/signs-briefs/lean1.sh
ALL=/home/agent3/lean/union-all
LETTERS="${1:-U W}"
declare -A FILE=( [U]=EvenUnion [W]=EvenWhole )
date -u +"check started %H:%M:%S UTC %d %b %Y; files taken from the provers: $LETTERS" > $LOG
echo "== 0. skeleton hashes" >> $LOG; (cd $SK && sha256sum -c SHA256-as-fixed) >> $LOG 2>&1
echo "   sha256 of the list: $(sha256sum $SK/SHA256-as-fixed | cut -d' ' -f1)" >> $LOG
echo "== 1. fixed declarations and escape hatches" >> $LOG
for c in $LETTERS; do f=${FILE[$c]}; $PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/$f.lean ~/lean/union-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 1a. the whole block from 'open Classical in' through the doc comment to ':= by' stands in the finished file" >> $LOG
for c in $LETTERS; do f=${FILE[$c]}; $PY - $SK/Pnq/$f.lean ~/lean/union-$c/Pnq/$f.lean >> $LOG 2>&1 <<'PYEOF'
import sys
sk = open(sys.argv[1]).read(); fin = open(sys.argv[2]).read()
i = sk.index('open Classical in\n/-- '); j = sk.index(':= by', i) + len(':= by')
b = sk[i:j]
print(f"{sys.argv[2]}: block of {len(b.splitlines())} lines found {fin.count(b)} time(s)")
PYEOF
done
echo "== 2. lines with instance, notation, macro, attribute, local, set_option, syntax, elab, open ... in (each to be looked at)" >> $LOG
for c in $LETTERS; do f=${FILE[$c]}; grep -nHE "^\s*(@\[|instance\b|notation\b|macro\b|attribute\b|local\b|set_option\b|syntax\b|elab\b|scoped\b|infix|prefix|postfix)|\bopen .* in\b|\bunseal\b|\bderiving\b|\bnative_decide\b|\bsorry\b|\badmit\b|^\s*axiom\b" ~/lean/union-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 3. each copy against the base copy (source files only; only its own file may differ)" >> $LOG
for c in $LETTERS; do echo "-- union-$c" >> $LOG; diff -rq --exclude .lake --exclude build.log $BASE ~/lean/union-$c >> $LOG 2>&1; done
echo "== 4. assembled in a fresh copy of the base" >> $LOG
if [ -e $ALL ]; then [ "$(realpath -- $ALL)" = "$ALL" ] && [ ! -L $ALL ] || { echo "union-all resolves elsewhere or is a link: stopping" >> $LOG; cat $LOG; exit 1; }; rm -rf $ALL; fi
cp -a $BASE $ALL
for c in $LETTERS; do f=${FILE[$c]}; cp ~/lean/union-$c/Pnq/$f.lean $ALL/Pnq/; done
cd $ALL
wc -l Pnq/EvenUnion.lean Pnq/EvenWhole.lean >> $LOG
touch Pnq/EvenUnion.lean Pnq/EvenWhole.lean
bash $W lake build Pnq.EvenWhole 2>&1 | awk -v c=/home/agent3/lean/union-all-build.warning-count.txt '/designed for use with the module system/ {n++; next} {print} END {print n+0 > c}' > ~/lean/union-all-build.log; echo "lake build Pnq.EvenWhole: exit ${PIPESTATUS[0]}; $(tail -1 ~/lean/union-all-build.log)" >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' ~/lean/union-all-build.log); with 'sorry': $(grep -c 'sorry' ~/lean/union-all-build.log)" >> $LOG
grep "declaration uses" ~/lean/union-all-build.log | cut -c1-120 >> $LOG
bash $W lake env lean PrintUnion.lean 2>&1 | grep -v "designed for use with the module system" > ~/lean/union-all-PrintUnion.out
echo "statements as Lean prints them, against the skeleton's print: $(cmp -s ~/lean/union-all-PrintUnion.out $SK/PrintUnion.skeleton.out && echo identical || echo DIFFERENT)" >> $LOG
cat > CheckUnionAxioms.lean <<'LEAN'
import Pnq.EvenWhole
#print axioms Pnq.card_exists_exists_levelBad_le
#print axioms Pnq.card_exists_badAt_le
LEAN
bash $W lake env lean CheckUnionAxioms.lean 2>&1 | grep -v "designed for use with the module system" > ~/lean/union-all-axioms.out; cat ~/lean/union-all-axioms.out >> $LOG
echo "axiom lines: $(grep -c 'depends on axioms' ~/lean/union-all-axioms.out); exactly the standard three: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' ~/lean/union-all-axioms.out); with sorryAx: $(grep -c 'sorryAx' ~/lean/union-all-axioms.out)" >> $LOG
echo "theorems and definitions in the two files: $(grep -cE '^(theorem|lemma) ' Pnq/EvenUnion.lean Pnq/EvenWhole.lean | tr '\n' ' '); defs: $(grep -cE '^(noncomputable def|def|abbrev) ' Pnq/EvenUnion.lean Pnq/EvenWhole.lean | tr '\n' ' ')" >> $LOG
date -u +"check ended %H:%M:%S UTC" >> $LOG
cat $LOG
