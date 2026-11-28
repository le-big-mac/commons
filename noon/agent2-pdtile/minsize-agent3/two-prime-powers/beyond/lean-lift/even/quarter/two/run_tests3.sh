#!/bin/bash
# third batch: 13 to 16 elements (exact U_p(m) from ptree.py), shaped multisets
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { timeout 110 nice -n 15 $PY test_cells.py "$@" 2>&1 | tail -3; }
s=300
for n in 45 105 225; do for m in 13 14 15 16; do s=$((s+1)); run shaped $n $m 25 $s; done; done
for m in 13 14; do s=$((s+1)); run shaped 315 $m 20 $s; s=$((s+1)); run random 45 $m 20 $s; done
echo "BATCH3 DONE"
