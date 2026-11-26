#!/bin/bash
# one chunk of the Z_100 patterns (60 s each), or the undecided Z_36 patterns again (600 s each); usage: run100.sh J | run100.sh again
J=$1; cd ~/pq2
if [ "$J" = again ]; then
  while IFS= read -r line; do nice -n 10 ~/welch/.venv/bin/python gen.py 36 --only "$line" --tlimit 600 --workers 3 --cap 36 | grep '^{' >> out/z36-again.jsonl; done < out/pats36-again.txt
  echo done > out/z36-again.done
else
  while IFS= read -r line; do nice -n 10 ~/welch/.venv/bin/python gen.py 100 --only "$line" --tlimit 60 --workers 3 --cap 100 | grep '^{' >> out/z100-$J.jsonl; done < out/pats100-$J.txt
  echo done > out/z100-$J.done
fi
