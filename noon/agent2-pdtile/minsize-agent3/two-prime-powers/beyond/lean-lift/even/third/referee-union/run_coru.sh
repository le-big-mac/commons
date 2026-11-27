#!/bin/bash
# Referee's driver: Corollary U runs, one process after another, each bounded by its own time limit.
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { nice -n 15 $PY coru.py "$@" ; }
{
for m in 1 2 3 4 5 6 7 8; do run 2 $m all 60; done
for m in 1 2 3 4 5 6 7; do run 4 $m all 60; done
for m in 1 2 3 4 5 6; do run 6 $m all 60; done
for m in 1 2 3 4 5 6; do run 8 $m all 60; done
for m in 1 2 3 4 5; do run 10 $m all 60; done
for m in 1 2 3 4 5; do run 12 $m all 60; done
for m in 2 3 4; do run 16 $m all 60; done
for m in 2 3 4; do run 18 $m all 60; done
for m in 2 3 4; do run 20 $m all 60; done
for m in 2 3 4; do run 24 $m all 60; done
} > coru-all.out 2>&1
{
for m in 7 8 9; do run 8 $m zero 60; done
for m in 6 7 8; do run 12 $m zero 60; done
for m in 5 6; do run 14 $m zero 60; done
for m in 5 6 7; do run 16 $m zero 90; done
for m in 5 6; do run 20 $m zero 60; done
for m in 5 6; do run 24 $m zero 90; done
run 28 5 zero 60
for m in 4 5; do run 32 $m zero 60; done
for m in 2 3 4 5; do run 30 $m zero 60; done
for m in 4 5; do run 36 $m zero 90; done
for m in 4 5; do run 40 $m zero 90; done
for m in 4 5; do run 42 $m zero 90; done
run 48 4 zero 60
for m in 3 4; do run 60 $m zero 60; done
run 70 4 zero 60
run 72 4 zero 60
for m in 3 4; do run 120 $m zero 150; done
run 210 3 zero 60
run 30 6 zero 150
} > coru-zero.out 2>&1
echo done > coru-done.flag
