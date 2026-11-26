#!/bin/bash
# run_enum.sh M S : 8 processes, outputs enum_M_S.job*.out
cd "$(dirname "$0")"
M=$1; S=$2
for j in 0 1 2 3 4 5 6 7; do ./enum table_$M.txt $S $j 8 > enum_${M}_${S}.job$j.out & done
wait
