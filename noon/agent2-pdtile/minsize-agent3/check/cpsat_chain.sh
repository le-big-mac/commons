#!/bin/bash
cd /home/agent3/minsize/check; PY=/home/agent3/welch/.venv/bin/python
for a in "2 7 2 multi 120 1 zero" "3 7 2 multi 120 1 zero" "2 11 2 multi 120 1 zero" "2 7 3 multi 120 1 zero" "7 3 2 multi 120 1 zero" "2 5 4 multi 120 1 x1"; do
  set -- $a
  nice -n 5 $PY cpsat_table.py $a > cpsat-table-p$1-q$2-n$3.out 2>&1
  echo "$(date -u +%H:%M:%S) done $a: $(tail -1 cpsat-table-p$1-q$2-n$3.out)"
done
