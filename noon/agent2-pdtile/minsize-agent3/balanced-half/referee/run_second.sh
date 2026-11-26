#!/bin/bash
# referee, second reading: Lemma 12, the constructions of Proposition 13, the Appendix (one core)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
: > out_lemma12.txt
for a in "2 3 3 6000 1" "2 3 4 6000 2" "2 3 5 3000 3" "3 2 2 6000 4" "3 2 3 6000 5" "3 2 4 2000 6" "2 5 3 4000 7" "2 5 4 2000 8" "5 2 2 4000 9" "5 2 3 1500 10" "3 5 2 4000 11" "3 5 3 1500 12" "2 7 3 3000 13" "7 2 2 3000 14" "5 3 2 3000 15" "3 7 2 3000 16"; do
  timeout 570 $PY ref_lemma12.py $a >> out_lemma12.txt 2>&1
done
: > out_prop13_construct.txt
for a in "2 3 6" "3 2 5" "2 5 5" "5 2 4" "3 5 4" "5 3 3" "2 7 4" "7 2 3" "3 7 3" "7 3 3" "2 11 4" "11 2 2" "5 7 2" "2 13 3"; do
  timeout 570 $PY ref_prop13_construct.py $a >> out_prop13_construct.txt 2>&1
done
: > out_appendix.txt
timeout 570 $PY ref_appendix.py lemmaT 1 >> out_appendix.txt 2>&1
timeout 570 $PY ref_appendix.py lemmaT 2 >> out_appendix.txt 2>&1
timeout 570 $PY ref_appendix.py exhaustive >> out_appendix.txt 2>&1
timeout 570 $PY ref_appendix.py random 1 >> out_appendix.txt 2>&1
echo done > run_second.done
