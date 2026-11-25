#!/bin/bash
# usage: run_jobs.sh JOBFILE NPROC TAG
cd /home/agent2/p3q2/referee2
nl -ba "$1" | xargs -P "$2" -L 1 bash -c 'n=$0; nice -n 5 /home/agent2/vuza/.venv/bin/python -B recheck.py "$@" > out/recheck_'"$3"'_$n.out 2>&1'
