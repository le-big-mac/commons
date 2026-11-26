#!/bin/bash
# referee: the constructions of section 6, from the words, for many (p, q) (one core)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
: > out_construct.txt
while read p q n dv; do
  $PY ref_construct.py $p $q $n $dv >> out_construct.txt 2>&1
done <<LIST
2 3 6 100
3 2 5 170
2 5 5 170
5 2 4 260
3 5 4 140
5 3 4 80
2 7 4 120
7 2 4 100
3 7 4 70
7 3 3 0
5 7 3 0
7 5 3 0
2 11 4 90
11 2 3 30
2 13 4 110
13 2 2 30
3 11 3 40
11 3 2 40
2 17 3 70
17 2 2 40
3 13 3 40
2 19 3 80
LIST
echo done > run_construct.done
