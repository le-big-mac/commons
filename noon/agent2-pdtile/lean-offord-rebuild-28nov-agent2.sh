#!/bin/bash
# A rebuild from nothing, by agent2 (Noon), 28 November 2026, of a PRIVATE copy of the joint Lean library with Yonder's two files of
# Erdős's bound and what follows from it (Offord.lean, OffordBad.lean: seven statements) added to the copy only.   usage: bash rebuild-offord.sh NEWDIR     (NEWDIR must not exist; nothing in the shared folder is written)
# The copy: every Lean and configuration file of the shared lean-tiling folder; the two finished files from the joint folder's offord-lean/
# (checked against its SHA256-finished) into Pnq/; two import lines at the end of Pnq.lean; seven "#print axioms" lines at the end of
# CheckPnq.lean.  Mathlib's built files are shared from my working copy.  One warning of lake's, which in Yonder's run was printed fifty-one
# million times and made a log of 8.6 GB, is counted and not kept.
set -u
SRC=/srv/commons/agent2-pdtile/lean-tiling; EV=/srv/commons/agent2-pdtile/minsize-agent3/two-prime-powers/beyond/lean-lift/offord-lean; NEW="$1"
FILES="Offord OffordBad"
NAMES="card_signedSum_eq_le_real card_signedSum_eq_le_complex card_badAt_le_choose not_badAt_one_of_odd card_exists_badAt_two_pow_le not_exists_badAt_two_pow_of_odd card_exists_badAt_le_divisors"
[ -e "$NEW" ] && { echo "the folder exists already: $NEW"; exit 1; }
( cd "$EV" && sha256sum -c SHA256-finished > /dev/null 2>&1 ) || { echo "the two files are not those of SHA256-finished: stopping"; exit 1; }
mkdir -p "$NEW" && cd "$NEW" || exit 1
( cd "$SRC" && find . -type f \( -name "*.lean" -o -name "lakefile*" -o -name "lake-manifest.json" -o -name "lean-toolchain" \) | sort ) > files.list
( cd "$SRC" && xargs -d '\n' sha256sum < "$NEW/files.list" ) > shared.before.sha
while IFS= read -r f; do mkdir -p "$(dirname "$f")"; cp "$SRC/$f" "$f"; done < files.list
xargs -d '\n' sha256sum < files.list > copy.sha
for f in $FILES; do [ -e "Pnq/$f.lean" ] && { echo "Pnq/$f.lean is in the shared folder already: stopping"; exit 1; }; cp "$EV/$f.lean" "Pnq/$f.lean"; printf 'import Pnq.%s\n' "$f" >> Pnq.lean; done
for n in $NAMES; do printf '#print axioms Pnq.%s\n' "$n" >> CheckPnq.lean; done
( cd Pnq && sha256sum $(for f in $FILES; do echo $f.lean; done) ) > added.sha
mkdir -p .lake && ln -s /home/agent2/lean/pqr/.lake/packages .lake/packages
cmp -s lake-manifest.json /home/agent2/lean/pqr/lake-manifest.json && echo "manifest: the same as my working copy's" > manifest.note || echo "manifest: DIFFERS from my working copy's" > manifest.note
date -u +%H:%M:%S > build.start
nice -n 15 lake build 2>&1 | awk '/designed for use with the module system/ { c++; next } { print } END { print "LINES OF THE ONE WARNING LEFT OUT: " c+0 }' > build.log; echo "lake build exit ${PIPESTATUS[0]}" > build.exit
date -u +%H:%M:%S > build.end
for f in Check CheckPnq CheckP2q2; do nice -n 15 lake env lean $f.lean 2>&1 | awk '/designed for use with the module system/ { next } { print }' > $(echo $f | tr 'A-Z' 'a-z').out; echo "$f exit ${PIPESTATUS[0]}" >> build.exit; done
( cd "$SRC" && xargs -d '\n' sha256sum < "$NEW/files.list" ) > shared.after.sha
echo "files taken from the shared folder: $(wc -l < files.list) ($(grep -c '\.lean$' files.list) Lean files); added in the copy only: 2 files, $(cat $(for f in $FILES; do echo Pnq/$f.lean; done) | wc -l) lines"
cmp -s shared.before.sha shared.after.sha && echo "shared folder before = after the build: identical" || echo "shared folder CHANGED during the build"
( cd "$EV" && sha256sum $(for f in $FILES; do echo $f.lean; done) ) | cmp -s - added.sha && echo "the two files in the copy = those in offord-lean/: identical" || echo "the two files in the copy DIFFER from offord-lean/"
cat manifest.note build.exit; echo "build $(cat build.start) to $(cat build.end) UTC"
grep -c '\] Built ' build.log | sed 's/^/modules built: /'; grep "LINES OF THE ONE WARNING" build.log; grep -v "LINES OF THE ONE WARNING" build.log | tail -1; echo "the word error in build.log: $(grep -ci 'error' build.log) times; the word sorry: $(grep -c 'sorry' build.log) times; size of build.log: $(wc -c < build.log) bytes"
for f in check.out checkpnq.out checkp2q2.out; do echo "$f: $(grep -c 'depends on axioms' $f) axiom lines, $(grep -c 'depends on axioms: \[propext, Classical.choice, Quot.sound\]$' $f) with exactly the standard three"; done
for n in $NAMES; do grep -A0 "Pnq.$n' depends on axioms" checkpnq.out | cut -c1-120; done
echo "sorry / native_decide / a line beginning axiom in Pqr/ Pnq/ P2q2/ and the root files: $(grep -rnE '\bsorry\b|native_decide|^axiom ' --include='*.lean' . | grep -v '^./.lake' | wc -l) matches"
echo "lines of Lean in Pqr/ Pnq/ P2q2/: $(cat Pqr/*.lean Pnq/*.lean P2q2/*.lean | wc -l)"
