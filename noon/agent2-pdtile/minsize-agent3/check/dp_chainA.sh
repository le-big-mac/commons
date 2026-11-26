#!/bin/bash
cd /home/agent3/minsize/check; PY=/home/agent3/welch/.venv/bin/python
for a in "3 2 5 255 255 multi" "3 2 3 54 54 multi" "2 3 6 96 96 multi"; do echo "$(date -u +%H:%M:%S) start $a"; nice -n 5 $PY dp_run.py $a 1; echo "$(date -u +%H:%M:%S) done $a"; done
