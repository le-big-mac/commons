#!/bin/sh
# cellbatch.sh: the cell problem at five heights, three windows at a time
cd /home/agent2/peel
xargs -P 3 -L 1 sh -c './cell $0 $1 $2 -profile runs/cell/profile-$1-$2.txt' < runs/cell/jobs.txt > runs/cell/cell.jsonl
echo done
