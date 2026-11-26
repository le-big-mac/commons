#!/bin/bash
# referee: more literal brute force (other primes, n = 4, p = 3 with n = 3) and comparison of the recursion with it
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
REF_DUMP=dump_5_2_2.npy timeout 570 $PY ref_brute.py all 5 2 2 5 > out_brute_all_5_2_2.txt 2>&1
REF_DUMP=dump_2_5_2.npy timeout 570 $PY ref_brute.py all 2 5 2 8 > out_brute_all_2_5_2.txt 2>&1
REF_DUMP=dump_3_2_3.npy timeout 570 $PY ref_brute.py all 3 2 3 5 > out_brute_all_3_2_3.txt 2>&1
REF_DUMP=dump_2_3_4.npy timeout 570 $PY ref_brute.py all 2 3 4 6 > out_brute_all_2_3_4.txt 2>&1
timeout 570 $PY ref_brute.py all 3 5 2 5 > out_brute_all_3_5_2.txt 2>&1
timeout 570 $PY ref_brute.py all 2 7 2 7 > out_brute_all_2_7_2.txt 2>&1
timeout 570 $PY ref_brute.py bal 2 5 2 3 > out_brute_bal_2_5_2.txt 2>&1
timeout 570 $PY ref_brute.py bal 2 7 2 2 > out_brute_bal_2_7_2.txt 2>&1
cmp() {  # p q n B smax
  ./ref_dp $1 $2 $3 $4 $4 dp_cmp.bin 2> /dev/null
  $PY ref_dp_check.py $1 $2 $3 $4 $4 dp_cmp.bin dump_$1_$2_$3.npy $5 | grep "comparison" | sed "s/^/p=$1 q=$2 n=$3:/"
  rm -f dp_cmp.bin
}
: > out_dp_vs_brute.txt
cmp 2 3 2 16 15 >> out_dp_vs_brute.txt
cmp 3 2 2 12 10 >> out_dp_vs_brute.txt
cmp 2 3 3 10 8 >> out_dp_vs_brute.txt
cmp 5 2 2 8 5 >> out_dp_vs_brute.txt
cmp 2 5 2 10 8 >> out_dp_vs_brute.txt
cmp 3 2 3 8 5 >> out_dp_vs_brute.txt
cmp 2 3 4 8 6 >> out_dp_vs_brute.txt
echo done > run_brute3.done
