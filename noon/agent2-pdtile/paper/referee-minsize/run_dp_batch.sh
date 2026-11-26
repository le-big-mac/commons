#!/bin/bash
# runs dp.c for a list of cases, at most 8 at a time, each under a 9-minute limit
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
printf '%s\n' "3 2 3 60" "5 2 2 60" "3 2 4 162" "5 3 2 75" "3 5 2 20" "2 7 2 14" "2 5 3 30" "5 2 3 250" "3 5 1 30" "5 3 1 30" "2 7 1 28" "7 2 1 28" "7 2 2 98" "2 3 4 72" |
xargs -P 8 -I{} bash -c 'set -- {}; f=dpout/dp-$1-$2-$3-B$4.txt; s=$(date +%s); timeout 540 ./dp $1 $2 $3 $4 > $f.tmp 2> dpout/dp-$1-$2-$3-B$4.err; rc=$?; e=$(date +%s); if [ $rc -eq 0 ]; then mv $f.tmp $f; else rm -f $f.tmp; fi; echo "$1 $2 $3 $4 rc=$rc seconds=$((e-s))"'
