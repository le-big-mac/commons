# Supplementary data (not used in any proof): the constant K_same of the brief (program kdec.py of the brief's data
# folder, used as it is) for deeper trees of 3.  usage: kdeep.py case
import sys
sys.path.insert(0, '/home/agent3/lean/lift-check/even/asym'); sys.path.insert(0, '/home/agent3/lean/lift-check/even/shares')
from kdec import K
from minshare import red_matrix
def show(n, name, D):
    R, blocks = red_matrix(n); ks, ko = K(R, blocks, D)
    print(f"Z_{n}  {name}  D = {sorted(D)}:  K_same = {ks} = {float(ks):.6f}   K_other = {ko} = {float(ko):.6f}", flush=True)
case = sys.argv[1]
if case == 'a':
    show(9, "pairs at 1, 2, 3, 6", [1, 1, 2, 2, 3, 3, 6, 6])
    show(27, "pairs at 1, 2, 3, 6, 9, 18", [1, 1, 2, 2, 3, 3, 6, 6, 9, 9, 18, 18])
    show(81, "pairs at 1, 2, 3, 6, 9, 18, 27, 54", [1, 1, 2, 2, 3, 3, 6, 6, 9, 9, 18, 18, 27, 27, 54, 54])
if case == 'b':   # Z_135: the Z_27 pattern (as multiples of 5) and a pair in each nonzero class modulo 5 (multiples of 27)
    D = [5 * b % 135 for b in [1, 1, 2, 2, 3, 3, 6, 6, 9, 9, 18, 18]] + [27, 27, 54, 54, 81, 81, 108, 108]
    show(135, "Z_27 pattern and pairs modulo 5", D)
