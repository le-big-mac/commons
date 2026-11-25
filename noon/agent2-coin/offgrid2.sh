#!/bin/sh
# offgrid2.sh: more ranges, after the referee: the near-tie at ten ranges; no coin of 1 for two coins at 1000 and four at 200.
cd /home/agent2/coin
for L in 60 75 150 300 400; do
  ./search plain 4 $L $((L-1)) > runs/offgrid/plain-4-$L.out
  ./search both 3 $L 150 > runs/offgrid/both-3-$L.out
done
./search both 2 1000 150 > runs/offgrid/both-2-1000.out
./search both 4 200 80 > runs/offgrid/both-4-200.out
echo done
