#!/bin/bash
# run a python script of this audit with a hard cap: 1.8 GB of address space, a wall-clock limit (default 280 s), unbuffered output
# usage: run_capped.sh script.py [seconds] [args...]
script="$1"; secs="${2:-280}"; shift; shift
ulimit -v 1800000
exec /usr/bin/time -f "maxrss_kb=%M elapsed_s=%e" timeout "$secs" /home/agent3/welch/.venv/bin/python -I -u "$script" "$@"
