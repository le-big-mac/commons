#!/bin/bash
# usage: run_search.sh   -- the checker's search.py on the seven WorldPop grids (re-gridded by the checker) and the eight GHS-POP grids, in parallel
PY=/home/agent3/welch/.venv/bin/python
C=/home/agent3/hemi2/check
for n in g2-2015 g2-2020 g2-2025 g2-2030 g1-2000 g1-2010 g1-2020; do
  $PY -I $C/search.py $n $C/grids/$n.npy $C/out/search-$n.json 0.25 > $C/out/search-$n.out 2>&1 &
done
for y in 1975 2000 2005 2010 2015 2025 2030; do
  $PY -I $C/search.py ghs-$y /home/agent3/hemi/grids/pop005_$y.npy $C/out/search-ghs-$y.json 0.25 > $C/out/search-ghs-$y.out 2>&1 &
done
$PY -I $C/search.py ghs-2020 /home/agent3/hemi/grids/pop005.npy $C/out/search-ghs-2020.json 0.25 > $C/out/search-ghs-2020.out 2>&1 &
wait
echo all searches finished
