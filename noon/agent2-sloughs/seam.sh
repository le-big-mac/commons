#!/bin/bash
# How many of the cutoffs in the ten cases of ruler.py removed a loop that lay across the seam of the valley (the other branch of the
# cutoff code)?  A build of river.c with -DCOUNTSEAM says so on each.   usage: ./seam.sh > seam.out
cd "$(dirname "$0")"; gcc -O2 -DCOUNTSEAM -o river-seam river.c -lm
total=0; seam=0
while read P DC LX T seed F; do
  tag="P$P-dc$DC-L$LX-s$seed"; [ -n "$F" ] && tag="$tag-f$F"
  n=$(./river-seam $P $DC $LX $T $seed -start out/ruler/$tag.start -out 1 ${F:+-f $F} 2>&1 >/dev/null | grep -c "across the seam")
  c=$(./river $P $DC $LX $T $seed -start out/ruler/$tag.start -out 1 ${F:+-f $F} | tail -1 | awk '{print $4}')
  echo "$tag: $c cutoffs, $n of them across the seam"; total=$((total + c)); seam=$((seam + n))
done <<CASES
3 0.4 40 30 7
3 0.2 40 26 8
3 0.8 40 26 9
2 0.4 40 80 10
2 0.8 40 80 11
4.5 0.4 30 13 12
6 0.2 30 8 13
6 0.8 30 8 14
3 0.4 40 30 15 0.1
6 0.4 30 10 16 0.5
CASES
echo "in all: $total cutoffs, $seam across the seam"
