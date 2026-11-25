"""Reads results.txt and prints the curves and what the sealed lines need.   usage: python -I analyse.py results.txt results.json"""
import sys, json
R = {}
for line in open(sys.argv[1]):
    _, mode, r, mean, end, doves, dn = line.split(); R.setdefault(mode, {})[round(float(r), 2)] = dict(mean=float(mean), end=float(end), doves=int(doves), dn=float(dn))
L4, L8, S4, MX = R['lattice4'], R['lattice8'], R['sync4'], R['mixed4']; grid = sorted(L4)
print("r     well mixed   4 neighbours   8 neighbours   all at once (4)     doves left at the end (4 nb)")
for r in grid: print(f"{r:.2f}    {1 - r:.2f}        {L4[r]['mean']:.4f}         {L8[r]['mean']:.4f}         {S4[r]['mean']:.4f}              {L4[r]['doves']}")
out = {}
print("\nH1. well-mixed control: " + "; ".join(f"r = {r}: {MX[r]['mean']:.4f} (1 - r = {1 - r:.2f})" for r in sorted(MX))); out['H1'] = max(abs(MX[r]['mean'] - (1 - r)) for r in MX)
print(f"H2. four neighbours: r = 0.10: {L4[0.10]['mean']:.4f}; r = 0.20: {L4[0.20]['mean']:.4f}"); out['H2'] = min(L4[0.10]['mean'], L4[0.20]['mean'])
print(f"H3. r = 0.5: {L4[0.50]['mean']:.4f}"); out['H3'] = L4[0.50]['mean']
ext = [r for r in grid if L4[r]['doves'] == 0]; print(f"H4. smallest r with no dove left at the end: {min(ext) if ext else None}; largest r with doves left: {max(r for r in grid if L4[r]['doves'] > 0)}"); out['H4'] = min(ext) if ext else None
below = [r for r in grid if L4[r]['mean'] < 1 - r]; print(f"H5. first r at which the lattice share is below 1 - r: {min(below)}; r at which it is not below: {[r for r in grid if L4[r]['mean'] >= 1 - r]}"); out['H5'] = min(below)
print(f"H6. eight neighbours, r = 0.5: {L8[0.50]['mean']:.4f}"); out['H6'] = L8[0.50]['mean']
print(f"H7. all at once against one at a time: r = 0.3: {S4[0.30]['mean']:.4f} against {L4[0.30]['mean']:.4f}; r = 0.5: {S4[0.50]['mean']:.4f} against {L4[0.50]['mean']:.4f}"); out['H7'] = max(abs(S4[r]['mean'] - L4[r]['mean']) for r in (0.30, 0.50))
e = L4[0.50]; print(f"H8. r = 0.5 at the end: a dove has {e['dn']:.3f} dove neighbours on average; 4 x share = {4 * e['end']:.3f}"); out['H8'] = e['dn'] - 4 * e['end']
out['curves'] = {m: [(r, R[m][r]['mean'], R[m][r]['end'], R[m][r]['doves'], R[m][r]['dn']) for r in sorted(R[m])] for m in R}
json.dump(out, open(sys.argv[2], 'w'), indent=1)
