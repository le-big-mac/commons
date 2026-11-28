#!/bin/bash
# exhaustive runs, one after the other (one process)
cd "$(dirname "$0")"
run() { timeout 595 nice -n 15 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python test_theorem.py "$@" 2>&1 | grep -v '^$'; }
for m in 3 4 5 6 7 8 9 10; do run ex 9 $m 0 1 200; done
for m in 3 4 5 6 7 8; do run ex 15 $m 0 1 200; done
for m in 3 4 5 6 7; do run ex 21 $m 0 1 200; done
for m in 3 4 5 6; do run ex 27 $m 0 1 200; done
for m in 5 6 7; do run ex 25 $m 0 1 200; done
for m in 3 4 5 6; do run ex 35 $m 0 1 200; done
for m in 3 4 5 6; do run ex 45 $m 0 1 300; done
for m in 3 4 5; do run ex 63 $m 0 1 200; done
for m in 3 4 5; do run ex 75 $m 0 1 200; done
for m in 3 4 5; do run ex 105 $m 0 1 200; done
run ex 15 9 0 1 400
run ex 21 8 0 1 400
run ex 27 7 0 1 400
echo CHAIN A DONE
