#!/bin/bash
# Runs the censuses one after another (one process at a time), each under the 2 GB cap.  Sizes were estimated first
# (t2_census.py prints the number of (multi)sets before it starts); the largest single run is Z_90 up to 8 elements,
# split in two parts of about 3 thousand million sets each.
cd /home/agent3/lean/sets-audit
PY="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python"
run() { $PY t2_census.py "$@" 2>&1 | tail -1; }
# multisets on the base groups Z_M
for mt in "2 18" "3 27" "5 25" "7 21" "11 12" "13 8" "6 18" "10 20" "12 12" "14 10" "15 12" "18 10" "20 8" "21 8" "24 8" "28 8" "33 7" "35 7" "50 6"; do
  set -- $mt; run multi $1 $2
done
# sets on the big groups Z_G
for gt in "4 4" "6 6" "8 8" "9 9" "10 10" "12 12" "14 14" "15 15" "16 16" "18 18" "20 20" "21 21" "22 22" "24 12" "25 25" "26 12" "27 27" \
          "28 10" "30 12" "32 12" "33 10" "35 9" "36 10" "39 8" "40 8" "42 8" "45 9" "48 8" "49 8" "50 8" "54 9" "56 8" "60 7" "63 8" "70 7" "72 8" \
          "75 7" "96 6" "98 6" "99 7" "108 7" "126 6" "150 6"; do
  set -- $gt; run set $1 $2
done
run set 90 8 0 9
run set 90 8 9 90
echo ALL DONE
