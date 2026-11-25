#!/bin/bash
# The runs made after the referee's report, each to redo or extend one of its controls.   usage: ./after.sh [processes]
#  corner-*:   the lowest setting of the sealed grid (P = 2, dc = 0.8) with half the time step, and with necks looked for at every step
#  fine01:     P = 6, dc = 0.1 at node spacing 0.05 (the dc = 0.1 column had spacing equal to the cutoff distance)
#  between-*:  dc = 1.0, 1.2, 1.4 at the four P, two seeds: where the ratio passes pi
#  minloop-*:  dc = 1.6 and 3.2 with a loop needing 6 cutoff distances to be cut (3 in the study), one seed
#  open-*:     the open-reach program (open.c) with one paper's values, four seeds
cd "$(dirname "$0")"; mkdir -p out/after; export OMP_NUM_THREADS=1
T2=4662.7; T3=1492.8; T45=636.3; T6=380.8
{
echo "corner-dt2 ./river 2 0.8 200 $T2 1 -out 1 -dt 0.0005"
echo "corner-every1 ./river 2 0.8 200 $T2 1 -out 1 -every 1"
echo "fine01 ./river 6 0.1 200 $T6 1 -out 1 -ds 0.05"
for dc in 1.0 1.2 1.4; do for seed in 1 2; do echo "between-P2-dc$dc-s$seed ./river 2 $dc 200 $T2 $seed -out 1"; done; done
echo "minloop-P2-dc3.2 ./river 2 3.2 200 $T2 1 -out 1 -amin 19.2"
echo "minloop-P2-dc1.6 ./river 2 1.6 200 $T2 1 -out 1 -amin 9.6"
for seed in 1 2 3 4; do echo "open-beatton-s$seed ./open 6.43 0.476 272 500 $seed -out 0.5 -f 1.86"; done
for dc in 1.0 1.2 1.4; do for seed in 1 2; do echo "between-P3-dc$dc-s$seed ./river 3 $dc 200 $T3 $seed -out 1"; done; done
echo "minloop-P3-dc3.2 ./river 3 3.2 200 $T3 1 -out 1 -amin 19.2"
echo "minloop-P3-dc1.6 ./river 3 1.6 200 $T3 1 -out 1 -amin 9.6"
for dc in 1.0 1.2 1.4; do for seed in 1 2; do echo "between-P4.5-dc$dc-s$seed ./river 4.5 $dc 200 $T45 $seed -out 1"; echo "between-P6-dc$dc-s$seed ./river 6 $dc 200 $T6 $seed -out 1"; done; done
echo "minloop-P4.5-dc3.2 ./river 4.5 3.2 200 $T45 1 -out 1 -amin 19.2"
echo "minloop-P4.5-dc1.6 ./river 4.5 1.6 200 $T45 1 -out 1 -amin 9.6"
echo "minloop-P6-dc3.2 ./river 6 3.2 200 $T6 1 -out 1 -amin 19.2"
echo "minloop-P6-dc1.6 ./river 6 1.6 200 $T6 1 -out 1 -amin 9.6"
} | xargs -P ${1:-11} -L 1 bash -c 'f=out/after/$0; [ -s $f.done ] || { nice -n 15 "${@}" -oxl $f.oxl > $f.out && echo ok > $f.done; }'
echo "after finished: $(ls out/after/*.done | wc -l) runs"
