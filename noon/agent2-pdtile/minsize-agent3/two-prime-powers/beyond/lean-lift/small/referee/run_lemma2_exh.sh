#!/bin/bash
# exhaustive runs of ref_lemma2.py, two streams
cd /home/agent3/lean/lift-check/small/referee
run() { timeout 590 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python ref_lemma2.py exh $1 $2 > lemma2_exh_$1_$2.out 2>&1; echo "exit status $? ; seconds $SECONDS" >> lemma2_exh_$1_$2.out; }
( run 9 6; run 15 6; run 25 5; run 21 5; run 27 5; run 81 3; run 75 3 ) &
( run 45 4; run 63 3; run 105 3; run 49 4; run 225 2; run 125 3 ) &
wait
