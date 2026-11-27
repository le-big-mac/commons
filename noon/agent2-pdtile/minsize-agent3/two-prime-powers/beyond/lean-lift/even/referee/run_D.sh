#!/bin/bash
# Proposition P / Theorem D brute force; at most three at a time, 290 s each, 2 GB cap.
cd "$(dirname "$0")"
PY="$HOME/welch/.venv/bin/python"
list() {
# exhaustive, 3 does not divide n
for nm in "10 4" "10 6" "10 8" "10 10" "10 5" "10 7" "10 9" "14 4" "14 6" "14 8" "14 5" "14 7" "20 4" "20 6" "20 5" "20 7" \
          "22 4" "22 6" "22 5" "28 4" "28 6" "28 5" "40 4" "40 5" "44 4" "50 4" "50 5" "56 4" "70 4" "98 4" "100 4" "110 4" "140 4" \
          "5 6" "7 6" "25 5" "35 4" "35 5" "49 4" "55 4" \
          "6 3" "6 4" "6 5" "6 6" "6 7" "6 8" "6 9" "6 10" "12 3" "12 4" "12 5" "12 6" "12 7" "12 8" "18 3" "18 4" "18 5" "18 6" "18 7" \
          "24 3" "24 4" "24 5" "24 6" "30 3" "30 4" "30 5" "30 6" "36 3" "36 4" "36 5" "42 3" "42 4" "42 5" "48 3" "48 4" "48 5" \
          "54 3" "54 4" "60 3" "60 4" "90 3" "90 4" "9 6" "9 7" "15 5" "15 6" "21 5" "27 5" "45 4" "45 5"; do
  set -- $nm
  echo "tD_exh_$1_$2.out tD.py exh $1 $2"
done
echo "tD_rand_no3_a.out tD.py rand 1 12000 10 14 20 22 28 40 44 50 56 70 98 100 110 130 140"
echo "tD_rand_no3_b.out tD.py rand 2 3000 154 170 182 190 238 250 260 280 350 770"
echo "tD_rand_3_a.out tD.py rand 3 12000 6 12 18 24 30 36 42 48 54 60 66 72 84 90 96 120"
echo "tD_rand_3_b.out tD.py rand 4 3000 126 150 180 210 270 330 420 630"
echo "tD_rand_odd.out tD.py rand 5 8000 15 21 35 45 55 63 75 77 105 135 165 175 225 315"
for n in 10 14 20 22 28 50 70; do for m in 6 8 10; do echo "tD_adv_${n}_${m}.out tD.py adv 7 $n $m 6 150"; done; done
for n in 6 12 18 30 60; do for m in 6 8; do echo "tD_adv_${n}_${m}.out tD.py adv 7 $n $m 6 150"; done; done
}
list | xargs -P 3 -L 1 bash -c 'name="$1"; shift; timeout 290 bash ~/bin/cap2g.sh '"$PY"' "$@" > "$name" 2>&1; echo "exit $?" >> "$name"' _
