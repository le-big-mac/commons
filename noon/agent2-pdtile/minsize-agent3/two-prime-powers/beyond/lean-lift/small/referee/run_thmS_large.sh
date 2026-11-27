#!/bin/bash
# one stream: multisets of 15..36 elements on two groups that none of Theorems 2, 3, 6, 7 covers
cd /home/agent3/lean/lift-check/small/referee
run() { # GROUP KIND SEED COUNT MMIN MMAX
  out=thmS_$1_$2_seed$3_sizes$5to$6.out
  timeout 590 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python ref_thmS.py "$@" > $out 2>&1
  echo "exit status $? ; seconds since the stream began $SECONDS" >> $out
}
run H caterpillar 61 25 15 36; run H product 61 30 15 36; run H fibres 61 20 15 36; run H subgroup 61 20 15 36; run H pool 61 10 15 36; run H random 61 10 15 36
run G caterpillar 62 12 15 36; run G product 62 12 15 36; run G subgroup 62 10 15 36; run G fibres 62 10 15 36
