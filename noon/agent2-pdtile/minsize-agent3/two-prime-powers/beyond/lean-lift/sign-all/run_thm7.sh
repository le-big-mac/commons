#!/bin/bash
# run_thm7.sh stream -- the end-to-end runs of thm7_check.py; writes thm7_<stream>.out here.
cd "$(dirname "$0")" || exit 1
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
case "$1" in
a) : > thm7_a.out
   $PY thm7_check.py 135 7 1 300 1 >> thm7_a.out 2>&1
   $PY thm7_check.py 225 7 1 300 2 >> thm7_a.out 2>&1
   $PY thm7_check.py 675 7 1 200 3 >> thm7_a.out 2>&1
   $PY thm7_check.py 675 0 0 300 4 >> thm7_a.out 2>&1 ;;
b) : > thm7_b.out
   $PY thm7_check.py 189 5 2 200 5 >> thm7_b.out 2>&1
   $PY thm7_check.py 1323 5 1 200 6 >> thm7_b.out 2>&1
   $PY thm7_check.py 4725 11 0 200 7 >> thm7_b.out 2>&1
   $PY thm7_check.py 2025 7 1 100 8 >> thm7_b.out 2>&1 ;;
esac
