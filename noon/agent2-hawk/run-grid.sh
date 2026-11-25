#!/bin/bash
# The grid of runs.   usage: bash run-grid.sh     (twelve at a time; about five minutes)
cd "$(dirname "$0")"
{ for m in lattice4 lattice8 sync4; do for i in $(seq 1 49); do r=$(printf "%.2f" $(echo "$i * 0.02" | bc -l)); echo "$m $r"; done; done; for r in 0.20 0.50 0.80; do echo "mixed4 $r"; done; } > grid.txt
cat grid.txt | xargs -P 12 -L 1 bash -c './hd $0 $1 200 15000 $(echo "$1 * 100 + 1000" | bc | cut -d. -f1) 10000 50 > runs/$0-$1.out'
grep -h "^R" runs/*.out | sort -k2,2 -k3,3n > results.txt; wc -l results.txt
