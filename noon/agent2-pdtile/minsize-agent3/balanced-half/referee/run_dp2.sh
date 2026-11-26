#!/bin/bash
# referee: larger runs of the recursion (one core; each cut off at 9.5 minutes)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/prove/referee
run() {  # p q n B Bfull
  tag="$1_$2_$3_B$4"
  ( time timeout 570 ./ref_dp $1 $2 $3 $4 $5 dp_$tag.bin ) > out_dp_$tag.txt 2>&1
  if [ $? -eq 0 ]; then timeout 570 $PY ref_dp_check.py $1 $2 $3 $4 $5 dp_$tag.bin >> out_dp_$tag.txt 2>&1; else echo "CUT OFF" >> out_dp_$tag.txt; fi
  rm -f dp_$tag.bin
}
run 5 2 3 50 50
run 7 2 2 40 40
run 3 2 4 165 165
run 2 5 3 40 40
echo done > run_dp2.done
