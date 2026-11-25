#!/bin/bash
# The sealed grid: P in {2, 3, 4.5, 6}, dc in {0.2, 0.4, 0.8}, four seeds, LX = 200, run length 800/sigma.
# usage: ./grid.sh [processes]
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
jobs=""
for P in 2 3 4.5 6; do
  T=$(awk -v p=$P 'BEGIN{s=(sqrt(p)-1)^2; printf "%.1f", 800/s}')
  for dc in 0.2 0.4 0.8; do for seed in 1 2 3 4; do
    jobs="$jobs$P $dc $T $seed\n"
  done; done
done
printf "$jobs" | xargs -P ${1:-8} -L 1 bash -c 'f=out/grid/P$0-dc$1-s$3; [ -s $f.done ] || { nice -n 15 ./river $0 $1 200 $2 $3 -out 1 -oxl $f.oxl > $f.out && echo ok > $f.done; }'
echo "grid finished: $(ls out/grid/*.done | wc -l) runs"
