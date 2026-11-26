#!/bin/bash
cd /home/agent3/minsize/check; PY=/home/agent3/welch/.venv/bin/python
for a in "7 2 2 98 98 multi" "7 2 3 255 255 multi" "5 2 4 255 255 multi" "2 5 2 30 30 multi" "5 3 2 75 75 multi" "5 2 3 250 250 set" "5 2 2 50 50 set" "2 3 5 96 96 set"; do echo "$(date -u +%H:%M:%S) start $a"; nice -n 5 $PY dp_run.py $a 1; echo "$(date -u +%H:%M:%S) done $a"; done
