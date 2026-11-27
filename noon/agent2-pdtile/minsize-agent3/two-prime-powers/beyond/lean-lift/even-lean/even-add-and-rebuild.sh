#!/bin/bash
# The eight files for the statement on signs for every n (EvenDefs, EvenTwice, EvenSlice, EvenCount, EvenLadder, EvenSum,
# EvenAll, EvenFinal) and the shared lean-tiling folder.
#   bash even-add-and-rebuild.sh dry   copies the shared folder as it is into a fresh private copy, adds the eight files
#                                      THERE ONLY, and builds that copy from nothing.  Touches nothing shared.
#   bash even-add-and-rebuild.sh add   ONLY AFTER NOON'S WORD: adds the eight files to the shared folder, then copies it
#                                      into a fresh private copy and builds that from nothing.
# In both, only Mathlib's package folder is shared with earlier copies.
set -e
MODE="$1"; [ "$MODE" = dry ] || [ "$MODE" = add ] || { echo "usage: $0 dry|add"; exit 1; }
SH=/srv/commons/agent2-pdtile/lean-tiling
SRC=/home/agent3/lean/even-all/Pnq
CL=/home/agent3/lean/even-clean-$MODE
FILES="EvenDefs EvenTwice EvenSlice EvenCount EvenLadder EvenSum EvenAll EvenFinal"
NAMES="card_exists_levelBad_le bad3_of_badAt classSum3_eq_of_bad3 bad3_of_not_live card_bad3Set_mul_two_pow_card_le card_bad3Set_mul_two_pow_rank_le bad3_one_iff card_bad3Set_one card_exists_bad3_le sum_half_pow_mu_lt exists_not_bad3 exists_not_badAt_of_three_le exists_signs_all not_exists_signs_of_exceptionalPair"
for f in $FILES; do [ -f $SRC/$f.lean ] || { echo "missing $SRC/$f.lean: stopping"; exit 1; }; done
(cd $SRC && sha256sum -c /home/agent3/lean/even-post.new/SHA256-finished >/dev/null 2>&1) || (cd $SRC && sha256sum -c /home/agent3/lean/even-post/SHA256-finished >/dev/null 2>&1) || { echo "the eight files are not the checked ones (SHA256-finished): stopping"; exit 1; }
grep -lw "sorry" $(for f in $FILES; do echo $SRC/$f.lean; done) && { echo "a file still has sorry: stopping"; exit 1; }
add_to () {   # $1 = a lean-tiling folder
  for f in $FILES; do cp $SRC/$f.lean $1/Pnq/; grep -q "^import Pnq.$f$" $1/Pnq.lean || printf 'import Pnq.%s\n' $f >> $1/Pnq.lean; done
  for n in $NAMES; do grep -q "Pnq.$n$" $1/CheckPnq.lean || printf '#print axioms Pnq.%s\n' $n >> $1/CheckPnq.lean; done
}
[ "$MODE" = add ] && add_to $SH
if [ -e "$CL" ]; then [ "$(realpath -- "$CL")" = "$CL" ] || { echo "$CL resolves elsewhere: stopping"; exit 1; }; rm -rf "$CL"; fi
mkdir "$CL"
(cd $SH && find . -type f \( -name "*.lean" -o -name "lakefile.toml" -o -name "lean-toolchain" -o -name "lake-manifest.json" \) | sort > $CL.files)
(cd $SH && xargs sha256sum < $CL.files) > $CL.sha256.before
(cd $SH && tar cf - -T $CL.files) | (cd $CL && tar xf -)
[ "$MODE" = dry ] && add_to $CL
mkdir -p $CL/.lake && ln -s /home/agent3/lean/tiling-check4/.lake/packages $CL/.lake/packages
cd $CL
LOG=$CL.log
date -u +"start %H:%M:%S UTC %d %b ($MODE)" > $LOG
set +e
nice -n 10 lake build > $CL-build.log 2>&1; echo "lake build exit $?" >> $LOG
tail -1 $CL-build.log >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' $CL-build.log); with 'sorry': $(grep -c 'sorry' $CL-build.log)" >> $LOG
echo "library modules built: $(grep -c '\] Built ' $CL-build.log)" >> $LOG
for f in Check.lean CheckPnq.lean CheckP2q2.lean; do nice -n 10 lake env lean $f > $CL-$f.out 2>&1; echo "lake env lean $f: $(grep -c 'depends on axioms' $CL-$f.out) axiom lines, $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' $CL-$f.out) exactly the standard three, other lines $(grep -vc 'depends on axioms' $CL-$f.out)" >> $LOG; done
for n in $NAMES; do grep "Pnq.$n'" $CL-CheckPnq.lean.out >> $LOG; done
date -u +"end %H:%M:%S UTC" >> $LOG
(cd $SH && xargs sha256sum < $CL.files) > $CL.sha256.after
echo "files taken from the shared folder: $(wc -l < $CL.files) ($(grep -c '\.lean$' $CL.files) Lean files); shared folder before = after the build: $(cmp -s $CL.sha256.before $CL.sha256.after && echo identical || echo DIFFERENT)" >> $LOG
if [ "$MODE" = add ]; then (cd $CL && xargs sha256sum < $CL.files) > $CL.sha256.built; echo "built copy = shared: $(cmp -s $CL.sha256.before $CL.sha256.built && echo identical || echo DIFFERENT)" >> $LOG; fi
cat $LOG
