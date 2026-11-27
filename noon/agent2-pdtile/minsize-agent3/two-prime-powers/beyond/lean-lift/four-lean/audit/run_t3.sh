#!/bin/bash
# A1 / exists_signs_odd: the exhaustive searches, one after the other (one process at a time).
# usage: bash run_t3.sh OUTFILE
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t3_a1.py"
out="$1"
: > "$out"
while read n mmax; do
  $P $n 1 $mmax >> "$out" 2>&1
done <<LIST
1 40
3 30
5 20
7 16
9 16
11 12
13 11
15 12
17 9
19 9
21 10
25 9
27 9
33 7
35 7
39 7
45 7
49 6
55 6
63 6
75 6
81 6
99 5
105 5
135 5
165 4
195 4
225 4
231 4
315 4
525 3
735 3
945 3
1155 3
1365 3
3465 2
2 6
4 6
6 6
10 5
12 5
30 4
LIST
echo finished >> "$out"
