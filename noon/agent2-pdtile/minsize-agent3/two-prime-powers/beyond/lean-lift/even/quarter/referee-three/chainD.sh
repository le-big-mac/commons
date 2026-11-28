#!/bin/bash
cd "$(dirname "$0")"
py() { timeout 595 nice -n 15 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python "$@" 2>&1 | grep -v '^$'; }
py examples.py
py small.py
py tree3.py 3 10
py tree3.py 4 8
for m in 4 5 6 7; do py shapes.py 27 $m ex; done
for m in 5 6 7 8 9 10; do py shapes.py 81 $m rnd 60000; py shapes.py 243 $m rnd 40000; done
py shapes.py 27 8 rnd 100000
echo CHAIN D DONE
