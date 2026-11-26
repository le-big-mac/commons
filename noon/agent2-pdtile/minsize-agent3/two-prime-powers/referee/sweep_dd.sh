#!/bin/bash
# double description for every M = p^n q^m (n, m >= 1) up to 400, and some larger ones; 6 processes; 15 minutes at most for one group
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
mkdir -p out/sweep
~/welch/.venv/bin/python - <<'PY' > out/sweep/list.txt
from lib import prime_factors
L = [M for M in range(6, 401) if len(prime_factors(M)) == 2]
L += [432, 500, 648, 675, 864, 972, 1000, 1125, 1296]
print('\n'.join(map(str, L)))
PY
cat out/sweep/list.txt | xargs -P 6 -I{} sh -c 'timeout 900 nice -n 10 ~/welch/.venv/bin/python dd.py {} > out/sweep/dd-{}.jsonl 2> out/sweep/dd-{}.err; echo "{} exit $?" >> out/sweep/exits.txt'
echo done > out/sweep/done
