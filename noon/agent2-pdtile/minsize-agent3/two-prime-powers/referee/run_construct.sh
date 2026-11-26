#!/bin/bash
# the construction of the sets proposition and other shifts, on larger groups; 6 processes
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
cat > out/construct-list.txt <<'L'
2 2 3 2 2 50 all
2 3 3 2 2 50 all
2 2 3 3 2 50 all
2 3 3 3 3 30 all
2 3 3 3 4 30 all
2 4 3 3 4 20 all
3 3 2 4 4 20 all
2 3 3 4 4 20 all
2 4 3 4 5 10 all
2 4 3 4 4 10
3 4 2 4 4 10
2 5 3 5 4 5
3 4 5 3 4 5
5 3 2 4 4 5
5 4 3 4 4 2
2 6 3 4 4 5
7 3 2 5 4 3
3 2 5 2 2 50 all
5 3 7 3 4 5 all
3 3 5 3 4 5 all
L
cat out/construct-list.txt | xargs -P 6 -L 1 sh -c 'nice -n 10 ~/welch/.venv/bin/python construct.py "$@" >> out/construct.jsonl 2>> out/construct.err' sh
echo done > out/construct.done
