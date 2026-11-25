#!/bin/bash
cd /home/agent2/p3q2/referee2
PY=/home/agent2/vuza/.venv/bin/python
lane() { for r in "$@"; do nice -n 5 $PY -B ycheck.py $r > out/ycheck_$r.out 2>&1; done; }
lane A1a A1b A2 B2 B3 &
lane Ap1 Ap2 C3 Cp &
wait
cat out/ycheck_*.out
