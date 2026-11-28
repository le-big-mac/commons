#!/bin/bash
# The tests of result.md, two streams at a time, each run under the 2 GB cap, niced, bounded to ten minutes.
cd /home/agent3/lean/lift-check/even/root/one
PY="nice -n 15 timeout 600 bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python test_lemmas.py"
stream_a() {
  for m in 3 4 5 6 7; do $PY exhaustive 9 $m; done
  for m in 3 4 5 6; do $PY exhaustive 15 $m; done
  for m in 3 4 5; do $PY exhaustive 27 $m; done
  for m in 3 4 5; do $PY exhaustive 21 $m; done
  for m in 3 4; do $PY exhaustive 45 $m; done
  for n in 15 45 105 135 225 315; do for m in 6 7 8 9 10 11 12; do $PY random $n $m 150 $((n + m)); done; done
}
stream_b() {
  for n in 9 15 27 45 75 81 105 135 225 243 315 525 675 1155; do $PY shaped $n 1500 $((7 * n + 1)); done
  for n in 27 81 243 45 135 405; do $PY shaped $n 1500 $((11 * n + 5)); done
}
stream_a > tests_a.out 2>&1 &
stream_b > tests_b.out 2>&1 &
wait
