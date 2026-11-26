# Look for bad stretches: the five largest and smallest monthly anomalies (rule L) at each gauge, 1990-2026.
import sys, io, contextlib, importlib.util
spec = importlib.util.spec_from_file_location('trace', '/home/agent1/trace/src/trace.py')
T = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(T)
for sid, name, lat in T.G:
    if name not in T.fit: continue
    a = sorted((T.anom(name, y, m), y, m) for (y, m) in T.mon[name] if 1990 <= y <= 2026)
    print(f"{name:<14} top: " + ", ".join(f"{v:.1f} ({y}-{m:02d})" for v, y, m in a[-5:][::-1]) + " | bottom: " + ", ".join(f"{v:.1f} ({y}-{m:02d})" for v, y, m in a[:3]))
print()
print("San Francisco 2024 monthly means (cm) and anomalies:", [(m, round(T.mon['San Francisco'].get((2024, m), float('nan')), 1), round(T.anom('San Francisco', 2024, m) or float('nan'), 1)) for m in range(1, 13)])
