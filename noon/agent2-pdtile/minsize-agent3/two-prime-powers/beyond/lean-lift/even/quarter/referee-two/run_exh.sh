#!/bin/bash
# exhaustive (or sampled) theorem tests; one process; bounded by the caller's timeout
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
export OMP_NUM_THREADS=1
for m in 3 4 5 6 7 8 9; do $PY r_brute.py exh 9 $m; done
for m in 3 4 5 6 7 8; do $PY r_brute.py exh 15 $m; done
for m in 3 4 5 6; do $PY r_brute.py exh 27 $m; done
for m in 3 4 5 6; do $PY r_brute.py exh 21 $m; done
for m in 3 4 5; do $PY r_brute.py exh 45 $m; done
for m in 5 6 7; do $PY r_brute.py exh 25 $m; done
for m in 3 4; do $PY r_brute.py exh 105 $m; done
for m in 3 4; do $PY r_brute.py exh 63 $m; $PY r_brute.py exh 75 $m; done
$PY r_brute.py exh 15 9
$PY r_brute.py exh 27 7
$PY r_brute.py exh 21 7
for m in 6 7 8; do $PY r_brute.py exh 45 $m 150000; $PY r_brute.py exh 35 $m 150000; $PY r_brute.py exh 105 $m 100000; done
echo done-exh
