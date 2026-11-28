#!/bin/bash
# structured random runs, one after the other (one process)
cd "$(dirname "$0")"
run() { timeout 595 nice -n 15 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python test_theorem.py "$@" 2>&1 | grep -v '^$'; }
for n in 45 105 75 315 225 135 525 175; do
  for m in 8 6 7; do run rnd $n $m 40000 $((n+m)) 45; done
done
for n in 45 75 105 315 225; do
  for m in 9 10 11 12; do run rnd $n $m 20000 $((n+m)) 45; done
done
for n in 1155 945 1575; do
  for m in 6 7 8 9 10; do run rnd $n $m 20000 $((n+m)) 40; done
done
for n in 15 45 105; do
  for m in 13 14; do run rnd $n $m 20000 $((n+m)) 40; done
done
echo CHAIN B DONE
