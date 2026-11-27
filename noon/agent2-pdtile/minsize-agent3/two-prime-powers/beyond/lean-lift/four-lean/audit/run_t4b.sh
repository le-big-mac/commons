#!/bin/bash
# sizes_eq_two_all: the censuses of Z_N and Z_2N, one pair after the other (one process at a time).
# usage: bash run_t4b.sh OUTFILE
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t4b_sizes.py"
out="$1"
: > "$out"
while read N S; do
  $P $N $S >> "$out" 2>&1
done <<LIST
1 30
2 24
3 16
4 14
5 12
6 11
7 10
8 10
9 9
10 9
11 8
12 8
13 8
14 8
15 8
16 8
17 7
18 7
19 7
20 7
21 7
22 6
23 6
24 6
25 6
26 6
27 6
28 6
29 6
30 6
32 6
33 5
35 5
36 5
40 5
42 5
45 5
48 5
60 5
63 5
64 5
75 4
90 4
105 4
128 4
165 4
195 4
210 4
231 4
315 3
420 3
1155 3
LIST
echo finished >> "$out"
