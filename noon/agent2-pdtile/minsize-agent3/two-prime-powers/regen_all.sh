#!/bin/bash
# after the Z_100 completion run has ended: rebuild the two tables, the note, and the files of the note beyond up-sets
set -e
cd ~/pq2
test -f out2/finish100.done
~/welch/.venv/bin/python make_tables2.py 36 2 3 note/table-36.new.md note/witnesses-36.jsonl > note/counts2-36.json
~/welch/.venv/bin/python make_tables2.py 100 2 5 note/table-100.new.md note/witnesses-100.jsonl > note/counts2-100.json
cp note/table-36.new.md note/table-36.md; cp note/table-100.new.md note/table-100.md
~/welch/.venv/bin/python make_note2.py note/read-text.txt note/lean-section.md > note/README.md
~/welch/.venv/bin/python after_referee.py > note/after_referee.out
cd rule
~/welch/.venv/bin/python status.py > status.out
~/welch/.venv/bin/python algebra2.py > algebra2.out
~/welch/.venv/bin/python either.py > either.out
~/welch/.venv/bin/python make_beyond.py > beyond-up-sets.md
date -u +"regenerated %H:%M:%S UTC"
