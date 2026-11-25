"""The real tables through the rulers. usage: run.py DATADIR [S|T ...]
Writes results-<frame>.npz (error series and fitted values) and prints the tables."""
import sys, os, json
import numpy as np
import gears, mech

DATA = sys.argv[1]
FRAMES = sys.argv[2:] or ['S', 'T']
HERE = os.path.dirname(os.path.abspath(__file__))
sky = {w: {b: mech.read(os.path.join(DATA, f'{b}_{w}.txt')) for b in mech.BODIES} for w in ('then', 'now')}
for w in sky:
    for b in sky[w]:
        jd = sky[w][b]['jd']
        print(f'{w:5s} {b:8s} rows {len(jd):6d}  JD {jd[0]:.2f} to {jd[-1]:.2f}  step {jd[1] - jd[0]:.4f} d')
for frame in FRAMES:
    R = mech.analyse(sky, frame)
    yrs = R['years']
    print(f'\n===== frame {frame} =====')
    print(f'span {R["dt"]:.1f} days = {yrs:.3f} Julian years; turns of b1 (the mean Sun) {R["dn"]:.5f}; mean Sun advance {R["sun_advance"]:.4f} deg')
    print('drift over the span (pointer minus sky, degrees), and as degrees per Julian year')
    for k in ('moon', 'apsides', 'node', 'mercury', 'venus', 'mars', 'jupiter', 'saturn'):
        print(f'  {k:8s} {R["drift"][k]:10.3f}   wrapped {float(mech.wrap(R["drift"][k])):8.3f}   {R["drift"][k] / yrs:+.6f}')
    print('planets: synodic rate error (mechanism minus sky), degrees per Julian year, beside the paper\'s printed error')
    for p in gears.SYNODIC:
        syn = R['drift'][p] / yrs if p in gears.INFERIOR else -R['drift'][p] / yrs
        print(f'  {p:8s} {syn:+.6f}   paper {gears.PAPER_EY[p]:+.6f}   ratio of sizes {abs(syn) / abs(gears.PAPER_EY[p]):.3f}')
    print('free fits: then | now: rms, largest (degrees); fitted size; and the ellipse fits\' rms')
    for b in mech.BODIES:
        ft, fn = R['fit']['then'][b], R['fit']['now'][b]
        a, c = mech.stats(ft['res']), mech.stats(fn['res'])
        size = ft.get('e', ft.get('rho')); size2 = fn.get('e', fn.get('rho'))
        extra = ''
        if b in ('sun', 'moon'): extra = f'  arcsin: {np.degrees(np.arcsin(size)):.4f} | {np.degrees(np.arcsin(size2)):.4f} deg'
        kb = 'earth' if b == 'sun' else b
        if kb in R['kep']['then']:
            extra += f'  ellipse rms {mech.stats(R["kep"]["then"][kb]["res"])["rms"]:.4f} | {mech.stats(R["kep"]["now"][kb]["res"])["rms"]:.4f}, e {R["kep"]["then"][kb]["e"]:.5f} | {R["kep"]["now"][kb]["e"]:.5f}'
        print(f'  {b:8s} {a["rms"]:7.4f} {a["max"]:7.3f} | {c["rms"]:7.4f} {c["max"]:7.3f}   size {size:.5f} | {size2:.5f}{extra}')
    print(f'  node: crossings {R["fit"]["then"]["node"]["n"]} | {R["fit"]["now"]["node"]["n"]}; rms about the line {np.std(R["fit"]["then"]["node"]["res"]):.3f} | {np.std(R["fit"]["now"]["node"]["res"]):.3f}')
    err = mech.pointer_now(R, sky, frame)
    print('the mechanism calibrated then, turned by its gears, read over the 76 years to today:')
    print('  body: mean error, rms about zero, largest, error on the last instant (today); rms about zero over floor rms')
    save = {}
    for b in mech.BODIES:
        e = err[b]
        fl = mech.stats(R['fit']['then'][b]['res'])['rms']
        rz = float(np.sqrt(np.mean(e ** 2)))
        print(f'  {b:8s} {np.mean(e):9.3f} {rz:8.3f} {np.max(np.abs(e)):8.3f} {e[-1]:9.3f}   {rz / fl:7.2f}')
        save['err_' + b] = e
        save['jd_' + b] = sky['now'][b]['jd']
        save['res_then_' + b] = R['fit']['then'][b]['res']
        save['jd_then_' + b] = sky['then'][b]['jd']
    np.savez_compressed(os.path.join(HERE, f'results-{frame}.npz'), **save)
    summ = dict(frame=frame, years=yrs, dn=R['dn'], sun_advance=R['sun_advance'], drift=R['drift'],
                fit={w: {b: {k: (float(v) if np.isscalar(v) else None) for k, v in R['fit'][w][b].items() if k != 'res'} for b in R['fit'][w]} for w in R['fit']},
                kep={w: {b: {k: float(v) for k, v in R['kep'][w][b].items() if k != 'res'} for b in R['kep'][w]} for w in R['kep']},
                today={b: float(err[b][-1]) for b in err})
    json.dump(summ, open(os.path.join(HERE, f'results-{frame}.json'), 'w'), indent=1)
