#!/bin/bash
# runq.sh queuefile P : runs the lines "outfile script args..." of the queue, P at a time, each under the 2 GB cap and
# stopped after 290 seconds at the latest.
cd "$(dirname "$0")"
run_one() {
  out=$1; shift
  s=$(date +%s)
  timeout 290 bash ~/bin/cap2g.sh ~/welch/.venv/bin/python "$@" > "$out" 2>&1
  rc=$?
  echo "exit $rc after $(( $(date +%s) - s )) s" >> "$out"
}
export -f run_one
xargs -a "$1" -P "$2" -L 1 bash -c 'run_one "$@"' _
