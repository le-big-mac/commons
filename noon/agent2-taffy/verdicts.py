"""Verdicts on the ten sealed expectations, by the letter.   usage: python verdicts.py sheet.json results.json"""
import sys, json, math
import numpy as np
R = json.load(open(sys.argv[1])); V = {}; M = {}
g = lambda k: R[k]['growth']
gold2, silver2 = (3 + math.sqrt(5)) / 2, 3 + 2 * math.sqrt(2)
V['T1'] = abs(g('T1') - gold2) <= 0.001; M['T1'] = f"{g('T1'):.5f} against {gold2:.5f}"
V['T2'] = abs(g('T2') - silver2) <= 0.001; M['T2'] = f"{g('T2'):.5f} against {silver2:.5f}"
L = R['T3']['lengths']; V['T3'] = L[3] == L[0] and L[6] == L[0] and L[9] == L[0]; M['T3'] = f"word lengths over nine periods: {L[:10]}"
root = max(x.real for x in np.roots([1, -2, 0, -2, 1]) if abs(x.imag) < 1e-12)
V['T4'] = abs(g('T4') - 2.2966) <= 0.001; M['T4'] = f"{g('T4'):.5f} against 2.2966 (the root is {root:.5f})"
V['T5'] = abs(g('T5') - (2 + math.sqrt(3))) <= 0.001; M['T5'] = f"{g('T5'):.5f} against {2 + math.sqrt(3):.5f}"
V['T6'] = abs(g('T6') - silver2) <= 0.001; M['T6'] = f"{g('T6'):.5f} against {silver2:.5f}"
F2 = R['flow_T2']['L']; V['T7'] = 5.5 <= F2[4] / F2[3] <= 7.5; M['T7'] = f"L4/L3 = {F2[4] / F2[3]:.3f} (ratios {', '.join(f'{b / a:.2f}' for a, b in zip(F2, F2[1:]))})"
F3 = R['flow_T3']['L']; V['T8'] = F3[6] < 30 * F3[0]; M['T8'] = f"L6/L0 = {F3[6] / F3[0]:.2f}"
V['T9'] = all(abs(R[k]['burau'] - g(k)) <= 0.001 for k in ('T1', 'T2')); M['T9'] = f"Burau {R['T1']['burau']:.5f} and {R['T2']['burau']:.5f} against growth {g('T1'):.5f} and {g('T2'):.5f}"
V['T10'] = g('T4') - R['T4']['burau'] > 0.01; M['T10'] = f"Burau {R['T4']['burau']:.5f} against growth {g('T4'):.5f}"
for k in sorted(V, key=lambda k: int(k[1:])):
    print(f"{k:4s} {'held  ' if V[k] else 'failed'}  {M[k]}")
print("Burau numbers of the other devices: " + ", ".join(f"{k} {R[k]['burau']:.5f} (growth {g(k):.5f})" for k in ('T3', 'T5', 'T6')))
json.dump(dict(verdicts={k: bool(v) for k, v in V.items()}, measured=M), open(sys.argv[2], 'w'), indent=1)
