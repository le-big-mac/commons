#!/bin/bash
# exists_lift_two_all: the exhaustive searches for lifts, one after the other (one process at a time).
# usage: bash run_t4.sh OUTFILE
cd "$(dirname "$0")"
P="bash $HOME/bin/cap2g.sh $HOME/welch/.venv/bin/python -I t4_lift.py"
out="$1"
: > "$out"
while read N mmin mmax; do
  $P $N $mmin $mmax >> "$out" 2>&1
done <<LIST
1 1 40
2 1 30
4 1 24
8 1 16
16 1 11
32 1 8
64 1 6
128 1 4
256 1 3
3 1 20
5 1 14
6 1 14
7 1 12
9 1 12
10 1 10
11 1 9
12 1 10
13 1 8
14 1 8
15 1 10
17 1 7
18 1 8
19 1 7
20 1 7
21 1 8
22 1 7
23 1 6
24 1 7
25 1 7
26 1 6
27 1 7
28 1 6
29 1 6
30 1 7
33 1 6
35 1 6
36 1 6
40 1 6
42 1 6
45 1 6
48 1 5
50 1 5
54 1 5
60 1 5
63 1 5
70 1 5
72 1 5
75 1 5
84 1 5
90 1 5
96 1 4
100 1 4
105 1 5
120 1 4
126 1 4
150 1 4
165 1 4
180 1 4
195 1 4
210 1 4
231 1 4
315 1 4
330 1 4
390 1 3
420 1 4
462 1 3
525 1 3
630 1 3
840 1 3
945 1 3
1155 1 3
2310 1 2
LIST
echo finished >> "$out"
