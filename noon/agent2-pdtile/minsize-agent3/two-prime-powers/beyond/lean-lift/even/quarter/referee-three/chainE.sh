#!/bin/bash
cd "$(dirname "$0")"
py() { timeout 595 nice -n 15 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python "$@" 2>&1 | grep -v '^$'; }
py tree3.py 3 16
py tree3.py 4 12
py tree3.py 5 10
for n in 25 75 225 125; do for m in 9 10 11 12 13; do py twolevels.py tl $n $m 100000 $((n+m)) 20; done; done
py targeted.py tg 675 8 400000 683 50
py targeted.py tg 1575 8 400000 1583 60
py targeted.py tg 525 8 400000 533 50
for n in 225 1155 945 1575; do for m in 9 10 11 12; do py test_theorem.py rnd $n $m 20000 $((n+m)) 30; done; done
for n in 1155 945 1575; do for m in 6 7 8; do py test_theorem.py rnd $n $m 20000 $((n+m)) 25; done; done
for n in 15 45 105; do for m in 13 14; do py test_theorem.py rnd $n $m 20000 $((n+m)) 40; done; done
echo CHAIN E DONE
