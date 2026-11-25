#!/bin/bash
# Runs beyond the sealed grid.  usage: ./extra.sh [processes]
#  - the base case with the feedback of length on slope (F0^2 = 0.1), four seeds          (sealed line M10)
#  - the base case at LX = 100 and LX = 400, two seeds each                               (first priced check)
#  - the base case at spacing 0.05, two seeds                                             (second priced check)
#  - the base case with snapshots, for the figure, the film and for measuring reaches
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
T=1492.8
{
for seed in 1 2; do echo "ds05-s$seed 3 0.4 200 $T $seed -out 1 -ds 0.05"; done
for seed in 1 2; do echo "LX400-s$seed 3 0.4 400 $T $seed -out 1 -snap 25 out/extra/LX400-s$seed.snap"; done
for seed in 1 2 3 4; do echo "feed-s$seed 3 0.4 200 $T $seed -out 1 -f 0.1"; done
for seed in 1 2; do echo "LX100-s$seed 3 0.4 100 $T $seed -out 1"; done
echo "snap-s5 3 0.4 200 $T 5 -out 1 -snap 25 out/extra/snap-s5.snap"
} | xargs -P ${1:-6} -L 1 bash -c 'f=out/extra/$0; [ -s $f.done ] || { nice -n 15 ./river "${@}" -oxl $f.oxl > $f.out && echo ok > $f.done; }'
echo "extra finished: $(ls out/extra/*.done | wc -l) runs"
