#!/bin/bash
# sets proposition and three primes; 4 processes
cd /home/agent3/pq2/referee/two-powers
export OMP_NUM_THREADS=1
cat > out/batch3-list.txt <<'L'
sets.py 18 highs 300 > out/sets-18.jsonl
sets.py 24 highs 300 > out/sets-24.jsonl
sets.py 48 highs 300 > out/sets-48.jsonl
sets.py 54 highs 300 > out/sets-54.jsonl
sets.py 72 highs 300 > out/sets-72.jsonl
sets.py 100 highs 300 > out/sets-100.jsonl
sets.py 108 highs 300 > out/sets-108.jsonl
three.py exhaust30 > out/three-exhaust30.jsonl
three.py top 42 highs 300 > out/three-top-42.jsonl
three.py top 66 highs 300 > out/three-top-66.jsonl
three.py top 70 highs 300 > out/three-top-70.jsonl
three.py top 105 highs 600 > out/three-top-105.jsonl
three.py top 60 highs 300 > out/three-top-60.jsonl
three.py top 78 highs 300 > out/three-top-78.jsonl
three.py top 110 highs 600 > out/three-top-110.jsonl
three.py pairs 30 highs 300 > out/three-pairs-30.jsonl
three.py pairs 42 highs 600 > out/three-pairs-42.jsonl
three.py upsets 42 highs 300 > out/three-42-upsets.jsonl
sets.py 144 highs 300 > out/sets-144.jsonl
sets.py 200 highs 300 > out/sets-200.jsonl
sets.py 225 highs 300 > out/sets-225.jsonl
construct.py 5 3 7 3 4 20 >> out/construct.jsonl
L
cat out/batch3-list.txt | xargs -P 4 -I{} sh -c 'nice -n 10 ~/welch/.venv/bin/python {} 2>> out/batch3.err'
echo done > out/batch3.done
