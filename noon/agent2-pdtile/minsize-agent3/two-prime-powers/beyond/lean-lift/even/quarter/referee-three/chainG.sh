#!/bin/bash
cd "$(dirname "$0")"
py() { timeout 595 nice -n 15 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python "$@" 2>&1 | grep -v '^$'; }
for n in 21 63 105 315 189 945; do py t7.py t7 $n 8 200000 $((n+8)) 30; done
echo CHAIN G DONE
