#!/bin/bash
# sizes_eq_mul_all: censuses of Z_N and Z_{Ns}, one N after the other (one process at a time).
# usage: bash run_t6.sh OUTFILE
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t6_mul.py"
out="$1"
: > "$out"
for N in 1 2 3 4 5 6 7 8 9 10 12 15 16 18 20 21 24 25 27 30 36 45 60 105; do
  $P 2e9 $N 4,6,8,12 >> "$out" 2>&1
done
# other factors: s = 1 (the same group), s = 2, odd s, and further even s
$P 2e9 1,6,12,30,36 1,2,3,5,9 >> "$out" 2>&1
$P 2e9 3,6,9,12,30,36 10,16,18,24 >> "$out" 2>&1
$P 2e9 210 4 >> "$out" 2>&1
# deeper, N outside the earlier theorems
$P 2e10 30 4,6,8,12 >> "$out" 2>&1
$P 2e10 36 4,6 >> "$out" 2>&1
$P 3e10 105 4 >> "$out" 2>&1
echo finished >> "$out"
