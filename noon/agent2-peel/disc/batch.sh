#!/bin/sh
# batch.sh: the clouds of the sheet (expectations.md, "The design"): each kind, 4,000 clouds of 10^5 points, 2,000 of 10^6, 200 of 10^7.
cd /home/agent2/peel/disc && mkdir -p runs
P=/home/agent2/vuza/.venv/bin/python
$P -I make.py chance 100000   4000 4000000 runs/chance-100000.jsonl 14
$P -I make.py exact  100000   4000 8000000 runs/exact-100000.jsonl 14
$P -I make.py chance 1000000  2000 5000000 runs/chance-1000000.jsonl 14
$P -I make.py exact  1000000  2000 7000000 runs/exact-1000000.jsonl 14
$P -I make.py chance 10000000 200  6000000 runs/chance-10000000.jsonl 12
$P -I make.py exact  10000000 200  9000000 runs/exact-10000000.jsonl 12
echo done
