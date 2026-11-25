"""Score the eleven expectations of predictions-hemi.md by the letter. Written before hemi_run.py had printed anything.

usage: score_hemi.py OUT_DIR CONFLUENCES_ON_LAND
(the second argument is the count printed by confluence.py for 1:10m land without ice shelves)
"""
import json
import sys

res = json.load(open(f'{sys.argv[1]}/results.json'))
conf = int(sys.argv[2])
L = res['land10']
rows = []


def add(name, held, what):
    rows.append((name, held, what))
    print(f'{name}: {"HELD" if held else "FAILED"} - {what}')


add('H1', L['km_from_nantes'] <= 150, f"c* = {L['lat']:.3f}, {L['lon']:.3f} is {L['km_from_nantes']:.0f} km from Nantes (limit 150)")
add('H2', 0.795 <= L['share'] <= 0.820, f"L(c*) = {100 * L['share']:.3f}% (79.5 to 82.0)")
d = 100 * (L['share'] - L['L_nantes'])
add('H3', d < 0.05, f"L(c*) - L(Nantes) = {d:.4f} percentage points (limit 0.05)")
S = res['shelves']
add('H4', S['same_point'], f"with ice shelves the centre is {S['km_from_cstar']:.3f} km from c* (must be the same point); overlap of shelves with land {S['overlap_km2']:,.0f} km2")
add('H5', res['land110']['km_from_cstar'] <= 100, f"1:110m centre is {res['land110']['km_from_cstar']:.0f} km from the 1:10m centre (limit 100)")
add('H6', 20897 <= conf <= 22189, f"{conf} whole-degree points on 1:10m land (20,897 to 22,189; remembered 21,543)")
P = res['people']
add('H7', 0.92 <= P['share'] <= 0.95, f"largest P(c) = {100 * P['share']:.3f}% (92.0 to 95.0)")
add('H8a', P['lat'] > 45, f"people centre latitude {P['lat']:.2f} (north of 45)")
add('H8b', 0 <= P['lon'] <= 70, f"people centre longitude {P['lon']:.2f} (0 to 70 E)")
add('H9', 0.905 <= P['P_cstar'] <= 0.93, f"people in the land hemisphere: {100 * P['P_cstar']:.3f}% (90.5 to 93.0)")
T = res['tokyo']
add('H10', T['km_from_boundary'] <= 150, f"Tokyo is {T['km_from_boundary']:.0f} km {'inside' if T['inside'] else 'outside'} the boundary (limit 150)")
Hf = res['half']
add('H11a', 3200 <= Hf['radius_km'] <= 3400, f"half of humanity in a cap of radius {Hf['radius_km']:.0f} km (3,200 to 3,400)")
add('H11b', Hf['km_from_quah'] <= 500, f"its centre {Hf['lat']:.2f}, {Hf['lon']:.2f} is {Hf['km_from_quah']:.0f} km from 21.7 N, 99.4 E (limit 500)")
print(f"held {sum(1 for r in rows if r[1])} of {len(rows)}")
