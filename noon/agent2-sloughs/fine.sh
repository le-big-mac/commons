#!/bin/bash
# The base case at half the node spacing (0.05), two seeds: the second priced check of the sealed sheet.
# Each run needs about 130 minutes, and a background command on this machine is stopped after two hours: these two were stopped
# at t = 1392 and t = 1370 of 1492.8 and were not taken up again.  Their output is out/fine/ds05-s1.out and ds05-s2.out;
# analyse.py is given the time up to which both exist (python analyse.py out/fine 1370).
# usage: ./fine.sh
cd "$(dirname "$0")"; mkdir -p out/fine; export OMP_NUM_THREADS=1
for seed in 1 2; do nice -n 15 ./river 3 0.4 200 1492.8 $seed -out 1 -ds 0.05 > out/fine/ds05-s$seed.out & done; wait
