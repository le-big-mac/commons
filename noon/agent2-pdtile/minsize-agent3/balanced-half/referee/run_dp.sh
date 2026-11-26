#!/bin/bash
# referee: recursion over the tree (own C code) + checks, one after another (one core)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
run() {  # p q n B Bfull [dump smax]
  tag="$1_$2_$3"
  ( time ./ref_dp $1 $2 $3 $4 $5 dp_$tag.bin ) > out_dp_$tag.txt 2>&1
  $PY ref_dp_check.py $1 $2 $3 $4 $5 dp_$tag.bin $6 $7 >> out_dp_$tag.txt 2>&1
  rm -f dp_$tag.bin
}
run 2 3 2 24 24 dump_2_3_2.npy 15
run 3 2 2 30 30 dump_3_2_2.npy 10
run 2 3 3 40 40 dump_2_3_3.npy 8
run 3 2 3 60 60
run 5 2 2 30 30
run 5 3 2 20 20
run 7 2 2 20 20
run 2 5 2 30 30
run 3 5 2 20 20
run 2 3 4 72 50
run 3 2 4 60 60
run 2 5 3 30 30
echo done > run_dp.done
