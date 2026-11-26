#!/bin/bash
# the sixteen patterns of Z_36 left undecided at 60 s, given 400 s each (at most 107 minutes in all)
cd ~/pq2
while IFS= read -r line; do nice -n 10 ~/welch/.venv/bin/python gen.py 36 --only "$line" --tlimit 400 --workers 3 --cap 36 | grep '^{' >> out/z36-again.jsonl; done < out/pats36-again.txt
echo done > out/z36-again.done
