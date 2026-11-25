#!/bin/bash
# usage: cmp_one.sh P C d T mode  -> one line: board lag T mode noon=<yes/no> mine=<YES/NO/timeout>
P=$1; C=$2; d=$3; T=$4; m=$5
noon=$(echo "" | timeout 20 nice -n 15 ./noon_lag $P $C $d $T $m | head -n 1 | cut -d' ' -f1)
mine=$(timeout 8 nice -n 15 ./ruler_${P}_${C} $m $d $T | sed 's/.*: \(YES\|NO\) .*/\1/')
[ -z "$mine" ] && mine=timeout
[ -z "$noon" ] && noon=timeout
echo "$P $C lag $d T $T $m noon=$noon mine=$mine"
