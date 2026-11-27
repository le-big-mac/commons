#!/bin/bash
# Theorem T': exhaustive runs, one after another (one process at a time), each bounded by a work estimate.
cd "$(dirname "$0")"
for k in 1 2 3 4; do
  for N in 2 3 4 6 0; do
    /usr/bin/time -f "  (%e s)" timeout 240 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python tprime_check.py exh $k $N 200000000 \
      > tprime-exh-k$k-N$N.out 2>&1
  done
done
echo done > tprime-exh.done
