#!/bin/bash
# Rerun published folders from copies of their published files and compare the results.   usage: bash run.sh   (writes report.out here)
P=/home/agent2/vuza/.venv/bin/python; S=/home/agent2/repro/scratch; C=/home/agent2/repro/compare.py
rm -rf "$S"; mkdir -p "$S"; exec > /home/agent2/repro/report.out 2>&1
echo "started $(date -u +%H:%M:%S) UTC"
cp -r /srv/commons/agent2-orbweb "$S/orbweb"; cd "$S/orbweb" && $P orbweb.py build new.json > /dev/null && $P $C "orb web, the threads and notes" new.json orb.json
cp -r /srv/commons/agent2-taffy "$S/taffy"; cd "$S/taffy" && nice $P taffy.py sheet new-sheet.json > new-sheet.out && $P $C "taffy, the sheet" new-sheet.json sheet.json && $P verdicts.py new-sheet.json new-results.json > new-verdicts.out && cmp new-verdicts.out verdicts.out && echo "taffy: verdicts.out identical"
cp -r /srv/commons/agent2-impetus "$S/impetus"; cd "$S/impetus" && $P impetus.py new-results.json > new.out && cmp new.out impetus.out && echo "impetus: impetus.out identical" && $P $C "impetus, results" new-results.json results.json
cp -r /srv/commons/agent2-onset "$S/onset"; cd "$S/onset"
nice $P onset.py sheet new-sheet.json > /dev/null && $P $C "onset, the sheet" new-sheet.json sheet.json
nice $P onset.py sizes-random new-sr.json > /dev/null && $P $C "onset, sizes with random tempos" new-sr.json sizes-random.json
nice $P onset.py sizes-regular new-sg.json > /dev/null && $P $C "onset, sizes with evenly spaced tempos" new-sg.json sizes-regular.json
$P verdicts.py new-sheet.json new-sr.json new-sg.json new-results.json > new-verdicts.out && cmp new-verdicts.out verdicts.out && echo "onset: verdicts.out identical"
nice $P onset.py curves new-curves.json > /dev/null && $P $C "onset, the curves" new-curves.json curves.json
nice $P climb.py new-climb.json > /dev/null && $P $C "onset, the climb" new-climb.json climb.json
nice $P long.py new-long.json > /dev/null && $P $C "onset, the long run" new-long.json long.json
echo "finished $(date -u +%H:%M:%S) UTC"
