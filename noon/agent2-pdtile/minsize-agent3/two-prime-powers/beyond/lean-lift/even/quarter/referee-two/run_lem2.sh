#!/bin/bash
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
export OMP_NUM_THREADS=1
for m in 13 14; do for n in 45 105 225 315 675 1575; do $PY r_brute.py lem $n $m 30 $((n+m)); done; done
for m in 10 12; do for n in 225 675 1575 2025 3375; do $PY r_brute.py lem $n $m 300 $((7*n+m)); done; done
for m in 15 16; do for n in 45 105 225 315; do $PY r_brute.py lem $n $m 10 $((n+m)); done; done
echo done-lem2
