"""ruler-control.py -- could the comparison of ruler.py fail?  One of its cases again, with slow.py given a P one part in three thousand
larger (3.001 for 3), and again with slow.py given a cutoff distance of 0.401 for 0.4.  If the two programs were not being compared
closely these would pass.   usage: python ruler-control.py"""
import subprocess, sys
py = sys.executable; start = "out/ruler/P3-dc0.4-L40-s7.start"
a = subprocess.run(["./river", "3", "0.4", "40", "30", "7", "-start", start, "-out", "1"], capture_output=True, text=True).stdout
ra = [l.split() for l in a.split("\n") if l and not l.startswith("#")]
for label, P, DC in (("P = 3.001 for 3", "3.001", "0.4"), ("cutoff distance 0.401 for 0.4", "3", "0.401")):
    b = subprocess.run([py, "-I", "slow.py", P, DC, "40", "30", start, "0.1"], capture_output=True, text=True).stdout
    rb = [l.split() for l in b.split("\n") if l and not l.startswith("#")]
    first = next((int(float(u[0])) for u, v in zip(ra, rb) if u[1] != v[1] or u[3] != v[3] or abs(float(u[2]) - float(v[2])) > 2e-5 or abs(float(u[4]) - float(v[4])) > 0.01), None)
    worst = max(abs(float(u[2]) - float(v[2])) for u, v in zip(ra, rb))
    print("slow.py given %s: %s; greatest difference in length/LX %.1e" % (label, ("the two differ from t = %d on" % first) if first is not None else "NO DIFFERENCE FOUND", worst))
