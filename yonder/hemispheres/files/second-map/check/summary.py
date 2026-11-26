"""Compact table of the checker's searches (out/search-*.json) beside the author's best centres (out/*.json of the study).
usage: python -I summary.py CHECK_OUT_DIR AUTHOR_OUT_DIR"""
import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chk
cd, ad = sys.argv[1], sys.argv[2]
names = ['ghs-1975', 'ghs-2000', 'ghs-2005', 'ghs-2010', 'ghs-2015', 'ghs-2020', 'ghs-2025', 'ghs-2030', 'g1-2000', 'g1-2010', 'g1-2020', 'g2-2015', 'g2-2020', 'g2-2025', 'g2-2030']
print('grid | checker: hard-edged best (share, lat, lon) | author: highest of four, soft edge (share, lat, lon, found by) | km between | regional bests relative to checker best, points: Alps (S of 47.5) | Palatinate box | Berlin box | Baltic box | farthest-from-Europe best | Palatinate summit refined')
for n in names:
    s = json.load(open(f'{cd}/search-{n}.json')); a = json.load(open(f'{ad}/{n}.json'))
    cands = [('search', a['best'])] + list(a['climb'].items())
    k, t = max(cands, key=lambda c: c[1]['share'])
    b = s['best']; R = s['regional']
    pal = [x for x in s['summits'] if 48.5 < x['lat'] < 50.0 and 11.5 < x['lon'] < 13.5]
    palt = f"{100 * (pal[0]['share'] - b['share']):+.4f} at {pal[0]['lat']:.2f},{pal[0]['lon']:.2f}" if pal else 'none listed'
    far = s['best_beyond_2000km_of_50N10E']
    print(f"{n} | {100 * b['share']:.4f}% {b['lat']:.2f} {b['lon']:.2f} | {100 * t['share']:.4f}% {t['lat']:.2f} {t['lon']:.2f} ({k}) | {chk.km(b['lat'], b['lon'], t['lat'], t['lon']):.0f} | "
          f"{100 * (R['south_of_47p5']['share'] - b['share']):+.4f} at {R['south_of_47p5']['lat']:.2f},{R['south_of_47p5']['lon']:.2f} | "
          f"{100 * (R['palatinate_48p5_50p5N_11_14E']['share'] - b['share']):+.4f} | {100 * (R['berlin_51_53p5N_11_15E']['share'] - b['share']):+.4f} at {R['berlin_51_53p5N_11_15E']['lat']:.2f},{R['berlin_51_53p5N_11_15E']['lon']:.2f} | "
          f"{100 * (R['baltic_54_59N_13_22E']['share'] - b['share']):+.4f} | {100 * (far['share'] - b['share']):+.3f} | {palt}")
print()
print('grid | all summits found in Europe within 0.10 points (smoothed) of the top: share relative to best, lat, lon')
for n in names:
    s = json.load(open(f'{cd}/search-{n}.json')); b = s['best']
    print(n, '| ' + '; '.join(f"{100 * (x['share'] - b['share']):+.4f} {x['lat']:.2f},{x['lon']:.2f}" for x in s['summits']))
print()
print('grid | connected regions of the 0.25-degree world map within 0.05 points of its best (top share, where)')
for n in names:
    s = json.load(open(f'{cd}/search-{n}.json'))
    print(n, '| ' + '; '.join(f"{100 * r['top_share']:.4f}% at {r['top_lat']:.2f},{r['top_lon']:.2f} ({r['points']} pts)" for r in s['regions_within_0.05']))
