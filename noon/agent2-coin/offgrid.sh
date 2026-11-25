#!/bin/sh
# offgrid.sh: the comparison "three coins both ways against four one way" at other ranges of amounts.
cd /home/agent2/coin
for L in 50 200 500; do
  M=$((L-1))
  ./search plain 3 $L $M > runs/offgrid/plain-3-$L.out
  ./search plain 4 $L $M > runs/offgrid/plain-4-$L.out
done
./search plain 5 50 49 > runs/offgrid/plain-5-50.out
./search plain 5 200 199 > runs/offgrid/plain-5-200.out
./search both 2 50 150 > runs/offgrid/both-2-50.out
./search both 2 200 400 > runs/offgrid/both-2-200.out
./search both 2 500 1000 > runs/offgrid/both-2-500.out
./search both 3 50 150 > runs/offgrid/both-3-50.out
./search both 3 200 300 > runs/offgrid/both-3-200.out
./search both 4 50 100 > runs/offgrid/both-4-50.out
seq 1 598 | xargs -P 10 -I{} sh -c './search both 3 500 600 {} > runs/both3-500/first-{}.out'
echo done
