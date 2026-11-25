"""pagecases.py: the states the page is tried in, with what lantern.py says the page must show in each.   python -I pagecases.py OUT.json"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lantern as L
MECH = {'right': dict(a=11.0), 'plate': dict(a=3.73, a2=3.67, b=3.50, p=1.84, e=0.0), 'words': dict(a=11.0, a2=math.sqrt(120.0), b=math.sqrt(120.0)), 'nhigh': dict(a=11.0, yN=0.1), 'lhigh': dict(a=11.0, yL=0.02), 'none': None}
STATES = [('right', 1.0), ('right', 1.5), ('right', 5.0), ('right', 10.0), ('right', 20.0), ('plate', 2.0), ('plate', 3.0), ('plate', 4.0), ('plate', 8.0), ('words', 1.0), ('words', 2.0), ('words', 5.0), ('words', 10.0), ('words', 20.0), ('nhigh', 2.0), ('nhigh', 5.0), ('nhigh', 10.0), ('lhigh', 5.0), ('lhigh', 10.0), ('lhigh', 20.0), ('none', 2.0), ('none', 5.0), ('none', 10.0), ('none', 20.0)]
def expect(mech, m, shade):
    D = L.D_of_m(m); want = L.focus(D)[0]; kw = MECH[mech]; x0 = 0.833 if shade else None
    if kw is None: s = L.focus(L.D_of_m(5.0))[0]
    else:
        s = L.Rods(**kw).lens(D)
        if s is not None and s <= 1: s = None
    out = {'mech': mech, 'm': m, 'shade': shade, 'D': D, 'want': want, 's': s, 'jam': s is None, 'rods': None if kw is None else [kw['a'], kw.get('a2', kw['a']), kw.get('b', math.sqrt(kw['a'] ** 2 - 1))]}
    if s is not None: out.update(patch=L.blur(D, s), size=(D - s) / s, light10=L.light(m, s, x0) / L.light(10.0, L.focus(L.D_of_m(10.0))[0], x0))
    return out
if __name__ == '__main__':
    cases = [expect(mech, m, shade) for mech, m in STATES for shade in (False, True)]; json.dump(cases, open(sys.argv[1], 'w'), indent=0); print('%d states, %d of them jammed' % (len(cases), sum(c['jam'] for c in cases)))
