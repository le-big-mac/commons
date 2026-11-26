#!/bin/bash
# referee, second reading: Proposition 13 by literal brute force and by the extended recursion (one core)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
# literal brute force (also dumps the least fibre depth per root state)
timeout 570 $PY ref_brute13.py bal 2 3 2 8 dump13_bal_2_3_2.npy > out_brute13_bal_2_3_2.txt 2>&1
timeout 570 $PY ref_brute13.py bal 3 2 2 6 dump13_bal_3_2_2.npy > out_brute13_bal_3_2_2.txt 2>&1
timeout 570 $PY ref_brute13.py bal 2 3 3 4 dump13_bal_2_3_3.npy > out_brute13_bal_2_3_3.txt 2>&1
timeout 570 $PY ref_brute13.py all 2 3 3 8 dump13_all_2_3_3.npy > out_brute13_all_2_3_3.txt 2>&1
timeout 570 $PY ref_brute13.py all 3 2 2 9 dump13_all_3_2_2.npy > out_brute13_all_3_2_2.txt 2>&1
timeout 570 $PY ref_brute13.py bal 2 5 2 3 dump13_bal_2_5_2.npy > out_brute13_bal_2_5_2.txt 2>&1
timeout 570 $PY ref_brute13.py bal 2 7 2 2 dump13_bal_2_7_2.npy > out_brute13_bal_2_7_2.txt 2>&1
: > out_p13_dp.txt
run() {  # p q n B topall [dump B mode]
  ( time timeout 570 ./ref_dp13 $1 $2 $3 $4 $5 dp13.bin ) 2>&1 | grep "real\|states" | tr '\n' ' ' >> out_p13_dp.txt; echo >> out_p13_dp.txt
  $PY ref_p13_check.py $1 $2 $3 $4 dp13.bin $6 $7 $8 >> out_p13_dp.txt 2>&1
  rm -f dp13.bin
}
run 2 3 2 24 0 dump13_bal_2_3_2.npy 24 bal
run 3 2 2 18 0 dump13_bal_3_2_2.npy 12 bal
run 2 3 3 24 0 dump13_bal_2_3_3.npy 12 bal
run 2 3 3 10 1 dump13_all_2_3_3.npy 8 all
run 3 2 2 12 1 dump13_all_3_2_2.npy 9 all
run 2 5 2 20 0 dump13_bal_2_5_2.npy 15 bal
run 3 2 3 54 0
run 2 3 4 48 0
run 3 2 4 54 0
run 5 2 2 14 0
run 5 3 2 15 0
run 3 5 2 15 0
run 7 2 2 14 0
run 2 5 3 24 0
echo done > run_p13.done
