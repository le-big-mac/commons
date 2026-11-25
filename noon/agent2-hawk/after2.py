"""Prints the referee's controls as redone by after2.sh, and two tallies from results.txt.   usage: python -I after2.py after2 results.txt"""
import sys, os
import numpy as np
d = sys.argv[1]
def series(name): return [(int(l.split()[1]), float(l.split()[2])) for l in open(os.path.join(d, name + '.out')) if l.startswith('t ')]
def at(name, gens): s = dict(series(name)); return ", ".join(f"{s[g]:.4f} at {g:,}" for g in gens if g in s)
print("A. Where the nearly all-dove state gives way, on longer runs (dove share at the generations named)")
print("   four neighbours, half and half at the start:")
print("      r = 0.205: " + at("a4-lattice4-0.205-s31", (15000, 30000, 60000, 100000)))
print("      r = 0.210: " + at("a4-lattice4-0.210-s31", (15000, 30000, 60000, 100000)))
print("      r = 0.215: " + at("a4-lattice4-0.215-s31", (15000, 30000, 60000)))
print("   four neighbours, r = 0.215, started with 99.5% doves: " + at("a4dove-lattice4-0.215-s32", (1000, 10000, 20000, 40000)))
print("   eight neighbours, half and half: r = 0.110: " + at("a8-lattice8-0.110-s33", (15000, 30000, 60000)) + ";  r = 0.112: " + at("a8-lattice8-0.112-s33", (15000, 30000, 60000)))
print("   eight neighbours, r = 0.115, started with 99% doves: " + at("a8dove-lattice8-0.115-s34", (1000, 10000, 20000, 30000)))
print("B. Where the doves die out (four neighbours unless said)")
for name, lab in (("d-lattice4-0.67-s41", "r = 0.67, seed 41"), ("d-lattice4-0.67-s42", "r = 0.67, seed 42"), ("d-lattice4-0.66-s43", "r = 0.66"), ("d8-lattice8-0.77-s44", "eight neighbours, r = 0.77")):
    s = series(name); gone = next((g for g, f in s if f == 0.0), None); tail = [f for g, f in s if g > s[-1][0] - 20000]
    print(f"   {lab}: " + (f"no dove left from generation {gone:,}" if gone else f"doves left after {s[-1][0]:,} generations: share {s[-1][1]:.4f} (between {min(tail):.4f} and {max(tail):.4f} over the last 20,000)"))
print("C. Hawks alone and hawks in pairs at generation 15,000 (four neighbours)")
for r in ("0.10", "0.15", "0.20"):
    a = np.fromfile(os.path.join(d, f"p-lattice4-{r}-s51.bin"), dtype=np.uint8)[-40000:].reshape(200, 200); h = 1 - a.astype(int)
    nh = np.roll(h, 1, 0) + np.roll(h, -1, 0) + np.roll(h, 1, 1) + np.roll(h, -1, 1); c = [int(((h == 1) & (nh == k)).sum()) for k in range(5)]
    lone_rate = 5 * float(r) ; back = 1.5 * (1 - 4 * float(r))
    print(f"   r = {r}: {c[0]} hawks with no hawk neighbour, {c[1]} with one, {sum(c[2:])} with more; share with one: {100 * c[1] / max(1, sum(c)):.0f}%")
print("D. All sites at once against one at a time, over the grid (from results.txt)")
R = {}
for line in open(sys.argv[2]):
    _, mode, r, mean, end, doves, dn = line.split(); R.setdefault(mode, {})[round(float(r), 2)] = (float(mean), int(doves))
diff = {r: R['sync4'][r][0] - R['lattice4'][r][0] for r in R['lattice4']}
mid = [r for r in sorted(diff) if 0.22 <= r <= 0.64]; print(f"   r from 0.22 to 0.64: all at once minus one at a time runs from {min(diff[r] for r in mid):+.4f} to {max(diff[r] for r in mid):+.4f}; positive at {sum(diff[r] > 0 for r in mid)} of {len(mid)} values")
print(f"   r = 0.20: {R['sync4'][0.20][0]:.4f} against {R['lattice4'][0.20][0]:.4f}; r = 0.66: {R['sync4'][0.66][0]:.4f} against {R['lattice4'][0.66][0]:.4f} ({R['sync4'][0.66][1]} doves at the end against {R['lattice4'][0.66][1]}); all at once ends with no hawk at r up to {max(r for r in R['sync4'] if R['sync4'][r][1] == 40000):.2f}")
print("E. Eight neighbours not at rest at small r either (first runs): dove share at generations 10,000, 12,500, 15,000")
for r in ("0.08", "0.10"):
    s = dict((int(l.split()[1]), float(l.split()[2])) for l in open(f"runs/lattice8-{r}.out") if l.startswith('t ')); print(f"   r = {r}: {s[10000]:.4f}, {s[12500]:.4f}, {s[15000]:.4f}")
