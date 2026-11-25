#!/bin/sh
# batch3.sh: the triangles of a million points, and the squares and triangles of ten million, with the binary whose
# bound on the candidates is tighter along straight sides (peel2: same layers, far fewer candidates).
cd /home/agent2/peel
grep "^triangle 1000000 \|^square 10000000 \|^triangle 10000000 " runs/jobs.txt | xargs -P 6 -L 1 sh -c './peel2 $0 $1 $2 -mult $3' > runs/poly.jsonl
echo done
