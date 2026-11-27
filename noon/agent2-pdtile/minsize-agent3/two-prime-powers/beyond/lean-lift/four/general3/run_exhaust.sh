#!/bin/bash
# every multiset with 0 on five small groups; two processes at a time, each under the 2 GB cap
cd "$(dirname "$0")"
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
( $PY exhaust.py 9 11 > exhaust_9.out 2>&1; $PY exhaust.py 15 8 > exhaust_15.out 2>&1; $PY exhaust.py 25 6 > exhaust_25.out 2>&1 ) &
( $PY exhaust.py 27 6 > exhaust_27.out 2>&1; $PY exhaust.py 45 5 > exhaust_45.out 2>&1 ) &
wait
