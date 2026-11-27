#!/bin/bash
# A' and B by brute force: two chains of short runs (each run stops itself after 270 s); usage: run_t4.sh A|B
cd /home/agent3/lean/even-audit
PY="bash /home/agent3/bin/cap2g.sh /home/agent3/welch/.venv/bin/python -I t4_all.py"
if [ "$1" = A ]; then
  out=t4_A.out; : > $out
  # every multiset (no translation), sizes 0..: the moduli of the brief that are prime to 3, and small ones
  for nm in "2 12" "4 9" "5 7" "8 7" "10 6" "20 5" "28 4" "40 4"; do set -- $nm; $PY A $1 0 $2 ALL >> $out 2>&1; done
  # multisets containing 0, sizes 3..
  for nm in "2 14" "4 12" "5 10" "7 9" "8 10" "10 9" "11 8" "13 8" "14 8" "16 8" "20 8" "22 7" "25 7" "26 7" "28 7" \
            "32 7" "35 7" "40 7" "44 6" "49 6" "50 6" "52 6" "55 6" "56 6" "64 6" "70 6" "77 5" "80 5" "100 5" \
            "140 4" "175 4" "200 4" "280 4" "385 3" "560 3" "700 3"; do
    set -- $nm; $PY A $1 3 $2 >> $out 2>&1
  done
  $PY A 140 5 5 >> $out 2>&1
  echo "chain A done" >> $out
else
  out=t4_B.out; : > $out
  for nm in "2 12" "4 9" "6 7" "8 7" "10 6" "12 6" "20 5" "24 5" "28 4" "40 4" "60 4"; do
    set -- $nm; $PY B $1 0 $2 ALL >> $out 2>&1; done
  for nm in "4 12" "6 10" "8 10" "9 9" "10 9" "12 9" "15 8" "18 8" "20 8" "21 7" "24 7" "27 7" "28 7" "30 7" "36 7" \
            "40 7" "42 6" "45 6" "48 6" "54 6" "60 6" "63 6" "72 6" "84 5" "90 5" "96 5" "105 5" "120 5" "180 4" \
            "210 4" "240 4" "420 3" "840 3"; do
    set -- $nm; $PY B $1 3 $2 >> $out 2>&1
  done
  echo "chain B done" >> $out
fi
