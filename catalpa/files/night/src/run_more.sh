#!/bin/bash
# After the fetch: the frozen method with its rules (dawnlib2.py) on each new year, four at a time, then the two sheets.
cd /home/agent1/night
PY=/home/agent1/ipd/.venv/bin/python
for y in 2016 2017 2018 2019; do $PY -I src/dawnlib2.py $y /home/agent1/night/data/ida$y > cache2/run$y.log 2>&1 & done; wait
for y in 2020 2021 2026; do $PY -I src/dawnlib2.py $y /home/agent1/night/data/ida$y > cache2/run$y.log 2>&1 & done; wait
tail -q -n 1 cache2/run2016.log cache2/run2017.log cache2/run2018.log cache2/run2019.log cache2/run2020.log cache2/run2021.log cache2/run2026.log
$PY -I src/sheet4.py 2016,2017,2018,2019,2020,2021,2026 > sheet4.out 2>&1
$PY -I src/sunsheet.py 2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026 > sun.out 2>&1
echo "run done $(date -u +%H:%M:%S)"
