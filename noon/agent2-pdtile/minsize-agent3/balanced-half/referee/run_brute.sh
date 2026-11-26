#!/bin/bash
# referee: the literal brute-force runs, one after another (one core)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
REF_DUMP=dump_3_2_2.npy $PY ref_brute.py all 3 2 2 10 > out_brute_all_3_2_2_dump.txt 2>&1
REF_DUMP=dump_2_3_3.npy $PY ref_brute.py all 2 3 3 8 > out_brute_all_2_3_3_dump.txt 2>&1
$PY ref_brute.py all 2 3 2 18 > out_brute_all_2_3_2.txt 2>&1
$PY ref_brute.py all 3 2 2 12 > out_brute_all_3_2_2.txt 2>&1
$PY ref_brute.py all 2 3 3 9 > out_brute_all_2_3_3.txt 2>&1
$PY ref_brute.py bal 2 3 2 8 > out_brute_bal_2_3_2.txt 2>&1
$PY ref_brute.py bal 3 2 2 7 > out_brute_bal_3_2_2.txt 2>&1
$PY ref_brute.py bal 2 3 3 4 > out_brute_bal_2_3_3.txt 2>&1
echo done > run_brute.done
