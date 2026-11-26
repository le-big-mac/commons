"""The condition on the sealed sheet c-prediction.md: the exact law at orders 6,400 and 6,401 must hold all but 1e-9 of its mass
inside the range computed.   usage: python -I tailcheck.py > tailcheck.out     (about three minutes)"""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'referee'))
from ref_Kkraw import K_law

if __name__ == '__main__':
    for n in (6400, 6401):
        r = K_law(n)
        print(f"order {n}: {len(r['pmf'])} values of the depth computed; mass left beyond them {r['tail']:.3e}; mass computed {r['pmf'].sum():.12f}; smallest step of the survival function {min(r['surv'][:-1] - r['surv'][1:]):.2e}", flush=True)
