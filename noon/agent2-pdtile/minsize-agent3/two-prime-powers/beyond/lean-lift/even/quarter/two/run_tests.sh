#!/bin/bash
# all tests of the lemmas, one process, each run bounded
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { timeout 170 nice -n 15 $PY test_cells.py "$@" 2>&1 | tail -3; }
for m in 3 4 5 6 7; do run all 15 $m 0 0; done
for m in 3 4 5 6; do run all 9 $m 0 0; done
for m in 4 5; do run all 45 $m 0 0; done
run all 21 5 0 0
run all 27 5 0 0
s=10
for n in 15 45 75 105 135 225 315 945; do
  for m in 6 7 8 9 10; do
    s=$((s+1)); run shaped $n $m 300 $s
    s=$((s+1)); run random $n $m 150 $s
  done
done
for n in 45 105 315; do for m in 11 12; do s=$((s+1)); run shaped $n $m 60 $s; done; done
echo "BATCH DONE"
