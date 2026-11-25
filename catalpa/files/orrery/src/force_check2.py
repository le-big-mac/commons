# Where does the constant radial residual of 1.485e-8 come from?  (a) Is Horizons' velocity the time-derivative of its position?  (b) Is there the same residual in the Earth's own
# barycentric acceleration (then it is a matter of units or time-scale), or only in Moon-minus-Earth (then it is in the Earth-Moon attraction)?
import sys, re, os, subprocess, numpy as np
hzdir, d0 = sys.argv[1], int(sys.argv[2])
BODIES = [10, 199, 299, 399, 301, 4, 5, 6, 7, 8, 9]; AU = 149597870.7; D = 86400.0
GMS = 132712440041.279419 * D * D / AU ** 3; GMEM = (398600.435507 + 4902.800118) * D * D / AU ** 3
num = r'([-+]?\d\.\d+E[-+]\d+)'
def hz(p):
    b = open(p).read().split('$$SOE')[1].split('$$EOE')[0]
    return np.array([[float(x) for x in m.groups()] for m in re.finditer(r'(\d+\.\d+) = [AB]\.[DC]\..*?\n\s*X\s*=\s*' + num + r'\s*Y\s*=\s*' + num + r'\s*Z\s*=\s*' + num + r'\s*\n\s*VX=\s*' + num + r'\s*VY=\s*' + num + r'\s*VZ=\s*' + num, b)])
S = [hz(f'{hzdir}/hz_{d0}_{b}.txt') for b in BODIES]; n = len(S[0]); h = 1 / 48
c = np.array([1 / 280, -4 / 105, 1 / 5, -4 / 5, 0, 4 / 5, -1 / 5, 4 / 105, -1 / 280]); ddt = lambda v: sum(c[k + 4] * v[4 + k:n - 4 + k] for k in range(-4, 5)) / h; sl = slice(4, n - 4)
print(f'(a) Horizons velocity against the differenced position, relative size of the mismatch (rms over the stretch):')
for name, b in (('Earth', 3), ('Moon', 4), ('Sun', 0)):
    dv = ddt(S[b][:, 1:4]) - S[b][sl, 4:7]; print(f'    {name}: {np.sqrt((dv ** 2).sum(1).mean()) / np.sqrt((S[b][sl, 4:7] ** 2).sum(1).mean()):.2e};   Moon-minus-Earth:' if b == 4 else f'    {name}: {np.sqrt((dv ** 2).sum(1).mean()) / np.sqrt((S[b][sl, 4:7] ** 2).sum(1).mean()):.2e}', end='')
    if b == 4:
        dv = (ddt(S[4][:, 1:4]) - ddt(S[3][:, 1:4])) - (S[4][sl, 4:7] - S[3][sl, 4:7]); vr = S[4][sl, 4:7] - S[3][sl, 4:7]; print(f' {np.sqrt((dv ** 2).sum(1).mean()) / np.sqrt((vr ** 2).sum(1).mean()):.2e}')
    else: print()
A = np.array([[float(x) for x in l.split()] for l in subprocess.run(['./orrery_acc', 'data/ic.txt', '1', '0.05', '2', '1', 'state'], env=dict(os.environ, J2='1', TIDE='195', LFIG='3', POLE='1', CASS='1', K2E='0.30', K2M='0.024', ACCIN=f'/tmp/acc_in_{d0}.txt'), capture_output=True, text=True, check=True).stdout.strip().split('\n')])
aE_m, aM_m = A[:, 1:4], A[:, 4:7]; aE_j, aM_j = ddt(S[3][:, 4:7]), ddt(S[4][:, 4:7])
rs = (S[3][:, 1:4] - S[0][:, 1:4])[sl]; rsh = rs / np.linalg.norm(rs, axis=1)[:, None]; a0s = GMS / (rs * rs).sum(1)
f1, f2 = 398600.435507 / (398600.435507 + 4902.800118), 4902.800118 / (398600.435507 + 4902.800118)
for name, aj, am in (('Earth alone', aE_j, aE_m[sl]), ('Earth-Moon barycentre', f1 * aE_j + f2 * aM_j, (f1 * aE_m + f2 * aM_m)[sl])):
    q = ((aj - am) * rsh).sum(1) / a0s * 1e10; tot = np.linalg.norm(aj - am, axis=1) / a0s * 1e10
    print(f'(b) {name}: barycentric acceleration, JPL - my model, along the Sun line, in 1e-10 of the Sun\'s attraction: mean {q.mean():+.3f}, rms {q.std():.3f};  whole residual rms {np.sqrt((tot ** 2).mean()):.3f}')
r = (S[4][:, 1:4] - S[3][:, 1:4])[sl]; rh = r / np.linalg.norm(r, axis=1)[:, None]; a0 = GMEM / (r * r).sum(1); q = (((aM_j - aE_j) - (aM_m - aE_m)[sl]) * rh).sum(1) / a0 * 1e10
print(f'    Moon minus Earth, along the Earth-Moon line, in 1e-10 of the mutual attraction: mean {q.mean():+.3f}, rms {q.std():.3f}')
# is the constant proportional to the Sun's potential at the Earth (it changes by 3.4% over the year) or a true constant?  compare the two epochs' means with (U + v^2/2)/c^2 and U/c^2
c2 = (299792.458 * D / AU) ** 2; vE = S[3][sl, 4:7] - S[0][sl, 4:7]; U = GMS / np.linalg.norm(rs, axis=1) / c2; K = (vE ** 2).sum(1) / (2 * c2)
print(f'    for scale: Sun\'s potential at the Earth / c^2 = {U.mean() * 1e10:.2f}e-10;  (U + v^2/2)/c^2 = {(U + K).mean() * 1e10:.2f}e-10;  3U/2c^2 = {1.5 * U.mean() * 1e10:.2f}e-10;  L_C = 148.08e-10;  L_B = 155.05e-10')
