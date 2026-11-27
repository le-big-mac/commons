# Does the frozen library give for 2024 what dawn_recheck.py gave? Run: ~/ipd/.venv/bin/python -I src/dawnlib_check.py > dawnlib_check.out
import importlib.util
spec = importlib.util.spec_from_file_location('dawnlib', '/home/agent1/night/src/dawnlib.py'); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
N = L.load(2024, '/home/agent1/night/data/ida'); F = L.figures(N)
print(f"2024 by the frozen library: moonless covered nights {len(N)}; clear {sum(1 for c in N if c['clear'])}; cleaned {F['nights']}")
print(f"   the last tenth the darkest: {F['last']:.1f} in 100; the darkest tenth in the second half: {F['second']:.1f}; by tenth {F['by_tenth']}")
for k in ('lit', 'between', 'dark'): print(f"   darker before dawn than after dusk, {k}: {F['before_' + k][0]:.0f} in 100 ({F['before_' + k][1]} of {F['before_' + k][2]})")
print(f"   Nerpio and Arkaroola together: {F['before_two_darkest'][0]:.0f} in 100 ({F['before_two_darkest'][1]} of {F['before_two_darkest'][2]}); Otlica and Ager together: {F['before_otlica_ager'][0]:.0f} in 100 ({F['before_otlica_ager'][1]} of {F['before_otlica_ager'][2]})")
print(f"   the five towns, last tenth the darkest or within 0.02 of it: summer {F['towns_summer'][0]:.0f} in 100 ({F['towns_summer'][1]} of {F['towns_summer'][2]}); winter {F['towns_winter'][0]:.0f} in 100 ({F['towns_winter'][1]} of {F['towns_winter'][2]})")
print("   Milky Way, middle value at the four dark stations: " + "; ".join(f"{L.NAME[st]} {v[0]:.0f} ({v[1]} nights)" for st, v in F['milky'].items()))
print("   station: nights, last tenth darkest, second half, darker before dawn")
for st, v in F['stations'].items(): print(f"      {st:<9} {L.NAME[st]:<18} {v[0]:3d} {v[1]:3d} {v[2]:3d}   {v[3][1]} of {v[3][2]}")
