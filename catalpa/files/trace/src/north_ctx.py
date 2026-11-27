# Context for north.out, not sealed: on all days of August-October 1950-2025, how closely does the sum at San
# Francisco and Crescent City follow San Diego's? Run: ~/ipd/.venv/bin/python -I src/north_ctx.py > north_ctx.out
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
def load(name):
    spec = importlib.util.spec_from_file_location(name, f'/home/agent1/trace/src/{name}.py'); m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
    return m
N = load('north'); S = N.S; summ = N.summ
days = [dt.date(y, 8, 1) + dt.timedelta(days=k) for y in range(1950, 2026) for k in range(92)]
print("ALL DAYS OF AUGUST-OCTOBER 1950-2025: the sum at another gauge on day t + lag against San Diego's on day t")
for name in ("La Jolla", "San Francisco", "Crescent City"):
    for L in (0, 1, 2, 3, 4, 6):
        p = [(summ("San Diego", d), summ(name, d + dt.timedelta(days=L))) for d in days]; p = np.array([q for q in p if q[0] is not None and q[1] is not None])
        r = np.corrcoef(p[:, 0], p[:, 1])[0, 1]; slope = np.polyfit(p[:, 0], p[:, 1], 1)[0]
        big = p[p[:, 0] >= 10]; mid = p[(p[:, 0] >= 5) & (p[:, 0] < 10)]
        print(f"   {name:<14} lag {L}: {len(p)} days; correlation {r:.2f}; slope {slope:.2f} cm per cm; where San Diego's sum is 10 or more ({len(big)} days): mean {big[:, 1].mean():+.1f}; 5 to 10 ({len(mid)} days): mean {mid[:, 1].mean():+.1f}")
