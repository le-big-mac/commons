#!/bin/sh
# batch.sh: the clouds of the study. Small ones twelve at a time; the two largest sizes six at a time (memory).
cd /home/agent2/peel
grep -v " 30000000 \| 100000000 " runs/jobs.txt | xargs -P 12 -L 1 sh -c './peel $0 $1 $2 -mult $3' > runs/small.jsonl
grep " 30000000 \| 100000000 " runs/jobs.txt | xargs -P 6 -L 1 sh -c './peel $0 $1 $2 -mult $3' > runs/large.jsonl
echo done
