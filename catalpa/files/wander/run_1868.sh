#!/bin/bash
# The eclipse of 18 August 1868: integrate back from J2000 with the full model and print states every 0.002 day for two days around it, with the Earth's pole (LIBOUT).
cd ~/orrery && J2=1 TIDE=195 LFIG=3 POLE=1 CASS=1 K2E=0.30 K2M=0.024 HDYN=0.00327253855882 DPSI0=-13.992430 DEPS0=-5.771763 OUTWINDOWS="-47983.3:-47981.3" LIBOUT=lib_1868.txt ./orrery_j2t data/ic.txt 131.5 -0.05 2 0.05 state > states_1868.txt 2> states_1868.err
wc -l states_1868.txt lib_1868.txt; head -c 300 states_1868.err
