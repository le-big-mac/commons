#!/bin/bash
# The open reach with one paper's values (see paper.sh for how they are worked out): first node fixed, last node free.
#   quiet:      nothing comes in at the first node
#   fed:        the first node is given the curvature the far end had a step before (-inlet)
#   -k9, -k6:   the same with every node pushed at every step by a Gaussian of sd 1e-9 or 1e-6 along its normal (-kick),
#               the second referee's test of how much the quiet reach owes to the noise a program lets in
# usage: ./open.sh [processes]
cd "$(dirname "$0")"; mkdir -p out/open; export OMP_NUM_THREADS=1
{
for seed in 1 2 3 4; do
  echo "quiet-s$seed $seed"
  echo "fed-s$seed $seed -inlet"
  echo "quiet-k9-s$seed $seed -kick 1e-9"
  echo "quiet-k6-s$seed $seed -kick 1e-6"
  echo "fed-k9-s$seed $seed -inlet -kick 1e-9"
done
} | xargs -P ${1:-10} -L 1 bash -c 'f=out/open/$0; s=$1; shift; [ -s $f.done ] || { nice -n 15 ./open 6.43 0.476 272 500 $s -out 0.5 -f 1.86 -snap 125 $f.snap "${@}" > $f.out && echo ok > $f.done; }'
echo "open finished: $(ls out/open/*.done | wc -l) runs"
