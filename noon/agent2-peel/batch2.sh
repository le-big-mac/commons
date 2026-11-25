#!/bin/sh
# batch2.sh: what was left when batch.sh was stopped (its ten-million-point squares were taking most of an hour each):
# the triangles at 10^5 and 10^6, and the large discs, side by side. The squares and triangles of 10^7 points are not run.
cd /home/agent2/peel
(grep "^disc 30000000 \|^disc 100000000 " runs/jobs.txt | xargs -P 6 -L 1 sh -c './peel $0 $1 $2 -mult $3' > runs/large.jsonl) &
(grep "^triangle 100000 \|^triangle 1000000 " runs/jobs.txt | xargs -P 8 -L 1 sh -c './peel $0 $1 $2 -mult $3' > runs/triangles.jsonl) &
wait
echo done
