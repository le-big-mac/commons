#!/bin/bash
# DRY RUN (the shared folder is only read): adds the nine files for the statement on signs for every odd n (SignDefs, SignSlice, SignCount, SignPivot, SignThree,
# SignSum, SignAll, SignFinal, SignMul) to the shared lean-tiling folder (ONLY after Noon's word; the audit is back), then
# rebuilds a fresh copy of the shared folder from nothing under my own account (only Mathlib's package folder is shared
# with earlier copies).
set -e
SRC=/srv/commons/agent2-pdtile/lean-tiling; SH=~/lean/signs-dry-shared; rm -rf $SH; mkdir -p $SH; (cd $SRC && find . -type f \( -name "*.lean" -o -name "lakefile.toml" -o -name "lean-toolchain" -o -name "lake-manifest.json" \) | sort | tar cf - -T -) | (cd $SH && tar xf -)
FILES="SignDefs SignSlice SignCount SignPivot SignThree SignSum SignAll SignFinal SignMul"
NAMES="classSum_eq_of_badAt badAt_of_not_live card_badSet_mul_two_pow_card_le badAt_one_iff card_badSet_one rank_lt_card_image exists_isPivot card_badSet_mul_two_pow_rank_le rank_lt_card card_badSet_three_pow_mul_le lhsN1_lt_one exists_not_badAt exists_signs_odd exists_lift_two_all sizes_eq_two_all sizes_eq_mul_all"
for f in $FILES; do [ -f ~/lean/signs-all/Pnq/$f.lean ] || { echo "missing ~/lean/signs-all/Pnq/$f.lean: stopping"; exit 1; }; done
grep -l "sorry" $(for f in $FILES; do echo ~/lean/signs-all/Pnq/$f.lean; done) && { echo "a file still has sorry: stopping"; exit 1; }
for f in $FILES; do cp ~/lean/signs-all/Pnq/$f.lean $SH/Pnq/; grep -q "^import Pnq.$f$" $SH/Pnq.lean || printf 'import Pnq.%s\n' $f >> $SH/Pnq.lean; done
for n in $NAMES; do grep -q "Pnq.$n$" $SH/CheckPnq.lean || printf '#print axioms Pnq.%s\n' $n >> $SH/CheckPnq.lean; done
rm -rf ~/lean/signs-dry; mkdir ~/lean/signs-dry
(cd $SH && find . -type f \( -name "*.lean" -o -name "lakefile.toml" -o -name "lean-toolchain" -o -name "lake-manifest.json" \) | sort > ~/lean/signs-dry.files)
(cd $SH && xargs sha256sum < ~/lean/signs-dry.files) > ~/lean/signs-dry.sha256.before
(cd $SH && tar cf - -T ~/lean/signs-dry.files) | (cd ~/lean/signs-dry && tar xf -)
mkdir -p ~/lean/signs-dry/.lake && ln -s /home/agent3/lean/tiling-check4/.lake/packages ~/lean/signs-dry/.lake/packages
cd ~/lean/signs-dry
LOG=~/lean/signs-dry.log
date -u +"start %H:%M:%S UTC %d %b" > $LOG
set +e
nice -n 5 lake build > ~/lean/signs-dry-build.log 2>&1; echo "lake build exit $?" >> $LOG
tail -1 ~/lean/signs-dry-build.log >> $LOG
echo "lines with 'error' in the build log: $(grep -c 'error' ~/lean/signs-dry-build.log); with 'sorry': $(grep -c 'sorry' ~/lean/signs-dry-build.log)" >> $LOG
echo "library modules built: $(grep -c '\] Built ' ~/lean/signs-dry-build.log)" >> $LOG
for f in Check.lean CheckPnq.lean CheckP2q2.lean; do lake env lean $f > ~/lean/signs-dry-$f.out 2>&1; echo "lake env lean $f: $(grep -c 'depends on axioms' ~/lean/signs-dry-$f.out) axiom lines, $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' ~/lean/signs-dry-$f.out) exactly the standard three, other lines $(grep -vc 'depends on axioms' ~/lean/signs-dry-$f.out)" >> $LOG; done
for n in $NAMES; do grep "Pnq.$n'" ~/lean/signs-dry-CheckPnq.lean.out >> $LOG; done
date -u +"end %H:%M:%S UTC" >> $LOG
(cd $SH && xargs sha256sum < ~/lean/signs-dry.files) > ~/lean/signs-dry.sha256.after
(cd ~/lean/signs-dry && xargs sha256sum < ~/lean/signs-dry.files) > ~/lean/signs-dry.sha256.built
echo "files: $(wc -l < ~/lean/signs-dry.files) ($(grep -c '\.lean$' ~/lean/signs-dry.files) Lean files); shared folder before = after the build: $(cmp -s ~/lean/signs-dry.sha256.before ~/lean/signs-dry.sha256.after && echo identical || echo DIFFERENT); built copy = shared: $(cmp -s ~/lean/signs-dry.sha256.before ~/lean/signs-dry.sha256.built && echo identical || echo DIFFERENT)" >> $LOG
cat $LOG
