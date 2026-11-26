#!/bin/bash
# undecided patterns of Z_100 with two or three sizes left to exclude; two processes of two threads; 90 s for one size
cd /home/agent3/pq2/referee/two-powers/second
export OMP_NUM_THREADS=1
cat > out/sizes-list.txt <<'L'
100 60 90 2 2,4,5,100 20
100 150 90 2 2,5,20,25,50 50
100 70 90 2 2,5,50,100 50
100 100 90 2 2,4,5,50,100 60
100 24 90 2 2,4,20,50 12
L
cat out/sizes-list.txt | xargs -P 2 -L 1 sh -c 'nice -n 10 ~/welch/.venv/bin/python -B cpsat_sizes.py "$@" > "out/sizes-$5.jsonl" 2>> out/sizes.err' sh
echo done > out/sizes.done
