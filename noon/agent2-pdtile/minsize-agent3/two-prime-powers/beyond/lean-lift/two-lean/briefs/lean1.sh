#!/bin/bash
# Runs one Lean job (lake build Pnq.X, or lake env lean File.lean) in the current copy, after waiting while the programs of this
# account hold more than 10 GiB (anonymous memory; the file cache, which is given back on demand, is not counted): all processes
# of the account share one limit, and going over it slows every job on the machine.
# usage: cd <your copy> && bash ~/lean/two-briefs/lean1.sh lake build Pnq.Sign
S=/sys/fs/cgroup/system.slice/system-agent.slice/[address removed]/memory.stat
for i in $(seq 1 60); do
  A=$(awk '$1=="anon"{print $2}' $S)
  [ "${A:-0}" -lt 10737418240 ] && break
  sleep 10
done
exec nice -n 5 "$@"
