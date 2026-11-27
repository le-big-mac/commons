#!/bin/bash
# Runs one Lean job (lake build Pnq.X, or lake env lean File.lean) in the current copy.
# Several instances work at once and all processes of this account share one memory limit, so:
#  - at most 5 Lean jobs of this task run at a time (five lock files; a job waits for a free one);
#  - a job does not start while the programs of this account hold more than 9 GiB of anonymous memory.
# usage: cd <your copy> && bash ~/lean/signs-briefs/lean1.sh lake build Pnq.SignSlice
L=/home/agent3/lean/signs-briefs/locks
mkdir -p "$L"
S=/sys/fs/cgroup/system.slice/system-agent.slice/[address removed]/memory.stat
while true; do
  for k in 1 2 3 4 5; do
    exec 9>"$L/slot$k"
    if flock -n 9; then
      for i in $(seq 1 60); do
        A=$(awk '$1=="anon"{print $2}' $S)
        [ "${A:-0}" -lt 9663676416 ] && break
        sleep 10
      done
      nice -n 5 "$@"
      exit $?
    fi
    exec 9>&-
  done
  sleep 3
done
