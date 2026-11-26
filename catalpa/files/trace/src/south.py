# Was the step of 28 September at San Diego seen earlier to the south? Daily values (Hawaii files, tide already
# filtered out by them) at the gauges south of the Mexican gap, 20 August to 30 September 2026, each minus its own
# mean of 1-20 August, cm. Exploration.
import sys, io, contextlib, importlib.util, datetime as dt
import numpy as np
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
names = ["Callao", "La Libertad", "Santa Cruz", "Baltra", "Quepos", "Acajutla", "San Diego", "La Jolla"]
extra = T.load("392")
base = {n: np.mean([v for d, v in T.daily[n].items() if dt.date(2026, 8, 1) <= d <= dt.date(2026, 8, 20)]) for n in names}
print("date        " + "".join(f"{n[:11]:>12}" for n in names))
day = dt.date(2026, 8, 20)
while day <= dt.date(2026, 9, 30):
    print(f"{day}  " + "".join("           -" if day not in T.daily[n] else f"{T.daily[n][day] - base[n]:12.1f}" for n in names))
    day += dt.timedelta(days=1)
