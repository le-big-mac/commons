#!/bin/bash
# local search for multisets with few good signings; two processes at a time, each under the 2 GB cap
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
( for a in "45 6 30 300 1" "45 8 30 300 2" "45 10 30 300 3" "45 12 20 300 4" "135 10 20 300 5" "135 12 20 300 6" "135 14 10 200 7" "9 12 20 300 15" "27 12 20 300 16"; do $PY adversary.py $a; done > adv_a.out 2>&1 ) &
( for a in "225 10 20 300 8" "225 12 20 300 9" "225 14 10 200 10" "315 10 20 300 11" "315 12 20 300 12" "315 14 10 200 13" "675 14 6 150 14" "105 12 20 300 17" "15 12 20 300 18"; do $PY adversary.py $a; done > adv_b.out 2>&1 ) &
wait
