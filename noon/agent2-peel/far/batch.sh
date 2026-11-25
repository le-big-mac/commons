#!/bin/sh
# batch.sh: the cell problem far up. AS RUN at 17:50 UTC on 24 November, with the build of that hour. The final cell2 starts
# the columns' random streams in a better way; to make these same fifteen windows with it, add  -seeding 1  (ftest.py and
# farfacts.py check that it then gives what that build gave).
# Twelve windows of period 32,768 to a height of 64,000 and three to 128,000,
# fifteen at a time. Each writes one line of JSON and a profile (band of height, points, mean depth, variance of depth).
cd /home/agent2/peel/far
(for s in 1 2 3 4 5 6 7 8 9 10 11 12; do echo "64000 $((640000 + s))"; done; for s in 1 2 3; do echo "128000 $((1280000 + s))"; done) | xargs -P 15 -L 1 sh -c './cell2 16384 2 $0 $1 -profile runs/profile-$0-$1.txt > runs/run-$0-$1.json'
echo done
