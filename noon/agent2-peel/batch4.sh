#!/bin/sh
# batch4.sh: the squares and triangles again, with their sizes corrected (the first runs, kept in runs/old-polygons/,
# used half-sides typed by hand that were a few parts in a million off the disc's area).
cd /home/agent2/peel
xargs -P 10 -L 1 sh -c './peel $0 $1 $2 -mult $3' < runs/jobs-polygons.txt > runs/polygons.jsonl
echo done
