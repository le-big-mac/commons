#!/bin/bash
cd /home/agent2/p3q2/referee2
for r in "$@"; do nice -n 5 /home/agent2/vuza/.venv/bin/python -B masscheck.py $r > out/mass_$r.out 2>&1; done
