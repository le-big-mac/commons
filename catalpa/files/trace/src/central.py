# Quepos and Acajutla (too short for rule L), and Cocos Island: monthly means minus the gauge's own mean for
# that calendar month over all years to 2025 (no trend taken out), and yearly means to show any step.
# Exploration after the sealed lines were scored.
import sys, io, contextlib, importlib.util, csv, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
extra = {"Cocos Island": T.monthly(T.load("392"))}
for name in ("Quepos", "Acajutla", "Cocos Island"):
    m = T.mon.get(name) or extra[name]
    clim = {mm: np.mean([v for (y, k), v in m.items() if k == mm and y <= 2025]) for mm in range(1, 13)}
    yrs = sorted({y for y, k in m})
    print(f"\n{name}: monthly mean minus own mean of that calendar month (all years to 2025), cm")
    print("year " + "".join(f"{c:>6}" for c in "JFMAMJJASOND") + "   year mean (months)")
    for y in yrs:
        vals = [m.get((y, k)) for k in range(1, 13)]
        a = [None if v is None else v - clim[k + 1] for k, v in enumerate(vals)]
        ok = [x for x in a if x is not None]
        print(f"{y} " + "".join(T.f(x) for x in a) + f"   {np.mean(ok):6.1f} ({len(ok)})")
