# Forces, not angles: JPL's acceleration of the Moon relative to the Earth (by differencing JPL's velocities) against what MY force model says at JPL's own positions and velocities.
# usage: python -I force_check.py <dir with hz_<day>_<body>.txt> <start day> <lib file with th and pole from my run> <label>
import sys, re, os, subprocess, numpy as np
hzdir, d0, libfile, label = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
BODIES = [10, 199, 299, 399, 301, 4, 5, 6, 7, 8, 9]; AU = 149597870.7; GMEM = (398600.435507 + 4902.800118) * 86400.0 ** 2 / AU ** 3
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
S = [hz(f'{hzdir}/hz_{d0}_{b}.txt') for b in BODIES]; jd = S[0][:, 0]; n = len(jd); h = round((jd[1] - jd[0]) * 1440) / 1440.0; jd = jd[0] + h * np.arange(n); t = jd - 2451545.0     # the step exactly (the printed JDs have nine decimals: taking the step from them put 1.5e-8 into every acceleration - my first run of this)
assert all(len(x) == n for x in S) and abs(h - 1 / 48) < 1e-9
# the Moon's rotation angle and the Earth's pole from my own run, interpolated to JPL's instants
L = np.loadtxt(libfile); L = L[np.argsort(L[:, 0])]; mk = (L[:, 0] >= t[0] - 1) & (L[:, 0] <= t[-1] + 1); L = L[mk]; assert len(L) > 100, 'lib file does not cover the stretch'
rate = np.polyfit(L[:, 0], L[:, 1], 1)[0]; th = np.interp(t, L[:, 0], L[:, 1] - rate * L[:, 0]) + rate * t
pole = np.array([np.interp(t, L[:, 0], L[:, 4 + k]) for k in range(3)]).T
inp = f'/tmp/acc_in_{d0}.txt'
with open(inp, 'w') as f:
    for i in range(n):
        f.write(f'{jd[i]:.9f} ' + ' '.join(' '.join(f'{v:.17e}' for v in S[b][i, 1:]) for b in range(11)) + f' {th[i]:.15e} ' + ' '.join(f'{v:.17e}' for v in pole[i]) + '\n')
def model(extra_env):
    env = dict(os.environ, J2='1', TIDE='195', LFIG='3', POLE='1', CASS='1', K2E='0.30', K2M='0.024', ACCIN=inp); env.update(extra_env)
    out = subprocess.run(['./orrery_acc', 'data/ic.txt', '1', '0.05', '2', '1', 'state'], env=env, capture_output=True, text=True, check=True).stdout
    A = np.array([[float(x) for x in l.split()] for l in out.strip().split('\n')]); return A[:, 4:7] - A[:, 1:4]
# JPL's acceleration: 8th-order central difference of the velocities
c = np.array([1 / 280, -4 / 105, 1 / 5, -4 / 5, 0, 4 / 5, -1 / 5, 4 / 105, -1 / 280]); vE, vM = S[3][:, 4:7], S[4][:, 4:7]
def ddt(v): return sum(c[k + 4] * v[4 + k:n - 4 + k] for k in range(-4, 5)) / h
aj = ddt(vM) - ddt(vE); sl = slice(4, n - 4); r = (S[4][:, 1:4] - S[3][:, 1:4])[sl]; v = (vM - vE)[sl]; tt = t[sl]
rh = r / np.linalg.norm(r, axis=1)[:, None]; hh = np.cross(r, v); hh /= np.linalg.norm(hh, axis=1)[:, None]; th_ = np.cross(hh, rh); a0 = GMEM / (r * r).sum(1)
def comps(x): return np.stack([(x * rh).sum(1), (x * th_).sum(1), (x * hh).sum(1)], 1) / a0[:, None]
print(f'== {label}: {len(tt)} instants over {tt[-1] - tt[0]:.1f} days; residual = JPL acceleration (Moon relative to Earth) - my model at JPL\'s state, in units of 1e-10 of the main attraction')
print('   model variant                                   radial: mean, rms        along-track: mean, rms     out-of-plane: mean, rms')
variants = [('full model', {}), ('  without the in-phase tides', {'K2E': '0', 'K2M': '0'}), ('  without the lagging tide', {'TIDE': '0'}), ("  Moon's figure with long axis on the Earth (LFIG=2)", {'LFIG': '2'}),
            ("  without the Moon's figure", {'LFIG': '0'}), ("  without the Earth's oblateness and all with it (J2 unset)", {'J2': None}), ('  Newton only for the planets (gr=0)', {'GR0': '1'})]
res_full = None
for name, ev in variants:
    if 'GR0' in ev:
        env = dict(os.environ, J2='1', TIDE='195', LFIG='3', POLE='1', CASS='1', K2E='0.30', K2M='0.024', ACCIN=inp)
        out = subprocess.run(['./orrery_acc', 'data/ic.txt', '1', '0.05', '0', '1', 'state'], env=env, capture_output=True, text=True, check=True).stdout
        A = np.array([[float(x) for x in l.split()] for l in out.strip().split('\n')]); am = A[:, 4:7] - A[:, 1:4]
    elif ev.get('J2', '') is None:
        env = dict(os.environ, ACCIN=inp); env.pop('J2', None)
        out = subprocess.run(['./orrery_acc', 'data/ic.txt', '1', '0.05', '2', '1', 'state'], env=env, capture_output=True, text=True, check=True).stdout
        A = np.array([[float(x) for x in l.split()] for l in out.strip().split('\n')]); am = A[:, 4:7] - A[:, 1:4]
    else: am = model(ev)
    q = comps(aj - am[sl]) * 1e10
    if res_full is None: res_full = q
    print(f'   {name:55s} {q[:, 0].mean():+9.2f} {q[:, 0].std():9.2f}      {q[:, 1].mean():+9.2f} {q[:, 1].std():9.2f}      {q[:, 2].mean():+9.2f} {q[:, 2].std():9.2f}')
np.save(f'/tmp/force_res_{d0}.npy', np.c_[tt, res_full, np.arctan2((rh * np.cross(hh, [0, 0, 1.0])).sum(1) * 0 + 0, 1)])
tot = np.sqrt((res_full ** 2).sum(1)); print(f'full model: rms of the whole residual {np.sqrt((res_full ** 2).mean(0).sum()):.2f}e-10; largest {tot.max():.2f}e-10')
np.savetxt(f'force_res_{d0}.txt', np.c_[tt, res_full], fmt='%.6f %.4f %.4f %.4f', header='days from J2000; residual radial, along-track, out-of-plane, in 1e-10 of the main attraction')
