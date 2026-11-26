"""Does dilation change any value?  The five-move bound (algebra2.py) and the six-move cost (algebra3.py) computed with and without the
dilation entries, and the five-move bound with only those stacks whose classes all carry one pattern, on the three groups.
usage: dilation_check.py"""
import sys
sys.path.insert(0, '/home/agent3/pq2/rule')
import algebra2, algebra3
from algebra import closure
def variants(mod, p, q):
    Calc = mod.Calc; orig = Calc.stack_entries
    full = Calc(p, q).U
    Calc.stack_entries = lambda self, N: [e for e in orig(self, N) if e[2][0] != 'dil']; no_dil = Calc(p, q).U
    Calc.stack_entries = lambda self, N: [e for e in orig(self, N) if e[2][0] == 'dil']; only_dil = Calc(p, q).U
    Calc.stack_entries = lambda self, N: [e for e in orig(self, N) if e[2][0] == 'dil' or len(set(e[2][3])) == 1]; one_pattern = Calc(p, q).U
    Calc.stack_entries = orig
    return full, no_dil, only_dil, one_pattern
for p, q in ((2, 3), (2, 5), (3, 5)):
    divs, mask, U3, how = closure(p, q)
    f5, n5, o5, s5 = variants(algebra2, p, q); u3 = {P: U3[mask(sorted(P))] for P in f5}
    f6, n6, o6, s6 = variants(algebra3, p, q)
    print(f'(p, q) = ({p}, {q}), 256 patterns: five moves without dilation = five moves: {n5 == f5}; six moves without dilation = six moves: {n6 == f6}; '
          f'dilation without stacking = three moves: {o5 == u3}; stacks whose classes all carry one pattern = three moves: {s5 == u3}')
