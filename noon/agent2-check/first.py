"""The first runs' records (lyap.py: REBOUND's MEGNO and its built-in Lyapunov estimate, with the energy error).
usage: python -I first.py run_dt8_seed1.txt run_dt8_seed2.txt run_dt4_seed3.txt        (26 November 2026)"""
import sys, re

if __name__ == '__main__':
    for f in sys.argv[1:]:
        rows = []
        for line in open(f):
            m = re.match(r'([\d.]+) Myr\s+megno ([\d.]+)\s+lyapunov time (\S+) Myr\s+dE/E (\S+)', line)
            if m:
                rows.append((float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))
        at = lambda x: min(rows, key=lambda r: abs(r[0] - x))
        last = rows[-1][0]
        marks = [x for x in (10, 20, 30, 40, 50, 60) if x <= last + 1e-9]
        print(f"{f}: {len(rows)} rows, to {last:.1f} Myr")
        print("  MEGNO at " + ", ".join(str(x) for x in marks) + " Myr: " + ", ".join(f"{at(x)[1]:.2f}" for x in marks)
              + f"; smallest and largest over the run {min(r[1] for r in rows):.2f} and {max(r[1] for r in rows):.2f}")
        print("  the built-in Lyapunov time at the same marks, Myr: " + ", ".join(("none" if at(x)[2] == float('inf') else f"{at(x)[2]:.0f}") for x in marks))
        e = sorted(r[3] for r in rows)
        print(f"  relative energy error at the {len(rows)} rows: median {e[len(e) // 2]:.1e}, largest {e[-1]:.1e}")
