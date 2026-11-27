#!/bin/bash
# usage: run.sh OUTFILE script.py args...   (runs inside referee2, 2 GB cap, 290 s limit, output to referee2/OUTFILE)
cd /home/agent3/lean/lift-check/even/referee2 || exit 1
out="$1"; shift
timeout 290 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python "$@" > "/home/agent3/lean/lift-check/even/referee2/$out" 2>&1
echo "exit $? : $out"
