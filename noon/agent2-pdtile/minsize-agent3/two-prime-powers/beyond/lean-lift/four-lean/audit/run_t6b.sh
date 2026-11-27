#!/bin/bash
# The lifts behind sizes_eq_mul_all for a general factor s, one N after the other (one process at a time).
# usage: bash run_t6b.sh OUTFILE
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t6b_liftmul.py"
out="$1"
: > "$out"
for N in 1 2 3 4 5 6 7 8 9 10 12 15 16 18 20 21 24 25 27 30 36 45 60 105 210 315 330 420; do
  $P 1e9 10 $N 4,6,8,12 >> "$out" 2>&1
done
$P 1e9 10 3,6,9,12,30,36,105 10,16,18,24 >> "$out" 2>&1
$P 1e9 10 6,12,30,36,105 2,3,5,9 >> "$out" 2>&1
# deeper, N outside the earlier theorems
$P 2e10 10 30 4,6,8,12 >> "$out" 2>&1
$P 2e10 10 36 4,6 >> "$out" 2>&1
$P 2e10 10 105 4,6,8,12 >> "$out" 2>&1
$P 2e10 10 210 4,6 >> "$out" 2>&1
echo finished >> "$out"
