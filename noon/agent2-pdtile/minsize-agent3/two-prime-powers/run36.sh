#!/bin/bash
# one chunk of the Z_36 patterns; usage: run36.sh J
J=$1; cd ~/pq2
while IFS= read -r line; do
  nice -n 10 ~/welch/.venv/bin/python gen.py 36 --only "$line" --tlimit 60 --workers 4 --cap 36 | grep '^{' >> out/z36-$J.jsonl
done < out/pats36-$J.txt
echo done > out/z36-$J.done
