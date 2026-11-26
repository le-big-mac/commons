"""The model set beside what is in print (26 November 2026, after a reader with the web found the papers).
usage: python -I beside.py > beside.out      (numpy, scipy; impetus.py beside it; a few seconds)
1. Old measurements: Robins's musket ball and 24-pound shot (1742), Helie's cannonball as Cohen and others (2014) give it.
2. The closed forms of Cohen and others for the range and the best elevation, against the integration.
3. How the place of the top moves with speed: as the logarithm, or as one over it?"""
import os, sys, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import impetus as I

def best(v0, vt):
    r = max((I.fly(v0, vt, e / 2)['range'], e / 2) for e in range(30, 100))
    return r

if __name__ == '__main__':
    print("1. old measurements against the model (constant drag coefficient 0.47, sea-level air)")
    vt, mass, dia = I.sphere(density=11340, diameter=0.75 * 0.0254); v0 = 1700 * 0.3048
    f = I.fly(v0, vt, 45)
    print(f"   Robins's musket ball: lead, 3/4 inch ({1000 * dia:.1f} mm), 1,700 feet a second ({v0:.0f} m/s); terminal velocity {vt:.0f} m/s, ratio {v0 / vt:.2f}")
    print(f"      model at 45 degrees: {f['range']:.0f} m; vacuum {v0 ** 2 / I.G:.0f} m ({v0 ** 2 / I.G / 1609.34:.1f} miles). Robins: 'about 17 miles' in a vacuum, in fact 'short of half a mile' (805 m)")
    print(f"      drag at the muzzle in the model: {(v0 / vt) ** 2:.0f} times the ball's weight. Robins measured about 120 times")
    vt, mass, dia = I.sphere(mass=24 * 0.45359, density=7800); v0 = 1650 * 0.3048
    f = I.fly(v0, vt, 45)
    print(f"   Robins's 24-pound shot: iron, {mass:.2f} kg, 1,650 feet a second ({v0:.0f} m/s); terminal velocity {vt:.0f} m/s, ratio {v0 / vt:.2f}")
    print(f"      model at 45 degrees: {f['range']:.0f} m; vacuum {v0 ** 2 / I.G:.0f} m ({v0 ** 2 / I.G / 1609.34:.1f} miles); model over vacuum {f['range_fraction']:.3f}. Robins: 'about 16 miles' in a vacuum, in fact 'less than three miles' (4,828 m), 'not ... the fifth part'; he cites a measured 2,250 French fathoms ({2250 * 1.949:.0f} m)")
    vt, mass, dia = I.sphere(mass=15.1, density=7800); v0 = 485.0
    r, e = best(v0, vt)
    print(f"   Helie's cannonball as given by Cohen and others: 15.1 kg at 485 m/s; in the model terminal velocity {vt:.0f} m/s, ratio {v0 / vt:.2f} (they give 2.05)")
    print(f"      model: greatest range {r:.0f} m at {e:.1f} degrees; at 37.5 degrees {I.fly(v0, vt, 37.5)['range']:.0f} m. Measured, as they give it: 5,690 m at 37.5 degrees")
    cd = lambda mach: 0.47 if mach < 0.6 else (0.95 if mach > 1.1 else 0.47 + (0.95 - 0.47) * (mach - 0.6) / 0.5)    # the sketch of after.py
    for name, (vt, v0), measured in (("Robins's musket ball", (I.sphere(density=11340, diameter=0.75 * 0.0254)[0], 1700 * 0.3048), "'short of half a mile' (805 m), by the writers he cites"),
                                     ("Robins's 24-pound shot", (I.sphere(mass=24 * 0.45359, density=7800)[0], 1650 * 0.3048), "4,385 m")):
        print(f"   {name} with my sketched rise of drag near the speed of sound (0.47 below Mach 0.6, 0.95 above Mach 1.1): {I.fly(v0, vt, 45, cd_of_mach=cd)['range']:.0f} m at 45 degrees; reported {measured}")
    vt205 = 485.0 / 2.05; r, e = best(485.0, vt205)
    print(f"   Helie's cannonball with the paper's own ratio of 2.05 (terminal velocity {vt205:.0f} m/s, a drag coefficient of {0.47 * (I.sphere(mass=15.1, density=7800)[0] / vt205) ** 2:.2f} for 15.1 kg of iron): greatest range {r:.0f} m at {e:.1f} degrees; measured 5,690 m at 37.5")
    vt47 = I.sphere(mass=15.1, density=7800)[0]
    for c in (0.30, 0.33, 0.36):
        vtc = vt47 * math.sqrt(0.47 / c); r, e = best(485.0, vtc); at = I.fly(485.0, vtc, 37.5)['range']
        print(f"   the same ball with a drag coefficient of {c:.2f} (ratio {485.0 / vtc:.2f}): {at:.0f} m at 37.5 degrees; greatest range {r:.0f} m at {e:.1f} degrees ({100 * (1 - at / r):.1f}% more than at 37.5)")
    print(f"   an iron ball of 8 cm, the diameter the paper prints, would weigh {7800 * math.pi * 0.08 ** 3 / 6:.1f} kg, not 15.1")
    print("   the musket ball's place between the two pictures at other elevations (area under the path over range squared; parabola tan(a)/6, straight out and straight down tan(a)/2):")
    s = I.SHOTS['musket ball']; row = []
    for el in (15, 30, 45, 60, 75):
        f = I.fly(s['v0'], s['vt'], el, dense=True, max_step=0.05); pts = f['path']; t = math.tan(math.radians(el))
        a = sum((x2 - x1) * (y1 + y2) / 2 for (x1, y1), (x2, y2) in zip(pts, pts[1:])) / f['range'] ** 2
        row.append(f"{el} degrees: {(a - t / 6) / (t / 2 - t / 6):.2f}")
    print("      " + ";  ".join(row))
    print("2. Cohen and others' closed forms, with L = vt^2/g and X = (v0/vt)^2:  range = (L/2) cos(a) ln(1 + 4 X sin(a));  best elevation = arctan sqrt(X / ((1 + X) ln(1 + X)))")
    for name, s in I.SHOTS.items():
        v0, vt = s['v0'], s['vt']; L = vt ** 2 / I.G; X = (v0 / vt) ** 2; a = math.radians(45)
        formula = 0.5 * L * math.cos(a) * math.log(1 + 4 * X * math.sin(a)); model = I.fly(v0, vt, 45)['range']
        r, e = best(v0, vt)
        print(f"   {name:16s} ratio {v0 / vt:5.2f}: range at 45 degrees, formula {formula:7.0f} m, integration {model:7.0f} m ({100 * (formula / model - 1):+.0f}%); best elevation, formula {math.degrees(math.atan(math.sqrt(X / ((1 + X) * math.log(1 + X))))):.1f}, integration {e:.1f}")
    print("3. the place of the top, as a share of the range, at 45 degrees")
    prev = None
    for ratio in (1, 3, 6.61, 10, 100, 1000, 10000):
        f = I.fly(ratio * 50.0, 50.0, 45); ap = f['apex_fraction']
        print(f"   {ratio:8.2f} terminal velocities: top at {ap:.3f}; left to the far end {1 - ap:.3f}; 1/(1 - top) = {1 / (1 - ap):.2f}; ln(ratio) = {math.log(ratio):.2f}; what is left times ln(ratio) = {(1 - ap) * math.log(ratio):.2f}")
