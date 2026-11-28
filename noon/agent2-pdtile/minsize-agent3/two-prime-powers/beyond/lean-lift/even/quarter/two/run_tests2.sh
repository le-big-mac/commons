#!/bin/bash
# second batch: exhaustive on Z_15 with eight elements, Z_21 with six, and moduli with four primes
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { timeout 420 nice -n 15 $PY test_cells.py "$@" 2>&1 | tail -3; }
run all 21 6 0 0
run all 15 8 0 0
s=200
for n in 1155 3465; do for m in 8 10 11 12; do s=$((s+1)); run shaped $n $m 80 $s; s=$((s+1)); run random $n $m 40 $s; done; done
for n in 675 525 2835; do for m in 9 10 12; do s=$((s+1)); run shaped $n $m 80 $s; done; done
echo "BATCH2 DONE"
