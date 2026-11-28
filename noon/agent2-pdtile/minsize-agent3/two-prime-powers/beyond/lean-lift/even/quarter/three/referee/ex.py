import sys
sys.path.insert(0, "/home/agent3/lean/lift-check/even/quarter/three")
from badlib import bad_count
from fractions import Fraction as F
for n, B, want in [(15, [0,1,2,3,9], F(1,4)), (105, [0,1,2,3,39,75,90], F(7,32)), (3, [0,0,1,1,2,2], F(11,32)), (3, [0,0,0,0,1,1,2,2], F(39,128)), (3, [0,1,2], F(1,4))]:
    cnt, m = bad_count(n, B)
    print(n, B, F(cnt, 2**m), want, F(cnt, 2**m) == want)
