#!/bin/bash
cd /home/agent3/minsize/prove/referee
while [ ! -f run_random.done ]; do sleep 5; done
./run_dp2.sh
./run_brute3.sh
echo done > run_rest.done
