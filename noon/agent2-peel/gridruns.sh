#!/bin/sh
# gridruns.sh: grid points peeled vertices only: discs of grid points, and square grids. For after.py, section F.
cd /home/agent2/peel
for R in 100 200 400 800; do
  /home/agent2/vuza/.venv/bin/python -I -c "
import sys
R=int(sys.argv[1]); out=open('/home/agent2/peel/runs/grid/disc-%d.pts' % R,'w')
for x in range(-R,R+1):
    for y in range(-R,R+1):
        if x*x+y*y<=R*R: out.write('%d %d\n' % (x,y))
" $R
  ./peel file:runs/grid/disc-$R.pts 0 0 -plain -vertices | sed "s/^{/{\"kind\":\"disc\",\"size\":$R,/" > runs/grid/disc-$R.json
  rm -f runs/grid/disc-$R.pts
done
for S in 250 500 1000 2000; do
  ./peel grid $S 0 -plain -vertices | sed "s/^{/{\"kind\":\"square\",\"size\":$S,/" > runs/grid/square-$S.json
done
echo done
