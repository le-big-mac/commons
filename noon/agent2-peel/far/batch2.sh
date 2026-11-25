#!/bin/sh
# batch2.sh: AS RUN at 18:26 UTC; cell2s was the build of 18:25, and the final cell2 gives the same windows (ftest.py and
# farfacts.py check it): to run again, put ./cell2 for ./cell2s.
# Twelve more windows of period 32,768 to a height of 128,000, with the build cell2s (the better seeding;
# slabs of the front written out). Each writes one line of JSON, a profile and a file of slabs.
cd /home/agent2/peel/far
for s in 4 5 6 7 8 9 10 11 12 13 14 15; do echo "128000 $((1280000 + s))"; done | xargs -P 12 -L 1 sh -c './cell2s 16384 2 $0 $1 -profile runs/profile-$0-$1.txt -snap runs/snap-$0-$1.bin > runs/run-$0-$1.json'
echo done
