#!/bin/bash
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
export OMP_NUM_THREADS=1
for m in 3 4 5 6; do $PY r_brute.py lemexh 9 $m l4; done
for m in 3 4 5 6; do $PY r_brute.py lemexh 15 $m l4; done
for m in 3 4; do $PY r_brute.py lemexh 21 $m l4; $PY r_brute.py lemexh 27 $m l4; done
$PY r_brute.py lemexh 45 3 l4
$PY r_brute.py lemexh 105 3 l4
for m in 6 8 10 7 9 12 11; do
  for n in 45 105 225 315 675 75 135 525 945 1155 3465; do
    if [ $m -le 9 ]; then $PY r_brute.py lem $n $m 100 $((n+m)) l4; else $PY r_brute.py lem $n $m 60 $((n+m)); fi
  done
done
echo done-lem
