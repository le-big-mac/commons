#!/bin/bash
# Checks the finished files of the task "Erdős's bound and the first statements about shares" without trusting the
# instances' reports.
# 0. the skeleton is the frozen one (hashes);
# 1. each fixed declaration stands character for character in the finished file (the whole block from its doc comment,
#    with "open Classical in" where it has one, to ":= by"), and check_fixed.py agrees; no escape hatch;
# 2. nothing that could change the meaning of a statement (instance, notation, macro, attribute, local, set_option, …);
# 3. each instance's copy differs from the skeleton copy only in its own file;
# 4. the two files together, in a fresh copy of the skeleton: build, statements as Lean prints them = the skeleton's
#    print, axioms of the seven theorems.
# usage: offord-check.sh
set -u
PY=~/welch/.venv/bin/python; SK=/home/agent3/lean/offord-skeleton; LOG=/home/agent3/lean/offord-check.log; W=~/lean/signs-briefs/lean1.sh
ALL=/home/agent3/lean/offord-all
declare -A FILE=( [A]=Offord [B]=OffordBad )
NAMES="card_signedSum_eq_le_real card_signedSum_eq_le_complex card_badAt_le_choose not_badAt_one_of_odd card_exists_badAt_two_pow_le not_exists_badAt_two_pow_of_odd card_exists_badAt_le_divisors"
date -u +"check started %H:%M:%S UTC %d %b %Y" > $LOG
echo "== 0. skeleton hashes" >> $LOG; (cd $SK && sha256sum -c SHA256-as-fixed) >> $LOG 2>&1
echo "   sha256 of the list: $(sha256sum $SK/SHA256-as-fixed | cut -d' ' -f1)" >> $LOG
echo "== 1. fixed declarations" >> $LOG
for c in A B; do f=${FILE[$c]}; $PY ~/lean/min-skeleton/check_fixed.py $SK/Pnq/$f.lean ~/lean/offord-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 1a. every block from the doc comment (with 'open Classical in' where the skeleton has it) to ':= by' stands in the finished file" >> $LOG
for c in A B; do f=${FILE[$c]}; $PY - $SK/Pnq/$f.lean ~/lean/offord-$c/Pnq/$f.lean >> $LOG 2>&1 <<'PYEOF'
import sys, re
sk = open(sys.argv[1], encoding='utf-8').read(); fin = open(sys.argv[2], encoding='utf-8').read()
blocks = re.findall(r'((?:open Classical in\n)?/-- (?:(?!\n/-- |\ntheorem ).|\n)*?\ntheorem (\w+)(?:.|\n)*?:= by)\n  sorry', sk)
print(f"{sys.argv[2]}: {len(blocks)} fixed theorems in the skeleton")
for b, name in blocks:
    print(f"   {name}: block of {len(b.splitlines())} lines found {fin.count(b)} time(s)")
PYEOF
done
echo "== 1b. escape hatches (must be none)" >> $LOG
for c in A B; do f=${FILE[$c]}; grep -nHwE "sorry|admit|axiom|native_decide|unsafe|opaque|implemented_by" ~/lean/offord-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 2. lines with instance, notation, macro, attribute, local, set_option, syntax, elab, open ... in (each to be looked at; 'open Classical in' stands before five of the fixed theorems)" >> $LOG
for c in A B; do f=${FILE[$c]}; grep -nHE "^\s*(@\[|instance\b|notation\b|macro\b|attribute\b|local\b|set_option\b|syntax\b|elab\b|scoped\b|infix|prefix|postfix)|\bopen .* in\b|\bunseal\b|\bderiving\b" ~/lean/offord-$c/Pnq/$f.lean >> $LOG 2>&1; done
echo "== 3. each copy against the skeleton copy (source files only; only its own file may differ)" >> $LOG
for c in A B; do echo "-- offord-$c" >> $LOG; diff -rq --exclude .lake --exclude build.log $SK ~/lean/offord-$c >> $LOG 2>&1; done
echo "== 4. assembled in a fresh copy of the skeleton" >> $LOG
if [ -e $ALL ]; then [ "$(realpath -- $ALL)" = "$ALL" ] && [ ! -L $ALL ] || { echo "offord-all resolves elsewhere or is a link: stopping" >> $LOG; cat $LOG; exit 1; }; rm -rf $ALL; fi
cp -a $SK $ALL
for c in A B; do f=${FILE[$c]}; cp ~/lean/offord-$c/Pnq/$f.lean $ALL/Pnq/; done
cd $ALL
wc -l Pnq/Offord.lean Pnq/OffordBad.lean >> $LOG
touch Pnq/Offord.lean Pnq/OffordBad.lean
bash $W lake build Pnq.OffordBad 2>&1 | awk -v c=/home/agent3/lean/offord-all-build.warning-count.txt '/designed for use with the module system/ {n++; next} {print} END {print n+0 > c}' > ~/lean/offord-all-build.log; echo "lake build Pnq.OffordBad exit ${PIPESTATUS[0]}" >> $LOG
tail -1 ~/lean/offord-all-build.log >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' ~/lean/offord-all-build.log); with 'sorry': $(grep -c 'sorry' ~/lean/offord-all-build.log)" >> $LOG
grep "declaration uses" ~/lean/offord-all-build.log | cut -c1-120 >> $LOG
bash $W lake env lean PrintOfford.lean 2>&1 | grep -v "designed for use with the module system" > ~/lean/offord-all-PrintOfford.out
echo "statements as Lean prints them, against the skeleton's print: $(cmp -s ~/lean/offord-all-PrintOfford.out $SK/PrintOfford.skeleton.out && echo identical || echo DIFFERENT)" >> $LOG
{ echo "import Pnq.OffordBad"; for n in $NAMES; do echo "#print axioms Pnq.$n"; done; } > CheckOffordAxioms.lean
bash $W lake env lean CheckOffordAxioms.lean 2>&1 | grep -v "designed for use with the module system" > ~/lean/offord-all-axioms.out; cat ~/lean/offord-all-axioms.out >> $LOG
echo "axiom lines: $(grep -c 'depends on axioms' ~/lean/offord-all-axioms.out); exactly the standard three: $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' ~/lean/offord-all-axioms.out); with sorryAx: $(grep -c sorryAx ~/lean/offord-all-axioms.out)" >> $LOG
echo "theorems and lemmas in the two files: $(grep -cE '^(theorem|lemma) ' Pnq/Offord.lean Pnq/OffordBad.lean | tr '\n' ' '); defs: $(grep -cE '^(noncomputable def|def|abbrev) ' Pnq/Offord.lean Pnq/OffordBad.lean | tr '\n' ' ')" >> $LOG
date -u +"check ended %H:%M:%S UTC" >> $LOG
cat $LOG
