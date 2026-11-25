import json, math, sys
sys.path.insert(0, '/home/agent3/antikythera')
from fractions import Fraction as F
R = json.load(open('/home/agent3/antikythera/results-S.json'))
ft, fn = R['fit']['then']['moon'], R['fit']['now']['moon']
print({k: v for k, v in ft.items() if not isinstance(v, list)})
print({k: v for k, v in fn.items() if not isinstance(v, list)})
ta, tb = 1646667.5, 2461368.0
dn = R['dn']
D2R = math.pi/180
def q(a, e):
    a = a*D2R
    return math.atan2(-e*math.sin(a), 1+e*math.cos(a))/D2R
wrap = lambda x: (x+180) % 360 - 180
MOON = 254/19; APS = 9*53/(19*223)
L = ft['L0'] + ft['r']*(ta-ft['tref']) + 360*MOON*dn
A = ft['A0'] + ft['rA']*(ta-ft['tref']) + 360*APS*dn
Ln = fn['L0'] + fn['r']*(tb-fn['tref'])
An = fn['A0'] + fn['rA']*(tb-fn['tref'])
today = json.load(open('/home/agent3/antikythera/today.json'))
ptr, sky = today['moon']
print('pointer by my sum %.3f, today.json %.3f; sky %.3f' % ((L+q(L-A, ft['e'])) % 360, ptr, sky))
print('mean Moon: gears minus sky fit  %+.3f' % wrap(L-Ln))
print('apsides:   gears minus sky fit  %+.3f' % wrap(A-An))
print('equation of centre: gears %+.3f (anomaly %.1f), sky fit %+.3f (anomaly %.1f); difference %+.3f' % (q(L-A, ft['e']), (L-A) % 360, q(Ln-An, fn['e']), (Ln-An) % 360, q(L-A, ft['e'])-q(Ln-An, fn['e'])))
print('   of which: had the apsides not drifted (gears anomaly with sky apsides): %+.3f' % (q(L-An, ft['e'])-q(Ln-An, fn['e'])))
print("theory's own error today (sky fit minus sky) %+.3f" % wrap(Ln+q(Ln-An, fn['e'])-sky))
print('sum %+.3f; pointer minus sky %+.3f' % (wrap(L-Ln)+q(L-A, ft['e'])-q(Ln-An, fn['e'])+wrap(Ln+q(Ln-An, fn['e'])-sky), wrap(ptr-sky)))
