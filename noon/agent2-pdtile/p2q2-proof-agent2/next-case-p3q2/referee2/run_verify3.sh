#!/bin/bash
# rerun of the author's verify3.py on copies of the published pickles, three lanes
cd /home/agent2/p3q2/referee2/orig
PY=/home/agent2/vuza/.venv/bin/python
lane() { for r in "$@"; do pre=split; [ "$r" = C3 ] && pre=region; [ "$r" = Cp ] && pre=region; nice -n 5 $PY -B verify3.py $r $pre > ../out/verify3_$r.out 2>&1; done; }
lane A1b A2 C3 Cp &
lane Ap1 Ap2 B1 &
lane B2 B3 A1a &
wait
