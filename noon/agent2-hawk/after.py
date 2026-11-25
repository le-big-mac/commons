"""Prints the checks made afterwards from after-results.txt and the time courses.   usage: python -I after.py after-results.txt after"""
import sys, os
R = {}
for line in open(sys.argv[1]):
    p = line.split(); R[p[0]] = dict(mode=p[2], r=float(p[3]), mean=float(p[4]), end=float(p[5]), doves=int(p[6]), dn=float(p[7]))
def get(tag): return sorted((v['r'], v) for k, v in R.items() if k.startswith(tag + '-'))
def series(name):
    return [(int(l.split()[1]), float(l.split()[2])) for l in open(os.path.join(sys.argv[2], name + '.out')) if l.startswith('t ')]
print("A. Where the all-but-all-dove state gives way. By hand: a hawk with one hawk neighbour out-earns a dove with two when (k - 1)(1 + r) > k - 2r, that is r > 1/(k + 1): 0.200 for four neighbours, 0.111 for eight")
print("   four neighbours:  " + "; ".join(f"r = {r:.3f}: {v['mean']:.4f}" for r, v in get('A') if v['mode'] == 'lattice4'))
print("   eight neighbours: " + "; ".join(f"r = {r:.3f}: {v['mean']:.4f}" for r, v in get('A') if v['mode'] == 'lattice8'))
print("B. Started with 1% hawks in place of 50% (four neighbours): dove share over generations 10,001 to 15,000, and at the end")
print("   " + "; ".join(f"r = {r:.2f}: {v['mean']:.4f}, {v['end']:.4f}" for r, v in get('B')))
print("C. Four times as long (60,000 generations): the dove share at 15,000, 30,000 and 60,000 generations")
for r, v in get('C'):
    s = dict(series(f"C-lattice4-{r:.2f}-L200-s9")); print(f"   r = {r:.2f}: {s[15000]:.4f}, {s[30000]:.4f}, {s[60000]:.4f}; hawks: {1 - s[15000]:.4f}, {1 - s[30000]:.4f}, {1 - s[60000]:.4f}")
print("D. Near the point where the doves die out: doves left after 30,000 generations, three more seeds (the first run, 15,000 generations, is in results.txt)")
for r in (0.60, 0.62, 0.64, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76):
    print(f"   r = {r:.2f}: " + ", ".join(str(R[f'D{sd}-lattice4-{r:.2f}-L200-s{sd}']['doves']) for sd in (11, 12, 13)) + "   mean share over the last 5,000: " + ", ".join(f"{R[f'D{sd}-lattice4-{r:.2f}-L200-s{sd}']['mean']:.4f}" for sd in (11, 12, 13)))
print("E. A lattice four times as large (400 x 400): " + "; ".join(f"r = {r:.2f}: {v['mean']:.4f}" for r, v in get('E')))
print("F. Two more seeds at 200 x 200: " + "; ".join(f"r = {r:.2f}: {v['mean']:.4f}" for r, k, v in sorted((v['r'], k, v) for k, v in R.items() if k.startswith('F-'))))
