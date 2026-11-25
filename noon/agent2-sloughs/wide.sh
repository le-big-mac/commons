#!/bin/bash
# Beyond the sealed grid: wider cutoff distances (1.6 and 3.2 D) and a narrower one (0.1 D), two seeds each.   usage: ./wide.sh [processes]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
jobs=""
for P in 2 3 4.5 6; do
  T=$(awk -v p=$P 'BEGIN{s=(sqrt(p)-1)^2; printf "%.1f", 800/s}')
  for dc in 1.6 3.2 0.1; do for seed in 1 2; do jobs="$jobs$P $dc $T $seed\n"; done; done
done
printf "$jobs" | xargs -P ${1:-6} -L 1 bash -c 'f=out/wide/P$0-dc$1-s$3; [ -s $f.done ] || { nice -n 15 ./river $0 $1 200 $2 $3 -out 1 -oxl $f.oxl > $f.out && echo ok > $f.done; }'
echo "wide finished: $(ls out/wide/*.done | wc -l) runs"
