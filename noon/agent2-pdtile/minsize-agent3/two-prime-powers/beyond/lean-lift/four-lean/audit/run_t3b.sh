#!/bin/bash
# A1 / exists_signs_odd: deeper exhaustive searches, one after the other (one process at a time).
# usage: bash run_t3b.sh OUTFILE
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t3_a1.py"
out="$1"
: > "$out"
while read n mmin mmax; do
  $P $n $mmin $mmax >> "$out" 2>&1
done <<LIST
9 17 22
15 13 14
21 11 11
27 10 10
45 8 8
63 7 7
105 6 6
165 5 5
195 5 5
525 4 4
3465 3 3
LIST
echo finished >> "$out"
