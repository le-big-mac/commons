#!/bin/bash
# runs prove/dp_sizes (copy of the referee's dp.c with a size dump) for a list of groups; 5 threads
cd /home/agent3/minsize/prove
export OMP_NUM_THREADS=5
for a in "$@"; do
  set -- $a
  tag="p$1-q$2-n$3-S$4"
  echo "$(date -u +%H:%M:%S) start $tag"
  ./dp_sizes $1 $2 $3 $4 $4 multi 1 dpout/sizes-$tag.txt > dpout/roots-$tag.txt 2> dpout/log-$tag.txt
  rc=$?
  echo "$(date -u +%H:%M:%S) done $tag rc=$rc"
done
