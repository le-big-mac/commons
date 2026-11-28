"""The limiting constants K_same, K_other (see kdec.py) for the decorations that the heuristic predicts are large:
one element in each nonzero class modulo each of several primes (odd total size: K_other), and pairs (K_same)."""
import sys
sys.path.insert(0, '/home/agent3/lean/lift-check/even/asym'); sys.path.insert(0, '/home/agent3/lean/lift-check/even/shares')
from kdec import K
from minshare import red_matrix
def show(n, name, D):
    R, blocks = red_matrix(n); ks, ko = K(R, blocks, D)
    print(f"Z_{n}  {name}  D = {sorted(D)}:  K_same = {ks} = {float(ks):.6f}   K_other = {ko} = {float(ko):.6f}", flush=True)
show(3, "one element in each nonzero class modulo 3", [1, 2])
show(15, "… modulo 3 and 5", [10, 5, 3, 6, 9, 12])
show(105, "… modulo 3, 5 and 7", [70, 35, 21, 42, 63, 84, 15, 30, 45, 60, 75, 90])
show(3, "two elements in each nonzero class modulo 3", [1, 1, 2, 2])
show(3, "four elements in each nonzero class modulo 3", [1, 1, 1, 1, 2, 2, 2, 2])
show(9, "pairs at 1, 2, 3, 6 modulo 9", [1, 1, 2, 2, 3, 3, 6, 6])
show(45, "the same in Z_45 (multiples of 5)", [10, 10, 20, 20, 30, 30, 15, 15])
show(45, "… with pairs in each nonzero class modulo 5 (multiples of 9)", [10, 10, 20, 20, 30, 30, 15, 15, 9, 9, 18, 18, 27, 27, 36, 36])
