#!/bin/bash
# A third batch, after T8 was added (the first text's two results on powers of 3): two streams, as run_tests.sh.
cd /home/agent3/lean/lift-check/even/root/one
PY="nice -n 15 timeout 600 bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python test_lemmas.py"
( for m in 5 6 7; do $PY exhaustive 9 $m; done; $PY exhaustive 27 5; $PY exhaustive 15 6
  for n in 45 135 315; do for m in 9 10 11 12; do $PY random $n $m 150 $((1000 + n + m)); done; done ) > tests_c1.out 2>&1 &
( for n in 9 27 81 243 45 135 405 675; do $PY shaped $n 1500 $((13 * n + 3)); done ) > tests_c2.out 2>&1 &
wait
