#!/bin/bash
# SEALED.  Reruns every computation quoted in sealed-derivations.md with the final upset_check.py.
# usage: ./run_all.sh      (writes out-*.txt beside itself; about a quarter of an hour on 16 cores)
cd "$(dirname "$0")" || exit 1
PY="$HOME/welch/.venv/bin/python -I"
for M in 12 18 36 72 100; do timeout 1500 $PY upset_check.py $M --time 40 > out-$M-multisets.txt 2>&1; done
for M in 12 18 36;        do timeout 600  $PY upset_check.py $M --sets --time 25 > out-$M-sets.txt 2>&1; done
timeout 600 $PY upset_check.py 36 --weak --time 25 > out-36-multisets-weak.txt 2>&1
timeout 600 $PY upset_check.py 30 --time 30 > out-30-multisets.txt 2>&1
timeout 200 $PY upset_check.py 42 --only 42 --time 90 > out-42-only42.txt 2>&1
timeout 500 $PY upset_check.py 105 --only 105 --time 400 > out-105-only105.txt 2>&1
for M in 12 18;           do timeout 300  $PY upset_check.py $M --all --time 15 > out-$M-allpatterns.txt 2>&1; done
timeout 1500 $PY upset_check.py 36 --all --time 15 > out-36-allpatterns.txt 2>&1
( $PY coset_sum.py 2 4 3 3 54 36 24 16; $PY coset_sum.py 3 4 2 3 24 36 54 81; $PY coset_sum.py 2 5 3 4 162 108 72 48 32
  $PY pattern.py 30 5 6 12 18 24 25; $PY pattern.py 30 0 15 0 10 20 0 6 12 18 24 ) > out-coset-sum.txt 2>&1
date -u +%FT%TZ > run_all.done
