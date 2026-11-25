#!/bin/bash
# One paper's own values, as far as I could read them (Schwenk, Lanzoni and Foufoula-Georgiou 2015: the Beatton River).
# Half-width 35 m, discharge 325.6 m3/s, friction 0.0036, valley slope 0.0067, alpha = 10 (their A = alpha + 1 = 11), E = 1.85e-8,
# a 40 km reach for 30,000 years, cutoff at one width.  From these: depth of the straight river 1.058 m, speed 4.40 m/s,
# D0 = 147 m, F0^2 = 1.86, P0 = (F0^2 + A)/2 = 6.43, dc = 70 m = 0.476 D0, valley 272 D0, time unit 240 years, so 30,000 years = 125 units.
# Run here on a repeating valley, with the feedback on, for 125 units (theirs) and for 500.   usage: ./paper.sh
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1
for seed in 1 2 3 4; do echo "$seed"; done | xargs -P 4 -L 1 bash -c 'f=out/paper/beatton-s$0; [ -s $f.done ] || { nice -n 15 ./river 6.43 0.476 272 500 $0 -out 0.5 -f 1.86 -snap 25 $f.snap > $f.out && echo ok > $f.done; }'
echo "paper finished: $(ls out/paper/*.done | wc -l) runs"
