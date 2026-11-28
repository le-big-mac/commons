#!/bin/bash
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
export OMP_NUM_THREADS=1
for n in 45 225 315 675; do
  $PY r_search.py $n 6 20 150 1; $PY r_search.py $n 6 20 150 2 pairs
  $PY r_search.py $n 8 20 150 3; $PY r_search.py $n 8 20 150 4 pairs
  $PY r_search.py $n 10 12 150 5; $PY r_search.py $n 10 15 150 6 pairs
  $PY r_search.py $n 12 8 120 7 pairs
done
$PY r_search.py 1575 10 10 150 8 pairs; $PY r_search.py 1575 12 6 120 9 pairs; $PY r_search.py 105 9 12 150 10; $PY r_search.py 315 11 8 120 11
echo done-search
