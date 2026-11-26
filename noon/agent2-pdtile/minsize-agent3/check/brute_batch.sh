#!/bin/bash
# exhaustive enumerations, three processes at a time
PY=/home/agent3/welch/.venv/bin/python
cd /home/agent3/minsize/check
for args in "2 3 2 12 set" "3 2 2 18 set" "2 5 2 20 set" "2 3 3 24 set" "3 2 2 18 multi" "2 5 2 15 multi" "2 3 3 14 multi"; do
  echo "$(date -u +%H:%M:%S) start $args"
  nice -n 5 $PY brute_run.py $args 3
  echo "$(date -u +%H:%M:%S) done $args"
done
