"""The three implementations of the bounding recursion (rec3.py: integers; test3.py and combine.py: fractions, written
separately) give the same xi(m) for every m <= M.   usage: crosscheck.py M"""
import sys, runpy, io, contextlib
M = int(sys.argv[1])
sys.argv = ['rec3.py', str(M)]
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path('rec3.py')
import test3, combine
x1 = g['xi']; x2 = test3.recursion(M); x3 = combine.recursion(M)
same = all(x1[m] == x2[m] == x3[m] for m in range(0, M + 1))
print(f"xi(m) from rec3.py, test3.py, combine.py equal for every m <= {M}: {same}")
