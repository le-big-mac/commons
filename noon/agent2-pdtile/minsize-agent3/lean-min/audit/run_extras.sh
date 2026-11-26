#!/bin/bash
# extra groups, beyond those asked for; at most 8 processes at any time
cd "$(dirname "$0")"
PY=/home/agent3/welch/.venv/bin/python
export OMP_NUM_THREADS=1
$PY runA.py 45:9 50:8 48:8
$PY runB.py --fullmax=1e9 --cap=4e10 2:7:1 7:2:1 3:7:1 7:3:1 2:11:1 11:2:1 2:7:2
$PY runB.py --fullmax=1e9 --cap=1e9 2:5:3 3:2:3 5:2:2 3:5:2
$PY runB.py --fullmax=1e9 --cap=3e8 2:3:4
echo finished
