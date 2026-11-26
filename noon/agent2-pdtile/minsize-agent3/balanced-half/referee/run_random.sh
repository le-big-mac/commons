#!/bin/bash
# referee: random structured multisets in larger groups (one core; each run cut off at 9 minutes)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
: > out_random.txt
while read p q n np seed; do
  timeout 540 $PY ref_random.py $p $q $n $np $seed 2>&1 | grep -v "^  level" >> out_random.txt
done <<LIST
2 3 5 200000 1
2 3 5 200000 2
2 3 6 100000 1
3 2 4 100000 1
3 2 5 30000 1
2 5 4 100000 1
2 7 3 100000 1
2 7 4 50000 1
3 5 3 60000 1
5 2 3 40000 1
5 3 2 100000 1
3 7 2 100000 1
7 2 2 100000 1
7 3 2 50000 1
2 11 3 50000 1
2 13 2 100000 1
LIST
echo done > run_random.done
