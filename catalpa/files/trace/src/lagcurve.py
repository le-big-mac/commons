# The whole curve of correlation against lag (after Santa Cruz), 2026 and 1997, same daily method as trace.py.
# Exploration: shows how flat the peaks are.
import sys, io, contextlib, importlib.util
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
for y in (2026, 1997):
    a, i0, i1 = T.series("Santa Cruz", y)
    names = ["La Libertad", "Quepos", "Acajutla", "San Diego", "San Francisco", "Neah Bay"] if y == 2026 else ["La Libertad", "Callao", "San Diego", "San Francisco", "Neah Bay", "Ketchikan"]
    print(f"\n{y}: correlation with Santa Cruz at each lag (days after Santa Cruz)")
    print(" lag " + "".join(f"{n[:11]:>12}" for n in names))
    ser = {n: T.series(n, y)[0] for n in names}
    for L in range(-20, 61, 4):
        print(f"{L:4d} " + "".join((lambda c: "           -" if c is None else f"{c:12.2f}")(T.lagcorr(a, ser[n], i0, i1, L)) for n in names))
