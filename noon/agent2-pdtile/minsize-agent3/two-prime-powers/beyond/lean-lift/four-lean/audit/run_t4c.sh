#!/bin/bash
# exists_lift_two_all: two deeper searches for N whose odd part has three primes.
# usage: bash run_t4c.sh OUTFILE
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t4_lift.py"
out="$1"
: > "$out"
$P 105 6 6 >> "$out" 2>&1
$P 210 5 5 >> "$out" 2>&1
echo finished >> "$out"
