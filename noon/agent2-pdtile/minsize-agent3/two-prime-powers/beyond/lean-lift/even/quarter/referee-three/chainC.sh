#!/bin/bash
# targeted runs (prescribed full group of 5; aligned 3-parts), one after the other (one process)
cd "$(dirname "$0")"
run() { timeout 595 nice -n 15 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python targeted.py "$@" 2>&1 | grep -v '^$'; }
for n in 45 135 225 315 675 75 1575 15 405; do run tg $n 8 400000 $((n+8)) 50; done
for n in 45 225 315 135; do run tg $n 6 200000 $((n+6)) 20; run tg $n 7 200000 $((n+7)) 20; done
for n in 15 45 75 225; do run tg $n 10 100000 $((n+10)) 30 2,2,2,2,2,0; done
for n in 25 75 225; do run tg $n 12 100000 $((n+12)) 40 2,2,2,2,2,2; done
for n in 15 45 75 225; do run tg $n 12 100000 $((n+12)) 40 4,2,2,2,2,0; run tg $n 12 100000 $((n+13)) 40 3,3,2,2,2,0; done
for n in 45 225 315; do for m in 9 10 11 12; do run tg $n $m 100000 $((n+m)) 40; done; done
echo CHAIN C DONE
