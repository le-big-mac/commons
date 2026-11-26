# The tropics against San Diego, month by month, for each event: rule L anomalies (cm).
# 'tropics' = mean of La Libertad and Santa Cruz. San Diego's October 2026 is from october.out (NOAA's hourly heights).
# Exploration after the sealed lines were scored.
import sys, io, contextlib, importlib.util
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
def trop(y, m):
    a, b = T.anom("La Libertad", y, m), T.anom("Santa Cruz", y, m)
    return None if a is None or b is None else (a + b) / 2
extra = {("San Diego", 2026, 10): 33.0, ("San Francisco", 2026, 10): 25.8}
def g(name, y, m): return extra.get((name, y, m), T.anom(name, y, m))
for y0 in (1982, 1991, 1997, 2009, 2015, 2023, 2026):
    months = [(y0, m) for m in range(4, 13)] + [(y0 + 1, m) for m in range(1, 7)]
    print(f"\n{y0}-{y0+1}        " + "".join(f"{'AMJJASONDJFMAMJ'[i]:>6}" for i in range(15)))
    print("tropics         " + "".join(T.f(trop(y, m)) for y, m in months))
    print("San Diego       " + "".join(T.f(g("San Diego", y, m)) for y, m in months))
    print("San Francisco   " + "".join(T.f(g("San Francisco", y, m)) for y, m in months))
    r = []
    for i, (y, m) in enumerate(months):
        if i == 0: r.append(None); continue
        py, pm = months[i - 1]; a, b = g("San Diego", y, m), trop(py, pm)
        r.append(a / b if a is not None and b is not None and b >= 8 else None)
    print("SD / tropics of the month before (where tropics >= 8 cm)\n                " + "".join("     -" if x is None else f"{x:6.2f}" for x in r))
