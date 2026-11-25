#!/bin/bash
# The base case with each choice of mine changed, one at a time, two seeds each.   usage: ./sweep.sh [processes]
#   amin2, amin5: a loop must be longer than 2 dc, or 5 dc, to be cut (3 dc in the study)
#   smooth2:      two nodes dropped either side of each join, as some authors do
#   every1:       necks looked for at every step (every fifth in the study)
#   dt2:          half the time step
cd "$(dirname "$0")"; mkdir -p out/sweep
export OMP_NUM_THREADS=1
T=1492.8
{
for seed in 1 2; do
  echo "amin2-s$seed 3 0.4 200 $T $seed -out 1 -amin 0.8"
  echo "amin5-s$seed 3 0.4 200 $T $seed -out 1 -amin 2.0"
  echo "smooth2-s$seed 3 0.4 200 $T $seed -out 1 -smooth 2"
  echo "every1-s$seed 3 0.4 200 $T $seed -out 1 -every 1"
  echo "dt2-s$seed 3 0.4 200 $T $seed -out 1 -dt 0.0005"
done
} | xargs -P ${1:-4} -L 1 bash -c 'f=out/sweep/$0; [ -s $f.done ] || { nice -n 15 ./river "${@}" > $f.out && echo ok > $f.done; }'
echo "sweep finished: $(ls out/sweep/*.done | wc -l) runs"
