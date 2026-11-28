#!/bin/bash
cd "$(dirname "$0")"
py() { timeout 595 nice -n 15 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python "$@" 2>&1 | grep -v '^$'; }
py examples2.py
py ex45.py ex 45 8 0 1 400 c
py ex45.py ex 45 8 0 1 400 a
py ex45.py ex 45 8 0 1 400 b
echo CHAIN F DONE
for n in 15 45 105; do for m in 13 14; do py test_theorem.py rnd $n $m 20000 $((n+m)) 30; done; done
for n in 1155 945 1575; do for m in 8 10 7; do py test_theorem.py rnd $n $m 20000 $((n+m)) 25; done; done
echo CHAIN F REALLY DONE
